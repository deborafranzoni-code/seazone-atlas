<!-- title: Edição de dados | url: https://outline.seazone.com.br/doc/edicao-de-dados-awTml23Mgp | area: Tecnologia -->

# Edição de dados

> *Implementar a interface e integração das páginas de edição de dados para que o time de Onboarding tenha autonomia para editar dados das propriedades.*

**Rota:** /editardados/ **Permissões:** Admin, SeazoneOnboarding

### Detalhes da tarefa

Haverá uma tela principal de edição de dados onde o usuários poderá selecionar quais dados quer editar. Inicialmente teremos apenas o card de "Editar dados da Propriedade" onde levará para um formulário para o usuário realizar a edição.

**Comportamento da página:**

* Usuário entra na página "Editar dados"
* Sistema exibe as possibilidades de edição, neste caso, será exibido o card de "Editar propriedade"
* Usuário seleciona "Editar propriedade"
* Sistema carrega formulário de edição de propriedade

Para que editar alguma propriedade, primeiro o usuário deverá selecionar um imóvel para editar, para isso:

* Será exibido um seletor de imóvel que será preenchido com a API `GET /calendar/properties/` exibindo apenas os imóveis que **não** estão **inativos**.
* Ao selecionar a propriedade, deverá ser realizado uma requisição na API `/properties/details/` (ou `property/manager`) e carregar os dados retornados nos respectivos campos para edição.

Ao fim da página haverá dois botões:

* **Cancelar**: volta para página inicial de "edição de dados" e não salva nada.
* **Salvar**: envia PATCH para API `/property/manager/<property_id>`, salvando os dados na base.