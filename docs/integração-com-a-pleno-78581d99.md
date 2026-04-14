<!-- title: Integração com a Pleno | url: https://outline.seazone.com.br/doc/integracao-com-a-pleno-20FALPPwd4 | area: Tecnologia -->

# Integração com a Pleno

**API Pleno - Documentação:** <https://documenter.getpostman.com/view/7403048/UVXdPeYB>

No momento estamos utilizando as API's de Vistoria da Pleno. Toda chamada aos endpoints vai precisar de um token de autenticação.

### Adquirir Token de autenticação

```python
response = requests.post(
    url="https://api.sistemaspleno.com/api/vistoria/usuario/login",
    json={
        'usu_email': email,
        'usu_senha': password,
        'sis_codigo': "3",
        'host': "seazone.sistemaspleno.com"
    }
)
response.raise_for_status()
response_data = response.json()

if response_data["success"] is True:
	auth_token = response_data["data"]["auth_token"]
```

Para saber quais são os amenities de um imóvel devemos buscar os detalhes de vistoria do imóvel.

### Buscar detalhes de vistoria de um imóvel

```python
auth_token = ...

prop_code = "XYZ123"
response = requests.get(
    url=f"{self._base_url}/vistoria?term={prop_code}",
    headers={
        "Authorization": f"Basic {token}",
    }
)

response.raise_for_status()
vistoria = response.json()
vistoria_id = vistoria["data"][0]["vis_codigo"]

response = requests.get(
    url=f"{self._base_url}/vistoria/{vistoria_id}/show",
    headers={
        "Authorization": f"Basic {auth_token}",
    }
)

response.raise_for_status()
vistorial_detail = response.json()
```

### Entendendo o retorno da Pleno

Nos detalhes de vistoria temos o campo `ambientes` que contém todos os detalhes dos ambientes do imóvel.

Exemplo. A Pleno diz que o Imóvel X possui 9 ambientes:

* Sala
* Cozinha
* Quarto
* Suíte
* Banheiro
* Banheiro (Suíte)
* Área de serviço
* Churrasqueira
* Geral

Cada um desses ambientes terá um campo `ambientes_itens` que irá especificar todos os "itens" de determinado ambiente.

Exemplo:

* Sala
  * Possui sofa em bom estado
  * Pussi televisão
  * Etc
* Cama
  * Possui cama de casal em bom estado
  * Possui colchão em bom estado
  * Etc

Exemplo de como pegar as informações do retorno da Pleno.

```python
vistoria_details = ...

ambientes = []

for amb in vistoria_details["data"]["ambientes"]:
    amb_data = {
        "amb_referencia": amb["amb_referencia"],
        "tip_amb_descricao": amb["tipo_ambiente"]["tip_amb_descricao"],
        "ambientes_itens": [],
    }
    for amb_item in amb["ambientes_itens"]:
        amb_item_data = {
            "tip_amb_ite_descricao": amb_item["tipo_ambiente_item"]["tip_amb_ite_descricao"],
            "tip_est_descricao": amb_item["tipo_estado"]["tip_est_descricao"],
            "detalhe_descricao": [],
        }

        for detalhe_desc in amb_item["detalhe_descricao"]:
            amb_item_data["detalhe_descricao"].append(
                {
                    "tip_det_descricao": detalhe_desc["tipo_detalhe_descricao"]["tip_det_descricao"],
                    "tip_det_nome": detalhe_desc["tipo_detalhe"]["tip_det_nome"],
                }
            )

        amb_data["ambientes_itens"].append(amb_item_data)

    ambientes.append(amb_data)
```