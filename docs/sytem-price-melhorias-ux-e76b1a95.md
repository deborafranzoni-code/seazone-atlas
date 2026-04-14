<!-- title: Sytem Price: Melhorias UX | url: https://outline.seazone.com.br/doc/sytem-price-melhorias-ux-PKRNM4uzga | area: Tecnologia -->

# Sytem Price: Melhorias UX

# **Proposta Simplificada**

**Contexto do Problema**\nO System Price atual é um sistema de precificação dinâmica e sua eficácia esta sendo comprovado por meio de teste A/B, mas enfrenta um desafio crítico de escalabilidade. A parametrização manual exige configuração de 96 parâmetros por categoria em uma matriz complexa, tornando inviável a expansão para as 600 categorias e 2 mil imóveis da carteira. O tempo gasto para configurar equivale à precificação manual, frustrando o objetivo de escalabilidade. O time de RM abandonou o sistema anterior por complexidade operacional.

**Solução Proposta**\nDesenvolver uma camada de usabilidade sobre o motor existente do System Price, mantendo intacta sua lógica de cálculo. A solução combina três elementos:


1. **Matrizes Pré-Configuradas na Nuvem**
   * Armazenar matrizes de parâmetros no S3, organizadas por clusters de similaridade.
   * Cada cluster terá 5 níveis de agressividade pré-definidos (Muito Agressivo e, Aggressive, Padrão, Moderado, Muito Moderado).
   * As matrizes são estáticas e mantidas pelo time de dados, com atualizações periódicas baseadas em desempenho.
2. **Interface de Visualização no Looker Studio**
   * Dashboard existente enriquecido com tooltips explicativos sobre regras aplicadas.
   * Simulador de cenários para visualizar impacto de mudanças de agressividade (apenas visual, sem alteração).
   * Botão de ação que direciona para ferramenta de ajustes externa.
3. **Micro-Serviço de Ajustes**
   * Ferramenta web simples (HTML/JS + Lambda) para ajustes de agressividade.
   * Usuário seleciona categoria, período e nível de agressividade em 3 cliques.
   * Alterações salvas no DynamoDB, que é consultado pelo System Price antes de cada execução.

**Benefícios Esperados**

* **Escalabilidade Imediata**: Redução de 96 para 1 parâmetro por ajuste, permitindo cobrir 600 categorias.
* **Redução de Complexidade**: Usuário não interage mais com matrizes, apenas escolhe níveis de agressividade.
* **Manutenção Simplificada**: Matrizes atualizadas centralmente pelo time de dados, sem intervenção do RM.
* **Zero Risco ao Motor**: Lógica de cálculo do System Price permanece inalterada, mantendo eficácia comprovada.
* **Custo-Benefício**: Arquitetura serverless (S3 + Lambda + DynamoDB) com custo operacional mínimo.


**Próximos Passos**


1. **Validação Técnica**:
   * Clusterizar 50 categorias não sazonais usando dados históricos.
   * Gerar matrizes piloto para 1 cluster.
2. **Desenvolvimento MVP** :
   * Adaptar dashboard do Looker com tooltips e simulador.
   * Implementar micro-serviço de ajustes (API Gateway + Lambda).
3. **Teste Controlado** :
   * Aplicar solução em 4 categorias do teste A/B original.
   * Comparar tempo de parametrização vs. método manual.
4. **Rollout Gradual** :
   * Expansão para mais categorias não sazonais.
   * Treinamento do time de RM com novo fluxo.

Links: \nApresentação: <https://chat.z.ai/space/e0xh870ess81-art>

App UI: <https://chat.z.ai/space/k0gju727ur40-ppt>