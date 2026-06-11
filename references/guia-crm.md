# Guia de Integração com CRM — Pipedrive, HubSpot e RD Station CRM

Esta referência explica como a skill envia os prospects para o CRM escolhido, como usar `scripts/push_to_crm.py`, o que fazer quando a API falha, e o formato de CSV de import manual para cada CRM (fallback quando não há token configurado).

---

## 1. Visão geral do fluxo de push

1. A skill já gerou a lista de prospects (MD + CSV) com base no ICP e nos triggers.
2. Ler `config/crm-config.md` para saber: qual CRM, token/credenciais, pipeline/estágio destino, owner padrão, regra de duplicados.
3. Gerar `config/crm-config.json` (arquivo gerado automaticamente — nunca pedir ao usuário pra editar isso à mão) extraindo os valores preenchidos de `crm-config.md`. Estrutura:

```json
{
  "crm": "pipedrive",
  "pipedrive": {"domain": "acme", "api_token": "xxxx"},
  "hubspot": {"token": "pat-xxxx"},
  "rdstation": {"token": "xxxx"},
  "pipeline_name": "Outbound",
  "stage_name": "Novo Lead",
  "owner": "felipe@acme.com",
  "duplicate_strategy": "skip",
  "extra_tag": "prospeccao-trigger"
}
```

4. Rodar primeiro em **modo dry-run** (sem flag `--execute`) — o script mostra o que seria criado para cada prospect, sem chamar a API.
5. Mostrar o resultado do dry-run ao usuário em uma tabela curta (empresa, o que seria criado, possíveis duplicados detectados).
6. Só rodar com `--execute` após confirmação explícita do usuário.
7. Ler o relatório (`crm-push-result.json`) gerado pelo script e resumir: quantos criados, quantos pulados (duplicado), quantos falharam e por quê.

```bash
python3 scripts/push_to_crm.py --config config/crm-config.json --csv prospects-2026-06-11.csv --output crm-push-result.json
python3 scripts/push_to_crm.py --config config/crm-config.json --csv prospects-2026-06-11.csv --output crm-push-result.json --execute
```

O CSV de entrada é o mesmo gerado no fluxo de prospecção, com colunas: `empresa, setor, porte, trigger_type, trigger_descricao, urgencia, decisor_nome, decisor_cargo, decisor_linkedin, gancho, mensagem_inicial, data_pesquisa`.

---

## 2. Pipedrive

### Autenticação
API token pessoal, passado como query param `api_token` em toda requisição. Base URL: `https://{domain}.pipedrive.com/api/v1`.

### O que o script cria por prospect
1. **Organization** (`POST /organizations`) — nome = empresa
2. **Person** (`POST /persons`) — nome = decisor, vinculado à organization via `org_id`
3. **Deal** (`POST /deals`) — título = "[Empresa] — Prospecção", vinculado a `org_id` e `person_id`, no `pipeline_id`/`stage_id` resolvidos pelo nome configurado, `owner_id` resolvido pelo nome/email configurado
4. **Note** (`POST /notes`) — conteúdo = trigger + gancho + mensagem inicial, vinculado ao `deal_id`

### Resolução de pipeline/stage/owner
O script busca `GET /pipelines` e `GET /stages` e procura por nome (case-insensitive) igual ao configurado em `crm-config.md`. Para owner, busca `GET /users` e procura por nome ou email.

Se não encontrar pipeline, stage ou owner pelo nome configurado, o script para com erro claro listando as opções disponíveis — não adivinha.

### Verificação de duplicados
Antes de criar, busca `GET /organizations/search?term={empresa}` (e/ou `/itemSearch`). Se encontrar organization com nome igual ou muito parecido, aplica `duplicate_strategy`.

### Erros comuns
- `401`: token inválido ou domínio errado
- `403`: token sem permissão (verificar plano do Pipedrive — alguns endpoints exigem plano específico)
- `404` em pipeline/stage: nome não bate exatamente — confirme no Pipedrive (Configurações → Funil de vendas)

### Fallback CSV (import manual)
Se `crm` = "nenhum" ou a API falhar, gerar CSV no formato de import do Pipedrive (Organizations + Deals separados, conforme o importador do Pipedrive pede). Colunas mínimas:

`Organization - Name, Deal - Title, Deal - Value, Deal - Pipeline, Deal - Stage, Person - Name, Person - Email, Note`

---

## 3. HubSpot

### Autenticação
Private App Token (Bearer), formato `pat-xxxx`. Base URL: `https://api.hubapi.com`. Header: `Authorization: Bearer {token}`.

