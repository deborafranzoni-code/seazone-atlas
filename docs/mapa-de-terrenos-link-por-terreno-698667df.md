<!-- title: Mapa de Terrenos: Link por Terreno | url: https://outline.seazone.com.br/doc/mapa-de-terrenos-link-por-terreno-P8LIVG4g7C | area: Tecnologia -->

# Mapa de Terrenos: Link por Terreno

**Projeto:** Mapa de Terrenos Seazone 

**Status:** Em Andamento (Especificação) 

**Stakeholders:** Vinícius (Terrenos), Nath (Diretora de Área), Bill( Lider da BU de Dados ).

## **1. Contexto e Resumo**

Atualmente, o Mapa de Terrenos é uma ferramenta interna poderosa para visualização, mas carece de recursos básicos de colaboração e acesso rápido a dados externos.

* **Dor Identificada:** Dificuldade em compartilhar a localização de um terreno específico com colegas que não têm o mapa aberto ou não são usuários frequentes. O usuário tem que explicar manualmente "qual é o ID" e a pessoa tem que buscar manualmente.
* **Objetivo:** Permitir que um usuário gere um link que, ao ser aberto, centralize o mapa no terreno desejado e forneça um atalho direto para o detalhamento no Pipefy.

## **2. Solução Proposta**

Para resolver as dores identificadas na call, propomos a implementação de duas funcionalidades principais:


1. **Link de Compartilhamento (Deep Linking):** Capacidade de gerar e compartilhar uma URL específica para um terreno, permitindo que qualquer pessoa abra o mapa já centralizado no ponto de interesse.
2. **Integração Direta com Pipefy:** Adição de um atalho visual dentro do marcador do terreno que leve o usuário diretamente para o card do Pipefy, eliminando a necessidade de copiar IDs e buscar na plataforma.

## **3. Especificação Funcional e Requisitos**

A solução deve ser implementada utilizando a stack atual (HTML/JS puro, Google Maps API, BigQuery). Abaixo, os comportamentos esperados do sistema:

### **3.1. Funcionalidade 1: URL Dinâmica (Deep Linking)**

O sistema deve permitir que o estado visual do mapa (foco em um terreno específico) seja compartilhável via URL.

**Comportamento Esperado:**


1. **Atualização de Estado:** Quando o usuário interagir com um terreno (selecionar um marcador), a URL do navegador deve refletir essa seleção (ex: adicionando o ID do terreno como um parâmetro). Isso deve ocorrer sem recarregar a página para não perder a navegação atual.
2. **Restauração de Estado:** Quando o site for carregado através de uma dessas URLs, o sistema deve identificar o parâmetro, buscar o terreno correspondente nos dados e ajustar a visualização do mapa (Centralizar/Pan e Zoom) para focar naquele ponto específico.
3. **Navegação:** O zoom aplicado deve ser suficiente para distinguir o terreno individualmente (ex: nível de aproximação de rua/lote), garantindo que o usuário não perca tempo procurando o ponto.

**Notas Técnicas para o Time de Dev:**

* A solução provavelmente envolve o uso de manipulação de Query Strings e Histórico do Navegador, aliado aos métodos de câmera da API do Google Maps para o posicionamento.

### **3.2. Funcionalidade 2: Link Direto Pipefy**

O sistema deve integrar o mapa visual com a fonte de dados detalhada (Pipefy) para facilitar o fluxo de análise profunda.

**Comportamento Esperado:**


1. **Disponibilidade de Dados:** A fonte de dados (BigQuery/Nekt) deve fornecer, para cada terreno, um identificador único ou a URL direta para o card correspondente no Pipefy.
2. **Elemento de Interface:** Dentro do componente de exibição de informações (*InfoWindow*), deve existir um elemento clicável (botão ou link) claramente visível.
3. **Navegação Externa:** Ao clicar neste elemento, o usuário deve ser redirecionado para uma nova aba/janela abrindo diretamente o card do terreno no Pipefy.

**Notas Técnicas para o Time de Dev:**

* Requer validação se o campo de ID do Pipefy está presente na query atual do BigQuery.
* O componente *InfoWindow* deverá ser modificado para renderizar este link de forma condicional ou fixa, baseando-se nas propriedades do objeto JSON recebido.

## **4. Definição de Pronto (DoD) - Critérios de Aceite**


1. **URL Dinâmica:**
   *  Ao interagir com um terreno, a URL da barra de endereços muda para incluir um identificador.
   *  Ao acessar um link com esse identificador, o mapa carrega centralizado no terreno correto.
   *  O zoom aplicado permite identificar o terreno imediatamente.
   *  O ID do terreno permanece visível ou acessível para confirmação visual.
2. **Link Pipefy:**
   *  O *InfoWindow* exibe um botão/link "Ver no Pipefy" (ou similar).
   *  Ao clicar, abre-se uma nova aba direcionando para o card correto do Pipefy daquele terreno.
   *  Se o terreno não possuir link associado (dado faltante), o botão não deve aparecer para evitar erros (fallback).
3. **UX/UI:**
   *  Os novos elementos de interface seguem o padrão visual atual do mapa.

## **5. Riscos e Dependências**

* **Dependência de Dados:** A implementação do Link Pipefy depende da confirmação de que o ID/Card ID do Pipefy está vindo na query do BigQuery. Se não vier, um ajuste prévio na query SQL (Nekt) será necessário antes do desenvolvimento do frontend.
* **Licença da API:** A funcionalidade de centralização e zoom via URL é nativa da licença atual, sem custos adicionais esperados.


\