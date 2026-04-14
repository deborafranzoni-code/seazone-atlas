<!-- title: Ambientes (Dev, Staging e Prod) | url: https://outline.seazone.com.br/doc/ambientes-dev-staging-e-prod-19QameFoSI | area: Tecnologia -->

# Ambientes (Dev, Staging e Prod)

O projeto possui 3 tipos de ambientes e esses ambientes estão organizados em diferentes branches no GitHub do projeto:

**Desenvolvimento (Development)**

> Ambiente isolado onde é codificado as novas features ou fixes. Neste está o código mais atual, mas nem sempre o mais estável.

**Branch:** `main` **Frontend:** <http://localhost:3000/> **Backend:** <http://localhost:8000/> || [Swagger](http://localhost:8000/swagger) || [Admin](http://localhost:8000/admin/)

> \

**Staging**

> É igual ao ambiente de produção porém utilizado para testes e demonstração de features antes das novas features/correções irem para o ar.

**Branch:** `staging` **Frontend:** <https://test.staging.sapron.com.br/> **Backend:** <https://api.staging.sapron.com.br/> || [Swagger](https://api.staging.sapron.com.br/swagger/) || [Admin](https://api.staging.sapron.com.br/admin)

> \

**Produção** (**Production)**

> Ambiente de produção, onde o usuário final utiliza o sistema. É onde fica o código mais estável possível.

**Branch:** `production` **Frontend:** <https://sapron.com.br/> **Backend:** <https://api.sapron.com.br/> || [Swagger](https://api.sapron.com.br/swagger/) || [Admin](https://api.sapron.com.br/admin/)

> \