<!-- title: Como organizamos os secrets no Kestra OSS | url: https://outline.seazone.com.br/doc/como-organizamos-os-secrets-no-kestra-oss-Cjhs0iQ7Ny | area: Tecnologia -->

# Como organizamos os secrets no Kestra OSS

## Opção atual: 

## ==Kubernetes Secret + extraEnv (em uso)==

Como funciona:

* Secrets armazenados em um K8s Secret (`kestra-app-secrets`, namespace `kestra-poc`)
* Injetados nos pods via `extraEnv` no Helm values
* No flow, acessados com `{{ secret('NOME') }}`

Implicações:

* Funciona no OSS sem configuração extra
* Requer **double base64**: uma camada para o Kestra (que espera SECRET_ em base64), outra para o K8s Secret (que faz decode automático)
* Secrets são visíveis para quem tem acesso ao cluster (`kubectl get secret`)
* Para adicionar ou alterar um secret, precisa editar o K8s Secret **e** o Helm values (extraEnv)

Config necessária no Helm:

```yaml
common:
  extraEnv:
    - name: SECRET_NOME
      valueFrom:
        secretKeyRef:
          key: SECRET_NOME
          name: kestra-app-secrets
```

Para encodar um novo secret:

```bash
# valor original → base64 (Kestra) → base64 novamente (K8s)
echo -n 'valor_original' | base64 | base64
```


---

## Outras opções no OSS

### ==Hardcoded no YAML do flow== 

* Colocar valores diretamente no `env:` do task
* Funciona mas expõe secrets no código do flow visível no UI
* Sem controle de rotação

### ==.env montado via Volumes==

* Criar um K8s Secret com um arquivo `.env` e montar como volume no worker
* O script lê o arquivo diretamente com `open('.env')`
* Problema: o caminho do volume precisa ser consistente entre os containers do DinD, difícil de garantir

### ==ConfigMap== 

* ConfigMap não é encriptado
* Visível em plain text por qualquer um com acesso ao namespace


---

## ==Secrets via API externa dentro do task==

A integração nativa do Kestra com secrets managers externos (`kestra.secrets.backend`) é Enterprise. Mas nada impede de **chamar a API do secrets manager diretamente dentro de um task**. Nesse caso, o único secret que precisa vir via `{{ secret() }}` é a credencial de acesso ao manager.

### Como funciona na prática


1. Armazena no Kestra OSS apenas a credencial de acesso (ex: AWS access key, Vault token)
2. No task, chama a API do secrets manager para buscar o valor real em runtime
3. Usa o valor dentro do mesmo script

> * AWS SSM / Secrets Manager
> * GCP Secret Manager
> * HashiCorp Vault

**Implicações geral dessa abordagem:**

* Só precisa manter 1-2 secrets no Kestra (credenciais de acesso ao manager)
* Rotação dos secrets acontece no manager, sem tocar o Kestra
* Adiciona latência na execução (uma chamada de API a mais por task)
* A credencial de acesso ao manager ainda precisa do double base64 + extraEnv


---

## O que realmente é Enterprise (sem workaround)

| Opção | O que seria |
|----|----|
| `kestra.secrets.backend` ==nativo== | ==Integrar secrets manager direto na configuração do Kestra, sem precisar de task intermediário== |
| ==Namespace Variables== | ==Variáveis por namespace, sem precisar de env== |
| ==Namespace-level Secrets== | ==Secrets isolados por namespace== |


---

## Secrets atuais no ambiente

| Secret | Usado por |
|----|----|
| POSTHOG_API_URL | fetch_posthog_views |
| POSTHOG_PROJECT_ID | fetch_posthog_views |
| POSTHOG_PERSONAL_API_KEY | fetch_posthog_views |
| METABASE_API_URL | fetch_metabase_reservations |
| METABASE_API_KEY | fetch_metabase_reservations |
| S3_ACCESS_KEY_ID | upload_to_s3 (desabilitado) |
| S3_SECRET_ACCESS_KEY | upload_to_s3 (desabilitado) |
| S3_REGION | upload_to_s3 (desabilitado) |
| S3_BUCKET_PROPERTIES_RANKING | upload_to_s3 (desabilitado) |