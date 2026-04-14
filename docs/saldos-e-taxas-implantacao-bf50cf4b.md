<!-- title: Saldos e Taxas Implantação✅ | url: https://outline.seazone.com.br/doc/saldos-e-taxas-implantacao-pHm06BGAg4 | area: Administrativo Financeiro -->

# Saldos e Taxas Implantação✅

![](../../Saldos%20e%20Taxas%20Implantac%CC%A7a%CC%83o%2007d21f3fc84c4d8e844aa0c047792b6b/FUNDOS_TRELLO_2_(1).png)

⛔

# Saldos e Taxas Implantação✅


\
**Descrição**


Saldos Iniciais são valores positivos ou negativos que devem ser considerados no Fechamento do Imóvel. Podem se tratar do abatimento da Taxa de Implantação ou do valor de um ajuste manual e despesa que não foram pagas no fechamento anterior, perdurando pelos próximos meses.


Taxa de Implantação é o valor cobrados do proprietário pela padronização do imóvel de acordo com os moldes Seazone.


**Prazos**


Os Saldos devem ser atualizados na **primeira semana pós fechamento e** as Taxas de Implantação dos novos imóveis devem ser atualizadas **uma vez por semana (durante o fechamento semanal).**


**Ordem de prioridade para desconto no Fechamento**

Se o valor de Saldo Inicial for **negativo e** o valor para repasse continuar sendo **negativo,** porém o valor para repasse for **menor** que o Saldo Inicial e o imóvel possuir mais de 1 tipo de saldo na [Conciliação Futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) (em caso de despesa, ajuste ou taxa de implantação), deve-se **atualizar** esse novo valor **subtraindo** dos saldos que o imóvel tiver, priorizando a ordem de:



1. **Despesas:** Subtrair primeiro o valor da despesa ou até mesmo excluí-la, caso o imóvel tenha abatido todo o valor da despesa;
2. **Ajustes:** Caso o imóvel tenha saldo de despesa e ajuste; ou ajuste e taxa, e o valor abatido for superior ao valor da despesa, deve-se diminuir o restante do valor no saldo do ajuste ou até mesmo excluí-lo, caso o imóvel tenha abatido todo o valor do ajuste. (Verificar o tipo de ajuste para saber se deve descontar primeiro do ajuste ou primeiro da taxa de implantação);
3. **Taxa de Implantação:** Caso o imóvel tenha saldo de despesa, ajuste e taxa; despesa e taxa; ou ajuste e taxa; e o valor abatido for superior aos valores dos outros saldos já excluídos, deve-se diminuir o restante do valor na taxa de implantação ou até mesmo excluí-la, caso o imóvel tenha abatido todo o valor da taxa.



1. **Processo de atualização de Saldos**

