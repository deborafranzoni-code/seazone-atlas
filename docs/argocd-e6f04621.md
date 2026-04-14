<!-- title: ArgoCD | url: https://outline.seazone.com.br/doc/argocd-m9JaKkX70L | area: Tecnologia -->

# ArgoCD

# O que é 

**Argo CD** é uma ferramenta de gerenciamento de implantação e entrega contínua (CD) para Kubernetes. Ela permite que as aplicações sejam implantadas e gerenciadas de maneira eficiente e escalável, utilizando um modelo baseado em GitOps. A principal função do Argo CD é garantir que o estado desejado da aplicação, armazenado em repositórios Git, seja refletido automaticamente no ambiente Kubernetes.

# Como funciona 

O Argo CD funciona com base no conceito de **GitOps**, onde a configuração das aplicações é armazenada em um repositório Git. O Argo CD monitora esse repositório e garante que o estado das aplicações no Kubernetes esteja sempre alinhado com o que está definido no Git.

Quando uma alteração é feita no repositório Git, o Argo CD detecta automaticamente essa mudança e aplica as configurações no cluster Kubernetes, garantindo que as aplicações sejam atualizadas conforme necessário. Caso algo mude no cluster que não corresponda ao repositório Git, o Argo CD pode corrigir automaticamente ou notificar os administradores para que tomem uma ação

# Como utilizar 

Abaixo estarão explicadas algumas funcionalidades e caracteristicas que quando entendidas facilitam o uso da ferramenta ArgoCd 

## Health Status

No Argo CD, **Health Status** refere-se ao estado atual das aplicações e dos recursos que estão sendo monitorados dentro do cluster Kubernetes

### 1. **Healthy**

**Significado:** A aplicação ou recurso está funcionando corretamente e está em conformidade com o estado desejado no repositório Git. Não há discrepâncias ou problemas

### 2. **Degraded**

**Significado:** A aplicação ou recurso está em funcionamento, mas existe algum problema que está impedindo o seu funcionamento ideal. Isso pode ser causado por falhas na configuração ou recursos não funcionando corretamente.

### 3. **Progressing**

**Significado:** A aplicação ou recurso está em processo de atualização ou deploy. Isso indica que o Argo CD está tentando aplicar uma nova versão ou configuração, mas o processo ainda não foi concluído.

### 4. **Suspended**

**Significado:** A aplicação foi pausada manualmente ou devido a uma política configurada no Argo CD. Nesse estado, não há mais atualizações ou mudanças sendo aplicadas à aplicação.

### 5. **Missing**

**Significado:** O recurso ou aplicação foi removido do cluster Kubernetes, mas ainda está presente no repositório Git. Isso significa que o estado desejado não pode ser aplicado porque o recurso foi perdido ou excluído do cluster.

### 6. **Unknown**

**Significado:** O estado da aplicação ou recurso não pôde ser determinado. Isso pode ocorrer devido a problemas de comunicação com o cluster ou outros erros inesperados.

## Sync Status 

### **Synced**

**Significado:** A aplicação ou recurso está completamente sincronizado com o estado desejado no repositório Git. Ou seja, as configurações no cluster Kubernetes estão em conformidade com o que foi definido no repositório.

###  **OutOfSync**

**Significado:** A aplicação ou recurso não está em conformidade com o estado desejado no repositório Git. Isso significa que houve alterações no cluster Kubernetes que não foram aplicadas no repositório Git, ou o estado do repositório Git foi alterado e o cluster ainda não foi atualizado.

### **Syncing**

**Significado:** A aplicação ou recurso está em processo de sincronização. O Argo CD está aplicando as alterações definidas no repositório Git para o cluster Kubernetes, mas o processo de sincronização ainda não foi concluído.

## Namespaces 

Namespaces são utilizados para criar divisões no cluster onde serviços podem ser organizados, por exemplo no namespace de monitoring haverá coisas de monitoramento, esses namespaces podem ser utilizados como filtros ali na interface do argo 

## Componentes visualizados 

### **Services**

**Descrição**: O **Service** é um recurso fundamental no Kubernetes para expor os pods dentro de um cluster ou para o mundo externo. Ele cria uma abstração de rede para os pods e define como as solicitações de rede são direcionadas para os pods adequados.

### **Ingress**

**Descrição**: O **Ingress** é um recurso no Kubernetes que gerencia o acesso externo aos serviços dentro do cluster, geralmente baseado em HTTP e HTTPS. Ele define regras de roteamento para enviar solicitações para diferentes serviços, de acordo com o host ou o caminho da URL.

### **Pods**

**Descrição**: O **Pod** é a menor unidade de execução no Kubernetes e pode conter um ou mais containers. Todos os containers dentro de um pod compartilham o mesmo espaço de rede (endereço IP, portas) e armazenamento. Os pods são a base para a execução de qualquer aplicação no Kubernetes.

### **Secrets**

**Descrição**: O **Secret** é um objeto no Kubernetes usado para armazenar e gerenciar informações sensíveis, como senhas, chaves de API ou certificados SSL. Eles são armazenados de forma codificada base64, mas devem ser utilizados de forma segura para evitar vazamento de dados sensíveis.