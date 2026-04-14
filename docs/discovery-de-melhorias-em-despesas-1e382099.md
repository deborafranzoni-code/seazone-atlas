<!-- title: Discovery de Melhorias em Despesas | url: https://outline.seazone.com.br/doc/discovery-de-melhorias-em-despesas-XAaKnbN2v5 | area: Tecnologia -->

# Discovery de Melhorias em Despesas

## Contexto 

Este discovery foi conduzido com base em entrevistas e observações realizadas junto ao time de Franquias, em especial durante o acompanhamento do processo de lançamento de despesas com a Analista Financeira de Franquias, Isabella Bino.

## Objetivo 

Identificar e propor soluções para os principais desafios enfrentados pelo time operacional no processo de lançamento e aprovação de reembolsos, visando aumentar a eficiência e reduzir retrabalhos.


---

## Problemas Identificados e Propostas de Solução


1. **Falhas no Lançamento de Reembolsos** 

**Problemas:** 

* Ausência de solicitação de autorização do proprietário:
  * Atualmente, a regra exige que reembolsos acima de R$ 300 tenham aprovação do proprietário, mas esse campo não é solicitado na tela do anfitrião.
* Dificuldade em vincular reembolsos a danos:
  * Quando um reembolso está relacionado a um dano, o analista só tem acesso ao código do imóvel para verificar seu status (se já foi pago ou não). Isso demanda tempo, pois é necessário buscar manualmente todas as informações do imóvel.

**Propostas de Solução:** 

* Refatorar a tela de lançamento de reembolsos:
  * Tornar obrigatório o envio da aprovação do proprietário para reembolsos acima de R$ 300.
  * Incluir um campo para vincular o reembolso a um dano (depende da refatoração do sistema de lançamento de danos).
  * Implementar notificações (pop-up) para o anfitrião quando houver pendências em seus reembolsos, agilizando a correção das solicitações.
  * Incluir subitens ao escolher motivo da despesa, os subitens funcionarão de acordo com [este documento](https://docs.google.com/spreadsheets/d/1C2yuCk2V3IhcIrKpGgOnZ0SE46bh7MD9onJNGarVkSc/edit?gid=1045034745#gid=1045034745)


---


2. **Processo de Aprovação de Reembolsos Ineficiente** 

**Problemas:** 

* Múltiplas etapas de pré-aprovação:
  * O processo atual é burocrático e demanda muito tempo para conclusão.
* Falta de transparência no status de danos:
  * O analista não consegue visualizar diretamente o status do dano associado ao reembolso, precisando filtrar apenas pelo código do imóvel.
* Ausência de registro de motivos de negativa:
  * Não há um campo para justificar a reprovação ou cancelamento de uma despesa, gerando insatisfação nos anfitriões, que alegam falta de clareza nas decisões.

**Propostas de Solução:** 

* Refatorar a tela de análise de despesas:
  * Simplificar as etapas de pré-aprovação.
  * Incluir o código e o status do dano diretamente na tela (depende da refatoração do sistema de danos).
  * Adicionar um campo para registro dos motivos de reprovação ou cancelamento, aumentando a transparência para o anfitrião.
  * Incluir filtro por motivo de despesa

**Indicadores de eficiência:**

* Medir o **tempo médio de aprovação** (antes e depois das melhorias).
* Rastrear os **motivos mais comuns de reprovação** para identificar gaps no processo.

  \