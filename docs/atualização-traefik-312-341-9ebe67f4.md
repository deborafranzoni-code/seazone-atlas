<!-- title: Atualização traefik 3.1.2 =>  3.4.1 | url: https://outline.seazone.com.br/doc/atualizacao-traefik-312-341-qKZ028O3y6 | area: Tecnologia -->

# Atualização traefik 3.1.2 =>  3.4.1

## Documentação Técnica: Atualização do Traefik de v3.1.2 para v3.4.1 em EKS\*\*


---

### 1. Objetivo da Atualização

Adequar o Traefik às versões mais recentes do Amazon EKS (1.3, 1.31 e 1.32), garantindo compatibilidade e suporte contínuo.


---

### 2. Justificativa Técnica

* **Suporte ao Kubernetes**: O Traefik segue a política de suporte do Kubernetes, garantindo compatibilidade com as três versões mais recentes. 
* **Compatibilidade com EKS**: Versões anteriores do Traefik podem não ser compatíveis com as versões mais recentes do EKS, necessitando de atualização para assegurar funcionalidade plena.


---

### 3. Procedimentos de Atualização

#### 3.1 Atualização do chart via Terraform

Para instalar ou atualizar o Traefik com suporte para as versões v3.3 e v3.4:

```hcl

resource "helm_release" "traefik" {
  name       = "traefik"
  namespace  = "traefik"
  repository = "https://traefik.github.io/charts"
  chart      = "traefik"
  version    = "34.4.0"

  values = [
    file("${path.module}/values.yaml")
  ]
}
```

#### 3.2 Atualização do traefik via Terraform no values

```yaml

image:
  registry: docker.io
  repository: traefik
  tag: v3.4.1 #ajustado de 3.12 para 3.4.1
  pullPolicy: IfNotPresent
```


---

**Nota**: A versão 34.4.0 do Helm Chart é a primeira a oferecer suporte condicional para as versões v3.3 e v3.4 do Traefik. 

#### 3.3 Aplicação das CRDs

Atualize as Custom Resource Definitions (CRDs) para a versão v1.8.1:

```bash

kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.4/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
```


**Importante**: A aplicação das CRDs é necessária para a compatibilidade com a versão v3.4 do Traefik.

#### 3.4 Atualização do ClusterRole

Modifique o ClusterRole para conceder permissões adequadas:

```yaml

kind: ClusterRole

metadata:
  name: traefik-traefik

rules:
  - apiGroups:
      - ""
    resources:
      - services
      - secrets
      - nodes
      - configmaps
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - discovery.k8s.io
    resources:
      - endpointslices
    verbs:
      - list
      - watch
  - apiGroups:
      - extensions
      - networking.k8s.io
    resources:
      - ingresses
      - ingressclasses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - update
  - apiGroups:
      - traefik.io
    resources:
      - middlewares
      - middlewaretcps
      - ingressroutes
      - traefikservices
      - ingressroutetcps
      - ingressrouteudps
      - tlsoptions
      - tlsstores
      - serverstransports
      - serverstransporttcps
    verbs:
      - get
      - list
      - watch
```


**Justificativa**: A partir da versão v3.4, o Traefik passou a utilizar o `reflector` para assistir recursos como `ConfigMap`, `Endpoints` e `Endpointslices`. A ausência de permissões adequadas resultava no erro:

```

Unhandled Error" err="k8s.io/client-go@v0.31.1/tools/cache/reflector.go:243: Failed to watch *v1.ConfigMap: failed to list *v1.ConfigMap: configmaps is forbidden: User \"system:serviceaccount:traefik:traefik-sa\" cannot list resource \"configmaps\" in API group \"\" at the cluster scope"
```


A atualização do ClusterRole resolve esse problema.


---

### 4. Validação Pós-Atualização

Após a atualização, execute os seguintes comandos para verificar o estado do Traefik:

* **Verificar Pods**:

  ```bash
  kubectl get pods -n traefik
  ```


*Todos os pods devem estar no estado* `Running` com a imagem `traefik:v3.4.1`.

* **Verificar Logs**:

  ```bash
  kubectl logs -n traefik <nome-do-pod>
  ```


*Os logs devem indicar que a versão do Traefik é* `v3.4.1` e não devem apresentar erros relacionados a permissões.

* **Verificar CRDs**:

  ```bash
  kubectl get crds | grep traefik
  ```


*As CRDs devem estar presentes com o grupo* `traefik.io`.


---

### 5. Rollback (Se Necessário)

Se for necessário reverter a atualização:

```bash

helm rollback traefik <REV_ANTERIOR>
kubectl apply -f backup-crds-v3.3.yml
```


**Nota**: Certifique-se de ter um backup das CRDs anteriores antes de realizar o rollback.


---

### 6. Considerações Finais

* **Compatibilidade**: A atualização para o Traefik v3.4.1 assegura compatibilidade com as versões mais recentes do EKS.
* **Segurança**: A versão v3.4.1 do Traefik inclui correções de segurança importantes.
* **RBAC**: A atualização do ClusterRole é essencial para garantir que o Traefik tenha as permissões necessárias para operar corretamente na versão v3.4.