<!-- title: Franquia Seazone - Projeto VibeCode | url: https://outline.seazone.com.br/doc/franquia-seazone-projeto-vibecode-xf1GeYDuaZ | area: Tecnologia -->

# Franquia Seazone - Projeto VibeCode

# DOCUMENTO DE PLANEJAMENTO – Sistema Operacional Franquia Seazone


---

## 1. Visão Geral

* Objetivo

Criar sistema de franquias no qual é possível realizar todas as tarefas operacionais de reserva, acompanhar gestão financeira e faturamento

* Público-alvo

Franquias seazone

* Métricas de sucesso

Quantidade de checkin realizados 

Quantidade de checkouts realizados 

Manutenções finalizadas 

Reembolsos pagos 


---

## 2. Arquitetura do Sistema

### 2.1 Módulos

* Dashboard/home
* Operacional
  * Check-in
  * Check-out
  * Danos de hóspede 
  * Reembolso 
  * Manutenção recorrente
  * Implantação
  * Reservas
  * Carteira de Imóveis
* Gestão Financeira 
  * Dashboard de faturamento
* Gestão e Comunicação 
  * Score da Franquia
  * Portal 360

    \
    \


---

## 3. Perfis e Permissões

Na versão inicial do MVP contará com apenas 01 usuário, sendo ele o host


---

## 4. Jornada Principal

### Princípio Estrutural

O sistema deve ser **orientado à reserva**, porque:

* Toda operação nasce de uma reserva
* Check-in e check-out dependem dela
* Danos derivam dela
* Reembolso deriva dela
* Faturamento deriva dela
* Manutenção pode ser consequência dela


---

### Jornada Principal (Macro)

A jornada principal completa é:

> Reserva confirmada → Preparação → Check-in → Estadia → Check-out → Vistoria → Danos/Reembolso (se houver) → Consolidação Financeira


---

## 5. Regras de Negócio por Feature

[Lista de features macro](https://outline.seazone.com.br/doc/lista-de-features-macro-FYaCxWkxOv)

[Check-in da Franquia](https://outline.seazone.com.br/doc/check-in-da-franquia-bWdkcZTWzT)

[Fluxo de Tarefas de Checkout](https://outline.seazone.com.br/doc/fluxo-de-tarefas-de-checkout-Vxt1vlNbx7)

[Danos de Hóspede](https://outline.seazone.com.br/doc/danos-de-hospede-0UYEZZcYkv)

[Reembolso](https://outline.seazone.com.br/doc/reembolso-PWVGaIPsQ7)

[Visualizar reservas](https://outline.seazone.com.br/doc/visualizar-reservas-LdIUK6Hauc)

Gestão Financeira 


---


6. ## Roadmap de Entregas

| Feature | STATUS | Responsável | VALIDADO | Semana de Entrega Prevista | Entrega |
|----|----|----|----|----|----|
| Login | MUST HAVE | Bessa |    | 10/03/26 | Ok - 10/03 |
| Home  | MUST HAVE | Bessa |    | 10/03/26 | Ok - 10/03 |
| Notificação | NICE TO HAVE | Ralph |    | 24/03 |    |
| Check-in  | MUST HAVE | Bruno/Bessa/Ralph |    | 10/03/26 | OK 10/03<br> |
| Check-out | MUST HAVE | Bruno |    | 10/03/26 | 17/03<br>- falta formulário de limpeza |
| Danos de Hóspede | MUST HAVE | Bessa |    | 17/03/26 | OK - 17/03 |
| Reembolso | MUST HAVE | Ralph |    | 17/03/26 | EM TESTE - 17/03 |
| Visualizar Reservas e fazer bloqueio | MUST HAVE | Bruno/Bessa |    | 17/03/26 | falta integrar pra fazer pra fazer bloqueio - 17/03 |
| Financeiro | MUST HAVE | Bessa |    | 24/03/26 | OK - 17/03 |
| Dados Bancário | MUST HAVE | Bessa |    | 24/03/26 |    |
| Manutenção | NICE TO HAVE | Bessa |    | 24/03/26 |    |
| Implantação | NICE TO HAVE | Bessa |    | 31/03/26 |    |