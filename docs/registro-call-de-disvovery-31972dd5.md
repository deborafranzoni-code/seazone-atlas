<!-- title: Registro call de Disvovery | url: https://outline.seazone.com.br/doc/registro-call-de-disvovery-SPz5wOAXaz | area: Tecnologia -->

# Registro call de Disvovery

# **Transcrição Estruturada - Call de Discovery: Evolução dos Sistemas de Alerta de Alta Demanda e Eventos**

## **Participantes**

* **Victor Guindani** - Analista de RM (usuário principal)
* **Fábio de Biasi Garcia** - Gerente de RM
* **Lucas Abel da Silveira** - Product Manager (facilitador)

## **1. Processo Atual de Uso dos Alertas**

### **1.1. Alertas de Concorrentes**

**Fluxo de trabalho atual:**


1. Recebe alertas no canal #data-alerts-rm-pico-demanda-em-concorrentes
2. Para cada alerta, verifica no BI se a região Seazone está ocupando
3. Se não estiver ocupando, pesquisa no Google por eventos na região
4. Se encontrar evento relevante, avalia ação; caso contrário, coloca em "stand by"
5. Regiões que sempre apitam sem ocupação (ex: São Paulo) são tratadas como dinâmica normal

**Exemplos de ações tomadas:**

* "Poucas vendas na SZ, período da Consciência"
* "São_Paulo-Butanta: Sem vendas, mas vale aumentar preços porque já vendemos bem novembro"
* "Salvador-Centro: Preços parecem ok, ainda não vendemos nada em novembro"

### **.2. Alertas Internos (Pico de Demanda)**

**Fluxo de trabalho atual:**


1. Recebe alertas no canal #data-alerts-rm-pico-demanda
2. Abre cada alerta no BI para verificar ocupação real
3. Analisa se o pico representa oportunidade real ou ruído
4. Verifica se é evento conhecido ou padrão sazonal
5. Decide por ação (aumentar preços) ou ignorar

**Tempo gasto:**

* Alertas de concorrentes: tempo variável
* Alertas internos: aproximadamente 1 hora por dia, dependendo do volume

## **2. Principais Dores e Problemas Identificados**

### **2.1. Excesso de Ruído e Falsos Positivos**

**Problemas específicos:**

* Alertas repetidos para datas adjacentes (ex: dia 20 e depois dia 22)
* Alertas para regiões onde Seazone não tem imóveis ativos (ex: Santos-Praia)
* Alertas para datas já rastreadas (eventos conhecidos como Natal, Reveillon)
* "Jogo de Tetris" - reservas longas que se sobrepõem em apenas um dia, gerando alerta irrelevante

### **2.2. Falta de Contexto e Informações Relevantes**

**Informações ausentes:**

* Ocupação real da Seazone no período
* Se o evento já está rastreado ou mapeado
* Comparação entre ocupação Seazone vs concorrentes
* Cadência das reservas (reservas antigas vs recentes)

### **2.3. Formato Inadequado de Entrega**

**Problemas com CSVs:**

* Múltiplos arquivos fragmentados por região
* Dificuldade para identificar repetições
* Não permite histórico ou acompanhamento de ações
* "Vem quebrando por cidade em várias mensagens fica ruim de importar para planilha"

### **2.4. Parametrização Inadequada**

**Problemas identificados:**

* Limiares muito sensíveis para regiões com muitos concorrentes (ex: São Paulo)
* Janela de análise muito curta (30 dias) gera ruído em períodos próximos
* Não considera tamanho relativo do polígono (ex: 3 reservas em polígono de 200 imóveis é irrelevante)

## **3. Sugestões e Melhorias Propostas**

### **3.1. Melhorias nos Alertas de Concorrentes**

**Sugestões do usuário:**


1. **Filtro de eventos já rastreados:** "Se já tem o evento, a gente ia conseguir eliminar boa parte"
2. **Ajuste de limiares por região:** "São Paulo deve ter centenas de concorrentes, era tipo 15% ocupar, é meio normal"
3. **Incluir ocupação Seazone:** "Se a gente tivesse uma coluna aqui da nossa ocupação nesse período, seria legal"
4. **Unificar em um único arquivo:** "Vir tudo em um csv só"
5. **Delta crítico:** "Considerar delta SZ e concorrentes para apitar? Se ja estivermos acima dos concorrentes não tem problema"

