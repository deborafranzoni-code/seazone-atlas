<!-- title: Clean code na prática (Front-end) | url: https://outline.seazone.com.br/doc/clean-code-na-pratica-front-end-ttSmz3QN3S | area: Tecnologia -->

# Clean code na prática (Front-end)

## O que é clean code?

O Clean code tem 2 perguntas principais para o desenvolvedor

* `Legibilidade`: O código de fácil leitura e entendimento ?
* `Fácil manutenção`: Alguém com o mesmo conhecimento técnico consegue fazer a manutenção do meu código com confiança e previsibilidade?

Obs: Clean code não está ligado ao tamanho de linhas de código, se for necessário é melhor um código maior e mais facil de entender.

Para poder responder essas perguntas com solidez temos 5 pilares que devemos seguir

* **Testes automátizados: trás confiança no código que estamos escrevendo**
* **Revisão: além de verificar se a funcionalidade está correta, é crucial validar a conformidade com os padrões de projeto presentes no código.**
* **Refatoração: A evolução dos códigos só é obtida com a refatoração**
* **Simplicidade: KISS (Keep it simple and stupid)**
* **Iterações curtas: Faça commits e PRs pequenos mesmo que a feature não esteja completa tornando mais fácil de testar  e criar novas features**

## Padrões de código do Front-end SAPRON:

* Todo o código deve ser implementado no idioma Inglês sempre que possível
* Nome de variáveis e estados devem seguir o padrão *camelCase*: **Exemplo:** **dailyPrice**
* Ao criar um novo componente ou uma nova página deve-se seguir o seguinte padrão:
  * *ComponentName*\*\*.tsx\*\*
  * *index*\*\*.ts\*\*
  * *styles*\*\*.tsx\*\*
* As telas devem ser responsivas para mobile, exceto quando estiver especificado que a tela não deve ser responsiva no card do Jira
* Implementar, sempre que possível, componentes reutilizáveis
* Reutilizar, sempre que possível, componentes que já tenham sido implementados para evitar ter componentes redundantes no projeto

## Clean code Java Script

### Nomenclaturas de variáveis

* Evite diminutivos
* Evite nomes genéricos (data, params, response, list, args)

```jsx
// Código sujo

const users = ['Patrick', 'Ananda', 'Alysson', 'Bernardo'];
//filtered é genérico, u está no diminutivo.
const filtered = users.filter(u -> {
	return u.startWith('A');
))

// Código limpo
const users = ['Patrick', 'Ananda', 'Alysson', 'Bernardo'];
const usersStartingWithLetterA = users.filter((user) -> {
	return user.startWith('A');
))

//Código sujo
function getUsersProperties() {
// data não é semantico
	const data = getUsersProperties();
	return data;
};

//Código limpo
function getUsersProperties() {
	const userProperies = getUsersProperties();
	return userProperies;
}
```

### Booleanos

As variáveis booleanas geralmente salvam estados de alguma informação, assim escrevemos sempre como se fosse uma pergunta com uma resposta de sim ou não. Devemos começar utilizando is, does, has, etc.

```jsx
// Código sujo

const disabled = true;

// Código limpo

const isDisabledUsersModal = true;
const doesUserHasGroup = false
```

### Causa e Efeito

Nomeie as variáveis de acordo contexto da aplicação.

```jsx
// Código sujo

const Button = () => {
	// Variável criada com base no efeito da aplicação, devemos criar a variável
	// de acordo com a causa 
	const isButtonDisabled = true;
	return (
		<button disabled={isButtonDisabled}>
			<span>icone</span>
			{ isButtonDisabled ? 'Carregando' : 'Enviar' }
		</button>
	);
};

// Código limpo
const Button = () => { 
	const isFormSubmitting = true;
	return (
		<button disabled={isFormSubmitting}>
			<span>icone</span>
			{ isFormSubmitting ? 'Carregando' : 'Enviar' }
		</button>
	);
};
```

### Código em ingles

O inglês é a língua padrão na indústria de desenvolvimento de software em todo o mundo. Usar o inglês torna o código mais acessível e compreensível para desenvolvedores de diferentes origens e regiões.

### Regras condicionais

* Evite sempre que possível negações

