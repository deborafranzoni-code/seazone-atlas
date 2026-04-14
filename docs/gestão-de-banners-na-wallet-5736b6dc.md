<!-- title: Gestão de Banners na Wallet | url: https://outline.seazone.com.br/doc/gestao-de-banners-na-wallet-aUUAAmi7Qq | area: Tecnologia -->

# 📸 Gestão de Banners na Wallet

## ℹ️ Descrição

Este documento descreve o processo completo para atualização de banners na plataforma **[Wallet](https://wallet.seazone.com.br)** utilizando o [PostHog](https://us.posthog.com/project/106793/feature_flags?tab=overview). A premissa é permitir que os banners da aplicação possam ser atualizados de forma no-code e sem necessidade de deployments.

### 🔧 Pré-requisitos

**Acessos Necessários**

* Acesso à conta da Seazone Hosting no [PostHog](https://us.posthog.com/project/106793/feature_flags?tab=overview)
* Acesso ao ambiente de [Produção da Wallet](https://wallet.seazone.com.br) 
* Acesso ao ambiente de [staging da Wallet](https://stg-wallet.seazone.com.br) (opcional, para validação antes de lançar ao usuário)

**Recursos Preparados**

* Imagem do banner:
  * Formato recomendado: JPG/PNG/WEBP
  * Proporções:
    * Home: `700x160` (Desktop) | `410x95` (Mobile)
    * Meus imóveis:`660x270`(Desktop) | `405x95` (Mobile)
  * Link válido da imagem no Google Drive/S3
* URL de destino para redirecionamento do banner
* (Opcional) Texto alternativo à imagem para fins de acessibilidade


---

## 🔁Processo

### 1. Upload das Imagens (Amazon S3/Google Drive)

Antes de configurar o banner, as imagens precisam estar hospedadas na internet. Para isso, você pode utilizar um dos serviços acima, se atentando apenas para algumas premissas:\n

**1.1. Upload via S3**

* Acesse o serviço **S3** no console da AWS.
* Abra o bucket público: `**seazone-wallet**`.
* Faça o upload dos arquivos de imagem (versão Desktop e Mobile).
* Após o upload, clique no arquivo e copie a **URL do objeto**

  
:::tip
  Dica: Abra o link em uma aba anônima para garantir que a imagem carrega corretamente.

  :::


**1.2. Upload via Drive**

* Acesse o Google Drive
* Faça o upload dos arquivos de imagem (versão Desktop e Mobile).
* Após o upload, clique com o botão direito e selecione a opção "**Compartilhar**"
* Certifique-se que o arquivo está aberto para **Qualquer pessoa com o link** (e não somente convidados ou Seazone Serviços)
* Após configurar as permissões, clique em **Copiar link**

  \


---


### 2. Configuração no PostHog

* Faça login no **PostHog**.
* No menu lateral, navegue até **Feature Flags**.
* Utilize a barra de busca para encontrar a flag do banner que deseja alterar:
  * 🏠 Para a Home: procure por `**ff_banner_home**`
  * 🏢 Para a área de Imóveis: procure por `**ff_banner_my_properties**`

 ![](/api/attachments.redirect?id=d339b456-69b8-46dc-9d2a-d114ff6df164 " =813x298")



---


### 3. Atualizando o Conteúdo (Payload)

Ao abrir a Feature Flag desejada:

* Certifique-se de que a flag está **Enable** (Ativada). *Se estiver desativada, o banner não aparecerá no site.*
* Role até a seção **Payload**.
* Você verá um código no formato JSON. Você deve substituir os valores que estão entre aspas `" "`, mantendo a estrutura do código intacta.

 ![](/api/attachments.redirect?id=ddfac3f9-c2ac-4a3f-8a42-15b0f7fe1c0a " =770x302")

**Estrutura do JSON (Copie e cole se necessário):**

```javascript
{
    "image": {
        "desktop": "COLE_AQUI_A_URL_DA_IMAGEM_DESKTOP",
        "mobile": "COLE_AQUI_A_URL_DA_IMAGEM_MOBILE"
    },
    "link": "COLE_AQUI_O_LINK_DE_REDIRECIONAMENTO",
    "alt": "ESCREVA_AQUI_O_TEXTO_DESCRITIVO_DO_BANNER"
}
```

#### 📝 Detalhamento dos Campos

* `**image.desktop**`: Link da imagem (S3) para telas grandes (computadores).
* `**image.mobile**`: Link da imagem (S3) para celulares.
* `**link**`: A URL para onde o usuário será enviado ao clicar no banner. É extremamente importante que essa url contenha o prefixo `https://`
* `**alt**`: Texto alternativo para acessibilidade (leitores de tela) e caso a imagem não carregue.

#### ✅ Exemplo Prático

Se você estiver subindo uma campanha para o "Campeche SPOT", o payload ficará assim:

```javascript
{
    "image": {
        "desktop": "https://seazone-wallet-stg.s3.sa-east-1.amazonaws.com/images/banners/banner_meusimoveis_desktop.jpg",
        "mobile": "https://seazone-wallet-stg.s3.sa-east-1.amazonaws.com/images/banners/banner_meusimoveis_mobile.jpg"
    },
    "link": "https://institucional.seazone.com.br/marketplace/novo-campeche-spot/",
    "alt": "Banner da Campanha do Campeche SPOT"
}
```

### ⚠️ Cuidados Importantes


:::warning
**Não remova as aspas e vírgulas:** O formato JSON é sensível. Se apagar uma aspa ou vírgula, o banner pode parar de funcionar.


**Cache:** A atualização é quase instantânea, mas pode levar alguns minutos para refletir para todos os usuários dependendo da conexão. Por via das dúvidas, um F5 é sempre válido ;)

:::



---


## Boas práticas

Para evitar erros visíveis aos usuários finais, é sempre bom validar a alteração inicialmente no ambiente de testes da Wallet (staging). Para isso, siga este fluxo de segurança:


1. **Configure no Staging:** Realize o setup da feature flag primeiro no projeto/ambiente de **Staging** do PostHog.

   ![](/api/attachments.redirect?id=f9520a85-c24b-45ee-adfc-4669c3d1d677 " =577x309")

   \
2. **Valide Visualmente:** Acesse a **Wallet Staging** e verifique:
   * A imagem carregou corretamente no Desktop e no Mobile?
   * O clique no banner está redirecionando para o link correto?
   * O layout da página quebrou ou sofreu alterações indesejadas?

     \
3. **Replique para Produção:** Apenas após confirmar que tudo funciona perfeitamente no ambiente de testes, copie o JSON validado e aplique no ambiente de **Produção** do PostHog.