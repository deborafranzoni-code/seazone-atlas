<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-8RvtJrma19 | area: Tecnologia -->

# Documentação do Usuário

## 📖 Guia do Usuário: Dashboard de Alertas - Detector de Eventos

### 🎯 1. Visão Geral e Objetivo

Bem-vindo(a) à Planilha de Gestão de Picos de Demanda!

Esta ferramenta foi criada para ser o seu centro de controle na identificação e ação sobre períodos de alta demanda inesperada. O objetivo é simples: usar dados para tomar decisões de precificação mais inteligentes, garantindo que não estamos perdendo oportunidades de receita.

A planilha consolida dois tipos de alertas:

* **Alertas Internos**: Baseados em um aumento súbito de reservas dentro da própria Seazone.
* **Alertas Externos**: Baseados em um aumento anormal na ocupação dos nossos concorrentes.

Seu papel é analisar esses alertas, tomar uma decisão estratégica e registrar sua ação, tudo de forma centralizada aqui.

### 📋 2. Componentes da Planilha (As Abas)

A planilha é organizada em várias abas. As principais para o seu trabalho diário são:

* `**Dashboard**`: Sua tela inicial. Apresenta um resumo quantitativo dos alertas e traz avisos importantes sobre o uso da ferramenta.
* `**Alertas_Internos_Ativos**`: Aqui você encontrará a lista de picos de demanda identificados a partir dos nossos próprios dados de reserva. São os alertas que precisam da sua análise.
* `**Alertas_Externos_Ativos**`: Lista de picos de demanda identificados a partir da análise de mercado dos concorrentes. Também aguardam sua análise.
* `**Alertas_Internos_Arquivado**`: Repositório de todos os alertas internos que você já tratou e marcou como concluídos.
* `**Alertas_Externos_Arquivado**`: Repositório de todos os alertas externos que você já tratou.
* `**competitor_peak_demand**` **/** `**internal_peak_demand**`: Estas abas contêm os dados brutos que alimentam a planilha. **Por favor, não edite ou modifique nada nestas abas.**

### workflow 3. O Fluxo de Trabalho Diário (Passo a Passo)

Sua rotina de análise seguirá estes passos simples:

#### **Passo 1: Recebimento dos Alertas**

* Todos os dias, entre 8h e 9h, o sistema processa os dados e envia as listas de alertas atualizadas para os canais do Slack.
* Você deve copiar os dados do arquivo CSV recebido no Slack e colá-los nas abas `**Alertas_Internos_Ativos**` e `**Alertas_Externos_Ativos**` correspondentes. Certifique-se de limpar os dados antigos antes de colar os novos para evitar duplicidade.

#### **Passo 2: Análise dos Alertas**

* Acesse as abas "Ativos". Cada linha representa um alerta para um polígono em um período específico.
* **Seu objetivo é investigar o "porquê" deste alerta.** Verifique se há feriados, eventos locais (shows, congressos), notícias ou qualquer outro fator que justifique a alta demanda.
* Utilize as colunas de dados (explicadas na seção 4) para entender o contexto. Por exemplo, um alerta externo com `occupancy_rate` de 40% é um sinal forte de que o mercado está aquecido para aquela data.

#### **Passo 3: Ação e Registro (O mais importante!)**

Para cada linha que você analisar, você deve registrar sua ação usando as três colunas de controle à direita: `**Status**`, `**Check**` e `**Comentário**`.


1. **Preencha o** `**Status**`: Selecione uma das opções da lista suspensa.
   * `**Ajustado**`: Você tomou uma ação de precificação (ex: aumentou o preço, aplicou uma restrição de estadia mínima).
   * `**Não Aplicável**`: O alerta é válido, mas nenhuma ação é necessária (ex: o preço já está no teto, ou a estratégia é manter o preço atual).
   * `**Falso Positivo**`: Após análise, você concluiu que o alerta não representa uma oportunidade real.
   * `**Em Análise**`: Você está investigando, mas ainda não concluiu a ação.
2. **Adicione um** `**Comentário**` **(Opcional, mas recomendado)**: Use este campo de texto livre para dar mais contexto à sua decisão. Ex: "Preço aumentado em 20% devido ao festival de música local."
3. **Marque o** `**Check**`: **Este é o último passo!** Após preencher o `Status`, marque a caixa de seleção na coluna `Check`.
   * **Atenção**: Ao marcar esta caixa, a automação irá **copiar automaticamente a linha inteira** para a aba "Arquivado" correspondente. Isso sinaliza ao sistema que este alerta foi tratado.

### 📊 4. Entendendo as Colunas Principais

Para te ajudar na análise, aqui está o significado das colunas mais importantes:

#### Em `Alertas_Internos_Ativos`:

* `**lead_time_bucket**`: Faixa de antecedência com que as reservas foram feitas (ex: "61-90 dias").
* `**metric_value**`: O número de reservas que se sobrepõem na data do alerta.
* `**threshold_used**`: O limiar que foi ultrapassado para gerar o alerta. Se `metric_value` > `threshold_used`, o alerta é criado.
* `**ocupacao_concorrentes**`: A taxa de ocupação dos concorrentes na mesma data do alerta. Valida se a demanda é um movimento de mercado.
* `**competitor_same_day**`: **(MUITO IMPORTANTE)** Diz "sim" se, para este mesmo dia e polígono, também existe um alerta na aba de concorrentes. Um "sim" aqui significa um sinal de demanda muito forte!

#### Em `Alertas_Externos_Ativos`:

* `**occupancy_rate**`: A taxa de ocupação dos concorrentes para aquele período. É o principal indicador deste tipo de alerta.
* `**total_active_listings**`: O número de imóveis de concorrentes analisados. Ajuda a entender a liquidez do mercado.
* `**same_internal_date**`: **(MUITO IMPORTANTE)** O inverso da coluna acima. Diz "sim" se, para este mesmo dia, também existe um alerta interno. Novamente, um sinal de alta confiança.

### ⚠️ 5. Regras de Ouro e Boas Práticas

Para garantir a integridade do processo, por favor, siga estas regras:

* **❌ NÃO modifique as colunas** `**Check**`**,** `**Status**` **e** `**Comentário**` **entre 8h e 9h.** Este é o intervalo em que os dados automáticos são processados e enviados.
* **↩️ Para corrigir um erro**: Se você marcou um "Check" por engano, **vá até a aba "Arquivado" correspondente e exclua a linha que foi copiada para lá**.
* **🧘‍♂️ O processo é automático**: Não clique em botões de "atualizar" que não existam na aba `Dashboard`. A automação de arquivamento acontece sozinha quando você marca o "Check".
* **🚫 Não edite as abas de dados brutos** (`competitor_peak_demand`, `internal_peak_demand`). Isso pode quebrar as referências da planilha.
* **✅ Lembre-se**: A automação só funciona se o campo `Status` estiver preenchido **antes** de você marcar o `Check`.