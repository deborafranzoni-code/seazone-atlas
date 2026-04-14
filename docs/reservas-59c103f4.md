<!-- title: Reservas | url: https://outline.seazone.com.br/doc/reservas-kEztAv20EB | area: Tecnologia -->

# Reservas

Gestão de testes que devem ser considerados no site seazone.com.br

 

[https://docs.google.com/spreadsheets/d/11ZI0DOOC8jaBL3l0uz5ndNHhb-hfW1qa0AcR%5FqP75aA/edit?usp=sharing](https://docs.google.com/spreadsheets/d/11ZI0DOOC8jaBL3l0uz5ndNHhb-hfW1qa0AcR%5FqP75aA/edit?usp=sharing)

# WEBSITE

## Testes funcionais

* Buscas de cidades/lugares
  * cidades existentes na szn
  * cidades não existentes 
  * cidades existentes na szn
* \


\

| Cenário | Cidade | Check-in | Check-out | Adulto | Criança | Bebê | Pet | Descrição |
|----|----|----|----|----|----|----|----|----|
| 1 | Válida | Válida | Válida | 2 | 0 | 0 | 0 | Reserva padrão para casal |
| 2 | Válida | Válida | Válida | 2 | 2 | 1 | 0 | Família com crianças e bebê |
| 3 | Válida | Válida | Válida | 1 | 0 | 0 | 1 | Viajante solo com pet |
| 4 | Válida | Válida | Válida | 4 | 0 | 0 | 2 | Grupo de adultos com dois pets |
| 5 | Válida | Válida | Válida | 2 | 1 | 1 | 1 | Casal, criança, bebê e pet |
| 6 | Inválida | Válida | Válida | 2 | 0 | 0 | 0 | Cidade inexistente |
| 7 | Válida | Passada | Válida | 2 | 0 | 0 | 0 | Data de check-in no passado |
| 8 | Válida | Válida | Antes Check | 2 | 0 | 0 | 0 | Check-out antes do check-in (erro de data) |
| 9 | Válida | Válida | Válida | 0 | 0 | 0 | 0 | Sem hóspedes (erro esperado) |
| 10 | Válida | Válida | Válida | 10 | 0 | 0 | 0 | Excede limite de adultos permitido |
| 11 | Válida | Válida | Válida | 2 | 5 | 0 | 0 | Excede limite de crianças |
| 12 | Válida | Válida | Válida | 2 | 0 | 0 | 5 | Excede limite de pets |

## Testes no-funcionais