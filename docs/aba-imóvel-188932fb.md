<!-- title: Aba Imóvel | url: https://outline.seazone.com.br/doc/aba-imovel-jn3SHsnPxU | area: Administrativo Financeiro -->

# Aba Imóvel

\
Fórmula para Arrastar para Baixo\nColunas: D/W/Y/X\n

Importação de Dados via Script Imóvel ⇒fechaImovel():\nColuna: A\~C/E\~R/V\n


Todos os exports e dados necessários para consistência da aba Imóvel

|    |    |    |
|:---|:---|:---|
| **Planilha** | **Abas** | **Colunas** |
| Fechamento Mensal Template | Despesa Mes | B, C, E, J |
| Conciliação Reserva Sapron | Faturamento Reservas Mes | C, D, I |
| Conciliação Reserva Sapron | Conciliação Fechamento | C, D, I |
| 00 - Banco de dados PMS | Apartment | E, R, AM |
| Relação Imóvel x Anfitrião | Relação 2.0 | A, B, C, E, F |

# Aba Despesas

Planilha: <https://docs.google.com/spreadsheets/d/1wL4SBGofNb04MH3nzWVmgus2evD26zUJaquuaR0wbCk/edit#gid=30783992>


Obs. essa aba é construída exclusivamente via API do Sapron, sendo que este possui um gatilho de ativação diário às AM 01:00. No entanto ele também pode ser ativado manualmente pelo link

<https://docs.google.com/spreadsheets/d/1WQiCJZJqJWV-ijk4KYasnkfQ4LwpV_8krXYvdJLWfkk/edit#gid=0>

Passo para atualização manual

Na parte superior da tela > Funcionalidades > Fechamento > Atualizar despesas


Obs2. esses dados entram pela aba Despesa Mês, via importrange

# Aba Faturamento Reservas Mes

Planilha: <https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=1353793656>


Essa aba é atualizada pelo botão na aba Dashboard "Faturamento Mensal"

# Aba Conciliação Fechamento

Planilha: <https://docs.google.com/spreadsheets/d/17vMaBCLcc7V1OpIjQMhf-OVI6fPEWkhMlDHMkn9G0N8/edit#gid=1353793656>


Esta aba é atualizada via importrange

# Aba Apartment

Planilha: <https://docs.google.com/spreadsheets/d/1u6C2KtkJqDvR6-ZKDRLsLKZ5leaAnYPp78tTG3v6NXo/edit#gid=169327024>


Obs. essa aba é construída exclusivamente via API do Sapron, sendo que este possui um gatilho de ativação diário às AM 01:00. No entanto ele também pode ser ativado manualmente pelo link

<https://docs.google.com/spreadsheets/d/1WQiCJZJqJWV-ijk4KYasnkfQ4LwpV_8krXYvdJLWfkk/edit#gid=0>


Passo para atualização manual

Na parte superior da tela > Funcionalidades > Fechamento > Atualizar Propriedades