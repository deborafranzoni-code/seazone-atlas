<!-- title: Evolução da Quarentena de Concorrentes (Fase 2) | url: https://outline.seazone.com.br/doc/evolucao-da-quarentena-de-concorrentes-fase-2-jAAD3dZ2X4 | area: Tecnologia -->

# Evolução da Quarentena de Concorrentes (Fase 2)

**Versão:** 1.0 

**Data:** 16 de Fevereiro de 2026 

**Autor:** Lucas Abel (PM de Dados) 

**Stakeholders:** Fábio de Biasi (RM), Belle Guerreiro (RM)

## 1. Resumo Executivo

Após 2 meses de operação da "Quarentena de Concorrentes", identificou-se a necessidade de evoluir a ferramenta para reduzir o esforço operacional (falso positivos em categorias saudáveis) e aumentar a precisão na detecção de anomalias (falso negativos em oscilações de preço e reviews). Este projeto visa automatizar decisões de baixo risco e refinar as regras heurísticas existentes.

## 2. O Problema


1. **Esforço Operacional Desnecessário:** O time de RM gasta tempo analisando e inativando manualmente imóveis em categorias "Verdes" (saudáveis), onde a remoção do outlier não impacta a saúde da meta. Essa é uma decisão repetitiva e de baixo risco.
2. **Falso Negativos (Regras Permissivas):** A regra atual de diária (3x a mediana do imóvel) deixa passar erros graves (ex: oscilações de 2.3x) e não considera o contexto da categoria, permitindo que dados ruins impactem a meta. Além disso, a regra de "ocupação sem review" falha em detectar imóveis com atividade espúria esporádica (1 review em 1 ano).
3. **Concorrentes Inativos:** Imóveis com calendário futuro totalmente bloqueado permanecem na base, distorcendo métricas de disponibilidade e competição.

## 3. Objetivos

* **Automatizar Decisões Seguras:** Reduzir em \~70% o volume de análises manuais para categorias "Verdes".
* **Aumentar Precisão:** Refinar regras para capturar erros de oscilação de preço e reviews sem gerar bloqueios indevidos em diárias baixas.
* **Limpeza de Base:** Remover imóveis sem disponibilidade futura do cálculo da meta.

## 4. Escopo da Solução

### 4.1. Melhorias de Processo (Governança)

**ID: GOV-01 | Automação de "Categorias Verdes"**

* **Descrição:** Se um imóvel for identificado como Outlier (IQR) e sua categoria tiver o status "Verde" (saudável), o sistema deve inativá-lo automaticamente da meta, sem necessidade de aprovação manual.
* **Lógica:**
  * Verificar coluna `farol_categoria` na tabela de metadados.
  * Se `farol_categoria == 'Verde'` E `status_atual == 'EM_QUARENTENA' (motivo IQR)`:
    * Atualizar `status_final` para `INATIVADO`.
    * Aplicar `participante_meta: NAO` na tabela principal.
* **Impacto:** Redução de trabalho manual.

### 4.2. Refinamento e Criação de Regras (Técnico)

**ID: REG-01 | Ajuste Fino de Reviews (Regra A)**

* **Problema:** Imóveis com ocupação alta, mas com apenas 1 review em anos, são tratados como legítimos.
* **Nova Lógica:** Alterar o critério de validação de qualidade.
  * De: `total_reviews = 0` .
  * Para: `quantidade_reviews_ultimos_180d <= 2`.
* **Ação:** Se não atender ao critério de reviews, manter bloqueio/inserir em quarentena.

**ID: REG-02 | Ajuste Fino de Diária (Regra B - Daily Fat Acima)**

* **Problema:** O multiplicador `3x` é alto demais e ignora o contexto da categoria. Diárias baixas (R$ 100) oscilando para R$ 300 são legítimas, mas o modelo antigo poderia flagrar erroneamente ou ignorar o caso `39104270` (oscilação de \~2.3x).
* **Nova Lógica (Híbrida Segura):** O dia será bloqueado se atender **AMBAS** condições:

  
  1. `Diária_Ocupada > 2 * Mediana_Movel_Diaria_Imovel` (Reduzido de 3x para 2x).
  2. `Diária_Ocupada > 1.5 * Mediana_Diaria_Categoria no dia` (Trava de segurança para não pegar diárias baixas legítimas).
* **Ação:**
  * Bloquear o dia específico (`day_fat = 0`).
  * Mover imóvel para Quarentena (Tag: `day_fat_acima`).

**ID: REG-03 | Nova Regra: Calendário Futuro Bloqueado**

* **Problema:** Concorrentes que saíram do mercado ou bloquearam todo o calendário continuam na base.
* **Nova Lógica:**
  * Se `Taxa_Indisponibilidade_Futuro_90d >= 0.90` (90% bloqueado/ocupado).
* **Ação:** Inserir na Quarentena com Tag `futuro_bloqueado` e INATIVAR).

## 5. Analise extra validar

* **Regra de Oscilação "Serra" (Variação dia-a-dia):** Detectar variações bruscas entre dias adjacentes (ex: 400 -> 900). Complexidade alta para validação de eventos..
* **Detecção de Erro de Categoria:** A distinção entre "dado errado" e "categoria errada" permanece sendo uma decisão humana apoiada pela interface.

## 6. Plano de Implementação


1. **Etapa 1 (Backend):** Atualização das Queries SQL para implementar REG-01, REG-02 e REG-03.
2. **Etapa 2 (Backend):** Implementação da lógica de automação GOV-01 (Job de processamento).

   \
3. **Etapa 3 (Testes):** Validação com o time de RM usando dados históricos de Janeiro/2026.