<!-- title: Franquia - Inserção de Taxa de Franquia | url: https://outline.seazone.com.br/doc/franquia-insercao-de-taxa-de-franquia-vCise1bIYU | area: Tecnologia -->

# Franquia - Inserção de Taxa de Franquia

**Instruções para registro de Taxas de Franquia**

* Os valores referentes às taxas de franquia cobradas, pagas (via PIX), descontos concedidos ou dívidas perdoadas deverão ser registrados mensalmente utilizando [esta planilha](https://docs.google.com/spreadsheets/d/1AhZo2AmzXjJLSbRfHDsqv8qT1i99IZXmzaLFYEuE_7U/edit?gid=1805712756#gid=1805712756) template.

**Preenchimento da Planilha Template**

* Na primeira linha do template, há comentários detalhando como preencher cada coluna. **Atente-se** às instruções de formato e valores especificados.

**Registro dos Valores**

* Após o preenchimento correto da planilha, os dados serão utilizados para povoar o banco de dados por meio de uma query. Essa operação irá atualizar a tabela: [Financial Host Franchise Fee Payment](https://metabase.sapron.com.br/question#eyJkYXRhc2V0X3F1ZXJ5Ijp7ImRhdGFiYXNlIjoyLCJ0eXBlIjoicXVlcnkiLCJxdWVyeSI6eyJzb3VyY2UtdGFibGUiOjIzOX19LCJkaXNwbGF5IjoidGFibGUiLCJ2aXN1YWxpemF0aW9uX3NldHRpbmdzIjp7fX0=)

**Tabela Financial Host Franchise Fee Payment**

* Esta tabela contém **todos os valores** de taxas de franquia cobradas, **inclusive retroativos.**
* Os métodos de pagamento podem ser filtrados na coluna Payment Method.

**Métodos de Pagamento Disponíveis**

* **debit**: Pagamento via PIX. Utilize este método para valores que não são abatidos da comissão do anfitrião.
* **discount**: Dívidas perdoadas ou descontos concedidos. Use este método para registrar valores que foram perdoados ou oferecidos como desconto.
* **commission_abatement**: Abatimento da taxa de franquia na comissão. Este método deve ser utilizado para valores cobrados no mês e abatidos diretamente da comissão do anfitrião.


\