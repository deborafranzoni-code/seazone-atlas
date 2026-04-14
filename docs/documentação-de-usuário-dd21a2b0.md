<!-- title: Documentação de Usuário | url: https://outline.seazone.com.br/doc/documentacao-de-usuario-4mUUaguF94 | area: Tecnologia -->

# Documentação de Usuário

## Introdução

O **Gestão de Preços Especiais** é uma ferramenta da Seazone para gerenciar regras de preços especiais de imóveis. Com ele, você pode:

* Criar, editar e excluir regras de preços
* Visualizar e filtrar todas as regras cadastradas
* Simular conflitos entre regras para entender qual prevalece
* As alterações são sincronizadas automaticamente com o backend


---

## Acesso ao Sistema

### Quem pode acessar?

Somente colaboradores da Seazone com email **@seazone.com.br**.

### Como fazer login


1. Acesse a URL da aplicação no navegador
2. Clique no botão **"Entrar com Google"**
3. Selecione sua conta Google corporativa (@seazone.com.br)
4. Você será redirecionado para a tela principal

### Logout

Clique no botão de **Sair** no canto superior direito da tela.


---

## Visão Geral da Interface

A aplicação possui duas abas principais:

### Aba "Regras"

Tela principal onde você visualiza, filtra, cria, edita e exclui regras de preços especiais.

**Elementos da tela:**

* **Cabeçalho:** Botão "Nova Regra", seu email e botão de sair
* **Barra de Filtros:** Campos para pesquisar e filtrar regras
* **Tabela de Regras:** Lista todas as regras com opções de editar e excluir

### Aba "Raio-X"

Simulador de hierarquia. Permite testar qual regra vence quando existem múltiplas regras para o mesmo imóvel.


---

## Gerenciamento de Regras

### Criar uma Nova Regra


1. Clique no botão **"Nova Regra"** no cabeçalho
2. Preencha os campos do formulário:

| Campo | Obrigatório | Descrição |
|----|:---:|----|
| Grupo / Imóvel | Sim | Identificador do imóvel ou grupo (ex: "IMV-001" ou "Grupo A"). O nível será calculado automaticamente |
| Data Início | Sim | Data em que a regra começa a valer |
| Data Fim | Sim | Data em que a regra para de valer (**exclusiva** — a regra NÃO vale neste dia) |
| Valor (R$) | Sim | Valor do preço em reais (deve ser maior que 0) |
| Acréscimo (%) | Não | Percentual de acréscimo sobre o valor |
| Tipo | Não | Tipo da regra: **Fixo**, **Mínimo** ou **Máximo** (padrão: Fixo) |
| Origem | Não | Quem solicitou: **Proprietário**, **RM** ou **Operação** |
| Região | Não | Região brasileira (Norte, Sul, Nordeste, Sudeste, Centro-Oeste) |
| Evento | Não | Nome do evento especial (ex: "Carnaval", "Réveillon") |
| Grandes Operações | Não | Disponível apenas para nível Imóvel. Indica operação de grande porte |
| Ignorar Hierarquia | Não | Quando ativado, a regra ignora o sistema de hierarquia e compete diretamente com todas as outras |
| Observação | Não | Notas adicionais sobre a regra |


3. Observe os **alertas de conflito** (se existirem):
   * **Alerta vermelho ("Substituição de Regras"):** Sua nova regra irá sobrepor regras existentes
   * **Alerta amarelo ("Regra será ignorada"):** Regras existentes têm prioridade sobre a sua nova regra
4. Clique em **"Salvar"** (ou **"Confirmar e Salvar"** se houver conflitos)
5. A regra aparece **imediatamente** na tabela — a sincronização com o backend acontece em segundo plano

### Editar uma Regra


1. Na tabela de regras, localize a regra desejada
2. Clique no botão de **editar** (ícone de lápis) na linha da regra
3. Modifique os campos desejados no formulário
4. O campo **Nível** será exibido como somente leitura durante a edição
5. Clique em **"Salvar"** — a tabela atualiza na hora

### Excluir uma Regra


1. Na tabela de regras, localize a regra desejada
2. Clique no botão de **excluir** (ícone de lixeira) na linha da regra
3. A regra é removida da tabela imediatamente

