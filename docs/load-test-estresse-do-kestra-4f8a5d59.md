<!-- title: Load Test & Estresse do Kestra | url: https://outline.seazone.com.br/doc/load-test-estresse-do-kestra-GpKzSI6tii | area: Tecnologia -->

# Load Test & Estresse do Kestra

Ambiente: **Kestra OSS 1.2.2** no GKE, worker com **16 threads**, namespace `production`. Data do teste: **2026-02-03**.


---

## Por quê 

Antes de decidir pela migração, precisávamos saber quanto a instância do Kestra aguenta na prática. Não só em cenários ideais, mas com múltiplas execuções ao mesmo tempo, com processamento pesado, e com a API em requisições rápidas. A ideia foi replicar, mais ou menos, o que aconteceria se nós disparássemos vários workflows de um só lado.


---

## O que foi testado

Dois flows simples criados só pra isso, ambos na namespace `production`:

| Flow | O que faz | Input principal |
|----|----|----|
| `load-test-sleep` | Simula execução com duração configurável (`time.sleep`) | `sleep_seconds` (default "5") |
| `load-test-cpu` | Multiplicação de matrizes via numpy — processamento CPU real | `matrix_size` (default "600") |

Quatro cenários, executados em sequência com 5s de pausa entre cada um:

| Cenário | Objetivo | Configuração |
|----|----|----|
| **BURST** | Disparar o máximo de execuções ao mesmo tempo | 20 × sleep (8s) simultâneas |
| **API STRESS** | Martelo rápido na API — testa throughput do scheduler | 40 × sleep (3s) em sequência, sem intervalo |
| **HEAVY** | Processamento CPU pesado | 5 × matrix 800×800 simultâneas |
| **MIXED** | Carga mista realista | 10 × sleep (8s) + 5 × matrix 600×600 ao mesmo tempo |


---

## Cenário 1 — BURST

 ![worker durante as 20 execuções simultâneas](/api/attachments.redirect?id=a4dcab6d-1245-497c-b18f-6ec9f1f8bf30 " =750x375")

**O que aconteceu:** as 20 execuções foram disparadas ao mesmo tempo. O worker preencheu os 16 threads em menos de 5 segundos. As 4 execuções que sobram ficaram na fila `pending` até um thread abrir. Todas completaram em 37s, sem falha.

| Métrica | Valor |
|----|----|
| Execuções disparadas | 20 |
| Resultado | ==20/20 SUCCESS== |
| Tempo total | 37.1s |
| Latência trigger (avg / min / max) | 808 / 639 / 900 ms |

**Observação:** foi o cenário que mostrou mais claramente o limite de 16 threads. A linha `pending` apareceu e ficou em 4 durante o pico, exatamente 20 - 16. Quando os primeiros sleep de 8s terminaram, a fila foi zerando rapidamente.


---

## Cenário 2 — API STRESS

 ![ Ocupação do worker durante os 40 triggers sequenciais](/api/attachments.redirect?id=86caaadc-6f7e-42ad-ad1f-b225c49b9141 " =750x375")

 ![ Latência de cada requisição individual, mostrando a degradação progressiva
](/api/attachments.redirect?id=7f77065f-6031-466a-8477-d7bb1b6600f6 " =825x375")

> **O que aconteceu:** 40 triggers disparados um após o outro, sem pausa. As primeiras 3 requisições voltaram em \~760ms. A partir da 4ª, a latência começou a subir e não parou, chegou a 1565ms na última. Todas as 40 execuções completaram em 50s.

| Métrica | Valor |
|----|----|
| Execuções disparadas | 40 |
| Resultado | ==40/40 SUCCESS== |
| Tempo total | 50.5s |
| Latência trigger (avg / min / max) | 1294 / 759 / 1565 ms |
| Slope da degradação | +16ms por requisição |

**Observação:** a degradação foi linear e muito consistente -+16ms por requisição. Isso não é a API travando, é o scheduler ficando mais ocupado à medida que a fila de execuções pendentes cresce. A 40 requisições a diferença acumulada foi de \~640ms. 


---

## Cenário 3 — HEAV