* **Passo a passo (PLANO A) -** **MACRO QUE SERÁ TESTADA**
* **Passo a passo (PLANO B)**

  **Regra Geral:**

  
   1. Acessar a planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba "Saldos em conta props";
   2. Copiar e colar, **sem a data**, todos os saldos com a data de referência do fechamento anterior (mês passado) para própria planilha nas colunas logo abaixo;
   3. Após copiar todas as informações, deve-se atualizar a data de referência do fechamento para a data do mês atual;
   4. Em seguida, excluir todos os casos de [Churn](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=1593897658) referente ao mês anterior;
   5. Imóveis inativos por situações peculiares (que não são churn e nem onboarding) devem ser mantidos na [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550);
   6. Trocar "Taxa de implantação - entrada" por "Taxa de implantação" na coluna F (Comentário) dos imóveis que foram copiados e colados do mês anterior e não dos que vieram com a macro Tx Implantação *(analisar passo a passo do "__[Processo de Inserir novas Taxas de Implantação](/doc/saldos-e-taxas-implantacao-pHm06BGAg4)__" em caso de dúvidas)*;
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
* **Passo a passo (PLANO C) -** **Fechamento Mensal Template**

  
  1. Seguir todos os passos do **PLANO B**, com exceção ao:

  a. **Passo 9** que, neste caso, deve-se acessar o a planilha do [Fechamento Mensal Template](https://docs.google.com/spreadsheets/d/1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0/edit#gid=1073825828);

  b. **Passo 10** que, neste caso, deve-se acessar a aba [Imóvel](https://docs.google.com/spreadsheets/d/1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0/edit#gid=1073825828) na planilha do [Fechamento Mensal Template](https://docs.google.com/spreadsheets/d/1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0/edit#gid=1073825828) e verificar os imóveis, um por um, **mesmo que tenham valor de Saldo Inicial ou não**. Ou seja, comparar a coluna **E** (**Saldo Inicial Seazone)** com as colunas **AA (Valor para Repasse)** e **AB (Saldo Atualizado Seazone),** (sendo esse último apenas para uma dupla segurança).



2. **Processo de atualização Taxas de Implantação Parceladas**

* **Passo a passo**

  
  1. Seguir todos os pontos da Regra Geral acima até o ponto 7;
  2. Em caso de parcelamento de taxa de implantação, todas as parcelas já estarão descritas na Conciliação futura do mês, sendo assim, deve-se analisar:

  a. Caso o imóvel t**enha abatido todo o** **valor da parcela**, deve-se excluir a linha que foi copiada do mês anterior (desse imóvel) e manter apenas a linha da parcela do mês de referência;

  b. Caso o imóvel **não tenha abatido nada do valor da parcela**, deve-se manter todas as linhas (a do mês de referência atual + as linhas das parcelas atrasadas atualizando o comentário "Parcela Atrasada m");

  c. Caso o imóvel **tenha abatido** **apenas uma parte do valor da parcela**, deve-se adicionar o novo valor da diferença no lugar do valor da parcela atrasada \[**sempre na(s) parcela(s) mais antigas**\] e manter a linha do mês de referência atual.



3. **Processo de Inserir novas Taxas de Implantação**

* **Passo a passo**

  
  1. Acessar a planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550) na aba de [Saldos em conta props](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550);
  2. Clicar na macro Tx Implantação (botão azul) que fica localizada na coluna E \[Saldo Onboarding (Taxa Implantação)\], para puxar as novas taxas de implantação automaticamente da aba [Handover Comercial → Onboarding](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289) da planilha [00 - Banco de Dados PMS](https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=228443289);
  3. Verificar se os sinais vieram corretos (com sinal negativo) e se todos os valores estão aparecendo (todos os valores diferente de zero);
  4. Em seguida, deve-se acessar o [Sapron](https://sapron.com.br/login), e verificar se todos os imóveis puxados pela macro Tx Implantação estão com o saldo inicial corretamente, sendo assim:

  a. Caso não estejam, é necessário **adicionar um ajuste direto com o valor do saldo da taxa apresentado na** **[Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=1400643550)**;

  b. Caso estejam com um valor de saldo inicial, mas o valor se encontra incorreto, é necessário i**nvestigar o que ocorreu antes de realizar qualquer correção ou ajuste**;

  c. Caso estejam corretos, apenas desconsiderar e ser feliz 🙂.

  \
  **Observação:** *todo dia 31 é necessário apagar o que foi realizado no fechamento semanal, pois dia 1, a macro irá atualizar sozinha.*



4. **Processo de atualização do Controle Financeiro das Taxas de Implantação**

* **Passo a passo**

  
  1. Após a rodagem das macros no fechamento, deve-se acessar a planilha do [BizOps](https://docs.google.com/spreadsheets/d/1Tkf29uV4ZFZcbvjofAo_9IHVPri9XY5JlTBE3Pcu-jo/edit#gid=1308026923) (em qualquer aba), clicar no cabeçalho da planilha em "Fechamento" → "Finalização Fechamento" e rodar a macro "Abatimento Taxa Implantação";
  2. Após terminar de rodar o script, abrir a planilha [Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047) na aba ["REC_IMPLANTAÇÃO"](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047) e verificar se todos os dados foram enviados para as colunas T (Imóvel), U (Valor), V (Recebimento) e W (Forma de Pgto) com a data do mês seguinte a data do mês que está na aba [Dashboard](https://docs.google.com/spreadsheets/d/1Tkf29uV4ZFZcbvjofAo_9IHVPri9XY5JlTBE3Pcu-jo/edit#gid=1308026923) da planilha do BizOps.



5. **Processo de atualização Repasses Segurados (proprietários que tem valor de repasse, mas não receberam por algum motivo)**

* **Passo a passo**

  
  1. Perguntar para o Financeiro *(confirmar o melhor membro para isso)* "se algum proprietário deixou de receber no mês;
  2. Acessar a aba Taxas de Implantação na planilha [Controle CRC](https://docs.google.com/spreadsheets/d/1Q1dV4hkJqfKABiPMsYXY5sLYVVq8l1NyBBediuWqApE/edit#gid=822640047) da Seazone Serviços e analisar:

  a. Caso o valor de repasse segurado se mantenha, ou seja, se o proprietário continuar optando por não receber mas não teve repasse no mês atual, deve-se copiar e colar na aba [Repasses Segurados](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=330946870) na planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=330946870) numa linha abaixo o valor anterior;

  b. Caso o valor de repasse se acumule com o atual, ou seja, se o proprietário continuar optando por não receber mas o valor mude, deve-se copiar e colar na aba [Repasses Segurados](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=330946870) na planilha de [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=330946870) numa linha abaixo o valor atualizado;

  c. Caso o valor seja repassado, ou seja, se o proprietário recebeu, deve-se excluir a linha na [Conciliação futura](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=330946870) do mês de referência e **NÃO** adicionar uma nova linha na aba de [Repasses Segurados](https://docs.google.com/spreadsheets/d/1k3fqGBd5bgsGYaRUywe69aa7qWPD22IzV_1XMwuIODA/edit#gid=330946870).

  \
  **Observação 1:** *Sempre atualizar as colunas E (comentário), F (explicação sheets), G (explicação Sapron) e H (se foi repassado) de acordo com o ocorrido.*



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