#!/usr/bin/env python3
"""
push_to_crm.py — Envia uma lista de prospects (CSV gerado pela skill prospeccao-multi-crm)
para o CRM configurado (Pipedrive, HubSpot ou RD Station CRM).

Uso:
    # Dry-run (padrao) - mostra o que seria criado, sem chamar a API
    python3 push_to_crm.py --config config/crm-config.json --csv prospects.csv --output crm-push-result.json

    # Execucao real - cria organizations/companies, contatos e deals no CRM
    python3 push_to_crm.py --config config/crm-config.json --csv prospects.csv --output crm-push-result.json --execute

CSV de entrada esperado (colunas geradas pelo fluxo de prospeccao):
    empresa, setor, porte, trigger_type, trigger_descricao, urgencia, decisor_nome,
    decisor_cargo, decisor_linkedin, gancho, mensagem_inicial, data_pesquisa

config/crm-config.json esperado:
{
  "crm": "pipedrive" | "hubspot" | "rdstation" | "none",
  "pipedrive": {"domain": "...", "api_token": "..."},
  "hubspot": {"token": "..."},
  "rdstation": {"token": "..."},
  "pipeline_name": "...",
  "stage_name": "...",
  "owner": "...",
  "duplicate_strategy": "skip" | "create" | "ask",
  "extra_tag": "..."
}
"""

import argparse
import csv
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def mask_token(token):
    if not token or len(token) < 8:
        return "****"
    return f"{token[:4]}{'*' * (len(token) - 8)}{token[-4:]}"


def http_request(method, url, headers=None, params=None, json_body=None, retries=3):
    """Minimal HTTP client using stdlib only (no extra dependencies needed)."""
    if params:
        sep = "&" if "?" in url else "?"
        url = url + sep + urllib.parse.urlencode(params)

    data = None
    headers = dict(headers or {})
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return resp.status, (json.loads(body) if body else {})
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            try:
                parsed = json.loads(body) if body else {}
            except json.JSONDecodeError:
                parsed = {"raw": body}
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return e.code, parsed
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return 0, {"error": str(e.reason)}


