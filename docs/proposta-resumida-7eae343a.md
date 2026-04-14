<!-- title: Proposta resumida | url: https://outline.seazone.com.br/doc/proposta-resumida-DngTmSVpEr | area: Tecnologia -->

# Proposta resumida

### **Problema & Contexto**

Os atuais sistemas de alertas de pico de demanda (internos e concorrentes) geram valor, mas operam de forma **isolada**, forçando o time a cruzar manualmente informações no BI. O resultado é **excesso de ruído** e **processo manual pesado** (\~1 hora/dia), com perda de oportunidades devido à falta de contexto integrado.

**Impacto:** Eventos detectados pelos concorrentes chegam antes, mas não são conectados aos dados internos, gerando atraso na ação estratégica.

### **Solução Proposta**

Evoluir os sistemas para **"conversarem entre si"** através de integração seletiva de dados, mantendo duas abas separadas mas com **contexto cruzado**:

#### **1. Motor de Filtros Inteligentes**

* **Filtro de Eventos Mapeados:** Eliminar alertas externos para datas com eventos já catalogados pelo RM
* **Filtro de Relevância:** Não alertar regiões sem imóveis Seazone ativos
* **Agrupamento Inteligente:** Combinar alertas de datas adjacentes (±3 dias) em único período

#### **2. Integração Seletiva** 

**Para Alertas Externos (Concorrentes):**

* Indicar se há **ocupação interna** para o mesmo período
* Mostrar **ocupação %** do polígono Seazone
* Sinalizar se há **alerta interno ativo** para aquela data
* Exemplo: "Concorrentes 45% ocupados | Seazone 0% | Sem alerta interno"

**Para Alertas Internos:**

* Trazer **ocupação dos concorrentes** para comparação
* Indicar se há **evento mapeado** pelo RM
* Sinalizar se o **sistema externo alertou** para aquela data
* Exemplo: "3 reservas sobrepostas | Concorrentes 38% | Evento: CCXP"

#### **3. Experiência Otimizada**

* **Duas Abas Especializadas:** "Alertas Internos" e "Alertas Concorrentes"
* **Colunas Cruzadas:** Incluir dados do outro sistema em cada aba
* **Status Unificado:** "Ajustar Preço", "Monitorar", "Ignorar", "Falso Positivo"
* **Histórico Inteligente:** Arquivamento automático com referência cruzada

#### **4. Parametrização Dinâmica**

* **Por Tamanho:** Ajustar limiares baseado no número de imóveis no polígono
* **Por Antecedência:** Regras diferentes para curto (35-60d), médio (61-90d) e longo prazo (91+d)
* **Por Sazonalidade:** Limiares mais altos para finais de semana e períodos naturalmente aquecidos