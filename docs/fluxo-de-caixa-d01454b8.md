<!-- title: Fluxo de Caixa | url: https://outline.seazone.com.br/doc/fluxo-de-caixa-SAiMrcBCvj | area: Administrativo Financeiro -->

# Fluxo de Caixa

![](/api/attachments.redirect?id=3c70bb21-3642-4f83-ab58-32c8e26f7b9a)

🔮

# Fluxo de Caixa


Fluxo de Caixa: **[Link](https://docs.google.com/spreadsheets/d/186jBo44YP6xkJXurZ_dGujIaYuD1N1V1bU2Qz39TBtk/edit#gid=572634908)**

O Fluxo de Caixa foi elaborado para porporcional visibilidade dos valores a pagar e a receber de cada empresa e com isso é possivel projetar nosso caixa necessário e residual.

Por sua vez, a atualizar é 100% automática, composta pelas seguintes Abas:


1. REC_OTA: essa aba é alimentada através de uma [planilha auxiliar](https://docs.google.com/spreadsheets/d/1x7ENRNB-_XDCEmUo52AUW6QjlfCXZC-hq4QjT0SfkdM/edit#gid=620209482) que possui API com a tabela *[Reservation_Total Price](https://metabase.sapron.com.br/question/254-reservation-total-price)* do Metabases, onde reuni todas as reservas abertas por OTA e por data de recebimento (cash date) de acordo com a regra de negócio de cada OTA;
2. REC_FUTURO: a aba compila todos os recebimentos futuros com exceção das reservas, sendo os principais: Comissão de vendas, Reembolso da SPE e Estruturação. Essa aba tem como origem os dados do [Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047);
3. CONSOLIDADO_PGTO: com origem na planilha [Controle CPG](https://docs.google.com/spreadsheets/d/12jFzCTYAISO2xVBFcC6YkDehBmR2m5ymYGcwQnU3fhA/edit#gid=1490415092). O foco aqui é compilar todas as solicitações de pagamentos vindas por requisições via formulário ou solicitações de outros setores, como RH e pagamento de variáveis do Comercial;
4. PGTO_RECORRENTES: os dados dessa aba também são colhidos da planilha Controle CPG, porém utilizamos as informações apenas dos pagamentos parcelados e recorrentes, como os Sistemas Integrados de Gestão (S.I.G.) pagamos por boleto e os impostos previstos;
5. REMUNERAÇÃO: outra aba que conecta-se com a Controle CPG, porém, desta vez, buscando os dados apenas dos colaboradores para que possamos vincular a previsão dos pagamentos de remunerações;
6. REPASSES: por fim, temos a aba de repasses, que provisiona de forma automática, buscando da *[2.0 BizOps - Fechamento Mensal Template - BizOps](https://docs.google.com/spreadsheets/d/1sgTsWUupuWscD6dYT1Lh0kfZgZjlGOmrKkTX4Nr4Hac/edit#gid=940361953)* os valores previstos de repasses para proprietários e anfitriões, separados no dia 05 e 10 do mês.