<!-- title: Estrutura do front | url: https://outline.seazone.com.br/doc/estrutura-do-front-vuRY63RpQa | area: Tecnologia -->

# Estrutura do front

---

A organização de pastas do front está colocada da seguinte forma:

* ***src***
  * ***assets →*** local destinado para os ícones e animações da aplicação
    * ***icons →*** - local destinada para ícones (todo arquivo inserido aqui deve ter o prefixo `icon_` no nome).
    * ***images →*** - local destinada para imagens (todo arquivo inserido aqui deve ter o prefixo `img_` no nome)
    * ***logo →*** - local destinada para logos (todo arquivo inserido aqui deve ter o prefixo `logo_` no nome)
  * ***components →*** local destinado para os componentes customizados da aplicação. Todo componente criado deve ter uma pasta com o nome referente a ele.
  * ***constants →*** local destinado para declarar constantes que serão usadas no projeto.
  * ***context →*** local destinado para os contextos que permitem gerenciar os estados compartilhados entre os componentes da aplicação
  * ***hooks →*** local destinado para os hooks da aplicação \*\*
  * ***layouts →*** local destinado para os layouts usados na aplicação \*\*
  * ***pages →*** *local destinado para as páginas*
    * ***apis →*** local destinado para as apis do front (bff).
  * ***services →*** *local destinado para os adicionar as requisições às apis*
  * ***styles →*** local destinado para os estilos globais e paleta de temas da aplicação
  * ***utils →*** local destinado para a criação de funcionalidades úteis da aplicação (exemplo: *Formatação de máscara de CPF, telefone, números, datas, entre outros.*)
  * ***Routes.tsx →*** local destinado para a definição das rotas e permissões de acesso às páginas da aplicação