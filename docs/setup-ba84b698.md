<!-- title: SETUP | url: https://outline.seazone.com.br/doc/setup-pV8jm0LVJv | area: Administrativo Financeiro -->

# SETUP

# **==________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Criação do menu com todos os botões para execução dos scripts

## *==———Documentação—————————==*

* Não há documentação

## *==———Sugestão————————————==*

* Usar texto descritivos para execução dos scripts
* Criar submenus, com os nomes das abas

# **==__________________Scripts______________________==**

### `onOpen`

* **Objetivo**: código para Gerar Menu de Código

```jsx
function onOpen() {
  var UserInterface = SpreadsheetApp.getUi();
  var MainMenu = UserInterface.createMenu("Menu Especial")

  .addSubMenu(UserInterface.createMenu("Consolidado")
    .addItem("📄 Atualizar", "MainConsolidado") 
    .addSeparator()
    .addItem("📄 Atualizar", "MainConsolidado") 
  )

  MainMenu.addToUi();
}
```