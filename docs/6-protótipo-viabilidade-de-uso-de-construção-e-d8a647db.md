<!-- title: 6 Protótipo Viabilidade de uso, de construção e | url: https://outline.seazone.com.br/doc/6-prototipo-viabilidade-de-uso-de-construcao-e-RopgVAfdpK | area: Tecnologia -->

# 6 Protótipo Viabilidade de uso, de construção e

**Ideias que poderiam solucionar isso:**

[FIGMA](https://www.figma.com/file/XoX6pEzowIRtdHHtFuebsg/Pr%C3%A9-check-in?type=design&node-id=510%3A419&t=QT3aVIqgl5y39jdd-1)

### **a) TELA ATENDIMENTO, ROTA COMPLETAR RESERVA:**

* A coluna de pré check-in deve conter o ícone de 'sininho' conforme modelo abaixo.
* Ao clicar no ícone deve abrir um modal com as seguintes informações:

**Pré check-in** : `header`: Título do modal **X :** `button` : Botão de fechar Grid com as seguintes colunas: **Imóvel** : indica o imóvel da reserva **Dono da reserva** : indica o nome da pessoa que será enviado o link **Check-in**: indica a data de check-in da reserva

**Gerar token para enviar ao hóspede :** `label button` : deve ser seguido de um ícone botão de copiar que gera o link para envio ao hóspede **Link de pré check-in enviado :** `label radio button` : deve ser acompanhado de um radio button que indique se o link foi enviado **Salvar :** `button` : Botão que permite salvar a informação de que o link foi enviado ao hóspede. O botão deve estar desabilitado enquanto não for selecionado o `radio button` **Link de pré check-in enviado**

**OBSERVAÇÂO:** Para imóveis que se enquadram no tipo 'Hotel' deverá aparecer a seguinte mensagem no modal:

Atenção: O arranjo de camas desta reserva deve ser inserido manualmente na tela de Completar dados da reserva.

Ao clicar no botão de salvar, se o check-box for marcado, o ícone de 'sininho' da coluna de pré check-in deve ser alterado para a cor azul, com a seguinte mensagem:

**Pré check-in enviado** : `tooltip`

Quando o hóspede inserir todos os dados e enviar o formulário, o ícone de 'sininho' da coluna de pré check-in deve ser alterado para a cor verde, com a seguinte mensagem:

**Pré check-in preenchido** : `tooltip`

Os dados enviados através do link de pré check-in devem ser disponibilizados na coluna de editar dados da reserva desta mesma rota, permitindo ao time de atendimento a edição de dados caso o hóspede altere os dados da reserva, bem como o envio do voucher para o hotel para imóveis que se caracterizem como tal.

 ![Frame 1927.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1927.png)

 ![Frame 1928.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1928.png)

 ![Frame 1928(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1928(1).png)

### b) TELA PRÉ CHECK-IN

A tela de pré check-in diferencia-se entre imóveis que se configuram como 'hotel' && 'casas' || 'apartamentos':

SE o imóvel da reserva for do tipo 'hotel' é obrigatório o preenchimento da quantidade de hóspedes, organização das camas e TODOS os dados do hóspede principal, segundo descrição abaixo.

SE o imóvel da reserva for do tipo 'casa' ou 'apartamento' é obrigatório o preenchimento da quantidade de hóspedes, pet, TODOS os dados do hóspede principal e preenchimento dos TODOS os dados dos hóspedes secundários, segundo descrição abaixo.

**Sessão 1**

**Faça seu pré check-in** : `header` com o seguinte texto abaixo:

Bem-vindo(a)! O pré check-in é o primeiro passo para uma experiência excepcional! Confirme os dados abaixo para facilitar o seu check-in. Estamos ansiosos para recebê-lo(a)!

\*\*Sessão 2

Código do imóvel :\*\* ex: ILC4213 **Endereço do imóvel :**  ex:  Av. dos Búzios, 170, Jurerê Internacional, Florianópolis-SC **Datas de check-in e check-out:** ex: 01/12/2023 - 12/03/2025 **Capacidade máxima de hóspedes:** ex: Até 5 hóspedes

**Sessão 3** **Hóspedes** : `header`

**Adicionar hóspede** : `button` : quando clicado adiciona os hóspedes secundários, de acordo com a capacidade máxima do imóvel.

**Sessão 4 - Hotel Hóspede principal** : `header` : deve vir como default **Os dados a seguir são obrigatórios!** : `<p**>` Nome completo\*\*\* : `input texto` **CPF**\* : `input number`

**Email**\* : `input texto` **Telefone**\* : `input número`

**Enviar foto do seu documento** : `label` : acompanhada do botão de adicionar o documento **Adicionar dados**  : `button` : botão que adiciona os dados do hóspede

**OBSERVAÇÃO:** Para imóveis de são do tipo 'hotel' não é obrigatório o preenchimento dos dados dos acompanhantes.

Ao final da página deve conter:

**Concluir** : `button` : deve ficar habilitado somente se o hóspede preencheu todos os dados obrigatórios do hóspede principal

\*\*Sessão 4 - Casas e apartamentos

Hóspede principal\*\* : `header` : deve vir como default **Os dados a seguir são obrigatórios!** : `<p**>` Nome completo\*\*\* : `input texto` **CPF**\* : `input number` **Email (opicional)** : `input texto` **Telefone**\* : `input número` **Vai levar pet?** : `radio button` com as opções Sim e Não, seguido da seguinte mensagem: *Esta solicitação está sujeita a disponibilidade e deve ser aprovada pelo atendimento. Consulte valores extras de cobrança.* **Enviar foto do seu documento** : `label` : acompanhada do botão de adicionar o documento **ATENÇÃO: o anfitrião entrará em contato caso necessite da placa do veículo** **Adicionar dados**  : `button` : botão que adiciona os dados do hóspede

**OBSERVAÇÃO:** Para imóveis de são do tipo 'casas' ou 'apartamentos' é obrigatório o preenchimento dos dados dos acompanhantes.

Ao final da página deve conter:

**Concluir** : `button` : deve ficar habilitado somente se o hóspede preencheu todos os dados obrigatórios do hóspede principal e os dados obrigatórios dos acompanhantes.

**CONSIDERAÇÕES**


1. Ao lado do header do hóspede secundário deverá aparecer um ícone de lixeira permitindo a exclusão do hóspede. Ao clicar no botão deve aparecer em um novo modal inferior a seguinte mensagem: *Tem certeza que deseja remover o hóspede?* **Sim** : `button` **Não** : `button`

SE o hóspede selecionar a opção sim, deve aparecer a seguinte mensagem de sucesso:

**Hóspede removido com sucesso**


2. Ao clicar no botão de 'Adicionar dados' deve aparecer a seguinte mensagem de sucesso:

**Hóspede adicionado com sucesso**


3. Ao clicar no botão de 'Concluir' deve abrir um modal com a seguinte mensagem:

Dados enviados com sucesso!

Agradecemos por enviar os seus dados! Se precisar atualizar a sua reserva, entre em contato com o atendimento!

 ![Pré check-in Hotel](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/fase_1.png)

Pré check-in Hotel

 ![Pré check-in imóveis residenciais](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Imveis_residenciais.png)

Pré check-in imóveis residenciais

### c) TELA ANFITRIÃO, ROTA CONTROLE, CARD DE CHECK-IN

A integração do pré check-in na página do anfitrião deve ser realizada no card de check-in na rota de controle conforme modelo especificado abaixo.

**Caso 1** : Atendimento enviou o link do pré check-in, porém o hóspede ainda não preencheu os dados

Abaixo do 'Número do documento' deve conter uma tag com a seguinte mensagem:

**Hóspede recebeu o link de pré check-in no dia 11/01/23 mas não preencheu os dados** **Gere o link clicando no botão de pré check-in abaixo**

Abaixo da mensagem deve conter:

**Gerar link** : `button` : botão que gera o link com o tokem para ser encaminhado ao hóspede. Após o clique deve aparecer uma mensagem de sucesso contendo o seguinte texto:

**O link para o pré check-in foi gerado com sucesso, e copiado para área de transferência.**

 ![Frame 1929.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1929.png)

**Caso 2** : Hóspede preencheu o pré check-in enviado pelo atendimento

Abaixo do 'Número do documento' deve conter uma tag com a seguinte mensagem:

**O hóspede preencheu os dados do pré check-in no dia 23/01/23. Clique no botão abaixo para visualizar ou editar dados**

Abaixo da mensagem deve conter:

**Visualizar dados** : `button` : botão que abre os dados preenchidos pelo hóspede

Ao clicar na página de visualização deve abrir um modal com as seguintes informações:

**x** : `button` : botão que fecha a página de dados da reserva e retorna para o card de pré check-in

 ![Frame 1930.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1930.png)

**Caso 3** : O atendimento não enviou o link de pré check-in

Abaixo do 'Número do documento' deve conter uma tag com a seguinte mensagem:

**O Atendimento não enviou o link de pré check-in** **Gere o link clicando no botão de pré check-in abaixo**

Abaixo da mensagem deve conter:

**Gerar link** : `button` : botão que gera o link com o tokem para ser encaminhado ao hóspede. Após o clique deve aparecer uma mensagem de sucesso contendo o seguinte texto:

**O link para o pré check-in foi gerado com sucesso, e copiado para área de transferência.**

 ![Frame 1926.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1926.png)

Página de visualização de dados do pré check-in:

**Dados da reserva** : `header`

\*\*Sessão 1

Código do imóvel :\*\* ex: ILC4213 **Endereço do imóvel :**  ex:  Av. dos Búzios, 170, Jurerê Internacional, Florianópolis-SC **Datas de check-in e check-out:** ex: 01/12/2023 - 12/03/2025 **Capacidade máxima de hóspedes:** ex: Até 5 hóspedes

\*\*Sessão 2

Hóspedes :\*\* `header` : ao lado do header deve conter um botão de copiar dados que deve copiar para área de transferência todos os dados inseridos no pré check-in; botão de editar dados que possibilita o anfitrião realizar alteções nos dados da reserva.

**Hóspede principal :** `header` **Nome completo:** traz a informação preenchida pelo hóspede, campo desabilitado para edição

**CPF:** traz a informação preenchida pelo hóspede, campo desabilitado para edição

**Email** : traz a informação preenchida pelo hóspede, campo desabilitado para edição

**Telefone** : traz a informação preenchida pelo hóspede, campo desabilitado para edição **Vai levar pet?** : traz a informação preenchida pelo hóspede, campo desabilitado para edição

**Foto do documento** : miniatura da foto do documento do hóspede. Quando clicado sobre a miniatura deve ser possível baixar a imagem

Para os acompanhantes a visualização de dados deve ocorrer da mesma forma.

Caso o anfitrião clique no botão de editar dados, deve abrir a mesma página com os dados mencionados acima, porém com os inputs abertos para edição.

Ao final da página deve conter:

**Atualizar dados** : `button` : quando o usuário clica nesse botão deve aparecer a seguinte mensagem de sucesso:

**Dados atualizados com sucesso**

 ![Modo visualização de dados de pré check-in](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Visualizar_dados_da_reserva.png)

Modo visualização de dados de pré check-in

 ![Modo edição de dados do pré check-in](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Editar_dados_da_reserva.png)

Modo edição de dados do pré check-in

 ![Mensagem de sucesso aparece ao clicar em 'Atualizar dados'](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Visualizar_dados_da_reserva(1).png)

Mensagem de sucesso aparece ao clicar em 'Atualizar dados'

### Feature - Incluir botão no formulário de Pré check-in (front) (in-progress)

No formulário de pré check-in deve conter um botão 'Você já conhece o site de reservas da Seazone?', conforme modelo abaixo que redirecione para o website de reservas. Os botões devem conter tag de rastreamento do GTM.

 ![fase 1(2).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/fase_1(2).png)

 ![Frame 1935(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1935(1).png)

## Solução Backend

Completar reservas - Atendimento

Modal de confirmação de envio:

 ![Frame 1925.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1925.png)

**GET** `calendar/reservations/{id}`

| **Imóvel** | listing.propertycode |
|----|----|
| **Dono da reserva** | guest.userfirst_name && guest.user.last_name |
| **Check-in** | check_in_date |
| **Botão gerar token** | **POST** `precheckin/generatelink` |

Copia o link para área de transferência | | **Radio button selecionado && Salvar** | **POST** `precheckin/admin/`

`is_pre_checkin_link_sent : true` `link_sent_at: 2023-06-11T11:59:48.293Z` | | **Cancelar** | Fecha o modal, nenhuma informação é alterada |

Troca de cores do sino da coluna de pré check-in:

 ![Frame 1928.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1928%201.png)

GET `precheckin/admin/` **SE** `is_pre_checkin_link_sent : true`

Sino do pré check-in fica azul, mensagem tooltip "Pré Chek-in enviado'

 ![Frame 1928(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Frame_1928(1)%201.png)

GET `precheckin/admin/`

**SE** `is_pre_checkin_completed: true,` Sino do pré check-in fica verde, mensagem tooltip "Pré Chek-in preenchido'

### Tela Pré check-in

 ![fase 1(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/fase_1(1).png)

GET `precheckin`

| Código da unidade | property.code |
|----|----|
| Endereço | address.street |
| address.number |    |
| address.neighborhood |    |
| address.city |    |
| address.state |    |
| Datas de check-in e check-out | check_in_date |
| check_out_date |    |
| Capacidade de hóspedes | property.guest_capacity |
| Ver localização no mapa | Pegar os dados do endereço e fazer a manipulação dentro da url do google maps para redirecionamento da página que abre em uma nova aba. |

Após correto preenchimento de todos os dados obrigatórios (de acordo com as especificações de quarto de hotel e imóveis residenciais) deve ocorrer o seguinte comportamento após clicar no botão de concluir:

Todos os dados pessoais:

POST `reservation_guests`

{"id": `number`, "reservation": `number`, "name": `string`,

"document": `string`,


"email": `string`, "phone_number": `string`, "document_photo": {"uid": `string`, "category":"`document`", "name": `string`,

"url": `string`,

"size": `number`,

"content_type":`"image/png"`}, "is_principal": `boolean`}

Arranjo de camas, quantidade de hóspedes e informação de pet:

PATCH `precheckin`

{ "id": `number`, "adult_guest_quantity": `number`, "child_guest_quantity": `number`, "has_pet": `number`, "bed_arrangement":`"Double_Bed"`, need_cradle": `boolean`, "is_pre_checkin_completed": `true`, "pre_checkin_fullfilled_at": `"2023-06-11T11:57:51.223Z"` }

### Tela anfitrião card check-in

 ![Group 1925.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Group_1925.png)

GET `precheckin` **SE**

`is_pre_checkin_link_sent :false`

| Botão de gerar link | **POST** `precheckin/generatelink`

Copia o link para área de transferência

**POST** `precheckin/admin/`

`is_pre_checkin_link_sent : true` `link_sent_at: 2023-06-11T11:59:48.293Z` | | --- | --- |

 ![Group 1925(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Group_1925(1).png)

GET `precheckin`

**SE** `is_pre_checkin_link_sent : true`

| Hóspede recebeu o link de pré check-in no dia {`link_sent_at`} mas não preencheu os dados | `link_sent_at: 2023-06-11T11:59:48.293Z` |
|----|----|
| Botão de gerar link | **POST** `precheckin/generatelink` |

Copia o link para área de transferência

**PATCH** `precheckin/admin/`

`is_pre_checkin_link_sent : true` `link_sent_at: 2023-06-11T11:59:48.293Z` |

**OBSERVAÇÃO:** Caso a chave `link_sent_at` já esteja guardando uma data de envio, o valor dessa chave deve ser sobrescrito

 ![Group 1925(2).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Group_1925(2).png)

GET `precheckin`

**SE** `is_pre_checkin_completed: true,`

| O hóspede preencheu os dados do pré check-in no dia {`pre_checkin_fullfilled_at`} | `pre_checkin_fullfilled_at: 2023-06-11T11:59:48.293Z` |
|----|----|
| Botão de visualizar dados | Abre a tela de visuzalização de dados |

### Tela de visualização de dados

 ![Visualizar dados da reserva(2).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Visualizar_dados_da_reserva(2).png)

GET `precheckin`

| Código da unidade | property.code |
|----|----|
| Endereço | address.street |
| address.number |    |
| address.neighborhood |    |
| address.city |    |
| address.state |    |
| Datas de check-in e check-out | check_in_date |
| check_out_date |    |
| Capacidade de hóspedes | property.guest_capacity |

Na sessão de dados de hóspede:

| Botão de copiar | Copia todos os dados preenchidos, exceto foto de documento, que deve ser possível salvar logo após clicar sobre a imagem do documento. |
|----|----|

Todos os dados pessoais:

GET `reservation_guests`

{"id": `number`, "reservation": `number`, "name": `string`,

"document": `string`,


"email": `string`, "phone_number": `string`, "document_photo": {"uid": `string`, "category":"`document`", "name": `string`,

"url": `string`,

"size": `number`,

"content_type":`"image/png"`}, "is_principal": `boolean`}

Arranjo de camas, quantidade de hóspedes e informação de pet:

GET `precheckin`

{ "id": `number`, "adult_guest_quantity": `number`, "child_guest_quantity": `number`, "has_pet": `number`, "bed_arrangement":`"Double_Bed"`, need_cradle": `boolean`, "is_pre_checkin_completed": `true`, "pre_checkin_fullfilled_at": `"2023-06-11T11:57:51.223Z"` }

### Tela edição de dados de pré checkin

 ![Editar dados da reserva(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20eb3294016a7e4b9591218894271eec5b/Editar_dados_da_reserva(1).png)

GET `precheckin`

| Código da unidade | property.code |
|----|----|
| Endereço | address.street |
| address.number |    |
| address.neighborhood |    |
| address.city |    |
| address.state |    |
| Datas de check-in e check-out | check_in_date |
| check_out_date |    |
| Capacidade de hóspedes | property.guest_capacity |

Na sessão de dados de hóspede:

| Botão de editar dados | Abre a tela e edição de dados |
|----|----|
| Botão de atualizar dados | Todas as chaves abaixo devem ser enviadas no método patch |

Todos os dados pessoais:

PATCH `reservation_guests`

{"id": `number`, "reservation": `number`, "name": `string`,

"document": `string`,


"email": `string`, "phone_number": `string`, "document_photo": {"uid": `string`, "category":"`document`", "name": `string`,

"url": `string`,

"size": `number`,

"content_type":`"image/png"`}, "is_principal": `boolean`}

Arranjo de camas, quantidade de hóspedes e informação de pet:

PATCH `precheckin`

{ "id": `number`, "adult_guest_quantity": `number`, "child_guest_quantity": `number`, "has_pet": `number`, "bed_arrangement":`"Double_Bed"`, need_cradle": `boolean`, "is_pre_checkin_completed": `true`, "pre_checkin_fullfilled_at": `"2023-06-11T11:57:51.223Z"` }