<!-- title: Parceiro - Atualizar dados | url: https://outline.seazone.com.br/doc/parceiro-atualizar-dados-9snaWJkzAl | area: Tecnologia -->

# Parceiro - Atualizar dados

## Regras de negocio

O campo `PersonID` não pode estar duplicado. Pois o worker que puxa as indicações dos parceiros ainda não lida com duplicidade e não atualiza os dados da planilha.


## Worker diário

Todos os dias na madrugada, é executado o worker que lê os dados da planilha e mostra para os parceiros. A cada execução é enviado uma notificação diária com o resumo, no slack  **#sapron-parceiros** com  as seguintes informações

**Erros ao atualizar comissões dos parceiros**

* **Códigos das Propriedades Não Encontradas:**
* **Person IDs Não Encontrados:**
* **Person IDs Duplicados:**
* **Person IDs Inválidos:**

Se o worker não conseguir executar e ler a planilha, então no gera registro no dia, nesses casos precisa verificar se a planilha tem algum dado errado.



:::info
NOTA

Por padrão, na hora da importação, se o campo de Parceiro está vazio, preenchemos com

 `partner_id = 1`

:::


## Solicitação de Resgate de Saldo do Parceiro

Verificar a tabela `Financial Partner Withdraw Request` pelo `partner_id`


## Solicitação de Resgate de Saldo do Parceiro

Verificar a tabela `Financial Partner Withdraw` pelo `partner_id`


## Regras sobre a Planilha

Aviso importante Boa tarde pessoal! Passando para reiterar alterações que podem ou não ser feitas na planilha "Fechamento parceiros", abas "BD_Acumulo" e "BD_Resgates"

```javascript
Como o "
```

```javascript
Saldo disponível
```

```javascript
" chega no Sapron dos parceiros?
```

 O saldo do parceiros é atualizado através [desta planilha](https://docs.google.com/spreadsheets/d/1O0qo1xyZnNyy1dLg8S5WCk-1XMH51GbC5T5bw3LrZAQ/edit?usp=sharing). Temos um script que roda uma vez ao dia e "lê" os dados das abas "BD_Acumulo" e "BD_Resgate", nos dando então o valor do Saldo do Parceiro.


\
 ![:warning:](/api/attachments.redirect?id=b57d5377-cbea-49d2-a3b3-117955169758 " =22x22")


\

```javascript
É recorrente recebermos dúvidas
```

 de saldos incorretos ou desatualizados por isso gostaríamos de elucidar o motivo de isto acontecer: alterações nesta planilha nas abas especificadas acima podem fazer com que o dado não seja atualizado. Quando isso acontece o script para de ler a planilha e o saldo fica desatualizado.


\
 ![:thinking_face:](/api/attachments.redirect?id=059c8857-b307-4f2b-bbf8-f1ad8ece5bbb " =22x22")


\

```javascript
O que pode ou não ser feito na planilha?
```

\nNa aba BD_Acumulo:

* Precisa ter **obrigatoriamente** uma coluna "Corretagem" (pode ter células em branco, é substituído por 0)
* Precisa ter **obrigatoriamente** uma coluna Data Fechamento com **TODAS** as células contendo um valor de mês/data no formato (mm/yyyy)

Na aba BD_Resgates:

* Precisa ter **obrigatoriamente** uma coluna "Valor Repassado" (pode ter células em branco, é substituído por 0)
* Precisa ter **obrigatoriamente** uma coluna "Data Pagamento" com **TODAS** as células contendo um valor de dia/mês/data como está atualmente (dd/mm/yyyy)


* Em ambas as abas, **TODAS** as colunas precisam manter **exatamente** os títulos como estão descritos;
* O posicionamento das colunas não importa contanto que o nome seja igual ao descrito;
* Podem ser criadas novas colunas mas as colunas ou linhas **não podem estar em branco**;
* Linhas e colunas **não podem ser agrupadas;**


Fonte [slack](https://seazone-fund.slack.com/archives/C04HQ2CLUPN/p1726846682830899)

## Parceiros e comissões 

As comissões dos parceiros são alimentados dessa planilha [Fechamento Parceiros SZS 2.0](https://docs.google.com/spreadsheets/d/1O0qo1xyZnNyy1dLg8S5WCk-1XMH51GbC5T5bw3LrZAQ/edit?usp=sharing) 

Aba "BD_acumulo" e "BD_Resgates", Se não estiver lá não estará no sapron. Esse valores podem ser verificados pelo ==#suporte-financeiro==


\
 ![:warning:](/api/attachments.redirect?id=b57d5377-cbea-49d2-a3b3-117955169758 " =22x22")


\
Ao realizar a troca de `PersonID` na tabela `Account_user`, normalmente **não é necessário fazer nenhuma alteração adicional**.

No entanto, é importante **verificar se o** `PersonID` **não está vinculado a outro usuário**. Caso esteja **duplicado**, será preciso **definir a qual usuário o** `PersonID` **deve permanecer associado**, para evitar inconsistências no sistema.


## Indicação de Parceiros

Precisa procurar o imovel na `Partners Indications Property` pelo Código do imóvel 

[https://metabase.seazone.com.br/question/1310-partners-indications-user-by-property-code](https://metabase.seazone.com.br/question/1310-partners-indications-user-by-property-code?objectId=57851)


Encontrar o PartnerID pelo PersonID nesse link <https://metabase.seazone.com.br/question/1233-account-partner-user>


Editar o registro do imóvel com o novo `PartnerID`