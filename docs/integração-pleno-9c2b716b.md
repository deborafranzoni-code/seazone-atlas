<!-- title: Integração Pleno | url: https://outline.seazone.com.br/doc/integracao-pleno-9mc7RmZGQy | area: Tecnologia -->

# Integração Pleno

A integração foi separada em algumas atividades baseado nas nossas necessidades e como a API da Pleno se comporta atualmente (20/05/25), então a documentação estará separado por atividade realizada, apontando seu endpoint, parâmetros e ações que são feitas.


## Tabelas

### `property_inspection`


1. property: Chave estrangeira pra `property_property`;
2. pleno_inspection_id (int): serve pra economizar uma requisição na hora de atualizar uma vistoria.

### `amenity_item`


1. pleno_item_id (int): Identificador do item na Pleno;
2. pleno_item_name (str): Nome do item na Pleno;
3. pleno_item_environment (str): Ambiente do item na Pleno;
4. item_name (str): Texto exibido dentro do Sapron, por padrão é o mesmo que pleno_item_name;
5. stays_item_id (str): Identificador do item na Stays. É alfanumérico e pode ser nulo por que ainda não começamos esse lado da integração;
6. stays_item_name (str): Nome do item na Stays, pode ser nulo pelo mesmo motivo;
7. stays_section (str): Nome da seção/acordeão do item na Stays, pode ser nulo pelo mesmo motivo;
8. is_address_item (bool): Se o item é uma comodidade de Endereço. Caso contrário, quer dizer que é de Anúncio. Por padrão é falso;
9. status (TextChoice): Se a comodidade deve ser retornada pro front do Sapron ou não. Valores aceitos: Active_Amenity | Inactive_Amenity.

### `property_inspection_amenity_items`


1. inspection: Chave estrangeira pra `property_inspection`;
2. item: Chave estrangeira pra `amenity_item`


## Ações

### Atualizar uma vistoria

Endpoint: POST `/channel_manager/pleno/sync/inspection`, body precisa de `property_code`

Descrição: Permite puxar as informações da vistoria de um imóvel a partir da Identificação (termo utilizado na Pleno, na api é `term`).

Validações:


1. Caso a vistoria da propriedade não exista na Pleno: Erro 404, vistoria não encontrada
2. Caso a vistoria exista, mas a propriedade ainda não exista no Sapron: Erro 424, propriedade não foi criada


---

### Atualizar todas as vistorias (Entrada)

Endpoint: POST `/channel_manager/pleno/task/sync_all_inspection`

Descrição: Permite puxar todas as vistorias com `tipoVistoria` 1032 (id interno da Pleno para "Entrada"). Na data de escrita, temos entorno de 500+ vistorias, então essa tarefa demora uns bons minutos e faz pelo menos 500 requisições. **Esse endpoint cria uma task assíncrona, não faça múltiplas chamadas**


---

### Atualizar vistorias por período

Endpoint: POST `/channel_manager/pleno/task/sync_inspections_from_period`, body precisa de `period_from` e `period_to`, onde:

* Ambos tem formato `YYYY-mm-dd`;
* `period_from` é obrigatório, `period_to` não, e por padrão é a data de hoje

Descrição: Permite puxar todas as vistorias feitas entre as datas inseridas. **Essa lógica é aplicada para uma tarefa diária que processa as vistorias dos últimos 7 dias durante a madrugada**. Foi feito por quê nem sempre a vistoria é feita antes do imóvel ter Onboarding no sistema, então puxar ela automaticamente durante a troca de dia adianta essa etapa.

Validações:


1. `period_to` é menor do que `period_from`: Erro 400, bad request


---

### Retornar itens presentes na vistoria

Endpoint: GET `/property/inspection/`

Descrição: Retorna um dicionário pra vistoria da propriedade requisitada com o formato:

```python
                  {
                      pleno_item_environment (str): {
                          "address": {
                              "amenities": [
                                  {"item_name": str, "is_present": bool},
                                  ...
                              ]
                          },
                          "listing": {
                              "amenities": [
                                  {"item_name": str, "is_present": bool},
                                  ...
                              ]
                          }
                      }
                  }
```

Validações:


1. Propriedade não tem vistoria sincronizada no Sapron: Erro 404, vistoria não encontrada


---

## Processamento de uma vistoria

O processamento é feito da mesma forma, independente se estamos atualizando uma única vistoria ou em grupo. Caso estejamos atualizando em grupo, o processamento é feito dentro de um loop, uma vistoria por vez.


O processo segue:


1. Buscamos na tabela `property_inspection` pela instância da vistoria da propriedade selecionada pra ver se existe `pleno_inspection_id`. Se não existe, cria a instância e armazena o dado.

   
   1. Caso a instância já exista, nós chamamos o método `.save()` nela pra engatilhar a atualização do campo `updated_at`, que vai ser entregue pro front exibir a data de última atualização.
2. Fazemos a chamada na API da pleno a partir do `pleno_inspection_id`

   
   1. seazone.sistemaspleno.com/vistoria/`inspection_id`/show
3. Verificamos os dados do obj `ambientes` que vem da resposta da pleno, extraindo os itens e salvando apenas aqueles que não são duplicatas usando a regra de unicidade com os seguintes campos juntos :

   
   1. is_address_item
   2. pleno_item_id
   3. pleno_environment

      
      1. Desse modo, é possível ter dois itens com o mesmo nome no ambiente "Geral", sendo um do endereço e outro do imóvel.

OBS: Sempre que fazemos busca de Propriedades, buscamos por status `Active` e `Onboarding` apenas.

OBS2: Sempre que fazemos busca de Itens/Amenities/Comodidades, buscamos apenas por status `Active_Amenity`