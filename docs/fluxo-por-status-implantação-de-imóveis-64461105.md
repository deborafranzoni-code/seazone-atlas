<!-- title: 🔄 Fluxo por Status – Implantação de Imóveis | url: https://outline.seazone.com.br/doc/fluxo-por-status-implantacao-de-imoveis-DfDdtdU7ue | area: Tecnologia -->

# 🔄 Fluxo por Status – Implantação de Imóveis

## **1. Contato inicial**

**Objetivo:** Primeiro contato com o proprietário e agendamento da vistoria inicial.

* **Dados exibidos:**
  * Nome do proprietário
  * Endereço do imóvel
  * Contato do proprietário (telefone/WhatsApp)
  * Taxa de limpeza
* **Ações permitidas:**
  * **Botão "Primeiro Contato"** → abre WhatsApp do proprietário (`wa.me/55[telefone]`).
    * Texto padrão:

      ```
      Olá [NOME DO PROPRIETÁRIO], tudo bem? 
      Sou da franquia [NOME] responsável pela implantação do seu imóvel [CÓDIGO/ENDEREÇO]. 
      Gostaria de confirmar seus dados e alinhar os próximos passos da vistoria inicial. 
      ```
  * **Agendar vistoria inicial** → abre agenda da vistoriadora.
    * Deve exibir lista de horários disponíveis.
    * Caso nenhum horário esteja disponível, exibir mensagem: "Nenhum horário disponível para vistoria inicial. Por favor, entre em contato com o time operacional."
* **Regras de negócio:**
  * A implantação só avança para *Aguardando vistoria inicial* após:

    
    1. Clique no botão de primeiro contato.
    2. Agendamento de vistoria confirmado.


---

## **2. Aguardando vistoria inicial**

**Objetivo:** Acompanhar a vistoria já agendada.

* **Dados exibidos:**
  * Link da reunião agendada (Google Calendar).
  * Data e horário da vistoria.
* **~~Ações permitidas:~~**
  * ~~Alterar horário → redirecionamento para agenda Google da vistoriadora.~~
* **Regras de negócio:**
  * Franquia não pode marcar outra vistoria por aqui, apenas alterar via agenda Google.
  * Após a realização da vistoria, o status do imóvel é atualizado conforme resultado registrado no Pipefy:
    * *Adequações complexas* ou
    * *Adequações simples* ou
    * Direto para *Confirmação de limpeza*.


---


## **3. Detalhes do imóvel**

**Objetivo:** Garantir que todas as informações operacionais do imóvel estejam cadastradas antes da ativação.

* **Dados a serem preenchidos pela franquia:**
  * **Senha da porta** (opcional)
  * **Senha do Wi-Fi** (campo obrigatório)
  * **Senha da portaria** (opcional)
  * **Garagem:**
    * Possui garagem? (Sim/Não)
    * Nº da vaga (se aplicável)
    * Quantidade de carros suportados
    * Forma de acesso (controle, tag, manual, outro)
  * **Endereço completo com link do Google Maps** (campo obrigatório)
  * **Fotos da fachada** (upload obrigatório)
  * **Imóvel é self check-in?** (Sim/Não)
  * **Contato do responsável pelo condomínio** (nome + telefone/e-mail) – obrigatório se imóvel for em condomínio.
* **Ações permitidas:**
  * Upload de fotos.
  * Preenchimento de formulário com campos obrigatórios/opcionais.
  * Botão "Salvar e Enviar" para confirmar as informações.



---

## **4. Adequações complexas**

**Objetivo:** Listar pendências críticas detectadas.

* **Dados exibidos:**
  * Relatório com itens que exigem adequação complexa.
* **Ações permitidas:**
  * Indicar novo horário para vistoria de adequações complexas.
  * Agendamento deve abrir agenda Google da vistoriadora.
* **Regras de negócio:**
  * Imóvel entra nesse status **apenas se** o card for incluído no *PIPE 2 – Adequação > FASE 2 ADEQUAÇÃO COMPLEXA*.
  * Após agendamento, o imóvel avança para *Aguardando vistoria – adequações complexas*.


