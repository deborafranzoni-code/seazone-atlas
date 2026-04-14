<!-- title: 🧾 PRD — Fluxo de Validação de Evidências em Tarefas de Franquia | url: https://outline.seazone.com.br/doc/prd-fluxo-de-validacao-de-evidencias-em-tarefas-de-franquia-mdbHYoUcdg | area: Tecnologia -->

# 🧾 PRD — Fluxo de Validação de Evidências em Tarefas de Franquia

### 📌 **Contexto**

Atualmente, o processo de acompanhamento de tarefas executadas por franquias não permite uma rastreabilidade clara sobre quais ações demandam comprovação (evidências) e quais podem ser concluídas sem essa etapa.\nO objetivo deste fluxo é **permitir o envio, vinculação e validação de evidências (PDF, foto ou vídeo)** em tarefas, garantindo controle, transparência e padronização na comunicação entre a equipe central e as franquias.


---

### 🎯 **Objetivo do Produto**

Implementar um fluxo de **validação de evidências em tarefas**, possibilitando:

* Atribuir tarefas com ou sem necessidade de evidência;
* Permitir à franquia o envio de arquivos de comprovação (PDF, imagem ou vídeo);
* Garantir um ciclo de aprovação/reprovação transparente e rastreável;
* Melhorar o acompanhamento da execução de tarefas e o controle de qualidade.


---

### 👤 **Usuários Envolvidos**

* **Time Central / Administração:** cria tarefas, define se há exigência de evidência e valida as entregas enviadas.
* **Franquia:** recebe tarefas, executa-as e, quando necessário, envia evidências para validação.


---

### 🔁 **Fluxo de Usuário (Visão Simplificada)**


1. **Criação da Tarefa**
   * O time central cria uma tarefa.
   * Deve existir a opção **"Requer evidência?"** (checkbox ou toggle).
   * Opcionalmente, a tarefa pode ser **vinculada a um imóvel específico** (campo "Imóvel vinculado").\n→ Esse vínculo é **opcional**.
2. **Execução pela Franquia**
   * A tarefa aparece no status **"PENDENTE"**.
   * Se a tarefa **requer evidência**, o envio de **PDF, Foto ou Vídeo** será **obrigatório** para marcar como concluída.
   * Caso a tarefa **não exija evidência**, a franquia poderá apenas marcar como concluída diretamente.
3. **Envio de Evidência**
   * Ao enviar o arquivo (PDF/FOTO/VÍDEO), a tarefa muda automaticamente para o status **"AGUARDANDO VALIDAÇÃO"**.
   * O arquivo fica visível para o time central validar.
4. **Validação pela Administração**
   * O time central avalia a evidência:
     * Se **aprovada**, a tarefa muda para **"FINALIZADO"**.
     * Se **reprovada**, a tarefa volta ao status **"PENDENTE"**, e o validador deve preencher um campo obrigatório de **"Motivo da Reprovação"**.
5. **Revisão pela Franquia**
   * A franquia visualiza o **motivo da reprovação** e pode reenviar nova evidência.
   * O fluxo segue até aprovação final.


---

### 🧩 **Regras de Negócio**

| Regra | Descrição |
|----|----|
| R1 | Toda tarefa nasce com o status **PENDENTE**. |
| R2 | Apenas tarefas marcadas como **"Requer evidência"** exigem upload de arquivo. |
| R3 | O campo de evidência aceita **PDF, imagem (.jpg/.png)** ou **vídeo (.mp4)**. |
| R4 | O envio de pelo menos um arquivo é **obrigatório** para tarefas que requerem evidência. |
| R5 | Após o envio, o status muda automaticamente para **AGUARDANDO VALIDAÇÃO**. |
| R6 | Ao reprovar uma evidência, o **campo "Motivo da Reprovação"** é **obrigatório**. |
| R7 | O motivo da reprovação deve ser exibido para a franquia na interface da tarefa. |
| R8 | A aprovação da evidência altera o status para **FINALIZADO**. |


---

### 📊 **Status e Transições**

| Status Atual | Ação | Próximo Status |
|----|----|----|
| **PENDENTE** | Envio de evidência pela franquia | **AGUARDANDO VALIDAÇÃO** |
| **AGUARDANDO VALIDAÇÃO** | Aprovação da evidência | **FINALIZADO** |
| **AGUARDANDO VALIDAÇÃO** | Reprovação da evidência (com motivo) | **PENDENTE** |


---

### 🧠 **Melhorias de Usabilidade Propostas**

* Mostrar na criação da tarefa uma **tooltip explicando o que é "Requer evidência"**.
* Exibir **pré-visualização dos arquivos enviados** pela franquia antes do envio.
* Permitir **comentários adicionais** opcionais no momento da reprovação.
* Adicionar **indicadores visuais** (ex: ícone de câmera/documento) nas tarefas que exigem evidência.
* Permitir **filtros de status** na listagem (Pendente, Aguardando Validação, Finalizado).


---


\