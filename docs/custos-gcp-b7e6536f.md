<!-- title: Custos GCP | url: https://outline.seazone.com.br/doc/custos-gcp-qzdCbjrJ90 | area: Tecnologia -->

# Custos GCP

Arquivo criado por conta de termos notado um billing acima do esperado no GCP, a partir disso resolvemos agir em conjunto com o time de dados nos projetos que mais estavam gerando custo para atuar em cima de otimizações, nesse documento traremos informações sobre as melhorias encontradas e ações tomadas em cima de cada um desses projetos 


## Seazone Tools

**Ações Executadas** :white_check_mark:

* **Remoção do Redis (Memory Store) do Chatwoot:** A instância foi removida pois o serviço não estava em uso ativo, eliminando um custo fixo de **$35,77/mês**.
* **Redimensionamento do Memory Store (Baserow):** A instância foi reduzida de 2GB para 1GB. O monitoramento indicou que o uso de memória era baixo e 1GB atende à demanda atual com folga. **Economia: $35,77/mês.**
* **Limpeza de IPs Estáticos:** Foram liberados 3 endereços IP externos que não estavam associados a nenhuma instância (remanescentes de testes e do Pritunl antigo). **Economia: $24,00/mês.**
* **Exclusão de Disco Persistente (Pritunl):** Identificado e removido um disco rígido sem uso, provavelmente vinculado a uma instância antiga já deletada. **Economia: $4,84/mês.**
* **Desativação do Cloud SQL (Kestra):** O banco de dados do Kestra foi removido por não estar sendo utilizado, sendo este o item de maior impacto individual. **Economia: $115,62/mês.**
* **Otimização do Cloud SQL (Tools):** Este banco (que atende Baserow e Outline) apresenta uso de CPU em 20% e memória em 30%. Foi realizado o redimensionamento para um tier menor, mantendo uma margem de segurança de 50% acima do uso comum para suportar picos.
  * **Economia estimada:** **$121,62/mês.**
  * **obs:** A execução foi  feita no período noturno, pois o ajuste exigiu o restart da instância.

**Ações Previstas** :hourglass:

• **Right-sizing da Instância Vault:** O monitoramento de performance mostra que a máquina utiliza apenas 15% de CPU/Memória. Planejo alterar o tipo de máquina para `e2-small` conforme recomendação do GCP, o que reduz o custo em **$11,99/mês** sem comprometer a operação. Essa não foi executada ainda, por que como depende do restart da máquina tem que ser averiguado o modo como a aplicação está rodando dentro da instância para ser executado

* Adicionar baserow no memory store de tools e remover memory store do baserow, economia de cerca 

**Resultados**

* Já tivemos um impacto no billing diário, que desceu de uma média de 300R$ diários para algo em torno de 250$, se mantendo nesssa casa a redução mensal esperada em janeiro em comparação com dezembro é  de cerca de 1500$, no forecasted aponta que teremos cerca de 2k de redução em janeiro comparando ocm dezembro, provavelmente por que taxas são levadas em conta 

 ![](/api/attachments.redirect?id=8a35f4b1-7022-4e2e-88b8-02403c923e6c " =1254x323")

## **Data Resources**

**Ações Executadas ✅**

* **Redução dos recursos do banco data-resources :** A instância rodava com 2 vCPU e 8 GB, agora está com **1 vCPU e 3.75 GB**.

**Ações Previstas ⌛**

* Organizar o Artifact Registry, excluindo imagens e versões de imagens ociosas
* Alteração de buckets de Multi-region para Region, resultando em redução de custo em "Multi-Region Standard Class A Operations" (estimativa de R$ 86,46/mês)

**Resultados**

* Redução dos recursos do banco terá um impacto de aproximadamente 99/mês, representando uma economia de 51% em comparação com o custo do banco na configuração anterior


## **Revenue Management**

**Ações Executadas** :white_check_mark:

* Ajuste no fluxo utilizado por RM para otimizar o uso da api do Gemini, aumentando o rate de requisições que fazemos 

## Sandbox

**Ações Executadas ✅**

* **Remoção de 6 elastic IPs** que não estavam alocados a nenhum recurso, gerando cerca de R$42 de economia mensal 
* **Remoção de load balancer** de teste que não estava em uso, economizando cerca de R$18,25 por mês 
* **Remoção de duas cloud functions** de teste, economizando cerca de R$130 por mês 

**Ações Previstas ⌛**

* migrar buckets **projeto-panorama-dados** e **image-scraper para contas de dados** 


## **Projeto Lake (dev, prd e stg)**

**Ações Previstas ⌛**

* **Remover Cloud Storage**: Eliminar dados antigos da migração do Lake, resultando em uma economia mensal de R$ 478.
* **Remover Compute Engine**: Desativar instância do Redis usada em uma solução de scraper implementada pela Servi, com economia aproximada de R$ 130 mensais.
* **Remover BigQuery**: Eliminar armazenamento de dados do Lake no BigQuery, com economia aproximada de R$ 48 mensais.
* **Remover Artifactory**: Desativar armazenamento de imagens de scrapers, gerando uma economia de R$ 11 mensais.
* **Migrar processo de checagem de proxy e remover o projeto relacionado**.


## Seazone Investimentos

**Ações Executadas ✅**

* Redução da instancia em modo enterprise plus para enterprise
* 1vcpu e 

**Ações Previstas ⌛**

* \

**Resultados**


\
## Todos os Projetos

### Suporte Enhanced

Atualmente existe um plano contratado no GCP de Suportes nível Enhanced, custando mais de 500 reais com taxas por mes