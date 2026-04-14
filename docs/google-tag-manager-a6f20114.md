<!-- title: Google Tag Manager | url: https://outline.seazone.com.br/doc/google-tag-manager-ndxp3Sv4kx | area: Tecnologia -->

# Google Tag Manager

## Inicialização do Tag Manager dentro do Sapron

Para fazer a inicializaçao/configuração do tag manager usamos a biblioteca 'react-gtm-module'.

A chave da propriedade é configurada dentro do .env do front na variável REACT_APP_TAG_MANAGER_KEY

O Google Tag Manager foi inicializado dentro do arquivo App.tsx passando pra função a váriavel que foi criada no .env

```tsx
const tagManagerArgs = {
  gtmId: process.env.REACT_APP_TAG_MANAGER_KEY as string,
};

TagManager.initialize(tagManagerArgs);
```

Dessa maneira é possivél criar várias versões do código e rastrear cada uma separadamente sendo possivél ter uma pra stagin, um pra produção e outro de teste alterando apenas a chave no .env.

<https://medium.com/finnovate-io/integrating-google-tag-manager-with-a-react-app-5a8584ee2251>