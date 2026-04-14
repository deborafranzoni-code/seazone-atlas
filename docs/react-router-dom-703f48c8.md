<!-- title: React-Router-Dom | url: https://outline.seazone.com.br/doc/react-router-dom-sBQx2hUfg7 | area: Tecnologia -->

# React-Router-Dom

## Rotas - Layout - Navegação

O react-router-dom é uma biblioteca responsável por fazer as rotas, lidar com a navegação, utilizar os parametros das rotas e criar o layout das páginas do sistema. Para isso utilizamos componentes e hooks providos pela biblioteca.

## Como criar uma nova rota

Para criar uma nova rota no projeto devemos acessar o arquivo Router.tsx que está `/front/src/Router.tsx` através dele podemos identificar no código um componente `Route` aninhado a outro, eles são resposáveis pela chamada do layout, do roteamento das páginas e chamada dos componentes respectivamente.

```jsx
<Route path="/" element={<DefaultLayout />}>
  <Route
    path="/"
    element={(
      <RequireAuth
        permissions={mobile ? [] : []}
      >
        <InicialRedirect />
      </RequireAuth>
  )}
  />
</Route>
```

O componente RequireAuth é responsável pelas rotas privadas e por redirecionar para a página adequada do sistema caso o usuário tente acessar uma das páginas sem a permissão necessária ou caso não esteja logado.

# Navegação entre rotas

Com a atualização do react-router-dom o hook `useHistory`, antes muito usado no projeto, não existe mais. No lugar dele agora é utilizado o `useNavigate` que funciona de forma bem parecida

```jsx
import { useNavigate } from 'react-router-dom';

const function = () => {
	const navigate = useNavigate();
	
	return(
		<Component onClick={()=> navigate('/{path}')}>
	)
}
```

# Layouts

Atualmente o projeto possui dois layouts, o layout default que é o menu lateral e o o layout do owner que possui um header e um footer. caso queria utilizar algum deles é só criar um componente <Route /> aninhado ao <Route /> do layout, caso queira criar um novo layout devemos criar uma pasta dentro da pasta `/front/src/layouts` com a componentização do layout e chama-lo no arquivo Router.tsx.

No arquivo criado devemos codar a estrutura do layout normalmente e a parte que mudará devemos colocar o conponente `<Outlet />` presente na biblioteca.

```jsx
<>
      <MenuMobile />
      <Container>
        <MenuLateral
          setOpenMenu={setOpenMenuLateral}
          openMenu={openMenuLateral}
        />
        <Outlet />
        <BottomHeader />
      </Container>
    </>
```

# Documentação

<https://reactrouter.com/en/main>