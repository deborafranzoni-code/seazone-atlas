<!-- title: Guia de Usuário | url: https://outline.seazone.com.br/doc/guia-de-usuario-BQ2LvFqXZ6 | area: Tecnologia -->

# Guia de Usuário

Versão 0.1 (POC) | Seazone Tech


---

## O que é

SeaNotes analisa automaticamente transcrições de reuniões do Google Meet e gera um documento estruturado com resumo, decisões e tarefas insipirado no formato FireFlies.

 ![](/api/attachments.redirect?id=dafb451b-8c79-433b-96e2-87f7fdafb03f " =2816x1536")



---

## Configuração (5 minutos)

 ![](/api/attachments.redirect?id=82fee687-8d75-4d8f-aad7-4e132f5dcc03 " =2816x1536")


### 1. Compartilhe sua pasta


1. Acesse **Google Drive** → `Meu Drive/Meet Recordings`
2. Clique em **Compartilhar**
3. Adicione: `automacao.governanca@seazone.com.br`
4. Permissão: **Editor**

### 2. Ative transcrição nas reuniões

**A cada reunião:**


1. Inicie a reunião no Google Meet
2. Três pontos (⋮) → ✅ **Marque:**  "**Ativar transcrição"**
3. Confirme

> ==Sem transcrição marcada, o SeaNotes não funciona.==


---

## Como funciona

**Você faz:**

* Prossegue reunião transcrição ativada

**SeaNotes faz:**

* Detecta nova transcrição na pasta
* Analisa com IA
* Cria arquivo `[SeaNotes].md` na mesma pasta (15-30 min depois)

**Exemplo na pasta:**

```
📁 Meet Recordings/
├── Reunião Comercial.txt
└── [SeaNotes] Reunião Comercial.md
```


---

## O que você recebe

Cada `[SeaNotes].md` contém:

* **Resumo Executivo**
* **Tópicos Principais** (com timestamps)
* **Action Items** (por pessoa)
* **Decisões Tomadas**
* **Pontos de Atenção**
* **Métricas e Dados**


---

## O que você recebe (detalhes)

### 📋 Resumo Executivo

Contexto geral da reunião em 2-3 parágrafos

### 📋 Tópicos Principais

Assuntos discutidos com timestamps quando disponíveis:

* Tópico importante (12:35)
  * Detalhe relevante mencionado

### 📋 Action Items

Tarefas organizadas por responsável:

* **João Silva**
  - [ ] Enviar proposta até sexta
  - [ ] Agendar follow-up

### 📋 Decisões Tomadas

Decisões importantes com contexto:

* Aprovado orçamento de R$ 50k para projeto X
* Definido prazo de entrega para 15/12

### 📋 Pontos de Atenção

Bloqueios ou riscos identificados

### 📋 Métricas e Dados

Números relevantes mencionados na reunião


---

## Perguntas Frequentes

> **Preciso fazer algo depois de configurar?** Não. Apenas lembre de marcar a transcrição ao iniciar reunões.
>
> **Quanto tempo demora?** 15-30 minutos após o fim da reunião.
>
> **Posso editar o arquivo gerado?** Sim, o `.md` é totalmente editável.
>
> **E se esquecer de marcar a transcrição?** Não será possível processar. Marque na próxima reunião.
>
> **Os arquivos antigos são reprocessados?** Não. Apenas arquivos novos ou modificados.
>
> **Funciona em reuniões organizadas por outros?** Sim, desde que a transcrição fique na SUA pasta.
>
> **SeaNotes lê vídeo?** Não. Apenas o texto da transcrição.
>
> **Meus dados são seguros?** Sim. Processamento via OAuth autorizado, arquivos ficam no seu Drive.


---

## Problemas Comuns e Soluções

### "Não apareceu o insight"

**Checklist completo:**


1. ✅ Pasta `Meet Recordings` compartilhada com `automacao.governanca@seudominio.com`?
2. ✅ Permissão de **Editor** foi concedida?
3. ✅ Transcrição foi marcada no início da gravação?
4. ✅ Arquivo `.txt` da transcrição apareceu na pasta?
5. ✅ Aguardou pelo menos 30 minutos?
6. \

**Se tudo acima está OK:**

* Verifique se o sistema está rodando (contate a Governança Tech)
* Verifique se não há erros na transcrição do Google Meet

### "Compartilhamento não funcionou"

**Passo a passo detalhado:**


1. Vá até a pasta `Meet Recordings`
2. Clique com botão direito → **Compartilhar**
3. No campo de email, digite exatamente: `automacao.governanca@seudominio.com`
4. Clique na caixa de permissões e selecione **Editor** (não Leitor!)
5. Clique em **Enviar**
6. Confirme que o email aparece na lista de pessoas com acesso

**Se continuar com erro:**

* Remova o compartilhamento e tente novamente
* Verifique se você é o proprietário da pasta (não apenas colaborador)

### "Insight está incompleto ou confuso"

**Causas possíveis:**

* **Áudio ruim:** Muito ruído de fundo ou microfone distante
* **Transcrição curta:** Reuniões < 5 minutos têm pouco conteúdo
* **Conversa informal:** Reuniões sem estrutura geram insights vagos
* **Múltiplas pessoas falando:** Dificulta a transcrição do Google Meet
* **Idioma misturado:** Alternância entre PT/EN pode confundir

**Como melhorar:**

* Use fone com microfone de qualidade
* Silencie quando não estiver falando
* Estruture a reunião (pauta clara)
* Mencione explicitamente: "João ficará responsável por..."
* Cite prazos claramente: "até sexta-feira dia 15"

### "Insight demorou mais de 1 hora"

**Causas:**

* Transcrição muito longa (reunião > 2 horas)
* Fila de processamento (múltiplas reuniões simultâneas)
* Sistema temporariamente offline

**O que fazer:**


1. Aguarde até 2 horas no máximo
2. Verifique se não há outros insights sendo processados


---

## Dicas para Melhores Resultados

* **Durante a reunião:** \nMencione nomes ao atribuir tarefas: "João, você pode..."\nCite prazos explicitamente: "até sexta, dia 15"\nResuma decisões importantes antes de encerrar

  Silencie quando não estiver falando
* **Após a reunião:** 

  Confirme que transcrição foi gerada\nAguarde 30 min antes de buscar o insight


---

Precisa de Ajuda?

**Contatos:**

* 💬 Slack: #suporte-governanca

**Ao reportar problema, inclua:**

* Nome do arquivo de transcrição
* Data/hora da reunião
* Descrição do comportamento esperado vs. real