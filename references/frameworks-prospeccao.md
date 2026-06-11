# Frameworks de Prospecção — Taxonomia de Triggers, ICP Scoring e Metodologia

Esta referência detalha como identificar, classificar e priorizar prospects com base em trigger events. A skill carrega este arquivo quando precisa pesquisar e qualificar novos prospects.

---

## 1. Taxonomia de trigger events

Trigger events são mudanças observáveis no mercado que criam janelas de oportunidade. O vendedor que chega primeiro após o trigger tem vantagem massiva: dados da Growthlist mostram que o primeiro a contatar após trigger event tem probabilidade significativamente maior de ganhar o deal.

### Categoria 1: Financeiros (Urgência tipicamente ALTA)

| Trigger | O que sinaliza | Tempo de reação ideal | Como pesquisar |
|---|---|---|---|
| Funding round (Seed, A, B, C+) | Empresa vai crescer, contratar, investir em infra | 24-48h | "[setor] funding round [ano] [região]" |
| M&A (fusão/aquisição) | Revisão de fornecedores, consolidação de processos | 24-72h | "[setor] aquisição fusão [ano]" |
| IPO / preparação para IPO | Pressão por processos, compliance, previsibilidade | 48-72h | "[setor] IPO preparação" |
| Resultado financeiro publicado | Se bom: expansão. Se ruim: reestruturação | 72h-7d | "[empresa] resultados financeiros [trimestre]" |

### Categoria 2: Organizacionais (Urgência tipicamente ALTA a MÉDIA)

| Trigger | O que sinaliza | Tempo de reação | Como pesquisar |
|---|---|---|---|
| Novo C-level (CEO, CRO, VP) | Revisão de processos, novos fornecedores em 90 dias | 24-48h | "[setor] novo CEO/CRO/VP [região]" |
| Novo Head de área relevante | Quer mostrar resultado rápido, aberto a novos vendors | 48-72h | LinkedIn: filtro "changed job" + cargo |
| Reestruturação de equipe | Processos antigos sendo questionados | 72h-7d | "[empresa] reestruturação equipe" |
| Hiring em posições-chave | Investimento na área, gap de capacidade | 72h-7d | LinkedIn Jobs, Gupy, Glassdoor |

### Categoria 3: Mercado/Estratégia (Urgência tipicamente MÉDIA)

| Trigger | O que sinaliza | Tempo de reação | Como pesquisar |
|---|---|---|---|
| Expansão geográfica | Precisa escalar processos, contratar, adaptar | 72h-7d | "[empresa] nova unidade filial [região]" |
| Novo produto/serviço | Precisa de go-to-market, vendas, processos novos | 72h-7d | "[empresa] lançamento novo produto" |
| Parceria estratégica | Pode abrir portas por associação | 7d | "[empresa] parceria [setor]" |
| Mudança regulatória no setor | Todo setor precisa se adaptar | 7d | "[setor] nova regulação [ano]" |

### Categoria 4: Tecnológicos (Urgência MÉDIA a BAIXA)

| Trigger | O que sinaliza | Tempo de reação | Como pesquisar |
|---|---|---|---|
| Mudança de CRM/ERP | Janela de implementação, processos em revisão | 72h-7d | "[empresa] implementando HubSpot/Salesforce" |
| Adoção de ferramenta relevante | Stack em evolução, momento de adicionar peças | 7d | BuiltWith, Wappalyzer, notícias |
| Transformação digital | Budget alocado, abertura para novas soluções | 7d | "[empresa] transformação digital" |

---

## 2. ICP Scoring — Como pontuar o fit de um prospect

Nem todo prospect com trigger é bom prospect. O scoring combina FIT (encaixa no ICP) com TIMING (trigger ativo).

### Matriz de priorização

|  | Trigger ALTO (24-48h) | Trigger MÉDIO (72h-7d) | Trigger BAIXO (contexto) |
|---|---|---|---|
| **Fit ALTO** (encaixa perfeitamente no ICP) | ⭐ PRIORIDADE 1 — contatar imediatamente | PRIORIDADE 2 — contatar essa semana | PRIORIDADE 3 — nurture |
| **Fit MÉDIO** (encaixa parcialmente) | PRIORIDADE 2 — contatar essa semana | PRIORIDADE 3 — nurture | Não prospectar agora |
| **Fit BAIXO** (não encaixa) | Descartar | Descartar | Descartar |

### Como avaliar FIT

