<!-- title: Atualizações para o projeto | url: https://outline.seazone.com.br/doc/atualizacoes-para-o-projeto-ejOlgMwqho | area: Tecnologia -->

# Atualizações para o projeto

# **Monorepo**

O monorepositorio aumenta a complexidade para o desenvolvimento e entendimento do codigo. A implementação de CI/CD pode consumir mais recurso e tempo a medida que o repositorio aumenta. Também é mais dificil de isolar as dependencias de um monorepo para trabalhar com um projeto especifico.

## **Solução:**

Quebrar monorepo em projetos separados (back e front). Cada repositorio terá sua branch main bem como seus CI/CDs, idependencia para o ambiente de testes, isolamento entre projetos e libs.

# **Organização e Ramificação do projeto**

O cenário atual de manter varias branches principais como "main", "staging" e "production" não é uma boa prática. O ideal é manter uma branch principal com o codigo que está em produção ou com as atualizações que irão para produção, e branches auxiliares fixas como a developemnt (branch com modificação em staging), além das branches temporarias como feature, refactor, bugfix, hotfix. Fica difícil rastrear as alterações associadas a cada merge sem essa padronização. Reverter uma funcionalidade se algo der errado possui uma complexidade maior;

## **Solução:**

A utilização de um padrão como o gitflow para trazer mais organização para o repositorio. A intenção é separar melhor o desenvolvimento, cada funcionalidade e correção em seu próprio branch, facilitando o rastreamento e até mesmo a reversão de mudanças, se necessário.

# descrever

- [ ]  SonarQube
- [x]  Invoke
- [x]  Criar Guides (setup, onboarding, docs, etc)
- [ ]  Documentação da regra de negócio
- [ ]  Automatizar envs (staging e production)
- [x]  Gerar tags e changelog
- [ ]  Documentar código (back e front)
- [ ]  Estruturar testes
- [ ]  Reestruturar Módulos do back
- [ ]  Monitoramento dos ambientes de prod e staging
- [ ]  Desempenho das Querysets
- [ ]  Implementar SSO (permitir login com o Google)
- [ ]  Atualizar Readme, badges
- [ ]  Remover dump do banco de dados e usar faker
- [ ]  Colocar Cloudflare/AWS WAF no front e back
- [ ]  Separar [urls.py](http://urls.py) para cada app
- [ ]  Implementar mais testes
- [ ]  Alterar senha do admin
- [ ]  Colocar variáveis de ambiente dos apps no S3
- [ ]  Implementar um gerenciador de acessos melhor (talvez), nem que seja um interno só pro nosso time
- [ ]  Colocar created_at e updated_at em todas as tabelas
- [ ]  Algumas queries estão sujeitas a SQL injections (_Q_TEDS e _QUERY, por exemplo)