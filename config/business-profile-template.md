# Business Profile — /prospeccao-multi-crm

> Este arquivo configura a skill para pesquisar prospects alinhados ao SEU negócio. Preencha UMA VEZ ao instalar. A skill vai conduzir você pelos blocos abaixo em uma conversa — você não precisa preencher isso manualmente, só responder às perguntas.
>
> **Reaproveitamento:** se você já preencheu o config de `apresentacao-de-vendas`, `proposta-automatica` ou da skill `prospeccao` original, pode reusar o ICP, proposta de valor e tom de voz. Copie de lá e complete o que falta aqui.

---

## Bloco 1: ICP — Perfil de Cliente Ideal

> A skill usa isso pra filtrar quais empresas vale a pena pesquisar. Sem ICP definido, qualquer empresa é "prospect" — e isso é o oposto de inteligência.

### 1.1 Setor(es)-alvo
> Quais setores você atende? Se atende vários, liste em ordem de prioridade.
> Ex: "1. Empresas de serviço B2B  2. SaaS  3. Indústria de médio porte"

**Setores:** [A PREENCHER]

### 1.2 Porte ideal
> Em que faixa de tamanho seus melhores clientes se encaixam? Use métrica que faz sentido (funcionários, faturamento, ou ambos).
> Ex: "20-200 funcionários, faturamento R$ 5-50M/ano" ou "PME até 500 funcionários"

**Porte:** [A PREENCHER]

### 1.3 Geografia
> Onde seus clientes estão? Regiões, estados, cidades.
> Ex: "Brasil todo, mas 70% em SP/RJ/MG" ou "Região Sul e Sudeste"

**Geografia:** [A PREENCHER]

### 1.4 Exclusões (quem NÃO prospectar)
> Setores, portes ou tipos de empresa que não valem o esforço.
> Ex: "Não prospectar governo, microempresa <5 func, concorrentes diretos"

**Excluir:** [A PREENCHER]

### 1.5 Sinais de bom fit (além de firmographics)
> O que diferencia um prospect bom de um que encaixa no ICP mas não compra?
> Ex: "Já tem time de vendas estruturado (3+ reps)", "Usa CRM", "Tem meta de receita definida"

**Sinais de fit:** [A PREENCHER]

---

## Bloco 2: Cargos-alvo

### 2.1 Decisor (quem assina)
> Cargo(s) que tipicamente tomam a decisão de compra.
> Ex: "CEO (empresas <50 func), VP Comercial ou Head de Vendas (>50 func)"

**Decisor:** [A PREENCHER]

### 2.2 Influenciadores (quem recomenda)
> Cargos que influenciam mas não decidem sozinhos.
> Ex: "Gerente Comercial, Head de RevOps, Diretor de Operações"

**Influenciadores:** [A PREENCHER]

### 2.3 Usuário final (quem vai usar)
> Quem vai interagir diretamente com seu produto/serviço no dia a dia?
> Ex: "SDR, AE, Customer Success Manager"

**Usuário final:** [A PREENCHER]

---

## Bloco 3: Proposta de valor

### 3.1 O que você vende? (1-2 frases)
> Se já preencheu em outra skill, cole aqui.
> Ex: "Consultoria que reorganiza o processo comercial de empresas B2B, reduzindo ciclo de venda e aumentando ticket médio."

**Oferta:** [A PREENCHER]

### 3.2 UVP — Proposta de valor única (1 frase)
> Por que você e não o concorrente? O que só você faz?
> Ex: "Implementamos processo comercial completo em 45 dias, com playbook documentado que elimina dependência do consultor."

**UVP:** [A PREENCHER]

### 3.3 Dor principal que resolve
> A dor #1 que seus clientes sentem ANTES de te contratar.
> Ex: "Time de vendas sem processo — cada rep vende de um jeito, forecast imprevisível, ciclo de 120+ dias"

**Dor:** [A PREENCHER]

---

## Bloco 4: Trigger events que interessam

> Quais tipos de evento de mercado sinalizam que uma empresa deveria ser contatada AGORA? Marque os que se aplicam ao seu negócio.

- [ ] **Funding/Investimento** — empresa recebeu aporte, rodada de investimento
- [ ] **Hiring/Contratação** — contratando para posição relevante (ex: "Head de Vendas", "SDR")
- [ ] **Expansão** — nova unidade, filial, entrada em nova região/país
- [ ] **Leadership change** — novo CEO, VP, diretor relevante
- [ ] **Tech change** — implementando/migrando ferramenta relevante (ex: CRM, ERP)
- [ ] **Notícia relevante** — prêmio, parceria, resultado financeiro publicado
- [ ] **M&A** — fusão, aquisição, spin-off
- [ ] **Outro:** [A PREENCHER]

### 4.1 Triggers que NÃO interessam
> Eventos que geram ruído sem valor para sua prospecção.
> Ex: "Não me interessa funding seed (empresa muito nova), nem contratação de estagiário"

**Excluir:** [A PREENCHER]

---

## Bloco 5: Tom de voz e abordagem

### 5.1 Tom de voz na mensagem inicial
> Como você se apresenta em cold outreach? Formal? Informal? Técnico? Consultivo?
> Ex: "Direto, informal, consultivo. Nunca auto-promocional. Sempre começa pelo prospect, não por mim."

**Tom:** [A PREENCHER]

### 5.2 Frase de abertura padrão (opcional)
> Se você tem uma frase de abertura que funciona bem, coloque aqui. A skill vai adaptar por prospect.
> Ex: "Vi que [trigger] — isso geralmente significa que [dor]. Como vocês estão lidando com isso?"

**Frase:** [A PREENCHER]

### 5.3 Canal preferido para primeiro contato
- [ ] Email
- [ ] LinkedIn (InMail ou connection request + mensagem)
- [ ] WhatsApp
- [ ] Telefone (cold call)
- [ ] Multi-canal (skill gera para 2-3 canais)

### 5.4 Frases proibidas
> Frases ou expressões que NUNCA devem aparecer na mensagem de prospecção.
> Ex: "Nunca: 'oportunidade imperdível', 'líder de mercado', 'solução completa', 'agendar uma call de 15min'"

**Proibido:** [A PREENCHER]

---

_Última atualização: [data] — Atualize quando mudar ICP, proposta de valor, ou estratégia de outreach._

_Próximo passo: depois de preencher este arquivo, complete `config/crm-config.md` (Bloco 6) para conectar a skill ao seu CRM._