### **3.2. Melhorias nos Alertas Internos**

**Sugestões do usuário:**


1. **Ajustar parâmetros V2:** Aumentar limiares (ex: de 3 para 5 reservas, de 4 para 6, de 15% para 20%)
2. **Considerar tamanho do polígono:** Aumentar porcentagem para polígonos muito grandes
3. **Filtro de datas adjacentes:** Considerar range de ±3 dias para evitar alertas repetidos
4. **Filtro de final de semana:** "Às vezes vende muito o final de semana, talvez botar um filtro seu período de final de semana"
5. **Aumentar janela inicial:** Mudar de 23-60 dias para 35-60 dias para sair do mês atual

### **3.3. Melhorias Gerais para Ambos Sistemas**

**Sugestões do usuário:**


1. **Integração com planilha (similar ao de preços):**
   * Uma aba para cada tipo de alerta
   * Colunas para status e check
   * Histórico para análise futura
   * Comunicação via status na planilha
2. **Lógica de reaparecimento:**
   * "Se aumentar 100% e comentar. Se ocupar os nossos imóveis nessa região, aí volta de novo o alarme"
   * Reaparecer apenas se houver mudança significativa na ocupação
3. **Validação automática:**
   * Verificar se região tem imóveis ativos antes de alertar
   * Cruzar com calendário de eventos conhecidos
   * Considerar cadência das reservas (reservas recentes vs antigas)

## **4. Insights e Observações Importantes**

### **4.1. Sobre a Utilidade dos Alertas**

* **Validação do MVP:** "O objetivo inicial como MVP foi validado, está sendo útil para RM, eles têm diariamente olhado os alertas, verificado as ocorrências e por vezes tomado ações"
* **Preferência por alertas internos:** "Acaba que você acaba utilizando muito mais o interno mesmo ali, do que o externo, que é o concorrentes"

### **4.2. Sobre a Análise Manual**

* **Processo complexo:** "Esse aqui eu gasto, dependendo do quanto que vem, eu gasto uma hora nele. É o que mais demora também, de fato"
* **Análise visual:** "Quando você bota no BI aqui, você consegue entender o que que tá acontecendo, entendeu? Daí, pra mim, é bem difícil parametrizar isso aí no sentido de um algoritmo fazer"

### **4.3. Sobre Padrões Identificados**

* **"Jogo de Tetris":** Reservas longas que se sobrepõem em apenas um dia, gerando alerta irrelevante
* **Reservas casadas:** "Às vezes tem muita venda casadinha, entre pessoas da mesma família, ou coisa do tipo"
* **Dinâmicas regionais:** "São Paulo, por exemplo, eu sei que ele sempre apita no dia 6 de dezembro, uma coisa assim. Só que a gente não ocupa"

## **5. Priorização de Implementação**

### **5.1. Definição de Prioridade**

**Pergunta do PM:** "Qual dos dois eu boto na frente para eles fazerem? Alerta de preços anômalos ou detector de eventos?"

**Resposta do Victor:**

* "Eu gasto mais tempo nesse dos nossos internos. Então, esse... E sendo feito mais rápido, acho que..."
* "Geralmente é esse \[alertas internos\]. E o preço anómalo ali, quando eu coloco na planilha assim, dá para... Às vezes ele apita coisa repetida e eu já vou cortando assim, dá para ir mais rápido"

**Resposta do Fábio:**

* "Pensa pela lógica de qual você gera mais encaminhamento, menos o que você..."

**Conclusão:** Alertas internos (pico de demanda) têm prioridade maior por:


1. Consomem mais tempo do analista
2. Geram mais encaminhamentos/acões
3. São mais complexos de analisar manualmente

## **6. Próximos Passos Definidos**


1. **Documentação:** PM vai preparar documento consolidando todos os pontos
2. **Validação:** Stakeholders irão revisar o documento para garantir que todos os pontos foram cobertos
3. **Priorização:** Alertas internos serão priorizados na implementação
4. **Estruturação:** Epic será preparado para a equipe de Solutions