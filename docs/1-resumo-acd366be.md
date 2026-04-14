<!-- title: 1. Resumo | url: https://outline.seazone.com.br/doc/1-resumo-fw4LiUrZTe | area: Tecnologia -->

# 1. Resumo

## **1.1 Introdução e objetivo**

O handover de proprietários consiste na inserção do proprietário no Sapron: quando o comercial dá ganho em um proprietário no Pipedrive, um analista insere seu DEAL_ID na página de "Onboarding" onde trazemos os dados pessoais do Proprietário e do seu imóvel.

Objetivos principais: a) Mapear os dados que são integrados entre Pipedrive e Sapron, deixando o processo semi-automatizado b) Quando um usuário for criado no Sapron, devemos enviar um email de primeiro acesso para o cliente c) Definir código do imóvel no Sapron evitando criação de códigos incorretos e duplicados. Quando se tratar de um imóvel de compra e venda, devemos realizar um comparativo do endereço do imóvel, caso o imóvel possua o mesmo endereço cadastrado no nosso BD, o imóvel deve ficar com o mesmo código

d) Realizar integração com o Pipedrive (possivelmente através de webhook) sempre que o lead estiver com a flag GANHO e) Garantir que proprietários que residem no exterior (main_adress ≠ BR) tenham o endereço de seus imóveis para suas notas fiscais (invoice_details)

## **1.2 Para quem é?**

\-Time de operações && financeiro

## **1.2 Glossário**

* **Lead**: um lead é uma pessoa ou empresa que demonstrou interesse em  nossos produtos e serviços. Neste contexto, um lead é um proprietário.
* **Pipedrive**: ferramenta de CRM (Customer Relationship Management) que ajuda equipes de vendas a gerenciar seus processos de vendas.
* **deal_id**: identificador único associado a um negócio (proprietário neste contexto)