```jsx
//Código sujo

const isUserOlderThan18Years = true;
const doesUserLivesOnBrazil = true;

if (!isUserOlderThan18Years && !doesUserLivesOnBrazil) {
	
}

//Código limpo

const isUserYoungerThan18Years = true;
const doesUserLivesOutsideBrazil = true;

if (isUserYoungerThan18Years && doesUserLivesOutsideBrazil) {
	
}

// Evitando negação a gente evita trocar o operador,ficando mais fácil de
// entender 
```

* Early return vs else

```jsx
// Devemos utilizar o else quando o early return está participando de uma
// função com grande porção de código
fuction isUserOlderThan18Years (user: User) {
	if (!user) {
		//muito código complexo aqui
		return 'erro'
	} else {
		return user.age >= 18;
	}
}

// Early return (mais utilizado)
fuction isUserOlderThan18Years (user: User) {
	if (!user) {
		return 'erro'
	} 
	return user.age >= 18;
}
```

* Evite condicionais aninhadas

```jsx
//Código sujo

function userHasMajority () {
	if (user.age > 18) {
		if(user.country === 'Brasil´) {
			retrun 'Atingiu maioridade';
		}
	}
return ´Não tem idade  suficiente';	
}

//Código limpo

function userHasMajority () {
	if (user.age > 18) {
		return ´Não tem idade  suficiente';
	}
	
	if(user.country === 'Brasil´) {
		retrun 'Atingiu maioridade';
	}
}
```

### Parâmetros e desestruturação

* Sempre tentar enviar parâmetros nomeados, isso permite que a função tenha descrito exatamente os campos  que ela está utilizando, assim ficando fácil de tirar de contexto caso necessário

```jsx
// Código sujo

// Rota para criação de usuário (name, email, password)
// Controller (name, email, password)
// Salvar no BD (name, email, password)

function createUserRoute (body) {
	//Validações do body
	createUserController(body)l;
};

function createUserControler(data) {
	db.createUser(data)
}

const db = {
	createUser(data) {
		// Cria usuário (name, email, password) 
	} 
}

//Código limpo

function createUserRoute (body) {
	const { name, email, password } = body;
	//Validações do body
	createUserController({ name, email, password });
};

function createUserControler(data) {
	const { name, email, password } = data;
	db.createUser({ name, email, password })
}

const db = {
	createUser({ name, email, password}) {
		// Cria usuário (name, email, password) 
	} 
}
```

* Prefira criar objetos para parametros da sua função

```jsx
// Código sujo
function createUserRoute (body, params) {
	const { name, email, password } = body;
	//Validações do body
	createUserController({ name, email, password });
};
createUserRoute({ name, email, password}, { id: 1 }); 
createUserRoute(null, { id: 1 }); // fica estranho, caso saia de contexto não
																	// da pra entender o que são as coisas

function createUserControler(data) {
	const { name, email, password } = data;
	db.createUser({ name, email, password })
}

//Codigo Limpo
function createUserRoute ({ body, params }) {
	const { name, email, password } = body;
	//Validações do body
	createUserController({ name, email, password });
};
createUserRoute(
	body: { name, email, password}, 
	params: { id: 1 },
); 
createUserRoute(
	body: null, 
	params: { id: 1 },
); 

function createUserControler(data) {
	const { name, email, password } = data;
	db.createUser({ name, email, password })
}
```

### Números mágicos

São cálculos que temos no nosso código que não são fáceis de saber o que significa sem um contexto do que está acontecendo

```jsx
//Código sujo

setTimeout(() -> {
	//função
}, 2592000000)

//Código limpo

const INTERVAL_30_DAYS = 1000 * 60 * 60 * 24 * 30;
setTimeout(() -> {
	//função
}, INTERVAL_30_DAYS)
```

### Syntatic Sugars

* Evite Syntatic sugars -  O termo "Syntatic sugars" refere-se a uma forma mais amigável ou mais conveniente de expressar algo em um código de programação. Em outras palavras, são construções de linguagem que não introduzem novos recursos ou funcionalidades, mas simplificam a sintaxe para tornar o código mais legível ou fácil de escrever.

## Clean code React

Como identificar que um componente precisa de uma refatoração?

Quando a sua camada de JavaScript estiver muito grande e complexa.

Quando separar um componente em componentes menores?


1. **Quando se tem algo repetitivo:**

   Analisar necessidade de separação, muitas vezes não é necessário quando a estrutura se repete, mas não tem nenhuma lógica envolvida, essa análise evita o excesso de componentização em um projeto.
