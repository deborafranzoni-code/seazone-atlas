<!-- title: Parceiros - Processos | url: https://outline.seazone.com.br/doc/parceiros-processos-nqvoa53OYk | area: Tecnologia -->

# Parceiros - Processos

### Relação de ganho de Parceiro - Inferência de Property_id

| Cenário | Processo | Regra de negócio | Problema |
|----|----|----|----|
| Parceiro faz uma indicação de Imóvel e converte em ganho | **Parceiro** realiza uma indicação, a indicação é criada na tabela `Patners_indications_Property`, sem o `id` e `code` da propriedade.<br>**Quando** a indicação converte em ganho, o `deal_id` contém o `partner_id` correto, e o `id` e `code` da propriedade são correlacionados na tabela `Partner_indications_property`. | Parceiro ganha comissão sobre a receita do imóvel:<br>`Receita x porcentagem da comissão = corretagem`.<br><br>**==Vigência de ganho:==**<br>**==1 ano:==** ==Parceiro ganha comissão **a partir da data de ativação do imóvel no Sapron.**==<br><br>**Vitalício: Sem data fim para ganho da corretagem**<br><br>**~~==Importante: um imóvel não muda quanto a vigência de ganho, independente da mudança de clusterização do parceiro.==~~**<br><br>**==Importante: Quando um parceiro muda de Básico (12 meses de ganho de corretagem) para Premium, a corretagem dos seus imóveis passa a ser vitalícia, CASO o período de corretagem do imóvel ainda não tenha passado os 12 meses.==**<br>**==Da mesma forma, se um parceiro passa de Premium para Basic, a corretagem do imóvel atrelado ao parceiro passa a ter vigência de 12 meses, caso não tenha vencido os 12 meses a partir da data de ativação do imóvel no Sapron.==**<br><br> | Atualmente não temos visibilidade de quais parceiros são vitalícios.<br>Além disso quando um parceiro é demovido, ou promovido, há solicitações de suportes para o financeiro alterar todos os imóveis do parceiro. |
| Parceiro faz uma indicação de Imóvel e converte em ganho, e o parceiro é alterado na mesma propriedade | **Parceiro** realiza uma indicação, a indicação é criada na tabela `Patners_indications_Property`, sem o `id` e `code` da propriedade.<br>**Quando** a indicação converte em ganho, o `deal_id` contém o `partner_id` correto, e o `id` e `code` da propriedade são correlacionados na tabela `Partner_indications_property`.<br><br>**Quando** o parceiro é alterado no pipedrive, a tabela `partner_indications_property,` não altera a inferência do novo parceiro. O parceiro "novo" não visualiza o ganho.  | Necessário alinhamento | Atualmente o sapron não suporta alterações de parceiro em uma mesma propriedade. É necessário alinhar esta regra de negócio. <br>No fechamento financeiro, como foram feitas muitas mudanças, isso ficou difícil de rastrear pois em alguns casos nao ficou claro o motivo da mudança. Além disso em um caso a corretagem foi paga em duplicidade, deixando a nova parceira com um saldo negativo de mais de 900 reais. |
| Códigos de propriedades sem property_id | Alguns imóveis estão como ganho no pipedrive mas não foram criados no sapron. Exemplo: ZART VEC222 | Necessário alinhamento | Isso impacta diretamente o fechamento atual pois a planilha fica sem referencia de property_id e por sua vez não é possível calcular a receita do imóvel que não existe no Sapron. |
| **Imóveis que já deram churn,** trocaram de parceiro e/ou proprietário, aparecem ainda como ganho para os parceiros pois os deals ainda permanecem como ganho no pipedrive |    | Necessário alinhamento | O parceiro continua vendo o imóvel como ganho, sendo que o imóvel já deu churn.<br><br>==Melhoria sapron: trazer o status do imóvel pro parceiro na rela de minhas indicações==  |

### Necessário cadastro de parceiros B2B no Sapron

