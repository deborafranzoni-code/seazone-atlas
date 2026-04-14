<!-- title: Sincronização de reservas - Refatoração Stays | url: https://outline.seazone.com.br/doc/sincronizacao-de-reservas-refatoracao-stays-HreXM1GmcG | area: Tecnologia -->

# Sincronização de reservas - Refatoração Stays

* **Sincronização de reservas**

  
  1. Garantir que as reservas sejam sincronizadas em tempo real, trazendo mais transparência aos proprietários e garantindo que os anfitriões consigam fazer a operação sem transtornos em casos de reservas de última hora e em casos de extensão (early check-in, late check-out)

  **O que fazemos hoje?** Está implementado o webhook que sincroniza as reservas em tempo real. Os gatilhos de disparo são os eventos da criação de novas reservas e atualização das reservas já existentes. 2. Garantir que o valor das taxas de limpeza sejam os valores atualizados na stays. Valores atualizados devem passar a valer a partir da DATA DE CRIAÇÃO de novas reservas. Exemplo: Imóvel A possui uma limpeza de R$250. No dia 24/10 a limpeza foi alterada para R$200. Portanto, todas as reservas que foram criadas até o dia 24/10 devem conter o valor de R$250. Reservas criadas a parir de 24/10 devem conter o valor de R$200,00 3. Garantir que a limpeza seja repassada para fins de fechamento no período de lançamento da stays 4. Garantir que uma reserva que possui mais de uma limpeza lançada seja repassada para fins de fechamento 5. Garantir que a data de lançamento de ajuste de limpeza apareça com acrual_date e cash_date para que seja considerado no fechamento. O que acontece atualmente é que um valor é inserido com data de registro 11/10, mas por algum motivo as colunas de acrual_date e cash_date aparece 19/10. Além disso, se tem algum valor de limpeza zerado, o valor de ajuste de limpeza não é considerado. O valor de ajuste de limpeza precisa ser considerado mesmo se o valor de limpeza do imóvel estiver zerado

  \
  
  1. Garantir que reservas de realocação reflitam nos calendários dos imóveis para os quais foram realocados
  2. Garantir que todos os valores cobrados e alterados devido a extensão ou saída antecipada sejam refletidos no sapron
  3. Garantir que reservas com extensão sejam sincronizadas mesmo que seu status esteja "conciliado"
  4. Garantir que a Stays seja um espelho do Sapron e vice versa, e que qualquer inconsistência seja reportado em log ou canal do Slack
  5. Garantir que bloqueios realizados no Sapron sejam refletidos instantaneamente na Stays e vice-versa
  6. Garantir que imóveis de compra e venda recebam suas respectivas reservas, considerando que a regra vigente é: a partir da data de contrato todas as reservas são migradas para o novo imóvel e todas as reservas até esta data permaneçam com o imóvel "antigo"
* **Garantir que alterações de listings sejam sincronizados em tempo próximo ao real**

  Listings neste contexto se trata da criação dos calendários de imóveis dentro da Stays. O que ocorre é que em alguns casos o listing é recriado e precisamos garantir que para estes, ocorra a migração de bloqueios e reservas para os novos listings, bem como a sincronização destes bloqueios e reservas no Sapron.

  **O que temos hoje?** Temos um webhook implementado que atualiza os listings de uma em uma hora.

  **O que precisamos fazer?**

  
  1. Diminuir o tempo de sincronização dos listings, para algo em torno de 5 a 10 minutos
  2. Garantir que criemos bloqueios e reservas no novo calendário apenas para casos em que o id na reservation tenha como status Ativo ou Concluído
* **Garantir que as extensões de reservas sejam sincronizadas em tempo real**

  É recorrente recebermos extensões de reservas, tanto de early check-in como late check-out.

  \*\*Qual a diferença de criação de extensões do Sapron entre as plataformas?

  (necessário investigar como está acontecendo no código e garantir que o Sapron seja um espelho da Stays)

  O que temos hoje?\*\*

  Precisamos garantir que as mesmas sejam refletidas nas telas: multicalendário, tela de controle e calendário proprietário.