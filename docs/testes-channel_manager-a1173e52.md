<!-- title: Testes Channel_Manager | url: https://outline.seazone.com.br/doc/testes-channel_manager-hXNtgw7nyX | area: Tecnologia -->

# Testes Channel_Manager

## Testes Unitários

Os testes unitários são uma parte fundamental da prática de desenvolvimento de software e são projetados para testar unidades individuais de código-fonte. Uma unidade pode ser uma função, um método, uma classe ou até mesmo um módulo, dependendo do contexto. O objetivo dos testes unitários é garantir que cada unidade do software funcione conforme o esperado. Para isso utilizamos o Jest.

### **django Docs**

[Django](https://docs.djangoproject.com/en/5.0/topics/testing/overview/)

## Testes já implementados no channel_manager

### **API**

* **API - test_pipefy.py**

  
  1. **Teste** `test_import_pipefy_data_user_allowed`:
     * **Descrição do Teste**: Verifica se um administrador pode acessar e iniciar a importação de dados do Pipefy.
     * **Riscos Mitigados**: Reduz o risco de acesso não autorizado às funcionalidades de importação do Pipefy.
  2. **Teste** `test_import_pipefy_data_user_forbbiden`:
     * **Descrição do Teste**: Verifica se um usuário sem permissões de administrador não pode acessar o endpoint de importação do Pipefy.
     * **Riscos Mitigados**: Evita que usuários não autorizados acessem e executem a importação de dados do Pipefy.

     \*\*Sugestões teste unitários:

     Testar diferentes casos de entrada →\*\* situações como dados de entrada inválidos, datas futuras, datas passadas, etc. Isso ajudará a garantir que o endpoint lide adequadamente com diferentes cenários.

     **Testar permissões para diferentes tipos de usuários →** É importante testar o comportamento do endpoint para usuários com diferentes papéis e permissões, como usuários normais ou sem permissões.

     **Testar respostas de erro →** você pode adicionar casos de teste para verificar como o endpoint responde a solicitações inválidas ou com erros. Isso inclui testar respostas para solicitações sem autenticação, solicitações com dados inválidos, etc.

     **Testar o conteúdo da resposta → T**estes para verificar outros aspectos da resposta, como o formato dos dados retornados, a presença de determinadas chaves, etc.
* **API - test_stays.py**

  **Teste** `test_import_stays_reservations_api`
  * **Descrição do Teste**: Verifica se um administrador pode acessar e iniciar a importação de reservas de estadias. Além disso, verifica se a resposta da API possui um código de status HTTP 200 e se o identificador da tarefa retornado está correto.
  * **Riscos Mitigados**: Reduz o risco de acesso não autorizado às funcionalidades de importação de reservas de estadias.

  \*\*Sugestões teste unitários:

  Testar diferentes casos de entrada →\*\* situações como dados de entrada inválidos, datas futuras, datas passadas, etc. Isso ajudará a garantir que o endpoint lide adequadamente com diferentes cenários.

  **Testar permissões para diferentes tipos de usuários →** É importante testar o comportamento do endpoint para usuários com diferentes papéis e permissões, como usuários normais ou sem permissões.

  **Testar respostas de erro →** você pode adicionar casos de teste para verificar como o endpoint responde a solicitações inválidas ou com erros. Isso inclui testar respostas para solicitações sem autenticação, solicitações com dados inválidos, etc.

  **Testar o conteúdo da resposta → T**estes para verificar outros aspectos da resposta, como o formato dos dados retornados, a presença de determinadas chaves, etc.

### **Integration**

* **Pipedrive - test_pipedrive_api.py**

  
  1. **Teste** `test_get_pipedrive_deal_by_id`:
     * **Descrição do Teste**: Testa a obtenção de um dado do Pipedrive por ID. Verifica se a função retorna os dados corretos quando o dado é encontrado e se retorna `None` quando o dado não é encontrado.
     * **Asserts**:
       * `self.assertEqual(response['data'], api_response['data'])`: Verifica se os dados retornados pela função correspondem aos dados esperados.
       * `self.assertIsNone(response)`: Verifica se a função retorna `None` quando o dado não é encontrado.
     * **Riscos Mitigados**: Garante que a função se comporte corretamente ao buscar negócios no Pipedrive, reduzindo o risco de retornar dados incorretos ou nulos.
  2. **Teste** `test_get_pipedrive_deal_by_id_success`:
     * **Descrição do Teste**: Testa o sucesso ao obter um negócio do Pipedrive por ID. Verifica se a função retorna os dados esperados e se a chamada para `requests.Session.get` é feita com os parâmetros corretos.
     * **Asserts**:
       * `self.assertEqual(response, {'data': {'id': 1, 'title': 'Test Deal'}})`: Verifica se os dados retornados pela função correspondem aos dados esperados.
       * `mock_get.assert_called_once_with(url=f"{self.base_url}deals/{deal_id}", params={"api_token": self.auth_token})`: Verifica se a função `requests.Session.get` é chamada com os parâmetros corretos.
     * **Riscos Mitigados**: Garante que a função se comporte corretamente ao obter dados do Pipedrive e que faça chamadas à API com os parâmetros corretos, reduzindo o risco de erros de comunicação ou de retorno de dados incorretos.
  3. **Teste** `test_get_pipedrive_deal_by_id_not_found`:
     * **Descrição do Teste**: Testa o cenário em que um dado não é encontrado no Pipedrive. Verifica se a função retorna `None` e se a chamada para `requests.Session.get` é feita com os parâmetros corretos.
     * **Asserts**:
       * `self.assertIsNone(response)`: Verifica se a função retorna `None` quando o negócio não é encontrado.
       * `mock_get.assert_called_once_with(url=f"{self.base_url}deals/{deal_id}", params={"api_token": self.auth_token})`: Verifica se a função `requests.Session.get` é chamada com os parâmetros corretos.
     * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com casos em que um negócio não é encontrado no Pipedrive, reduzindo o risco de erros de manipulação de dados ou de comunicação.
  4. **Teste** `test_get_pipedrive_all_deals:`
     * **Descrição do Teste**: Testa a recuperação de todos os negócios com paginação da API do Pipedrive. Configura mocks para simular o retorno de múltiplas respostas da API com mais de uma página de resultados. Verifica se a função retorna todos os negócios esperados e se a função `requests.Session.get` é chamada duas vezes, uma vez para cada página.
     * **Asserts**:
       * Verifica se a função retorna os negócios esperados, incluindo aqueles presentes em várias páginas de resultados: `self.assertEqual(response, [{"id": 1, "title": "Deal 1", "pipeline_id": "1"}, {"id": 2, "title": "Deal 2", "pipeline_id": "2"}, {"id": 3, "title": "Deal 3", "pipeline_id": "1"}])`.
       * Verifica se a função `requests.Session.get` é chamada duas vezes, uma vez para cada página de resultados: `self.assertEqual(mock_get.call_count, 2)`.
     * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com a paginação de resultados da API do Pipedrive, garantindo que todos os negócios sejam recuperados corretamente, mesmo quando distribuídos em várias páginas de resultados. Isso reduz o risco de perder dados importantes devido a uma implementação incorreta da lógica de paginação.
  5. **Teste** `test_get_pipedrive_all_deals_non_200_status`:
     * **Descrição do Teste**: Testa o tratamento de códigos de status não 200 da API do Pipedrive. Configura um mock para simular uma resposta com um código de status não 200. Verifica se a função retorna uma lista vazia quando recebe um código de status não 200 da API.
     * **Asserts**:
       * Verifica se a função retorna uma lista vazia quando recebe um código de status não 200: `self.assertEqual(response, [])`.
     * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com respostas da API do Pipedrive que não possuem um código de status 200, reduzindo o risco de falhas ou comportamentos inesperados quando a API retorna erros. Isso também assegura que o sistema seja resiliente a falhas na comunicação com a API do Pipedrive.

     
     1. **Teste** `test_get_pipedrive_all_deals_missing_data`:
        * **Descrição do Teste**: Testa o tratamento de respostas da API do Pipedrive que estão faltando a chave 'data'. Configura um mock para simular uma resposta da API que não possui a chave 'data'. Verifica se a função retorna uma lista vazia quando a resposta da API está faltando a chave 'data'.
        * **Asserts**:
          * Verifica se a função retorna uma lista vazia quando a resposta da API está faltando a chave 'data': `self.assertEqual(response, [])`.
        * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com respostas da API do Pipedrive que estão faltando a chave 'data', reduzindo o risco de falhas ou comportamentos inesperados quando a estrutura da resposta da API está incorreta. Isso ajuda a garantir a estabilidade e a confiabilidade do sistema, mesmo quando a API retorna dados inesperados ou mal formatados.

        
         1. **Teste** `test_get_pipedrive_all_deals_network_error`:
            * **Descrição do Teste**: Testa o tratamento de erros de rede durante a solicitação à API do Pipedrive. Configura um mock para simular uma exceção `RequestException` ao fazer a chamada à API. Verifica se a função retorna uma lista vazia quando ocorre um erro de rede e se um erro é registrado nos logs do sistema.
            * **Asserts**:
              * Verifica se a função retorna uma lista vazia quando ocorre um erro de rede: `self.assertEqual(response, [])`.
              * Verifica se um erro é registrado nos logs do sistema: `self.assertIn('Error', cm.output[0])`.
            * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com erros de rede durante a comunicação com a API do Pipedrive, garantindo que o sistema seja resiliente a falhas de rede. Além disso, registra um erro nos logs do sistema para fins de monitoramento e depuração, permitindo que os desenvolvedores identifiquem e resolvam problemas de forma eficaz.
         2. **Teste** `test_get_pipedrive_person_by_id:`
            * **Descrição do Teste**: Testa a obtenção de uma pessoa do Pipedrive por ID. Configura um mock para simular uma resposta bem-sucedida da API contendo os detalhes da pessoa. Verifica se a função retorna os dados corretos quando uma pessoa é encontrada e se a chamada à API é feita com os parâmetros corretos. Além disso, simula uma resposta 404 da API para testar o cenário em que a pessoa não é encontrada e verifica se a função retorna `None` nesse caso.
            * **Asserts**:
              * Verifica se a função retorna os dados corretos quando uma pessoa é encontrada: `self.assertEqual(response, api_response)`.
              * Verifica se a chamada à API é feita com os parâmetros corretos: `mock_get.assert_called_once_with(url=f"{self.base_url}persons/{person_id}/", params={"api_token": self.auth_token})`.
              * Verifica se a função retorna `None` quando a pessoa não é encontrada: `self.assertIsNone(response)`.
            * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com a obtenção de detalhes de uma pessoa do Pipedrive por ID, reduzindo o risco de retornar dados incorretos ou inesperados. Além disso, verifica se a chamada à API é feita corretamente com os parâmetros adequados, garantindo uma integração eficaz com a API do Pipedrive.
         3. **Teste** `test_create_pipedrive_person_success`:
            * **Descrição do Teste**: Testa a criação bem-sucedida de uma pessoa no Pipedrive. Configura um mock para simular uma resposta bem-sucedida da API após a criação da pessoa, incluindo os detalhes da pessoa recém-criada. Verifica se a função retorna os dados corretos da pessoa recém-criada e se a chamada à API é feita com os parâmetros corretos para criar a pessoa.
            * **Asserts**:
              * Verifica se a função retorna os dados corretos da pessoa recém-criada: `self.assertEqual(response['data'], api_response['data'])`.
              * Verifica se a chamada à API é feita com os parâmetros corretos para criar a pessoa: `mock_post.assert_called_once_with(url=f"{self.base_url}persons", params={"api_token": self.auth_token}, json=payload)`.
            * **Riscos Mitigados**: Garante que a função de criação de pessoa no Pipedrive se comporte corretamente ao lidar com a criação de uma nova pessoa, reduzindo o risco de criar pessoas com dados incorretos ou inesperados. Além disso, verifica se a chamada à API é feita corretamente com os parâmetros adequados para criar a pessoa no Pipedrive.
         4. **Teste** `test_create_pipedrive_person_failure`:
            * **Descrição do Teste**: Testa o tratamento de falhas ao criar uma pessoa no Pipedrive. Configura um mock para simular uma resposta de falha da API ao tentar criar a pessoa. Verifica se a exceção `RequestException` é levantada quando ocorre uma falha na chamada da API.
            * **Asserts**:
              * Verifica se a exceção `RequestException` é levantada: `with self.assertRaises(requests.exceptions.RequestException)`.
            * **Riscos Mitigados**: Garante que a função de criação de pessoa no Pipedrive se comporte corretamente ao lidar com falhas na criação de uma nova pessoa, evitando comportamentos inesperados ou erros não tratados ao interagir com a API do Pipedrive.
         5. **Teste** `test_create_pipedrive_deal`:
            * **Descrição do Teste**: Testa a criação de um novo dado no Pipedrive. Configura um mock para simular uma resposta de sucesso da API ao criar um novo dado. Verifica se a função retorna os dados corretos do novo dado criado e se a chamada para a API foi feita com os parâmetros corretos. Além disso, simula uma resposta de erro da API para testar o tratamento de erros quando parâmetros incorretos são fornecidos para a criação de um dado.
            * **Asserts**:
              * Verifica se a função retorna os dados corretos do novo dado criado: `self.assertEqual(response, api_response)`.
              * Verifica se a chamada para a API foi feita com os parâmetros corretos: `mock_post.assert_called_once_with(url=f"{self.base_url}deals", params={"api_token": self.auth_token}, json=deal_params)`.
              * Verifica se uma exceção é levantada quando a API retorna um código de status 400 (erro de solicitação): `with self.assertRaises(Exception)`.
            * **Riscos Mitigados**: Garante que a função de criação de dados no Pipedrive se comporte corretamente ao lidar com respostas de sucesso e erros da API, evitando comportamentos inesperados ou erros não tratados ao interagir com a API do Pipedrive.
         6. **Teste** `test_find_pipedrive_person_by_email_success`:
            * **Descrição do Teste**: Testa a busca de uma pessoa no Pipedrive pelo e-mail com sucesso. Configura um mock para simular uma resposta de sucesso da API ao buscar uma pessoa pelo e-mail fornecido. Verifica se a função retorna os dados corretos da pessoa encontrada e se a chamada para a API foi feita com os parâmetros corretos.
            * **Asserts**:
              * Verifica se a função retorna os dados corretos da pessoa encontrada: `self.assertEqual(result, {"id": 123, "name": "Test Person", "email": "test@example.com"})`.
              * Verifica se a chamada para a API foi feita com os parâmetros corretos: `mock_get.assert_called_once_with(url="http://api.pipedrive.com/persons/search", params={"api_token": "test_auth_token", 'fields': 'email', 'term': "test@example.com"})`.
            * **Riscos Mitigados**: Garante que a função de busca de pessoa por e-mail no Pipedrive se comporte corretamente ao lidar com uma resposta de sucesso da API, evitando comportamentos inesperados ou erros não tratados ao realizar a busca por e-mail.
         7. **Teste** `test_find_pipedrive_person_by_phone_success`:
            * **Descrição do Teste**: Este teste avalia o sucesso da função de buscar uma pessoa no Pipedrive pelo número de telefone. Ele configura um mock para simular uma resposta bem-sucedida da API ao procurar uma pessoa pelo número de telefone fornecido. Verifica se a função retorna os dados corretos da pessoa encontrada e se a chamada para a API foi feita com os parâmetros corretos.
            * **Asserts**:
              * Verifica se a função retorna os dados corretos da pessoa encontrada: `self.assertEqual(result, {"id": 123, "name": "Test Person", "phone": "123456789"})`.
              * Verifica se a chamada para a API foi feita com os parâmetros corretos: `mock_get.assert_called_once_with(url="http://api.pipedrive.com/persons/search", params={"api_token": "test_auth_token", 'fields': 'phone', 'term': "123456789"})`.
            * **Riscos Mitigados**: Garante que a função de busca de pessoa por número de telefone no Pipedrive se comporte corretamente ao lidar com uma resposta de sucesso da API, evitando comportamentos inesperados ou erros não tratados ao realizar a busca por número de telefone.
         8. **Teste** `test_get_pipedrive_deal_fields_success`:
            * **Descrição do Teste**: Este teste verifica o sucesso da função para obter os campos de negócio (deal) no Pipedrive. Ele configura um mock para simular uma resposta bem-sucedida da API ao solicitar os campos de negócio, verificando se a função retorna os dados corretos dos campos de negócio e se a chamada para a API foi feita com os parâmetros corretos.
            * **Asserts**:
              * Verifica se a função retorna os dados corretos dos campos de negócio: `self.assertEqual(result, [{"id": 1, "name": "Deal Name", "field_type": "text"}, {"id": 2, "name": "Deal Value", "field_type": "currency"}])`.
              * Verifica se a chamada para a API foi feita com os parâmetros corretos: `mock_get.assert_called_once_with(url="http://api.pipedrive.com/dealFields", params={"api_token": "test_auth_token"})`.
            * **Riscos Mitigados**: Garante que a função de obtenção de campos de negócio no Pipedrive se comporte corretamente ao lidar com uma resposta de sucesso da API, evitando comportamentos inesperados ou erros não tratados ao solicitar os campos de negócio.
         9. **Teste** `test_get_pipedrive_deal_fields_non_200_status`:
            * **Descrição do Teste**: Este teste verifica o comportamento da função `get_pipedrive_deal_fields` ao lidar com um código de status não-200 da API do Pipedrive. Ele simula uma resposta de erro da API configurando um mock para retornar um código de status 400 e lançar uma exceção de solicitação. Em seguida, verifica se a função retorna uma lista vazia e registra um erro de log.
            * **Asserts**:
              * Verifica se a função retorna uma lista vazia em caso de erro de rede: `self.assertEqual(response, [])`.
              * Verifica se um erro é registrado no log: `self.assertIn('Error', cm.output[0])`.
            * **Riscos Mitigados**: Garante que a função se comporte corretamente ao lidar com um código de status não-200 da API do Pipedrive, evitando comportamentos inesperados ou falhas não tratadas e garantindo que os erros sejam devidamente registrados para diagnóstico posterior.
        10. **Teste** `test_get_pipedrive_person_by_id_success`:
            * **Descrição do Teste**: Este teste verifica o comportamento da função `get_pipedrive_person_by_id` ao receber uma resposta bem-sucedida da API do Pipedrive. Ele simula uma resposta de sucesso configurando um mock para retornar um código de status 200 e um JSON contendo os detalhes da pessoa solicitada. O teste verifica se a função faz a chamada correta para a API, incluindo o URL esperado e os parâmetros corretos, e se retorna os dados esperados.
            * **Asserts**:
              * Verifica se a função faz a chamada correta para a API: `mock_get.assert_called_once_with(url=expected_url, params={"api_token": self.auth_token})`.
              * Verifica se os dados retornados pela função correspondem aos dados esperados: `self.assertEqual(result, {"data": {"id": person_id, "name": "Test Person"}})`.
            * **Riscos Mitigados**: Garante que a função `get_pipedrive_person_by_id` se comporte corretamente ao receber uma resposta bem-sucedida da API do Pipedrive, retornando os dados esperados e fazendo a chamada correta para a API, evitando assim comportamentos inesperados e garantindo a integridade dos dados retornados.
        11. **Teste** `test_attach_files_to_deal_success`:
            * **Descrição do Teste**: Este teste verifica o comportamento da função `attach_files_to_deal` ao anexar arquivos a um negócio (deal) no Pipedrive. Ele simula uma resposta de sucesso configurando um mock para retornar um código de status 200 e um JSON indicando o sucesso da operação, juntamente com os detalhes do arquivo anexado. O teste verifica se a função faz a chamada correta para a API, incluindo o URL esperado, os cabeçalhos corretos, os parâmetros corretos e os arquivos a serem anexados, e se retorna os dados esperados.
            * **Asserts**:
              * Verifica se a função faz a chamada correta para a API: `mock_post.assert_called_once_with(...)`.
              * Verifica se os dados retornados pela função correspondem aos dados esperados: `self.assertEqual(result, {"success": True, "data": {"id": 12345}})`.
            * **Riscos Mitigados**: Garante que a função `attach_files_to_deal` se comporte corretamente ao anexar arquivos a um negócio no Pipedrive, fazendo a chamada correta para a API com os parâmetros e arquivos corretos e retornando os dados esperados em caso de sucesso, evitando assim erros na anexação de arquivos e garantindo a integridade dos dados retornados.

        **Sugestão**:

        
        1. **Testes de Limites e Valores Extremos**:
           * Teste a função `get_pipedrive_all_deals` com diferentes tamanhos de página e verifique se a paginação está funcionando corretamente.
           * Teste a função `create_pipedrive_person` com diferentes combinações de campos obrigatórios e opcionais, garantindo que os dados sejam válidos e corretamente tratados pela API.
           * Teste a função `create_pipedrive_deal` com diferentes valores de moeda, incluindo casos em que a moeda não é suportada pela API.
        2. **Testes de Erro e Exceções**:
           * Teste o tratamento de erros da função `get_pipedrive_all_deals` quando a API retorna um status de erro diferente de 200.
           * Teste o tratamento de erros da função `create_pipedrive_person` quando a API retorna um status de erro, garantindo que a exceção seja tratada corretamente.
           * Teste o tratamento de erros da função `create_pipedrive_deal` quando a API retorna um status de erro, incluindo casos de validação de dados inválidos.
* **Pipefy - test_pipefy_api.py**

  ### **Teste** `test_make_request_session`

  ### Descrição do Teste:

  Este teste verifica se a função `make_request_session` é chamada corretamente.

  ### Asserts:
  * Não há asserts explícitos neste teste, pois a função `make_request_session` não retorna nada. O objetivo deste teste é garantir que a função seja chamada sem erros.

  ### Riscos Mitigados:
  * Garante que a função `make_request_session` seja chamada corretamente, evitando possíveis erros devido a chamadas incorretas ou ausentes desta função.

  ### **Teste** `test_get_pipefy_data`

  ### Descrição do Teste:

  Este teste verifica se o método `get_pipefy_data` da classe `PipefyApi` faz uma solicitação GraphQL para a API do Pipefy com os parâmetros corretos.

  ### Asserts:
  * `mock_request_session.post.assert_called_once_with(...)`: Verifica se o método `post` do objeto de sessão de solicitação foi chamado exatamente uma vez com os parâmetros esperados.

  ### Riscos Mitigados:
  * Garante que o método `get_pipefy_data` faça a solicitação GraphQL corretamente, evitando possíveis erros devido a parâmetros incorretos ou ausentes na solicitação. Isso ajuda a mitigar o risco de integração com a API do Pipefy.

  **Sugestões:**

  
  1. **Teste de Caso Vazio**:
     * Descrição: Teste se a função `get_pipefy_data` funciona corretamente quando é chamada com uma string vazia como argumento.
     * Asserts: Verifique se a função não lança exceções e se não há chamadas feitas ao `mock_request_session.post`.
  2. **Teste de Chamada sem Parâmetros**:
     * Descrição: Verifique se a função `get_pipefy_data` funciona corretamente quando chamada sem argumentos.
     * Asserts: Verifique se a função não lança exceções e se não há chamadas feitas ao `mock_request_session.post`.
  3. **Teste de Chamada com Parâmetros Inválidos**:
     * Descrição: Teste se a função `get_pipefy_data` lida corretamente com parâmetros inválidos, como um tipo de dado não suportado.
     * Asserts: Verifique se a função lança uma exceção apropriada ao receber parâmetros inválidos.
  4. **Teste de Chamada com Token Inválido**:
     * Descrição: Verifique se a função `get_pipefy_data` lida corretamente com um token de autenticação inválido.
     * Asserts: Verifique se a função lança uma exceção ao tentar fazer a chamada à API.
  5. **Teste de Chamada com Exceção na Requisição**:
     * Descrição: Verifique se a função `get_pipefy_data` lida corretamente com uma exceção ao fazer a requisição.
     * Asserts: Verifique se a função lança uma exceção apropriada ao ocorrer uma falha na requisição.
* **Stays - test_stays_api.py**

  **Teste** `test_make_request_session`

  **Descrição do Teste:** Este teste verifica se a função `make_request_session` é chamada corretamente.

  **Asserts:**
  * Verifica se a função `make_request_session` é chamada.

  **Riscos Mitigados:** Garante que a função `make_request_session` é chamada sem lançar exceções, assegurando que o objeto de sessão de requisição seja criado corretamente.

  
---

  **Teste** `test_get_stays_reservations_by_date_range`

  **Descrição do Teste:** Este teste verifica se a função `get_stays_reservations_by_date_range` faz uma chamada correta para a API do Stays ao buscar reservas dentro de um determinado intervalo de datas.

  **Asserts:**
  * Verifica se a função faz a chamada correta para a API, incluindo o URL esperado, os cabeçalhos e os parâmetros JSON.
  * Verifica se a função é chamada com os parâmetros corretos: `date_from`, `date_to` e `date_type`.

  **Riscos Mitigados:** Garante que a função `get_stays_reservations_by_date_range` se comporte corretamente ao buscar reservas dentro do intervalo de datas especificado, evitando comportamentos inesperados e garantindo a integridade dos dados retornados pela API.

  
---

  **Teste** `test_get_stays_reservations_by_id`

  **Descrição do Teste:** Este teste verifica se a função `get_stays_reservation_by_id` faz uma chamada correta para a API do Stays ao buscar uma reserva por ID.

  **Asserts:**
  * Verifica se a função faz a chamada correta para a API, incluindo o URL esperado e os cabeçalhos.
  * Verifica se a função é chamada com o ID da reserva correto.

  **Riscos Mitigados:** Garante que a função `get_stays_reservation_by_id` se comporte corretamente ao buscar uma reserva específica por ID, evitando comportamentos inesperados e garantindo a integridade dos dados retornados pela API.

  **Sugestão:**

  
  1. **Teste de Busca de Reservas por Status:**
     * Descrição do Teste: Verifique se a função `get_stays_reservations_by_status` retorna corretamente as reservas com base em um status específico.
  2. **Teste de Manipulação de Erros:**
     * Descrição do Teste: Verifique se a função `StaysApi` lida corretamente com erros de comunicação ou respostas inesperadas da API.
     * Reserva que não existe
     * Passando parâmetros não aceitos
     * validar a resposta do GET
     * Validar o corpo da resposta do GET

**Action**

* **Stays - test_stays_calculator.py**

  
  1. **Teste:** `test_stays_calc_stays_simple`

  **Descrição do Teste:** Este teste verifica se os cálculos relacionados à reserva de estadias estão corretos no módulo "channel_manager". Ele simula uma reserva de estadias e verifica se os valores calculados pela função `calculate_ota_values()` correspondem aos valores esperados.

  **Risco Mitigado:** O teste ajuda a mitigar o risco de erros nos cálculos relacionados às reservas de estadias no sistema, garantindo a precisão financeira das transações. Além disso, ao ser automatizado, pode ser executado repetidamente durante o desenvolvimento e a manutenção do sistema para detectar alterações que possam introduzir erros nos cálculos de reserva de estadias.

  
  1. **Teste**: `test_stays_calc_stays_with_cf`

  **Descrição do Teste:** Este teste verifica se os cálculos relacionados à reserva de estadias, incluindo a taxa de limpeza, estão corretos no módulo "channel_manager". Ele simula uma reserva de estadias com uma taxa de limpeza e verifica se os valores calculados pela função `calculate_ota_values()` correspondem aos valores esperados.

  **Risco Mitigado:** Esse teste ajuda a mitigar o risco de erros nos cálculos relacionados às reservas de estadias, especialmente no que diz respeito à inclusão da taxa de limpeza. Garante que a taxa de limpeza seja corretamente considerada nos cálculos, o que é fundamental para a precisão financeira das transações relacionadas às reservas de estadias.

  
  1. `Teste test_stays_calc_stays_with_cf_and_md`

  **Descrição do Teste:** Este teste verifica se os cálculos relacionados à reserva de estadias, incluindo a `manual_discount`, estão corretos no módulo "channel_manager". Ele simula uma reserva de estadias com uma taxa de limpeza e verifica se os valores calculados pela função `calculate_ota_values()` correspondem aos valores esperados.

  **Risco Mitigado:** Esse teste ajuda a mitigar o risco de erros nos cálculos relacionados às reservas de estadias, especialmente no que diz respeito à inclusão da taxa de limpeza. Garante que a taxa de limpeza seja corretamente considerada nos cálculos, o que é fundamental para a precisão financeira das transações relacionadas às reservas de estadias.

  
  1. **Teste:** `test_stays_calc_stays_with_cf_and_cd`

  **Descrição Resumida do Teste:** O teste verifica o cálculo dos valores relacionados a uma reserva de estadias com um cupom de desconto, comparando os resultados esperados com os valores calculados.

  **Risco Mitigado:** O teste ajuda a mitigar erros nos cálculos de valores de reserva, garantindo precisão financeira e satisfação do cliente. Ao isolar o código de dependências externas, o teste é mais confiável e previsível.

  
  1. **Teste:** `test_stays_calc_stays_with_cf_and_ef`

  **Descrição Resumida do Teste:** Este teste avalia o cálculo dos valores relacionados a uma reserva de estadias com uma taxa extra (`extra_fee`), sem desconto de cupom. Ele compara os resultados esperados com os valores calculados para garantir precisão.

  **Risco Mitigado:** Este teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando há taxas extras envolvidas. Isso assegura a precisão financeira e reduz o risco de cobranças incorretas. Além disso, ao utilizar a simulação (`mock`) do desconto do cupom, o teste isola o código de dependências externas, melhorando a confiabilidade e previsibilidade do teste.

  
  1. **Teste:** `test_stays_calc_stays_no_cf_with_md_and_cd_and_ef`

  **Descrição Resumida do Teste:** Este teste avalia o cálculo dos valores relacionados a uma reserva de estadias sem taxa de limpeza (`cleaning_fee_value`), mas com desconto manual (`manual_discount`), desconto de cupom (`cupom_discount`) e taxa extra (`extra_fee`). Ele verifica se os valores calculados correspondem aos valores esperados.

  **Risco Mitigado:** Este teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando há descontos e taxas extras envolvidos. Garantindo que os cálculos estejam corretos, reduz-se o risco de cobranças incorretas aos clientes, garantindo a integridade financeira e a satisfação do cliente. Ao simular o desconto do cupom, o teste isola o código de dependências externas, tornando-o mais confiável e previsível.

  
  1. **Teste:** `test_stays_calc_stays_no_cf_with_cd`

  **Descrição Resumida do Teste:** Este teste avalia o cálculo dos valores relacionados a uma reserva de estadias sem taxa de limpeza (`cleaning_fee_value`), mas com desconto de cupom (`cupom_discount`). Ele verifica se os valores calculados correspondem aos valores esperados.

  **Risco Mitigado:** O teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando há descontos envolvidos. Isso reduz o risco de cobranças incorretas aos clientes, garantindo a integridade financeira e a satisfação do cliente. Ao simular o desconto do cupom, o teste isola o código de dependências externas, tornando-o mais confiável e previsível.

  
  1. **Teste:** `test_stays_calc_stays_no_cf_with_md_and_cd`

  **Descrição Resumida do Teste:** Este teste verifica o cálculo dos valores relacionados a uma reserva de estadias sem taxa de limpeza (`cleaning_fee_value`), com desconto manual (`manual_discount`) e desconto de cupom (`cupom_discount`). Ele compara os resultados esperados com os valores calculados.

  **Risco Mitigado:** O teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando há descontos envolvidos. Isso garante a precisão financeira e reduz o risco de cobranças incorretas aos clientes. Ao simular o desconto do cupom, o teste isola o código de dependências externas, tornando-o mais confiável e previsível. Além disso, testar o desconto manual garante que ele seja aplicado corretamente, garantindo a precisão dos cálculos.

  
  1. **Teste:** `test_stays_garbage_01_cleaning_fee`

  **Descrição Resumida do Teste:** Este teste avalia o cálculo dos valores relacionados a uma reserva de estadias com taxa de limpeza (`cleaning_fee_value`) zero. Ele verifica se os valores calculados correspondem aos valores esperados.

  **Risco Mitigado:** O teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando há taxas de limpeza envolvidas. Garantir que a taxa de limpeza zero seja tratada corretamente é crucial para evitar cobranças incorretas aos clientes. Isso contribui para a integridade financeira e a satisfação do cliente.

  
  1. **Teste:** `test_stays_round_gross_daily_value_error`

  **Descrição Resumida do Teste:** Este teste verifica o cálculo dos valores relacionados a uma reserva de estadias onde ocorre um erro de arredondamento no valor bruto diário (`gross_daily_value`). Ele compara os resultados esperados com os valores calculados.

  **Risco Mitigado:** O teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando há valores arredondados envolvidos. Isso garante a precisão financeira e reduz o risco de cobranças incorretas aos clientes. Ao simular o desconto do cupom, o teste isola o código de dependências externas, tornando-o mais confiável e previsível.

  11\.**Teste:** `test_stays_cleaning_fee_calc_error`

  **Descrição Resumida do Teste:** Este teste avalia o cálculo dos valores relacionados a uma reserva de estadias onde ocorre um erro no cálculo da taxa de limpeza (`cleaning_fee_value`). Ele compara os resultados esperados com os valores calculados.

  **Risco Mitigado:** O teste ajuda a mitigar erros nos cálculos de valores de reserva, especialmente quando envolve o cálculo de taxas, como a taxa de limpeza. Isso garante a precisão financeira e reduz o risco de cobranças incorretas aos clientes.

  Sugestão:

  
  1. **Teste de Cálculo de Taxas Extras:**
     * Verifique o cálculo correto de taxas extras quando diferentes valores são fornecidos, como uma taxa fixa ou uma taxa variável.
  2. **Teste de Descontos Cumulativos:**
     * Avalie o comportamento do sistema ao aplicar descontos cumulativos, como desconto de cupom e desconto manual.
  3. **Teste de Exceção de Dados Ausentes:**
     * Teste como o sistema lida com a ausência de dados obrigatórios para o cálculo, como a falta de informações sobre a reserva.
  4. **Teste de Valores Extremos:**
     * Teste o comportamento do sistema com valores extremos, como reservas com preços muito altos ou muito baixos.
  5. **Teste de Dados Inválidos:**
     * Verifique se o sistema trata corretamente dados inválidos ou inesperados, como valores negativos para preços ou descontos.
* **Stays - test_expedia_calculator.py**

  **Descrição do Teste:** `test_calc_expedia_extra_fee, test_calc_expedia_garbage_cleaning_fee`

  Este teste visa verificar o cálculo correto dos valores associados a reservas feitas através do serviço Expedia. Ele aborda duas situações específicas: uma reserva com uma taxa extra e outra com uma taxa de limpeza inválida.

  **Risco Mitigado:**

  
  1. **Cálculo de Taxa Extra Preciso:**
     * O teste garante que a taxa extra seja calculada corretamente para reservas Expedia. Isso ajuda a mitigar o risco de erros nos valores adicionais cobrados dos clientes.
  2. **Lidando com Dados de Limpeza Inválidos:**
     * Ao simular uma reserva com uma taxa de limpeza inválida, o teste verifica se o sistema lida adequadamente com esses dados e se os valores calculados são coerentes. Isso ajuda a evitar possíveis problemas quando os dados da reserva não estão corretos.
  3. **Garantia de Precisão nos Valores Totais:**
     * Ao comparar os valores totais calculados com os valores esperados, o teste garante que o sistema esteja produzindo resultados precisos para os clientes Expedia. Isso é crucial para manter a confiança dos clientes e evitar disputas sobre cobranças incorretas.
  4. **Verificação de Descontos e Taxas:**
     * O teste também verifica se os descontos e taxas são aplicados corretamente às reservas Expedia. Isso é importante para garantir que os clientes recebam os benefícios corretos de suas promoções ou cupons.

  Em resumo, este teste ajuda a garantir a integridade e a precisão dos cálculos associados às reservas feitas através do serviço Expedia, contribuindo para uma experiência consistente e confiável para os clientes.

  **Sugestão:**

  
   1. **Teste de Cálculo de Comissão Ota:**
      * Verifique se a comissão da OTA é calculada corretamente com base no total da reserva e se está dentro dos limites esperados.
   2. **Teste de Desconto de Cupom:**
      * Avalie o cálculo do desconto de cupom para diferentes tipos de desconto (percentual, valor fixo) e verifique se é aplicado corretamente ao total da reserva.
   3. **Teste de Taxa Ota:**
      * Verifique se a taxa da OTA é calculada corretamente com base no total da reserva e se está dentro dos limites esperados.
   4. **Teste de Limpeza Bruta:**
      * Avalie se o cálculo da limpeza bruta é feito corretamente subtraindo a soma das diárias e a taxa extra do total da reserva.
   5. **Teste de Limpeza Líquida:**
      * Verifique se a limpeza líquida é calculada corretamente subtraindo a taxa da OTA da limpeza bruta.
   6. **Teste de Diária Bruta e Líquida:**
      * Avalie o cálculo das diárias bruta e líquida, garantindo que a taxa extra seja incluída na diária bruta e que a taxa da OTA seja subtraída da diária líquida.
   7. **Teste de Valor Total da Reserva:**
      * Verifique se o valor total da reserva é calculado corretamente somando as diárias, a taxa extra e a limpeza líquida.
   8. **Teste de Valor Pago e Valor Descontado:**
      * Avalie se o valor pago e o valor descontado estão corretamente representados nos resultados finais, considerando descontos de cupom e descontos manuais.
   9. **Teste de Cobrança de Taxa Extra:**
      * Verifique se a taxa extra é corretamente adicionada ao total da reserva e se é exibida corretamente nos resultados finais.
  10. **Teste de Reservas com Diferentes Tipos de Descontos:**
      * Teste o comportamento do sistema ao lidar com reservas que têm descontos diferentes aplicados, como descontos de cupom, descontos automáticos ou descontos por associação a programas de fidelidade.
* **Stays - test_booking_calculator.py**

  
  1. **Teste:** `test_calc_booking_no_cleaning_fee`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando não há taxa de limpeza incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na ausência de uma taxa de limpeza, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  
  1. **Teste:** `test_calc_booking_with_cleaning_fee`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando uma taxa de limpeza está incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na presença de uma taxa de limpeza, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  
  1. **Teste:** `test_calc_booking_extra_fee_no_cleaning_fee`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando há uma taxa extra incluída, mas não há taxa de limpeza. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na presença de uma taxa extra, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  
  1. **Teste:** `test_calc_booking_extra_fee_with_cleaning_fee_booking`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando há uma taxa extra e uma taxa de limpeza incluídas. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na presença de uma taxa extra e uma taxa de limpeza, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  
  1. `Teste: test_stays_garbage_01_cleaning_fee`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando não há taxa de limpeza e uma taxa extra está incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na ausência de uma taxa de limpeza e com a inclusão de uma taxa extra, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  
  1. **Teste:** `test_stays_garbage_02_cleaning_fee`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando não há taxa de limpeza e nenhuma taxa extra está incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na ausência de uma taxa de limpeza e sem a inclusão de uma taxa extra, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  
  1. **Teste:** `test_stays_garbage_04_cleaning_fee`

  **Descrição do teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) quando não há taxa de limpeza e nenhuma taxa extra está incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco mitigado com esse teste:**

  Ao assegurar que o cálculo dos valores de uma reserva de estadia esteja correto mesmo na ausência de uma taxa de limpeza e sem a inclusão de uma taxa extra, este teste ajuda a mitigar o risco de discrepâncias nos custos para os clientes ou prejuízos financeiros para a empresa.

  Sugestões:

  
  1. **Teste com desconto de cupom aplicado:**
     * Crie um teste onde um desconto de cupom é aplicado à reserva e verifique se os valores calculados refletem corretamente o desconto aplicado.
  2. **Teste com taxa extra e taxa de limpeza:**
     * Elabore um teste onde tanto uma taxa extra quanto uma taxa de limpeza estão incluídas na reserva e verifique se os cálculos são precisos nessas condições.
  3. **Teste com desconto manual aplicado:**
     * Crie um teste onde um desconto manual é aplicado à reserva e verifique se os valores calculados refletem corretamente o desconto manual aplicado.
  4. **Teste com diferentes valores de comissão OTA:**
     * Crie testes com diferentes valores de comissão OTA e verifique se os cálculos dos valores totais e das comissões estão corretos para cada valor.
  5. **Teste com diferentes taxas de limpeza:**
     * Elabore testes com diferentes valores de taxa de limpeza e verifique se os cálculos são precisos para cada valor.
  6. **Teste com valores de taxa extra variáveis:**
     * Crie testes com diferentes valores de taxa extra e verifique se os cálculos são precisos para cada valor.
  7. **Teste com desconto de cupom múltiplo:**
     * Crie um teste onde múltiplos descontos de cupom são aplicados à reserva e verifique se os valores calculados refletem corretamente todos os descontos aplicados.
