<!-- title: Analise de Custos NatGateway | url: https://outline.seazone.com.br/doc/analise-de-custos-natgateway-nn7XMq6cdV | area: Tecnologia -->

# Analise de Custos NatGateway

# Problema

Após a migração do cluster para a região de São Paulo (sa-east-1) em setembro de 2025, identificamos um custo significativo de SAE1-NatGateway-Bytes que não existia anteriormente. A análise revelou que o custo estimado apenas de processamento de dados através dos NAT Gateways em setembro foi de aproximadamente $1,765.84, processando cerca de 18.99 TB de dados.


---

# Analise de custos:

De acordo com os gráficos de custos abaixo, houve um pico significativo em setembro de 2025, com destaque para:

* SAE1-NatGateway-Bytes: Novo custo que apareceu após a migração
* Custo total do SAE1-NatGateway-Bytes em $1,765.84 vs custo total de USW2-NatGateway-Bytes em $10.82

 ![](/api/attachments.redirect?id=c78b45be-3a28-4861-9ad2-9d0cec61208d " =1628x644")

 ![](/api/attachments.redirect?id=e4aa776a-55c7-4847-b115-101850bbdfca " =1622x574")

 ![](/api/attachments.redirect?id=90bfde46-887a-4992-b308-08f321866541 " =1623x373")



---

# Comparando arquiteturas

## São Paulo (sa-east-1) - Configuração Atual

**VPC:** `vpc-0548553c6551bf056` (10.0.0.0/16) - `general-vpc`

**NAT Gateways:**

* `nat-0f8479d7cc5022dff` (sa-east-1a) - subnet-056a375af8b46533b
* `nat-0eb13a8f05f1fcdc4` (sa-east-1b) - subnet-0f7cae94337120b90
* **Status:** Ativos

**Subnets:**

* 2 subnets privadas (1a, 1b) - onde rodam as instâncias EKS
* 2 subnets públicas (1a, 1b) - onde ficam os NAT Gateways

**VPC Endpoints:** **0 CONFIGURADOS**

**EKS:**

* Cluster: `general-cluster`

**Route Tables (Privadas):**

* `rtb-068e11f2d5bff30f3` (subnet-0738d4978d18db909)
* `rtb-0cd3c45875103bf22` (subnet-09b73b4549a184bf5)

```json

Routes:
  - 10.0.0.0/16 → local
  - 205.0.0.0/16 → peering/tgw
  - 10.2.56.0/23 → peering/tgw
  - 0.0.0.0/0 → NAT Gateway (todo o resto vai para o NAT)
```

## Oregon (us-west-2) - Configuração Anterior

**VPC:** `vpc-0b001c93e1cbfa59d` (205.0.0.0/16) - `vpc-seazone-cluster-production`

**NAT Gateways:**

* `nat-0518fc8730e65faad` (us-west-2a) - subnet-0260750d7357e47f3
* **Status:** Ativo

**Subnets:**

* 5 subnets privadas (2a, 2b, 2c) - múltiplas por AZ
* 3 subnets públicas (2a, 2b, 2c)

**VPC Endpoints:** **1 CONFIGURADO**

* `vpce-0ef62df2bc3d6cbd0` - S3 Gateway Endpoint
* Tipo: Gateway (sem custo adicional)
* Associado às route tables privada e pública

**EKS:**

* Cluster: `eks_seazone_prod`

**Route Tables (Privadas):**

* `rtb-0be6f648c76a85739` (subnet-0a796ed197d1fd55f)
* `rtb-0860cc538daba1ae8` (subnet-015c34cf458c345fe)

```json

Routes:
  - 205.0.0.0/16 → local
  - 10.0.0.0/16 → peering/tgw
  - 10.2.56.0/23 → peering/tgw
  - 172.31.0.0/16 → peering/tgw
  - 0.0.0.0/0 → NAT Gateway (todo o resto vai para o NAT)
  - S3 → vpce-0ef62df2bc3d6cbd0 (VPC Endpoint)
```


---

# O que são os custos de NAT Gateway e as labels (SAE1-NatGateway-Bytes e USW2-NatGateway-Bytes)

## Conceito

O NAT Gateway (Network Address Translation Gateway) é um serviço gerenciado da AWS que permite que instâncias em sub-redes privadas acessem a internet ou outros serviços da AWS, mantendo-se inacessíveis a conexões de entrada não solicitadas.

## Como funciona

O NAT Gateway atua como um intermediário entre as sub-redes privadas e a internet:


1. **Tráfego de Saída**: Instâncias em sub-redes privadas enviam tráfego para o NAT Gateway
2. **Tradução de Endereços**: O NAT Gateway traduz endereços IP privados para um IP público
3. **Roteamento**: O tráfego é roteado para a internet ou serviços AWS
4. **Resposta**: As respostas retornam pelo mesmo caminho, sendo traduzidas de volta para IPs privados

## Labels SAE1-NatGateway-Bytes e USW2-NatGateway-Bytes

Essas labels representam **Usage Types** no AWS Cost Explorer:

* **SAE1-NatGateway-Bytes**: Dados processados pelo NAT Gateway na região **South America East 1** (São Paulo)
* **USW2-NatGateway-Bytes**: Dados processados pelo NAT Gateway na região **US West 2** (Oregon)

### Estrutura da Label:

