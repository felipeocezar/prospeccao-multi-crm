---
name: prospeccao-multi-crm
description: |
  Pesquisa prospects B2B qualificados com base em trigger events reais, dentro do ICP de CADA usuario, e envia os leads priorizados direto para o CRM que o usuario escolher (Pipedrive, HubSpot ou RD Station CRM). Use SEMPRE que o usuario mencionar "me traz prospects", "pesquisa empresas do setor X", "quero prospectar", "lista de prospects", "quem eu deveria prospectar", "empresas que acabaram de receber funding", "acha empresas contratando", "novas empresas pra minha cadencia", "preciso de leads novos", "monta lista de prospeccao", "acha decision makers no setor X", "manda esses prospects pro pipedrive/hubspot/rd station", "cria os leads no crm", "sobe essa lista pro funil", "joga os prospects no meu funil", "configura minha prospeccao", ou qualquer variacao envolvendo encontrar novas empresas/contatos para pipeline comercial e (opcionalmente) registra-los automaticamente no CRM. Na primeira execucao, conduz uma configuracao guiada do ICP e do CRM de destino — cada usuario configura o proprio.
---

# Prospecção Multi-CRM — Trigger-Based Prospecting com Push Automático pro CRM

Versão configurável e compartilhável da prospecção trigger-based: cada pessoa que instala esta skill configura o próprio ICP, cargos-alvo, tom de voz e o CRM onde os leads devem cair (Pipedrive, HubSpot ou RD Station CRM). Tudo fica salvo localmente na pasta da skill de cada usuário — nada é compartilhado entre pessoas.

Transforma prospecção de "spray and pray" em inteligência de mercado acionável. Dados reais: prospecção genérica tem 1-2% de taxa de resposta (Gong, 30k emails). Prospecção trigger-based sobe para 12-18% — até 400% mais conversão. O diferencial: cada prospect vem com o PORQUÊ — qual trigger event justifica o contato agora — e, se configurado, já entra no CRM pronto para o vendedor trabalhar.

## Quando usar

Dispare esta skill quando o usuário precisar de novos prospects para o pipeline, com ou sem pedido explícito de envio ao CRM. Não precisa dizer "prospecção" — se mencionar "preciso de mais pipeline", "topo do funil tá fraco", "quem eu deveria abordar essa semana", ou "sobe esses leads pro CRM", a skill entra.

**NÃO use esta skill para:**
- Follow-up de deals existentes (use skill follow-up-inteligente)
- Análise de pipeline ou forecast (use skill reuniao-de-forecast)
- Atualizar deals existentes a partir de transcrições de call (use skill crm-updater)
- Pesquisa de um prospect específico já identificado (pesquisa ad-hoc normal)
- Enriquecimento de lista existente sem trigger (isso é data append, não prospecção)

## Fluxo de execução

### Passo 0: Checar configuração

Verificar se existem `config/business-profile.md` e `config/crm-config.md`, e se ambos estão preenchidos (sem `[A PREENCHER]` pendente nos campos essenciais). Se algum não existir ou estiver incompleto, entrar em **Modo Configuração** para a parte que falta.

Isso significa que dois colegas usando a mesma skill podem ter ICPs e CRMs completamente diferentes — cada um configura o próprio na primeira vez que usa.

### Modo Configuração (primeiro uso)

A skill ainda não sabe o ICP, os cargos-alvo, os triggers que importam, nem onde os leads devem cair. Conduzir entrevista em 6 blocos curtos (3-4 perguntas cada), salvando progressivamente.

**Blocos 1-5 (ICP, cargos, proposta de valor, triggers, tom de voz):** ler `config/business-profile-template.md` para a estrutura completa e salvar em `config/business-profile.md`.

**Reaproveitamento:** se o usuário já tem config das skills `apresentacao-de-vendas`, `proposta-automatica` ou da `prospeccao` original, boa parte do ICP e proposta de valor pode ser reaproveitada. Perguntar: "Vi que você já tem config de [skill]. Quer que eu importe os dados de lá e só complete o que falta?"

