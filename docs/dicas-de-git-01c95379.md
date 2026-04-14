<!-- title: Dicas de Git | url: https://outline.seazone.com.br/doc/dicas-de-git-xeeAQdtIqn | area: Tecnologia -->

# Dicas de Git

### Como voltar a um commit específico

git reset --hard <commit_hash> git push origin develop -f

***Atenção****: Isso irá voltar toda a branch **develop** para o commit especificado. É importante que faça backup do que foi commitado nesse meio tempo para evitar perca de trabalho. Use isso com cautela.*