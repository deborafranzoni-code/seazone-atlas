<!-- title: Overrides de Links do Google Maps | url: https://outline.seazone.com.br/doc/overrides-de-links-do-google-maps-doWAbL5Wtg | area: Tecnologia -->

# 🗺️ Overrides de Links do Google Maps

# Override de Links do Google Maps via Baserow

## Visão Geral

O sistema de override de links do Google Maps permite substituir dinamicamente o endereço padrão de um imóvel nas mensagens de WhatsApp (check-in) por um link personalizado do Google Maps, configurado em uma tabela no Baserow. Isso elimina a necessidade de manter códigos de propriedade hardcoded no frontend.

### Contexto (PR #2286)

Anteriormente, a função `getAddressForMessage()` no `CheckinModal.tsx` continha lógica hardcoded com listas de códigos de propriedade (ex: `VGZ0001`–`VGZ0007`, `PRJ001`–`PRJ025`, prefixos `FFS`) e coordenadas fixas. Qualquer novo override exigia uma alteração de código e deploy.

Com a nova implementação, todos os overrides são gerenciados na tabela `**property_maps_overrides**` do Baserow. A aplicação consulta essa tabela em tempo real, sem necessidade de alterações no código-fonte.


---

## Arquitetura da Solução

### Tabela no Baserow: `property_maps_overrides`

**URL:** `[https://baserow.seazone.com.br/database/353/table/1410/5946]()`

| Campo | Tipo | Descrição |
|----|----|----|
| `id` | number | ID automático do Baserow (não editar) |
| `property_code` | string | Código do imóvel (ex: `VGZ0001`, `FFS1102`, `PRJ001`) |
| `maps_link` | string | URL completa do Google Maps para o imóvel |

### Arquivos do Frontend

| Arquivo | Função |
|----|----|
| `app/src/services/Baserow/request.ts` | Serviço genérico para chamadas à API do Baserow (axios) |
| `app/src/services/Baserow/types.ts` | Tipagens TypeScript (`BaserowRow`, `PropertyMapsOverride`) |
| `app/src/hooks/usePropertyMapsOverride/usePropertyMapsOverride.ts` | Hook React Query que busca o override por `property_code` |
| `app/src/hooks/usePropertyMapsOverride/index.ts` | Barrel export do hook |
| `app/src/components/ControllerPage/Modal/CheckinModal.tsx` | Modal de check-in que consome o hook |
| `app/src/hooks/useWhatsappTemplate/useWhatsappTemplate.ts` | Templates de WhatsApp (usa `{{mapsUrl}}` em vez de `{{address}}`) |

### Variáveis de Ambiente

As seguintes variáveis devem estar configuradas no `.env` da aplicação:

```
REACT_APP_BASEROW_URL=<URL base da API do Baserow>
REACT_APP_BASEROW_MAPS_TABLE_ID=<ID da tabela property_maps_overrides>
REACT_APP_BASEROW_API_TOKEN=<Token de API do Baserow>
```


---

## Fluxo de Funcionamento


1. O usuário abre o **Modal de Check-in** de uma reserva no Sapron.
2. O hook `usePropertyMapsOverride` é chamado com o `property_code` da reserva.
3. O hook faz uma requisição GET à API do Baserow filtrando por `property_code`:

   ```
   GET {BASEROW_URL}/api/database/rows/table/{TABLE_ID}/?user_field_names=true&filter__property_code__equal={code}
   ```
4. Se existir um registro correspondente, retorna o valor de `maps_link`.
5. Na montagem da mensagem de WhatsApp:
   * **Com override:** o link do `maps_link` do Baserow é usado diretamente como `mapsUrl`.
   * **Sem override (fallback):** é gerado um link padrão `https://www.google.com/maps/place/{endereço codificado}`.
6. O cache do React Query mantém o resultado por **10 minutos** (`staleTime: 1000 * 60 * 10`), evitando chamadas repetidas.


---

## Como Adicionar um Novo Override

Para adicionar um override de link do Google Maps para um novo imóvel, siga estes passos:

### Passo 1: Obter o link do Google Maps


