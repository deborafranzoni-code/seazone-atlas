<!-- title: Boas práticas | url: https://outline.seazone.com.br/doc/boas-praticas-IjpT0ee6WH | area: Tecnologia -->

# Boas práticas

**Manual de Boas Práticas para Uso do n8n**

**Objetivo:** Este manual visa orientar os times da empresa na utilização eficiente e organizada da ferramenta de automação n8n, promovendo agilidade, clareza e colaboração.


---

### 1. Nomenclatura Clara e Descritiva

* **Workflows:** Utilize nomes que reflitam claramente a função do workflow. Exemplo: `Processar Leads de Entrada`  `Enviar Email de Confirmacao`  `Resetar senha google`.
* **Credenciais:** Nomeie as credenciais de forma a identificar facilmente o serviço ou aplicação associada. Exemplo: `Gmail_Prod`, `Airtable_Leads`.
* **Nós:** Renomeie os nós para descrever suas funções específicas. No n8n, é possível renomear nós pressionando `F2` ou clicando no nome do nó na visualização detalhada .


---

### 2. Uso de Tags para Organização

* **Identificação por Equipe:** Adicione tags que representem as equipes responsáveis ou áreas de atuação. Exemplo: `Marketing`, `Financeiro`, `Suporte`.
* **Filtragem:** Utilize as tags para filtrar workflows e facilitar a localização e gestão .


---

### 3. Definição de Timeouts

* **Prevenção de Processos Longos:** Sempre defina um tempo limite (timeout) para workflows que possam ter processamento demorado. Isso evita que processos travem indefinidamente.
* **Configuração:** No n8n, é possível configurar o tempo de execução máximo de um workflow para evitar que ele ultrapasse o tempo desejado .


---

### 4. Documentação Interna

* **Notas Explicativas:** Utilize o recurso de sticky notes para adicionar descrições sobre a funcionalidade de cada workflow.
* **Objetivo:** Isso facilita o entendimento de outros usuários e a manutenção futura dos workflows.


---

### 5. Boas Práticas Adicionais

* **Modularização:** Para workflows complexos, considere dividi-los em workflows menores e interdependentes. Isso facilita a manutenção e o entendimento.
* **Ambientes:** Mantenha workflows distintos para ambientes de desenvolvimento, homologação e produção, evitando sobreposição e possíveis erros.


---

**Conclusão:** A adoção dessas boas práticas contribuirá para um ambiente de automação mais organizado, eficiente e colaborativo, permitindo que os times desenvolvam soluções de forma ágil e sustentável.