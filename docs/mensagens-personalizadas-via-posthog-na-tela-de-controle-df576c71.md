<!-- title: Mensagens personalizadas via PostHog na tela de controle | url: https://outline.seazone.com.br/doc/mensagens-personalizadas-via-posthog-na-tela-de-controle-MhNcSWC9Jc | area: Tecnologia -->

# 💬 Mensagens personalizadas via PostHog na tela de controle

:desktop_computer: **Projeto/Sistema:** Sapron de Franquias\n:spiral_calendar_pad: **Criado em:** 6 de novembro de 2025 às 14:20 \n:arrows_counterclockwise: **Atualizado em:** 10 de novembro de 2025 às 10:01 \n**👥 Autores:** @[Aridan Silva Pantoja](mention://9da1472c-7fee-4a9b-abcb-4c7fef44bcc8/user/15233988-fd3f-4e3d-977a-932d59e65f23) @[Karol Wojtyla Sousa Nascimento](mention://66c0fd3b-416e-470d-9b6a-2bf5c9f01e84/user/a171b710-1218-4034-9406-e6b14888bd9f) \n:white_check_mark: **Status:** finalizado


---

## 🎯 Objetivo da Documentação

Esta documentação tem como objetivo descrever a funcionalidade de **mensagens de WhatsApp personalizadas via PostHog** na aplicação **Sapron de Franquias**.\nEla foi estruturada em **duas visões complementares**:

* **Visão de Produto/Marketing:** voltada para PMs e analistas, explicando o funcionamento do fluxo, onde editar as mensagens e quais ferramentas utilizar.
* **Visão Técnica (Dev Use):** voltada para desenvolvedores, detalhando a implementação e os pontos de integração com o PostHog.

O propósito é facilitar tanto a **autonomia na gestão dos conteúdos de comunicação**, quanto a **manutenção técnica e evolução do sistema.**


---

## 🧭 Contexto geral

Alguns fluxos da aplicação **Sapron de Franquias** enviam mensagens de WhatsApp automaticamente através da rota `api.whatsapp.com/send`.

Essas mensagens eram anteriormente **hardcoded no código**, o que exigia alterações técnicas e novos deploys sempre que o conteúdo precisava mudar.

Agora, os templates são **controlados dinamicamente via Feature Flags no PostHog**, permitindo que **times de Produto e Marketing atualizem os textos** em tempo real — sem intervenção técnica.


---

## 👁️ Visão de Produto/Marketing

Esta seção explica o funcionamento do fluxo, como atualizar as mensagens e quais ferramentas usar.

### 📋 O que esse fluxo faz

Cada etapa do processo de checkin do hóspede (como pré-checkin, checkin e checkin pendente) possui **mensagens padronizadas** enviadas por WhatsApp.

Essas mensagens seguem templates que são personalizados automaticamente com informações da reserva — como nome do hóspede, cidade, data de check-in e horário previsto.

Atualmente, existem 4 templates de mensagem, conforme sumarizado abaixo:

| Nome da FF | Fluxo | Descrição |
|----|----|----|
| [ff_message_pre_checkin](https://us.posthog.com/project/127887/feature_flags/236533) | Pré-Checkin | Template acionado no botão de **Mensagem** **Pré-Checkin**. Imutável. |
| [ff_message_checkin](https://us.posthog.com/project/127887/feature_flags/236540) | Checkin | Template da mensagem de checkin convencional do fluxo feliz, quando o usuário já respondeu o pré-checkin. Utilizado no botão de **Mensagem de Check-in.** |
| [ff_message_pending_checkin](https://us.posthog.com/project/127887/feature_flags/236554) | Pré-Checkin não respondido | Template usado quando o usuário recebeu a mensagem para realizar o pré-checkin, mas não o fez. Contém, idealmente, o link do pré-checkin e os dados necessários para realiza-lo. Utilizado no botão de **Mensagem de Check-in.** |
| [ff_message_same_day_pending_checkin](https://us.posthog.com/project/127887/feature_flags/236556) | Checkin no mesmo dia | Template usado para reservas express - quando a reserva foi criada para o mesmo dia de checkin. Utilizado no botão de **Mensagem de Check-in.** |

As mensagens de check-in, conforme descrito acima, são disparadas por triggers específicos, também descritos no fluxograma abaixo:

[https://miro.com/app/board/uXjVJuo6bis=/?focusWidget=3458764632024015081](https://miro.com/app/board/uXjVJuo6bis=/?focusWidget=3458764632024015081)

### ✍️ Como atualizar uma mensagem


1. Acesse o [PostHog](https://app.posthog.com/) do Sapron, na aba de feature flags, e procure pela **Feature Flag** desejada (ex: `ff_message_checkin`).
2. Clique na flag e clique em **Edit**.
3. Desça até a seção **Payload.**
4. Substitua o texto da mensagem no formato **compatível com o WhatsApp**, utilizando os placeholders disponíveis (`{{guestName}}`, `{{city}}`, `{{checkinTime}}`, etc.).
   * Importante: quebras de linha devem ser representadas com \\n\\n.
5. Salve a flag. As alterações serão refletidas imediatamente nos botões de envio de mensagem da aplicação em produção.


:::tip
Para auxiliar na construção e preview das mensagens adicionadas, foi construída a ferramenta [PostHog Message Editor](https://posthog-message-editor.vercel.app/), cujo objetivo é facilitar a criação e formatação das mensagens antes de colá-las no PostHog. Ela converte automaticamente o texto no formato que o sistema espera.

 ![](/api/attachments.redirect?id=83e0eab0-c03e-4ca4-a83d-b04db81f18ab " =685x373")

:::

## Adicionar mensagem no código do SAPRON (Dev Use):


 1. Ir até `useWhatsappTemplates.ts`
 2. Adicionar tipo da mensagem no `enum TemplateType`
 3. Adicionar fallback da mensagem em `FALLBACK_TEMPLATES`
 4. Criar feature flag em `enum ``*FeatureFlagsOptions*` *dentro de* `*useFeaturesFlags/types.ts *`
 5. Adicionar a feature flag dentro de flagKeys dentro do `FeatureFlagProvider`
 6. Mapear o TemplateType da mensagem com a FF do posthog em `FEATURE_FLAG_MAP` dentro de `useWhatsappTemplates.ts`
 7. Configurar uma variável que guarda se a feature flag da mensagem está ativada ou não

    ```javascript
      const isPreCheckinFlagEnabled = featureFlags[FeatureFlagsOptions.FF_SAPRON_FRONT_TEMPLATE_PRE_CHECKIN];
      const isCheckinMessageFlagEnabled = featureFlags[FeatureFlagsOptions.FF_SAPRON_FRONT_TEMPLATE_CHECKIN_MESSAGE];
      const isPendingCheckinMessageFlagEnabled = featureFlags[FeatureFlagsOptions.FF_SAPRON_FRONT_TEMPLATE_PENDING_CHECKIN_MESSAGE];
      const isSameDayPendingCheckinMessageEnabled = featureFlags[FeatureFlagsOptions.FF_MESSAGE_SAME_DAY_PENDING_CHECKIN]
    ```
 8. Dentro de `getWhatsappLinks` é necessário criar uma prop nova dentro do objeto `messages` e passar o nome da mensagem nova, a função que vai processar o template da mensagem com os parâmetros: tipo da mensagem, data, se a feature flag está ativa ou não

    ```typescript
    const messages = {
            preCheckin: getProcessedTemplate(TemplateType.PRE_CHECKIN, data, isPreCheckinFlagEnabled),
            checkin: getProcessedTemplate(TemplateType.CHECKIN_MESSAGE, data, isCheckinMessageFlagEnabled),
            pendingCheckin: getProcessedTemplate(TemplateType.PENDING_CHECKIN_MESSAGE, data, isPendingCheckinMessageFlagEnabled),
            sameDayPendingChekin: getProcessedTemplate(TemplateType.SAME_DAY_PENDING_CHECKIN_MESSAGE, data, isSameDayPendingCheckinMessageEnabled)
          };
    ```
 9. Ao final, é necessário retornar o link da mensagem em um objeto como:
10. ```typescript
    return {
            preCheckinWhatsappLink: createWhatsappLink(phoneNumber, messages.preCheckin),
            checkinDayWhatsappLink: createWhatsappLink(phoneNumber, messages.checkin),
            checkinDayPendingWhatsappLink: createWhatsappLink(phoneNumber, messages.pendingCheckin),
            sameDayPendingChekinWhatsappLink: createWhatsappLink(phoneNumber, messages.sameDayPendingChekin),
            directMessage: createWhatsappLink(phoneNumber),
          };
    ```

### Como utilizar

```typescript
const { getWhatsappLinks } = useWhatsappTemplates();

const {
    checkinDayPendingWhatsappLink,
    checkinDayWhatsappLink,
    preCheckinWhatsappLink,
    sameDayPendingChekinWhatsappLink,
    directMessage,
  } = getWhatsappLinks({
    data: {
      guestName: reservationData.guestName[0] || '',
      nickname: userInformation?.nickname || '',
      code: reservationData.code || '',
      formattedCheckInDate: reservationData.formattedCheckInDate,
      formattedCheckOutDate: reservationData.formattedCheckOutDate,
      address: reservationData.address,
      city: reservationData.city,
      staysReservationCode: reservationData.staysReservationCode,
      checkInTime: reservation?.pre_checkin?.check_int_expected_at.slice(0, 5) || '15:00',
    },
    phoneNumber: reservationData.phoneNumber,
  });
```


a