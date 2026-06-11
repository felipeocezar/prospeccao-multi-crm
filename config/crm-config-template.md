# CRM Config — /prospeccao-multi-crm

> Bloco 6 da configuração. Preencha UMA VEZ, depois de terminar `config/business-profile.md`.
>
> **Importante sobre segurança:** este arquivo vai conter um token de API (uma senha de acesso ao seu CRM). Preencha os valores **diretamente neste arquivo**, não cole o token no chat. Não compartilhe este arquivo com colegas — cada pessoa preenche o próprio. Se você compartilhar esta skill com o time, compartilhe a pasta da skill SEM este arquivo preenchido (ou copie o `crm-config-template.md` em branco).

---

## 6.1 Qual CRM você usa?

Marque uma opção:

- [ ] **Pipedrive**
- [ ] **HubSpot**
- [ ] **RD Station CRM**
- [ ] **Nenhum** — só quero gerar a lista em Markdown/CSV pra importar manualmente

**CRM escolhido:** [A PREENCHER]

---

## 6.2 Credenciais de API

Preencha apenas a seção do CRM escolhido. Deixe as outras como estão.

### Se Pipedrive

> Onde encontrar: dentro do Pipedrive, vá em **Configurações pessoais → API** (ícone de avatar no canto superior direito → "Configurações pessoais" → aba "API"). Copie o "Your personal API token".

- **Domínio da empresa** (a parte antes de `.pipedrive.com` na URL, ex: se a URL é `https://acme.pipedrive.com`, o domínio é `acme`): [A PREENCHER]
- **API Token**: [A PREENCHER]

### Se HubSpot

> Onde encontrar: **Configurações → Integrações → Private Apps → Criar app privado**. Em "Scopes", marque pelo menos: `crm.objects.contacts.write`, `crm.objects.contacts.read`, `crm.objects.companies.write`, `crm.objects.companies.read`, `crm.objects.deals.write`, `crm.objects.deals.read`. Copie o token gerado (começa com `pat-`).

- **Private App Token**: [A PREENCHER]

### Se RD Station CRM

> Onde encontrar: dentro do RD Station CRM, vá em **Configurações → Integrações → API → Tokens de Integração** e gere um token. (Atenção: RD Station CRM é diferente do RD Station Marketing — confirme que é o produto de CRM/funil de vendas.)

- **Token de API**: [A PREENCHER]

---

## 6.3 Pipeline e estágio de destino

> A skill cria os novos prospects como negócios/leads logo no início do funil. Diga em qual funil e em qual estágio eles devem entrar — use o nome exatamente como aparece no seu CRM.

- **Nome do pipeline/funil**: [A PREENCHER] (ex: "Funil Comercial", "Outbound", "Vendas")
- **Nome do estágio inicial**: [A PREENCHER] (ex: "Novo Lead", "Prospecção", "Para Contatar")

---

## 6.4 Responsável padrão (owner)

> Quem deve aparecer como dono/responsável pelos novos leads/negócios? Use o nome ou e-mail exatamente como cadastrado no CRM.

- **Nome ou e-mail do responsável**: [A PREENCHER]

---

## 6.5 Campos e tags adicionais (opcional)

> Algo que deve ser preenchido automaticamente em todo prospect criado por esta skill? Útil para rastrear a origem.
> Ex: "Adicionar tag 'prospeccao-trigger'", "Campo customizado 'Origem' = 'Prospecção automática'"

- **Campo/tag adicional**: [A PREENCHER]

---

## 6.6 Como lidar com duplicados

> Se a empresa já existir no CRM, o que a skill deve fazer?

- [ ] Pular (não criar de novo, só avisar)
- [ ] Criar mesmo assim (pode gerar duplicata)
- [ ] Perguntar caso a caso

**Escolha:** [A PREENCHER] (recomendado: Pular)

---

_Última atualização: [data]_
