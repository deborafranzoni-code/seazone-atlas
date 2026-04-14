<!-- title: Frontend | url: https://outline.seazone.com.br/doc/frontend-788G10k4d4 | area: Tecnologia -->

# Frontend

## **Dependências de ambiente de desenvolvimento, staging e produção**

* **1.** **Framework React e Utilitários**
  * [\*\*react](https://pt-br.reactjs.org/docs/getting-started.html) -\*\* framework para implementar as interfaces
  * [\*\*react-dom](https://www.npmjs.com/package/react-dom) -\*\* *Este pacote serve como ponto de entrada para o DOM e renderizadores de servidor para React. Destina-se a ser emparelhado com o pacote React genérico, que é enviado como* `react`npm.
  * [\*\*react-router-dom](https://www.npmjs.com/package/react-router-dom) -\*\* *disponibiliza recursos para lidar com rotas no React*
  * [\*\*react-scripts](https://www.npmjs.com/package/react-scripts) -\*\* *inclui scripts e configuração usados pelo **[Create React App](https://github.com/facebook/create-react-app)***
  * [\*\*babel-loader](https://www.npmjs.com/package/babel-loader) -\*\* *permite* transpilar arquivos JavaScript usando **[Babel](https://github.com/babel/babel)** e **[webpack](https://github.com/webpack/webpack)** .
  * [\*\*react-is](https://www.npmjs.com/package/react-is) -\*\* *permite testar valores arbitrários e ver se eles são um tipo de elemento React específico*
  * [\*\*web-vitals](https://www.npmjs.com/package/web-vitals) -\*\* A `web-vitals`biblioteca é uma biblioteca modular pequena para medir todas as métricas do **[Web Vitals](https://web.dev/vitals/)** em usuários reais, de uma forma que corresponda com precisão como eles são medidos pelo Chrome e relatados a outras ferramentas do Google (por exemplo, **[Chrome Relatório de experiência do usuário](https://developers.google.com/web/tools/chrome-user-experience-report)** , **[Page Speed Insights](https://developers.google.com/speed/pagespeed/insights/)** , **[Relatório de velocidade do Search Console](https://webmasters.googleblog.com/2019/11/search-console-speed-report.html)**)
* **2. Material UI Design / Pacotes de ícones**
  * [\*\*Material UI](https://mui.com/pt/) -\*\* *disponibiliza componentes customizados (ex: TextFields, DatePickers, Dropdowns, etc)*
  * [\*\*Material UI Icons](https://mui.com/pt/material-ui/material-icons/) -\*\* disponibiliza ícones
  * [\*\*react-feather](https://www.npmjs.com/package/react-feather) -\*\* *disponibiliza uma coleção de ícones de código aberto*
* **3. Pacotes para estilizar componentes React**
  * [\*\*styled-components](https://www.npmjs.com/package/styled-components) -\*\* *permitem escrever código CSS para estilizar componentes React*
  * [\*\*color](https://www.npmjs.com/package//color) -\*\* *permite fazer a conversão e manipulação de cores imutáveis com suporte para strings de cores CSS*
* **4. Pacotes para manipular datas**
  * [\*\*Date-fns](https://date-fns.org/) -\*\* permite *manipular datas*
  * [\*\*moment](https://momentjs.com/) -\*\* permite *manipular datas*
  * [\*\*moment-range](https://www.npmjs.com/package/moment-range) -\*\* *permite manipular ranges de datas*
* **5. Pacotes para manipular e validar formulários**
  * [\*\*formik](https://formik.org/docs/overview) -\*\* *permite manipular formulários*
  * [\*\*yup](https://www.npmjs.com/package/yup) -\*\* *permite validar formulários*
* **6. Pacotes para manipular requisições http**
  * [\*\*axios](https://axios-http.com/ptbr/docs/intro) -\*\* *permite o front se comunicar com o back e fazer solicitações http*
* **7. Componentes customizados**
  * [\*\*react-calendar](https://www.npmjs.com/package/react-calendar) -\*\* *disponibiliza um componente de calendário customizado*
  * [\*\*react-circular-progressbar](https://www.npmjs.com/package/react-circular-progressbar) -\*\* disponibiliza *componente de barra de progresso circular*
  * [\*\*react-dnd](https://react-dnd.github.io/react-dnd/about) -\*\* *disponibiliza um* *conjunto de utilitários React que permite construir interfaces complexas de arrastar e soltar (Drag-and-drop)*
  * [\*\*react-dnd-html5-backend](https://www.npmjs.com/package/react-dnd-html5-backend) -\*\* *backend HTML5 com suporte oficial para **[React DnD](http://react-dnd.github.io/react-dnd/)***
  * [\*\*react-dropzone](https://react-dropzone.js.org/) -\*\* *disponibiliza um hook (*`useDropzone`) para lidar com interfaces de arrastar e soltar (Drag-and-drop)
  * [\*\*react-virtualized](https://www.npmjs.com/package/react-virtualized) -\*\* *disponibiliza componentes para renderizar com eficiência grandes listas e dados tabulares*
* **8. Pacotes para manipular apis externas**
  * [\*\*react-ga4](https://www.notion.so/8db92720ac6849c6943983e857673d39?pvs=21) -\*\* *permite manipular eventos para analisá-los no [Google Analytics](https://analytics.google.com/)*
  * [\*\*react-gtm-module](https://www.npmjs.com/package/react-gtm-module) -\*\* *permite o front estabeler uma conexão com o [Google Tag Manager](https://tagmanager.google.com/)*
  * [\*\*react-onesignal](https://www.npmjs.com/package/react-onesignal) -\*\* *permite criar e enviar Push Notifications usando a api do [One Signal](https://documentation.onesignal.com/docs/onesignal-api)*
* **9. Pacotes para armazenar dados em cache**
  * [\*\*react-query](https://www.npmjs.com/package/react-query) -\*\* *disponibiliza hooks para buscar, armazenar em cache e atualizar dados assíncronos no React*
* **10. Outros / utilitários**
  * [\*\*@simonwep/selection-js](https://simonwep.github.io/selection/) - \*\**permite selecionar elementos da página (ex: a seleção do range de datas no multicalendário "pressionando e arrastando" o mouse)*
  * [\*\*file-saver](https://www.npmjs.com/package/file-saver) -\*\* *permite salvar arquivos no lado do cliente*
  * [\*\*filesize](https://www.npmjs.com/package/filesize) -\*\* *permite obter o tamanho de um arquivo (ex: 100kb, 10Mb, etc)*
  * [\*\*history](https://www.npmjs.com/package/history) -\*\* *permite gerenciar o histórico de sessões em qualquer lugar que o JavaScript seja executado*
  * [\*\*html2canvas](https://www.npmjs.com/package/html2canvas) -\*\* *permite realizar capturas/prints da página web*
  * [\*\*jspdf](https://www.npmjs.com/package/jspdf) -\*\* *permite gerar PDFs*
  * [\*\*jwt-decode](https://www.npmjs.com/package/jwt-decode) -\*\* *permite decodificar tokens JWT*
  * [\*\*react-intersection-observer](https://www.npmjs.com/package/react-intersection-observer) -\*\* *informa quando um elemento HTML entra ou sai da janela de visualização*
  * [\*\*use-context-selector](https://www.npmjs.com/package/use-context-selector) -\*\* *React Context e useContext são frequentemente usados para evitar o drill de prop, mas sabe-se que há um problema de desempenho. Quando um valor de contexto é alterado, todos os componentes que useContext serão renderizados novamente.* Para resolver este problema, **[o useContextSelector](https://github.com/reactjs/rfcs/pull/119)** é proposto
  * [\*\*scheduler](https://www.npmjs.com/package/scheduler) -\*\* *pacote para agendamento cooperativo em um ambiente de navegador. Necessário para usar a lib [use-context-selector](https://www.npmjs.com/package/use-context-selector)*
  * [\*\*uuid](https://www.npmjs.com/package/uuid) -\*\* *permite gerar uuids*

[Frontend](/doc/frontend-pPCLa3MyyR)