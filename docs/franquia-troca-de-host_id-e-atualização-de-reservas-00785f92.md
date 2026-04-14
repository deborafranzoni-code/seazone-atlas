<!-- title: Franquia - Troca de host_id e atualização de reservas | url: https://outline.seazone.com.br/doc/franquia-troca-de-host_id-e-atualizacao-de-reservas-M0iZMBbpgf | area: Tecnologia -->

# Franquia - Troca de host_id e atualização de reservas

Pra troca de Franqueado precisa de uma troca válida na property_host_time_in_property com as seguintes validações:

Tabelas utilizadas: `property_host_time`, `property`


1. `property_host_time_in_property.old_host_id = property.host_id`
2. `replacement_date` não está no meio de uma reserva concluída
3. Na `property_host_time_in_property` o status deve estar '`Pending`'



4. Para rodar a task de troca pode ser chamada em <https://api.sapron.com.br/swagger/>

* `properties/tasks/change_host`



5. Para verificar o status, vá em `tasks/{task_id}` a `task_id` é o código que foi gerado pelo `change_host`


\

:::info
NOTA:

Se o `replacement_date` é uma data no futuro, a mudança vai acontecer apenas no dia agendado.

:::