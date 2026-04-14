<!-- title: Proposta de Melhoria para o trimestre - Franquias e Proprietário | url: https://outline.seazone.com.br/doc/proposta-de-melhoria-para-o-trimestre-franquias-e-proprietario-yEetY1kF8a | area: Tecnologia -->

# Proposta de Melhoria para o trimestre - Franquias e Proprietário

## Objetivo 

Listar os pontos de melhoria nos processos relacionados a **proprietários** e **franquias**, com foco em impactar diretamente as metas globais de **faturamento por headcount** e **faturamento da holding**.


---

##  Proprietários

### 1. Área de Performance do Imóvel

* **Problema identificado**: Proprietários têm baixa visibilidade da performance do imóvel e dificuldade em entender seus resultados financeiros, causando aumento de tickets de suporte com dúvidas a respeito de precificação.
* **Objetivo**: Criar uma área onde o proprietário acompanhe a performance do imóvel e compare com dados de imóveis concorrentes.
* **Hipótese**: A maior transparência e visibilidade de dados reduzirá dúvidas e aumentará a confiança do proprietário.
* **Entregáveis**:
  * Gráfico de faturamento mensal (comparativo mês a mês)
  * Gráfico de faturamento vs despesas mensais
  * Gráfico de lucro acumulado ao longo dos meses
* **KPI de sucesso**:
  * Redução percentual nos tickets abertos relacionados a dúvidas sobre precificação


---

### 2. PWA na Wallet

* **Problema identificado**: Baixo engajamento e percepção limitada de valor por parte do proprietário.
* **Objetivo**: Testar o engajamento e aumentar a confiança através de notificações via PWA.
* **Hipótese**: Notificações relevantes aumentam o uso da plataforma e percepção de valor.
* **Entregável inicial**:
  * Notificação de que o comprovante de repasse está disponível na Wallet
* **KPI de Sucesso:** 


---

### 3. Comprovante de Repasse na Wallet

* **Problema identificado**: Falta de transparência sobre os repasses realizados.
* **Objetivo**: Disponibilizar os comprovantes diretamente na Wallet, aumentando a clareza para o proprietário.
* **Status**: ==Em andamento==


---


4. **Gestão de Contas - Teste** 

* **Problema identificado:** Demanda ao time de CS para coletar informações para gestão de contas 
* **Objetivo:** Aumentar faturamento possibilitando adesão simplificada e diminuir trabalho junto ao time de CS
* **Entregáveis** 
  * Banner para engajamento do proprietário para adesão de gestão de contas 
  * Assinatura de aditivo de contrato pela wallet 
  * Incluir dados de gestão de contas no banco de dados  
  * Coletar informações dos PDFs de despesas 
  * ==Automatizar coleta de faturas  - buscar a partir da data de vencimento==
    * Celesc - 89 propriedades - 41,6% das faturas 
* **KPI de Sucesso:** 
  * Aumentar o número de imóveis com gestão de conta
  * Automatização em 100% dos processos 


---

##  Franquias

### 1. Refatoração da Tela de Lançamento de Reembolso - Franqueado

* **Problema identificado**: Lançamentos incompletos geram retrabalho do time operacional.
* **Objetivo**: Reduzir o retrabalho por meio da exigência de informações essenciais no momento do lançamento.
* **Entregáveis**:
  * Tornar obrigatório o envio de aprovação do proprietário para reembolsos > R$ 300
  * Campo para vincular o reembolso a um dano (depende da refatoração do sistema de danos)
  * Notificações pop-up para anfitrião em caso de pendências
  * Sub itens de motivo de reembolso 
* **KPI de Sucesso:**


---

### 2. Refatoração da Tela de Despesas

* **Problema identificado**: Processo atual exige muitas etapas.
* **Objetivo**: Simplificar a pré-aprovação e melhorar a visibilidade das informações.
* **Entregáveis**:
  * Simplificar etapas para pré-aprovação de uma despesa
  * Inclusão do código e status do dano na tela (dependente da refatoração do sistema de danos)
  * Campo para registro dos motivos de reprovação ou cancelamento
  * Incluir filtro por motivo de despesa
  * IA de possível fraude em despesa
  * imóvel possui easy cover 


---

### 3. Refatoração da Tela de Lançamento de Dano - Franqueado

* **Problema identificado**: Faltam informações obrigatórias no lançamento, gerando retrabalho.
* **Objetivo**: Garantir completude e rastreabilidade nos lançamentos.
* **Entregáveis**:
  * Obrigatoriedade de NF ou link de cotação
  * Geração automática de código de dano
  * Campo para vincular despesa a um dano via código
  * Exibição do código gerado na visualização do dano
* **KPI de Sucesso:**


---

### 4. Integração Pipefy x Sapron

* **Problema identificado**: Atualizações manuais consomem tempo da equipe e são sujeitas a erro.
* **Objetivo**: Automatizar a sincronização entre Pipefy e Sapron para ganho de eficiência operacional.
* **Entregáveis**:
  * Atualizar automaticamente o status no Sapron ao mover o card para "Reembolso Pago"
  * Atualizar automaticamente o status no Sapron ao mover o card para "Reembolso Cancelado"
* **KPI de Sucesso:**