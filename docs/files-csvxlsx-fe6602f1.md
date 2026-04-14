<!-- title: Files CSV/XLSX | url: https://outline.seazone.com.br/doc/files-csvxlsx-HY9beNwcv4 | area: Tecnologia -->

# Files CSV/XLSX

## Gerar arquivo XLSX

A função para gerar um arquivo XLSX de NF utiliza alguns parâmetros para buscar os dados no banco de dados converter no formato XLSX e enviar o arquivo para o S3 da AWS.

Dentro do processo de geração do arquivo XLSX, serão gerados dois tipos de arquivos com números de serviços diferentes. O arquivo com número 11778 contém as NF emitidas pela Seazone para os proprietários. Enquanto o arquivo com número 8761, tem a lista de informação para os anfitriões emitirem suas NFs.

Em posso dos dados das NFs para cada número de serviço, é alterado o cabeçalho das informações e o dataset é quebrado em *chunks* de no máxima 50 linhas. Esse processo é feito devido a limitação do sistema que o financeiro utiliza para enviar as NF. Cada *chunk* é salvo em um arquivo chamado `remessa-x.xlsx` e todos os arquivos são zipados em um arquivo por número de serviço e depois zipados novamente em um arquivo raiz que contém os 2 zips de serviços. Gerando 2 arquivos chamados `servico-11778.zip` e `servico-8761.zip` que ficaram dentro de um arquivo zip principal. Esse arquivo é enviados para a AWS para download.

## Gerar arquivo CSV

A função para gerar um arquivo CSV de NF utiliza alguns parâmetros para buscar os dados no banco de dados converter no formato CSV e enviar o arquivo para o S3 da AWS.

Depois de buscar os dados no banco, é feito um tratamento para renomear o cabeçalho e é preenchido o valor do código do IBGE da cidade através de uma base em formato JSON. Os dados então são convertidos para o formato CSV em um arquivo nomeado remessa-0.csv. Esse arquivo então é Zipado e enviado para a AWS.