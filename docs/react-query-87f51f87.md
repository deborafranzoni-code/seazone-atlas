<!-- title: React-Query | url: https://outline.seazone.com.br/doc/react-query-t4Xb2znPaZ | area: Tecnologia -->

# React-Query

## Rotas - Layout - Navegação

O react-query é uma biblioteca responsável por melhorar a experiência do usuário quando realizamos a busca de dados em uma API. Suponhamos que estamos na página de controle anfitrião onde foram carregados os cards de check-in, check-out e limpeza da semana, quando clicamos para ir para próxima semana fazemos outra chamada a API e recebemos os novos dados dessa página, hoje no sistema se quisermos voltar para primeira página precisaríamos fazer mais uma chamada para API recebendo os dados novamente, mas com o react-query funciona um pouco diferente, ele salva essas informações que já foram carregadas no cache local por um período de tempo e quando queremos acessá-la podemos fazê-la de forma instantânea. Mas isso também faz com que sincronizar esses dados sempre que tenha alguma mudança nele.

## Como configurar

Primeiro adicionamos a biblioteca utilizando o comando

```bash
**yarn add react-query**
```

Devemos criar um arquivo em services que exporte o queryClient pois ele será utilizado em vários aquivos.

```jsx
**import { QueryClient } from 'react-query';**

**const queryClient = new QueryClient();**
```

Após isso devemos importar o QueryClientProvider do react-query e o queryClient do services no App.tsx para envolver toda aplicação.

```jsx
**import { QueryClientProvider } from 'react-query';
import { queryClient } from './utils/QueryClient/QueryClient';**
```

então criamos um novo cliente e passamos ele como propriedade do provider

```jsx
**<*QueryClientProvider* *client*={queryClient}>
 ...
  <Routes />
 ...
</*QueryClientProvider*>**
```

# Listando dados - useQuery()

Para listar os dados devemos importar o hook useQuery  e para utilizá-lo passamos como primeiro parâmetro uma chave, um nome para identificar o dado no cache local, podemos passar uma string ('nome') ou para um vetor \['nome', —-\] para um retorno paginado, como segundo parâmetro passamos uma função que retornará os dados que serão salvos na cache e por fim como terceiro parâmetro recebemos um objeto com algumas configurações importantes, como a staleTime: que é responsável por ditar de quanto em quanto tempo os dados estarão "frescos" e o enable: que é responsável por fazer querys condicionais.

<aside> 💡 Obs: —- pode ser uma variável, um número, um objeto, etc.

</aside>

Utilizando o hook recebemos algumas informações que são importantes: data, isLoading, isSuccess, isError ajudando na tratativa da aplicação

```jsx
const { data, isLoading, isSucces, isError, ...} = useQuery(
    'event-checkin', 
		async () => {
      const data: RequestEvent[] = await getCheckinDates(
        dates[0].format('YYYY-MM-DD'),
        dates[mobile ? 0 : 6].format('YYYY-MM-DD'),
        'checkin',
      );
      return data;
    }, 
		{
      enabled: dates.length > 1
			staleTime: 1000 * 60 * 15 //15min
    },
  );
```

# Criar alterar ou deletar dados - useMutations()

Utilizamos esse recurso quando queremos fazer uma ação na api que não é de busca de dados, pode ser uma forma de criar, alterar ou deletar algo na nossa api. Para isso, primeiro devemos importar o hook useMutations e para utiliza-lo passamos como primeiro parâmetro a função que é responsável por fazer as requisições, como segundo parâmetro enviamos um objeto com os parâmetros que precisarmos (Principalmente o onSuccess, que utilizamos para invalidar as querys quando fazemos uma mudança nos dados.)

```jsx
const concludeCheckList = useMutation(async (newConcluded: boolean) => {
	await postChecklist(
	  reservation.id,
	  checkin,
	  checkout,
	  clearning,
	  checklistData,
	)},
  {
    onSuccess: () => {
      queryClient.invalidateQueries('event-list');
      queryClient.invalidateQueries('event-checkin');
      queryClient.invalidateQueries('event-checkout');
      queryClient.invalidateQueries('event-cleaning');
    },
  });
```

# Devtools

O react-query possui um console de desenvolvedor que lista os dados salvos, seu estado e todas as informações pelo devtools e para utiliza-lo é bem simples.. Primeiro você deve importar o componente

```jsx
**import { ReactQueryDevtools } from 'react-query/devtools';**
```

Após isso é só retornar o componente no fim do arquivo

```jsx
**return(
  <>
    {Componentes}
    <*ReactQueryDevtools* />
  </>
);**
```

## Para deixar o código mais limpo faça seu hook!

Para fazer seu hook, crie uma pasta e um arquivo na pasta hooks com o nome do seu hook (utilize use'Nome' para manter o padrão dos hooks). Nesse arquivo exporte uma função recebendo os parâmetros necessários e retorne a query.

```jsx
export function useEventCheckin(dates: Moment[], mobile: boolean) {
  let firstDate = null;
  if (dates.length > 0) {
    firstDate = dates[0].format('YYYY-MM-DD');
  }
  return useQuery(
    ['event-checkin', firstDate], async () => {
      const data: RequestEvent[] = await getCheckinDates(
        dates[0].format('YYYY-MM-DD'),
        dates[mobile ? 0 : 6].format('YYYY-MM-DD'),
        'checkin',
      );
      return data;
    }, {
      enabled: dates.length > 1 && firstDate !== null,
    },
  );
}
```

No arquivo utilize o hook desta maneira:

```jsx
const listCheckin = useEventCheckin(dates, mobile);
```

Link da documentação do React-Query: