<!-- title: Criando novas branches | url: https://outline.seazone.com.br/doc/criando-novas-branches-YYpDzrLEZh | area: Tecnologia -->

# Criando novas branches

Todo novo desenvolvimento deve ser iniciado em cima da `branch main` uma vez que o desenvolvimento esteja a ponto de ser revisado, deve ser aberto um pull request para a branch main para integrar o desenvolvimento.

## Nosso padrão de nomenclatura de braches

* Os nomes das branches são compostos por duas partes: primeiro o tipo e segundo descrição. O tipo vem normalmente descrito no card e pode ser:
  * **docs:** apenas mudanças de documentação;
  * **feat:** uma nova funcionalidade;
  * **fix:** a correção de um bug;
  * **hotfix:** correção de um bug urgente;
  * **perf:** mudança de código focada em melhorar performance;
  * **refactor:** mudança de código que não adiciona uma funcionalidade e também não corrigi um bug;
  * **test:** adicionar ou corrigir testes.
* Exemplos de alguns nomes de branches que podem existir em nossa aplicação:

```
feat/create-payment-form
```

```
feat/create-payment-form
```

```
fix/property-search
```