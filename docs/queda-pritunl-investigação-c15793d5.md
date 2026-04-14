<!-- title: Queda Pritunl [investigação] | url: https://outline.seazone.com.br/doc/queda-pritunl-investigacao-8D9apdhMiG | area: Tecnologia -->

# Queda Pritunl [investigação]

# Relatório de Análise: Incidente VPN Pritunl (Maio 2025)

## Resumo Executivo

Em 5 de maio de 2025, a VPN Pritunl apresentou uma falha reportada pelos usuários. Durante nossa investigação, descobrimos que os logs necessários para identificar a causa raiz do problema foram perdidos devido à substituição completa da instância VPN em 6 de maio, onde a nova instância foi criada a partir de uma imagem desatualizada de janeiro de 2025.

## Análise do Incidente

### Cronologia dos Eventos


1. **10 de janeiro de 2025**: Criação da imagem "pritunl-mongo" da instância VPN original
2. **Janeiro a Maio 2025**: Operação normal da VPN na instância "vpn-1rsk"
3. **5 de maio de 2025**: Ocorrência do incidente reportado pelos usuários (causa raiz desconhecida)
4. **6 de maio de 2025, 05:58:59**: Exclusão da instância "vpn-1rsk" (contendo os logs do incidente)
5. **6 de maio de 2025, 06:02:58**: Criação da nova instância "vpn-xplq" a partir da imagem de janeiro

### Evidências Coletadas

#### Identificação da Substituição da Instância

Verificamos que houve uma substituição completa da instância e não apenas uma reinicialização:

```bash
# Verificar quando a instância atual foi criada

gcloud compute instances list --project="tools-440117" --filter="name~'vpn'" --format="table(name, zone, status, creationTimestamp)"
```

Resultado:

```
NAME      ZONE                  STATUS   CREATION_TIMESTAMP

vpn-xplq  southamerica-east1-a  RUNNING  2025-05-06T06:02:58.094-07:00
```

```bash
# Verificar operações de exclusão de instâncias VPN

gcloud compute operations list --project="tools-440117" --filter="operationType=delete AND targetLink~vpn" --limit=5
```

Resultado:

```
NAME                                                     TYPE    TARGET                                   HTTP_STATUS  STATUS  TIMESTAMP

operation-1746536339566-634772e1b7137-b9409eed-a3b86a40  delete  southamerica-east1-a/instances/vpn-1rsk  200          DONE    2025-05-06T05:58:59.841-07:00
```

#### Origem da Nova Instância

A instância atual foi criada a partir de uma imagem de janeiro:

```bash
# Verificar origem do disco atual

gcloud compute disks describe vpn-xplq --zone=southamerica-east1-a --project="tools-440117" --format="json(name, sizeGb, sourceImage, creationTimestamp)"
```

Resultado:

```json
{
  "creationTimestamp": "2025-05-06T06:02:58.102-07:00",
  "name": "vpn-xplq",
  "sizeGb": "10",
  "sourceImage": "https://www.googleapis.com/compute/v1/projects/tools-440117/global/images/pritunl-mongo"
}
```

```bash
# Verificar detalhes da imagem utilizada

gcloud compute images describe pritunl-mongo --project="tools-440117" --format="json(name, creationTimestamp, sourceDisk)"
```

Resultado:

```json
{
  "creationTimestamp": "2025-01-10T09:27:05.824-08:00",
  "name": "pritunl-mongo",
  "sourceDisk": "https://www.googleapis.com/compute/v1/projects/tools-440117/zones/southamerica-east1-a/disks/instance-20250110-170255"
}
```

#### Verificação do Sistema e Logs

```bash
# Verificar quando o sistema atual foi iniciado

uptime -s

who -b
```

Resultado:

```
2025-05-06 13:03:16

system boot  2025-05-06 13:03
```

```bash
# Verificar histórico de reinicializações

sudo last reboot | head
```

Resultado:

