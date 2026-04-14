<!-- title: Documentação do Usuário | url: https://outline.seazone.com.br/doc/documentacao-do-usuario-KzM5a7JQeB | area: Tecnologia -->

# Documentação do Usuário

# **Manual do Usuário: Dashboard de Aquisição Viva Real**

## **1. Introdução**

Bem-vindo ao Dashboard de Aquisição Viva Real! 

Esta ferramenta foi projetada para que você possa explorar, filtrar e analisar os dados mais recentes de imóveis listados no portal Viva Real. Com ela, você pode entender o mercado imobiliário em regiões específicas, encontrar oportunidades e acompanhar métricas importantes como o preço médio por metro quadrado.

Os dados são coletados por um processo automático e atualizados periodicamente. A data da última atualização é sempre exibida no topo do painel para sua referência.

## **2. Visão Geral da Interface**

A tela do dashboard é dividida em três áreas principais, como mostrado na imagem abaixo:


1. **Painel de Filtros (Esquerda):** Permite que você refine a busca de imóveis com base em diversos critérios.
2. **Indicadores Principais (Topo):** Exibe os números mais importantes que resumem os dados com base nos filtros aplicados.
3. **Tabela de Imóveis (Direita):** Lista detalhada de todos os imóveis encontrados que correspondem à sua busca.

## **3. Como Utilizar o Dashboard**

#### **3.1. Filtrando os Dados** 

Para encontrar exatamente o que você procura, utilize o painel de filtros à esquerda. Sempre que você alterar um filtro, todo o dashboard (indicadores e tabela) será atualizado automaticamente.

* **Localização:**
  * `Estado`, `Cidade`, `Bairro`: Use os menus para selecionar a localização desejada.
* **Detalhes do Imóvel:**
  * `Número de Quartos` e `Número de Banheiros`: Arraste as barras para definir o intervalo (mínimo e máximo).
  * `Preço` e `Área M²`: Da mesma forma, defina a faixa de preço e de área em metros quadrados.
* **Tipo de Imóvel:**
  * Marque as caixas (`casa`, `apartamento`, etc.) para incluir os tipos de imóvel que você deseja ver. Você pode marcar mais de uma opção.
* **Nome do Anunciante:**
  * Se você quiser ver imóveis de uma imobiliária ou anunciante específico, pode selecioná-lo neste campo.

#### **3.2. Analisando os Resultados** 

Após aplicar os filtros, os resultados são exibidos nos indicadores e na tabela:

* **Indicadores Principais:**
  * **Imóveis Únicos Encontrados:** Mostra o número total de anúncios que correspondem aos seus filtros. No exemplo, foram encontrados **6.564** imóveis.
  * **Preço Médio / M²:** Calcula o valor médio do metro quadrado para todos os imóveis listados. É um excelente indicador para avaliar se uma região está cara ou barata.
* **Tabela de Imóveis:**
  * Esta tabela lista todos os imóveis encontrados.
  * **listing_title:** O título do anúncio, como aparece no Viva Real.
  * **link_url:** Um **link clicável** que leva você diretamente para a página do anúncio no site do Viva Real, permitindo que você veja fotos e mais detalhes.
  * **Navegação:** Na parte inferior da tabela, você pode ver quantos imóveis estão sendo exibidos (`1 - 100 / 6564`) e usar as setas `<` e `>` para navegar entre as páginas de resultados.

## **4. Exportando Dados para o Google Sheets**

Uma das funcionalidades mais poderosas deste dashboard é a capacidade de exportar os dados da tabela para que você possa fazer suas próprias análises em uma planilha.

Para exportar os dados para o Google Sheets, siga estes passos:


1. **Passe o mouse** sobre a área da **Tabela de Imóveis**.
2. Procure por um ícone de **três pontos (**`...`) ou um ícone de **download (uma seta para baixo** `↓`) que geralmente aparece no canto superior direito da tabela.
3. **Clique** neste ícone para abrir um menu de opções.
4. Selecione a opção **"Exportar"** ou **"Fazer o download"**.
5. Você verá diferentes formatos disponíveis. Escolha a opção **"Planilhas Google" (Google Sheets)**.

Pronto! Uma nova planilha será criada na sua conta do Google Drive com todos os dados da tabela que você filtrou no dashboard.