<!-- title: Login via URL Params | url: https://outline.seazone.com.br/doc/login-via-url-params-KjqtQrvMhv | area: Tecnologia -->

# Login via URL Params

## Contexto

Atualmente, o hóspede recebe um link genérico de pré-checkin via WhatsApp e precisa preencher manualmente o formulário de login com: **código da reserva**, **data de check-in** e **data de check-out**. Isso gera fricção desnecessária, já que o backend já possui todas essas informações no momento do disparo da mensagem.

A proposta é eliminar esse passo manual: o hóspede clicará no link e já verá a tela logada (formulário de pré-checkin), no máximo com um loading intermediário.


---

## Decisões de Projeto

### Contrato de Integração (Front <> Back)

Formato da URL acordado entre front-end e back-end:

```
https://seazone.com.br/checkin/?check_in_date=2026-03-13&check_out_date=2026-03-14&stays_reservation_code=CODIGO
```

| Param | Tipo | Formato | Exemplo |
|----|----|----|----|
| `check_in_date` | string | `YYYY-MM-DD` | `2026-03-13` |
| `check_out_date` | string | `YYYY-MM-DD` | `2026-03-14` |
| `stays_reservation_code` | string | alfanumérico | `ABC123` |

### Responsabilidades

| Parte | Responsabilidade |
|----|----|
| **Backend** | Alterar o template de mensagem da Meta na Newbyte para disparar a nova URL com os params preenchidos |
| **Frontend** | Detectar os query params na URL, executar o login automaticamente e redirecionar o hóspede para a tela logada (`/v2/pre-checkin/formulario`) |
| **Newbyte (fornecedora)** | Atualizar o template de mensagem do WhatsApp Business API na Meta para suportar o novo formato de link |


---

## Arquitetura Atual (as-is)

### Fluxo de Login Atual

```
Hóspede recebe link genérico no WhatsApp
         |
         v
/v2/pre-checkin (página de login)
         |
         v
Hóspede preenche manualmente:
  - Código da Reserva
  - Data de Check-in
  - Data de Check-out
         |
         v
Submit do formulário
         |
         v
POST /auth/pre-check-in  (payload: stays_reservation_code, check_in_date, check_out_date)
         |
         v
Recebe JWT token -> salva em cookie httpOnly (pre_checkin_token)
         |
         v
router.push("/v2/pre-checkin/formulario")
```

### Arquivos Chave

| Arquivo | Função |
|----|----|
| `src/app/v2/pre-checkin/page.tsx` | Página de login (renderiza `<PreCheckin />`) |
| `src/components/PreCheckin/index.tsx` | Componente principal do login (layout mobile/desktop) |
| `src/components/PreCheckin/_components/Content/PreCheckinForm.tsx` | Formulário de login (Formik + Yup) |
| `src/hooks/usePreCheckin/index.ts` | Hook de estado do login (state machine: form/loading/error/success) |
| `src/services/PreCheckin/auth.ts` | Server action de autenticação (`POST /auth/pre-check-in`) |
| `src/components/PreCheckin/schemas/preCheckinSchema.ts` | Schema de validação Yup |
| `types/pre-checkin/pre-checkin.ts` | Tipos e interfaces do módulo |
| `src/services/PreCheckin/get-reservation-data.ts` | Busca dados da reserva pós-login |
| `src/app/v2/pre-checkin/formulario/page.tsx` | Página do formulário de checkin (destino pós-login) |

### Autenticação

* **Endpoint**: `POST {WALLET_API_URL}/auth/pre-check-in`
* **Request**: `{ stays_reservation_code, check_in_date, check_out_date }`
* **Response**: `{ access_token: string }` (JWT)
* **Storage**: Cookie httpOnly `pre_checkin_token` (max-age: 1 dia)
* **Dados do JWT**: `reservation_id`, `exp`, `iat`, `access_type`


---

## Arquitetura Futura (to-be)

### Novo Fluxo

```
Hóspede recebe link parametrizado no WhatsApp:
  https://seazone.com.br/checkin/?check_in_date=...&check_out_date=...&stays_reservation_code=...
         |
         v
/v2/pre-checkin?check_in_date=...&check_out_date=...&stays_reservation_code=...
         |
         v
Frontend detecta query params
         |
    +----+----+
    |         |
    v         v
  Com params   Sem params
    |             |
    v             v
  Loading      Formulário manual
  (auto-login)  (fluxo atual)
    |
    v
POST /auth/pre-check-in (mesma API, mesmos dados)
    |
    +-------+-------+
    |               |
    v               v
  Sucesso         Erro
    |               |
    v               v
  redirect to    Formulário manual
  /formulario    pré-preenchido
                 com os dados da URL
```