* **Stays - test_airbnb_calculator.py**

  
  1. **Teste Unitário:** `test_stays_calc_airbnb_simple`

  **Descrição do Teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) proveniente de uma integração com o Airbnb. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco Mitigado com Este Teste:**

  Este teste ajuda a mitigar o risco de discrepâncias nos cálculos financeiros para reservas provenientes de integrações com o Airbnb. Garante que os valores totais, taxas e comissões estejam corretamente calculados, o que é crucial para evitar prejuízos financeiros para a empresa e para manter a confiança dos clientes.

  
  1. **Teste Unitário:** `test_stays_calc_airbnb_extra_fee`

  **Descrição do Teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) proveniente de uma integração com o Airbnb, que inclui uma taxa extra. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco Mitigado com Este Teste:**

  Este teste ajuda a mitigar o risco de discrepâncias nos cálculos financeiros para reservas provenientes de integrações com o Airbnb que incluem taxas extras. Garante que os valores totais, taxas e comissões estejam corretamente calculados, assegurando que a taxa extra seja adequadamente incorporada ao preço total da reserva.

  
  1. **Teste Unitário:** `test_stays_calc_airbnb_no_cleaning_fee`

  **Descrição do Teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) proveniente de uma integração com o Airbnb, em que não há taxa de limpeza incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco Mitigado com Este Teste:**

  Este teste ajuda a mitigar o risco de discrepâncias nos cálculos financeiros para reservas provenientes de integrações com o Airbnb que não incluem taxa de limpeza. Garante que os valores totais, taxas e comissões estejam corretamente calculados, mesmo na ausência dessa taxa.

  
  1. **Teste Unitário:** `test_stays_garbage_01_cleaning_fee`

  **Descrição do Teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) proveniente de uma fonte não especificada, em que não há taxa de limpeza incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco Mitigado com Este Teste:**

  Este teste ajuda a mitigar o risco de discrepâncias nos cálculos financeiros para reservas provenientes de fontes diversas que não incluem taxa de limpeza. Garante que os valores totais, taxas e comissões estejam corretamente calculados, mesmo na ausência dessa taxa.

  
  1. **Teste Unitário:** `test_stays_garbage_02_cleaning_fee`

  **Descrição do Teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) proveniente de uma fonte não especificada, em que não há taxa de limpeza incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco Mitigado com Este Teste:**

  Este teste ajuda a mitigar o risco de discrepâncias nos cálculos financeiros para reservas provenientes de fontes diversas que não incluem taxa de limpeza. Garante que os valores totais, taxas e comissões estejam corretamente calculados, mesmo na ausência dessa taxa.

  
  1. **Teste Unitário:** `test_stays_garbage_03_cleaning_fee`

  **Descrição do Teste:**

  Este teste unitário verifica o cálculo dos valores relacionados a uma reserva de estadia (stays reservation) proveniente de uma fonte não especificada, em que não há taxa de limpeza incluída. Utiliza um mock de desconto de cupom para simular a ausência de desconto aplicado. Os valores calculados são comparados com os valores esperados para garantir a precisão do cálculo.

  **Risco Mitigado com Este Teste:**

  Este teste ajuda a mitigar o risco de discrepâncias nos cálculos financeiros para reservas provenientes de fontes diversas que não incluem taxa de limpeza. Garante que os valores totais, taxas e comissões estejam corretamente calculados, mesmo na ausência dessa taxa.

  **Sugestão:**

  
  1. **Teste Unitário de Reserva com Desconto de Cupom:**
     * Descrição do Teste: Verificar o cálculo dos valores quando um desconto de cupom é aplicado à reserva.
     * Risco Mitigado: Garantir que os descontos de cupom sejam aplicados corretamente aos valores calculados.
  2. **Teste Unitário de Reserva com Desconto Manual:**
     * Descrição do Teste: Verificar o cálculo dos valores quando um desconto manual é aplicado à reserva.
     * Risco Mitigado: Assegurar que os descontos manuais sejam aplicados corretamente aos valores calculados.
  3. **Teste Unitário de Reserva com Taxa Extra e Desconto de Cupom:**
     * Descrição do Teste: Verificar o cálculo dos valores quando uma taxa extra e um desconto de cupom são aplicados à reserva.
     * Risco Mitigado: Garantir que tanto a taxa extra quanto o desconto de cupom sejam aplicados corretamente aos valores calculados.
  4. **Teste Unitário de Reserva com Taxa de Limpeza e Desconto Manual:**
     * Descrição do Teste: Verificar o cálculo dos valores quando uma taxa de limpeza e um desconto manual são aplicados à reserva.
     * Risco Mitigado: Assegurar que tanto a taxa de limpeza quanto o desconto manual sejam aplicados corretamente aos valores calculados.
  5. **Teste Unitário de Reserva com Taxa de Limpeza e Taxa Extra:**
     * Descrição do Teste: Verificar o cálculo dos valores quando uma taxa de limpeza e uma taxa extra são aplicadas à reserva.
     * Risco Mitigado: Garantir que tanto a taxa de limpeza quanto a taxa extra sejam consideradas nos valores calculados.
  6. **Teste Unitário de Reserva com Desconto de Cupom e Desconto Manual:**
     * Descrição do Teste: Verificar o cálculo dos valores quando um desconto de cupom e um desconto manual são aplicados à reserva.
     * Risco Mitigado: Assegurar que tanto o desconto de cupom quanto o desconto manual sejam aplicados corretamente aos valores calculados.
  7. **Teste Unitário de Reserva com Taxa de Limpeza, Taxa Extra e Desconto de Cupom:**
     * Descrição do Teste: Verificar o cálculo dos valores quando uma taxa de limpeza, uma taxa extra e um desconto de cupom são aplicados à reserva.
     * Risco Mitigado: Garantir que todos os elementos da reserva sejam corretamente considerados nos valores calculados.
  8. **Teste Unitário de Reserva com Valores Nulos:**
     * Descrição do Teste: Verificar o comportamento do sistema quando a reserva possui valores nulos ou vazios.
     * Risco Mitigado: Identificar e corrigir possíveis falhas no sistema ao lidar com entradas inválidas.