def read_prospects(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Pipedrive
# ---------------------------------------------------------------------------

class PipedriveClient:
    def __init__(self, cfg):
        self.domain = cfg["pipedrive"]["domain"]
        self.token = cfg["pipedrive"]["api_token"]
        self.base = f"https://{self.domain}.pipedrive.com/api/v1"
        self.pipeline_name = cfg.get("pipeline_name")
        self.stage_name = cfg.get("stage_name")
        self.owner_name = cfg.get("owner")
        self._pipeline_id = None
        self._stage_id = None
        self._owner_id = None

    def _params(self, extra=None):
        p = {"api_token": self.token}
        if extra:
            p.update(extra)
        return p

    def resolve_targets(self):
        """Resolve pipeline, stage and owner names to IDs. Raises ValueError with
        a helpful message (listing available options) if not found."""
        status, data = http_request("GET", f"{self.base}/pipelines", params=self._params())
        if status != 200:
            raise ValueError(f"Erro ao buscar pipelines do Pipedrive: {data}")
        pipelines = data.get("data") or []
        match = next((p for p in pipelines if p["name"].lower() == (self.pipeline_name or "").lower()), None)
        if not match:
            names = [p["name"] for p in pipelines]
            raise ValueError(
                f"Pipeline '{self.pipeline_name}' nao encontrado no Pipedrive. "
                f"Pipelines disponiveis: {names}"
            )
        self._pipeline_id = match["id"]

        status, data = http_request("GET", f"{self.base}/stages",
                                      params=self._params({"pipeline_id": self._pipeline_id}))
        if status != 200:
            raise ValueError(f"Erro ao buscar estagios do Pipedrive: {data}")
        stages = data.get("data") or []
        match = next((s for s in stages if s["name"].lower() == (self.stage_name or "").lower()), None)
        if not match:
            names = [s["name"] for s in stages]
            raise ValueError(
                f"Estagio '{self.stage_name}' nao encontrado no pipeline '{self.pipeline_name}'. "
                f"Estagios disponiveis: {names}"
            )
        self._stage_id = match["id"]

        if self.owner_name:
            status, data = http_request("GET", f"{self.base}/users", params=self._params())
            if status == 200:
                users = data.get("data") or []
                match = next(
                    (u for u in users
                     if self.owner_name.lower() in (u.get("name", "").lower(), u.get("email", "").lower())),
                    None,
                )
                if match:
                    self._owner_id = match["id"]

    def find_existing_org(self, name):
        status, data = http_request("GET", f"{self.base}/organizations/search",
                                      params=self._params({"term": name, "exact_match": "false"}))
        if status != 200:
            return None
        items = (data.get("data") or {}).get("items") or []
        for item in items:
            org = item.get("item", {})
            if org.get("name", "").strip().lower() == name.strip().lower():
                return org
        return None

    def create_prospect(self, row, dry_run, duplicate_strategy, extra_tag):
        empresa = row["empresa"]
        result = {"empresa": empresa, "actions": [], "status": "ok", "error": None}

        existing = self.find_existing_org(empresa)
        if existing:
            if duplicate_strategy == "skip":
                result["status"] = "skipped_duplicate"
                result["actions"].append(f"Organization '{empresa}' ja existe (id={existing['id']}) - pulado")
                return result
            result["actions"].append(f"AVISO: Organization '{empresa}' ja existe (id={existing['id']}) - criando mesmo assim")

        if dry_run:
            result["actions"] = [
                f"[dry-run] Criaria Organization '{empresa}'",
                f"[dry-run] Criaria Person '{row.get('decisor_nome') or '(sem nome)'}' ({row.get('decisor_cargo','')}) vinculado a organization",
                f"[dry-run] Criaria Deal '{empresa} — Prospeccao' no pipeline '{self.pipeline_name}' / estagio '{self.stage_name}'"
                + (f" / owner '{self.owner_name}'" if self.owner_name else ""),
                f"[dry-run] Adicionaria nota com trigger e mensagem inicial",
            ]
            return result

        # 1. Organization
        org_payload = {"name": empresa}
        status, data = http_request("POST", f"{self.base}/organizations",
                                      params=self._params(), json_body=org_payload)
        if status not in (200, 201):
            result["status"] = "error"
            result["error"] = f"Falha ao criar organization: {data}"
            return result
        org_id = data["data"]["id"]
        result["actions"].append(f"Organization criada (id={org_id})")

        # 2. Person
        person_id = None
        if row.get("decisor_nome"):
            person_payload = {"name": row["decisor_nome"], "org_id": org_id}
            status, data = http_request("POST", f"{self.base}/persons",
                                          params=self._params(), json_body=person_payload)
            if status in (200, 201):
                person_id = data["data"]["id"]
                result["actions"].append(f"Person criada (id={person_id})")
            else:
                result["actions"].append(f"AVISO: falha ao criar person: {data}")

        # 3. Deal
        deal_payload = {
            "title": f"{empresa} — Prospeccao",
            "org_id": org_id,
            "pipeline_id": self._pipeline_id,
            "stage_id": self._stage_id,
        }
        if person_id:
            deal_payload["person_id"] = person_id
        if self._owner_id:
            deal_payload["user_id"] = self._owner_id
        status, data = http_request("POST", f"{self.base}/deals",
                                      params=self._params(), json_body=deal_payload)
        if status not in (200, 201):
            result["status"] = "error"
            result["error"] = f"Falha ao criar deal: {data}"
            return result
        deal_id = data["data"]["id"]
        result["actions"].append(f"Deal criado (id={deal_id})")

        # 4. Note
        note_lines = [
            f"Trigger ({row.get('trigger_type','')}): {row.get('trigger_descricao','')}",
            f"Urgencia: {row.get('urgencia','')}",
            f"Gancho: {row.get('gancho','')}",
            "",
            "Mensagem inicial sugerida:",
            row.get("mensagem_inicial", ""),
        ]
        if extra_tag:
            note_lines.insert(0, f"Origem: {extra_tag}")
        note_payload = {"content": "\n".join(note_lines), "deal_id": deal_id}
        status, data = http_request("POST", f"{self.base}/notes",
                                      params=self._params(), json_body=note_payload)
        if status in (200, 201):
            result["actions"].append("Nota adicionada ao deal")
        else:
            result["actions"].append(f"AVISO: falha ao adicionar nota: {data}")

        return result


# ---------------------------------------------------------------------------
# HubSpot
# ---------------------------------------------------------------------------

class HubSpotClient:
    def __init__(self, cfg):
        self.token = cfg["hubspot"]["token"]
        self.base = "https://api.hubapi.com"
        self.pipeline_name = cfg.get("pipeline_name")
        self.stage_name = cfg.get("stage_name")
        self.owner_name = cfg.get("owner")
        self._pipeline_id = None
        self._stage_id = None
        self._owner_id = None

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def resolve_targets(self):
        status, data = http_request("GET", f"{self.base}/crm/v3/pipelines/deals", headers=self._headers())
        if status != 200:
            raise ValueError(f"Erro ao buscar pipelines do HubSpot: {data}")
        pipelines = data.get("results") or []
        match = next((p for p in pipelines if p["label"].lower() == (self.pipeline_name or "").lower()), None)
        if not match:
            labels = [p["label"] for p in pipelines]
            raise ValueError(
                f"Pipeline '{self.pipeline_name}' nao encontrado no HubSpot. "
                f"Pipelines disponiveis: {labels}"
            )
        self._pipeline_id = match["id"]
        stages = match.get("stages") or []
        stage_match = next((s for s in stages if s["label"].lower() == (self.stage_name or "").lower()), None)
        if not stage_match:
            labels = [s["label"] for s in stages]
            raise ValueError(
                f"Estagio '{self.stage_name}' nao encontrado no pipeline '{self.pipeline_name}'. "
                f"Estagios disponiveis: {labels}"
            )
        self._stage_id = stage_match["id"]

        if self.owner_name:
            status, data = http_request("GET", f"{self.base}/crm/v3/owners", headers=self._headers())
            if status == 200:
                owners = data.get("results") or []
                match = next(
                    (o for o in owners
                     if self.owner_name.lower() in (o.get("email", "").lower(),
                                                      f"{o.get('firstName','')} {o.get('lastName','')}".strip().lower())),
                    None,
                )
                if match:
                    self._owner_id = match["id"]

    def find_existing_company(self, name):
        body = {
            "filterGroups": [{"filters": [{"propertyName": "name", "operator": "EQ", "value": name}]}],
            "limit": 1,
        }
        status, data = http_request("POST", f"{self.base}/crm/v3/objects/companies/search",
                                      headers=self._headers(), json_body=body)
        if status != 200:
            return None
        results = data.get("results") or []
        return results[0] if results else None

    def create_prospect(self, row, dry_run, duplicate_strategy, extra_tag):
        empresa = row["empresa"]
        result = {"empresa": empresa, "actions": [], "status": "ok", "error": None}

        existing = self.find_existing_company(empresa)
        if existing:
            if duplicate_strategy == "skip":
                result["status"] = "skipped_duplicate"
                result["actions"].append(f"Company '{empresa}' ja existe (id={existing['id']}) - pulado")
                return result
            result["actions"].append(f"AVISO: Company '{empresa}' ja existe (id={existing['id']}) - criando mesmo assim")

        if dry_run:
            result["actions"] = [
                f"[dry-run] Criaria Company '{empresa}'",
                f"[dry-run] Criaria Contact '{row.get('decisor_nome') or '(sem nome)'}' ({row.get('decisor_cargo','')})",
                f"[dry-run] Criaria Deal '{empresa} — Prospeccao' no pipeline '{self.pipeline_name}' / estagio '{self.stage_name}'"
                + (f" / owner '{self.owner_name}'" if self.owner_name else ""),
                "[dry-run] Associaria company <-> contact <-> deal e adicionaria nota",
            ]
            return result

        # 1. Company
        status, data = http_request("POST", f"{self.base}/crm/v3/objects/companies",
                                      headers=self._headers(), json_body={"properties": {"name": empresa}})
        if status not in (200, 201):
            result["status"] = "error"
            result["error"] = f"Falha ao criar company: {data}"
            return result
        company_id = data["id"]
        result["actions"].append(f"Company criada (id={company_id})")

        # 2. Contact
        contact_id = None
        nome = row.get("decisor_nome", "").strip()
        if nome:
            partes = nome.split(" ", 1)
            firstname = partes[0]
            lastname = partes[1] if len(partes) > 1 else ""
            contact_props = {"firstname": firstname, "lastname": lastname}
            if row.get("decisor_cargo"):
                contact_props["jobtitle"] = row["decisor_cargo"]
            status, data = http_request("POST", f"{self.base}/crm/v3/objects/contacts",
                                          headers=self._headers(), json_body={"properties": contact_props})
            if status in (200, 201):
                contact_id = data["id"]
                result["actions"].append(f"Contact criado (id={contact_id})")
            else:
                result["actions"].append(f"AVISO: falha ao criar contact: {data}")

        # 3. Deal
        deal_props = {
            "dealname": f"{empresa} — Prospeccao",
            "pipeline": self._pipeline_id,
            "dealstage": self._stage_id,
        }
        if self._owner_id:
            deal_props["hubspot_owner_id"] = self._owner_id
        status, data = http_request("POST", f"{self.base}/crm/v3/objects/deals",
                                      headers=self._headers(), json_body={"properties": deal_props})
        if status not in (200, 201):
            result["status"] = "error"
            result["error"] = f"Falha ao criar deal: {data}"
            return result
        deal_id = data["id"]
        result["actions"].append(f"Deal criado (id={deal_id})")

        # 4. Associations (deal <-> company, deal <-> contact)
        for obj_type, obj_id in (("companies", company_id), ("contacts", contact_id)):
            if not obj_id:
                continue
            status, _ = http_request(
                "PUT",
                f"{self.base}/crm/v3/objects/deals/{deal_id}/associations/default/{obj_type}/{obj_id}",
                headers=self._headers(),
            )
            if status in (200, 201, 204):
                result["actions"].append(f"Deal associado a {obj_type[:-1]} (id={obj_id})")
            else:
                result["actions"].append(f"AVISO: falha ao associar deal a {obj_type[:-1]}")

        # 5. Note
        note_lines = [
            f"Trigger ({row.get('trigger_type','')}): {row.get('trigger_descricao','')}",
            f"Urgencia: {row.get('urgencia','')}",
            f"Gancho: {row.get('gancho','')}",
            "",
            "Mensagem inicial sugerida:",
            row.get("mensagem_inicial", ""),
        ]
        if extra_tag:
            note_lines.insert(0, f"Origem: {extra_tag}")
        note_body = {
            "properties": {"hs_note_body": "\n".join(note_lines), "hs_timestamp": str(int(time.time() * 1000))},
            "associations": [{
                "to": {"id": deal_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 214}],
            }],
        }
        status, data = http_request("POST", f"{self.base}/crm/v3/objects/notes",
                                      headers=self._headers(), json_body=note_body)
        if status in (200, 201):
            result["actions"].append("Nota adicionada e associada ao deal")
        else:
            result["actions"].append(f"AVISO: falha ao adicionar nota: {data}")

        return result


