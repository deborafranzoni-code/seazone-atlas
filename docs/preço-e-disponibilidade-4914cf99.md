<!-- title: Preço e Disponibilidade | url: https://outline.seazone.com.br/doc/preco-e-disponibilidade-cJhOEnlumc | area: Tecnologia -->

# Preço e Disponibilidade

Atualmente pra trazer o preço e disponibilidade da Stays utilizamos o endpoint `GET /external/v1/calendar/listing/{listingId}. `

Ele nos traz as informações:

* Se um determinado dia está ou não disponível
* Qual o preço desse dia
* Estadia mínima (min_stays)

Rodamos uma task assíncrona a cada **30 minutos** (em produção) para atualizar o preço e disponibilidade do imóvel no *Open Search. Obs:* Nós não salvamos em BD informações de preços e disponibilidade.

**Observação:**

Na busca geral de imóveis serve pra dar uma ideia muito boa do preço, mas pode não ser preciso (que é o que acontece hoje). Uma vez que o usuário escolhe o imóvel, as outras APIs estão dizendo extamente o valor que será cobrado (na página de Detalhes do Imóvel)

### Relacionado

[Detalhes do imóvel](/doc/detalhes-do-imovel-BaMhIIjVEk)

[Resultados da Busca](/doc/resultados-da-busca-ApyKILy3uk)