### Pontos Importantes


1. **Retrocompatibilidade**: o formulário manual continua funcionando normalmente se não houver params na URL.
2. **Fallback em caso de erro**: se o auto-login falhar, o formulário é exibido **pré-preenchido** com os dados extraídos da URL, para que o hóspede possa tentar manualmente.
3. **UX**: o hóspede vê apenas um loading entre o clique no link e a tela logada. Não há formulário intermediário.
4. **Segurança**: os dados na URL (código de reserva + datas) não são sensíveis por si só — servem apenas como credenciais de autenticação que o backend valida. O token JWT continua sendo armazenado em cookie httpOnly.


---

## Plano de Execução - Frontend

### Etapa 1: Leitura dos Query Params

**Arquivo**: `src/app/v2/pre-checkin/page.tsx`

* A `page.tsx` do Next.js App Router recebe `searchParams` como prop.
* Extrair `check_in_date`, `check_out_date` e `stays_reservation_code` dos search params.
* Passar esses valores como props para o componente `<PreCheckin />`.

### Etapa 2: Auto-login no Hook `usePreCheckin`

**Arquivo**: `src/hooks/usePreCheckin/index.ts`

* Adicionar um parâmetro opcional ao hook (ou receber via props no componente) com os dados vindos da URL.
* No mount do componente, se todos os 3 params estiverem presentes:
  * Setar o state para `"loading"` imediatamente.
  * Chamar `handleSubmit()` automaticamente com os dados da URL.
* Se os params forem parciais ou ausentes, manter o fluxo atual (exibir formulário).

### Etapa 3: Pré-preenchimento do Formulário (Fallback)

**Arquivo**: `src/components/PreCheckin/_components/Content/PreCheckinForm.tsx`

* Se os query params existirem mas o auto-login falhar:
  * Converter `check_in_date` e `check_out_date` (strings `YYYY-MM-DD`) para objetos `Date`.
  * Passar como `initialValues` para o Formik.
  * O hóspede vê o formulário já preenchido e pode submeter manualmente ou corrigir dados.

### Etapa 4: Componente de Loading para Auto-login

**Arquivo**: `src/components/PreCheckin/_components/Content/PreCheckinContent.tsx`

* O componente `PreCheckinContent` já renderiza por state (`form`, `loading`, `error`, `success`).
* O state `loading` já é tratado pelo `PreCheckinLoading`.
* Validar que o loading exibido durante o auto-login tem boa UX (mensagem adequada, spinner visível).

### Etapa 5: Tipos e Interfaces

**Arquivo**: `types/pre-checkin/pre-checkin.ts`

* Adicionar interface para os query params da URL:

  ```typescript
  export interface PreCheckinURLParams {
    check_in_date?: string;
    check_out_date?: string;
    stays_reservation_code?: string;
  }
  ```

### Etapa 6: Testes e Validação

- [ ] URL com todos os params -> auto-login -> redireciona para `/formulario`
- [ ] URL com params parciais -> exibe formulário manual (pré-preenchido com o que estiver disponível)
- [ ] URL sem params -> exibe formulário manual (fluxo atual inalterado)
- [ ] URL com params inválidos -> auto-login falha -> exibe formulário pré-preenchido + mensagem de erro
- [ ] Verificar que o loading aparece imediatamente ao abrir o link
- [ ] Verificar que o cookie httpOnly é setado corretamente após auto-login
- [ ] Testar em dispositivos móveis (alvo principal — link vem do WhatsApp)


---

## Log de Alterações

| Data | Autor | Descrição |
|----|----|----|
| 2026-03-13 | @[Karol Wojtyla Sousa Nascimento](mention://90b877b0-686d-4176-ac6c-deb1ad6c50bd/user/a171b710-1218-4034-9406-e6b14888bd9f) | Criação do documento, definição do contrato de integração e plano de execução |


---

## Referências

* Contrato de integração definido entre Front <> Back
* Fornecedora de WhatsApp Business API: **Newbyte**
* Template de mensagem: a ser atualizado na plataforma Meta via Newbyte