**Bloco 6 (CRM de destino):** ler `config/crm-config-template.md` e salvar em `config/crm-config.md`. Conduzir assim:

1. Perguntar qual CRM o usuário usa: Pipedrive, HubSpot, RD Station CRM, ou nenhum (só quer MD/CSV).
2. Explicar de onde tirar o token de API daquele CRM especificamente (instruções estão no template, seção 6.2 de cada CRM).
3. **IMPORTANTE — segurança:** pedir para o usuário preencher o token **diretamente no arquivo `config/crm-config.md`**, não colar o token no chat. Se o usuário colar o token na conversa mesmo assim, usar normalmente para esta sessão mas recomendar que ele mova para o arquivo e, se possível, gere um token novo depois (boa prática quando um segredo passa por chat).
4. Perguntar pipeline/funil e estágio onde os novos leads devem entrar — usar os nomes exatamente como aparecem no CRM do usuário.
5. Perguntar quem deve ser o responsável (owner) padrão dos novos leads.
6. Perguntar a estratégia de duplicados (recomendar "skip").

Se o usuário escolher "nenhum CRM", pular o resto do Bloco 6 — a skill vai gerar apenas MD/CSV (igual ao fluxo padrão de prospecção).

### Modo Execução

Com config carregado, coletar o pedido:

**Input típico (1 turno):**
1. Quantos prospects? (default: 10)
2. Algum filtro específico? (setor, região, porte — ou "usa meu ICP padrão")
3. Tipo de trigger prioritário? (ou "qualquer trigger recente")
4. Enviar pro CRM ou só gerar a lista? (se o usuário não especificar e tiver CRM configurado, perguntar; se não tiver CRM configurado, gerar só a lista)

Se o usuário já deu contexto ("me traz 10 prospects de logística que receberam funding e já manda pro pipedrive"), extrair de lá sem perguntar de novo.

### Pesquisar triggers via web_search

Ler `references/frameworks-prospeccao.md` para a taxonomia completa de triggers e o scoring de urgência.

Executar pesquisas estruturadas por tipo de trigger:

1. **Funding/M&A:** "[setor] + funding round 2025 2026 Brasil" ou equivalente
2. **Hiring:** "[setor] + contratando + [cargo] + [região]"
3. **Leadership change:** "[setor] + novo CEO/VP/diretor + [região]"
4. **Expansão:** "[setor] + nova unidade/filial + [região]"
5. **Tech change:** "[setor] + implementando/migrando + [tecnologia relevante]"
6. **Notícia relevante:** "[setor] + [keyword do ICP] + notícia recente"

Fazer 3-5 buscas complementares para cobrir os triggers configurados. Não fazer 15 buscas — cada busca deve ter alvo claro.

### Filtrar e validar contra ICP

Para cada empresa encontrada:

1. Confirmar que encaixa no ICP (setor, porte, geografia)
2. Verificar se o trigger é de fato recente (últimos 90 dias)
3. Identificar o decisor mais provável (cargo-alvo do config)
4. Classificar urgência do trigger:

| Urgência | Prazo de ação | Exemplos de trigger |
|---|---|---|
| **Alta** (contatar em 24h) | Janela curta, concorrentes também viram | Funding anunciado, novo C-level nomeado, M&A |
| **Média** (contatar em 72h) | Relevante mas menos perecível | Hiring de equipe, mudança de tech stack, expansão |
| **Baixa** (contatar em 7d) | Contexto útil mas sem urgência imediata | Notícia de setor, relatório publicado, evento do setor |

### Gerar lista priorizada

Para cada prospect, montar ficha:

