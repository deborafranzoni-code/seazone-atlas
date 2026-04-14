<!-- title: Setup Groups | url: https://outline.seazone.com.br/doc/setup-groups-ZtOUsOP7Us | area: Tecnologia -->

# Setup Groups

O módulo de setup groups tem o objetivo de identificar discrepâncias entre os anúncios em inputs do Sirius e os anúncios na Stays. A implementação deste módulo se encontra dentro do repositório api-stays (abrange integração Sheets ↔ AWS e AWS ↔ Stays), pois seu funcionamento está concentrado em um único Lambda ativado pelo Sheets através de uma chamada de API.

Github: [api-stays](https://github.com/Khanto-Tecnologia/api-stays)

## Funcionamento

O módulo de setup groups é executado através de uma chamada do tipo PUT no método setup-groups/make-diff da API de comunicação com o sheets realizada diretamente na [aba de inputs](/doc/comunicacao-e-dados-aWFByTFvPo).

### Aba Grupos:

* Os inputs são postos de forma manual nas colunas "Lista de Imóveis" (id do imóvel) e "Lista de Grupos" (grupo do imóvel)
* A data e hora da última execução do processo se encontra em "Última execução"
* O status e, caso tenha, descrição do erro, da última execução se encontra em "Status última execução"
* Apesar do processo rodar de maneira automática todo dia às 7:00h, também é possível executa-lo de forma manual clicando no botão "Executar"

 ![Untitled](/api/attachments.redirect?id=367ea6a2-b785-4958-8bf8-a98d2bdc70a7)

### Aba Warnings:

* Os Warnings são escritos nas colunas "Imóvel" (id do imóvel) e "Warning" (motivo do imóvel estarem warnings)
* A coluna "Warning" possui dois valores: "Faltando" quando o imóvel está na Stays porém não nos inputs e "Sobrando" quando o imóvel está nos inputs porém não na Stays

 ![Untitled](/api/attachments.redirect?id=187708f7-9bf0-45b4-9882-618f7a746617)