* **SAE1/USW2**: Código da região AWS
* **NatGateway**: Serviço específico
* **Bytes**: Unidade de medida (dados processados)

## Como é calculado

### Componentes de Custo:


1. **Cobrança por Hora**: $0.045/hora por NAT Gateway provisionado
2. **Cobrança por Processamento de Dados**: $0.045/GB de dados processados

### Fórmula de Cálculo:

```
Custo Total = (Horas × $0.045) + (GB Processados × $0.045)
```

### Exemplo Prático:

* **NAT Gateway ativo**: 730 horas/mês
* **Dados processados**: 18,987.55 GB (setembro 2025)
* **Cálculo**:
  * Cobrança horária: 730 × $0.045 = $32.85
  * Cobrança por dados: 18,987.55 × $0.045 = $854.44
  * **Total**: $887.29

## O que causa esse custo

### Principais Causas:


1. **Tráfego para Serviços AWS**: Acesso a S3, ECR, SSM, STS sem VPC Endpoints
2. **Tráfego de Internet**: Downloads, updates, APIs externas
3. **Tráfego entre Regiões**: Comunicação entre clusters em diferentes regiões
4. **Tráfego de Monitoramento**: Logs, métricas, telemetria

### Fatores que Aumentam os Custos:

* **Volume de Dados**: Quanto mais dados processados, maior o custo
* **Múltiplos NAT Gateways**: Cada AZ com NAT Gateway separado
* **Ausência de VPC Endpoints**: Tráfego AWS passando pelo NAT Gateway
* **Tráfego Desnecessário**: Aplicações fazendo requests desnecessários

### Estratégias de Redução:


1. **VPC Endpoints**: Redirecionar tráfego AWS para endpoints privados
2. **Otimização**: Reduzir tráfego desnecessário
3. **Monitoramento**: Identificar padrões de uso com VPC Flow Logs


---

# Causa Raiz dos Custos Elevados

Após analise e comparação de arquiteturas foi identificado que a principal causa dos custos elevados de SAE1-NatGateway-Bytes na região de São Paulo é a ausência de VPC Endpoints.

* Impacto: Todo o tráfego entre o cluster EKS e serviços essenciais da AWS (como S3, ECR, etc.) estava sendo roteado através do NAT Gateway, gerando custos desnecessários de processamento de dados.
* Custo: $0.052/GB processado através do NAT Gateway

## Analise do terraform

Foi constatado que o módulo Terraform da VPC, apesar de ter as variáveis para endpoints habilitadas no arquivo terragrunt.hcl, não estava efetivamente criando os recursos. O módulo VPC existente atuava como um wrapper simplificado e não possuía a lógica para criar VPC Endpoints, ignorando as configurações definidas no terragrunt.hcl.

[==https://github.com/seazone-tech/terraform-governanca/pull/18==](https://github.com/seazone-tech/terraform-governanca/pull/18)

# Solução Implementada

Foi criado um novo módulo Terraform em `production-711387131913/modules/aws/vpc-endpoints/` e em seguida foi criado o arquivo `production-711387131913/global/vpc-endpoints/terragrunt.hcl`. que instrui o terragrunt a provisionar os endpoins essenciais (S3, ECR API, ECR DKR, SSM, STS) usando o novo modulo.

# Resultados esperados

Redução Drástica de Custos: O tráfego para o S3, que é o maior contribuinte para os custos de NAT Gateway, será redirecionado através do Gateway Endpoint, eliminando quase todo o custo de processamento de dados do NAT Gateway.

Melhora na Segurança: O tráfego para os serviços AWS não precisará mais sair para a internet pública via NAT Gateway. Ele permanecerá dentro da rede privada da AWS, reduzindo a exposição a ameaças.

Melhora na Performance: A comunicação com os serviços da AWS através dos endpoints geralmente oferece menor latência e maior largura de banda em comparação com o acesso via internet.

# Validação

## Testes executados dentro do cluster


1. **Teste de Conectividade com a Internet:**
   * **Comando:** `ping -c 3 8.8.8.8`
   * **Resultado:** **Sucesso.**
   * **Análise:** Confirmou que o pod tinha uma rota funcional para a internet pública através do NAT Gateway, estabelecendo uma linha de base.
2. **Teste de Conectividade com o S3:**
   * **Comando:** `wget -q --spider https://s3.sa-east-1.amazonaws.com`
   * **Resultado:** **Sucesso.**
   * **Análise:** Confirmou que o pod conseguia estabelecer uma conexão HTTPS com o serviço S3, provando que o serviço estava acessível.
3. **Teste de Rota de Rede para o S3:**
   * **Comando:** `traceroute s3.sa-east-1.amazonaws.com`
   * **Resultado:** **Timeouts após o primeiro salto, sem exibir IPs públicos ou do NAT Gateway.**
   * **Análise:** Este é o resultado mais importante e o comportamento esperado. O `traceroute` não mostrou o caminho via NAT Gateway. Em vez disso, o tráfego foi interceptado pela tabela de rotas da VPC e direcionado para o endpoint do S3, que não responde a pacotes de traceroute.

## Conclusão dos Testes

A combinação dos testes confirma inequivocamente que o **S3 Gateway Endpoint está funcionando corretamente.** O tráfego do cluster para o S3 está sendo roteado internamente pela rede da AWS, bypassando o NAT Gateway.