>  ![ ocupação do worker durante os 5 jobs CPU pesados](/api/attachments.redirect?id=7b288473-28d6-4398-b6d5-4c9ac1144727 " =750x375")
>
> **O que aconteceu:** 5 jobs de multiplicação de matrizes 800×800 rodam simultaneamente dentro de containers Docker separados. O worker manteve exatamente 5 threads ocupados durante \~60 segundos, todo o tempo que a multiplicação levou. Sem fila, sem pending.

| Métrica | Valor |
|----|----|
| Execuções disparadas | 5 |
| Resultado | ==5/5 SUCCESS== |
| Tempo total | 72.4s |
| Latência trigger (avg / min / max) | 608 / 558 / 754 ms |

**Observação:** foi o cenário com menor latência de trigger, só 5 requisições na API, sem contencão. O ponto mais importante aqui é que o processamento CPU acontece dentro do container, completamente isolado. O worker apenas gerencia a thread e não roda o cálculo na memória dele.


---

## Cenário 4 — MIXED

 ![ ocupação do worker durante os 5 jobs CPU pesados](/api/attachments.redirect?id=9e6dc44d-96e0-4d91-afca-fdafe4a97897 " =750x375")

**O que aconteceu:** 15 execuções misturadas, 10 sleep de 8s e 5 jobs CPU de 600×600. Todas disparadas ao mesmo tempo. O worker encheu rapidamente e ficou no limite durante a maior parte do teste. Os sleep terminaram primeiro (8s), liberando threads para os CPU que levaram mais tempo.

| Métrica | Valor |
|----|----|
| Execuções disparadas | 15 |
| Resultado | ==15/15 SUCCESS== |
| Tempo total | 79.9s |
| Latência trigger (avg / min / max) | 1043 / 821 / 1148 ms |

**Observação:** não há priorização entre tipos de workload. Sleep e CPU competem pelos mesmos 16 threads em base primeiro-a-chegar. Na prática, isso significa que um job longo de CPU não trava os outros mas ocupa uma thread enquanto roda.


---

## Comparativo geral

 ![Comparação de latência de trigger entre os 4 cenários (min / avg / max)](/api/attachments.redirect?id=c22b0650-6e4e-4780-b39b-29e965429553 " =825x375")

 ![painel com os 4 cenários lado a lado


](/api/attachments.redirect?id=ad2c8ba4-635c-4f99-8630-4c427a0f06d7 " =1350x750")

| Cenário | Execuções | Sucesso | Duração | Trigger avg | Trigger max |
|----|----|----|----|----|----|
| BURST | 20 | 20/20 | 37s | 808ms | 900ms |
| API STRESS | 40 | 40/40 | 51s | 1294ms | 1565ms |
| HEAVY | 5 | 5/5 | 72s | 608ms | 754ms |
| MIXED | 15 | 15/15 | 80s | 1043ms | 1148ms |
| **Total** | **80** | **80/80** | — | — | — |

Zero falhas em 80 execuções.


---

## Insights & implicações


1. **O limite é 16 threads no worker.** Qualquer coisa acima disso vai para a fila `pending` e aguarda. ==Não falha, apenas espera.== Configurável via Helm (`worker.threads`).
2. **CPU-bound não trava a instância.** Cada execução roda em container próprio. O worker só gerencia a thread, o cálculo pesado é isolado. ==Uma vantagem real frente ao modelo do Argo, onde um container travado podia impactar o pod.==
3. **Não há priorização de workloads.** Sleep e CPU competem igualmente pelos threads. 

## Arquivos gerados

Todos no diretório raiz do projeto (`playground/testes/`):

 ![](/api/attachments.redirect?id=8fc1b9d1-58e6-4acf-84b6-587c927c199b " =1279x204")

| Arquivo | O que é |
|----|----|
| `load-test-sleep.yml` | Flow alvo, sleep configurável |
| `load-test-cpu.yml` | Flow alvo, multiplicação de matrizes |
| `run-load-test.py` | Script principal — executa os 4 cenários, coleta métricas, gera gráficos |


---

[run-load-test.py 12835](/api/attachments.redirect?id=8e7b4d58-9311-48ff-b10b-be46549a5add)

<https://kestra.seazone.com.br/ui/main/flows?filters%5Bscope%5D%5BEQUALS%5D=USER>