| Cenário | Processo | Problema |
|----|----|----|
| Deals com ganho no pipedrive, atrelados a parceiros B2B não cadastrados no Sapron | **Quando** um deal for dado como ganho no pipedrive<br>**Então** é necessário o cadastro do parceiro no Sapron, garantindo que o parceiro tenha visibilidade do ganho, e consiga solicitar o saque das corretagens associadas ao parceiro. | Parceiros B2B não cadastrados no Sapron, geram erro de person_id/partner_id inexistentes, parceiro não tem visibilidade do ganho e não consegue solicitar o resgate do saldo |

### Proprietário - parceiro

| Cenário | Processo | Problema |
|----|----|----|
| Proprietário torna-se parceiro | **Quando** um proprietário torna-se também parceiro<br>**Então** é necessário o cadastro no banco de dados (direto nas tabelas)  | Atualmente o Sapron não permite o cadastro de proprietários como parceiros.<br><br>==SAPRON: Necessário desenvolvimento da solução que permite inserir um proprietário na tela de parceiros, garantindo que o proprietário tenha acesso a página de parceiros através da Wallet.== |

### Franqueado dá churn e mantém vínculo de parceiro

| Cenário | Processo | Problema |
|----|----|----|
| Franqueado dá churn mas mantém vínculo de parceiros | **Quando** um franqueado dá churn, mas permanece como parceiro<br>**Então** é necessário: <br>1. Abrir um suporte, solicitando a desativação da conta da franquia;<br>2. Criar uma conta de parceiro na tela de Inserir Parceiro;<br>3. Solicitar via suporte a migração das indicações vinculadas ao franqueado à sua nova conta de parceiro;<br>4. Solicitar ajuste ao Time financeiro, garantindo que as inferências retroativas sejam corrigidas tanto na aba BD_ACUMULO como na aba BD_Resgate | Franqueados deram churn mas não foram corrigidas na planilha de fechamento financeiro.<br>Isso gerou problema de inferência de corretagens, relacionadas ao Parner_id, impactando na visualização do saldo do parceiro<br><br><br>==SAPRON \[Melhoria\]: Permitir migração automática no formulário de parceiros, garantindo o processo descrito.==<br><br>==Quando a franquia da churn, alterar o email de acesso na página de editarparceiros== |

### Proprietário é franqueado, e por sua vez é parceiro

| Cenário | Processo | Problema |
|----|----|----|
| Proprietário é franqueado, e por sua vez é parceiro | **Quando** um proprietário é também franquedo & parceiro<br>**Então** o vínculo de acesso à página de parceiros **é associada a conta da franquia**, e não a conta de acesso de proprietário (Wallet)<br><br>`Partner_id` e `person_id` **devem ter associação de 1:1** | Franqueados e proprietários possuíam dois Parner_ID, gerando o erro de person_id.<br><br>Isso gera problema de processamento da corretagem pois o código não consegue identificar o apontamento correto do partner_id por conta da duplicidade do person_id.<br><br>==Melhoria Sapron/Wallet: permitir que proprietário/franqueado/parceiro possuam um login unificado==<br><br>  |

### Processo fechamento de parceiros (Sapron)