* **Pipefy - test_pipefy_importer.py**

  
  1. **Teste Unitário:** `test_execute`

  **Descrição do teste:** Este teste unitário verifica a execução do processo de importação de dados do Pipefy para o sistema, envolvendo a criação ou atualização de propriedades de imóveis e de dados de onboarding. Utiliza mocks para simular chamadas a APIs externas e interações com o banco de dados. Após a execução do processo, verifica se todas as operações esperadas foram realizadas corretamente, como a obtenção de informações de cartão do Pipefy, a criação ou atualização de dados de propriedades e onboarding no sistema.

  **Risco mitigado com esse teste:** Ao garantir que o processo de importação de dados do Pipefy funcione corretamente, este teste ajuda a mitigar o risco de inconsistências nos dados do sistema ou falhas na integração com o Pipefy. Ele também assegura que as informações dos cartões do Pipefy sejam corretamente mapeadas e atualizadas no sistema, reduzindo o risco de erros ou perda de dados durante o processo de importação.

  
  1. **Teste Unitário:** `test_execute_with_property_code`

  **Descrição do teste:** Este teste unitário verifica a execução do processo de importação de dados do Pipefy para o sistema, especificamente quando o código do imóvel está disponível nos campos do cartão do Pipefy. Utiliza mocks para simular chamadas a APIs externas e interações com o banco de dados. Após a execução do processo, verifica se todas as operações esperadas foram realizadas corretamente, como a obtenção de informações de cartão do Pipefy, a criação ou atualização de dados de propriedades e onboarding no sistema.

  **Risco mitigado com esse teste:** Ao garantir que o processo de importação de dados do Pipefy funcione corretamente, mesmo quando o código do imóvel está disponível em um campo específico, este teste ajuda a mitigar o risco de inconsistências nos dados do sistema ou falhas na integração com o Pipefy. Ele assegura que as informações dos cartões do Pipefy sejam corretamente mapeadas e atualizadas no sistema, mesmo em cenários específicos, reduzindo o risco de erros ou perda de dados durante o processo de importação.

  
  1. **Teste Unitário:** `test_execute_without_property_code`

  **Descrição do teste:** Este teste unitário verifica a execução do processo de importação de dados do Pipefy para o sistema quando o código do imóvel não está disponível nos campos do cartão do Pipefy. Utiliza mocks para simular chamadas a APIs externas e interações com o banco de dados. Após a execução do processo, verifica se todas as operações esperadas foram realizadas corretamente, como a obtenção de informações de cartão do Pipefy e a execução do onboarding no sistema.

  **Risco mitigado com esse teste:** Ao garantir que o processo de importação de dados do Pipefy funcione corretamente mesmo quando o código do imóvel não está disponível nos campos do cartão do Pipefy, este teste ajuda a mitigar o risco de falhas no processo de importação quando as informações de identificação da propriedade não estão adequadamente preenchidas no Pipefy. Isso assegura que o sistema seja capaz de lidar com diferentes cenários de dados incompletos ou ausentes, garantindo a robustez do processo de importação.

  Sugestões:

  
  1. **Teste para verificar a importação de dados de vários cartões do Pipefy:**
     * Descrição: Este teste verifica se o sistema é capaz de lidar corretamente com a importação de dados de vários cartões do Pipefy em uma única execução.
     * Risco mitigado: Garante que o sistema possa lidar com cenários nos quais há vários cartões a serem processados simultaneamente, garantindo a escalabilidade e a eficiência do processo de importação.
  2. **Teste para verificar o tratamento de exceções durante a importação:**
     * Descrição: Este teste simula uma exceção durante o processo de importação de dados do Pipefy e verifica se o sistema lida corretamente com essa exceção, registra adequadamente o erro e continua a execução sem interrupções.
     * Risco mitigado: Garante que o sistema seja robusto o suficiente para lidar com situações inesperadas, como falhas de rede ou erros nos dados de entrada, minimizando possíveis interrupções no processo de importação.
  3. **Teste para verificar a atualização de propriedades existentes:**
     * Descrição: Este teste verifica se o sistema é capaz de atualizar adequadamente as propriedades existentes no banco de dados com novos dados importados do Pipefy, mantendo a consistência e a integridade dos dados.
     * Risco mitigado: Garante que o sistema possa atualizar informações existentes sem introduzir duplicatas ou conflitos de dados, mantendo a precisão e a confiabilidade das informações armazenadas.
  4. **Teste para verificar a execução do onboarding para diferentes tipos de propriedades:**
     * Descrição: Este teste verifica se o sistema executa corretamente o processo de onboarding para diferentes tipos de propriedades (por exemplo, residencial, comercial, industrial) com base nos dados importados do Pipefy.
     * Risco mitigado: Garante que o sistema seja capaz de adaptar o processo de onboarding de acordo com as características específicas de cada tipo de propriedade, proporcionando uma experiência personalizada e adequada para cada cliente.
  5. **Teste para verificar a importação de dados de vários cartões do Pipefy:**
     * Descrição: Este teste verifica se o sistema é capaz de lidar corretamente com a importação de dados de vários cartões do Pipefy em uma única execução.
     * Risco mitigado: Garante que o sistema possa lidar com cenários nos quais há vários cartões a serem processados simultaneamente, garantindo a escalabilidade e a eficiência do processo de importação.
  6. **Teste para verificar o tratamento de exceções durante a importação:**
     * Descrição: Este teste simula uma exceção durante o processo de importação de dados do Pipefy e verifica se o sistema lida corretamente com essa exceção, registra adequadamente o erro e continua a execução sem interrupções.
     * Risco mitigado: Garante que o sistema seja robusto o suficiente para lidar com situações inesperadas, como falhas de rede ou erros nos dados de entrada, minimizando possíveis interrupções no processo de importação.
  7. **Teste para verificar a atualização de propriedades existentes:**
     * Descrição: Este teste verifica se o sistema é capaz de atualizar adequadamente as propriedades existentes no banco de dados com novos dados importados do Pipefy, mantendo a consistência e a integridade dos dados.
     * Risco mitigado: Garante que o sistema possa atualizar informações existentes sem introduzir duplicatas ou conflitos de dados, mantendo a precisão e a confiabilidade das informações armazenadas.
