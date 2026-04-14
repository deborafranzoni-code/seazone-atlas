<!-- title: Swagger | url: https://outline.seazone.com.br/doc/swagger-cJ8Sxcf1jz | area: Tecnologia -->

# Swagger

[FastAPI - Swagger UI](https://api.staging.reservas.sapron.com.br/docs)

*Swagger (de staging) contendo a documentação das APIs*

### FAQ


---

* **Como se autenticar no Swagger?**

  
  1. Obtenha o seu token de acesso:

     
     1. Para obter acesse o front do ambiente que deseja sincronizar **([staging](https://seazone-reservas-staging.vercel.app/) | [produção](https://seazone.com.br/))**
     2. Faça login com sua conta
     3. Copie o seu **auth_token**
  2. Acesse o **Swagger** do ambiente que deseja sincronizar **([staging](https://api.staging.reservas.sapron.com.br/docs#/tasks/sync_properties_tasks_sync_properties_put) | [produção](https://api.reservas.sapron.com.br/docs#/tasks/sync_properties_tasks_sync_properties_put))**
  3. Clique em **"Authorize 🔒"** e então cole seu **auth_token**
  4. **Fim, está autenticado.**