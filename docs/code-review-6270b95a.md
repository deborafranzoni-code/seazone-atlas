<!-- title: Code review | url: https://outline.seazone.com.br/doc/code-review-pGfagwAgk5 | area: Tecnologia -->

# Code review

Pontos importantes para analisar durante o code review:

### Responsividade

* As páginas e componentes devem ser responsivos
* As páginas devem ser fiéis ao design do figma

### Segurança

* Verificar se todas as informações sensíveis (senhas, tokens, etc.) estão sendo armazenadas de forma segura e criptografadas.
* Verificar se nenhum dado sensível está exposto no network

### SEO

* Verificar se o título da página e as meta descrições são únicos e relevantes para cada página
* Páginas devem estar otimizadas para SEO
* As imagens devem ter atributo `alt` bem descritivo
* Nome das imagens devem ser bem descritivas e estar de acordo com padrão de projeto.
* Rich snipets <https://schema.org/>
* Verificar se conteúdo da página é indexável pelos motores de busca

### Clean code

* Verificar se o código segue boas práticas de programação e padrões da comunidade
* Boa nomenclatura dos componentes
* Verificar se há código duplicado