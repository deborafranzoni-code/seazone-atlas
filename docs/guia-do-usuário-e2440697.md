<!-- title: GUIA DO USUÁRIO | url: https://outline.seazone.com.br/doc/guia-do-usuario-QvqTlouyK8 | area: Tecnologia -->

# GUIA DO USUÁRIO

## **O que o fluxo faz?**

Quando um cliente falta a uma reunião, o sistema automaticamente tenta recuperar enviando uma mensagem via MIA no dia útil seguinte às 10:00.


---

## **O que o vendedor vê no Pipedrive**

Após o envio bem-sucedido:

✔ Uma nova atividade é criada:

> **Tentativa de recuperação de no-show**

✔ Uma nota é adicionada contendo:

* confirmação do envio
* link da conversa MIA

Exemplo:

> "Confirmação de reunião enviada via Morada - MIA\nAcesse: https://app.morada.ai/conversations/XXXXX"


---

## **Quando isso acontece**

| Evento | Ação |
|----|----|
| No-show detectado | Fluxo inicia |
| Dia útil seguinte 10:00 | MIA envia mensagem |
| Após envio | CRM registra resultado |


---

## **Se algo der errado**

Em caso de falha:

⚠ Nota no deal\n⚠ Notificação no Slack

O vendedor deve então retomar manualmente.


---

## **O que o usuário NÃO precisa fazer**

* Não precisa clicar
* Não precisa reagendar
* Não precisa enviar mensagem
* Não precisa marcar atividade
* Tudo é automático