1. Abra o [Google Maps](https://www.google.com/maps).
2. Pesquise pelo endereço exato do imóvel, estabelecimento ou pelas coordenadas.
3. Copie uma URL válida que funcione tanto no computador, quanto no celular. Que pode ser:

   
   1. A URL completa da barra de endereços do navegador.
      * Exemplo: `https://www.google.com/maps/place/28%C2%B008'49.1%22S+48%C2%B039'28.2%22W`
   2. A URL gerada ao clicar em "Compartilhar"
      * Exemplo: `<https://maps.app.goo.gl/ixeMdSf5whrJfUDq7>`

        ![](/api/attachments.redirect?id=bee28713-7593-49af-834e-1c36bbfd801f " =1413x818")
   3. URL encurtada via `shorten.seazone.com.br`
      * Exemplo: `<https://shorten.seazone.com.br/#/mt5tki>`

### Passo 2: Adicionar na tabela do Baserow


1. Acesse a tabela `property_maps_overrides` no Baserow: **<https://baserow.seazone.com.br/database/353/table/1410/5946>**
2. Clique na última linha vazia ou no botão de adicionar registro.
3. Preencha os campos:
   * `**property_code**`: O código do imóvel exatamente como aparece no Sapron (ex: `VGZ0008`, `FFS1201`, `ABC001`).
   * `**maps_link**`: A URL completa do Google Maps copiada no passo anterior.
4. O registro é salvo automaticamente.

### Passo 3: Validar


1. No Sapron, abra o modal de check-in de uma reserva do imóvel configurado.
2. Clique em "Mensagem (Dia do check-in)".
3. Verifique que o link do Google Maps na mensagem do WhatsApp aponta para o link configurado no Baserow.
4. (Opcional) Abra o Console do navegador (F12) e confirme que não há erros relacionados ao Baserow.

> **Importante:** Não é necessário nenhum deploy ou alteração de código. O override entra em vigor imediatamente (ou em até 10 minutos, se o cache anterior ainda estiver ativo).


---

## Como Remover um Override


1. Acesse a tabela `property_maps_overrides` no Baserow.
2. Localize o registro do imóvel desejado.
3. Delete a linha correspondente.
4. O imóvel voltará a usar o endereço padrão da reserva na próxima consulta (após expiração do cache).


---

## Detalhes Técnicos

### Serviço Baserow (`request.ts`)

O serviço utiliza `axios` com autenticação via token. A função `fetchBaserowRows<T>` é genérica e pode ser reutilizada para outras tabelas do Baserow:

```typescript
fetchBaserowRows<T>(tableId: string, filters: Record<string, string>): Promise<T[]>
```

Parâmetros sempre enviados: `user_field_names=true` (para usar nomes de campo legíveis).

### Hook `usePropertyMapsOverride`

```typescript
usePropertyMapsOverride(propertyCode: string): { mapsLink: string | null, isLoading: boolean }
```

Configurações do React Query:

* `enabled`: Só executa se `propertyCode` existir.
* `staleTime`: 10 minutos (600.000 ms).
* `refetchOnWindowFocus`: Desabilitado.

### Templates de WhatsApp

Os templates de fallback utilizam a variável `{{mapsUrl}}` que é preenchida com:

* O `mapsLink` do Baserow (se houver override), ou
* `https://www.google.com/maps/place/{endereço codificado}` (fallback padrão).


---

## Troubleshooting

| Problema | Causa Provável | Solução |
|----|----|----|
| Link do Maps não muda após adicionar override | Cache do React Query ainda ativo | Aguarde 10 minutos ou recarregue a página com cache limpo (Ctrl+Shift+R) |
| Erro 401 no Console | Token do Baserow inválido ou expirado | Verificar `REACT_APP_BASEROW_API_TOKEN` no `.env` |
| Erro 404 no Console | ID da tabela incorreto | Verificar `REACT_APP_BASEROW_MAPS_TABLE_ID` no `.env` |
| Override não funciona para um imóvel | `property_code` não corresponde | Conferir se o código no Baserow é idêntico ao exibido no Sapron (case-sensitive) |