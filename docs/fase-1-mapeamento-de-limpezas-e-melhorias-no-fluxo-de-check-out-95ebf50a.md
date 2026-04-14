<!-- title: Fase 1 - Mapeamento de Limpezas e Melhorias no Fluxo de Check-out | url: https://outline.seazone.com.br/doc/fase-1-mapeamento-de-limpezas-e-melhorias-no-fluxo-de-check-out-urk5qlQtJT | area: Tecnologia -->

# Fase 1 - Mapeamento de Limpezas e Melhorias no Fluxo de Check-out

## **Visão Geral do Produto**

O objetivo desta fase é **estruturar e automatizar o fluxo operacional de check-out** das franquias, garantindo maior controle e rastreabilidade sobre as etapas de saída dos hóspedes e execução das limpezas. Essa fase visa substituir processos manuais e descentralizados, trazendo fluidez ao fluxo de limpeza, visibilidade em tempo real e integração com as operações de manutenção e danos.


---

## 🎯 Objetivo Principal

* Padronizar e digitalizar o processo de **check-out** e **gestão de limpezas** das franquias.
* Garantir que **nenhum imóvel seja finalizado sem confirmação da limpeza**.
* Criar uma **base unificada de responsáveis pela limpeza**, com cadastro e reaproveitamento de contatos.
* Reduzir erros operacionais e aumentar a confiabilidade das informações de status pós-checkout.


---

## 🧩 Escopo da Fase 1

### **1. Fluxo de Mensagens de Pré Check-out**

* A franquia deve disparar as mensagens de **pré check-out** **01 dia antes da saída do hóspede**.
* O envio será manual, através de botão no card de check-out.
* Integração com WhatsApp (via envio padrão já existente no sistema).


---

### **2. Registro de Horários e Limpeza**

* Após o envio do pré check-out, a franquia deve:

  
  1. Inserir **horário de saída do hóspede**.
  2. Definir **horário de limpeza do imóvel**.
  3. Escolher **pessoa responsável pela limpeza**.

#### **Campo "Equipe de Limpeza"**

* Campo de busca com **autocomplete** por nome.
* Caso o nome não exista, a franquia poderá **cadastrar diretamente** (nome + telefone).
* Após o cadastro, o nome passa a aparecer automaticamente nas próximas buscas.


---

### **3. Disparo da Limpeza**

* No **dia do check-out**, a franquia deve clicar em **"Disparar limpeza"** através de um botão no card de check-out.
* O sistema enviará o **formulário de limpeza via WhatsApp** para a pessoa cadastrada.


---

### **4. Simplificação do Card de Check-out**

#### **Remover do card:**

* Formulário de check-out do hóspede
* Mensagem de feedback
* Dados sobre limpeza e danos do hóspede

#### **Manter e/ou adicionar ao card:**

* Código da reserva
* Detalhes da reserva
* Campos para:
  * Horário de saída
  * Horário de limpeza
  * Equipe de limpeza (com autocomplete e cadastro)
* Botão "Enviar formulário de limpeza por WhatsApp"
* Tag de status da limpeza:
  * 🟢 **Limpeza concluída**
  * 🟡 **Limpeza pendente**
  * 🔴 **Ocorrência detectada**

#### **Regras de Finalização do Card:**

| Situação | Ação permitida |
|----|----|
| Limpeza feita, sem ocorrências | Pode finalizar o card |
| Limpeza feita, com ocorrências | Exibir link "Ver Ocorrências" |
| Limpeza não realizada | Não pode finalizar o card |


---

### **5. Formulário de Limpeza**

#### **Conteúdo do Formulário**

* Código e localização do imóvel
* Nome do hóspede
* Horário da limpeza
* Perguntas de checklist (baseadas no [modelo](https://docs.google.com/forms/d/1COr9XJaOYbn1HFe4SPVtoiyy4eKDpTwVk13j5j0mJmg/edit))
* Caso alguma pergunta aponte problema:
  * **Obrigatório envio de foto ou vídeo**
* No final, **obrigatório envio de vídeo curto do estado geral do imóvel**


---

### **6. Tela de Acompanhamento de Limpezas**

Nova tela para gestão operacional das franquias.

#### **Funcionalidades:**

* Exibir todas as **limpezas do dia** (com filtros por status e data)
* Mostrar status:
  * Finalizadas
  * Pendentes
  * Com ocorrência
* Permitir **visualizar ocorrências** e **classificá-las** como:
  * ✅ Falso positivo
  * 💢 Dano de hóspede
  * 🔧 Manutenção necessária

#### **Ações baseadas na classificação:**

* **Dano de hóspede:** redireciona para o módulo de lançamento de danos.
* **Manutenção:** cria automaticamente um **card no Pipefy** de manutenção.


---

## 🧠 Regras de Negócio Principais


1. Não é possível finalizar o card de check-out enquanto a limpeza não estiver marcada como **concluída sem ocorrências**.
2. O cadastro de nova pessoa de limpeza deve persistir e ficar disponível para todas as futuras buscas da franquia.
3. Ocorrências de limpeza devem ser registradas e categorizadas para rastreabilidade futura.
4. Cada limpeza só pode ser marcada como concluída após o **envio completo do formulário**, com os uploads obrigatórios.


---