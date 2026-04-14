<!-- title: Boilerplate workflows | url: https://outline.seazone.com.br/doc/boilerplate-workflows-NAZzAzlcCS | area: Tecnologia -->

# Boilerplate workflows

## Visão Geral

O repositório **governanca-workflows-template** é responsável por armazenar e padronizar todos os workflows utilizados nas pipelines do cluster. Ele tem como objetivo centralizar, organizar e otimizar o uso dos arquivos de workflows do GitHub Actions, facilitando a implementação, reutilização e manutenção dos processos automatizados.


:::warning
Sempre tomar muito cuidado ao fazer alteração para a main deste repositório, pois ele controla os workflows de todos os serviços do cluster. Uma alteração incorreta pode gerar erros no ci dos times.

:::

## Benefícios

* **Padronização**: Garante consistência na configuração e execução das pipelines.
* **Reutilização**: Evita a duplicação de código ao fornecer workflows modulares e compartilháveis.
* **Facilidade de Manutenção**: Centraliza as definições, tornando mais simples a aplicação de correções e melhorias.
* **Otimização de Tempo**: Reduz esforços na criação e gestão de workflows para novas pipelines.

## Uso dos Workflows

Os workflows armazenados aqui são projetados para serem referenciados por outros repositórios através de **reusable workflows** do GitHub Actions. Isso permite que diferentes projetos utilizem a mesma definição padronizada sem precisar duplicar os arquivos.

### Exemplo de Referência a um Workflow Reutilizável

```bash
  build:
    name: Building
    permissions:
      contents: read
      id-token: write
    uses: seazone-tech/governanca-workflows-template/.github/workflows/app-ci-build.yaml@main
    secrets:
      account_region: x
      account_id: x
      deployment_role: x
    with:
      app_name: "x"
      cluster_namespace: 'x'
      build: 'x'
```

### Arquivos do Repositório

| Arquivo | Ação | Key-words |
|----|----|----|
| app-ci-build-wallet-bff.yaml | Cria imagem específica para o wallet-bff (env) | Build |
| app-ci-build-wallet.yaml | Builda novas imagens para produção e staging sempre (cliente) | Build |
| app-ci-build.yaml | Workflow padrão de build | Build |
| app-ci-notify.yaml | Notifica a ocorrência de um workflow no slack e trigga o gitops | Notificação e Trigger |
| app-ci-preparing.yaml | Valida requisitos para rodar como Dockerfile e nome | Validação |
| app-deploy-helm.yaml | Realiza ações no cluster como deploy e reboot  | Deploy, Reboot |
| gitops-new-version-dispatch.yaml | Recebe o trigger no gitops e atualiza o arquivo values.yaml | Values.yaml |