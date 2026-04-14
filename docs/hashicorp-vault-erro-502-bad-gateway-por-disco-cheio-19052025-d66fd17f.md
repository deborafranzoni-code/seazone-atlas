<!-- title: [HashiCorp Vault] - Erro 502 Bad Gateway por Disco Cheio - 19/05/2025 | url: https://outline.seazone.com.br/doc/hashicorp-vault-erro-502-bad-gateway-por-disco-cheio-19052025-SjeQaCsNhb | area: Tecnologia -->

# [HashiCorp Vault] - Erro 502 Bad Gateway por Disco Cheio - 19/05/2025

# 📌 HashiCorp Vault - Erro 502 Bad Gateway por Disco Cheio - 19/05/2025

## 🕒 Data

19/05/2025

## 🌍 Ambiente

Produção

## ☁️ Cluster / Conta AWS

Seazone Technology / EC2 (i-0244fb4c46013a717)

## 🚨 Descrição do Incidente

O serviço HashiCorp Vault ficou indisponível, retornando erro 502 Bad Gateway ao tentar acessar a interface web através do endpoint `https://vault.sapron.com.br/`. Este serviço é crítico para gerenciamento de segredos e credenciais da organização.

Ao investigar o servidor, identificamos que o disco estava com 100% de uso (7.6GB/7.6GB), impedindo o funcionamento adequado do contêiner Docker que hospeda o Vault. Além disso, o contêiner estava operando em estado "sealed" após sua reinicialização, necessitando das chaves de desbloqueio (unseal keys) para voltar a funcionar corretamente.

## 🧠 Causa Raiz

Identificamos duas causas principais:


1. **Disco cheio (100% de utilização)**: Arquivos de log e imagens Docker não utilizadas consumiram todo o espaço disponível do disco raiz, impedindo a operação normal do sistema e causando o erro 502.
2. **Vault em estado selado (sealed)**: Após reinicialização do contêiner, o Vault entrou em estado selado e requeria pelo menos 3 chaves de desbloqueio para voltar ao funcionamento normal. Estas chaves não estavam prontamente disponíveis no servidor.

## 🔧 Ações Corretivas Aplicadas

### 1. Liberação de espaço em disco:

```bash
# Remoção de logs antigos

sudo find /var/log -type f -name "*.gz" -delete

sudo find /var/log -type f -name "*.old" -delete

sudo find /var/log -type f -name "*.1" -delete

# Limpeza de recursos Docker não utilizados

docker rm $(docker ps -a -q -f status=exited)
docker image prune -a -f
```

### 2. Reinicialização do serviço Vault:

```bash

docker restart 611  # ID do contêiner vault-server
```

### 3. Desbloqueio do Vault:

Após conseguir as chaves de desbloqueio com @Marcio Fazolin, que as tinha salvas, procedemos com o desbloqueio do Vault utilizando a interface web. Foram necessárias 3 das 5 chaves de desbloqueio para completar o processo. Posteriormente, as chaves foram armazenadas de forma segura no AWS Systems Manager Parameter Store para evitar problemas futuros.

### 4. Expansão do volume do disco:

```bash
# Via AWS CLI, aumentamos o tamanho do volume de 8GB para 16GB

aws ec2 modify-volume --volume-id vol-0712c1d0c1477f519 --size 16

# Expansão da partição no sistema operacional

sudo growpart /dev/nvme0n1 1

# Expansão do sistema de arquivos

sudo resize2fs /dev/nvme0n1p1
```

### 5. Implementação de monitoramento preventivo:

Criamos um script para monitorar o uso do disco e alertar quando atingir níveis críticos:

```bash
#!/bin/bash
# Configuração

SLACK_WEBHOOK_URL="[WEBHOOK_REDACTED]"
SLACK_CHANNEL="#data-governanca"  
SERVER_NAME="Servidor Vault"
THRESHOLD=80  # Limite de porcentagem para alerta
# Verifica o uso do disco na partição raiz

CURRENT=$(df / | grep / | awk '{ print $5}' | sed 's/%//g')
AVAILABLE=$(df -h / | grep / | awk '{ print $4}')
TOTAL=$(df -h / | grep / | awk '{ print $2}')
USED=$(df -h / | grep / | awk '{ print $3}')
# Formata a data e hora

DATE=$(date "+%d/%m/%Y %H:%M:%S")
if [ "$CURRENT" -gt "$THRESHOLD" ]; then
    # Preparar a mensagem para o Slack
    read -r -d '' PAYLOAD << EOM
{
    "text": "*ALERTA: Espaço em disco crítico - ${SERVER_NAME}*\nO uso do disco está em *${CURRENT}%* (acima do limite de ${THRESHOLD}%)\n*Total:* ${TOTAL}\n*Usado:* ${USED}\n*Disponível:* ${AVAILABLE}\n*Data/Hora:* ${DATE}\n*Servidor:* $(hostname)"
}
EOM
    # Envia a mensagem para o Slack
    curl -s -X POST -H 'Content-type: application/json' --data "${PAYLOAD}" "${SLACK_WEBHOOK_URL}"
fi
```

