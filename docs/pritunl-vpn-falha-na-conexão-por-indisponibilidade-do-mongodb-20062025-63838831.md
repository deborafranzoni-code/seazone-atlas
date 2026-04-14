<!-- title: [Pritunl VPN] - Falha na conexão por indisponibilidade do MongoDB - 20/06/2025 | url: https://outline.seazone.com.br/doc/pritunl-vpn-falha-na-conexao-por-indisponibilidade-do-mongodb-20062025-EBZKb9iJEK | area: Tecnologia -->

# [Pritunl VPN] - Falha na conexão por indisponibilidade do MongoDB - 20/06/2025

🕒 **Data:** 20/06/2025

🌍 **Ambiente:** Produção

☁️ **Cluster / Conta:** Google Cloud Platform - `tools-440117`


🚨 **Descrição do Incidente:** O serviço Pritunl VPN tornou-se inacessível com falha na autenticação e conexão de usuários. 

O servidor apresentava erro `pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused`, indicando que o Pritunl não conseguia conectar-se ao banco de dados MongoDB. 

Os logs mostravam falhas tanto no thread de execução de tarefas quanto no thread de verificação de tarefas do Pritunl. Usuários não conseguiam estabelecer conexões VPN.


🧠 **Causa Raiz:**

* **Espaço em disco crítico**: O disco principal (`/dev/root`) estava com 97% de utilização (8.4GB de 8.7GB), causando instabilidade no sistema

 ![](/api/attachments.redirect?id=285e0247-466e-455d-b1be-0c4e28e6895f " =802x274")

* **Lock file do MongoDB**: Arquivo `mongod.lock` permaneceu após crash anterior, impedindo a inicialização do serviço MongoDB

  ![](/api/attachments.redirect?id=3076cf07-481a-4ec5-ac5c-85b7b7189551 " =802x77")

  ![](/api/attachments.redirect?id=01c024fb-43de-4e09-95f0-1d0049ca6f33)


🔧 **Ações Corretivas Aplicadas**

**Solução Inicial (Resolução do Incidente):**

```bash
# 1. Limpeza de espaço em disco

sudo journalctl --vacuum-time=3d  # Liberou 192.1M

sudo apt clean && sudo apt autoclean

sudo truncate -s 0 /var/log/syslog /var/log/kern.log

sudo rm -f /var/log/*.log.*
sudo rm -f /var/log/*/*.log.*
sudo rm -f /var/log/*.gz

# 2. Correção do MongoDB

sudo rm -f /var/lib/mongodb/mongod.lock

sudo systemctl start mongod

# 3. Reinicialização do Pritunl

sudo systemctl restart pritunl
```

✅ **Resultados da Solução Inicial**

* **Limpeza inicial**: Utilização de disco reduziu de 97% para 94%
* **MongoDB**: Iniciou corretamente (`Active: active (running)`)
* **Pritunl**: Reconectou ao banco e voltou a funcionar normalmente
* **Servidor HTTPS**: Pritunl reiniciou na porta 80
* **Conexões VPN**: Voltaram a ser aceitas

 ![](/api/attachments.redirect?id=8d423ff8-6509-438d-95f9-e6771375761f)

**Ação Posterior (Expansão do Disco):**

Após resolver o incidente, foi realizada a expansão do disco para evitar recorrência do problema.

```bash
# 4. Expansão do disco
gcloud compute disks resize vpn-pqdt --size=20GB --zone=southamerica-east1-a

sudo gdisk /dev/sda  # Corrigir tabelas GPT (mismatch após resize)
sudo growpart /dev/sda 1  # Expandir partição

sudo resize2fs /dev/sda1  # Expandir filesystem
```

**Observação**: O comando `gdisk` foi necessário porque após o redimensionamento do disco no GCP, as tabelas GPT ficaram desatualizadas (`GPT PMBR size mismatch`), sendo preciso corrigi-las antes da expansão da partição.

 ![](/api/attachments.redirect?id=48a98844-08a9-465a-99bb-bcb9e021bb42 " =844x140")

✅ **Resultados da Expansão**

* **Expansão final**: Disco expandido de 8.7GB para 19GB
* **Utilização final**: Reduziu de 94% para **45%**
* **Espaço disponível**: Aumentou de 580MB para **11GB**

  ![](/api/attachments.redirect?id=8c378d35-fad6-4a92-8ded-0d2098a48f8a)

🔎 **Verificações**

```bash

sudo systemctl status mongod pritunl  # Ambos serviços ativos

df -h  # Confirmação: /dev/root 19G 8.1G 11G 45% /
sudo journalctl -u pritunl -f  # Logs sem erros de conexão

sudo fdisk -l  # Disco expandido para 20GB

# Acesso realizado com sucesso!
```


\
 ![](/api/attachments.redirect?id=6228bc54-a304-4700-8cce-b7e2b7c52b95)

📝 **Recomendações Futuras**


1. **Monitoramento de disco**: Implementar alertas quando uso ultrapassar 85%
2. **Limpeza automatizada**: Script cron para limpeza periódica de logs
3. **Monitoramento de serviços**: Alertas para falhas do MongoDB e Pritunl
4. **Documentação**: Procedimento operacional para esse tipo de falha

**Lições Aprendidas:**

* Mesmo com discos dedicados para dados (MongoDB), o disco do sistema operacional pode causar falhas
* A remoção do lock file do MongoDB foi suficiente para resolver o problema de inicialização
* A limpeza de logs pode liberar espaço significativo rapidamente


🏷️ **Tags**#pritunl #mongodb #diskspace #vpn #gcp


👥 **Responsáveis:** @[John Paulo da Silva Paiva](mention://56bd7d04-1766-4562-aae3-fa97977c743d/user/65c61c86-6a76-426e-8af9-6f1dd54caf65) 


**Duração Total do Incidente**: \~4h 52min (desde primeira falha até resolução completa)