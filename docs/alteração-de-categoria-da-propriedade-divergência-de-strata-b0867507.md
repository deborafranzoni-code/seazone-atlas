<!-- title: Alteração de Categoria da Propriedade (Divergência de Strata) | url: https://outline.seazone.com.br/doc/alteracao-de-categoria-da-propriedade-divergencia-de-strata-OTeWtvuUdc | area: Tecnologia -->

# Alteração de Categoria da Propriedade (Divergência de Strata)

## 📌 Contexto


Em alguns cenários, identificamos divergências na **categoria da propriedade** entre o que está cadastrado no sistema e o que é informado via *Strata*. Essas inconsistências podem impactar:

* Regras de repasse
* Relatórios internos
* Integrações com parceiros
* Exibição em produtos (portais, apps, etc)


---

## ✅ O que fazer


Antes de montar a query e executar qualquer alteração, centralizamos as informações nessa [tabela](https://metabase.seazone.com.br/question/1949-property-categoryid-stratas) do *metabase* planilha abaixo, que serve como checklist de validação e histórico das alterações:

📄 [Planilha de Alteração de Categoria](https://docs.google.com/spreadsheets/d/15Nm0gi-9O9MqY35efIAKGL2yTAYn7J8QeHS-TsyyI1c/edit?gid=712145169#gid=712145169)

A planilha deve conter:

* ID da propriedade
* Categoria atual
* Categoria correta (`category_id`)
* Observações ou justificativas (quando aplicável)

Essa etapa é crucial pra garantir que nenhuma alteração errada vá parar no banco.


Quando a categoria correta da propriedade é confirmada, realizamos um **UPDATE** direto no banco de dados, atualizando o valor da coluna `category_id` na tabela `property_property`.


---

## 🧬 Query de Exemplo

```sql
UPDATE public.property_property
SET category_id = 00
WHERE id = 00;
```

> 💡 **Substitua os valores conforme o caso:**
>
> * category_id: novo ID da categoria correta
> * id: ID da propriedade com divergência


---

## ⚠️ Boas práticas antes da alteração

* Validar com o time ou usuário
* Confirmar se há dependências atreladas à categoria da propriedade
* Se possível, documentar quem autorizou a mudança