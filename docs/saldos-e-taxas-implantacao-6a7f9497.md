<!-- title: Saldos e Taxas Implantação | url: https://outline.seazone.com.br/doc/saldos-e-taxas-implantacao-J24PIbbQie | area: Administrativo Financeiro -->

# Saldos e Taxas Implantação

![](Saldos%20e%20Taxas%20Implantac%CC%A7a%CC%83o%2007d21f3fc84c4d8e844aa0c047792b6b/FUNDOS_TRELLO_2_(1).png)

⛔

# Saldos e Taxas Implantação


\
**DESCRIÇÃO**

ℹ️

Saldos Iniciais são valores positivos ou negativos que devem ser considerados no Fechamento do Imóvel. Podem se tratar do abatimento da Taxa de Implantação ou do valor de um ajuste manual ou de despesa que não foram pagas no fechamento anterior, perdurando pelos próximos meses.\n\nTaxa de Implantação é o valor cobrados do proprietário pela padronização do imóvel de acordo com os moldes Seazone.\n


**PRAZO**

⏰

Os Saldos devem ser atualizados na **primeira semana pós fechamento e** as Taxas de Implantação dos novos imóveis devem ser atualizadas **uma vez por semana (durante o fechamento semanal).**


**ORDEM DE PRIORIDADE PARA DESCONTO**

⚠️

Se o valor de Saldo Inicial for **negativo e** o valor para repasse continuar sendo **negativo,** porém o valor para repasse for **menor** que o Saldo Inicial e o imóvel possuir mais de 1 tipo de saldo na [Conciliação Futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) (em caso de despesa, ajuste ou taxa de implantação), deve-se **atualizar** esse novo valor **subtraindo** dos saldos que o imóvel tiver, priorizando a ordem de:\n\n1.\n**Despesas:** Subtrair primeiro o valor da despesa ou até mesmo excluí-la, caso o imóvel tenha abatido todo o valor da despesa;\n2.\n**Ajustes:** Caso o imóvel tenha saldo de despesa e ajuste; ou ajuste e taxa, e o valor abatido for superior ao valor da despesa, deve-se diminuir o restante do valor no saldo do ajuste ou até mesmo excluí-lo, caso o imóvel tenha abatido todo o valor do ajuste. (Verificar o tipo de ajuste para saber se deve descontar primeiro do ajuste ou primeiro da taxa de implantação);\n3.\n**Taxa de Implantação:** Caso o imóvel tenha saldo de despesa, ajuste e taxa; despesa e taxa; ou ajuste e taxa; e o valor abatido for superior aos valores dos outros saldos já excluídos, deve-se diminuir o restante do valor na taxa de implantação ou até mesmo excluí-la, caso o imóvel tenha abatido todo o valor da taxa.



1. **Processo de atualização de Saldos**

* **Passo a passo (PLANO A)**

  **Regra Geral:**\n1. Após o pós fechamento, devemos acessar a planilha\n[3.0 BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) , em qualquer aba, e rodar a Macro Fechamento → Finalização Fechamento → **Conciliação futura**;

  
  2. Acessar a planilha **[Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550),** na aba "**Saldos em conta props**", filtrar pela data do fechamento do mês de referencia e verificar se os dados entraram corretamente.