Configuramos a execução deste script diariamente via cron:

```bash

0 9 * * * /usr/local/bin/check-disk-space.sh
```

## ✅ Resultados

* Serviço Vault completamente restaurado e operacional.
* Espaço em disco aumentado de 8GB para 16GB, reduzindo o uso de 93% para 46%.
* Implementação de alertas preventivos para evitar problemas futuros relacionados a espaço em disco.
* Chaves de desbloqueio armazenadas de forma segura no SSM Parameter Store.

## 🔎 Verificações

```bash
# Verificação do status do Vault

ubuntu@ip-172-31-22-185:/usr/local/bin$ docker exec vault-server vault status

Key                     Value
---                     -----
Seal Type               shamir

Initialized             true

Sealed                  false

Total Shares            5

Threshold               3

Version                 1.11.0

Build Date              2022-06-17T15:48:44Z

Storage Type            raft

Cluster Name            vault-cluster-5d13986c

Cluster ID              fca4a8e8-39f1-dbec-23e9-1b593bd5bd04

HA Enabled              true

HA Cluster              https://127.0.0.1:8201

HA Mode                 active

Active Since            2025-05-19T18:44:27.487463314Z

Raft Committed Index    297111

Raft Applied Index      297111

# Output: Sealed: false (confirmando que o Vault está desbloqueado)

# Verificação de espaço em disco

ubuntu@ip-172-31-22-185:/usr/local/bin$ df -h

Filesystem       Size  Used Avail Use% Mounted on
/dev/root         16G  6.9G  8.5G  45% /
tmpfs            961M     0  961M   0% /dev/shm

tmpfs            385M  1.1M  384M   1% /run

tmpfs            5.0M     0  5.0M   0% /run/lock
/dev/nvme0n1p15  105M  6.1M   99M   6% /boot/efi

tmpfs            193M  4.0K  193M   1% /run/user/1000

# Output: /dev/root  16G  6.9G  8.5G  45% /

# Teste de acesso à interface web

ubuntu@ip-172-31-22-185:/usr/local/bin$ curl -I https://vault.sapron.com.br/ui/
HTTP/2 200 
date: Mon, 19 May 2025 19:59:46 GMT

content-type: text/html; charset=utf-8

content-length: 587359

accept-ranges: bytes

cache-control: no-store

content-security-policy: default-src 'none'; connect-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'unsafe-inline' 'self'; form-action  'none'; frame-ancestors 'none'; font-src 'self'
service-worker-allowed: /
strict-transport-security: max-age=31536000; includeSubDomains

vary: Accept-Encoding

x-content-type-options: nosniff

# Output: HTTP/1.1 200 OK
```

## 📝 Recomendações Futuras


1. **Implementar Auto-Unseal do Vault**: Configurar o Vault para desbloquear automaticamente utilizando o serviço AWS KMS, conforme documentação: [Auto-Unseal com AWS KMS](https://developer.hashicorp.com/vault/docs/configuration/seal/awskms).
2. **Aumentar monitoramento de recursos**: Adicionar monitoramento mais abrangente para CPU, memória, e conexões de rede, além do disco.
3. **Documentar procedimento de desbloqueio do Vault**: Criar documentação clara sobre o procedimento de desbloqueio do Vault e localização segura das chaves para referência da equipe.
4. **Avaliar upgrade do Vault**: Considerar atualização para versão mais recente do HashiCorp Vault que tenha melhorias de estabilidade e novas funcionalidades.

## 🏷️ Tags

\#vault #hashicorp #aws #ecw #disk-space #docker #unseal #auto-unseal #monitoring

## 👥 Responsáveis

[john.paiva@seazone.com.br](mailto:john.paiva@seazone.com.br)

[guilherme.santos@seazone.com.br](mailto:guilherme.santos@seazone.com.br)

[marcio.fazolin@seazone.com.br](mailto:marcio.fazolin@seazone.com.br)