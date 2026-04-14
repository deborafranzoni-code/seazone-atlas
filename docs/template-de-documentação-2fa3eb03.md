<!-- title: Template de documentação | url: https://outline.seazone.com.br/doc/template-de-documentacao-QbQLO021XL | area: Tecnologia -->

# Template de documentação

### Modelo de documentação

> Este modelo será usado para documentações de features do frontend. Este modelo deve ser seguido por todos  do frontend para documentar uma feature.

## Fluxograma

Sites que facilitam a criação de fluxogramas:

<https://app.diagrams.net/>

<https://whimsical.com/>

Para utilizar o modelo, basta copiar e colar no arquivo da documentação que está criando.

```markdown
# MÓDULO: {Atendimento, Proprietário, Anfitrião, Financeiro...}
## Tela: {nome da página}

## Feature: {nome da feature}
### Descrição da feature
Descreva aqui a feature...

Permissões:** {attedant, admin, host, owner, ...} 
**Rota para a página:** `/rotadapagina`

**Fluxograma:**
(Link para o fluxograma)[linkaqui.com.br]

### Instruções para o usuário**
Descreva aqui o passo a passo para o usuário testar a feature...

**### Como está codado?**
Adicione aqui informações importantes sobre como está codado a página...

APIs utilizadas:**
- `/endpoint/`
- `/outro/endpoint/`**

### Como testar esta feature?
Descreva o passo a passo para testar está funcionalidade
- Passo 1
- Passo 2

### Onde está o código?
Informe o link/caminho para onde está localizado o código desta feature

### Dicas de manutenção/o que está hard coded?
```

* Visualização da doc

  # MÓDULO: {Atendimento, Proprietário, Anfitrião, Financeiro...}

  ## Tela: {nome da página}

  ## Feature: {nome da feature}

  ### Descrição da feature

  Descreva aqui a feature...

  **Permissões:** {attedant, admin, host, owner, ...} **Rota para a página:** `/rotadapagina`

  **Fluxograma:** (Link para o fluxograma)\[[linkaqui.com.br](http://linkaqui.com.br/)\]

  ### Instruções para o usuário

  Descreva aqui o passo a passo para o usuário testar a feature...

  ### Como está codado?

  Adicione aqui informações importantes sobre como está codado a página...

  **APIs utilizadas:**
  * `/endpoint/`
  * `/outro/endpoint/`

  ### Como testar esta feature?

  Descreva o passo a passo para testar está funcionalidade
  * Passo 1
  * Passo 2

  ### Onde está o código?

  Informe o link/caminho para onde está localizado o código desta feature

  ### Dicas de manutenção/o que está hard coded?