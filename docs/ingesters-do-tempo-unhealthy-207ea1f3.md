<!-- title: Ingesters do tempo unhealthy | url: https://outline.seazone.com.br/doc/ingesters-do-tempo-unhealthy-pebQ6nUKux | area: Tecnologia -->

# Ingesters do tempo unhealthy

---

### ✅ \[Recuperação de Hash Ring no Grafana Tempo: Limpeza de Ingesters Unhealthy\]

#### 🧭 Contexto

Tudo começou quando os dashboards que monitoram a latência das aplicações simplesmente pararam de funcionar. Investigando o motivo, a gente viu que as aplicações estavam dando erro na hora de enviar os traces (como o erro de Axios 400 que aparece na **Imagem 1**), o que interrompeu a geração das métricas.

O problema técnico era que os pods do Tempo estavam travados: eles apareciam como Running, mas não ficavam Ready (aquele estado 0/1 que dá pra ver nas **Imagens 2, 4 e 5**). Olhando os logs, a gente achou o culpado: uma mensagem dizendo que existiam instâncias com problema no ring e que os novos pods não ficariam prontos até que isso fosse resolvido.

A nossa principal hipótese é que isso tenha a ver com a mudança de nodepools que fizemos recentemente. É bem provável que, durante a realocação das instâncias, alguns nós antigos não tenham respondido o heartbeat a tempo e ficaram "pendurados" como **Unhealthy** no sistema (exatamente como mostra a **Imagem 3**), sujando o ring e travando a entrada dos pods novos.

#### ✅ Padrão Adotado

Para resolver o bloqueio e permitir que os novos pods assumam o tráfego, o procedimento padrão de limpeza manual deve ser seguido:


1. **Acesso ao Painel de Administração:** Realizar um port-forward para o serviço do distributor (ou qualquer componente que exponha o ring):

   ```bash
   kubectl port-forward svc/tempo-distributor 3200 -n <namespace>
   ```
2. **Intervenção Manual via UI:** Acessar `http://localhost:3200/ingester/ring` no navegador. Identificar todos os nós com o status **UNHEALTHY** e clicar no botão **"Forget"** para removê-los do anel.
3. **Configuração de Prevenção (Recomendado):** Adicionar a configuração de `autoforget` no YAML do Tempo para automação em futuras migrações:

   ```yaml
   tempo:
     ingester:
       lifecycler:
         ring:
           heartbeat_timeout: 1m
           autoforget_unhealthy: true # Remove automaticamente nós mortos após o timeout
   ```

#### 🎯 Justificativa

O Grafana Tempo depende da integridade do anel de hash para distribuir spans de trace de forma consistente. Se o anel contém nós marcados como ativos, mas que estão inacessíveis (unhealthy), o sistema impede que novos nós se tornem "Ready" para evitar corrupção de dados ou perda de consistência. A limpeza manual (ou automatizada via config) força o reequilíbrio dos *tokens* entre os pods saudáveis.

#### 📝 Observações

**Evidências do Incidente:**

* **Estado dos Pods:** Os pods permaneciam em loop de prontidão (conforme Imagens 2, 4 e 5), travados em `0/1`.
* **Interface do Ring:** A Imagem 3 demonstra claramente os nós de `tempo-ingester-5` a `9` com status **UNHEALTHY**, retendo fatias da carga de trabalho que deveriam estar nos novos pods.
* **Erro de Aplicação:** A Imagem 1 mostra que falhas na ingestão (AxiosError 400) podem ocorrer em ferramentas conectadas (como n8n ou SDKs de tracing) enquanto o ring não é estabilizado.

  \