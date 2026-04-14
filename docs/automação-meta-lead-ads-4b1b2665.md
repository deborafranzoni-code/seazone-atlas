<!-- title: Automação Meta Lead Ads | url: https://outline.seazone.com.br/doc/automacao-meta-lead-ads-rGyxNwxq2u | area: Tecnologia -->

# Automação Meta Lead Ads

**Autor:** Geozedeque Guimarães **Stakeholders:** Marketing (Renan Amorim) **Data:** 29/01/2026

### 1. Resumo

Ajustar a automação de recebimento de leads para tratar eventos de teste originados pela ferramenta de debug do Meta. Atualmente, esses testes enviam campos incompletos, causando a quebra do fluxo e impedindo a validação de novas campanhas.

### 2. O Problema

* **Contexto:** O time de Marketing utiliza a ferramenta de testes do Meta para validar se os formulários de anúncios estão enviando dados corretamente.
* **Dores do Time:** Quando um lead de teste é enviado, ele não possui metadados de campanha (`campanha_id`, `ad_name`, etc.). A automação atual espera esses dados de forma obrigatória; ao não encontrá-los, o erro interrompe a execução (quebra o fluxo).
* **Impacto no Negócio:** Impossibilidade de realizar testes em novas campanhas de forma ágil, gerando insegurança no lançamento de anúncios e dependência de suporte técnico para tratar os erros.

### 3. Objetivos e Informações Técnicas

* **Sistemas Envolvidos:** Meta (Facebook/Instagram), Ferramenta de Automação (n8n), Baserow (banco de dados de mocks).
* **Volume/Frequência:** Baixo volume (apenas em momentos de criação/teste de campanhas), mas crítico para o processo de setup.
* **Objetivo Principal:** Garantir que 100% dos leads de teste do Meta passem pela automação sem gerar erros, sendo identificados e tratados com dados fictícios (mocks).

### 4. Escopo

* **Dentro do Escopo:**
  * Criação de um nó de validação/filtro para identificar leads de teste ou incompletos.
  * Integração com Baserow para buscar dados de um "Empreendimento de Teste".
  * Substituição de campos vazios por dados mockados.

### 5. Proposta de Solução (Visão Geral)

* **Gatilho (Trigger):** Webhook recebendo dados do Meta Lead Ads.
* **Fluxo Lógico (To-Be):**

  
  1. Recebe o dado.
  2. **Validação:** Os campos `campanha_id` ou `ad_id` estão presentes?
  3. **Se SIM (Caminho Feliz):** Segue o fluxo normal.
  4. **Se NÃO (Exceção):** Busca no Baserow os dados de "Lead Teste", preenche as variáveis e segue para o destino final sem quebrar.