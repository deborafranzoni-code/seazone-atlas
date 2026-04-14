<!-- title: Utils | url: https://outline.seazone.com.br/doc/utils-5m7dBALKVe | area: Tecnologia -->

# Utils

<aside> 👨🏻‍💻 Aqui estão algumas utilidade que facilitam realizar algumas ações durante o desenvolvimento das telas.

</aside>

**Sumário**


---

### JSON para descrever áreas de atuação


---

Agora temos um JSON no front onde descrevemos as areas de atuação, para utilizar basta importar as duas funções uma para os estados e outra para a cidade

 ![Untitled](/api/attachments.redirect?id=dd842375-4523-4a55-93e1-0f11896e767d)

*Ref: [PR 1819](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1819)*

## Função única de Logout


---

Outra adição importante é que agora temos uma função de logout unica, que adiciona alguns parametros no localStorage ao mesmo tempo que limpa outros, isso é importante para mantermos a consistencia da feature de limpar automaticamente os dados cada vez que a versão atualizar, ela se encontra em: `front/utils/logoutAndClearData.ts` e para usar basta importar a função.

*Ref: [PR 1819](https://github.com/Khanto-Tecnologia/sapron-pms-web/pull/1819)*