<!-- title: Formato de entregas em Data | url: https://outline.seazone.com.br/doc/formato-de-entregas-em-data-MQHGLaG9wr | area: Tecnologia -->

# Formato de entregas em Data

## Estrutura Proposta para o Slack:


1. **Mensagem Principal no Canal (Header da Entrega):**

   ```none
     --- 📢 NOVA ENTREGA | TIME DE DADOS ---
   *Título:* [Nome padrão utilizado no Card/Epic - Ex: Inativar Imóveis da Precificação (Sirius)]
   
   *Para:* [@ÁreaSolicitante ou @PessoaPrincipal]
   
   *Data:* DD/MM/AAAA
   
   *Tipo:* [BI | Planilha | API | Alerta | ML | Feature | Atualização]
   
   *ID da Task :* `[JIRA-123(caso epic colocar o epic)]`
   
    *Todos os detalhes, como usar, validar e impactos na THREAD *
   ```

   \
2. **Primeira Mensagem na Thread (Detalhes da Entrega):**

   ```none
   --- 💬 DETALHES DA ENTREGA: [Repetir o Título da Task para Contexto] ---
   
   *🎯 Objetivo Principal/Problema Resolvido:*
   [Descreva em 1-2 frases o valor que esta entrega gera para o cliente interno.]
   
   *✅ O que foi Entregue (Visão do Cliente):*
   *   Ponto 1
   *   Ponto 2
   *   ...
   
   *🛠️ Como Utilizar/Acessar:*
   [Instruções diretas de como o cliente pode interagir com a entrega.]
   *   Ex: Acesse a planilha X no link Y, aba Z.
   *   Ex: A nova feature está disponível na tela W do sistema ABC, seguindo os passos...
   
   *🔍 Como Validar (Critérios de Aceite):*
   [O que o cliente interno deve verificar para confirmar que a entrega atende à sua necessidade?]
   *   Ex: Verifique se os imóveis marcados como 'inativo' não aparecem mais nas regras de precificação.
   
   *⚠️ Impactos e Observações Relevantes:*
   [Qualquer informação adicional importante: dependências, efeitos colaterais, limitações conhecidas.]
   *   Ex: Imóveis marcados como 'inativos' serão removidos da visualização X.
   
   *🔗 Links Úteis (Documentação, Planilha, Dashboard, etc.):*
   *   `[Nome do Recurso 1]: [Link]`
   *   `[Nome do Recurso 2]: [Link]`
   
   *🙋 Ponto de Contato (Time de Dados):* `[@seu.nome ou @nome.do.responsavel.pela.entrega]`
   
   *🏷️ Tags para Busca:* `#[NomeDoProjeto/Produto] #[TipoDeEntrega] #[AreaSolicitante] #[PalavraChave1]`
   ```

## Exemplo Prático 


1. **Mensagem Principal no Canal (Header da Entrega):**

   ```none
   --- 📢 NOVA ENTREGA | TIME DE DADOS ---
   
   *Título:* Implementação de Tag para Imóveis em Teste no PriceLabs
   *Para:* @Fábio Biasi , @Lucas Borges   
   *Data:* 26/05/2025
   *Tipo:* Feature (Planilha)
   *ID da Task :* `https://seazone.atlassian.net/browse/DS-572`
   
   *Todos os detalhes, como usar, validar e impactos na THREAD
   ```
2. **Primeira Mensagem na Thread:**

   ```none
   --- 💬 DETALHES DA ENTREGA: Funcionalidade para Inativar Imóveis da Precificação (Sirius) ---
   
   *🎯 Objetivo Principal/Problema Resolvido:*
   Permitir que o time de precificação possa facilmente excluir imóveis específicos das regras de 
   precificação automática, sem removê-los completamente do sistema, para casos como imóveis em 
   PriceLabs ou outras situações especiais.
   
   
   *✅ O que foi Entregue (Visão do Cliente):*
   *   Implementada a lógica para reconhecer imóveis marcados como 'Inativo' no produto Sirius.
   *   Imóveis designados como 'Inativo' serão desconsiderados de todas as regras de precificação.
   *   A designação é feita diretamente na planilha `setup grupos`.
   
   🛠️ Como Utilizar/Acessar:*
   *   Acesse a planilha `setup grupos`, que faz parte do produto Sirius.
   *   Navegue até a aba `Grupos`.
   *   Na terceira coluna ('Tipo de Grupo'), para os imóveis desejados, preencha com o valor `Inativo`.
   *   Opcional: Na coluna 'Justificativa', pode-se adicionar um motivo (ex: `PriceLabs`). Este campo é apenas para registro e não afeta a funcionalidade.
   
   *🔍 Como Validar (Critérios de Aceite):*
   *   Escolha um imóvel teste e marque-o como `Inativo` conforme as instruções acima.
   *   Verifique se este imóvel não é mais considerado nas simulações/cálculos de precificação quando rodar a AGC.
   *   Confirme que o imóvel não aparece com preços da Stays no 'Supervisório'.
   
   *⚠️ Impactos e Observações Relevantes:*
   *   **Supervisório:** Imóveis marcados como 'Inativos' serão retirados do 'Supervisório' no que tange a preços da Stays, pois estariam com valores incorretos se precificados externamente (ex: PriceLabs).
   *   **BI-CS/RM:** Os valores de preços das diárias para imóveis 'Inativos' estarão incorretos ou não serão exibidos.
   *   **Acompanhamento de Locação:** Será possível continuar acompanhando os valores de locação desses imóveis (informação do Sapron) normalmente, no BI-CS/RM.
   
   *🔗 Links Úteis:*
   *   `Planilha Sirius - Setup Grupos`: `https://docs.google.com/spreadsheets/d/1MdC9TJreLsOZyUDRu0kxB8kkzmb-E4mt9BueXAv5ESc/edit?gid=0#gid=0]`
   
   
   *🙋 Ponto de Contato (Time de Dados):* `@Lucas Abel `
   ```

   \
   \
   \
   \
   \
   \