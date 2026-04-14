<!-- title: Fechamento Imóvel | url: https://outline.seazone.com.br/doc/fechamento-imovel-ICOl7GDZej | area: Administrativo Financeiro -->

# Fechamento Imóvel

![](Fechamento%20Imo%CC%81vel%2050dfed6c02dd486a83866820246ef2a6/FUNDOS_TRELLO_5_(1).png)

🏠

# Fechamento Imóvel


\
**DESCRIÇÃO**

ℹ️

O Fechamento de Imóvel consiste em compilar os dados das reservas que ocorreram ao longo do mês, assim como, os valores de saldos, taxas de implantação e ajustes. É a partir dele que surgem os valores de repasse dos proprietários e anfitriões.


**PRAZO**

⏰

O Fechamento do Imóvel deverá ser realizado nos **primeiros cinco dias úteis do mês**, a partir do momento em que as macros finais de conciliação e a de imóvel na planilha de fechamento são rodadas.


**ALTERAÇÃO TEMPLATE DE FECHAMENTO**

* **Passo a passo**

  
  1. Acessar a aba Dashboard da planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) e alterar:
  * O "Mês Atual" para a data de referência do fechamento atual;
  * O "ID Conciliação" para ID da Conciliação de referência do fechamento atual;
  * O "ID Fechamento Passado" para o ID da planilha de fechamento do fechamento anterior ao do fechamento atual.

  \
  ⚠️

  **Observação 1:** O ID das planilhas (Conciliação e Fechamento) são encontrados no link da planilha entre barras. A seguir, vemos um exemplo, onde a parte pintada em azul é o ID da planilha acessada:\n\n- https://docs.google.com/\nspreadsheets/d/15Je5soLIH9qCZs2t40_k0OXJn1D3in9-fBhJkzkEx68/edit#gid=1920421574

  ⚠️

  **Observação 2:** Os fechamentos anteriores podem ser encontrados no [Histórico Fechamentos](https://drive.google.com/drive/folders/1csgpu2PaB15XOvTuvXcdmBszo-l5xM2z).

  ⚠️

  **Observação 3:** A Conciliação pode ser encontrada no [Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp).


**DIVISÃO DE TROCAS**

ℹ️

Realizar a divisão das reservas de acordo com os casos de trocas de proprietário.

* **Passo a passo (Plano A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828);
  2. Rodagem da Macro **Imovel 2.**

  \
* **Passo a passo (Plano B)**

  
  1. Acessar a planilha [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=135477343) na aba Troca de proprietários;
  2. Acessar a pasta [Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp) e selecionar a planilha com a data de referência do fechamento atual;
  3. Acessar a aba Conciliação Fechamento para fins de conferência e quebra;
  4. Acessar o [Sapron](https://sapron.com.br/fechamentoimovel) na aba Fechamento Imóvel e verificar se de acordo com a data da troca do proprietário, a divisão das reservas está correta e anotar a proporção das reservas na aba Troca de proprietários na coluna "Observação";
  5. Caso a divisão das reservas não esteja correta, deve-se acessar o [Suporte do Sapron](https://suportesapron.atlassian.net/servicedesk/customer/portals) e abrir uma solicitação de suporte para correção.
  6. Caso o antigo proprietário ainda possua valores, deve-se acessar a planilha [Plano de Contingência](https://docs.google.com/spreadsheets/d/1daMGyKDwmwK1mQPvVX8E9cknJxKKaidqi7m16TAKgvA/edit#gid=1333715817) na aba Apartment e ativar o imóvel à força na coluna Ativar a Força;
  7. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) e rodar pela última vez a macro de imóvel \[ir no menu superior e clicar em Fechamento → Atualização de Abas → Imóvel (Do Início ou Continuação, a depender do caso)\]
  8. Acessar a aba Imóvel e quebrar as colunas de receita, faturamento, despesa e ajustes de acordo com a data de troca (lembrando de conferir a comissão de cada proprietário na planilha [Plano de Contingência](https://docs.google.com/spreadsheets/d/1daMGyKDwmwK1mQPvVX8E9cknJxKKaidqi7m16TAKgvA/edit#gid=1333715817) na aba Apartment);
  9. Após as conferências acima, ainda na aba Imóvel:
  * Adicionar a letra "O" no código do imóvel do **proprietário antigo ou daquele que não tenha saldo inicial** para melhor identificação (Exemplo: se o código era "OPA234" ele será "OPAO234");

  
  10. Efetuar a mesma quebra de receita, limpezas, comissão e despesas na aba Anfitrião, de acordo com a data de troca.

  \
  ⚠️

  **Observação:** as reservas antes da data da troca são do proprietário antigo e as reservas depois da data da troca, são do proprietário novo e deve-se atentar às reservas de booking e expedia devido a regra 30+.


**MÉTRICAS DE CONFERÊNCIA**

ℹ️

São métricas de conferências aplicadas durante o processo para precaver erros e trazer mais segurança nos dados apontados no Fechamento de Imóvel.



1. **Imóveis sem Anfitrião**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Dashboard;
  2. Ir no menu superior e clicar em Fechamento → Atualização de Abas → Imóvel (Do Início);
  3. Após a rodagem da macro, deve-se acessar a aba Imóvel (ainda na mesma planilha);
  4. Filtrar a coluna C (Anfitrião) e selecionar "Espaços em branco" para verificar se algum imóvel ainda está sem anfitrião;
  5. Em caso de existirem imóveis sem anfitrião, acessar a planilha [Relação Imóvel x Anfitrião](https://docs.google.com/spreadsheets/d/1W_a4KKvl-UKzH3ma5bzAWHG1amRPmEpVHfX-KqFmtBw/edit#gid=1582638460) na aba Relação 2.0 e apagar as linhas do mês de referência do fechamento e clicar em **Import** na coluna A para rodar a macro novamente;
  6. Rodar novamente a macro Imóvel na aba Dashboard após as verificações/atualizações.

  \
  ⚠️

  **Observação 1:** *para rodar a macro, em alguns momentos, será necessário realizar uma autorização. Caso isso aconteça, após autorizar, é necessário repetir o passo 2.*


⚠️

**Observação 1:** *para rodar a macro, em alguns momentos, será necessário realizar uma autorização. Caso isso aconteça, após autorizar, é necessário repetir o passo 2.*


\

2. **Conferência dos Saldos**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Saldos;
  2. Filtrar a coluna "Flag Verificação" como FALSO e analisar se esses saldos realmente não deveriam entrar no Fechamento **(avaliar caso a caso)**;
  3. Após essa análise, conferir se a soma da coluna "Saldo Inicial" na aba Imóvel é igual à soma das colunas "Saldo Inicial Seazone" + "Saldo Inicial Onboarding" na aba Saldos (em caso de divergência investigar o motivo para solucioná-lo);
  4. Acessar a planilha [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba "Saldos em conta props" e filtrar a coluna "Mês" pela data de referência do fechamento atual e retirar os imóveis que se mantiveram com a flag "FALSO" do passo 2;
  5. Conferir se o resultado encontrado no ponto 3 é igual a soma das colunas "Saldo Inicial Seazone" + "Saldo Onboarding (Taxa Implantação)" na planilha [04 - Conciliação futura e verificações](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba "Saldos em conta props" (em caso de divergência investigar o motivo para solucioná-lo).

  \
  ⚠️

  **Observação:** *Encontrar a causa, se necessário, no ponto 2, que podem envolver imóveis com o ID errado, valores com formatação divergente, imóveis que não entraram no fechamento ou imóveis que entraram duplicados.*

  ⚠️

  **Observação 2:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID do fechamento anterior na parte superior da aba antes de realizar qualquer comparação.*


⚠️

**Observação:** *Encontrar a causa, se necessário, no ponto 2 que podem envolver imóveis com o ID errado, valores com formatação divergente, imóveis que não entraram no fechamento ou imóveis que entraram duplicados.*



3. **Valores das OTAs**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Imóvel e conferir:
  * Se a soma da coluna receita é igual a coluna faturamento da OTA Stays (Q = J);
  * Conferir se a soma da coluna receita é igual a coluna faturamento da OTA Airbnb (E = F);

  
  2. Acessar a planilha do fechamento do mês anterior na pasta de [Históricos de Fechamentos](https://drive.google.com/drive/folders/1csgpu2PaB15XOvTuvXcdmBszo-l5xM2z) e conferir:
  * Se a soma da coluna receita no fechamento atual é igual a coluna faturamento no fechamento anterior da OTA Booking (M atual = H anterior);
  * Se a soma da coluna receita no fechamento atual é igual a coluna faturamento no fechamento anterior da OTA Expedia (O atual = J anterior);

  
  3. Se houver divergência em alguma OTA, encontrar quais os imóveis e o padrão para consertar (Ex. inserção dos novos, macro, realocação);
  4. Rodar novamente a macro Imóvel na aba Dashboard da planilha de [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) após a referida atualização.

  \
  ⚠️

  **Observação:** *Deve-se desconsiderar a conferência das colunas de Homeaway e das colunas de Contrato, pois os valores devem ser igual à 0,00.*

  ⚠️

  **Observação 2:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID do fechamento anterior na parte superior da aba antes de realizar qualquer comparação.*


⚠️

**Observação:** *Deve-se desconsiderar a conferência das colunas de Homeaway e das colunas de Contrato, pois os valores devem ser igual à 0,00.*


\

4. **Receita Total**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Imóvel;
  2. Acessar a planilha Conciliação Reservas Sapron do mes de referencia na aba Conciliação Fechamento;
  3. Conferir se a soma de todas as colunas referente à receita das OTAs na aba imóvel da planilha de Fechamento é igual a soma da coluna "Valor Diárias Mês" na aba Conciliação Fechamento.

  \
  ⚠️

  **Observação:** *Deve-se retirar os imóveis TST (teste) da planilha* [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0)*. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*

  ⚠️

  **Observação 2:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID do fechamento anterior na parte superior da aba antes de realizar qualquer comparação.*

  \
  ⚠️

  **Observação:** *Deve-se retirar os imóveis TST (teste) da planilha* [04 - Conciliação Reservas Sapron](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=0)*. A planilha que deve ser utilizada é a cópia mais recente presente no* *[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)__.*



5. **Despesas**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Despesas Mês;
  2. Filtrar a coluna "Quem Paga" por "Proprietário";
  3. Verificar na coluna de "Flag Fechamento Imóvel" se todos as despesas estão como 1 (inclusas no fechamento), e caso não, encontrar qual o motivo;
  4. Após resolvido qualquer situação com as flags, retirar os imóveis que devem permanecer com a flag 0;
  5. Acessar a aba Imóvel da planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) e conferir se o valor da coluna Despesas (Despesas Anfitrião + Despesas Seazone) é igual ao valor da soma das despesas da aba "Despesas Mês" (com o filtro aplicado no passo 2 e 4);
  6. Acessar a planilha [14 -BD despesas](https://docs.google.com/spreadsheets/d/1wL4SBGofNb04MH3nzWVmgus2evD26zUJaquuaR0wbCk/edit#gid=30783992) na aba Despesas;
  7. Filtrar a coluna Data por todas as datas do mês de referência atual (dia primeiro até o último dia do mês), em seguida filtrar a coluna Status por "Approved" e em seguida a coluna Quem Paga por "Proprietário", retirando os imóveis que a flag deve permanecer 0;
  8. Conferir se na aba "Despesas Mês" da planilha de Fechamento o valor é igual ao valor presente na aba "Despesas" da planilha BD despesas.

  \
  ⚠️

  **Observação:** _Caso a "_*Flag Fechamento Imóvel" esteja igual a 2, a despesa estará duplicada na aba Imóvel, e se a flag estiver igual a 0, a despesa não terá entrado na aba Imóvel.*

  ⚠️

  **Observação 2:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID do fechamento anterior na parte superior da aba antes de realizar qualquer comparação.*


⚠️

**Observação:** _Caso a "_*Flag Fechamento Imóvel" esteja igual a 2, a despesa estará duplicada na aba Imóvel, e se a flag estiver igual a 0, a despesa não terá entrado na aba Imóvel.*


\

6. **Saldo Mês**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Dashboard;
  2. Conferir no gabarito presente nessa aba se o valor da soma da coluna de "Saldo mês", é igual a soma das colunas de Receitas das OTAs menos o total da coluna de despesas e menos o total da coluna de comissão na aba imóvel (Saldo = Receita - Despesas - Comissão).

  \
  ⚠️

  **Observação:** *Conferir manualmente na aba Imóvel, caso seja necessário.*



7. **Ajustes**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Imóvel;
  2. Acessar a aba Ajustes na planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) ;
  3. Filtrar a coluna Proprietário/Anfitrião por "PROP" e conferir se a soma da coluna Ajustes na aba Imóvel é igual a soma da coluna "Valor" na aba Ajustes (com o filtro aplicado);
  4. Caso o valor seja divergente, analisar caso a caso.

  \
  ⚠️

  **Observação:** *É possível realizar essas comparações diretamente pelos gabaritos presentes na aba Dashboard. Lembrar de atualizar os ID do fechamento anterior na parte superior da aba antes de realizar qualquer comparação.*

  ⚠️

  **Observação 2:** *Encontrar a causa, se necessário, no ponto 2 que podem envolver imóveis com o ID ou escrita errada, valores com formatação divergente, imóveis que não entraram no fechamento ou imóveis que entraram duplicados.*


⚠️

**Observação:** *Encontrar a causa, se necessário, no ponto 2 que podem envolver imóveis com o ID ou escrita errada, valores com formatação divergente, imóveis que não entraram no fechamento ou imóveis que entraram duplicados.*



8. **Valor Repasse**

* **Passo a passo (PLANO A)**

  
  1. Acessar a planilha [3.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) na aba Dashboard;
  2. Conferir no gabarito presente nessa aba se o valor da coluna "Repasse" é igual ao valor da soma das colunas "Saldo Mês", "Ajustes" e "Saldo Inicial Seazone" (Repasse = Saldo Mês + Ajustes + Saldo Inicial Seazone).

  \
  ⚠️

  **Observação:** *Conferir manualmente na aba Imóvel, caso seja necessário.*.


\
**FLUXOGRAMAS DO PROCESSO**

Processo Tático

\[

https://lucid.app/lucidchart/c696772f-509b-4622-a49e-9c3e1d38cbb3/edit?page=0_0&invitationId=inv_e549dc8b-c0c7-4ca1-9907-c4d848e57118#

\](https://lucid.app/lucidchart/c696772f-509b-4622-a49e-9c3e1d38cbb3/edit?page=0_0&invitationId=inv_e549dc8b-c0c7-4ca1-9907-c4d848e57118#)