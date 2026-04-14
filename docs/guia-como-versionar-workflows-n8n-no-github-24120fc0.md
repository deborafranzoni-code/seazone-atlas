<!-- title: Guia: Como Versionar Workflows n8n no GitHub | url: https://outline.seazone.com.br/doc/guia-como-versionar-workflows-n8n-no-github-rdgiUxa2aZ | area: Tecnologia -->

# Guia: Como Versionar Workflows n8n no GitHub

## Como Funciona

 ![](/api/attachments.redirect?id=d35daa8f-bcbf-46fb-a8f8-dac60f176db6 " =500x625")


Para versionar um workflow, adicione 2 tags obrigatórias:


1. `**git-versioned**` - Tag global que ativa o versionamento
2. `**\[setor\]-\[contexto\]**` - Uma váriavel que define onde o arquivo será salvo (use hífen como separador)

   **Exemplo:**

   ![Exemplo em suportes GOV](/api/attachments.redirect?id=937b786f-6bef-40ec-a474-e96b2ed0654d " =1152x648")

   \

O sistema converte as tags em caminhos de pasta automaticamente:

> **Tag:** 
>
> `revops-marketplace` → Resultado: *Revops/Marketplace/nome_do_workflow.json*  
>
> **Tag:** 
>
> `revops-lancamento-spots` → Resultado: *Revops/Lancamento_Spots/nome_do_workflow.json* **Tag:** 
>
> `gov-mia` → Resultado: *Gov/Mia/nome_do_workflow.json*


**Regras importantes:**

* Use **hífen (-)** como separador, não underscore
* O sistema capitaliza automaticamente as palavras
* Contextos compostos são unidos com underscore no caminho final


---

## Tags de Contexto Disponíveis

As tags abaixo já estão em uso e são recomendadas:

**Revops:** `revops-marketplace`, `revops-lancamento`, `revops-lancamento-spots`, `revops-szs`, `revops-szi`, `revops-cadencia`, `revops-vendas-spot`, `revops-utils`

**Gov:** `gov-mia`, `gov-suportes`

**Data:** `data-terrenos`, `data-suportes`

**Web:** `web-hosting`, `web-suporte`

Se precisar criar uma nova combinação, siga o padrão `setor-contexto`, sempre pode-se criar variáveis de salvamento novas! apenas adicione como tag **seguindo o padrão** no n8n.


---

## Exemplos Práticos

### Válido

* Tags: `git-versioned` + `revops-marketplace` → `Revops/Marketplace/`
* Tags: `git-versioned` + `gov-mia` → `Gov/Mia/`
* Tags: `git-versioned` + `data-terrenos` → `Data/Terrenos/`

### Inválido (vai para Uncategorized/General/)

* Só `git-versioned` sem tag de contexto
* `git-versioned` + `revops` (falta contexto)
* `git-versioned` + `revops_marketplace` (underscore em vez de hífen)

### Ignorado completamente

* Workflow sem a tag `git-versioned`


---

## Funcionamento Automático

O backup roda diariamente às **03:00 UTC (00:00 Brasília)** e executa:


1. Busca workflows com tag `git-versioned` via API
2. Valida tags de contexto e organiza em pastas
3. Remove campos voláteis do JSON para evitar commits desnecessários
4. **Detecta mudanças reais** na lógica do workflow
5. Cria commits (individual para poucas mudanças, batch para muitas)
6. **Sincroniza deleções:** se remover a tag ou deletar o workflow no n8n,  ele é removido do GitHub também.

   ![](/api/attachments.redirect?id=f2bbe0b3-fc07-470d-bc01-99114b1fe784 " =1146x489")


---

## Execução Manual

Para forçar backup imediato:


1. Vá em [https://github.com/seazone-tech/n8n-workflows-backup/actions](https://github.com/seazone-tech/n8n-workflows-backup/actions/workflows/backup.yml)
2. Clique em **"Run workflow"**

   ![](/api/attachments.redirect?id=6a84ae52-8b0c-4104-8be3-18d9df0853cb " =1302x446")


---

## Checklist Rápido

Quando criar ou atualizar um workflow que precisa ser versionado:

- [ ] Adicione tag `git-versioned`
- [ ] Adicione tag de contexto no formato `setor-contexto`
- [ ] Aguarde o próximo backup automático ou execute manualmente
- [ ] Verifique no GitHub se apareceu no caminho correto


---

## Links

* **n8n:** <https://workflows.seazone.com.br>
* **Repositório:** <https://github.com/seazone-tech/n8n-workflows-backup>
* **README:** <https://github.com/seazone-tech/n8n-workflows-backup/blob/main/README.md>