* **Pipedrive - test_pipedrive_importer.py (Testes comentados)**

  
  1. **Teste** `Unitário: setUp`

  **Descrição do Teste:** Este teste unitário configura o ambiente de teste criando dois parceiros (partners) e fazendo duas indicações de propriedade (property) e duas indicações de investimento (investment) para cada parceiro. Em seguida, ele testa se a configuração do pipeline do Pipedrive está correta e se a função para traduzir a coluna do funil comercial está sendo chamada.

  **Risco Mitigado com Esse Teste:** Este teste ajuda a garantir que a criação de parceiros e indicações esteja funcionando corretamente no módulo. Além disso, verifica se as configurações do pipeline do Pipedrive estão corretas e se a função de tradução da coluna do funil comercial está sendo chamada adequadamente. Isso ajuda a reduzir o risco de falhas na criação de parceiros e indicações, bem como na configuração incorreta do pipeline do Pipedrive, garantindo assim a integridade dos dados e o correto funcionamento da integração com o Pipedrive.

  
  2. **Teste Unitário:** `test_execute_create_property_indication_success`

  **Descrição do Teste:** Este teste unitário verifica se a criação de uma indicação de propriedade (property indication) é bem-sucedida. Ele simula a criação de um negócio (deal) no Pipedrive e verifica se a indicação correspondente foi criada corretamente no banco de dados. Além disso, verifica se o parceiro (partner) e o usuário associados à indicação foram atualizados corretamente após a execução da ação.

  **Risco Mitigado com Esse Teste:** Ao testar a criação bem-sucedida de uma indicação de propriedade, este teste ajuda a garantir que o processo de integração com o Pipedrive esteja funcionando corretamente. Ele reduz o risco de falhas na criação de indicações no Pipedrive e no banco de dados local

  **Sugestões:**

  
  1. **Teste de Falha na Criação de Indicação:**
     * Descrição: Este teste simularia uma falha na criação de uma indicação de propriedade no Pipedrive, garantindo que o sistema lida adequadamente com esse cenário e não cria a indicação localmente se a operação no Pipedrive falhar.
     * Risco Mitigado: Garante que o sistema seja robusto o suficiente para lidar com falhas de integração e evita inconsistências nos dados entre o Pipedrive e o banco de dados local.
  2. **Teste de Exceção para Campos Ausentes:**
     * Descrição: Este teste simularia uma situação em que campos obrigatórios estão ausentes no negócio criado no Pipedrive, garantindo que o sistema trate adequadamente essas exceções e não crie a indicação localmente se informações essenciais estiverem faltando.
     * Risco Mitigado: Ajuda a garantir que o sistema seja robusto o suficiente para lidar com cenários inesperados e evita a criação de indicações incompletas ou inválidas no banco de dados local.
  3. **Teste de Integração com API Pipedrive:**
     * Descrição: Este teste irá verificar se a integração com a API do Pipedrive está funcionando corretamente, simulando chamadas de API para criar e atualizar negócios e garantindo que os dados sejam sincronizados corretamente entre os sistemas.
     * Risco Mitigado: Reduz o risco de problemas de integração entre o sistema local e o Pipedrive, garantindo que as operações de criação e atualização de negócios ocorram sem falhas.