**Atenção:** A exclusão é sincronizada automaticamente com o backend em segundo plano. Não é possível desfazer esta ação.


---

## Filtros e Busca

A barra de filtros permite encontrar regras específicas rapidamente.

### Campos de filtro

| Filtro | Como funciona |
|----|----|
| **Grupo / Imóvel** | Busca textual pelo nome do grupo ou imóvel. Não diferencia maiúsculas de minúsculas |
| **Data Início** | Mostra apenas regras que terminam após esta data (ainda ativas a partir dela) |
| **Data Fim** | Mostra apenas regras que começam antes desta data (ativas até ela) |
| **Região** | Filtra por região brasileira específica |
| **Nível** | Filtra por tipo de nível: Imóvel, Categoria ou Região |

### Como usar


1. Preencha um ou mais filtros
2. Clique em **"Pesquisar"** para aplicar
3. A tabela mostrará apenas as regras que correspondem aos filtros
4. Para limpar os filtros, clique em **"Limpar"**

### Paginação

A tabela exibe **50 regras por página**. Use os controles de paginação na parte inferior da tabela para navegar.


---

## Simulador de Hierarquia (Raio-X)

### Para que serve?

Quando existem múltiplas regras para o mesmo imóvel ou grupo, o sistema precisa decidir qual prevalece. O Raio-X mostra:

* Qual regra **vence** (será aplicada)
* Quais regras **perdem** e **por quê** foram ignoradas

### Como usar


1. Clique na aba **"Raio-X"**
2. No campo **"Imóvel / Grupo"**, pesquise e selecione o imóvel ou categoria desejada
   * O dropdown separa as opções em **Imóveis** e **Categorias**
   * Você pode digitar para filtrar as opções
3. (Opcional) Selecione uma **data** específica para ver apenas regras que estão ativas naquele dia
4. Os resultados aparecem automaticamente

### Lendo os resultados

* **Card verde ("Vencedora"):** A regra que será aplicada. Mostra todos os detalhes: período, valor, tipo, nível, etc.
* **Cards cinza ("Ignorada"):** Regras que existem mas não serão aplicadas. Cada card inclui uma explicação em itálico do motivo:
  * "Regra vencedora ignora hierarquia"
  * "Sobreposta por nível superior (Imóvel)"
  * "Máximo ignorado — vencedora tem valor menor"
  * "Fixo ignorado — vencedora tem valor maior"


---

## Como Funciona a Hierarquia de Regras

Quando várias regras se aplicam ao mesmo imóvel na mesma data, o sistema resolve o conflito seguindo estas prioridades:

### Prioridade 1: Flag "Ignorar Hierarquia"

Regras com a flag **"Ignorar Hierarquia"** ativada competem diretamente com todas as outras, independente do nível.

### Prioridade 2: Nível hierárquico

Níveis mais específicos vencem níveis mais gerais:

```
Imóvel (mais específico, vence)
  → Categoria
    → Região (mais geral, perde)
```

Uma regra definida diretamente para um **Imóvel** sempre vence uma regra definida para a **Categoria** ou **Região** a que ele pertence.

### Prioridade 3: Tipo e valor

Quando duas regras estão no mesmo nível:

| Situação | Quem vence |
|----|----|
| Dois preços **Fixo** | O **maior** valor |
| Dois preços **Mínimo** | O **maior** valor |
| Dois preços **Máximo** | O **menor** valor |
| **Mínimo** vs **Fixo** | O que tiver **maior** valor |
| **Fixo** vs **Máximo** | O que tiver **maior** valor |
| **Mínimo** vs **Máximo** | O que tiver **maior** valor |

### Exemplo prático

Imagine 3 regras para o imóvel IMV-001 no dia 15/03/2026:


1. **Regra A:** Nível Região, Tipo Fixo, Valor R$ 500
2. **Regra B:** Nível Categoria, Tipo Mínimo, Valor R$ 400
3. **Regra C:** Nível Imóvel, Tipo Fixo, Valor R$ 350

**Resultado:** A **Regra C** vence porque está no nível Imóvel (mais específico), mesmo tendo o menor valor.


---

