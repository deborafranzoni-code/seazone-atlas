<!-- title: Post-mortem - Divergência de Saldo | url: https://outline.seazone.com.br/doc/post-mortem-divergencia-de-saldo-B9HewjOXxw | area: Tecnologia -->

# Post-mortem - Divergência de Saldo

**Projeto/Sistema:** Sapron e WalletSapron\n**Data do Evento:** 24/04/2025\n**Autor(es):** Natália Bessa, Roberto Campos, Renata Domingues, Bruno da Silva Campos, Felipe Ribeiro Machado\n**Data do Relatório:** 12/0512/05/2025


## **1. Visão Geral**


### Descrição do Incidente 

O problema teve início com reservas apresentando taxa de limpeza zerada. Isso ocorreu porque a Stays passou a enviar o valor da limpeza em uma nova chave, que ainda não estava integrada ao nosso sistema. Para mitigar o impacto imediato, implementamos uma correção temporária.

Na tentativa de acelerar a normalização dos valores, buscamos sincronizar as reservas diretamente pelo Sapron. No entanto, começaram a surgir relatos de que algumas reservas não estavam sendo sincronizadas corretamente na ferramenta.

Em seguida, franqueados passaram a reportar divergências nos valores exibidos no dashboard financeiro, indicando flutuações nos dados ao longo do dia.

Durante a investigação, identificamos também um problema na regra de negócio aplicada no grid financeiro do anfitrião, que estava calculando de forma incorreta a distribuição dos valores.

### Impacto: 

* Todos os franqueados Seazone estavam sofrendo com a divergência de saldo, pois a feature flag estava chamando as rotas das tabelas com prefixo `proper_pay` que estavam descontinuadas.
* Reservas a partir de 22/04 foram afetadas com com taxas de limpeza zeradas, o que ocasionou com que proprietários e anfitriões tivessem a visualização errada dos valores a receber.

### Gravidade: 

==Altíssima== - Dados financeiros incorretos, falta de transparência com o cliente final, sensação de insegurança.


---

## **2. Linha do Tempo do Incidente**

| Data | Evento |
|----|----|
| 22/04 | Identificamos que stays havia alterado o parâmetro de envio de taxa de limpeza. |
| 23/04 | Sapron começou a considerar extra fee para taxa de limpeza, fazendo com que reservas a partir dessa data não fossem mais afetadas. |
| 23/04 | Como medida paliativa, tentamos realizar uma sincronização de todas as reservas pelo Sapron para garantir que os valores de taxa de limpeza fossem atualizados de forma correta. |
| 24/04 | Identificamos que não estávamos sincronizando reservas no Sapron desde a noite anterior. Foi identificado que a fila de sincronizar reservas ficou engargalada por conta da tentativa de sincronização pelo Sapron. |
| 24/04 | Primeiro report de divergências de valores no dashboard financeiro - Franquias. |
| 28/04  | Identificamos que a tela de dashboard financeiro estava puxando dados das tabelas `proper_pay` - no mesmo dia tiramos do ar a FF que ocasionava o problema. |
| 29/04 | Subimos o ajuste de taxa de limpeza e com isso tiramos o código o experimento de diluição de taxa de limpeza. |
| 30/04 | Divergência de saldo do dashboard financeiro voltou a acontecer |
| 02/05 | Feito o rollback do ajuste de taxa de limpeza e voltamos o código de experimento de taxa de limpeza diluída na diária. |
| 05/05 | Iniciamos as investigações para verificar se as tabelas `proper_pay` ainda estavam sendo consumidas.  |
| 05/05 | Subimos o ajuste que corrigia a regra de negócio do dashboard financeiro. |
| 05/05 | Ajuste de configuração de envio de taxa de limpeza na Stays. |



---

## **3. Causa Raiz**

* Feature flag estava falhando, e nos momentos de falha, utilizava as tabelas de prefixo `proper_pay` (tabela descontinuada do cálculo de fechamento anterior) para povoar o Sapron.
* Ao realizar a refatoração do código que puxava corretamente o valor da taxa de limpeza segundo reestruturação da API da Stays, deletamos do código a parte que considerava os imóveis do experimento de taxa de limpeza diluída. Por este motivo, as taxas de limpeza dos imóveis que participaram do experimento foram inferidas incorretamente com o valor 0.
* Ajuste de taxa de limpeza estava sendo mostrado na linha de "outros recebimentos" e não na linha de "Receita de limpeza".


---

## **4. Resolução e Medidas Tomadas**

* Investigação na tabela `reservation_reservation` de [todas as reservas](https://docs.google.com/spreadsheets/d/1NeQPxKZVptffHS0PxxkSvFmXVdBa8trpWk8jD4vmzsM/edit?usp=sharing) que estavam com a taxa de limpeza zerada.


* Feature flag foi desconsidera no Sapron.
* Rollback no código que atualizava as taxas de limpeza seguindo o novo modelo da API da Stays. Com a reversão, o cálculo da taxa de limpeza passou a ser calculado corretamente
* Refatoração do código, garantindo que que a os dados de ajuste de limpeza fossem mostradas na linha correta do dashboard (Receita de limpeza)


---

## **5. Ações Preventivas**

| Ação | Prazo | Responsável |
|----|----|----|
| Criação de KPI que monitora reservas com taxa de limpeza zeradas indevidamente | ==Implementado== |    |
| Verificar e remover todas as rotas que fazem inferência às tabelas `proper_pay` e garantir que a rota aponte para as tabelas de prefixo `closing_` | 26/05/2025 |   |
| Criar monitoramento das filas de importação de reservas  | 23/05/2025 |    |
| Solicitar da stays a publicação de releases a respeito das rotas utilizadas no Sapron | a definir |    |



---

## **6. Lições Aprendidas**

* Envolver a engenharia desde o inicio da investigação para garantir uma solução definitiva mais rápida.
* Não subir nada relacionado as fluxos crítico de fechamento financeiro, próximo/durante o processo de fechamento do mês.
* Tratamento de erros de feature flags.
* Monitoramento de tempo de vida das feature flags no sistema.
* Melhorar senso de urgência durante gestão de crise.
* Criar processo para averiguação de necessidade de remoção de tabelas no banco.
* Solicitar da stays a publicação de releases.