# ---------------------------------------------------------------------------
# RD Station CRM
# ---------------------------------------------------------------------------

class RDStationClient:
    def __init__(self, cfg):
        self.token = cfg["rdstation"]["token"]
        self.base = "https://crm.rdstation.com/api/v1"
        self.pipeline_name = cfg.get("pipeline_name")
        self.stage_name = cfg.get("stage_name")
        self.owner_name = cfg.get("owner")
        self._stage_id = None
        self._owner_id = None

    def _params(self, extra=None):
        p = {"token": self.token}
        if extra:
            p.update(extra)
        return p

    def resolve_targets(self):
        status, data = http_request("GET", f"{self.base}/deal_pipelines", params=self._params())
        if status != 200:
            raise ValueError(f"Erro ao buscar funis do RD Station CRM: {data}")
        pipelines = data if isinstance(data, list) else data.get("deal_pipelines", [])
        match = next((p for p in pipelines if p["name"].lower() == (self.pipeline_name or "").lower()), None)
        if not match:
            names = [p["name"] for p in pipelines]
            raise ValueError(
                f"Funil '{self.pipeline_name}' nao encontrado no RD Station CRM. "
                f"Funis disponiveis: {names}"
            )
        stages = match.get("deal_stages") or []
        stage_match = next((s for s in stages if s["name"].lower() == (self.stage_name or "").lower()), None)
        if not stage_match:
            names = [s["name"] for s in stages]
            raise ValueError(
                f"Estagio '{self.stage_name}' nao encontrado no funil '{self.pipeline_name}'. "
                f"Estagios disponiveis: {names}"
            )
        self._stage_id = stage_match["id"]

        if self.owner_name:
            status, data = http_request("GET", f"{self.base}/users", params=self._params())
            if status == 200:
                users = data if isinstance(data, list) else data.get("users", [])
                match = next(
                    (u for u in users
                     if self.owner_name.lower() in (u.get("email", "").lower(), u.get("name", "").lower())),
                    None,
                )
                if match:
                    self._owner_id = match["id"]

    def find_existing_org(self, name):
        status, data = http_request("GET", f"{self.base}/organizations", params=self._params({"name": name}))
        if status != 200:
            return None
        orgs = data if isinstance(data, list) else data.get("organizations", [])
        for org in orgs:
            if org.get("name", "").strip().lower() == name.strip().lower():
                return org
        return None

    def create_prospect(self, row, dry_run, duplicate_strategy, extra_tag):
        empresa = row["empresa"]
        result = {"empresa": empresa, "actions": [], "status": "ok", "error": None}

        existing = self.find_existing_org(empresa)
        if existing:
            if duplicate_strategy == "skip":
                result["status"] = "skipped_duplicate"
                result["actions"].append(f"Organization '{empresa}' ja existe (id={existing['id']}) - pulado")
                return result
            result["actions"].append(f"AVISO: Organization '{empresa}' ja existe (id={existing['id']}) - criando mesmo assim")

        if dry_run:
            result["actions"] = [
                f"[dry-run] Criaria Organization '{empresa}'",
                f"[dry-run] Criaria Contact '{row.get('decisor_nome') or '(sem nome)'}' ({row.get('decisor_cargo','')})",
                f"[dry-run] Criaria Deal '{empresa} — Prospeccao' no estagio '{self.stage_name}'"
                + (f" / owner '{self.owner_name}'" if self.owner_name else ""),
                "[dry-run] Adicionaria nota com trigger e mensagem inicial",
            ]
            return result

        # 1. Organization
        status, data = http_request("POST", f"{self.base}/organizations",
                                      params=self._params(), json_body={"name": empresa})
        if status not in (200, 201):
            result["status"] = "error"
            result["error"] = f"Falha ao criar organization: {data}"
            return result
        org_id = data["id"]
        result["actions"].append(f"Organization criada (id={org_id})")

        # 2. Contact
        contact_id = None
        if row.get("decisor_nome"):
            contact_payload = {
                "name": row["decisor_nome"],
                "title": row.get("decisor_cargo", ""),
                "organization_id": org_id,
            }
            status, data = http_request("POST", f"{self.base}/contacts",
                                          params=self._params(), json_body=contact_payload)
            if status in (200, 201):
                contact_id = data["id"]
                result["actions"].append(f"Contact criado (id={contact_id})")
            else:
                result["actions"].append(f"AVISO: falha ao criar contact: {data}")

        # 3. Deal
        note_lines = [
            f"Trigger ({row.get('trigger_type','')}): {row.get('trigger_descricao','')}",
            f"Urgencia: {row.get('urgencia','')}",
            f"Gancho: {row.get('gancho','')}",
            "",
            "Mensagem inicial sugerida:",
            row.get("mensagem_inicial", ""),
        ]
        if extra_tag:
            note_lines.insert(0, f"Origem: {extra_tag}")

        deal_payload = {
            "name": f"{empresa} — Prospeccao",
            "organization": {"id": org_id},
            "deal_stage_id": self._stage_id,
        }
        if contact_id:
            deal_payload["contacts"] = [{"id": contact_id}]
        if self._owner_id:
            deal_payload["user_id"] = self._owner_id
        status, data = http_request("POST", f"{self.base}/deals",
                                      params=self._params(), json_body=deal_payload)
        if status not in (200, 201):
            result["status"] = "error"
            result["error"] = f"Falha ao criar deal: {data}"
            return result
        deal_id = data["id"]
        result["actions"].append(f"Deal criado (id={deal_id})")

        # 4. Note (best-effort: tenta /notes, depois /tasks)
        status, _ = http_request("POST", f"{self.base}/deals/{deal_id}/notes",
                                  params=self._params(), json_body={"text": "\n".join(note_lines)})
        if status in (200, 201):
            result["actions"].append("Nota adicionada ao deal")
        else:
            result["actions"].append("AVISO: nao foi possivel adicionar nota automaticamente — adicione manualmente")

        return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CLIENTS = {
    "pipedrive": PipedriveClient,
    "hubspot": HubSpotClient,
    "rdstation": RDStationClient,
}


