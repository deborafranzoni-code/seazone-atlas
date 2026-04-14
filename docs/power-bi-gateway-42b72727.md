<!-- title: Power Bi Gateway | url: https://outline.seazone.com.br/doc/power-bi-gateway-YU5OgK7n6f | area: Tecnologia -->

# Power Bi Gateway

## Cluster de Gateway de dados para o Power BI instalado.


A configuração do cluster do gateway de dados esta configurado em duas instâncias ec2 na conta seazone-technology. A documentação para configurar o gateway e o cluster está neste [link](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-install). Como cada configuração é única e possui um hash não é possível 


## Gateways Images

Como não é possível reiniciar a máquina com alguma automação em caso de falhas, a solução foi criar imagens configuradas com o gateway e somente inicializar as novas instâncias com as imagens quando necessário. As imagens são:

| Image | Gateway | Ami Id |
|----|----|----|
| khanto-bi-gateway-0 | Khanto Bi Gateway Cluster 2 | [ami-0243522699ff97199](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#ImageDetails:imageId=ami-0243522699ff97199) |
| Khanto-Bi-Gateway-Cluster | Khanto Bi Gateway Cluster | [ami-0883901fbfe4bba08](https://us-west-2.console.aws.amazon.com/ec2/home?region=us-west-2#ImageDetails:imageId=ami-0883901fbfe4bba08) |

## Security groups

As máquinas do cluster possuem dois security groups, um majoritariamente para dar acesso as aplicações e outro para os acessos pessoais. Em caso de alteração de bancos ou datasource é muito importante que o novo endereço seja registrado no security groups sg-0b7636f2211c5f0e9.


## Configurando Data Sources

Para configurar os data sources basta [acessar](https://www.notion.so/Acessos-Vault-69c195e6a2ff4c65a914e16401db6042 https://vault.sapron.com.br/ui/vault/secrets/secret/show/governanca/password_powerBI_instances) a máquina e abrir o odbc:


 ![](/api/attachments.redirect?id=1cd26ea4-bd99-4e0a-89b3-504f85d006ac)

Acessando "System Dsn" no menu você pode visualizar todas as configurações que a máquina do gateway possui. Nesta tela você pode adicionar, remover e editar o dsn conforme necessário.


 ![](/api/attachments.redirect?id=d88d84d0-c64c-454a-b8f8-5e82620037d6)

Em caso de dúvidas em relação ao usuário que esta sendo utilizado na autenticação vocẽ pode visualizar o usuário clicando na dns desejada e abrindo a opção "Authentication Options". 

 ![](/api/attachments.redirect?id=06c8673a-2b0b-48a7-81f1-9a47419daf15)


:::info
Os usuários utilizados para configurar estas dsns estão no vault na aba database, porém para os usuários da aws, caso seja necessário você pode criar uma nova chave.

:::


## Configuração da Nekt


Acessar à máquina que está rodando o gateway e:

* Atualizar o PowerBI para a versão mais recente;
* Atualizar o On-Premises Data Gateway para a versão mais recente;
* Baixar e instalar o driver Amazon Athena ODBC 2.x;
* Baixar o conector da Nekt (**nekt.mez**) e salvar na pasta 

  ```javascript
  [Documents]\Power BI Desktop\Custom Connectors
  ```

   (ou similar, é preciso ver qual pasta a versão do PowerBI que estão rodando no gateway);
* Abrir o Power BI nessa máquina e nas configurações de Data Extensions permitir o uso de conectores externos;


Depois disso, será necessário configurar o On-premises data gateway em si.

**Configurando o On-Premises Data Gateway**O primeiro passo é identificar qual o nome usuário o data gateway está usando na máquina Windows. O usuário padrão é 

```javascript
NT SERVICE\PBIEgwService
```

Para confirmar que usuário você está usando, basta abrir o On-Premises Data Gateway e navegar para o menu de 

```javascript
Service Settings
```

.Nesse exemplo de screenshot que estou enviando, ele deixa explicito o usuário ali no final, dizendo:

```javascript
The gateway is currently running as NT SERVICE\PBIEgwService.
```

 ![](/api/attachments.redirect?id=fe195f43-bb1a-4e7b-aa0f-09febcd49a58)

O próximo passo é dar acesso para esse usuário do On-Premises Data Gateway poder executar o conector.

Você deverá fazer isso assim:

* Abrir a pasta onde estão salvos os conectores customizados utilizados pelo gateway;
* Clicar com o botão direito e clicar em `Properties`
* Ir para a aba `Security` (no exemplo abaixo, você vai notar que na seção `Group or user names` já existe o usuário `PBIEgwService`, mas no seu gate provavelmente esse usuário não estará nessa lista), e clicar em `Edit`
* Uma nova janela irá abrir chamada `Permissions for Custom Connectores`, nessa janela, clicar em `Add` para adicionar um novo usuário.
* Na seção `Enter the object names to select`, digitar `NT SERVICE\PBIEgwService` (ou o nome do seu usuário do gateway) e clicar em Check Names. Se o usuário for válido, ele irá substituir somente pela segunda parte do usuário `PBIEgwService` e ficará com um sublinhado, indicando que o Windows localizou esse usuário. Clicar em OK
* Você voltará para a tela anterior, onde pode atribuir os direitos que esse usuário tem nessa pasta. Conceder os direitos de `Read & execute`, `List folder contents`, `Read`, e clicar em `OK` para finalizar o processo.

[Screen Recording 2024-10-14 at 16.05.18 (1).mov 1080x910](/api/attachments.redirect?id=4f27bb09-e3a6-4611-b1a5-cd579b9a4b78)

Uma vez concedido essas permissões, você deve voltar ao app do On-Premisses Data Gateway, dessa vez no menu `Connectors`

 e definir a pasta onde estão seus conectores customizados. No exemplo abaixo, o conector da Nekt já aparece listado na parte superior, mas acredito que no seu gateway ainda não aparecerá nessa etapa.Se for esse o caso, por favor abre o menu `Service Settings`

 e reinicia o gateway. Volte para o menu `Connectors` e confirme se o conector da Nekt aparece na lista.

 ![](/api/attachments.redirect?id=31c4183a-84a7-4300-b3e1-e1215ca22fdd)

 ![](/api/attachments.redirect?id=cc0bcc00-f741-4105-b596-7e9b3434d2df)


 ![](/api/attachments.redirect?id=e2fb2b0c-4b2d-4212-b16c-d507cc3dfee6)