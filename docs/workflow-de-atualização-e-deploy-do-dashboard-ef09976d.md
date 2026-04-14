<!-- title: Workflow de Atualização e Deploy do Dashboard | url: https://outline.seazone.com.br/doc/workflow-de-atualizacao-e-deploy-do-dashboard-iyn0Mff9UV | area: Tecnologia -->

# Workflow de Atualização e Deploy do Dashboard

Claro! Explicar o fluxo de trabalho (workflow) é fundamental para que todos na equipe entendam como as atualizações chegam até o dashboard final.

Aqui está o resumo do processo de atualização e deploy, desde a sua máquina local até o app hospedado no Streamlit Cloud.


---

### **Workflow de Atualização e Deploy do Dashboard**

O processo se divide em 3 fases principais: **Desenvolvimento Local**, **Controle de Versão (Git)** e **Deploy Automático na Nuvem**.

#### **Fase 1: Desenvolvimento e Testes Locais ("Rodando")**

Esta é a fase onde você faz e valida todas as mudanças no seu computador, antes de torná-las públicas.


1. **Fazer as Alterações no Código:**
   * Você abre os arquivos (ex: `2_data_prepar.py`, `streamlit_app.py`) no seu editor (VS Code).
   * Implementa as novas funcionalidades ou correções.
2. **Gerar Novos Dados (se necessário):**
   * Se a mudança envolver novas métricas ou queries, você precisa rodar os scripts de preparação.
   * Ex: `python scripts/1_import_data.py` e depois `python scripts/2_data_prepar.py`.
   * Isso gera os novos arquivos CSV na pasta `data/processed`.
3. **Testar o App Localmente:**
   * No terminal, dentro da pasta do projeto, você roda o Streamlit.
   * `streamlit run app/streamlit_app.py`
   * Você acessa `http://localhost:8501` no seu navegador.
   * **Importante:** Teste exaustivamente as novas funcionalidades. Verifique se os gráficos aparecem, se os filtros funcionam, se não há erros, etc.

#### **Fase 2: Salvar as Mudanças no Git ("Subindo para o Git")**

Após testar e confirmar que tudo funciona localmente, você "salva" a versão do código no repositório do GitHub. Isso cria um histórico de todas as alterações.


1. **Verificar o Status:** No terminal, na pasta do projeto, veja quais arquivos foram alterados.

   ```bash
   git status
   ```
2. **Adicionar Arquivos Modificados:** Adicione todos os arquivos que você quer salvar.

   ```bash
   git add .
   ```

   (O `.` significa "todos os arquivos modificados e novos")
3. **Criar um "Commit":** Crie um registro da mudança com uma mensagem descritiva.

   ```bash
   git commit -m "feat: Adiciona análise de Preço Mínimo (Pmin) e status de System Price"
   ```
   * **Dica:** Use mensagens claras. `feat:` para nova funcionalidade, `fix:` para correção de bug.
4. **Enviar para o GitHub (Push):** Envie suas alterações para a branch `dash-v1_01` no repositório remoto.

   ```bash
   git push origin dash-v1_01
   ```

#### **Fase 3: Deploy Automático no Streamlit Cloud ("Hospedado na Nuvem")**

Esta é a parte mais simples, pois é **automática**.


1. **A Mágica Acontece:** O Streamlit Cloud está configurado para "observar" a sua branch `dash-v1_01` no GitHub.
2. **Notificação Automática:** Quando você executa o `git push`, o GitHub envia uma notificação para o Streamlit Cloud, dizendo: "Há um novo código disponível!".
3. **Atualização do App:** O Streamlit Cloud automaticamente:
   * Puxa o novo código do GitHub.
   * Instala as dependências listadas no seu `requirements.txt`.
   * Reinicia sua aplicação com o novo código.

Se tudo correr bem, em alguns minutos seu app online já estará atualizado com as novas funcionalidades. Se houver algum erro, o Streamlit Cloud mostrará um log de deploy para ajudar a identificar o problema.

### **Resumo do Fluxo (Checklist)**


1. **\[Local\]** Fazer as mudanças no código.
2. **\[Local\]** Rodar os scripts de dados, se necessário.
3. **\[Local\]** Testar tudo com `streamlit run`.
4. **\[Git\]** `git add .`
5. **\[Git\]** `git commit -m "mensagem clara"`
6. **\[Git\]** `git push origin dash-v1_01`
7. **\[Nuvem\]** Aguardar o Streamlit Cloud atualizar automaticamente.