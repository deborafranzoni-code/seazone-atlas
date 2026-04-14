<!-- title: Configuração de máquinas | url: https://outline.seazone.com.br/doc/configuracao-de-maquinas-jUIfiqIyiL | area: Tecnologia -->

# Configuração de máquinas

Para configurar o auto-scale das máquinas, atualmente utilizamos o karpenter e o aws auto-scaler.


## Auto Scaler Aws - Node Group

A configuração do auto-scaler é feita na aws e atualmente conta com 2 máquinas t3-medium. A configuração foi aplicada via terraform, então em caso de alteração o arquivo terraform esta neste [diretório](https://github.com/seazone-tech/terraform/tree/main/Production/Eks) do repositório [terraform](https://github.com/seazone-tech/terraform).


## Karpenter

A configuração do karpenter é realizada via arquivos de configuração yaml. Neste arquivo você pode configurar as máquinas que podem ser provisionadas, delimitando a quantidade de cpu, memória, familia e até o nome. Atualmente por motivos de previsibilidade nos custos optamos em utilizar o nome das máquinas para o Karpenter. A configuração é divida por tipo de workload e esta neste [diretório](https://github.com/seazone-tech/terraform/tree/main/Production/Helms/karpenter).



| Node Pool | Máquinas | Arch | Zonas | Limits |
|----|----|----|----|----|
| Apps | "t4g.medium","t3.medium","t3a.medium","t4g.large","t3.large" | amd64 | A,B e C | cpu=20 |
| Monitoring | "r8g.xlarge","r7g.xlarge","r6g.xlarge" | arm64 | A | cpu=20 |
| tools | "m8g.large","t4g.large","t4g.medium","t3.large" | amd64,arm64 | A,B e C | cpu=20 |


\