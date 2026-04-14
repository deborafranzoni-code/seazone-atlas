<!-- title: Sapron Webhooks | url: https://outline.seazone.com.br/doc/sapron-webhooks-Tg2PudaX0C | area: Tecnologia -->

# 📡 Sapron Webhooks

Projeto habilitador: @[Sapron Events](mention://4dba42c5-1740-4643-8f68-0cd31ad71ef0/document/413641e4-dd0c-4126-9bd7-e50a9081a302)

# TL;DR

Permitir que eventos do Sapron possam ser externalizados a terceiros por meio de Webhooks.

# Objetivo

Facilitar a criação de automações e centralizar o Sapron como fonte de dados canônica.

# Casos de Uso

## Eventos do Sapron disparam fluxos no N8N

Exemplo:

* Indicação de imóvel deve disparar registro na Morada: <https://workflows.seazone.com.br/workflow/SQqUI4cfD76lqxHM>

## Eventos do Sapron disparam notificações web

Exemplo:

* Ao atualizar uma solicitação de saque como "Paga", enviar notificação para o usuário.

## Sincronização de reservas do website a partir do Sapron

Atualmente, as reservas do website são sincronizadas a partir da Stays (assim como o Sapron). A ideia é tornar o Sapron a fonte de dados com relação a dados de reservas.

## Pagamento/verificação automática de solicitação de saque

Ao solicitar saque, podemos criar um workflow que automatiza o trabalho manual feito pelo time financeiro (integração com Omie).

/h2

## Plus: migração das N planilhas para o BD do Sapron e seus eventuais disparos

Atualmente, temos N planilhas que hoje servem como base de dados para diversos times. Algumas dessas bases de dados podem ter fluxos que se beneficiem dos webhooks.

# Arquitetura


 ![](/api/attachments.redirect?id=c62bf71a-f17a-4f4e-9aff-9f659e3cf1db " =1242x590")


 ![](/api/attachments.redirect?id=e2ed060d-aa86-446e-9de8-ebb97d43c59e " =2542x520")


## Banco de dados

 ![](/api/attachments.redirect?id=2fdd43ca-b510-4c00-aedb-e16d7fdc485e " =1242x601")


\