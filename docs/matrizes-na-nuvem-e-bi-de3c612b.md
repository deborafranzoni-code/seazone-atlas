<!-- title: Matrizes na Nuvem e BI | url: https://outline.seazone.com.br/doc/matrizes-na-nuvem-e-bi-VunxEFMycv | area: Tecnologia -->

# Matrizes na Nuvem e BI

#### **Contexto**

O System Price demonstrou eficácia comprovada em teste A/B, mas enfrenta desafios de escalabilidade devido à complexidade de parametrização manual. A iniciativa "Matrizes na Nuvem e BI" visa criar uma infraestrutura de dados centralizada na GCP (BigQuery) e uma interface de análise no Looker Studio, permitindo que o time de Revenue Management gerencie a precificação automatizada através de matrizes por cluster e ajustes de agressividade, mantendo o desacoplamento do sistema legado Sirius (AWS).

#### **Objetivo**

Desenvolver uma infraestrutura de dados e interface de análise que permita:

* Armazenar matrizes de parâmetros por cluster de forma centralizada e versionada
* Gerenciar configurações de agressividade por categoria de forma simples e auditável
* Fornecer visibilidade completa do desempenho do System Price através de dashboards interativos
* Habilitar ajustes rápidos de estratégia de precificação com impacto visual imediato
* Garantir integração entre o cálculo de preços (GCP) e a aplicação final (AWS/Sirius)

## **Detalhamento e Requisitos da Infraestrutura**

### **1. Matrizes de Parâmetros por Cluster**

**Conceito:**\nMatrizes estáticas que representam o comportamento padrão de precificação para cada cluster de categorias. Cada matriz contém 96 combinações de parâmetros (12 linhas × 8 colunas) baseadas em sazonalidade, ocorrência, ocupação e antecedência.

**Estrutura da Matriz:**

EX:. Formato JSON (Armazenamento no BigQuery) 

```json
{
  "cluster_id": "CLUSTER_01",
  "version": "1.0",
  "created_at": "2025-01-15T10:30:00Z",
  "metadata": {
    "cluster_name": "Apartamentos 1Q - Goiânia",
    "categories_count": 45,
    "base_period": "2024-01 to 2024-12"
  },
  "matrix": [
    {
      "sazonalidade": "Saz-Goiania-Leste-apartamento-SUP-1Q",
      "ocorrencia": "Dia de semana",
      "sigla": "GL_DDS",
      "nivel_ocupacao": "Low",
      "faixas_antecedencia": {
        "0-5": {"percentil": 8, "tipo": "mix"},
        "6-15": {"percentil": 18, "tipo": "mix"},
        "16-30": {"percentil": 30, "tipo": "mix"},
        "31-45": {"percentil": 35, "tipo": "mix"},
        "46-60": {"percentil": 40, "tipo": "mix"},
        "61-75": {"percentil": 45, "tipo": "mix"},
        "76-90": {"percentil": 50, "tipo": "mix"},
        "91-360": {"percentil": 93, "tipo": "mix"}
      }
    },
    {
      "sazonalidade": "Saz-Goiania-Leste-apartamento-SUP-1Q",
      "ocorrencia": "Dia de semana",
      "sigla": "GL_DDS",
      "nivel_ocupacao": "Medium",
      "faixas_antecedencia": {
        "0-5": {"percentil": 10, "tipo": "mix"},
        "6-15": {"percentil": 20, "tipo": "mix"},
        "16-30": {"percentil": 35, "tipo": "mix"},
        "31-45": {"percentil": 40, "tipo": "mix"},
        "46-60": {"percentil": 45, "tipo": "mix"},
        "61-75": {"percentil": 50, "tipo": "mix"},
        "76-90": {"percentil": 55, "tipo": "mix"},
        "91-360": {"percentil": 93, "tipo": "mix"}
      }
    }
    // ... 10 combinações restantes (FDS, Feriado, Evento × 3 níveis de ocupação)
  ]
}
```

**Requisitos Técnicos:**

* **Armazenamento:** BigQuery com particionamento por cluster_id e versionamento
* **Chave Primária:** cluster_id + version
* **Atualização:** Somente pelo time de dados através de processos controlados
* **Versionamento:** Cada alteração gera nova versão com histórico mantido
* **Integridade:** Validação de schema antes de ingestão (todas as 96 combinações obrigatórias)

### **2. Tabela de Configuração de Agressividade**

**Conceito:**\nTabela dinâmica que armazena o nível de agressividade atual para cada categoria, permitindo ajustes rápidos sem modificar as matrizes base. Esta é a interface entre o sistema de precificação e as decisões do time de RM.