Checklist de 5 critérios (cada um vale 0-2 pontos, total máximo = 10):

| Critério | 2 pontos | 1 ponto | 0 pontos |
|---|---|---|---|
| **Setor** | Setor-alvo principal | Setor adjacente | Fora do escopo |
| **Porte** | Dentro da faixa ideal | Próximo da faixa (±30%) | Totalmente fora |
| **Geografia** | Região prioritária | País ok, região secundária | Fora da geografia |
| **Cargo do decisor** | Cargo-alvo exato disponível | Cargo adjacente | Sem acesso ao decisor |
| **Sinal de fit** | Match com 2+ sinais do config | Match com 1 sinal | Nenhum sinal |

**Score 8-10:** Fit ALTO → priorizar
**Score 5-7:** Fit MÉDIO → considerar com trigger forte
**Score 0-4:** Fit BAIXO → descartar

---

## 3. Metodologia de pesquisa estruturada

### Fase 1: Pesquisa de triggers (web_search)

Organizar as buscas em 3 rodadas:

**Rodada 1 — Triggers de alta urgência:**
- "[setor] + [funding / aquisição / novo CEO] + [região] + [ano]"
- 1-2 buscas focadas nos triggers financeiros e organizacionais

**Rodada 2 — Triggers de média urgência:**
- "[setor] + [contratando / expansão / novo produto] + [região]"
- 1-2 buscas nos triggers de mercado e hiring

**Rodada 3 — Enriquecimento e validação:**
- "[empresa específica] + [notícia recente]" (para prospects encontrados nas rodadas 1-2)
- Confirmar que trigger é real e recente

**Total: 3-5 buscas.** Não fazer 15 buscas — cada uma deve ter alvo claro.

### Fase 2: Filtragem contra ICP

Para cada empresa encontrada nos resultados:
1. Avaliar fit com ICP (scoring acima)
2. Confirmar recência do trigger (< 90 dias)
3. Eliminar duplicatas e empresas que o usuário já prospecta

### Fase 3: Enriquecimento de prospect

Para cada prospect que passou no filtro:
1. Identificar decisor/cargo no LinkedIn (se possível via web_search)
2. Buscar 1 dado adicional que personalize a mensagem (ex: post recente do decisor, projeto da empresa)
3. Classificar urgência do trigger

### Fase 4: Geração de mensagem

Para os top 5-10 prospects, gerar mensagem usando templates de `references/templates-mensagens.md`. Personalizar com:
- Nome da empresa
- Trigger específico
- Ponte entre trigger e dor que o usuário resolve
- CTA adequado ao canal

---

## 4. Métricas de qualidade da lista

Uma lista de prospecção boa tem:

| Métrica | Meta | Abaixo da meta = problema |
|---|---|---|
| % com trigger real (< 90 dias) | 100% | Lista virou catálogo |
| % dentro do ICP | 100% | Filtro mal feito |
| % com decisor identificado | >70% | Pesquisa incompleta |
| % com mensagem personalizada | >50% (top prospects) | Genérico demais |
| Diversidade de triggers | 2+ tipos diferentes | Viés de pesquisa |

Se a lista não atingir essas metas, informar o usuário e sugerir pesquisa adicional em vez de entregar lista fraca.

---

## 5. Fontes de dados para pesquisa

### Fontes gratuitas via web_search
- Google News (notícias de trigger)
- LinkedIn (mudanças de cargo, vagas — via web_search)
- Crunchbase (funding — versão pública)
- Sites de emprego (Gupy, Glassdoor, LinkedIn Jobs — hiring como trigger)
- Jornais de negócio (Valor Econômico, InfoMoney, Exame — M&A, resultados)
- Portais setoriais (dependem do setor do ICP)

### Dados que a skill NÃO consegue acessar sem ferramenta paga
- Email pessoal/corporativo do decisor (não inventar)
- Telefone direto (não inventar)
- Dados financeiros detalhados (só públicas/startups com dados divulgados)
- Tecnographics em tempo real (só plataformas como BuiltWith)

**Regra de ouro:** se não encontrou o dado via web_search, informar ao usuário. Nunca fabricar dados de contato ou métricas financeiras.

---

_Referências: Gong Labs (300M+ cold calls), Growthlist (trigger-based prospecting), Apollo/Clay (ICP scoring methodology), Bridge Group SaaS GTM 2025 (rep productivity), McKinsey B2B Buying Journey 2024-2025._