```
EMPRESA: [Nome]
SETOR: [Setor] | PORTE: [Estimativa de funcionários/faturamento]
TRIGGER: [O que aconteceu] — [Fonte] — [Data]
URGÊNCIA: [Alta/Média/Baixa]
DECISOR SUGERIDO: [Nome + Cargo] — LinkedIn: [URL se encontrado]
POR QUE PROSPECTAR AGORA: [1-2 frases explicando o PORQUÊ — trigger + fit com ICP + valor que você entrega]
GANCHO: [1 frase de abertura personalizada vinculando trigger ao valor]
```

Ordenar por: Urgência (Alta primeiro) → Fit com ICP → Recência do trigger.

### Gerar mensagem inicial personalizada

Ler `references/templates-mensagens.md` para os templates por trigger type e canal.

Para cada prospect dos top 5-10, gerar mensagem personalizada em 1 canal (email por default, ou o canal configurado). A mensagem segue a estrutura:

1. **Gancho** (referência ao trigger — mostra que você pesquisou)
2. **Ponte** (conexão entre trigger e uma dor que o prospect provavelmente sente)
3. **Valor** (o que você resolve, não o que você vende)
4. **CTA** (pergunta leve, não convite para demo)

### Gerar arquivos da lista

Gerar 2 arquivos, sempre — mesmo quando o push pro CRM acontece, eles servem de registro/auditoria:

**Arquivo 1 — Tabela legível (markdown):**
Tabela com: Empresa | Setor | Porte | Trigger | Urgência | Decisor | Gancho

**Arquivo 2 — CSV:**
Colunas: `empresa, setor, porte, trigger_type, trigger_descricao, urgencia, decisor_nome, decisor_cargo, decisor_linkedin, gancho, mensagem_inicial, data_pesquisa`

Salvar em:
- `/mnt/user-data/outputs/prospects-[data].md`
- `/mnt/user-data/outputs/prospects-[data].csv`

### Push para o CRM (se configurado)

Se `config/crm-config.md` tem um CRM configurado (diferente de "nenhum") e o usuário quer enviar:

1. Ler `references/guia-crm.md` — tem todos os detalhes de API, payloads e tratamento de erro por CRM (Pipedrive, HubSpot, RD Station CRM).
2. Gerar `config/crm-config.json` a partir dos valores preenchidos em `config/crm-config.md` (arquivo intermediário, gerado automaticamente).
3. Rodar `scripts/push_to_crm.py` em **modo dry-run primeiro** (sem `--execute`):
   ```bash
   python3 scripts/push_to_crm.py --config config/crm-config.json --csv prospects-[data].csv --output crm-push-result.json
   ```
4. Mostrar ao usuário o que seria criado (organizations/companies, contatos, deals, em qual pipeline/estágio) e quaisquer duplicados detectados.
5. **Pedir confirmação explícita** antes de rodar com `--execute`.
6. Após confirmação, rodar com `--execute` e ler `crm-push-result.json` para o resumo final.

Se o push falhar (token inválido, pipeline não encontrado, etc.), o erro vem com instrução clara do que corrigir em `config/crm-config.md` — explicar isso ao usuário em vez de tentar adivinhar.

Se não houver CRM configurado, mencionar no resumo final: "Quer que eu configure o envio automático pro seu CRM? É só completar o Bloco 6 da configuração."

### Entregar resultado

Entregar MD + CSV via `present_files`.

Resumo inline cobrindo: "Encontrei X prospects com trigger ativo. Y de urgência alta (contatar em 24h). O trigger mais quente é [resumo]." + (se houve push) "Z foram criados no [CRM], W pulados por já existirem, V com erro — [detalhes se houver erro]."

## Arquivos de referência

