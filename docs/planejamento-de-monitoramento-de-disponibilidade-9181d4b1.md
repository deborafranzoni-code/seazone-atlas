<!-- title: Planejamento de Monitoramento de Disponibilidade | url: https://outline.seazone.com.br/doc/planejamento-de-monitoramento-de-disponibilidade-beu2sSBTfA | area: Tecnologia -->

# Planejamento de Monitoramento de Disponibilidade

# Objetivo

Este documento tem como objetivo organizar e definir o escopo do desenho de um futuro dashboard no Grafana para monitorar o processo de atualização de disponibilidade dos nossos imóveis. A proposta visa garantir suporte à ampliação da janela de disponibilidade para além de 180 dias. Para mais detalhes de como o processo funciona hoje, consulte o documento **[Processo de disponibilidade e sincronização com a stays](/doc/processo-de-disponibilidade-e-sincronizacao-com-a-stays-Nj6E5SaAGJ)**.

# Sugestão

## Métricas de Execução

* Total de execuções em um intervalo de tempo (X);
* Total de exceções disparadas por triggers em um intervalo de tempo (X);
* Taxa de sucesso (% de execuções sem erro);
* Tempo médio de execução por task.

## Recursos do Servidor

* Uso de CPU;
* Uso de Memória.

## Fila de Processamento

* Total de tasks na fila;
* Taxa de sucesso no processamento das tasks.

## Alertas

* Taxa de sucesso < 90% em X execuções consecutivas;
* Uso de memória > 80% por mais de Y minutos.

# Próximos passos

* Necessário o Grafana de prod estár estável para a construção da dash.