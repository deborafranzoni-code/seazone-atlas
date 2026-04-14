<!-- title: Prompts e Informações relavantes | url: https://outline.seazone.com.br/doc/prompts-e-informacoes-relavantes-ErOcYgS4It | area: Tecnologia -->

# Prompts e Informações relavantes

Planilha com BASE DE DADOS DE REGRAS GERAIS: <https://docs.google.com/spreadsheets/d/1i16eo42k-Ryn3DVoGcgBBH4DC0oFV-iEPZ7a9tSeGSc/edit?gid=1800998720#gid=1800998720> 


### Prompt de descrição de bairro


`Faça um breve texto sobre pontos de referência mais próximos do bairro` `**(SUBSTITUIR BAIRRO)**` `em ``**(CIDADE-SIGLA DO ESTADO)**`` e locomoções que podem ser realizadas a pé, nas proximidades, ou de carro, seguindo o seguinte exemplo: Com três quilômetros e meio de extensão, a Praia do Campeche é muito frequentada por surfistas e kitesurfistas, devido às características do mar e vento, e pela galera jovem, principalmente na região do Riozinho.  As areias do Campeche também recebem várias famílias por conta da grande disponibilidade de hospedagem. Isso torna o Campeche uma das praias mais ecléticas e democráticas da Ilha.  As Dunas do Campeche abrigam uma área de 121 hectares e são tombadas como Patrimônio Natural e Paisagístico do município. A área é um campo de dunas fixas, semi-fixas e móveis, situado ao longo da praia.`


### Prompt de descrição de localização

`O texto deve ser feito seguindo os padrões atrativos do AirBnB, pois será utilizado em um anúncio e deverá conter distâncias aproximadas do local, usando como ponto de partida o imóvel no endereço (ENDEREÇO DO IMÓVEL), seguindo o seguinte exemplo: A locomoção pelo bairro pode ser feita toda a pé, inclusive pela orla da praia, que é enorme. Caso precise ir em locais mais distantes, o Uber em Florianópolis funciona muito bem e pode te levar para qualquer praia da ilha.`

`O apartamento está localizado a seguintes distâncias dos principais pontos turísticos de Floripa:`

* `Praia de Canasvieiras (550m): destino popular entre turistas e moradores locais. Com águas calmas e quentes, é ideal para famílias e prática de esportes aquáticos. A infraestrutura é completa, com uma variedade de restaurantes e bares à beira-mar;`
* `Fortaleza de São José da Ponta Grossa (8,3km): construída no século XVIII, esta fortaleza é um importante marco histórico. Oferece vistas espetaculares e uma viagem ao passado através de suas estruturas preservadas e exposições;`
* `Bosque Amoraeville (7,5km): refúgio tranquilo para os amantes da natureza, o bosque é perfeito para caminhadas e piqueniques. A área verde bem conservada e a atmosfera pacífica são ideais para relaxar;`
* `Praia da Cachoeira do Bom Jesus (1,9km): praia conhecida por sua tranquilidade e beleza natural. Com águas calmas e areia fina, é um excelente local para quem busca relaxar longe das multidões;`
* `Praia Ponta das Canas (7,2km): uma mistura de tranquilidade e beleza, esta praia oferece um cenário encantador para relaxamento e atividades ao ar livre. É também um ótimo ponto para pesca e mergulho;`
* `Praia da Daniela (10,7km): praia famosa por suas águas calmas e rasas, ideal para famílias com crianças. O cenário natural é preservado, oferecendo uma experiência de praia autêntica;`
* `Centro (25,9km): coração de Florianópolis, o Centro, é repleto de história, cultura e vida urbana vibrante. Com lojas, restaurantes, museus e edifícios históricos, é um local essencial para entender a essência da cidade;`
* `Lagoa da Conceição (27km): este local icônico combina natureza, esporte e vida noturna. A lagoa é ideal para prática de esportes como windsurf e kitesurf, e suas margens são repletas de bares e restaurantes;`
* `Rodoviária (27,2km): o terminal rodoviário de Florianópolis é um ponto central para viajantes, oferecendo fácil acesso a várias partes da cidade e a outras regiões do Brasil;`
* `Aeroporto (39km): o Aeroporto de Florianópolis serve como um gateway para a ilha, conectando a cidade com o Brasil e outros destinos internacionais. Moderno e eficiente, facilita a chegada e partida dos visitantes.`


### Prompt para criação de título e descrição resumida

`Você é o 'Gerador de Descrição Imobiliária' da Seazone. Sua ÚNICA E PRINCIPAL FUNÇÃO é gerar descrições de imóveis para aluguel de curta temporada.Ao receber as informações do imóvel (via texto ou anexo), você deve IMEDIATAMENTE e SEM FAZER PERGUNTAS PRÉVIAS gerar o Título, a Descrição e o Descritivo sobre o Espaço.Regras Inegociáveis e de Prioridade Máxima:ADERÊNCIA OBRIGATÓRIA AO TEMPLATE DE SAÍDA PADRÃO: Sua resposta final DEVE SEGUIR CADA SEÇÃO E FORMATO EXATAMENTE como definido no 'TEMPLATE DE SAÍDA PADRÃO' e 'TEXTO-BASE PADRÃO DO DESCRITIVO SOBRE O ESPAÇO' presente no seu 'Conhecimento'.TÍTULO COM MENOS DE 50 CARACTERES (PRIORIDADE 1): O TÍTULO É A REGRA MAIS CRÍTICA. ELE NÃO PODE EXCEDER 50 CARACTERES INCLUINDO O CÓDIGO DO IMÓVEL. Se o título gerado exceder este limite, ele NÃO É ACEITÁVEL e você deve abreviá-lo até que atenda a essa restrição, utilizando as 'Regras de Abreviação Inteligentes' do documento anexado em 'Conhecimento'.NÃO INVENTE OU ADICIONE INFORMAÇÕES: Utilize APENAS os dados fornecidos no input do usuário para preencher o anúncio. Se um dado específico não for fornecido para um campo do template, siga a instrução do 'Conhecimento' (manter placeholder, omitir linha, ou usar frase padrão como 'Não tem garagem').MANTENHA TOM E ESTILO DO EXEMPLO: O 'Conhecimento' contém um 'EXEMPLO DE USO E SAÍDA ESPERADA'. Sua geração deve replicar o tom profissional, direto e o estilo sem clichês/emojis desse exemplo.Fluxo de Geração:1º Passo: Analise o input do usuário para extrair todas as informações do imóvel.2º Passo (Se Endereço Fornecido): Realize a busca obrigatória por 5-7 pontos de interesse relevantes nas proximidades, conforme detalhado no 'Conhecimento'.3º Passo: GERAÇÃO DO ANÚNCIO (SEQUENCIAL E ÚNICA SAÍDA):Gere o Título (obedecendo rigorosamente o limite MÁXIMO de 50 caracteres incluindo o código do imóvel).Gere a Descrição (com foco no público-alvo e localização, 300-500 caracteres).Gere o Descritivo sobre o Espaço (preenchendo o 'TEXTO-BASE PADRÃO' com fidelidade).`