```
reboot   system boot  6.8.0-1020-gcp   Tue May  6 13:03   still running

reboot   system boot  6.8.0-1020-gcp   Fri Jan 10 17:16 - 17:21  (00:05)
reboot   system boot  6.8.0-1020-gcp   Fri Jan 10 17:04 - 17:13  (00:09)
reboot   system boot  6.8.0-1020-gcp   Thu Jan  9 18:27 - 11:46  (17:18)

wtmp begins Thu Jan  9 18:27:06 2025
```

```bash
# Verificar histórico de reinicializações do MongoDB

sudo grep "SERVER RESTARTED" /var/log/mongodb/mongod.log
```

Resultado:

```
{"t":{"$date":"2025-01-09T18:54:40.819+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-01-09T18:55:25.247+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-01-09T18:59:34.386+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-01-10T17:04:17.444+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-01-10T17:06:18.556+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-01-10T17:09:53.123+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-01-10T17:16:42.331+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-05-06T13:03:47.324+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
{"t":{"$date":"2025-05-06T13:04:11.397+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
```

```bash
# Verificar configuração de discos da VPN

df -h /var/lib/mongodb
```

Resultado:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb         98G  404M   93G   1% /var/lib/mongodb
```

#### Análise da Perda de Logs

Durante a análise, descobrimos uma descontinuidade significativa nos logs:

```
# Resultado do grep "SERVER RESTARTED" no MongoDB
{"t":{"$date":"2025-01-10T17:16:42.331+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
[... lacuna de janeiro a maio ...]
{"t":{"$date":"2025-05-06T13:03:47.324+00:00"},"s":"I",  "c":"CONTROL",  "id":20698,   "ctx":"main","msg":"***** SERVER RESTARTED *****"}
```

## Impacto da Substituição da Instância

A investigação foi comprometida devido à perda completa dos logs do incidente por causa da substituição da instância:


1. A instância original da VPN "vpn-1rsk" estava em operação até 6 de maio de 2025
2. Após o incidente reportado em 5 de maio, a instância foi substituída por "vpn-xplq"
3. A nova instância foi criada a partir de uma imagem "pritunl-mongo" de janeiro de 2025
4. Consequências dessa substituição:
   * Perda definitiva dos logs operacionais entre janeiro e maio de 2025
   * Impossibilidade de determinar a causa raiz do incidente
   * Perda do histórico de eventos e configurações do período

## Recomendações

Para evitar problemas semelhantes no futuro, recomendamos:


1. **Gerenciamento de Imagens**:
   * Atualizar regularmente as imagens de backup da VPN
   * Documentar claramente o processo de substituição de instâncias
2. **Persistência de Logs**:
   * Configurar o Cloud Logging para capturar logs do Pritunl e MongoDB
   * Implementar um sistema de armazenamento de logs externo (Stackdriver, Elastic, etc.)
3. **Backups e Snapshots**:
   * Configurar um processo de backup antes de qualquer substituição de instância
4. **Documentação e Processos**:
   * Documentar a arquitetura da VPN e seus componentes
   * Estabelecer um processo claro para atualizações e substituições
   * Implementar um checklist pré-substituição que inclua backup de dados e logs
5. **Monitoramento**:
   * Implementar monitoramento proativo do serviço Pritunl
   * Configurar alertas para falhas e problemas de conectividade

## Conclusão

Não foi possível determinar a causa raiz do incidente original da VPN ocorrido em 5 de maio, devido à perda completa dos logs quando a instância "vpn-1rsk" foi substituída pela nova instância "vpn-xplq" em 6 de maio. A nova instância foi criada a partir de uma imagem de janeiro de 2025, resultando na perda definitiva dos registros do período entre janeiro e maio.

Esta investigação destaca a importância crítica de manter logs persistentes e realizar backups adequados antes de qualquer substituição de infraestrutura. A implementação das recomendações acima é essencial para garantir que futuros incidentes possam ser adequadamente diagnosticados, mesmo após mudanças na infraestrutura.