<!-- title: Incidentes e Análises Pós-Incidente | url: https://outline.seazone.com.br/doc/incidentes-e-analises-pos-incidente-oKSaykEsY7 | area: Tecnologia -->

# Incidentes e Análises Pós-Incidente

## Descrição:

Documentação de eventos que causaram falhas, degradação ou indisponibilidade parcial/total de serviços. Cada registro inclui o que aconteceu, por que aconteceu e o que foi feito para resolver. Incidentes com impacto mais relevante devem conter uma análise pós-incidente mais completa (RCA/postmortem), incluindo lições aprendidas e medidas preventivas.


***

### Template

```none
📌 [Serviço] - [Resumo do Incidente] - [Data]

🕒 Data

Ex: 24/04/2025

🌍 Ambiente

Produção / Staging / Dev

☁️ Cluster / Conta AWS

Ex: tools / seazone-prod

🚨 Descrição do Incidente

Descreva o que aconteceu, como foi percebido (alertas, logs), impacto no serviço e usuários afetados.

🧠 Causa Raiz

Explique o motivo principal do incidente, técnico ou processual.

🔧 Ações Corretivas Aplicadas

Liste os comandos, alterações ou ações executadas.

✅ Resultados

Quais melhorias ou correções foram confirmadas após a intervenção.

🔎 Verificações

Comandos ou validações usadas para confirmar a resolução.

📝 Recomendações Futuras

Ideias de melhoria, automação ou prevenção de recorrência.

🏷️ Tags

#aws #eviction #karpenter #metabase #infra

👥 Responsáveis

Nome 1  
Nome 2
```

\n