2. **Quando é possível isolar algo do seu contexto, sem prejudicar o comportamento original:**

   Quando existe alguma variável, função, `useEffect`, etc. que está totalmente associado à uma parte específica da interface.

### Componentes puros

Quando se separa um componente em outros menores, é muito comum que se leve toda a lógica do *script* para o componente novo e às vezes essa lógica depende de comunicação com API/*back-end*, `useEffect()` em variáveis do componente pai, entre outros, nesses casos o componente criado não é um componente puro e sim um componente separado em dois arquivos.

Componente puro é um tipo de componente cuja existência não depende do contexto em que está, ele tem autonomia de funcionamento sem precisar de informações externas, desde que respeitadas suas propriedades.

Exemplo: o **Header** de uma aplicação contém um botão com uma função que adiciona uma nota em uma lista de notas, para ele se tornar um componente puro o correto seria criar uma *interface* que recebe justamente esta função a ser utilizada, assim o **Header** pode exister em qualquer outro contexto da aplicação desde que seja passado alguma função para ser executada no botão.

### Funções e eventos no React

Recomendação de prefixos para nomes de funções: `handle` e `on`.

Quando o componente está expondo algum evento a outro componente, prefira utilzar o prefixo `on`, semelhante aos efeitos do HTML `onClick`, `onFocus`, exemplos: `onSubmitForm()`, `onCreateNewUser()`.

Quando o objetivo da função é responder o disparo de um algum evento do usuário, prefira utilzar o prefixo `handle`, exemplos: `handleSubmitForm()`, `handleCreateNewUser()`.

```jsx
function onHover() {
	// code
}

async function handleGetData() {
	// code
}
```

### Composição vs. Customização

É muito comum durante a criação de componentes de Input que se definam configurações deste componente, como *label*, tipo, mensagem de erro, classe CSS, etc., essas propriedades podem ser obrigatórias ou opcionais e são recebidas pelo componente através de uma interface.

O problema em se fazer isso é que a estrutura do HTML acaba ficando engessada e de difícil expansão, por exemplo, caso no futuro eu precise customizar ainda mais esse *input*, adicionar um ícone ou que a mensagem de erro venha acima da *label* ou trocar o ícone de lado, o componente vai precisar receber ainda mais propriedades e criar casos condicionais de renderização, tornando um processo complexo.

A solução encontrada para isso é utilizar o *pattern* de composição, onde o componente-pai engloba os componentes-filhos, então o componente Input poderia ser divido em Label, Icon, InputField, etc., a disposição deles no HTML pode ser feita de forma mais fluída de acordo com a chamada dos respectivos componentes dentro do componente-pai.

```jsx
export function Root({ children }: RootProps) {
	return (
		<div>
			{children}
		</div>
	)
}

interface LabelProps extends LabelHTMLAttributes<HTMLLabelElement> {
	title: string;
}

export function Label(props: LabelProps) {
	return (
		<label {...props}>{props.title}</label>
	)
}

interface Input extends InputHTMLAttributes<HTMLInputElement> {}

export function Input(props: FormFieldProps) {
	return (
		<input {...props} />
	)
}

interface IconProps {
	children: ReactNode;
}

export function Icon({ children }: IconProps) {
	return (
		<span>
			{children}
		</span>
	)
}

interface ErrorMessageProps {
	message: string;
}

export function ErrorMessage({ message }: ErrorMessageProps) {
	return (
		<span>{message}</span>
	)
}

function InputComposição() {
	return (
		<Input.Root>
			<Input.Icon />
			<Input.Input>
			<Input.ErrorMessage />
		</Input.Root>
	);
}

interface InputCustomizaçãoProps {
	label?: string;
	initialIcon?: ReactNode;
	icon?: ReactNode;
	errorMessage?: string;
}

export function InputCustomização({
	label, 
	initialIcon, 
	icon, 
	errorMessage
}: InputProps) {
	return (
		<div>
			{label ? <label>{label}</label> : null}
			{initialIcon}
			<input type="text" />
			{icon}
			{errorMessage ? <span>{errorMessage}</span> : null}
		</div>
	)
}

function InputCustomização() {
	return (
		<Input 
			initialIcon={src/icon}
			placeholder="input"
			value={value}
			errorMessage="message"
			label="label"
		/>
	)
}
```

### Condicionais no *render*

Evite condicionais na camada HTML de seu código, prefira criar variáveis com o condicional na camada JavaScript.