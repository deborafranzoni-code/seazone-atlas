<!-- title: Fechamento Anfitriões | url: https://outline.seazone.com.br/doc/fechamento-anfitrioes-TIoFFuoyxE | area: Administrativo Financeiro -->

# Fechamento Anfitriões

![](Fechamento%20Anfitrio%CC%83es%20e0c90030d1c94e2d8b0ef4f1ecb28324/FUNDOS_TRELLO_5_(1).png)

👨🏻‍💻

# Fechamento Anfitriões


\
**DESCRIÇÃO**

ℹ️

O Fechamento de Anfitrião consiste em compilar os dados de todos os imóveis que gerencia. É a partir dele que encaminhamos a lista de TEDs para o Financeiro realizar as transações e a lista de NFs que cada anfitrião deve emitir.


**PRAZO**

⏰

O Fechamento de Anfitrião deverá ser realizado nos **primeiros cinco dias úteis do mês**, a partir do momento em que os fechamentos de imóvel e proprietário estiverem finalizados e a macro de anfitrião tiver sido rodada.


**DIVISÃO DE MIGRAÇÕES E TROCAS**

ℹ️

Realizar a divisão das reservas de acordo com os casos de migração de anfitrião e troca de proprietário.

* Passo a passo

  
  1. Acessar a planilha [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=541252494) na aba Migração de anfitrião;
  2. Acessar a pasta [Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp) e selecionar a planilha com a data de referência do fechamento atual;
  3. Acessar a aba Conciliação Fechamento para fins de conferência e quebra;
  4. Acessar o [Sapron](https://sapron.com.br/fechamentoimovel) na aba Fechamento Imóvel para fins de conferência e quebra;
  5. Acessar o [Sapron](https://sapron.com.br/fechamentoimovel) na aba Fechamento Anfitrião e verificar se de acordo com a data da troca do anfitrião, a divisão das reservas está correta e anotar a proporção das reservas na aba Migração de anfitrião na coluna "Observação";
  6. Caso a divisão das reservas não esteja correta, deve-se acessar o [Suporte do Sapron](https://suportesapron.atlassian.net/servicedesk/customer/portals) e abrir uma solicitação de suporte para correção;
  7. Acessar a aba Anfitrião na planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) e quebrar as colunas de números de reservas, receita reservas, número de limpezas, limpezas, comissão total, despesas e comissão franqueado, de acordo com a data de troca.

  \
  ⚠️

  **Observação:** as reservas antes da data da troca são do anfitrião antigo e as reservas depois da data da troca, são do anfitrião novo e deve-se atentar às reservas de booking e expedia devido a regra 30+.


**MÉTRICAS DE CONFERÊNCIA**

ℹ️

São métricas de conferências aplicadas durante o processo para precaver erros e trazer mais segurança nos dados apontados no Fechamento de Anfitrião.



1. **Número de Reservas**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha 04 - Conciliação Reservas Sapron na aba Conciliação Fechamento e conferir se a soma da coluna "Número de Reservas" na aba Anfitrião é igual a contagem das linhas da aba Conciliação Fechamento (descontando cabeçalho).

  \
  ⚠️

  **Observação:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*

  ⚠️

  **Observação 2:** *Deve-se retirar os imóveis TST (teste) da planilha* *[01 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=1596704130)__. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*


⚠️

**Observação:** *Deve-se retirar os imóveis TST (teste) da planilha* *[01 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=1596704130)__. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*



2. **Receita de Reservas**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0) na aba Conciliação Fechamento e conferir se a soma da coluna "Receita Reservas" na aba Anfitrião é igual a soma da coluna "Valor Diárias Mês" na aba Conciliação Fechamento.

  \
  ⚠️

  **Observação:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*

  ⚠️

  **Observação 2:** *Deve-se retirar os imóveis TST (teste) da planilha* [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0)*. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*

  \


⚠️

**Observação:** *Deve-se retirar os imóveis TST (teste) da planilha* [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0)*. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*



3. **Número de Limpezas**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha[04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1umoS7iPcPKeK-ieko2gLsNe_Yokgwkglsfc3ubtaNHU/edit?gid=1353793656#gid=1353793656) na aba Limpezas Mês;
  3. Filtrar a coluna Valor( O ) retirando todos os valores 0 e os espaços em branco, e conferir se a soma da coluna Número de Limpezas na aba Anfitrião é igual a contagem das linhas na aba Limpezas Mês.

  \
  ⚠️

  **Observação:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*

  ⚠️

  **Observação 2:** *Deve-se retirar os imóveis TST (teste) da planilha* [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0)*. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*


⚠️

**Observação:** *Deve-se retirar os imóveis TST (teste) da planilha* [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0)*. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*



4. **Valor de Limpezas**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1umoS7iPcPKeK-ieko2gLsNe_Yokgwkglsfc3ubtaNHU/edit?gid=1353793656#gid=1353793656) na aba Limpezas Mês;
  3. Conferir se a soma da coluna "Limpezas" na aba Anfitrião é igual a soma da coluna "Valor" aba Limpezas Mês.

  \
  ⚠️

  **Observação:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*

  ⚠️

  **Observação 2:** *Deve-se retirar os imóveis TST (teste) da planilha* *[01 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=1596704130)__. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*


⚠️

**Observação:** *Deve-se retirar os imóveis TST (teste) da planilha* *[01 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=1596704130)__. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*


\

5. **Receita Total**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Imóvel;
  3. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Proprietário;
  4. Conferir se a soma das colunas de Receitas da aba Imóvel é igual a soma da coluna de Receita na Aba Proprietário e igual a soma da coluna de Receita da Aba Anfitrião.
  5. Caso os valores não sejam os mesmos, analisar caso a caso.

  \
  ⚠️

  **Observação:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID do fechamento anterior na parte superior da aba antes de realizar qualquer comparação.*



6. **Despesas**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828)na aba Despesas Mês;
  3. Filtrar a coluna "Flag Anfitrião", na aba Despesas Mês, por FALSO e verificar o motivo dela estar falsa;
  4. Após solucionar os casos, filtrar a coluna "Tipo", na aba Despesas Mês, retirando tudo o que estiver como Gestão de Contas e filtrar a "Flag Anfitrião" retirando tudo o que deve permanecer como FALSO;
  5. Filtrar retirando Anfitrião Seazone das duas abas;
  6. Conferir se a soma das colunas de Despesas na aba Anfitrião é igual ao valor da soma das despesas da aba Despesas Mês (com os filtros do ponto 3, 4 e 5 aplicados).

  \
  ⚠️

  **Observação:** *Caso seja necessário, é possível verificar se as informações das despesas estão corretas na planilha* *[14 -BD despesas](https://docs.google.com/spreadsheets/d/1wL4SBGofNb04MH3nzWVmgus2evD26zUJaquuaR0wbCk/edit#gid=30783992)* *na aba Despesas.*

  ⚠️

  **Observação 2:** *Encontrar a causa, se necessário, no ponto 3, que podem envolver imóveis duplicados, anfitriões diferentes ou imóveis faltando na aba Anfitrião.*

  ⚠️

  **Observação 3:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*


⚠️

**Observação:** *Caso seja necessário, é possível verificar se as informações das despesas estão corretas na planilha* *[14 -BD despesas](https://docs.google.com/spreadsheets/d/1wL4SBGofNb04MH3nzWVmgus2evD26zUJaquuaR0wbCk/edit#gid=770690575)* *na aba Despesas (Legacy).*

⚠️

**Observação 2:** *Encontrar a causa, se necessário, no ponto 3, que podem envolver imóveis duplicados, anfitriões diferentes ou imóveis faltando na aba Anfitrião.*



7. **Ajustes**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Ajustes;
  3. Filtrar a coluna Proprietário/Anfitrião retirando todos os nomes PROP na aba Ajustes e conferir se a soma da coluna Ajustes na aba Anfitrião é igual a soma dos ajustes na aba Ajustes (com o filtro aplicado), caso não seja, analisar caso a caso.

  \
  ⚠️

  **Observação:** *Encontrar a causa, se necessário, no ponto 3, que podem envolver imóveis com o ID ou escrita errada, valores com formatação divergente, imóveis que não entraram no fechamento, imóveis que entraram duplicados ou com o nome do anfitrião escrito errado.*

  ⚠️

  **Observação 2:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*

  ⚠️

  **Observação:** *Encontrar a causa, se necessário, no ponto 3, que podem envolver imóveis com o ID ou escrita errada, valores com formatação divergente, imóveis que não entraram no fechamento, imóveis que entraram duplicados ou com o nome do anfitrião escrito errado.*



8. **Comissão Total**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Imóvel;
  3. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Proprietário;
  4. Conferir se a soma da coluna Comissão na aba Imóvel é igual a soma da coluna Comissão Total da aba Anfitrião e se é igual a soma da coluna Comissão da aba Proprietário.

  \
  ⚠️

  **Observação 2:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID da Conciliação na parte superior da aba antes de realizar qualquer comparação.*

  \



9. **Resumo Anfitrião**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Resumo Anfitrião;
  3. Conferir se todos os Anfitriões que estão na aba Anfitrião também estão na aba Resumo Anfitrião e aplicar todas as métricas de conferências anteriores entre as abas Anfitrião e resumo Anfitrião.

  \
  ⚠️

  **Observação:** *a aba Resumo Anfitrião deve ter os mesmos valores da aba Anfitrião.*


⚠️

**Observação:** *a aba Resumo Anfitrião deve ter os mesmos valores da aba Anfitrião.*


\

10. **Ajustes Diretos**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Resumo Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828)[s](https://docs.google.com/spreadsheets/d/1Tkf29uV4ZFZcbvjofAo_9IHVPri9XY5JlTBE3Pcu-jo/edit#gid=1615370528) na aba TxFranquia;
  3. Conferir se todos os anfitriões com taxa de franquia em aberto na aba TxFranquia estão com o abatimento feito na aba Resumo Anfitrião de acordo com o modelo de cobrança (parcela fixa ou desconto na comissão);
  4. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Ajustes e verificar todos os ajustes diretos (aqueles com um traço na coluna de imóvel) e, adicionar manualmente na aba Resumo Anfitrião todos os ajustes diretos anotados para os anfitriões a que se referem.


\

11. **Repasse**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Anfitrião;
  2. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Resumo Anfitrião;
  3. Verificar se o valor da coluna Repasse na aba Resumo Anfitrião é igual a soma da coluna Repasse da aba Anfitrião subtraindo a coluna Ajuste Direto na aba Resumo Anfitrião \[**Repasse** (aba Resumo Anfitrião) **= Repasse** (aba Anfitrião) **- Ajuste Direto** (aba Resumo Anfitrião)\].


**FLUXOGRAMAS DO PROCESSO**

Processo Tático

\[

https://lucid.app/lucidchart/a3c31d81-e689-4050-9d98-a724e6356d92/edit?from_internal=true

\](https://lucid.app/lucidchart/a3c31d81-e689-4050-9d98-a724e6356d92/edit?from_internal=true)


Métricas de Conferência

\[

https://lucid.app/lucidchart/9334ebae-74a0-45f2-a744-2a0f6c5bcd5d/edit?page=0_0#

\](https://lucid.app/lucidchart/9334ebae-74a0-45f2-a744-2a0f6c5bcd5d/edit?page=0_0#)


Ajustes Diretos

\[

https://lucid.app/lucidchart/e5a33ba8-9686-41cb-ba65-e2132c835416/edit?from_internal=true

\](https://lucid.app/lucidchart/e5a33ba8-9686-41cb-ba65-e2132c835416/edit?from_internal=true)


Liberação dos Repasses (Lista de TEDs)

\[

https://lucid.app/lucidchart/4fde02dd-83cf-4dc7-a7be-3445e8a5a790/edit?page=0_0&invitationId=inv_180c7bf4-649f-4579-9ce6-4146aee99d5d#

\](https://lucid.app/lucidchart/4fde02dd-83cf-4dc7-a7be-3445e8a5a790/edit?page=0_0&invitationId=inv_180c7bf4-649f-4579-9ce6-4146aee99d5d#)

\[

https://lucid.app/lucidchart/ff58381f-6653-4cc2-9a54-896c6c9a26bd/edit?page=0_0&invitationId=inv_b89afa78-8a29-4197-9c97-65a7c4dcc61a#

\](https://lucid.app/lucidchart/ff58381f-6653-4cc2-9a54-896c6c9a26bd/edit?page=0_0&invitationId=inv_b89afa78-8a29-4197-9c97-65a7c4dcc61a#)