- `config/business-profile.md` — ICP, cargos, triggers, tom de voz (preenchido 1x por usuário)
- `config/business-profile-template.md` — template com perguntas dos blocos 1-5 do modo configuração
- `config/crm-config.md` — CRM escolhido, credenciais, pipeline/estágio, owner (preenchido 1x por usuário, NUNCA compartilhar)
- `config/crm-config-template.md` — template com perguntas do bloco 6 (CRM)
- `references/frameworks-prospeccao.md` — taxonomia de triggers, ICP scoring, metodologia de pesquisa
- `references/templates-mensagens.md` — templates de mensagem por trigger type e canal (email, LinkedIn, WhatsApp)
- `references/guia-crm.md` — detalhes de API, payloads, resolução de pipeline/estágio/owner e fallback CSV para Pipedrive, HubSpot e RD Station CRM
- `scripts/push_to_crm.py` — script que cria organizations/companies, contatos e deals no CRM configurado (dry-run por padrão)

## Exemplo de uso bom

**Usuário:** "Me traz 10 prospects do setor de logística que tiveram alguma movimentação recente e já sobe pro meu Pipedrive."

**Skill:**
1. Carrega `config/business-profile.md` — ICP = empresas B2B serviço, 50-500 func, Brasil. Triggers = funding, hiring, expansão
2. Carrega `config/crm-config.md` — CRM = Pipedrive, pipeline "Outbound", estágio "Novo Lead"
3. Pesquisa web: "[logística] + funding/expansão/contratando + 2026 + Brasil"
4. Encontra 14 empresas com trigger. Filtra contra ICP: 11 passam
5. Prioriza: 3 alta urgência, 5 média, 3 baixa. Gera lista de 10 com fichas completas
6. Gera mensagem inicial personalizada para os 5 top
7. Gera MD + CSV
8. Roda `push_to_crm.py` em dry-run, mostra o que seria criado no Pipedrive, usuário confirma
9. Roda com `--execute`. Resumo: "10 prospects com trigger ativo. 3 urgência alta. Criei 9 deals no Pipedrive (pipeline Outbound / Novo Lead) — 1 já existia e foi pulado."

## Exemplo de uso ruim (a evitar)

**Usuário:** "Me traz uma lista de empresas de tecnologia."

**Resposta ruim:** gerar lista genérica sem trigger, ou tentar enviar pro CRM sem configuração feita.

**Resposta certa:** "Posso pesquisar empresas de tecnologia, mas preciso de contexto pra entregar algo útil: qual porte? Qual região? E mais importante — que tipo de evento recente te interessa? Por exemplo: empresas que receberam funding, que estão contratando, que trocaram de CTO? Sem trigger, a lista vira catálogo genérico em vez de inteligência acionável." (Se a config ainda não existe, conduzir o Modo Configuração antes de pesquisar.)

## Armadilhas a evitar

- **Nunca entregar prospect sem trigger.** A proposta de valor inteira da skill é trigger-based. Lista sem trigger = Apollo genérico = 1% de resposta.
- **Não inventar triggers.** Se a web_search não encontrou evento recente, não fabricar. Melhor entregar 5 prospects com trigger real do que 10 com triggers inventados.
- **Cuidado com dados desatualizados.** Trigger de 6 meses atrás não é trigger — é contexto. Limite: 90 dias. Se o único trigger é antigo, sinalizar: "Trigger de [data] — pode já estar frio."
- **Não confundir prospect com lead.** Prospect = empresa com fit + trigger. Lead = alguém que demonstrou interesse. Essa skill gera prospects, não leads.
- **LinkedIn URLs podem mudar.** Sempre sinalizar que o usuário deve confirmar o perfil antes de enviar mensagem. Se não encontrar LinkedIn, não inventar.
- **Nunca pular o dry-run do CRM.** Push em massa sem revisão pode encher o CRM de duplicatas e deals mal configurados. Sempre dry-run → review → confirmação → execute.
- **Configs são pessoais.** `config/business-profile.md` e `config/crm-config.md` são por usuário. Se um colega instalar esta skill, ele preenche os próprios — nunca copiar a config de outra pessoa (especialmente o token de API).
- **Tokens nunca em texto plano no resumo.** Ao mostrar configuração ou erros, mascarar tokens (ex: `pat-****1234`).