def main():
    parser = argparse.ArgumentParser(description="Envia prospects para o CRM configurado.")
    parser.add_argument("--config", required=True, help="Caminho para config/crm-config.json")
    parser.add_argument("--csv", required=True, help="CSV de prospects gerado pela skill")
    parser.add_argument("--output", required=True, help="Onde salvar o relatorio JSON")
    parser.add_argument("--execute", action="store_true", help="Executa de verdade (default = dry-run)")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)

    crm = cfg.get("crm", "none")
    duplicate_strategy = cfg.get("duplicate_strategy", "skip")
    extra_tag = cfg.get("extra_tag", "")

    if crm == "none":
        print("CRM configurado como 'none' — nada a enviar. Use o CSV/MD gerado para import manual.")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"crm": "none", "results": []}, f, ensure_ascii=False, indent=2)
        return

    if crm not in CLIENTS:
        print(f"ERRO: CRM '{crm}' desconhecido. Opcoes: {list(CLIENTS.keys())} ou 'none'.", file=sys.stderr)
        sys.exit(1)

    client = CLIENTS[crm](cfg)

    try:
        client.resolve_targets()
    except ValueError as e:
        print(f"ERRO de configuracao: {e}", file=sys.stderr)
        sys.exit(1)

    rows = read_prospects(args.csv)
    dry_run = not args.execute
    mode = "DRY-RUN (nada sera criado)" if dry_run else "EXECUCAO REAL"
    print(f"Modo: {mode} | CRM: {crm} | {len(rows)} prospects no CSV")

    results = []
    for row in rows:
        res = client.create_prospect(row, dry_run, duplicate_strategy, extra_tag)
        results.append(res)
        status_label = {"ok": "OK", "skipped_duplicate": "PULADO (duplicado)", "error": "ERRO"}.get(res["status"], res["status"])
        print(f"- {res['empresa']}: {status_label}")
        for action in res["actions"]:
            print(f"    {action}")
        if res["error"]:
            print(f"    ERRO: {res['error']}")

    summary = {
        "crm": crm,
        "dry_run": dry_run,
        "total": len(results),
        "created": sum(1 for r in results if r["status"] == "ok"),
        "skipped_duplicates": sum(1 for r in results if r["status"] == "skipped_duplicate"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "results": results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(
        f"\nResumo: {summary['created']} criados, {summary['skipped_duplicates']} pulados (duplicado), "
        f"{summary['errors']} com erro. Relatorio salvo em {args.output}"
    )


if __name__ == "__main__":
    main()