* **Pipedrive - test_pipedrive_creator.py**

  
  1. **Teste Unitário:** `setUp`

  **Descrição do Teste:** Este teste configura o ambiente de teste para a execução de outros testes relacionados ao módulo `channel_manager`. Durante a configuração, ele cria objetos de usuário e parceiro no banco de dados de teste, atribui funções específicas a esses usuários, e cria indicações de propriedade e investimento associadas a esses parceiros. O teste visa preparar um cenário realista para os testes subsequentes do módulo.

  **Risco Mitigado com Esse Teste:** Esse teste ajuda a garantir que o ambiente de teste esteja devidamente configurado antes da execução de outros testes no módulo. Ao criar objetos de usuário, parceiro e indicação, ele reduz o risco de erros relacionados à ausência ou configuração incorreta desses objetos durante os testes subsequentes. Isso ajuda a garantir que os testes subsequentes sejam executados em um ambiente controlado e previsível, melhorando assim a confiabilidade e a precisão dos resultados dos testes.

  
  1. **Teste Unitário:** `test_execute_property_indication_no_persons_no_email_success`

  **Descrição do Teste:** Neste teste, o Pipedrive Creator é acionado para criar uma indicação no Pipedrive quando não há pessoas associadas à indicação e nenhum e-mail disponível para busca de pessoas indicadas. Mocks são configurados para simular a interação com a API do Pipedrive. Isso inclui a criação de uma pessoa associada ao parceiro, a busca por uma pessoa indicada com base em seu e-mail ou telefone (sem sucesso neste caso), e a criação de um negócio no Pipedrive. O objetivo é verificar se a execução do Pipedrive Creator ocorre conforme o esperado quando não há pessoas associadas à indicação e nenhum e-mail está disponível para busca de pessoas indicadas.

  **Risco Mitigado com Esse Teste:** Este teste ajuda a mitigar o risco de falhas na criação de indicações quando não há pessoas associadas à indicação ou nenhum e-mail disponível para busca de pessoas indicadas. Ele verifica se o Pipedrive Creator lida corretamente com esses cenários, garantindo que o processo de criação de indicações continue de forma adequada, mesmo quando algumas informações necessárias estão ausentes. Isso ajuda a garantir a robustez e a resiliência do sistema em situações adversas.

  **Sugestões**:

  
  1. **Teste Unitário de Execução com E-mail de Pessoa Indicada Ausente:**
     * Neste teste, simule a situação em que a busca por uma pessoa indicada através do e-mail não retorna resultados. Certifique-se de que o sistema lida adequadamente com essa situação, talvez gerando um log de erro apropriado ou realizando uma ação alternativa.
  2. **Teste Unitário de Execução com Telefone de Pessoa Indicada Ausente:**
     * Semelhante ao teste anterior, este teste verifica o comportamento do sistema quando a busca por uma pessoa indicada através do telefone não retorna resultados. Garanta que o sistema trate essa situação corretamente, podendo gerar um log de erro ou tomar uma medida alternativa.
  3. **Teste Unitário de Execução com Pessoas Indicadas Duplicadas:**
     * Este teste cria um cenário em que múltiplas pessoas indicadas compartilham o mesmo e-mail ou número de telefone. Verifique se o sistema trata corretamente essa condição, evitando duplicações e garantindo a integridade dos dados.
  4. **Teste Unitário de Execução com Falha na Criação da Pessoa Parceira:**
     * Simule uma falha na criação da pessoa parceira no Pipedrive e verifique se o sistema lida adequadamente com esse erro, possivelmente revertendo as alterações ou registrando informações para análise posterior.
  5. **Teste Unitário de Execução com Falha na Criação do Negócio no Pipedrive:**
     * Este teste verifica como o sistema responde a uma falha na criação do negócio no Pipedrive. Garanta que as ações apropriadas sejam tomadas para lidar com essa situação, como registrar informações de erro e reverter transações.
  6. **Teste Unitário de Execução com Dados de Indicação Ausentes:**
     * Este teste verifica o comportamento do sistema quando os dados da indicação estão ausentes ou incompletos. Garanta que o sistema trate essas condições, possivelmente gerando um erro ou ignorando a execução.
  7. **Teste Unitário de Execução com Parceiro Inativo:**
     * Crie um cenário em que o parceiro associado à indicação esteja marcado como inativo. Verifique se o sistema lida adequadamente com essa condição, talvez gerando um aviso ou ignorando a execução da operação.
  8. **Teste Unitário de Execução com Dados de Indicação Inválidos:**
     * Neste teste, forneça dados de indicação inválidos ou incorretos e verifique se o sistema os valida adequadamente antes de prosseguir com a execução. Certifique-se de que o sistema rejeite dados inválidos e informe o usuário sobre o problema.
* **Legacy_stays - test_airbnb_extension_log.py**

  Teste: `test_log_creating_when_there_is_late_extension_on_reservation`

  **Descrição do teste:** Este teste unitário verifica se um log é criado quando uma reserva do Airbnb está sendo atualizada e há uma extensão atrasada na reserva do SAPRON que foi conciliada.

  **Risco mitigado com este teste:** O risco mitigado com este teste é a garantia de que um log seja criado corretamente quando uma situação específica ocorre durante a atualização de uma reserva do Airbnb. Isso ajuda a assegurar que o sistema esteja registrando corretamente as informações relevantes e que as operações de atualização de reserva estejam funcionando conforme o esperado, especialmente em casos de extensões tardias. Isso contribui para a integridade dos registros do sistema e para a rastreabilidade das ações realizadas.

  Sugestão:

  
  1. **Teste de criação de log quando não há extensão atrasada na reserva do SAPRON:**
     * Descrição: Este teste verifica se um log não é criado quando não há extensão atrasada na reserva do SAPRON durante a atualização de uma reserva do Airbnb.
     * Risco mitigado: Garantir que logs não sejam criados desnecessariamente quando não há situações específicas ocorrendo durante a atualização da reserva.
  2. **Teste de criação de log quando a reserva do SAPRON não está conciliada:**
     * Descrição: Este teste verifica se um log não é criado quando a reserva do SAPRON associada não está conciliada durante a atualização de uma reserva do Airbnb.
     * Risco mitigado: Garantir que logs não sejam criados quando a reserva do SAPRON não está em um estado que exija a criação de um log durante a atualização da reserva do Airbnb.
  3. **Teste de criação de log sem dados de reserva do SAPRON:**
     * Descrição: Verifica se um log não é criado quando não há dados válidos da reserva do SAPRON durante a atualização de uma reserva do Airbnb.
     * Risco mitigado: Garantir que logs não sejam criados se os dados da reserva do SAPRON estiverem ausentes ou forem inválidos, evitando assim registros incorretos ou desnecessários.
  4. **Teste de criação de log sem dados de reserva do Airbnb:**
     * Descrição: Verifica se um log não é criado quando não há dados válidos da reserva do Airbnb durante a atualização.
     * Risco mitigado: Garantir que logs não sejam criados se os dados da reserva do Airbnb estiverem ausentes ou forem inválidos, evitando assim registros incorretos ou desnecessários.
  5. **Teste de criação de log com dados de reserva válidos:**
     * Descrição: Verifica se um log é criado corretamente quando todos os dados de reserva são válidos e atendem aos critérios para criação de log.
     * Risco mitigado: Garantir que os logs sejam criados corretamente quando todas as condições para criação de log forem atendidas, assegurando a precisão e integridade das informações registradas.
  6. **Teste de criação de log com informações de propriedade inválidas:**
     * Descrição: Verifica se um log não é criado quando as informações da propriedade associada à reserva do SAPRON são inválidas.
     * Risco mitigado: Evitar a criação de logs com informações inconsistentes ou inválidas, o que pode comprometer a integridade dos registros do sistema.
  7. **Teste de criação de log com informações de usuário inválidas:**
     * Descrição: Verifica se um log não é criado quando as informações do usuário associado à reserva do SAPRON são inválidas.
     * Risco mitigado: Evitar a criação de logs com informações de usuário inconsistentes ou inválidas, o que pode comprometer a integridade dos registros do sistema.
