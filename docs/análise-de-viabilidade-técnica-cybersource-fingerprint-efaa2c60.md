<!-- title: Análise de Viabilidade Técnica: CyberSource Fingerprint | url: https://outline.seazone.com.br/doc/analise-de-viabilidade-tecnica-cybersource-fingerprint-pNpV3stwkk | area: Tecnologia -->

# Análise de Viabilidade Técnica: CyberSource Fingerprint

# Fingerprint da CyberSource

## Preocupações/Dúvidas


1. Precisamos adicionar uma tag/script da cybersource na nossa página de checkout. A recomendação é que a gente execute esse código da tag o mais cedo possível, pois o idela é que tenha de 5 a 10 segundos entre o disparo da tag e a submissão do pedido. Isso gera preocupação porque se esse proceso precisar de algum dado do usuário (ex: email, visitor_id), só seria possível executar ele depois que o hóspede clicar em pagar, se assim for, entendo que ao clicar teremos que esperar os 10 segundos, o que pode gerar uma péssima experiência para o usuário. Ademais, muitos processos já ocorrem ao clicar nessa botão. (fonte: pdf)
2. O MerchantID seri ao da Tuna ou um da CyberSource?
3. O script da página de checkout já faz todo o trabalho de comunicação com a Cyber? Precisamos integrar com a API da Cyber de algum jeito? Precisamos obter o fingerprint gerado e enviar para a Tuna de alguma forma (ex: no PaymentInit)?

## Entendimentos

O diagrama disponível do PDF mostra uma interação com um serviço denominado ThreatMetrix Cloud, onde parece que enviaremos pra ele um sessionID. Esse processo seria feito via tag/scrpt da página de checkout. Lendo um pouco mais sobre, parece que é esse ThreatMetrix o responsável por criar um fingerprint para o CyberSource, isso seria feito a partir das variáveis descritas na tabela abaixo.

### **Variáveis do Fingerprint**

A tabela a seguir apresenta as variáveis para configuração do Fingerprint com a Threatmetrix e Cybersource. (fonte: <https://docs.cielo.com.br/risco/docs/fingerprint-cybersource#como-configurar-o-fingerprint-na-cybersource>)

| **VARIÁVEL** | **DESCRIÇÃO** | **VALOR** | **FORMATO** | **TAMANHO** |
|----|----|----|----|----|
| `org_id` | Indica o ambiente na Threatmetrix: Sandbox ou Produção. | Sandbox = 1snn5n9w<br>Produção = k8vif92e | String | 08 |
| `ProviderMerchantId` | Identificador da sua loja ou operação, fornecido pela Braspag, no formato braspag_nomedaloja.* \*É diferente do MerchantId\*\*. | Fornecido pela Braspag após a contratação. | String | 30 |
| `ProviderIdentifier` | Variável que você deve gerar para identificar a sessão. Recomendamos usar um GUID. É o valor que será enviado no campo `Customer.BrowserFingerprint`. | Personalizado | GUID ou String, na qual são aceitos inteiro, letra maiúscula ou minúscula, hífen e "_" (*underscore*). | 88 |
| `session_id` (para web) | Concatenação das variáveis `ProviderMerchantId` e `ProviderIdentifier`. O valor do `session_id` irá compor a [URL da Threatmetrix](https://docs.cielo.com.br/risco/docs/web-fingerprint#1-preencha-a-url-da-threatmetrix) que será enviada no [script](https://docs.cielo.com.br/risco/docs/web-fingerprint#2-adicione-as-tags-ao-script) da integração web. | Personalizado | `ProviderMerchantIdProviderIdentifier` | 118 |
| `MyVariable` (para mobile) | Concatenação das variáveis `ProviderMerchantId` e `ProviderIdentifier`. Veja mais detalhes em [6. Crie a variável de identificação da sessão](https://docs.cielo.com.br/risco/docs/fingerprint-android#6-crie-a-vari%C3%A1vel-de-identifica%C3%A7%C3%A3o-da-sess%C3%A3o) | Personalizado | `ProviderMerchantIdProviderIdentifier` | 118 |

## Tarefas

\[ Front \] Adicionar o script/tag na página de checkout: precisaria obter o `last_visitor_id` do usuário para passar como sessionID no script.

# Fontes

[CYBS_FINGERPRINT-Integration_ptbr_v2 (1).pdf 536437](/api/attachments.redirect?id=4eab2fd0-ff47-4138-942f-8a31f0ec9dd4)

<https://docs.cielo.com.br/risco/docs/web-fingerprint>

<https://docs.cielo.com.br/risco/docs/fingerprint-cybersource>

<https://docs.cielo.com.br/risco/docs/fingerprint-cybersource#como-configurar-o-fingerprint-na-cybersource>