<!-- title: Guia do Usuário | url: https://outline.seazone.com.br/doc/guia-do-usuario-pcsnXCXuB0 | area: Tecnologia -->

# Guia do Usuário

# O que é a Cadência MIA?

É um sistema automático que:

* Envia mensagens WhatsApp
* Faz múltiplas tentativas
* Registra tudo no Pipedrive
* Para automaticamente quando necessário


---

# Quando a cadência inicia?

Ela inicia automaticamente quando:

* Deal entra no pipeline configurado
* Está com a tag correta
* Está aberto
* Passou do tempo mínimo configurado


---

# O que acontece em cada tentativa?


1. Envia WhatsApp via MIA
2. Cria atividade no Pipedrive
3. Registra nota com link da conversa


---

# Quando a cadência para?

Ela para automaticamente se:

* Deal virar LOST
* Deal mudar de stage
* Deal deixar de estar open
* Atingir número máximo de tentativas


---

# O que acontece se der erro?

* Deal é transferido para Jennifer Correa
* Nota é criada
* Slack é notificado
* Erro fica registrado


---

Como acompanhar?

No deal você verá:

* Nota com link da conversa
* Histórico de tentativas
* Label de cadência concluída


---

# Como alterar quantidade de tentativas?

Ajustar em:

`Baserow → tb_funis_pipedrive `

Campo:

`cadence_steps `


---

# Como alterar mensagem?

Ajustar em:

`Baserow → tb_parametrizacao_cadencia `

Editar:

* template
* parâmetros
* step correspondente


---

# Fluxo Visual Resumido

Trigger\n⬇\nFiltra deals\n⬇\nBusca parametrização\n⬇\nDefine Step\n⬇\nExecuta Workflow Principal\n⬇\nEnvia mensagem\n⬇\nRegistra execução\n⬇\nCria próxima atividade