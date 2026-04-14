<!-- title: 6 Protótipo Viabilidade de uso, de construção e | url: https://outline.seazone.com.br/doc/6-prototipo-viabilidade-de-uso-de-construcao-e-86j1EQyvWW | area: Tecnologia -->

# 6 Protótipo Viabilidade de uso, de construção e

**Ideias que poderiam solucionar isso:**

[Protótipo em baixa](https://docs.google.com/spreadsheets/d/1cNTtPlapkK4Am85PkxoTFmPcetsG6ix4BIbbWVRd_Ys/edit?usp=sharing) com modelos aprovados

[FIGMA - V0](https://www.figma.com/file/41KHQO29gYoWbCkE8jThv3/Onboarding?type=design&node-id=306%3A1079&t=Az15xQfBXIXNIHTi-1)

[Protótipo V0 - Todos os modelos com rotas](https://drive.google.com/file/d/1UpOGupLuwMNXQ6bfQA7cIsMaXYLSab-f/view?usp=sharing)

**Lista de Proprietários (com opção de editar dados):**

Disponibilizar um grid 'Lista de proprietários' com os dados pessoais previamente inseridos, dando a opção e editar o Login e resetar a senha, através do link que direciona para a tela de Editar dados - Proprietário

**Lista de propriedades dinâmica:**

Disponibilizar um grid 'Lista de propriedades', como se fosse planilha, onde apareçam as etapas da implantação do imóvel atualizadas automaticamente. Além disso, a lista de propriedades deve conter a coluna de Listings, em que o onboarding possa verificar em quais plataformas os imóveis já estão ativos e o link de redirecionamento para a criação do listing que ainda não foi criado.

**Fluxo de implantação**

Disponibilizar o fluxo de implantação para proprietário e anfitrião, que é atualizado automaticamente através de dados provenientes do pipedrive, informando os detalhes da etapa em que o imóvel se encontra.

### **Solução ideal:**

### **a) TELA USUÁRIO ONBOARDING:**

* **Lista de proprietários:** o grid da lista de proprietários deverá ser acessado através da rota já existente **/proprietarios**  e deve conter as colunas que seguem abaixo. As colunas de integração estão sinalizadas na cor roxa. **Person Id :** Código do proprietário que redireciona ao pipedrive; **Nome :** Nome completo do proprietário **CPF/CNPJ :** Cpf ou cnpj cadastrado do proprietário **Telefone :** Telefone do proprietário com link direto para o WhatsApp **Quantidade de imóveis :**  Quantidade de imóveis que o proprietário possui **Endereço :**  Endereço do proprietário com a opção de copiar, **Login Sapron :** incluindo as colunas : **Email** : email de login no Sapron;  **Resetar a senha** : solicita ao suporte do slack a redefinição de senha do proprietário

 ![Onboarding - Lista de proprietários- Grid expandido.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Onboarding_-_Lista_de_proprietrios-_Grid_expandido.png)

**TELA USUÁRIO ONBOARDING e ANFITRIÃO:**

* **Lista de propriedades:** o grid da lista de proprietários deverá ser acessado através da rota já existente **/propriedades**  e deve conter as colunas que seguem abaixo. As colunas de integração estão sinalizadas na cor roxa. **Código do imóvel :** Código do imóvel gerado pelo Sapron **Status do imóvel :** Sinalizar se o imóvel está ativo ou inativo **Data inicial do contrato :**  Data da assinatura do contrato **Etapa do processo de implantação :** As etapas do processo de implantação devem ser atualizadas automaticamente através dos dados provenientes do pipedrive utilizando as datas em que os cards são movidos como finalizados. As etapas e subetapas para Casas e Apartamentos são as seguintes:

| Etapa | Sub-etapa finalizada | Sub-etapa pendente |
|----|----|----|
| Coleta das chaves | Chaves disponibilizadas em 23/05/23 |    |

Agendamento das chaves realizado em 23/05/23

Coleta das chaves realizada em 23/05/23  | Disponibilização das chaves pendente

Agendamento das chaves pendente

Coleta das chaves pendente | | Primeira visita ao imóvel | Coleta inicial de informações do imóvel realizada em 23/05/23 | Coleta inicial de informações do imóvel pendente | | Adequação | Relatório de adequação enviado em 23/05/23

Adequação finalizada em 23/05/23

Disponibilização realizada em 23/05/23 | Relatório de adequação pendente

Adequação pendente

Disponibilização pendente | | Anúncios | Anúncios criados em 23/05/23 | Criação de anúncios pendente | | Vistoria profissional | Vistoria agendada em 23/05/23

Vistoria recebida em 23/05/23

Vistoria assinada em 23/05/23 | Agendamento de vistoria pendente

Recebimento de vistoria pendente

Assinatura de vistoria pendente | | Fotos profissionais | Fotos agendadas em 23/05/23

Fotos recebidas em 23/05/23

Fotos adicionadas ao anúncios em 23/05/23 | Agendamento de fotos pendente

Recebimento de fotos pendente

Inclusão de fotos no anúncio pendente | | Processo de implantação finalizado! | Seu imóvel já está ativo!

**OBSERVAÇÃO**: esta etapa deve aparecer como finalizado quando todas as etapas anteriores forem encerradas. |  |

**OBSERVAÇÃO:** Para os imóveis que se enquadram na categoria de Quarto de hotel não será necessário a visualização da tela de acompanhamento do processo de implantação.

**Deal ID :** Código do proprietário que redireciona ao pipedrive; **Listing :** Deve apresentar as logos com os ícones das plataformas dos anúncios já criados. Ao clicar no botão deve aparecer um modal com um grid e os seguintes dados:

Origem da reserva, ID (da plataforma), Título e Taxa no rodapé do modal deve conter um botão que redirecione para a página "Novo Listing", para o caso de anúncios da propriedade que ainda não foram criados. Ao lado da linha de cada listing deve conter um botão de edição de dados que redireciona para a rota já existente de edição de listing.

As seguintes colunas devem ser expansíveis, conforma modelo no figma, para melhor usabilidade:

**Dados do proprietário : Nome e Telefone (com link direto para WhatsApp) Dados da propriedade: Anfitrião, Categoria do imóvel, Localização, Tipo, Endereço, Taxa de limpeza; Comodidades: Camas total, Camas casal, Camas solteiro, Camas king, Camas queen, Sofá cama individual, Sofás cama duplo, Quartos, Banheiros total, Banheiros, Lavatório, Capacidade.**  A coluna de comodidades deve conter um botão redirecionando para a página de "Editar propriedade", caso haja divergências que necessitam de correção pelo time do onboarding. \*\*Taxas e comissões: Taxa de adesão, Valor pago de entrada, Forma de pagamento da taxa, Comissão, Plano, Forma de pagamento.

OBSERVAÇÃO:\*\* A sessão de taxas e comissões não deve aparecer para a role host

 ![Lista de propriedades - Modo visualização](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Onboarding_-_Lista_de_propriedades_-_Grid_expandido.png)

Lista de propriedades - Modo visualização

 ![Lista de propriedades - Colunas expandidas](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Onboarding_-_Lista_de_propriedades_-_Grid_completo.png)

Lista de propriedades - Colunas expandidas

 ![Modal de visualização dos listings ativos](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Onboarding_-_Lista_de_propriedades_-_Listings.png)

Modal de visualização dos listings ativos

\*\*b) TELA PROPRIETÁRIO:

Etapa do processo de implantação :\*\* As etapas do processo de implantação devem ser atualizadas automaticamente através dos dados provenientes do pipefy utilizando as datas em que os cards são movidos como finalizados. As etapas e subetapas para Casas e Apartamentos são as mencionadas na [tabela](/doc/6-prototipo-viabilidade-de-uso-de-construcao-e-W6KvmHMBL8) referenciada acima.

Os imóveis que estão na categoria de Quarto de hotel não terão acompanhamento do processo de implantação.

**CONSIDERAÇÕES PARA AS SOLUÇÕES APRESENTADAS**

O fluxo das etapas de implantação dos imóveis deve aparecer através do botão 'Visualizar imóvel' As colunas de status de locação deve conter o texto 'Processo de implantação' e receita deve conter o texto 'Aguardando dados'. O botão de 'Extrato' deve estar desabilitado.

**SE** o imóvel estiver ativo, porém ainda esteja em processo de implantação o mesmo será sinalizado com um ícone ao lado da coluna de de status de locação, com uma tag indicando que o imóvel ainda encontra-se em processo de implantação.

Para as etapas do processo de implantação que contenham duas ou mais etapas, deve ser implementada a seguinte lógica: Aparece somente a etapa vigente (quando concluída) e a etapa posterior sinalizada como pendente: Deve aparecer somente duas etapas para visualização nestes casos.

 ![Tela inicial proprietário, imóvel inativo](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Proprietrio_-_Imvel_em_implantao.png)

Tela inicial proprietário, imóvel inativo

 ![Tela inicial proprietário, imóvel ativo porém ainda em processo de implantação](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Proprietrio_-_Imvel_disp_porem_em_implantao.png)

Tela inicial proprietário, imóvel ativo porém ainda em processo de implantação

 ![Visualização mobile](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Proprietrio_-_Processo_de_implantao_-_Casas_e_apartamentos.png)

Visualização mobile

 ![Visualização das etapas que possuem mais de três sub-etapas](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Desktop_-_Casas_e_apartamentos.png)

Visualização das etapas que possuem mais de três sub-etapas

**CONSIDERAÇÕES PARA AS SOLUÇÕES APRESENTADAS**


1. Para a visualização do processo de implantação, as barras de carregamento das etapas devem ser 'preenchidas' de acordo com as sub-etapas finalizadas.
2. A última etapa do processo deve aparecer como finalizada somente quando as etapas e subetapas anteriores forem concluídas. Quando a última etapa for finalizada a tela de visualização do processo de onboarding deve ficar disponível após 30 dias apenas.
3. Para etapas que possuem 2 ou 3 sub-etapas deve aparecer somente a etapa concluída e a etapa posterior como 'pendente'. Se todas as sub-etapas estiverem pendentes, deve aparecer somente uma sub-etapa, sinalizada como pendente, e o círculo de carregamento, assim como o ícone deve estar sinalizado na cor cinza, indicando que aquela etapa não está em andamento
4. Para a versão mobile, o processo deverá ser acompanhado através de uma barra de carregamento horizontal que segue a mesma lógica de conclusão de etapas e sub-etapas.
5. Todas as variações de texto para etapas concluídas e pendentes encontram-se detalhadas na imagem abaixo, assim como os círculos e barra de carregamento
6. \

 ![Componentes.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Componentes.png)

### Solução backend

**Usuário Onboarding - Lista de proprietários**

 ![Onboarding - Lista de proprietários- Grid expandido(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Onboarding_-_Lista_de_proprietrios-_Grid_expandido(1).png)

GET `owners`

| PERSON ID | user.pipedrive_person_id |
|----|----|
| CPF/CNPJ | user.cpf |
| Endereço | user.main_adress |
| Telefone | user.phone_number1 |

Observação: quando clicado no botão do WhatsApp deve seguir o seguinte formato de url wa.me/${phone_number1} | | Login sapron

Email

Botão de resetar a senha |

user.email

Abertura de chamado no slack para alteração de senha |

**Usuário Onboarding e Anfitrião - Lista de propriedades**

 ![Captura de tela de 2023-06-13 14-19-33.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Captura_de_tela_de_2023-06-13_14-19-33.png)

| Etapa do processo de implementação | GET API a ser desenvolvida, de acordo com o esquema abaixo. Deve ser atualizado a partir da tabela `progresso_implantação` , considerando que todas as etapas iniciam como default false, e que só alteram para true caso todas as sub-etapas estejam finalizadas (setadas como true) | | --- | --- | | Deal_id | GET `property/handover_details pipedrive_deal_id` | | Listing | GET `listings` |

 ![Captura de tela de 2023-06-13 14-19-48.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Captura_de_tela_de_2023-06-13_14-19-48.png)

GET `property/categorylocation`

| Categoria | `category` |
|----|----|
| Localização | `location` |
| Tipo | GET `properties/details/{id}` |

`property_type` |

 ![Captura de tela de 2023-06-13 14-20-07.png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Captura_de_tela_de_2023-06-13_14-20-07.png)

GET `property/handover_details`

| Taxa de adesão | `setup_value` |
|----|----|
| Valor Pago de entrada |    |
| Forma de pagamento da taxa |    |
| Comissão |    |
| Plano | `plan` |
| Forma de pagamento | `payment_method` |

### Modal conferência de listings

 ![Modal de visualização dos listings ativos](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Onboarding_-_Lista_de_propriedades_-_Listings.png)

Modal de visualização dos listings ativos

| GET listings/{id} |    |
|----|----|
| OTA | `ota` |
| ID | `id_in_ota` |
| Título | `title_in_ota` |
| Taxa | `ota_fee` |

### Página proprietário

 ![Tela inicial proprietário, imóvel inativo](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Proprietrio_-_Imvel_em_implantao.png)

Tela inicial proprietário, imóvel inativo

GET properties/owner

| Processo de implantação | `property_condition`: valor onboarding deve vir como 'Processo de implantação' |
|----|----|
|    |    |
|    |    |

### Processo de implantação

 ![Desktop - Casas e apartamentos(1).png](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Desktop_-_Casas_e_apartamentos(1).png)

Para setar as etapas do processo de implantação, bem como as sub-etapas, deve ser criado uma API que será alimentada pelo pipefy. Na primeira tabela temos os progressos de implantação, que são as etapas gerais. Os valores devem vir como `default false` e devem mudar somente para `true`, quando todas as sub-etapas ligadas aquela chave forem marcadas como finalizadas (`true`). Além disso, para cada sub-etapa, devemos armazenar a data em que o card daquela etapa foi finalizado, possibilitando assim que os usuários envolvidos tenham visibilidade das datas em que ocorreram o processo.

Enquanto as sub-etapas estiverem marcadas como `false` devemos considerar que ela está pendente.

 ![Untitled.svg](6%20Proto%CC%81tipo%20Viabilidade%20de%20uso,%20de%20construc%CC%A7a%CC%83o%20e%20d9b7dc30d4e14ddc8d63e63967fce325/Untitled.svg)