* **Passo a passo (PLANO B)**

  **Regra Geral:**

  
   1. Acessar a planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba "Saldos em conta props";
   2. Copiar e colar, **sem a data**, todos os saldos com a data de referência do fechamento anterior (mês passado) para própria planilha nas colunas logo abaixo;
   3. Após copiar todas as informações, deve-se atualizar a data de referência do fechamento para a data do mês atual;
   4. Em seguida, excluir todos os casos de [Churn](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=1593897658) referente ao mês anterior;
   5. Imóveis inativos por situações peculiares (que não são churn e nem onboarding) devem ser mantidos na [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550);
   6. Trocar "Taxa de implantação - entrada" por "Taxa de implantação" na coluna F (Comentário) dos imóveis que foram copiados e colados do mês anterior e não dos que vieram com a macro Tx Implantação *(analisar passo a passo do "__[Processo de Inserir novas Taxas de Implantação](/doc/saldos-e-taxas-implantacao-J24PIbbQie)__" em caso de dúvidas)*;
   7. Selecionar o filtro direto e filtrar a coluna A (Mês) pelo mês de referência do fechamento atual;
   8. Após essa seleção, **utilizando o mesmo filtro**, clicar em classificar de A → Z no filtro da coluna B para ordenar os imóveis por ordem alfabética, facilitando qualquer outra comparação entre planilhas;
   9. Acessar o drive de [Histórico Fechamentos](https://drive.google.com/drive/folders/1csgpu2PaB15XOvTuvXcdmBszo-l5xM2z), buscar pelo ano atual e abrir a planilha do BizOps referente ao mês de fechamento anterior;
  10. Acessar a aba Imóvel na planilha do BizOps e verificar os imóveis, um por um, **mesmo que tenham valor de Saldo Inicial ou não**. Ou seja, comparar as colunas **Saldo Inicial Seazone** com as colunas **Valor para Repasse** e **Saldo Atualizado Seazone** (sendo esse último apenas para uma dupla segurança).
  11. Caso o valor de Saldo Inicial seja **divergente** do valor para repasse, analisar:

  a. Se o valor de Saldo Inicial for **zero ou positivo**, mas o valor para repasse for negativo, **inserir** esse novo valor para repasse como **Saldo Inicial Seazone** na [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) levando em consideração a **data do mês de referência atual**;

  b. Se o valor de Saldo Inicial for **negativo**, mas o valor para repasse for positivo (acima de zero), **excluir** esse imóvel da [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) levando em consideração a **data do mês de referência atual;**

  c. Se o valor de Saldo Inicial for **negativo e** o valor para repasse continuar sendo negativo porém diferentes, **atualizar** esse novo valor para repasse como **Saldo Inicial Seazone** na [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) levando em consideração a **data do mês de referência atual.**

  \
  **Observação 1:** *Para saber se é uma despesa ou um ajuste verificar as colunas Q (despesas) e X (ajustes) na aba Imóvel da planilha do BizOps.*

  **Observação 2:** *Sempre verificar se a diferença do Saldo Inicial é uma despesa ou ajuste na planilha do BizOps (aba imóvel). Se for o caso*, *adicionar o comentário correto na coluna F (Comentário) na planilha de Conciliação futura e colocar o valor na coluna D (Saldo Inicial Seazone).*

  **Observação 3:** *Sempre que se tratar de uma despesa ou ajuste, deve ser adicionada uma linha a mais com o comentário correto e o valor deve constar na coluna D (Saldo Inicial Seazone).*

  \
  
  12. Caso o valor de Saldo Inicial seja igual ao valor para repasse, mantém-se o que está no ponto 2.

  \


\

2. **Processo de atualização Taxas de Implantação Parceladas**

* **Passo a passo**

  
  1. Seguir todos os pontos da Regra Geral acima até o ponto 7;
  2. Em caso de parcelamento de taxa de implantação, todas as parcelas já estarão descritas na Conciliação futura do mês, sendo assim, deve-se analisar:

  a. Caso o imóvel t**enha abatido todo o** **valor da parcela**, deve-se excluir a linha que foi copiada do mês anterior (desse imóvel) e manter apenas a linha da parcela do mês de referência;

  b. Caso o imóvel **não tenha abatido nada do valor da parcela**, deve-se manter todas as linhas (a do mês de referência atual + as linhas das parcelas atrasadas atualizando o comentário "Parcela Atrasada m");

  c. Caso o imóvel **tenha abatido** **apenas uma parte do valor da parcela**, deve-se adicionar o novo valor da diferença no lugar do valor da parcela atrasada \[**sempre na(s) parcela(s) mais antigas**\] e manter a linha do mês de referência atual.



3. **Processo de Inserir novas Taxas de Implantação**

* **Passo a passo (Semanal)**

  
  1. Acessar a planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba de [Saldos em conta props](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550);
  2. Clicar na macro Tx Implantação Atual (botão azul) que fica localizada na coluna E \[Saldo Onboarding (Taxa Implantação)\], para puxar as novas taxas de implantação automaticamente da aba [Handover Comercial → Onboarding](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289) da planilha [00 - Banco de Dados PMS](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289).

  \
* **Passo a passo (Mensal)**

  
  1. Acessar a planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba de [Saldos em conta props](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550);
  2. Excluir os dados do mês de referencia ( que foram trazidos pela macro rodada durante o fechamento semanal)
  3. Clicar na macro Tx Implantação Anterior (botão azul) que fica localizada na coluna E \[Saldo Onboarding (Taxa Implantação)\], para puxar as novas taxas de implantação automaticamente da aba [Handover Comercial → Onboarding](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289) da planilha [00 - Banco de Dados PMS](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289).



4. **Processo de atualização do Controle Financeiro das Taxas de Implantação (Pós fechamento)**

* **Passo a passo**

  
  1. Após a rodagem das macros no fechamento, deve-se acessar a planilha do [3.0 BizOps](https://docs.google.com/spreadsheets/d/1o216mX4uUnUAwFhUi3pfFtTdg2wlSEmo6Eh08gdTu50/edit#gid=1073825828) (em qualquer aba), clicar no cabeçalho da planilha em "Fechamento" → "Finalização Fechamento" e rodar a macro "Abatimento Taxa Implantação";
  2. Após terminar de rodar o script, abrir a planilha [Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047) na aba ["REC_IMPLANTAÇÃO"](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047) e verificar se todos os dados foram enviados para as colunas T (Imóvel), U (Valor), V (Recebimento) e W (Forma de Pgto) com a data do mês seguinte a data do mês que está na aba [Dashboard](https://docs.google.com/spreadsheets/d/1Tkf29uV4ZFZcbvjofAo_9IHVPri9XY5JlTBE3Pcu-jo/edit#gid=1308026923) da planilha do BizOps.



5. **Processo de atualização Repasses Segurados (proprietários que tem valor de repasse, mas não receberam por algum motivo)**

* **Passo a passo**

  
  1. Perguntar para o Financeiro *(Malice)* "se algum proprietário deixou de receber no mês;
  2. Caso aja algum repasse segurado, deve se acessar a planilha [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=936983766), na aba de ''Repasse segurado'', adicionando todas as informações da coluna A até a coluna J, deve-se manter a coluna ''E'' com a flag de ''não'' e a coluna ''F'' com a flag de ''mantido'' selecionado;
  3. Após deve-se acessar a planilha [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=936983766), na aba ''Saldos em conta props'' e adicionar o imovel que possui o repasse segurado com valor e descrição correta no mês de referencia;
  4. Caso o imovel que possuia repasse segurado tenha recebido seu repasse, deve-se acessar a planilha [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=936983766), na aba de ''Repasse segurado'', e atualizar a coluna E para ''sim'' e a coluna F ''ok'' (Assim que for finalizado o passo 5);
  5. Após atualizar a aba de repasse segurado nos casos de repasse feito, deve-se acessar a planilha [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=936983766), na aba ''Saldos em conta props'' e excluir o(s) imovel(s) do mes de referencia.

  \
  **Observação 1:** *Sempre atualizar as colunas E (comentário), F (explicação sheets), G (explicação Sapron) e H (se foi repassado) de acordo com o ocorrido.*

  \



6. **Processo de alteração no modelo de Abatimento de Taxa de Implantação**

* **Passo a passo**

  
  1. Em casos específicos onde se é solicitado para que a taxa de implantação seja alterada de "à vista" para abatimento parcelado, deve-se observar, seguindo o que foi informado e solicitado pelo **time de CS.**

  a. Em quantas vezes será parcelado e qual o mês da primeira parcela;

  b. Se o valor será distribuído de forma integral (sem considerar caso tenha tido algum abatimento no valor antes) ou a diferença (caso tenha que considerar o que já foi abatido), entre as parcelas;

  c. Se será necessário excluir algum ajuste ou valor do [Sapron](https://sapron.com.br/fechamentoimovel).

  
  2. Deve-se adicionar os ajustes no [Sapron](https://sapron.com.br/fechamentoimovel) observando as regras do passo 1, ou seja, em quais meses deverá ser adicionado esses ajustes, e qual o valor desses ajustes.
  3. Na planilha da [Conciliação Futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba "[Saldos em contas props](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550)", deve-se excluir as linhas de taxa de implantação desse imóvel nos meses anteriores e adicionar as novas também observando as regras do passo 1, adicionando nos meses corretos e com os valores informados pelo **time de CS***.*


\

\