* **Legacy_stays - test_airbnb_extesion.py**

  **Teste:** `LegacyStaysAirbnbExtensionTestCase`

  **Descrição do teste:** Este teste verifica se a extensão do Airbnb é tratada corretamente pelo módulo `LegacyStaysAirbnbExtension`. Ele cria uma reserva de estadia (stays_reservation) e seus detalhes, e também uma reserva no sistema SAPRON (sapron_reservation). Em seguida, associa a reserva do SAPRON à reserva de estadia e executa a extensão do Airbnb. Após a execução da extensão, verifica se a contagem de objetos `Reservation_State` é igual a 2, garantindo que a reserva de extensão do Airbnb foi tratada adequadamente.

  **Risco mitigado com este teste:** Este teste ajuda a mitigar o risco de erros na lógica de extensão do Airbnb. Garante que, quando uma reserva de estadia do Airbnb é estendida, a ação correspondente no sistema SAPRON é executada corretamente e a associação entre as duas reservas é mantida, evitando discrepâncias ou falhas no tratamento da extensão.

  Sugestões:

  
  1. **Teste de Extensão do Airbnb com Reserva de Estadia em Outro OTA:**
     * **Descrição:** Este teste verifica o comportamento do sistema quando uma reserva de estadia de um OTA diferente do Airbnb é estendida.
     * **Risco Mitigado:** Garante que a funcionalidade de extensão do Airbnb não afeta inadvertidamente reservas de outros OTAs.
  2. **Teste de Extensão do Airbnb com Reserva de Estadia sem Reserva Correspondente no SAPRON:**
     * **Descrição:** Verifica como o sistema trata uma extensão do Airbnb quando não há uma reserva correspondente no SAPRON.
     * **Risco Mitigado:** Garante que o sistema lida corretamente com situações incomuns ou erros de integração, como reservas faltantes no SAPRON.
  3. **Teste de Extensão do Airbnb com Dados de Reserva Ausentes:**
     * **Descrição:** Este teste simula uma extensão do Airbnb com dados de reserva ausentes ou incompletos.
     * **Risco Mitigado:** Ajuda a identificar e corrigir possíveis falhas de tratamento de exceções ou erros de integração quando os dados de reserva estão incompletos.
  4. **Teste de Extensão do Airbnb com Datas de Reserva Incorretas:**
     * **Descrição:** Verifica como o sistema reage a uma tentativa de extensão do Airbnb com datas de reserva inconsistentes.
     * **Risco Mitigado:** Garante que o sistema valide adequadamente as datas de reserva e evite comportamentos inesperados ou erros de processamento.
  5. **Teste de Extensão do Airbnb com Dados de Hóspedes Ausentes:**
     * **Descrição:** Este teste examina o comportamento do sistema quando os dados do hóspede estão ausentes durante uma extensão do Airbnb.
     * **Risco Mitigado:** Garante que o sistema seja capaz de lidar com situações em que os dados do hóspede não estão disponíveis e continue executando a extensão de forma adequada.
  6. **Teste de Extensão do Airbnb com Reserva de Estadia sem Código de Propriedade Correspondente:**
     * **Descrição:** Verifica como o sistema trata uma extensão do Airbnb quando não há um código de propriedade correspondente no SAPRON.
     * **Risco Mitigado:** Garante que o sistema seja capaz de lidar com situações em que a associação entre a reserva de estadia e a propriedade no SAPRON não é encontrada.
  7. **Teste de Extensão do Airbnb com Falha na Execução da Ação:**
     * **Descrição:** Este teste força uma falha na execução da ação de extensão do Airbnb e verifica como o sistema lida com essa situação.
     * **Risco Mitigado:** Garante que o sistema seja resiliente a falhas e possa lidar adequadamente com exceções ou erros durante o processo de extensão.
* **Legacy_stays - test_airbnb_updater.py**

  
  1. **Teste**: `test_ota_calculations e test_ota_calculations_none_cleaning_fee`

  **Descrição do teste**: Este teste verifica se os cálculos relacionados às taxas do OTA (Online Travel Agency) estão sendo realizados corretamente durante a atualização de uma reserva no sistema. Ele calcula a taxa de limpeza líquida, a comissão do OTA e o valor líquido diário da reserva com base nos dados fornecidos.

  **Risco mitigado com esse teste**: Este teste ajuda a garantir que os cálculos relacionados às taxas do OTA estejam corretos e consistentes. Isso é crucial para garantir que os valores financeiros das reservas sejam calculados com precisão, evitando assim erros que possam levar a discrepâncias nos registros financeiros e possíveis perdas financeiras para a empresa.

  **Sugestões:**

  
   1. \*\*`test_ota_calculations_cleaning_fee_not_none**:` Este teste verifica se os cálculos relacionados às taxas do OTA são corretos quando a taxa de limpeza não é nula. Ele pode incluir cenários em que diferentes valores de taxa de limpeza são atribuídos e verificar se os cálculos são precisos para cada um desses valores.
   2. `test_ota_calculations_total_forward_fee_zero`: Este teste verifica o comportamento do sistema quando a taxa total do OTA é zero. Isso pode ser útil para garantir que o sistema seja capaz de lidar adequadamente com situações em que não há taxa a ser cobrada pelo OTA.
   3. \*\*`test_ota_calculations_negative_gross_price**:` Este teste verifica se o sistema lida corretamente com cenários em que o preço bruto da reserva é negativo. Isso pode incluir situações em que há descontos aplicados à reserva que resultam em um preço líquido negativo.
   4. \*\*`test_ota_calculations_invalid_ota_fee**:` Neste teste, verifica-se como o sistema responde quando a taxa do OTA é invalidamente definida, por exemplo, como um valor negativo ou como uma string não numérica. Isso ajuda a garantir que o sistema seja robusto o suficiente para lidar com entradas inválidas e evitar falhas inesperadas.
   5. \*\*`test_ota_calculations_invalid_property_data**:` Este teste verifica se o sistema lida corretamente com dados de propriedade inválidos ou ausentes durante os cálculos das taxas do OTA. Pode incluir cenários em que a propriedade associada à reserva não está presente no sistema ou possui informações inconsistentes.
   6. `test_ota_calculations_invalid_reservation_data`: Este teste verifica o comportamento do sistema quando os dados da reserva são inválidos ou incompletos. Isso pode incluir cenários em que informações essenciais estão ausentes na reserva ou são fornecidas de forma incorreta.
   7. \*\*`test_ota_calculations_invalid_guest_data**:` Neste teste, verifica-se como o sistema lida com dados de hóspedes inválidos ou ausentes durante os cálculos das taxas do OTA. Isso pode incluir situações em que as informações do hóspede não estão disponíveis ou são inconsistentes.
   8. \*\*`test_ota_calculations_high_precision**:` Este teste verifica se os cálculos relacionados às taxas do OTA são precisos mesmo para valores de alta precisão, como números decimais longos. Isso ajuda a garantir que o sistema possa lidar com diferentes escalas de valores sem perder precisão nos cálculos.
   9. \*\*`test_ota_calculations_large_data_volume**:` Este teste verifica o desempenho do sistema ao lidar com um grande volume de dados de reserva. Ele pode incluir a criação de um grande número de reservas e verificar se os cálculos das taxas do OTA são concluídos dentro de um tempo razoável e sem sobrecarga excessiva no sistema.
  10. \*\*`test_ota_calculations_boundary_cases**:` Este teste examina os limites do sistema, incluindo valores mínimos, máximos e casos extremos para os parâmetros envolvidos nos cálculos das taxas do OTA. Isso ajuda a garantir que o sistema se comporte corretamente em todas as situações possíveis.
* **Legacy_stays - test_stays_blocker.py**

  
  1. **Teste:** `test_block_creation`

  **Descrição do teste:** Este teste verifica se um bloqueio de reserva é criado corretamente no sistema legado. Ele cria um objeto de reserva de bloqueio usando dados fictícios e verifica se os atributos do bloqueio são configurados corretamente, incluindo o status da reserva, se é um bloqueio, a lista associada, as datas de criação, check-in e check-out.

  **Risco mitigado com esse teste:** Este teste garante que a criação de um bloqueio de reserva funcione conforme o esperado, ajudando a mitigar o risco de falhas na criação de bloqueios, o que poderia levar a reservas não bloqueadas ou bloqueadas incorretamente.

  **Sugestões:**

  
  1. **Teste de bloqueio de reserva com lista vazia de bloqueio:**
     * Descrição: Este teste verifica se uma exceção é levantada quando a lista de bloqueios de reserva está vazia.
     * Risco mitigado: Garante que o sistema seja robusto o suficiente para lidar com casos inesperados, evitando falhas inesperadas devido a dados ausentes.
  2. **Teste de bloqueio de reserva com reserva inválida:**
     * Descrição: Este teste verifica se uma exceção é levantada ao tentar bloquear uma reserva que não existe no sistema.
     * Risco mitigado: Evita que bloqueios sejam criados para reservas inválidas, garantindo a integridade dos dados e a consistência do sistema.
  3. **Teste de bloqueio de reserva com reserva já bloqueada:**
     * Descrição: Verifica se uma exceção é levantada ao tentar bloquear uma reserva que já está marcada como bloqueada no sistema.
     * Risco mitigado: Impede a duplicação de bloqueios para a mesma reserva, evitando inconsistências e problemas de gerenciamento de recursos.
  4. **Teste de bloqueio de reserva com propriedade inválida:**
     * Descrição: Testa se uma exceção é levantada ao tentar bloquear uma reserva para uma propriedade que não existe no sistema.
     * Risco mitigado: Garante que apenas propriedades válidas possam ser associadas a bloqueios de reserva, evitando erros relacionados à integridade dos dados.
  5. **Teste de bloqueio de reserva com dados inválidos:**
     * Descrição: Este teste verifica se uma exceção é levantada ao tentar bloquear uma reserva com dados inválidos ou ausentes.
     * Risco mitigado: Garante que apenas dados válidos sejam aceitos durante o processo de bloqueio de reserva, reduzindo o risco de inconsistências ou erros no sistema.
  6. **Teste de bloqueio de reserva com o mesmo ID de reserva já existente:**
     * Descrição: Verifica se uma exceção é levantada ao tentar bloquear uma reserva com o mesmo ID de reserva já existente no sistema.
     * Risco mitigado: Evita a duplicação de registros de bloqueio para a mesma reserva, garantindo a integridade dos dados e a consistência do sistema.
  7. **Teste de atualização de bloqueio de reserva com dados inválidos:**
     * Descrição: Este teste verifica se uma exceção é levantada ao tentar atualizar um bloqueio de reserva com dados inválidos ou ausentes.
     * Risco mitigado: Garante que apenas dados válidos sejam aceitos durante o processo de atualização de bloqueio de reserva, reduzindo o risco de inconsistências ou erros no sistema.
