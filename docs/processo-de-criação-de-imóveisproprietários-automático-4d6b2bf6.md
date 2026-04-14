<!-- title: Processo de criação de imóveis/proprietários automático | url: https://outline.seazone.com.br/doc/processo-de-criacao-de-imoveisproprietarios-automatico-Eh9jYEJ2DQ | area: Tecnologia -->

# Processo de criação de imóveis/proprietários automático

1. Pipedrive Comercial SZS
2. Card em Contrato
3. Card dado como **GANHO (ativação do trigger):**

   
   1. Mensagem no `#slack-webhook-wallet-tests`
   2. Informações de Log salva na tabela `**Property Onboarding Record**`

      
      1. **Sucesso:**

         
         1. O imóvel é criado
         2. e-mail de primeiro acesso enviado (quando o prop. não existe)
         3. Todas as informações salvas no banco de dados
         4. <https://stg.sapron.com.br/propriedades> para pesquisar propriedade
         5. <https://sapron.com.br/editardados/propriedade> para editar dados do imóvel
      2. **Erro:**

         
         1. O imóvel NÃO é criado
         2. Erros informados no `#slack-webhook-wallet-tests` para correção

            \

 ![](/api/attachments.redirect?id=db659460-55f9-4a50-8000-5af4be8720f8 " =1000x226.5")


**Observações:**


1. Caso o **ganho** for dado antes do card estiver em contrato, não ativa o trigger.
2. Para ativar o trigger novamente, precisa **reabrir** o card e dar como **Ganho** novamente.


Caso dê algum problema e precisamos voltar pro fluxo anterior:

* Desligar a Features Flag: `ff_sapron_backend_enable_onboarding_automation`