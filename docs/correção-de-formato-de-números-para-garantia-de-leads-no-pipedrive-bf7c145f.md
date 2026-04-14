<!-- title: Correção de Formato de Números para Garantia de Leads no Pipedrive | url: https://outline.seazone.com.br/doc/correcao-de-formato-de-numeros-para-garantia-de-leads-no-pipedrive-PQets4JCuh | area: Tecnologia -->

# Correção de Formato de Números para Garantia de Leads no Pipedrive

**Autor:** Geozedeque Guimarães  **Stakeholders:** Leandro Shimanuki - Marketing **Data:** 14-01-2026


---

# **1. Resumo**

Otimizar a integração entre Meta Ads e Pipedrive para garantir que 100% dos leads (MQLs) sejam registrados, tratando números internacionais ou mal formatados que hoje são ignorados pela MIA.

# **2. O Problema:**

* **Contexto:** Nos formulários de Lead Ads, casos em que os números de contato preenchido pelos leads estejam fora do padrão ou seja um numero internacionais a MIA não reconhece. Com isso, não ela nem cria o deal no pipedrive. 
* **Dores do Time:** As perda de leads no fluxo automático gera um trabalho manual de criação de deals por parte da equipe de marketing e com isso atraso no primeiro contato comercial.
* **Impacto no Negócio:** Risco de perda de leads qualificados e atraso no tempo de resposta comercial.
* **Insumos/Massa de Dados:** [Link da Planilha de Leads com Erro](https://docs.google.com/spreadsheets/d/1YjXEeKlJ4sq5Snc9STL2V2kg_yu7iuVDuZuvOyKdqRY/edit?gid=0#gid=0)

# 3.Objetivos e Requisitos de Sucesso

**Objetivo Geral:** Eliminar a perda de leads (MQLs) provenientes do Meta Ads, garantindo que 100% das conversões resultem na criação automática de um Deal no Pipedrive, independente da compatibilidade com a IA MIA.

**Requisitos de Sucesso:**

* **Normalização de Dados:** Implementar script que limpe e formate obrigatoriamente todos os números de telefone (removendo espaços, caracteres especiais e zeros à esquerda), padronizando o input para o Pipedrive e para a MIA.
* **Triagem por DDI (Nacional vs Internacional):** Criar lógica de identificação de prefixo para garantir que números brasileiros (+55) sigam o fluxo da MIA, enquanto números internacionais (Outros DDIs) sejam desviados para criação direta via API no Pipedrive.
* **Integridade do Funil:** Garantir que o volume de leads registrados no Meta Ads seja idêntico ao volume de novos Deals criados no Pipedrive, eliminando 100% do retrabalho de inserção manual pelo time de Marketing.

# **4. Escopo**

* **Dentro do Escopo:** 
* 1. Normalizar números nacionais para o padrão aceito pela MIA (+55...). 
* 2. Identificar números internacionais. 
* 3. Criar Deal diretamente no Pipedrive via API para números internacionais ou rejeitados pela MIA.

  \