* **Legacy_stays - test_stays_canceller.py**

  
  1. **Teste**: `test_cancel`
     * **Descrição**: Este teste verifica se uma reserva é cancelada corretamente quando um pedido de cancelamento válido é recebido.
     * **Risco Mitigado**: Garante que o sistema é capaz de cancelar corretamente as reservas quando um pedido de cancelamento válido é recebido, evitando erros de processamento de cancelamento e garantindo uma experiência consistente para os usuários.
  2. **Teste:** `test_cancel_invalid_state`
     * **Descrição**: Este teste verifica se uma exceção é levantada corretamente quando um pedido de cancelamento é feito para uma reserva em um estado inválido para cancelamento.
     * **Risco Mitigado**: Garante que o sistema se comporte adequadamente ao receber pedidos de cancelamento para reservas em estados que não podem ser cancelados, evitando operações indevidas e possíveis inconsistências nos dados de reserva.

  **Sugestões:**

  
  1. **Teste de Cancelamento com Reserva Ausente**:
     * Descrição: Verifica se uma exceção é levantada quando um pedido de cancelamento é feito para uma reserva que não existe.
     * Risco Mitigado: Garante que o sistema não tente cancelar reservas que não estão presentes no sistema, evitando possíveis erros de processamento.
  2. **Teste de Cancelamento com Reserva Nula**:
     * Descrição: Verifica se uma exceção é levantada quando um pedido de cancelamento é feito para uma reserva nula.
     * Risco Mitigado: Evita possíveis erros devido a falhas no sistema ao tentar cancelar uma reserva que não foi corretamente inicializada.
  3. **Teste de Cancelamento com Reserva Inativa**:
     * Descrição: Verifica se uma exceção é levantada quando um pedido de cancelamento é feito para uma reserva que está inativa.
     * Risco Mitigado: Garante que apenas reservas ativas possam ser canceladas, mantendo a integridade dos dados e evitando operações indevidas.
  4. **Teste de Cancelamento com Pedido de Cancelamento Inválido**:
     * Descrição: Verifica se uma exceção é levantada quando um pedido de cancelamento é feito com dados inválidos ou incompletos.
     * Risco Mitigado: Garante que o sistema valide corretamente os pedidos de cancelamento e trate adequadamente as entradas inválidas, evitando operações inesperadas ou incorretas.
  5. **Teste de Cancelamento com Dados de Reserva Incorretos**:
     * Descrição: Verifica se uma exceção é levantada quando um pedido de cancelamento é feito com dados inconsistentes ou incorretos sobre a reserva.
     * Risco Mitigado: Garante que o sistema seja capaz de identificar e lidar adequadamente com dados inconsistentes ou inválidos, prevenindo potenciais erros de processamento.
* **Legacy_stays - test_stays_expedia_updater.py**

  
  1. **Teste Unitário**: `test_ota_calculations`
  * **Descrição**: Este teste verifica se os cálculos relacionados à atualização de uma reserva Expedia estão corretos. Ele testa se os valores da taxa de limpeza líquida, comissão OTA e valor líquido diário são calculados corretamente com base nos dados da reserva.
  * **Risco Mitigado**: Este teste ajuda a mitigar o risco de erros nos cálculos relacionados à atualização de reservas Expedia. Ao garantir que os cálculos estejam corretos, reduzimos a possibilidade de cobranças incorretas para os clientes e possíveis prejuízos financeiros para a empresa.

  **Sugestão**:

  
  1. **Teste Unitário**: `test_ota_calculations_no_cleaning_fee`
     * **Descrição**: Verifica se os cálculos ainda são precisos quando a taxa de limpeza é nula.
     * **Risco Mitigado**: Garante que o sistema possa lidar adequadamente com casos em que não há taxa de limpeza definida, evitando erros de cálculo ou comportamento inesperado.
  2. **Teste Unitário**: `test_ota_calculations_no_ota_fee`
     * **Descrição**: Testa se os cálculos ainda estão corretos quando a taxa OTA é nula.
     * **Risco Mitigado**: Garante que o sistema possa lidar adequadamente com casos em que não há taxa OTA definida, garantindo que o valor líquido diário seja calculado corretamente.
  3. **Teste Unitário**: `test_ota_calculations_zero_total_price`
     * **Descrição**: Verifica o comportamento do sistema quando o preço total da reserva é zero.
     * **Risco Mitigado**: Ajuda a garantir que o sistema possa lidar com casos incomuns, como reservas com preço total zero, sem causar erros ou falhas inesperadas.
  4. **Teste Unitário**: `test_ota_calculations_negative_cleaning_fee`
     * **Descrição**: Testa o comportamento quando a taxa de limpeza é negativa.
     * **Risco Mitigado**: Garante que o sistema possa lidar com entradas inesperadas de dados sem causar resultados incorretos nos cálculos.
  5. **Teste Unitário**: `test_ota_calculations_negative_total_price`
     * **Descrição**: Verifica como o sistema lida com um preço total de reserva negativo.
     * **Risco Mitigado**: Ajuda a garantir que o sistema seja robusto o suficiente para lidar com entradas de dados inválidas e proteja contra resultados incorretos ou inesperados.
* **Legacy_stays - test_stays_extender.py**

  
  1. **Teste:** `test_extension_create`

  **Descrição do teste:** Este teste verifica se a extensão de uma reserva é criada corretamente. Ele cria uma reserva de extensão de estadia e verifica se os detalhes dessa extensão são armazenados corretamente no sistema, incluindo informações sobre a reserva original, hóspedes, datas, preços e outros detalhes relevantes.

  **Risco mitigado com esse teste:** Este teste ajuda a garantir que o sistema seja capaz de lidar adequadamente com a extensão de reservas de estadia. Ao verificar se as informações da extensão são corretamente armazenadas e associadas à reserva original, o teste ajuda a mitigar o risco de erros ou falhas no processo de extensão de reservas, garantindo que os hóspedes tenham uma experiência contínua e sem problemas ao estender sua estadia.

  
  1. **Teste:** `test_extension_update`

  **Descrição do teste:** Este teste verifica se a atualização de uma extensão de reserva é feita corretamente. Ele cria uma reserva de extensão de estadia e a associa a uma reserva original existente. Em seguida, verifica se os detalhes dessa extensão são atualizados corretamente no sistema, incluindo informações sobre a reserva original, hóspedes, datas, preços e outros detalhes relevantes.

  **Risco mitigado com esse teste:** Este teste ajuda a garantir que o sistema seja capaz de lidar adequadamente com a atualização de extensões de reservas de estadia. Ao verificar se as informações da extensão são corretamente atualizadas e associadas à reserva original, o teste ajuda a mitigar o risco de erros ou falhas no processo de atualização de extensões de reservas, garantindo que os hóspedes tenham uma experiência contínua e sem problemas ao estender sua estadia.

  Sugestão:

  
   1. **Teste de extensão com reserva original inexistente:** Verifique se uma exceção é levantada quando uma tentativa de estender uma reserva é feita, mas a reserva original correspondente não existe.
   2. **Teste de extensão com reserva original em estado inválido:** Teste se uma exceção é levantada quando uma tentativa de extensão é feita em uma reserva original que não está em um estado válido para extensão (por exemplo, cancelada).
   3. **Teste de extensão com datas inválidas:** Garanta que uma exceção seja levantada se as datas de extensão fornecidas forem inválidas (por exemplo, data de check-out anterior à data de check-in).
   4. **Teste de extensão com propriedade inválida:** Verifique se uma exceção é levantada quando a propriedade fornecida para a extensão não é válida ou não existe.
   5. **Teste de extensão com usuário inválido:** Teste se uma exceção é levantada quando o usuário associado à reserva original não é válido ou não existe.
   6. **Teste de atualização de extensão com datas inválidas:** Verifique se uma exceção é levantada se as datas da extensão forem inválidas durante a atualização.
   7. **Teste de atualização de extensão com detalhes ausentes:** Garanta que uma exceção seja levantada se alguns detalhes necessários para a extensão estiverem ausentes durante a atualização.
   8. **Teste de atualização de extensão com propriedade inválida:** Verifique se uma exceção é levantada quando a propriedade fornecida durante a atualização da extensão não é válida.
   9. **Teste de cancelamento de extensão:** Teste se uma extensão pode ser corretamente cancelada e se a reserva original é restaurada para o estado anterior.
  10. **Teste de cancelamento de extensão com reserva original cancelada:** Verifique se uma exceção é levantada ao tentar cancelar uma extensão se a reserva original já estiver cancelada.