**Estrutura da Tabela:**

Formato BigQuery (Tabela: system_price.aggressiveness_config)

```markdown
CREATE TABLE system_price.aggressiveness_config (
  categoria_id STRING NOT NULL,
  cluster_id STRING NOT NULL,
  aggressiveness_level STRING NOT NULL OPTIONS(
    description="Nível de agressividade atual: very_moderate, moderate, standard, aggressive, very_aggressive"
  ),
  last_updated TIMESTAMP NOT NULL OPTIONS(
    description="Última atualização da configuração"
  ),
  updated_by STRING NOT NULL OPTIONS(
    description="Usuário ou sistema que realizou a última atualização"
  ),
  effective_date DATE NOT NULL OPTIONS(
    description="Data de início de vigência da configuração"
  ),
  is_active BOOLEAN NOT NULL OPTIONS(
    description="Indica se a configuração está ativa"
  ),
  safety_interval_min FLOAT64 OPTIONS(
    description="Preço mínimo de segurança (Pmin)"
  ),
  safety_interval_max FLOAT64 OPTIONS(
    description="Preço máximo de segurança (Pmax)"
  )
) PARTITION BY RANGE_BUCKET(cluster_id, 10, 100);
```

**Requisitos Técnicos:**

* **Chave Primária:** categoria_id
* **Particionamento:** Por cluster_id para otimizar consultas
* **Coluna de Enum:** aggressiveness_level com valores pré-definidos
* **Histórico:** Manter registro de alterações com effective_date
* **Integração:** API REST para atualizações em tempo real
* **Segurança:** Validação de segurança_interval_min/max contra preços mínimos do proprietário

OBS:. Verificar a dificuldade de termos granularidad imóvel. 

### **3. Experimentação de Níveis de Agressividade**

**Conceito:**\nO desenvolvedor deverá testar diferentes abordagens para calcular os níveis de aggressividade a partir da matriz padrão, avaliando qual método melhor se adapta aos diferentes padrões de mercado.

Ex **Abordagens a Testar:**

Opção 1: Delta Percentual Fixo

* **Método:** Adicionar/subtrair porcentagem fixa do percentil padrão
* **Fórmula:** percentil_novo = percentil_padrao × (1 ± delta)
* **Exemplo:**
  * Padrão: P40
  * Aggressive (-10%): P36
  * Very Aggressive (-20%): P32

Opção 2: Delta de Percentil Absoluto

* **Método:** Adicionar/subtrair pontos absolutos de percentil
* **Fórmula:** percentil_novo = percentil_padrao ± delta_pontos
* **Exemplo:**
  * Padrão: P40
  * Aggressive (-4): P36
  * Very Aggressive (-8): P32

Opção 3: Delta Adaptativo por Faixa

* **Método:** Delta variável conforme posição do percentil padrão
* **Fórmula:** delta = f(percentil_padrao)
* **Exemplo:**
  * Se P20: delta = -2 (para P18)
  * Se P80: delta = -8 (para P72)

**Critérios de Avaliação:**


1. **Consistência:** Manter relação lógica entre níveis (ex: aggressive < padrão < moderate)
2. **Impacto:** Variação percentual esperada no preço final
3. **Limites:** Respeitar intervalos de segurança (Pmin/Pmax)
4. **Simplicidade:** Facilidade de compreensão pelo time de RM
5. **Performance:** Custo computacional de cálculo


### **4. Interface de Ajustes**

**Requisitos da Interface de Ajustes**

**Conceito:**\nInterface web leve (HTML/JS) acessada diretamente do Looker Studio através de botão ou link, permitindo que o time de RM ajuste a agressividade por categoria e período de forma simples e rápida.

**Fluxo de Interação:**


1. Usuário clica em "Ajustar Agressividade" no dashboard do Looker
2. Interface abre em modal/iframe com pré-seleção:
   * Categoria e período conforme filtros ativos no dashboard
   * Nível de agressividade atual destacado
3. Usuário seleciona novo nível (5 botões radio ou dropdown)
4. Sistema valida contra intervalos de segurança
5. Confirmação visual e atualização dos gráficos

**Requisitos Técnicos:( Exemplos )**

* **Hospedagem:** Arquivos estáticos no S3 (CloudFront para CDN)
* **Backend:** Cloud Functions (GCP) com integração ao BigQuery
* **Frontend:** HTML/JS vanilla (sem frameworks para simplicidade)
* **Integração Looker:** Parâmetros na URL (categoria, período, nível_atual)

Componentes: 

