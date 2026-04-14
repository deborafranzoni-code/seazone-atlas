<!-- title: Proposta de Execução: System Price Sazonal (Lab Floripa - Fase 1) | url: https://outline.seazone.com.br/doc/proposta-de-execucao-system-price-sazonal-lab-floripa-fase-1-39HSUDtAFk | area: Tecnologia -->

# Proposta de Execução: System Price Sazonal (Lab Floripa - Fase 1)

**Objetivo** Expandir Sytem Price para mercados de **Sazonalidade**, iniciando com um MVP em Florianópolis. O foco é validar se o algoritmo consegue manter os imóveis dentro ou acima da **Meta de Faturamento**, liberando o time de Revenue Management (RM) da precificação manual de alta temporada.

**Escopo do Piloto (Cluster Inicial)** Para validar a hipótese com baixo risco e alta velocidade de aprendizado, focaremos no recorte urbano de Florianópolis:

* **Região:** Centrão de Florianópolis + Região da UFSC.
* **Stratas:** Apenas categorias **JR** (Junior) e **SUP** (Superior).
  * *Exclusões:* Categorias TOP e MASTER ficam fora desta fase (complexidade distinta).
* **Tamanho:** Imóveis de **até 3 quartos**.

**Ajustes na Estratégia de Precificação** Para atender à volatilidade sazonal, a matriz de parâmetros sofrerá as seguintes alterações em relação aos não-sazonais:


1. **Granularidade de Eventos:** Criação de níveis de importância (1, 2 e 3) para Feriados e Eventos (ex: Réveillon = Nível 3, Show Local = Nível 1).
2. **Regras de Final de Semana:** O "degrau" de preço para fins de semana não será uma regra fixa de sistema. Será parametrizado individualmente na matriz para máxima flexibilidade (ex: pode variar entre sazonalidades).
3. **Limites de Segurança:** Utilizaremos o histórico de precificação manual do mesmo período sazonal (ano anterior) como referência. Sem correção inflacionária automática nesta fase.

**Plano de Validação e Rollout** O processo ocorrerá em duas etapas para mitigar riscos:


1. **Fase 1 - Modo Simulado:**
   * O motor calcula os preços e grava os dados em tabela dedicada.
   * **Visualização apenas no BI.** Nada é enviado para as OTAs (canais de venda).
   * Validação visual e qualitativa pelo time de RM.
2. **Fase 2 - Em produção Controlado:**
   * Após aprovação da Fase 1, um subconjunto de imóveis será selecionado para precificação real.
   * Aceitação de risco calculado: Há entendimento de que imóveis piloto podem ter prejuízo pontual em troca da validação da estratégia no mercado real.

**Critério de Sucesso** O piloto será considerado bem-sucedido se o **System Price** atingir performance de faturamento equivalente ou superior à meta estabelecida, sem necessidade de intervenção manual massiva.