<!-- title: IaC/Terraform | url: https://outline.seazone.com.br/doc/iacterraform-Eep0ylPzvt | area: Tecnologia -->

# IaC/Terraform

# 🏗️ Terraform + Terragrunt - Governança Tech

## 📋 Visão Geral

Estrutura completa de **Infrastructure as Code** com **Terraform + Terragrunt**, organizada por contas, ambientes e produtos, com módulos reutilizáveis e governança centralizada.

## 🏗️ Arquitetura da Infraestrutura

### **Organização Hierárquica**

 ![](/api/attachments.redirect?id=a7f66ef2-d581-464f-a597-8205b401967e)

### **Separação de Responsabilidades**

Nesta arquitetura, a responsabilidade pela infraestrutura é centralizada para garantir consistência e segurança.

* **🏛️ Time de Governança/Infra**: É o único time responsável por gerenciar todo o ciclo de vida da infraestrutura como código. Eles codificam, revisam e aplicam as mudanças em todos os níveis: `global`, `environments/common` e de `produto`.
* **👥 Time de Desenvolvimento**: Atua como o cliente da infraestrutura. Eles **solicitam** os recursos necessários para suas aplicações (como um novo bucket S3 ou um repositório ECR), e o time de Governança/Infra implementa a configuração no Terraform.

O diagrama abaixo ilustra este fluxo:

 ![](/api/attachments.redirect?id=d6b49ff2-5148-4bb7-85f1-14b19d3d02f9)

## 🗂️ Estrutura Completa do Repositório

### **Organização Detalhada**

```
terraform-governanca/
├── production-711387131913-aws/      # <-- Raiz para a conta AWS
│   ├── global/                         # <-- Infraestrutura Global (VPC, EKS, etc.)
│   │   ├── eks/
│   │   ├── iam/
│   │   ├── s3/
│   │   ├── ssm/
│   │   └── vpc/
│   ├── environments/                   # <-- Configurações por Ambiente
│   │   ├── dev/
│   │   │   ├── common/                 # <-- Recursos comuns ao ambiente DEV
│   │   │   │   ├── rds/
│   │   │   │   └── elasticache/
│   │   │   ├── reservas/
│   │   │   ├── sapron/
│   │   │   └── wallet/
│   │   ├── prd/                        # <-- Ambientes de Produção e Staging (similares a dev)
│   │   └── stg/
│   ├── modules/                        # <-- Módulos Terraform reutilizáveis
│   ├── policies/                       # <-- Policy as Code (OPA, Checkov)
│   ├── scripts/                        # <-- Scripts de automação e utilitários
│   └── terragrunt-config/              # <-- Configuração raiz do Terragrunt (_include)
└── seazone-tools-gcp5435-gcp/        # <-- Exemplo para outra conta/projeto
```

## 🔧 Configuração Terragrunt

### **Root Configuration (**`terragrunt-config/terragrunt.hcl`)

O arquivo raiz do Terragrunt agora vive em `terragrunt-config/terragrunt.hcl`. Ele é incluído em todos os outros arquivos `terragrunt.hcl` e define as configurações globais, como o backend remoto e os provedores.

### **Global Infrastructure (**`global/eks/terragrunt.hcl`)

```hcl
# terragrunt-governanca/production-711387131913-aws/global/eks/terragrunt.hcl

include "root" {
  path = find_in_parent_folders("terragrunt.hcl", "../terragrunt-config/terragrunt.hcl")
}

terraform {
  source = "../../../modules/aws/eks"
}

dependency "vpc" {
  config_path = "../vpc"
}

inputs = {
  cluster_name = "seazone-production"
  cluster_version = "1.28"
  vpc_id = dependency.vpc.outputs.vpc_id
  # ... outros inputs
}
```

### **Environment-Specific Configuration (**`environments/dev/common/rds/terragrunt.hcl`)

```hcl
# terragrunt-governanca/production-711387131913-aws/environments/dev/common/rds/terragrunt.hcl

include "root" {
  path = find_in_parent_folders("terragrunt.hcl", "../../../../terragrunt-config/terragrunt.hcl")
}

terraform {
  source = "../../../../../modules/aws/rds"
}

# Depende da infraestrutura global

dependency "eks" {
  config_path = "../../../../global/eks"
}

inputs = {
  instance_class = "db.t3.micro" # Instância menor para dev
  # ... outros inputs
}
```

## 🔄 Gerenciamento e Fluxo de Deploy

### **Fase 1: Deploy da Infraestrutura Global (Execução Rara)**

Esta fase provisiona a infraestrutura base da conta, como a VPC e o cluster EKS. É executada apenas quando há mudanças nesses recursos centrais.

```javascript
# 1. Navegue até o diretório da infraestrutura global
cd terraform-governanca/production-711387131913-aws/global

# 2. Gere e revise o plano de execução. Este passo é obrigatório.
terragrunt run-all plan

# 3. Após a revisão e aprovação do plano, aplique as mudanças.
terragrunt run-all apply
```

### **Fase 2: Deploy de Ambientes (Execução Frequente)**

Esta é a operação mais comum, usada para gerenciar recursos dentro de um ambiente específico (dev, stg, prd). Terragrunt permite aplicar as mudanças de forma granular.

#### **A. Aplicando em um Ambiente Completo**

Use este comando para aplicar todas as mudanças pendentes em um ambiente, incluindo todos os produtos.

```javascript
# Exemplo para o ambiente de 'dev'
cd terraform-governanca/production-711387131913-aws/environments/dev
terragrunt run-all plan
# Após revisar o plano...
terragrunt run-all apply
```

#### **B. Aplicando em um Único Produto dentro de um Ambiente**

Para limitar o impacto, o ideal é aplicar as mudanças no escopo de um único produto.

```javascript
# Exemplo para aplicar apenas as mudanças do produto 'wallet' em 'dev'
cd terraform-governanca/production-711387131913-aws/environments/dev/wallet
terragrunt run-all plan
# Após revisar o plano...
terragrunt run-all apply
```

### **Fluxo de Trabalho com Pull Request (PR)**

Nenhuma mudança deve ser aplicada diretamente sem revisão. O processo padrão é:


1. **Branch**: O time de Governança/Infra cria uma nova *feature branch* para a mudança.
2. **Código**: A infraestrutura é codificada nos arquivos `.tf` apropriados.
3. **Pull Request**: Um PR é aberto no GitHub.
4. **CI/CD (Automação)**: Um pipeline de CI (ex: GitHub Actions) é acionado automaticamente para validar o código (`terragrunt hclfmt`,`validate`) e gerar os planos (`terragrunt run-all plan`).
5. **Revisão**: O output do `plan` é publicado como um comentário no PR. A equipe revisa as mudanças propostas para garantir que estão corretas e seguras.
6. **Merge e Deploy**: Após a aprovação e o merge do PR, um membro do time de Governança/Infra executa o `terragrunt run-all apply` manualmente a partir do diretório correto, conforme os exemplos acima.