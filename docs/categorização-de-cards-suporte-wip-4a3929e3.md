<!-- title: Categorização de cards - suporte - WIP | url: https://outline.seazone.com.br/doc/categorizacao-de-cards-suporte-wip-STP4kUKFnN | area: Tecnologia -->

# Categorização de cards - suporte - WIP

***==Opções disponíveis no formulário atual==***

### Setor - *Preenchido pelo usuário*

*     "Atendimento - Anfitriões",
*     "Atendimento - Hóspedes",
*     "Atendimento - Proprietário",
*     "Fechamento",
*     "Financeiro",
*     "Franquias",
*     "Tecnologia/RM",
*     "Sou proprietário",
*     "Outros"


### **Tipo de Solicitação -** *Preenchido pelo usuário (categorias)*

*     "Acessos - Problema com login e senha",
*     "Ajuste em dados bancários",
*     "Alteração de comissão",
*     "Calendário (bloqueio e extensão de reservas)",
*     "Envio de reservas - hotel",
*     "Erros no sistema",
*     "Indicação de parceiros",
*     "Nota fiscal eletrônica",
*     "Outros (página de proprietário)",
*     "Outros (página de anfitrião)",
*     "Preciso tirar uma dúvida",
*     "Problemas com dados e informações",
*     "Solicitações administrativas e ajustes",
*     "Solicitação de melhorias"


### **Origem do Problema - *Preenchido após avaliação PM***

*     "Falso positivo",
*     "Erro de Processo",
*     "Dados inconsistentes",
*     "Sugestão de melhoria/Ajuste",
*     "Bug no Sapron",
*     "Falha de Rede",
*     "Pedido operacional",
*     "Outros",
*     =="Sou um proprietário" ? perguntar==


\
### **Perfis do usuário**:

* Proprietário
* Anfitrião
* Parceiro
* Fechamento
* Atendimento


### Categoria Principal *(PM - Preenchido na avaliação)*

Após um card passar para a etapa de Priorização, deve ser definido a sua **Categoria Principal** que podem ser as seguintes opções:

* **Bug no Sapron**
  * bug na regra de negocio ou front/back
* **Dados inconsistentes**
  * dados errados seja por ajuste de dados ou sincronização
* **Pedido operacional**
  * Quando alguma funcionalidade ainda não esta no sapron e precisa ser feito manualmente
* **Sugestão de melhoria/Ajuste**
  * Quando uma funcionalidade existente no sapron precisa de uma melhoria ou 
  * Quando precisa desenvolver uma funcionalidade (nestes casos vai ao board do time como backlog e segue o processo normal de desenvolvimento)


* **Erro de Processo**
  * Quando não foi seguido o fluxo de alguma funcionalidade e precisa de ajusteis operacionais
* **Falso positivo**
* **Falha de Rede**
* **Outros**


### Sub Categorias - WIP - *Dividido conforme os tipos de usuario*

O objetivo das *sub-categorias* é identificar os tipos de suporte sejam bug, dados ou operacional. Com esses dados será possível ter uma visão ampla sobre o tipo de suporte que é recorrente.

 

**LOGIN/ACESSO**

* login


**PROPIEDADE / IMOVEL**

* migracion-propiedade ()

  \

**FECHAMENTO**

* financeiro
* fechamento-financeiro
  * ajuste-dados
  * ajuste-calculo-valores [pipefy-card](https://app.pipefy.com/open-cards/1029969055)


* comissão
  * mudança de comissões 

  \

**SAPRON**

* sync-sapron-stays
  * Reservas criadas em imóveis diferentes [pipefy-card](https://app.pipefy.com/open-cards/1031054204)
* sync-bloqueio-sapron-stays
  * bloqueio na sapron que não esta na stays pipefy-card


* files-aws
  * png não visibel [pipefy](https://app.pipefy.com/open-cards/1020626097)

  \

**RESERVAS**

* categoria-imovel
  * no salva categoria
* migracao-reservas
  * reservas que precisam mudar 

  \

**OPERACIONAL**

* migrar-reservas
* migrar-imoveis


BUG SAPRON

SalvarDadosnoBanco