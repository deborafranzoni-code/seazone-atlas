<!-- title: Templates de e-mail (MJML) | url: https://outline.seazone.com.br/doc/templates-de-e-mail-mjml-tCnNRjdXpX | area: Tecnologia -->

# Templates de e-mail (MJML)

# 1) Visão geral

* **Objetivo:** padronizar e-mails usando **MJML**.
* **Ferramenta escolhida:** [MJML](https://mjml.io/).
  * Por que MJML?
    * A ferramenta MJML facilita a criação de templates de e-mail (responsivo por padrão).
    * Reduz a quantidade de código escrita pelo desenvolvedor (gera um HTML no final, sendo inline por padrão).
    * Possui componentes próprios (já responsivos) como mj-section, mj-column, mj-text, mj-button, entre outros.

# 2) Stack & fluxo de desenvolvimento

* **Ferramenta de desenvolvimento:** Pode ser feito tanto em IDEs como no editor de email do MJML ([MJML/Try-it-live](https://mjml.io/try-it-live)) 
  * Benefícios do editor de email do MJML:
    * Possui um visualizador do template (tanto na versão desktop, quanto na versão mobile)
    * Gera o HTML sem precisar compilar (tanto formatado quanto na versão inline/minify)

 ![](/api/attachments.redirect?id=7fbf0586-a88f-4e96-a7ce-19fadac6ef31 " =1917x947")

# 3) Boas práticas com MJML

* **Versione e salve dois artefatos:** sempre salve/commit o `**.mjml**` e o `**.html**`. O `.mjml` é a *fonte de verdade*. Embora o editor do MJML gere HTML, **não há conversão confiável de HTML → MJML**, portanto, qualquer edição de template deve ser feita no `.mjml`.


# 4) Templates do sistema

* E-mail de confirmação de reserva/pagamento:
  * MJML: 

    [confirmation_email.mjml 14409](/api/attachments.redirect?id=86737b83-df81-449b-ae06-31e3b7230392)

  * HTML:

    [confirmation_email.html 57755](/api/attachments.redirect?id=fb57d3f6-3627-45af-ad45-21feecc10085)