\n  ─────────────────────────────────────────────────────────────────┐
│ AJUSTAR NÍVEL DE AGRESSIVIDADE │
├─────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ INFORMAÇÕES SELECIONADAS │ │
│ ├─────────────────────────────────────────────────────────────┤ │
│ │ Categoria: \[Saz-Goiania-Leste-apartamento-SUP-1Q\] │ │
│ │ Período: \[16-30 dias\] │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ OPÇÕES DE AGRESSIVIDADE │ │
│ ├─────────────────────────────────────────────────────────────┤ │
│ │ Selecione o novo nível: │ │
│ │ │
│ │ ◉ Muito Moderado ◉ Moderado ● Padrão ◉ Agressivo │ │
│ │ ◉ Muito Agressivo │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ │
│ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ AÇÕES │ │
│ ├─────────────────────────────────────────────────────────────┤
│ │ \[ CANCELAR \] \[ SALVAR ALTERAÇÃO \] │
│ └─────────────────────────────────────────────────────────────┘


## **Detalhamento do BI e Requisitos**

### **1. Filtros Gerais**

**Requisitos:**

* **Cluster:** Dropdown com lista de clusters disponíveis, opção "Todos"
* **Categoria:** Dropdown dinâmico populado conforme cluster selecionado
* **Imóvel:** Dropdown com imóveis da categoria selecionada
* **Período:** Seletor de datas com predefinições (últimos 7/15/30 dias, mês atual)
* **Funcionalidade:** Todos os filtros devem ser combináveis entre si

### **2. Camadas de Análise (Inteligência)**

**Requisitos:**

* **Preços Simulados de Agressividade:**
  * 5 níveis pré-definidos com cores distintas
  * Checkbox para mostrar/ocultar cada nível individualmente
  * Valores calculados em tempo real conforme filtros aplicados
  * Legendas claras identificando cada nível
* **Preços Concorrentes:**
  * Três categorias: Ocupados, Disponíveis, Mix
  * 5 percentis por categoria (P10, P25, P50, P75, P90)
  * Checkbox para mostrar/ocultar cada categoria
  * Representação visual diferenciada (linhas tracejadas para concorrentes)
* **Preços Históricos:**
  * Dois períodos: M-1 (mês anterior) e Ano-1 (ano anterior)
  * Checkbox para mostrar/ocultar cada período
  * Indicação visual de dados históricos (cores mais claras)

### **3. Gráfico Principal: Evolução de Preços**

**Requisitos:**

* **Tipo:** Gráfico de linhas múltiplas
* **Eixo X:** Sequência temporal (dias)
* **Eixo Y:** Valores monetários (R$)
* **Séries:** Linhas para cada nível de agressividade ativo
* **Interatividade:**
  * Hover sobre pontos mostra detalhes completos
  * Tooltip deve conter: Data, Preço, Percentil Aplicado, Regra Aplicada, Nível de Agressividade
  * Zoom horizontal para períodos específicos
  * Destaque para intervalos de segurança (Pmin/Pmax como áreas sombreadas)

### **4. Gráfico Secundário: Ocupação Comparativa**

**Requisitos:**

* **Tipo:** Gráfico de barras agrupadas
* **Eixo X:** Mesma sequência temporal do gráfico principal
* **Eixo Y:** Percentual (0-100%)
* **Séries:** Duas barras por dia (Categoria vs Concorrentes)
* **Visualização:**
  * Cores distintas e consistentes (ex: azul para categoria, laranja para concorrentes)
  * Percentil
  * Agressividade
  * Valores exatos no hover das barras

### **5. Tabela Detalhada**

**Requisitos:**

* **Colunas Obrigatórias:**
  * Data (formato DD/MM/AAAA)
  * Preço System Price (formato monetário R$)
  * Percentil Concorrente (ex: P45)
  * Taxa de Ocupação (formato percentual)
  * Regra Aplicada (ex: DDS_Low_0-5d)
  * Nível de Agressividade (ex: Standard)
* **Funcionalidades:**
  * Ordenação por qualquer coluna (cabeçalho clicável)
  * Paginação para grandes volumes (padrão 50 linhas)
  * Busca textual em qualquer coluna
  * Exportação para CSV com formatação correta
  * Destaque visual para finais de semana e feriados

### **6. Integração com Sistema de Ajustes**

**Requisitos:**

* **Botão de Ação:** Elemento visual claro que abre interface de ajustes
* **Parâmetros na URL:** Deve passar categoria, período e nível atual
* **Feedback Visual:** Indicação quando ajuste é aplicado com sucesso
* **Atualização Automática:** Ver possíbilidade de Gráficos atualizar após ajuste
* **Consistência:** Mesmos dados e filtros devem ser mantidos após retorno


\

\

\