## Conceitos Importantes

### Tipos de Regra

| Tipo | Significado |
|----|----|
| **Fixo** | O preço será exatamente este valor |
| **Mínimo** | O preço não pode ser menor que este valor (piso) |
| **Máximo** | O preço não pode ser maior que este valor (teto) |

### Níveis

| Nível | O que abrange |
|----|----|
| **Imóvel** | Um imóvel individual específico |
| **Categoria** | Um grupo/categoria de imóveis |
| **Região** | Uma região geográfica (polígono, bairro, cidade, estado, etc.) |

### Origens

| Origem | Quem solicitou |
|----|----|
| **Proprietário** | O proprietário do imóvel |
| **RM** | Revenue Management |
| **Operação** | Equipe de operações |

### Data Fim Exclusiva

A data de fim de uma regra é **exclusiva**. Se uma regra tem fim em 10/03, ela **não vale** no dia 10/03 — vale até o dia 09/03.

### Ignorar Hierarquia

Quando esta opção está ativada, a regra "fura a fila" e compete diretamente com regras de todos os níveis. Útil para regras de eventos especiais ou situações excepcionais.

### Grandes Operações

Flag disponível apenas para regras de nível **Imóvel**. Indica que a regra está associada a uma operação de grande porte.

### Sincronização e atualização dos dados

Os dados da tela são carregados uma única vez ao abrir a aplicação. Eles **só são atualizados** quando você:

* **Salva** uma nova regra
* **Edita** uma regra existente
* **Exclui** uma regra

Essas ações refletem **imediatamente** na tela, e a sincronização com o backend acontece em segundo plano. Se a sincronização falhar, você verá uma mensagem de erro.

Se outro usuário fez alterações ou você quer garantir que está vendo os dados mais recentes, **recarregue a página** (F5).


---

## Perguntas Frequentes (FAQ)


1. **Não consigo fazer login**

* Verifique se está usando um email **@seazone.com.br**
* Emails pessoais (Gmail, Hotmail, etc.) não são aceitos
* Tente limpar o cache do navegador e fazer login novamente


2. **Criei uma regra mas ela não aparece na tabela**

* Se você já tem filtros aplicados, a regra aparece automaticamente se corresponder aos filtros ativos
* Se não tem filtros aplicados, use os filtros e clique em **"Pesquisar"** para ver as regras
* Verifique se os filtros aplicados correspondem à regra criada


3. **Minha regra está sendo ignorada**

* Use o **Raio-X** para verificar quais regras estão ativas para o imóvel
* Provavelmente existe uma regra de nível mais específico (ex: Imóvel > Categoria)
* Considere ativar a opção **"Ignorar Hierarquia"** se necessário


4. **Qual a diferença entre Fixo, Mínimo e Máximo?**

* **Fixo:** Define um preço exato
* **Mínimo:** Define o menor preço aceitável (piso)
* **Máximo:** Define o maior preço aceitável (teto)


5. **O que acontece quando excluo uma regra?**

* A regra é removida do sistema e a lista atualizada é sincronizada com o backend
* Esta ação não pode ser desfeita


6. **Quando devo usar "Ignorar Hierarquia"?**

* Use em situações excepcionais onde a regra deve valer independentemente de existirem regras mais específicas
* Exemplo: Um preço mínimo obrigatório para um evento que se aplica mesmo que o imóvel tenha uma regra individual


7. **A data de fim está inclusa no período?**

* **Não.** A data de fim é exclusiva. Uma regra com fim em 15/03 vale até 14/03.


8. **Como sei se minha regra vai sobrepor outra?**

* Ao criar ou editar uma regra, o sistema mostra automaticamente alertas de conflito:
  * **Vermelho:** Sua regra irá substituir regras existentes
  * **Amarelo:** Regras existentes têm prioridade sobre a sua
* Use o **Raio-X** para simulações mais detalhadas


9. **Os dados são salvos automaticamente?**

* Sim. Ao clicar em "Salvar", a regra aparece na hora na tabela e é sincronizada com o backend em segundo plano
* Se houver falha na sincronização, você será notificado por uma mensagem de erro
* Ao recarregar a página, os dados são buscados novamente da API para garantir consistência