* **Legacy_stays - test_stays_handler.py**

  
  1. Teste: `test_handle_update`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama o `StaysUpdater` com os parâmetros corretos ao lidar com uma atualização de estadia.
  * Risco mitigado com esse teste: Este teste garante que a lógica de atualização de estadia esteja funcionando corretamente, o que é crítico para garantir que as informações das estadias sejam atualizadas conforme esperado no sistema.

  
  1. Teste: `test_handle_update_with_listing_previous_created`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama o `StaysUpdater` com os parâmetros corretos ao lidar com uma atualização de estadia quando a lista correspondente já foi criada anteriormente.
  * Risco mitigado com esse teste: Este teste garante que a lógica de atualização de estadia lida corretamente com casos em que a lista correspondente já foi criada anteriormente, evitando a criação duplicada e garantindo consistência no sistema.

  
  1. Teste: `test_handle_airbnb_update`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama o `StaysAirbnbUpdater` com os parâmetros corretos ao lidar com uma atualização de estadia proveniente do Airbnb.
  * Risco mitigado com esse teste: Este teste garante que a lógica de tratamento de atualizações provenientes do Airbnb funciona corretamente, garantindo que as atualizações específicas desse canal sejam processadas de maneira adequada e consistente.

  
  1. Teste: `test_handle_expedia_update`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama o `StaysExpediaUpdater` com os parâmetros corretos ao lidar com uma atualização de estadia proveniente da API da Expedia.
  * Risco mitigado com esse teste: Este teste assegura que a lógica de tratamento de atualizações provenientes da Expedia está funcionando corretamente, garantindo que as atualizações específicas desse canal sejam processadas de maneira precisa e consistente.

  
  1. Teste: `test_handle_block`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama o `StaysBlocker` com os parâmetros corretos ao lidar com o bloqueio de uma reserva de estadia.
  * Risco mitigado com esse teste: Este teste garante que a lógica de tratamento de bloqueios de reserva esteja funcionando conforme o esperado, garantindo que as reservas bloqueadas sejam tratadas corretamente pelo sistema. Isso ajuda a evitar erros na manipulação de bloqueios, o que poderia levar a inconsistências nos dados ou falhas no sistema.

  
  1. Teste: `test_handle_update_cancel`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama o `StaysUpdater` com os parâmetros corretos ao lidar com o cancelamento de uma reserva de estadia.
  * Risco mitigado com esse teste: Esse teste ajuda a garantir que a lógica de tratamento de cancelamento de reserva esteja funcionando corretamente. Ao simular um cancelamento de reserva, podemos verificar se o sistema executa as operações necessárias, como atualização do status da reserva e notificação aos usuários relevantes.

  
  1. Teste: `test_handle_cancel`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama corretamente o `StaysCanceller` ao lidar com o cancelamento de uma reserva de estadia. Ele cria uma reserva de cancelamento fictícia no sistema de estadia e uma reserva correspondente no sistema SAPRON, e então verifica se o método `handle` chama o `StaysCanceller` com os parâmetros adequados.
  * Risco mitigado com esse teste: Este teste ajuda a garantir que o processo de cancelamento de reservas de estadia esteja funcionando corretamente, especialmente em termos de integração entre o sistema de estadia e o sistema SAPRON.

  
  1. Teste: `test_handle_extension`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama corretamente o `StaysExtender` ao lidar com a extensão de uma reserva de estadia. Ele cria uma reserva de extensão fictícia no sistema de estadia e verifica se o método `handle` chama o `StaysExtender` com os parâmetros apropriados.
  * Risco mitigado com esse teste: Esse teste garante que o processo de extensão de reservas de estadia funcione corretamente. Ao simular uma extensão de reserva e verificar se o `StaysExtender` é chamado adequadamente, o teste ajuda a evitar problemas como a falha na extensão real da reserva

  
  1. Teste: `test_handle_airbnb_extension`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama corretamente o `StaysAirbnbExtender` ao lidar com a extensão de uma reserva de estadia proveniente do Airbnb. Ele cria uma reserva de estadia fictícia no sistema do Airbnb e uma reserva correspondente no sistema SAPRON. O teste simula a extensão da reserva no Airbnb e verifica se o método `handle` chama o `StaysAirbnbExtender` com os parâmetros apropriados.
  * Risco mitigado com esse teste: Esse teste garante que o processo de extensão de reservas de estadia provenientes do Airbnb funcione corretamente. Ao simular uma extensão de reserva no Airbnb e verificar se o `StaysAirbnbExtender` é chamado adequadamente, o teste ajuda a evitar problemas como a falha na extensão real da reserva, a falta de comunicação entre os sistemas do Airbnb e a SAPRON

  
  1. Teste: `test_extend_reservation_conciliada`
  * Descrição do teste: Este teste verifica se o método `handle` do `StaysHandler` chama corretamente o `StaysExtender` ao lidar com a extensão de uma reserva conciliada. Ele cria uma reserva de estadia fictícia no sistema do Booking (OTA) e uma reserva correspondente no sistema SAPRON, ambas conciliadas. O teste simula a extensão da reserva e verifica se o método `handle` chama o `StaysExtender` com os parâmetros apropriados.
  * Risco mitigado com esse teste: Esse teste garante que o processo de extensão de reservas conciliadas funcione corretamente. Ao simular uma extensão de reserva conciliada e verificar se o `StaysExtender` é chamado adequadamente, o teste ajuda a evitar problemas como a falha na extensão real da reserva conciliada, a falta de comunicação entre os sistemas do OTA e a SAPRON, ou a extensão incorreta de reservas conciliadas.

  
  1. Teste: `handle`
  * Descrição do teste: Este teste verifica se o método `handle` do `LegacyStaysHandler` chama corretamente os métodos relevantes de atualização, extensão, bloqueio e cancelamento das reservas de estadia. Ele simula o processamento de uma reserva de estadia recebida do sistema de um determinado OTA e verifica se os métodos apropriados são chamados com os parâmetros corretos com base no tipo de reserva (atualização, extensão, bloqueio, cancelamento). O teste também verifica se uma entrada é criada na tabela `Reservation_State` para rastrear a relação entre a reserva de estadia do OTA e a reserva correspondente no sistema SAPRON.
  * Risco mitigado com esse teste: Este teste ajuda a garantir que o manipulador de reservas de estadia (`LegacyStaysHandler`) seja capaz de lidar corretamente com diferentes tipos de operações de reserva, como atualização, extensão, bloqueio e cancelamento. Isso reduz o risco de falhas no processamento de reservas de estadia, garantindo que as operações sejam executadas conforme o esperado e que as informações sejam devidamente registradas no sistema. Além disso, a verificação da criação da entrada na tabela `Reservation_State` ajuda a garantir que a sincronização entre as reservas do OTA e do SAPRON seja rastreável e mantida corretamente.

  
  1. Teste: `test_handle_stays_reservation_details_without_listing`
  * Descrição do teste: Este teste verifica o comportamento do método `handle` do `LegacyStaysHandler` quando os detalhes da reserva de estadia não incluem informações sobre a propriedade (`_idlisting`). Ele simula esse cenário criando uma reserva de estadia no SAPRON sem uma propriedade registrada e sem informações sobre a propriedade nos detalhes da reserva de estadia. O teste verifica se o método `handle` lida corretamente com essa situação, garantindo que as operações de extensão, atualização, bloqueio, cancelamento e extensão do Airbnb não sejam acionadas e que a consulta para obter as configurações da lista de estadias não seja feita.
  * Risco mitigado com esse teste: Esse teste ajuda a garantir que o manipulador de reservas de estadia (`LegacyStaysHandler`) seja robusto o suficiente para lidar adequadamente com casos em que os detalhes da reserva de estadia estejam incompletos ou inconsistentes, como a falta de informações sobre a propriedade. Isso reduz o risco de falhas no processamento de reservas de estadia e garante que o sistema seja capaz de lidar com uma variedade de situações inesperadas de entrada de dados. Além disso, o teste garante que consultas desnecessárias não sejam feitas quando as informações sobre a propriedade estão ausentes.

  
  1. Teste: `test_handle_no_stays_reservation_details`
  * Descrição do teste: Este teste verifica o comportamento do método `handle` do `LegacyStaysHandler` quando os detalhes da reserva de estadia não estão disponíveis. Ele simula esse cenário configurando o retorno da chamada `mock_get_stays_reservation_by_id` como `None`. O teste verifica se o método `handle` executa corretamente a operação de atualização (`update`) mesmo quando os detalhes da reserva de estadia não estão disponíveis.
  * Risco mitigado com esse teste: Esse teste ajuda a garantir que o manipulador de reservas de estadia (`LegacyStaysHandler`) seja robusto o suficiente para lidar adequadamente com casos em que os detalhes da reserva de estadia estejam ausentes. Isso reduz o risco de falhas no processamento de reservas de estadia e garante que o sistema seja capaz de lidar com situações em que as informações necessárias não estão disponíveis.

  Sugestões:

  
   1. **Teste de manipulação de reserva de estadia para outros provedores de OTA:**
      * Teste se o método `handle` corretamente chama o manipulador de atualização apropriado para outros provedores de OTA, como Expedia, Airbnb, etc.
   2. **Teste de manipulação de reserva de estadia com reserva anteriormente criada:**
      * Verifique se o método `handle` funciona corretamente quando a reserva já está criada anteriormente no sistema.
   3. **Teste de manipulação de reserva de estadia com reserva cancelada:**
      * Verifique se o método `handle` executa corretamente a lógica de cancelamento quando a reserva de estadia é cancelada.
   4. **Teste de manipulação de reserva de estadia com extensão de reserva:**
      * Verifique se o método `handle` lida corretamente com a extensão de reserva, garantindo que as datas de check-in e check-out sejam atualizadas conforme necessário.
   5. **Teste de manipulação de reserva de estadia com detalhes de reserva ausentes:**
      * Teste se o método `handle` lida adequadamente com o cenário em que os detalhes da reserva de estadia estão ausentes.
   6. **Teste de manipulação de reserva de estadia com propriedade não registrada:**
      * Verifique se o método `handle` cria uma nova propriedade se a propriedade associada à reserva de estadia não estiver registrada no sistema.
   7. **Teste de manipulação de reserva de estadia com falha na atualização:**
      * Teste se o método `handle` lida corretamente com cenários de falha ao tentar atualizar a reserva de estadia no sistema.
   8. **Teste de manipulação de reserva de estadia com reserva bloqueada:**
      * Verifique se o método `handle` executa corretamente a lógica de bloqueio quando a reserva de estadia é uma reserva bloqueada.
   9. **Teste de manipulação de reserva de estadia com reserva expirada:**
      * Teste se o método `handle` lida corretamente com cenários em que a reserva de estadia expirou.
  10. **Teste de manipulação de reserva de estadia com dados inválidos:**
      * Verifique se o método `handle` valida corretamente os dados de entrada e trata cenários de dados inválidos de forma apropriada.
  11. **Teste de manipulação de reserva de estadia com manipuladores mockados:**
      * Use mocks para simular diferentes cenários e comportamentos externos, como falhas de rede ou respostas inesperadas da API, e verifique se o método `handle` lida corretamente com essas situações.
* **Legacy_stays - test_stays_puller.py**

  
  1. **Teste:** `test_pull_created_today`
     * **Descrição:** Este teste verifica se o método `pull_created_today` do `LegacyStaysPuller` está recuperando as reservas criadas hoje e passando-as para o manipulador de reservas.
     * **Risco mitigado:** Garante que as reservas criadas hoje são recuperadas corretamente, ajudando a manter os dados atualizados e precisos no sistema.
  2. **Teste:** `test_pull_future`
     * **Descrição:** Este teste verifica se o método `pull_future` do `LegacyStaysPuller` está recuperando as reservas futuras e passando-as para o manipulador de reservas.
     * **Risco mitigado:** Garante que as reservas futuras são recuperadas corretamente, permitindo ao sistema preparar-se para essas reservas com antecedência e garantir uma operação suave.

  **Sugestões:**

  
  1. **Teste de exceção para nenhum resultado:**
     * Verifique o comportamento quando não há reservas retornadas pelo método `get_stays_reservations_by_date_range`.
  2. **Teste de reserva inválida:**
     * Verifique o comportamento quando uma reserva inválida é retornada pelo método `get_stays_reservations_by_date_range`.
  3. **Teste de manipulador de reservas chamado corretamente:**
     * Verifique se o manipulador de reservas é chamado com os parâmetros corretos quando as reservas são recuperadas com sucesso.
  4. **Teste de chamada única ao método de API:**
     * Verifique se o método `get_stays_reservations_by_date_range` é chamado apenas uma vez durante a execução do método `pull_created_today` e `pull_future`.
  5. **Teste de argumentos passados para o método de API:**
     * Verifique se os argumentos passados para o método `get_stays_reservations_by_date_range` estão corretos, incluindo `date_from`, `date_to` e `date_type`.
  6. **Teste de manipulador de reservas chamado com reservas corretas:**
     * Verifique se o manipulador de reservas é chamado com as reservas corretas retornadas pelo método `get_stays_reservations_by_date_range`.
  7. **Teste de chamada ao método de manipulador de reservas:**
     * Verifique se o método do manipulador de reservas é chamado corretamente e se o retorno é tratado adequadamente.
* **Legacy_stays - test_stays_updater.py**

  
  1. **Teste:** `test_creation`

  **Descrição do teste:** Este teste verifica se a criação de uma reserva é feita corretamente pelo `LegacyStaysUpdater`. Ele simula a atualização de uma reserva no sistema, verificando se os dados são corretamente atribuídos à reserva criada.

  **Risco mitigado com esse teste:** Este teste ajuda a garantir que a função `update` do `LegacyStaysUpdater` esteja funcionando conforme o esperado. Garante que as reservas sejam corretamente criadas e que os dados sejam atribuídos corretamente, ajudando a evitar erros que possam surgir devido a problemas na criação ou atualização de reservas.

  
  1. **Teste:** `test_update`

  **Descrição do teste:** Este teste verifica se a atualização de uma reserva existente é feita corretamente pelo `LegacyStaysUpdater`. Ele simula a atualização de uma reserva no sistema, verificando se os dados são corretamente atribuídos à reserva existente.

  **Risco mitigado com esse teste:** Este teste ajuda a garantir que a função `update` do `LegacyStaysUpdater` esteja funcionando conforme o esperado. Garante que as reservas existentes sejam corretamente atualizadas com os novos dados fornecidos, ajudando a evitar erros que possam surgir devido a problemas na atualização de reservas.

  
  1. **Teste:** `test_invalid_update`

  **Descrição do teste:** Este teste verifica se uma exceção `InvalidStaysUpdate` é levantada corretamente quando uma tentativa é feita para atualizar uma reserva inválida. Ele simula o cenário em que uma reserva inválida é passada para o `LegacyStaysUpdater` para atualização e verifica se uma exceção é levantada conforme esperado.

  **Risco mitigado com esse teste:** Este teste ajuda a garantir que o `LegacyStaysUpdater` lida corretamente com casos em que uma reserva inválida é passada para atualização. Garante que o sistema se comporte conforme o esperado, levantando uma exceção adequada para impedir a atualização de reservas inválidas.

  
  1. **Teste:** `test_update_canceled`

  **Descrição do teste:** Este teste verifica se uma reserva é atualizada corretamente para o estado de "cancelada". Ele simula o cenário em que uma reserva de estadia é cancelada no sistema legado e verifica se a reserva correspondente no sistema local é atualizada com o status de "cancelada" após a atualização.

  **Risco mitigado com esse teste:** Este teste ajuda a garantir que o `LegacyStaysUpdater` lide corretamente com casos em que uma reserva de estadia é cancelada no sistema legado. Garante que a reserva local seja atualizada corretamente com o status de "cancelada" após a atualização, garantindo consistência entre os sistemas legado e local.

  **Sugestões:**

  
  1. **Testar atualização de reserva com reserva inexistente:**
     * Verifique se o sistema lida corretamente com a tentativa de atualização de uma reserva que não existe no sistema local.
  2. **Testar atualização de reserva com propriedade inexistente:**
     * Verifique se o sistema trata corretamente a tentativa de atualização de uma reserva com uma propriedade que não existe no sistema.
  3. **Testar atualização de reserva com usuário inexistente:**
     * Garanta que o sistema trate adequadamente a tentativa de atualização de uma reserva com um usuário que não está registrado no sistema.
  4. **Testar atualização de reserva com detalhes ausentes:**
     * Verifique se o sistema lida corretamente com a tentativa de atualização de uma reserva com detalhes ausentes, como data de check-in ou check-out.
  5. **Testar atualização de reserva com detalhes inválidos:**
     * Garanta que o sistema valide corretamente os detalhes da reserva durante a atualização e trate adequadamente os valores inválidos.
  6. **Testar atualização de reserva com diferentes tipos de OTA:**
     * Teste a atualização de reserva com diferentes tipos de OTA (Online Travel Agencies) para garantir que o sistema lide corretamente com as peculiaridades de cada OTA.
  7. **Testar atualização de reserva com diferentes tipos de dados de reserva:**
     * Verifique se o sistema trata corretamente diferentes tipos de reservas, como reservas de longo prazo, reservas de última hora, etc.
  8. **Testar atualização de reserva em diferentes cenários de disponibilidade de propriedade:**
     * Teste a atualização de reserva em diferentes cenários de disponibilidade de propriedade, como propriedade totalmente reservada, propriedade com disponibilidade limitada, etc.
  9. **Testar atualização de reserva com informações de hóspedes ausentes ou inválidas:**
     * Verifique se o sistema valida corretamente as informações dos hóspedes durante a atualização da reserva e trata adequadamente os casos de informações ausentes ou inválidas.

**Testes de integração**