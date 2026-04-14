<!-- title: Atualização Compilado ✅ | url: https://outline.seazone.com.br/doc/atualizacao-compilado-cRag57kdPR | area: Administrativo Financeiro -->

# Atualização Compilado ✅

![](../../Atualizac%CC%A7a%CC%83o%20Compilado%202c4004b4c72c41cf8c59c6c9c3171286/FUNDOS_TRELLO_1.png)

🕵🏻‍♂️

# Atualização Compilado ✅\n\n


**Descrição**


Ao final de cada fechamento o setor deve alimentar uma planilha que compila os dados de cada mês para fins de consulta futura.


\
**Prazo**

\nAté o dia 15 de cada mês\n


\
**Fluxograma do Processo**


*Passo a Passo*

\[

https://lucid.app/lucidchart/6c6d95db-8874-406c-8824-97b270b90e23/edit?page=6MV-HVPSOX9\~&invitationId=inv_571afb2b-a5c2-4dda-b86d-7b60a25a668a#

\](https://lucid.app/lucidchart/6c6d95db-8874-406c-8824-97b270b90e23/edit?page=6MV-HVPSOX9\~&invitationId=inv_571afb2b-a5c2-4dda-b86d-7b60a25a668a#)


\
**Processo Atualização da Aba Imóvel**


* Acessar a Aba Imóvel da Planilha Compilado Fechamento

[Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit#gid=0)


* A fórmula utilizada deve ser colocada na primeira célula livre da coluna B: =IMPORTRANGE("1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0";"Imovel!A3:AB")\n\n
* Depois de importar os dados, selecione todos (ctrl C) e cole somente os valores (Ctrl + Shift + V)


* Preencha a coluna A com o mês de referência do Fechamento (Ex: 03/2023)


\
**Processo Atualização da Aba Anfitrião**


* Acessar a Aba Anfitrião da Planilha Compilado Fechamento

[Compilado Fechamentos](https://docs.google.com/spreadsheets/d/1HDgd7eOk1P23zwJyzAGqR5k5cWDN4jd2kJZ87RXFi0c/edit#gid=1257400142)


* A fórmula utilizada deve ser colocada na primeira célula livre da coluna B: =IMPORTRANGE("1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0"; "'Resumo Anfitrião'!A2:Y")


* Depois de importar os dados, selecionar todos eles (ctrl C) e colar somente os valores (ctrl + Shift + V).


* Selecionar células adicionadas na coluna S clicando com o botão direito, e inserir células para deslocar para a direita a comissão da adequação.


* Preencher a coluna A com o mês de ref do fechamento (Ex: 03/2023)


\
**Processo Atualização Modelo de Exportação Anfitriões**


* Acessar a Planilha Fechamento Mensal Template

[Fechamento Mensal Template](https://docs.google.com/spreadsheets/d/1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0/edit)


* No menu superior do fechamento (onde tem as macros para gerar os PDFs) rodar a macro "Gerar modelo de exportação do anfitrião".


* Verificar as flags nas colunas AC e AD na aba Anfitriões do template do fechamento para encontrar divergências de limpezas/receitas em cada imóvel e arrumar na aba modelo exportação comparando com a conciliação (Aba conciliação/fechamento).


* Para as migrações talvez seja necessário alterar o anfitrião na aba de modelo de exportação da planilha do fechamento.


* Flag de Limpeza (copiar todas as limpezas da aba limpezas mês com a data do dia 01, colar e olhar as flags de duplicidade). Se ainda sobrarem Falsas, olhar individualmente\nFlag de comissão olhar individualmente\n


* Fórmula utilizada na primeira célula da coluna A livre

=IMPORTRANGE("1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0";"'Modelo de Exportação - Anfitriões'!A3:O")


* Depois de importar os dados, selecionar todos eles com (ctrl C) e colar somente os valores (ctrl + alt + v).


\

**Processo Atualização Modelo de Exportação Proprietários**


* Acessar a Planilha Fechamento Mensal Template

[Fechamento Mensal Template](https://docs.google.com/spreadsheets/d/1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0/edit)


* No menu superior do fechamento (onde tem as macros para gerar os PDFs) rodar a macro "Gerar modelo de exportação".\n\n
* Verificar as flags nas colunas AK e AL na aba Imóvel da Planilha Fechamento Mensal Template para encontrar divergências de comissão e receitas em cada imóvel


* Acessar a aba Conciliação/Fechamento da Conciliação referente ao mês para sanar as divergências (lembrar tirar o filtro)

[Histórico Conciliações](https://drive.google.com/drive/folders/1mu85gM6wVMPDCONGN8UWMBhydJo45tAp)


* Fórmula utilizada na primeira célula da coluna A livre

=query(IMPORTRANGE("1UoGdsSrhNuyeTupWzP3tgg1mKUF81X8Ac6rwspoTRD0";"'Modelo de Exportação - Props'!A3:Z");"Select Col1, Col2, Col3, Col4, Col5, Col7, Col8, Col9, Col11, Col12, Col13, Col14")


* Depois de importar os dados, selecionar todos eles com (ctrl C) e colar somente os valores (ctrl + Shift + V).\n\n


\