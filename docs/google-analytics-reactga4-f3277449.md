<!-- title: Google Analytics (reactga4) | url: https://outline.seazone.com.br/doc/google-analytics-reactga4-z0KcRaajvg | area: Tecnologia -->

# Google Analytics (reactga4)

---

## Como analisar usuário novos e recorrentes no Sapron

O google analytics nos permite ver esses número dentro do relatório de Retenção. Para issó basta selecionar o período desejado e ele vai mostrar o número de usuário novos e o número de usuários recorrentes.

 ![novos usuários x recorrentes.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/novos_usurios_x_recorrentes.png)

# 1. **Visão geral de tecnologia usado pelos usuários Sapron**

Para ter um contexto geral sobre sistema operacional, categoria do dispositivo(desktop/mobile), navegador e resolução de tela usados pelos usuários do sapron.

Nessa aba ele vai mostra:

* Quandtidade de usuários por sistema operacional;
* Quantidade de usuários por categoria de dispositivo (desktop e mobile);
* Quatidade de usuários por navegador;
* Resolução de tela usadas pelos usuários;

 ![Captura de tela de 2022-12-02 09-02-05.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_09-02-05.png)

> Para saber informações mais detalhadas sobre as tecnologias usamos a aba explorar para criar relatórios personalizados.

## 1.1 Relatório de usuários por sistema operacional e navegador

 ![Captura de tela de 2022-12-02 09-53-15.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_09-53-15.png)

 ![Captura de tela de 2022-12-02 10-06-11.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-06-11.png)

Esse relatório lista todos os sitemas operacionais de onde o sapron foi acessado e o total de usuários divididos por navegador, permitindo visualizar:

* Quantidade de usuários windows que usam determinado navegador.
* Quantidade de usuários linux que usam determinado navegador.
* Quantidade de usuários ios que usam determinado navegador.
* Quantidade de usuários android que usam determinado navegador.

## 1.2 Relatório de usuários por página, sistema operacional e navegador

Selecionado a segunda aba do relatório é possível ver um relátorio mais detalhado que lista todas as páginas do sapron de qual sistema opracional foram acessadas dividido por navegador utilizado.

 ![Captura de tela de 2022-12-02 10-22-28.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-22-28.png)

Esse relatório nos permite visualizar:

* Quantos usuários acessaram a página X usando o sistema operacional W e navegador Y. (Ex: Quantos usuários acessaram a página Despesas usando o sistema operacional Windows e navegador chrome? a resposta seria 7.

### 1.2.0 Aplicando filtro nesse relatório

É possível aplicar filtros nesse relatório para pegar apenas uma página específica, para isso é necessário clicar em **Filtros** na aba configurações da guia que fica ao lado esquerdo da tela.

1 - Clique em Filtros

 ![Captura de tela de 2022-12-02 10-34-28.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-34-28.png)

2 - Selecione a opção Título da página;

 ![Captura de tela de 2022-12-02 10-34-49.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-34-49.png)

3 - Ele vai abrir um campo para selecionar o tipo;

 ![Captura de tela de 2022-12-02 10-35-14.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-35-14.png)

4 - Selecione a opção **Contém**;

 ![Captura de tela de 2022-12-02 10-35-24.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-35-24.png)

5 - Agora no campo insira a expressão escre o nome da página desejada e quando ele aparecer selecione; Nesse exemplo eu quero ver a página proprietário.

 ![Captura de tela de 2022-12-02 10-35-54.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-35-54.png)

6 - Após isso é só clicar em **Aplicar**;

 ![Captura de tela de 2022-12-02 10-36-05.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-36-05.png)

E o sistema vai mostrar todos os sitemas opracionais e navegadores de onde essa página foi acessada.

 ![Captura de tela de 2022-12-02 10-36-21.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-12-02_10-36-21.png)

### Como identificar o usuário (e sua role) que acessou?

No google analytics acesse o menu Relatŕios → Engajamento → Eventos: Nome do evento.

Os eventos de usuário são mostrados da seguinte forma: Role + id + Nome.

 ![Captura de tela de 2022-05-05 09-19-32.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-05-05_09-19-32.png)

### **Glossário:**

* **Scroll:** esse evento mostra a quantidade de vezes que o usuário rolou a página(scroll) até o fim ou em 90% dela.
* **Page_view:** esse evento mostra todas as páginas que foram visitadas pelos usuários e o tempo médio que passaram nela.

 ![Captura de tela de 2022-05-05 08-40-54.png](Google%20Analytics%20(reactga4)%20cd1cfdaa0fa74bd1b4b3ff3a62600dec/Captura_de_tela_de_2022-05-05_08-40-54.png)

* **First_visit:** esse evento contabiliza quantos pessoas novas acessaram o site ou seja fizeram a primeira visita.
* **Session_start:** esse evento contabiliza todas as vezes que um usuário interage com o site.
* **user_engagement:** quando o sapron está em primeiro plano ou a página da Web está em foco por pelo menos um segundo.
* Todos esses eventos a cima contabiliza os valores levando em consideração todos os usuários que acessam o sapron.