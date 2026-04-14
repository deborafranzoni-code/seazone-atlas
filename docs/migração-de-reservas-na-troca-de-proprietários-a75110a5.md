<!-- title: Migração de Reservas na Troca de Proprietários | url: https://outline.seazone.com.br/doc/migracao-de-reservas-na-troca-de-proprietarios-GgDG3VpUI8 | area: Tecnologia -->

# Migração de Reservas na Troca de Proprietários

Solicitado em [SAP-1808](https://seazone.atlassian.net/browse/SAP-1808)


## Processo operacional:


1. Em <https://sapron.com.br/inserirdados/mudar-status-imovel>, mudar o status do imóvel desejado para "Inativo";
2. Em <https://sapron.com.br/onboarding>, cadastrar o proprietário (opcional) e o imóvel com o mesmo código;
3. Em <https://sapron.com.br/inserirdados/mudar-status-imovel>, quando o Onboarding for concluído, mudar o status do novo imóvel para "Ativo" com a data onde a migração das reservas deve iniciar.


## Problemas comuns

> ### __[⚠️⚠️ ](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjI3aun_KKKAxXbLrkGHbivGwIQFnoECBwQAQ&url=https%3A%2F%2Femojipedia.org%2Fwarning&usg=AOvVaw3r2cGE48TfsgfLLpDGiOog&opi=89978449)__As datas de contrato (`contract_start_date`) na tabela `property_property` são inputs do usuário, então se houver problemas relacionados a migração de reservas e sempre for atualizado de maneira a não cumprir a lógica, verifique os dados de todas as propriedades com o mesmo `code`. __[⚠️⚠️](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjI3aun_KKKAxXbLrkGHbivGwIQFnoECBwQAQ&url=https%3A%2F%2Femojipedia.org%2Fwarning&usg=AOvVaw3r2cGE48TfsgfLLpDGiOog&opi=89978449)__


## O que acontece por baixo dos panos:

Quando reservas são:

* Importadas (`stays_import_new_reservations_task`) a cada 15 minutos (1 dia antes até o dia corrente) ou
* Atualizadas (`stays_update_reservations_task`) a cada 6 horas (30 dias atrás até o dia corrente, filtrando pela data de check-out)


## Verificações realizadas 


1. As tasks caem na classe StaysHandler, método handle, linha 105, checa se a reserva da Stays tem um internalName (equivalente ao `property_property.code`)


* ![](/api/attachments.redirect?id=bf0b9bce-ed6b-4608-8809-be998ef1d39d)
* Se sim, olha as propriedades que temos na `property_property` filtrando pela coluna `code`, ordenando por `contract_start_date`.

  \
* ![](/api/attachments.redirect?id=5b0b0611-503c-4497-8d50-f788e75ba3f6)
* Da mesma maneira, há uma verificação pelo registro em `reservation_listing` utilizando `property_id` e `ota_id`, se não existe, é criado com para ser referenciando na `reservation_reservation`.


Dessa forma, as reservas se mantém com `property_id` e `listing_id` atualizados periodicamente na eventual migração de proprietário.


## Exemplo

É possível ver essa mudança na `reservation_audit`: 

Seguindo o processo operacional mencionado no início, tivemos a propriedade TST001 sendo recriada para um novo proprietário


\
 ![](/api/attachments.redirect?id=9e28d6db-cf47-4fd0-9390-400a8753c70b)


Na tabela `reservation_reservation` podemos notar que as reservas com `check_in_date` superior a `contract_start_date` foram importadas ou alteradas em `listing_id` e `property_id` da nova propriedade ![](/api/attachments.redirect?id=48172457-41a9-425d-aac6-d9f69ab75887)


Através da `reservation_audit` podemos ver, por exemplo, a reserva 390705 foi atualizada por uma task ![](/api/attachments.redirect?id=2c87cf23-1c33-49f8-941d-e1c9431a4c8c)