---

## **4. Aguardando vistoria – adequações complexas**

**Objetivo:** Acompanhar a vistoria das adequações complexas.

* **Dados exibidos:**
  * Data e horário do agendamento.
  * Link da reunião agendada.
* **Regras de negócio:**
  * Alterações de horário seguem o mesmo processo via agenda Google.
  * Após vistoria, se todas as adequações estiverem concluídas → imóvel avança para *Confirmação de limpeza*.
  * Caso ainda existam pendências → retorna para *Adequações complexas*.


---

## **5. Adequações simples**

**Objetivo:** Listar pequenas adequações e permitir envio de evidências.

* **Dados exibidos:**
  * Lista de adequações simples identificadas.
* **Ações permitidas:**
  * Upload de fotos/documentos como evidência da adequação realizada.
* **Regras de negócio:**
  * Esse status **não bloqueia avanço**.
  * O imóvel pode seguir para *Confirmação de limpeza* independentemente das evidências enviadas.


---

## **6. Confirmação de limpeza**

**Objetivo:** Validar se o imóvel já foi limpo.

* **Dados exibidos:**
  * Instrução: "Confirme se o imóvel já está limpo e envie fotos amadoras como evidência."
* **Ações permitidas:**
  * Upload de fotos amadoras do imóvel.
  * Botão "Confirmar limpeza realizada".
* **Regras de negócio:**
  * Apenas após confirmação e upload de fotos o status avança para *Enxoval*.


---

## **7. Enxoval**

**Objetivo:** Garantir que o imóvel possui enxoval para ativação.

* **Dados exibidos:**
  * Pergunta: "Este imóvel possui enxoval de giro disponível?"
  * Campo para indicar data prevista de chegada, caso não possua.
* **Regras de negócio:**
  * Se **possui enxoval** → imóvel avança para *Aprovação do anúncio*.
  * Se **não possui enxoval** → imóvel permanece no status *Enxoval* até chegada da data prevista.


---

## **8. Fotos profissionais**

**Objetivo:** Registrar e acompanhar o agendamento de fotos profissionais.

* **Dados exibidos:**
  * Sugestão de horários disponíveis.
  * Agenda Google para agendamento.
* **Ações permitidas:**
  * Agendar data para fotos.
  * Confirmar realização das fotos na data marcada.
* **Regras de negócio:**
  * Etapa liberada **após limpeza confirmada e enxoval de giro disponível**.
  * Não depende da aprovação do anúncio.


---

## **9. Aprovação do anúncio**

**Objetivo:** Validar o anúncio criado antes da ativação.

* **Dados exibidos:**
  * Link do anúncio (ex.: `https://ssl.stays.com.br/pt/apartment/TST011`).
  * Checklist:
    * Endereço e localização do pin.
    * Amenities.
    * Configuração das camas.
* **Ações permitidas:**
  * Confirmar se anúncio está correto.
  * Reportar inconsistências via botão "Solicitar ajuste".
* **Regras de negócio:**
  * Caso imóvel ainda não tenha sido criado no *PIPE 5 – Criação Stays | Sem fotos*, exibir mensagem: "O anúncio ainda está em criação. Você será notificado assim que estiver disponível para conferência."
* **Texto de apoio exibido:**

  ```
  TST011 - Conferência do anúncio
  
  O anúncio do imóvel TST011 foi criado e estamos prontos para seguir com o processo de ativação.  
  Para conferir o anúncio, acesse: [LINK]  
  
  Por favor, verifique com atenção os seguintes pontos:  
  - Endereço e localização do pin  
  - Amenities  
  - Configuração das camas  
  ```


---

## **10. Imóvel ativo**

**Objetivo:** Finalizar a implantação e liberar o imóvel para operação.

* **Regras de negócio:**
  * Imóvel é marcado como "Ativo" automaticamente após validação no Pipefy.
  * Não há ações adicionais da franquia nesse status.