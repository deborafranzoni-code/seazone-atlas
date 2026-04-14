<!-- title: Automação de Lost por Falta de Retorno (Mia) | url: https://outline.seazone.com.br/doc/automacao-de-lost-por-falta-de-retorno-mia-tynlDxCQWw | area: Tecnologia -->

# Automação de Lost por Falta de Retorno (Mia)

Autor: Geozedeque Guimarães | Stakeholders: BU Comercial (Renata Domingues) | Data: 20/01/2026

# 1. Resumo 

Automatizar o descarte (status "Lost") de deals no Pipedrive que não interagem após a cadência completa de 3 tentativas de contato realizadas pela IA Mia. 

# 2. **O Problema**

### **Contexto**: 

Leads vindos do Facebook Ads entram no fluxo da Mia, que realiza até 3 tentativas de contato. Atualmente, o time precisa mover manualmente para "Lost" ou o card fica parado na coluna. 

### Dores do Time: 

Sobrecarga visual no funil com cards inativos e esforço manual para conferir se houve resposta antes de dar lost. 

### Impacto no Negócio: 

Processo não escalável e poluição de dados no CRM.

# 3. Objetivos e Informações Técnicas

Sistemas: Pipedrive (Funil: Prospecção Parceiro / Canal: Marketing POC). 

Objetivo Principal: Garantir que 100% dos leads sem resposta na 3ª tentativa sejam arquivados automaticamente. 

# 4. Escopo

### Dentro: 

Identificar 3ª tentativa, verificar campo "Mia Lid respondeu", mover para Lost, adicionar tag e log. 

# 5. Proposta de Solução

### Gatilho: 

Conclusão da 3ª tentativa de contato pela Mia. 

### Fluxo Lógico:

 Se (Tentativa = 3) E (Respondeu = Não) → Mover para Lost + Tag + Histórico. 

# 6. Detalhamento de Regras

### Regra de Bloqueio: 

Se na 3ª tentativa o campo "Mia Lid respondeu" for igual a "Sim", a automação não deve agir.