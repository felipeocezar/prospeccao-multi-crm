# Prospecção Multi-CRM

Skill para Claude (Cowork / Claude Code com skills) que pesquisa prospects B2B qualificados a partir de **trigger events reais** — funding, contratações, troca de liderança, expansão, mudança de tecnologia — e (opcionalmente) cria os leads direto no seu CRM: **Pipedrive, HubSpot ou RD Station CRM**.

Cada pessoa que instala configura o **próprio ICP** e o **próprio CRM** na primeira execução. Nada é compartilhado entre usuários — cada configuração fica local, na máquina de quem instalou.

## Por que trigger-based

Prospecção genérica tem taxa de resposta de 1-2% (Gong Labs, 30 mil emails analisados). Prospecção baseada em trigger event sobe para 12-18% — até 400% mais conversão. A diferença é que cada prospect vem com o **porquê**: o evento que justifica o contato agora, não há 3 meses.

## O que a skill entrega

- Lista priorizada de prospects (markdown + CSV), cada um com: empresa, setor, porte, trigger identificado (com fonte e data), nível de urgência, decisor sugerido e gancho de abordagem
- Mensagem inicial personalizada para os prospects de maior prioridade (email, LinkedIn ou WhatsApp)
- Push automático dos leads para o CRM configurado, com revisão em modo dry-run antes de qualquer escrita

## Instalação

1. Baixe o arquivo [`prospeccao-multi-crm.skill`](./prospeccao-multi-crm.skill) deste repositório.
2. No Claude (Cowork ou Claude Code), vá em **Settings → Capabilities → Skills** e instale o arquivo `.skill`.
3. Na primeira vez que pedir uma prospecção, a skill vai conduzir uma configuração guiada (veja abaixo).

## Configuração na primeira execução

A skill conduz uma entrevista curta em 6 blocos e salva tudo localmente nos arquivos `config/business-profile.md` e `config/crm-config.md`:

1. **ICP** — setor, porte, geografia
2. **Cargos-alvo** — quem é o decisor que você quer alcançar
3. **Proposta de valor** — o que você resolve e principais cases
4. **Trigger events relevantes** — quais sinais de mercado importam para o seu produto
5. **Tom de voz** — como suas mensagens devem soar
6. **CRM de destino** — Pipedrive, HubSpot, RD Station CRM ou nenhum (só gera lista)

### Sobre tokens de API do CRM

Se você conectar um CRM, vai precisar de um token de API (instruções de onde encontrar cada um estão em `config/crm-config-template.md`). O token fica **somente no seu arquivo local `config/crm-config.md`** — nunca é enviado para terceiros, nunca deve ser colado em chat ou commitado em repositório.

## Como usar

Exemplos de pedidos que disparam a skill:

```
Me traz 10 prospects do setor de logística que receberam funding recente
e já sobe pro meu Pipedrive.

Preciso de pipeline novo: empresas de tecnologia que estão contratando
VP de vendas no Brasil.

Quem eu deveria abordar essa semana? Qualquer trigger recente no meu ICP.
```

Antes de qualquer escrita no CRM, a skill roda em modo **dry-run** e mostra exatamente o que seria criado (organizations, contatos, deals, pipeline/estágio). Só executa após confirmação.

## Estrutura do repositório

```
prospeccao-multi-crm/
├── SKILL.md                          # definição da skill (gatilhos + fluxo)
├── prospeccao-multi-crm.skill        # pacote pronto para instalar
├── config/
│   ├── business-profile-template.md  # template do ICP (blocos 1-5)
│   └── crm-config-template.md        # template de conexão com CRM (bloco 6)
├── references/
│   ├── frameworks-prospeccao.md      # taxonomia de triggers, ICP scoring, metodologia
│   ├── templates-mensagens.md        # templates de mensagem por trigger e canal
│   └── guia-crm.md                   # detalhes de API por CRM
└── scripts/
    └── push_to_crm.py                # script de push (Pipedrive / HubSpot / RD Station CRM)
```

## CRMs suportados

| CRM | Autenticação | Status |
|---|---|---|
| Pipedrive | API token pessoal | Suportado |
| HubSpot | Private App Token | Suportado |
| RD Station CRM | API token | Suportado |
| Nenhum | — | Gera apenas MD/CSV para import manual |

## Limitações

- Dados vêm de busca web pública — sem acesso a e-mail/telefone direto de contatos (a skill não inventa esses dados)
- Triggers com mais de 90 dias são sinalizados como possivelmente "frios"
- O push para o CRM depende dos nomes de pipeline/estágio configurados baterem exatamente com os do seu CRM

## Licença

Uso livre e adaptação para fins internos. Sem garantias — revise o dry-run antes de qualquer escrita em produção no seu CRM.
