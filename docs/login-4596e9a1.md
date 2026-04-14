<!-- title: Login | url: https://outline.seazone.com.br/doc/login-Uzls0O90vv | area: Tecnologia -->

# Login

* **Users/me**

  Cria um novo campo no endpoint `/users/me` no momento apenas quando o usuário logado é um Owner. Conforme descrito no card a API verifica uma serie de informação para definir se uma ação requirida de completar o cadastro deve ser retornada. O novo campo é chamado de `actions_required`.

  **Estrutura definida para actions_required**

  Será sempre retornado um array com constantes informando cada ação necessário para o User. Se nenhuma ação foi encontrado retorna apenas um array vazio. A única ação definida no momento é `COMPLETE_PERSONAL_DATA`.Ex:

  `{     "actions_required": []   }   {     "actions_required": ["COMPLETE_PERSONAL_DATA"]   }`