| Atual | Sapron | Problema |
|----|----|----|
| A corretagem é dos parceiros é calculada a partir da leitura da planilha de [Fechamento 2.0](https://docs.google.com/spreadsheets/d/1O0qo1xyZnNyy1dLg8S5WCk-1XMH51GbC5T5bw3LrZAQ/edit?gid=32645293#gid=32645293&fvid=1724946670), aba BD_Acúmulo.<br><br>O Script lê a coluna "Partner_id" e associa a corretagem, dando entrada do registro na tabela `**Financial Partner Commission Property**`**.**<br><br>**A planilha é alimentada através de macros e muitos processos manuais** |    | 
1. **Se não existe** `**parner_id/person_id**` **criado** no banco de dados, a corretagem não é processada
2. **Se o código da propriedade não existe** no Sapron, a corretagem não é processada
3. Macros falham no processo de imóveis que já estão inativados no Sapron, e permanecem ativos no pipedrive, calculando corretagem zerada
4. Persons foram mesclados ou excluídos no pipedrive. Para os persons excluídos, a planilha de fechamento continua puxando a corretagem para o person_id inexistente, o campo de parceiro no pipedrive fica como (oculto) e o parceiro não visualiza a corretagem de ganho pois a corretagem está sendo direcionada para um usuário inexistente no pipedrive (exemplo: person_id 31202 person_id criado, 31510 person_id excluído, mas se trata da mesma pessoa)
5. Falta de visibilidade da vigência de ganhos, podendo ser calculadas corretagem a mais ou a menos dependendo do cenário
6. Macro realiza o fechamento de imóveis que ainda não foram inseridas no Sapron, gerando o erro de property_id no Sapron
7. Limite de dados da planilha, e muitos processos manuais não é escalável e torna a operação frágil com tendência a erros<br><br><br>  |

### Processo de pagamentos de parceiros (Sapron)

### 🔁 **Cenário 1 — Parceiro Básico (vigência de 12 meses)**

* **Tipo de parceiro:** Básico
* **Data de ativação do imóvel no Sapron:** 01/01/2025
* **Porcentagem de comissão:** 2%
* **Vigência:** 12 meses

📘 **Exemplo:**\nO parceiro recebe comissão de 2% sobre a receita do imóvel entre **01/01/2025 e 31/12/2025**.\nApós essa data, o imóvel deixa de gerar corretagem para esse parceiro.


---

### 🔁 **Cenário 2 — Parceiro Premium (vigência vitalícia)**

* **Tipo de parceiro:** Premium
* **Data de ativação do imóvel no Sapron:** 01/01/2025
* **Porcentagem de comissão:** 2%
* **Vigência:** Vitalícia

📘 **Exemplo:**\nO parceiro recebe comissão de 2% sobre a receita do imóvel **sem data de término**, enquanto o imóvel estiver ativo no Sapron e vinculado a ele.


---

### 🔁 **Cenário 3 — Mudança de Básico → Premium (antes de vencer os 12 meses)**

* **Tipo inicial:** Básico
* **Data de ativação do imóvel:** 01/01/2025
* **Data da mudança de clusterização:** 01/07/2025 (6 meses depois)

📘 **Regra aplicada:**\nComo o imóvel **ainda não completou 12 meses de vigência**, ao mudar para **Premium**, a vigência passa a ser **vitalícia**.

✅ **Resultado final:**\nO imóvel passa a gerar corretagem **sem data fim**, mesmo após os 12 meses.


---

### 🔁 **Cenário 4 — Mudança de Básico → Premium (após o vencimento dos 12 meses)**

* **Tipo inicial:** Básico
* **Data de ativação do imóvel:** 01/01/2025
* **Data da mudança de clusterização:** 01/03/2026 (14 meses depois)

📘 **Regra aplicada:**\nO período de 12 meses de corretagem já venceu antes da mudança.\nMesmo que o parceiro se torne Premium, **esse imóvel não volta a gerar corretagem**.

🚫 **Resultado final:**\nO imóvel não volta a ser remunerado, pois o direito expirou.


---

### 🔁 **Cenário 5 — Mudança de Premium → Básico (antes dos 12 meses)**

* **Tipo inicial:** Premium
* **Data de ativação do imóvel:** 01/01/2025
* **Data da mudança de clusterização:** 01/07/2025 (6 meses depois)

📘 **Regra aplicada:**\nAo se tornar Básico, a vigência da corretagem do imóvel passa a ser **de 12 meses** contados **a partir da data de ativação** (não da mudança).

✅ **Resultado final:**\nO parceiro recebe até **31/12/2025**, respeitando os 12 meses desde a ativação.


---

### 🔁 **Cenário 6 — Mudança de Premium → Básico (após os 12 meses)**

* **Tipo inicial:** Premium
* **Data de ativação do imóvel:** 01/01/2024
* **Data da mudança de clusterização:** 01/04/2025 (15 meses depois)

📘 **Regra aplicada:**\nComo o imóvel foi ativado há mais de 12 meses, ao mudar para Básico, **a corretagem é encerrada imediatamente**, pois já ultrapassou o período permitido para o plano Básico.

🚫 **Resultado final:**\nO imóvel deixa de gerar corretagem a partir da mudança.

\n\n\n