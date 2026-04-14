<!-- title: Discovery - Aviso de Novas Reservas | url: https://outline.seazone.com.br/doc/discovery-aviso-de-novas-reservas-gql5zN54U5 | area: Tecnologia -->

# Discovery - Aviso de Novas Reservas

#### **Contexto**

Este discovery foi conduzido com base na análise dos principais tickets abertos por hosts e em entrevistas com 11 franqueados, que compartilharam suas principais dores e insatisfações com a plataforma Sapron. O objetivo foi identificar oportunidades de melhoria que aprimorem a experiência do franqueado e maximizem os resultados operacionais. Os resultados das entrevistas e a proposta de solução foram apresentados e validados com Bernardo Lana, Iara Moraes e Daisi Marsaro, garantindo alinhamento estratégico e viabilidade.


---

#### **Objetivo Principal**

Identificar e propor soluções para os principais desafios enfrentados pelos franqueados, com foco em melhorar a organização e eficiência no gerenciamento de reservas instantâneas.


---

#### **Participantes das Entrevistas**

Foram entrevistados os seguintes franqueados, que gerenciam um número significativo de imóveis:


 1. Ana Márcia Pereira Buzzacchino - 26 imóveis
 2. Gabriela da Luz Nunes - 36 imóveis
 3. Katia Leite do Nascimento Emmel - 105 imóveis
 4. Nabiha Kasmas Denis - 61 imóveis
 5. Fábio Moreira Campos Monteiro - 27 imóveis
 6. Carlos Eduardo Inacio Diniz - 14 imóveis
 7. Matheus Peu (cohost de Rodrigo Ruas) - 15 imóveis
 8. Alan Mesquita Maciel - 21 imóveis
 9. Dineia Pedroso de Almeida - 29 imóveis
10. Madego Goias - 43 imóveis


---

#### **Problemática Identificada**

**Dificuldade de organização para reservas instantâneas**\nOs hosts relataram desafios significativos ao preparar imóveis quando recebem reservas instantâneas para o mesmo dia ou para o dia seguinte. A falta de comunicação ágil e automatizada resulta em atrasos e possíveis falhas na experiência do hóspede.


---

#### **Cenário Atual**

* Reservas instantâneas são realizadas com frequência (média de 1.800 por mês).
* Os franqueados não recebem alertas imediatos sobre essas reservas, o que dificulta o preparo do imóvel e a comunicação com o hóspede.
* A falta de automatização gera sobrecarga operacional e riscos de falhas no atendimento.


---

#### **Proposta de Solução**

**Envio de mensagens automáticas via WhatsApp**\nImplementar um sistema de alertas automáticos via WhatsApp para notificar os franqueados sobre reservas instantâneas realizadas para o mesmo dia ou para o dia seguinte.


---

#### **Detalhes da Solução**


1. **Gatilho para Alerta**
   * O alerta será acionado automaticamente quando uma reserva instantânea for realizada para o mesmo dia da solicitação
2. **Informações do Alerta**\nO alerta conterá os seguintes dados da reserva:
   * Código do Imóvel
   * Data de check-in e check-out
   * Nome do hóspede principal
   * Telefone de contato do hóspede
   * Mensagem padrão: *"Aviso: atualize a tela de controle no SAPRON para obter mais informações sobre a reserva e realizar o check-in."*
3. **Canal de Comunicação**
   * O alerta será enviado via WhatsApp para o número cadastrado nos dados pessoais do anfitrião.


---

#### **Insights e Dados Relevantes**

* **Volume de Reservas:** Em média, 1.800 reservas instantâneas são realizadas mensalmente, o que confirma a relevância da dor relatada pelos franqueados.
* **Impacto Operacional:** A falta de comunicação ágil resulta em atrasos no preparo dos imóveis e possíveis insatisfações dos hóspedes.


---

#### **Viabilidade Financeira**

* **Custo de Implementação - BLIP:** A integração com a API da Blip (já existente na empresa) tem um custo de **R$ 0,30 por mensagem enviada**, podendo gerar um **custo mensal de R$ 600,00.** 
* **Custo de Implementação - WhatsApp:** a integração com a API do WhatsApp ainda não está integrada, o que demandaria um tempo maior de implementação da feature, com um custo de **R$ 0, 048 por mensagem enviada**, podendo gerar um **custo mensal de R$ 86,40.**

  \n