### O que o script cria por prospect
1. **Company** (`POST /crm/v3/objects/companies`) — `properties.name` = empresa
2. **Contact** (`POST /crm/v3/objects/contacts`) — `properties.firstname`/`lastname` = decisor, `jobtitle` = cargo
3. **Deal** (`POST /crm/v3/objects/deals`) — `properties.dealname`, `pipeline` e `dealstage` resolvidos via `GET /crm/v3/pipelines/deals` (procurar pelo `label` configurado e pegar o `id`)
4. **Associations** (`PUT /crm/v3/objects/deals/{dealId}/associations/default/companies/{companyId}` e `.../contacts/{contactId}`) — associa deal ↔ company ↔ contact
5. **Note** (`POST /crm/v3/objects/notes` + association ao deal) — trigger + gancho + mensagem

### Resolução de pipeline/stage
`GET /crm/v3/pipelines/deals` retorna pipelines com `label` e `stages` (cada stage com `label` e `id`). Buscar pelo `label` configurado (case-insensitive). Se não achar, parar com erro listando os pipelines/estágios disponíveis.

### Verificação de duplicados
`POST /crm/v3/objects/companies/search` filtrando por `name` igual ao da empresa. Se encontrar, aplica `duplicate_strategy`.

### Owner
`GET /crm/v3/owners` para resolver `owner` (nome/email) → `ownerId`, atribuído via `properties.hubspot_owner_id` no deal/contact.

### Erros comuns
- `401`: token inválido ou app sem os scopes necessários (ver `config/crm-config-template.md` 6.2)
- `429`: rate limit — o script já espera e tenta de novo (retry com backoff)

### Fallback CSV (import manual)
Formato compatível com o importador de CSV do HubSpot (uma linha por contato/empresa, HubSpot casa registros por nome de empresa no import). Colunas mínimas:

`Company name, Contact: First Name, Contact: Last Name, Contact: Job Title, Deal Name, Pipeline, Deal Stage, Notes`

---

## 4. RD Station CRM

> Atenção: **RD Station CRM** (funil de vendas / antigo Plug CRM) é um produto diferente do **RD Station Marketing**. Confirme com o usuário qual produto ele usa antes de configurar — as APIs são completamente diferentes.

### Autenticação
Token de API passado como query param `token`. Base URL: `https://crm.rdstation.com/api/v1`.

### O que o script cria por prospect
1. **Organization** (`POST /organizations`) — nome = empresa
2. **Contact** (`POST /contacts`) — nome = decisor, cargo = `job_title`, vinculado à organization
3. **Deal** (`POST /deals`) — `name`, `organization` (id), `contacts` (ids), `deal_stage_id` resolvido pelo nome do estágio configurado, `deal_source` = "Prospecção automática" (ou o valor de `extra_tag`)
4. **Task/Note** — RD Station CRM trata anotações como `deals/{id}/tasks` ou `deals/{id}/notes` dependendo da versão da API; o script tenta `notes` primeiro e cai para `tasks` (tipo "Anotação") se não disponível

### Resolução de pipeline/stage
`GET /deal_pipelines` retorna funis com `deal_stages` (cada um com `name` e `id`). Buscar pelo nome configurado.

### Owner
`GET /users` para resolver `owner` (nome/email) → `user_id`.

### Erros comuns
- `401`: token inválido
- `422`: campo obrigatório faltando (RD Station CRM costuma exigir `organization` e `deal_stage_id` para criar deal)

### Fallback CSV (import manual)
RD Station CRM não tem importador de CSV nativo tão flexível quanto Pipedrive/HubSpot — para fallback, gerar CSV genérico e instruir o usuário a importar via **Configurações → Importar dados** ou cadastrar manualmente os prospects de prioridade alta (geralmente poucos, 2-5 por rodada).

`Empresa, Contato, Cargo, Funil, Estágio, Origem, Anotação`

---

## 5. Quando NÃO há CRM configurado ("Nenhum")

Pular toda a etapa de push. Entregar apenas MD + CSV (fluxo padrão da prospecção) e, no resumo final, mencionar: "Para enviar esses prospects automaticamente pro CRM, complete o Bloco 6 em `config/crm-config.md`."

---

## 6. Segurança e boas práticas

- Nunca imprimir o token completo em logs, mensagens ou no `crm-push-result.json` — mascarar (`pat-****1234`).
- Nunca commitar/compartilhar `config/crm-config.json` ou `config/crm-config.md` preenchido — são pessoais por usuário.
- Sempre rodar dry-run antes de `--execute`. Push em massa sem revisão pode poluir o CRM com duplicatas.
- Respeitar `duplicate_strategy` — o padrão recomendado é "skip" (pular duplicados).
- Se a API retornar erro em um prospect específico, não interromper o lote inteiro — registrar o erro no relatório e seguir para o próximo.
