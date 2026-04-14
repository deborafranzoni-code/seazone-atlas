<!-- title: Reservas - envio de Voucher | url: https://outline.seazone.com.br/doc/reservas-envio-de-voucher-ZXQWwU7hdm | area: Tecnologia -->

# Reservas - envio de Voucher

Suporte [SAP-1981](https://seazone.atlassian.net/browse/SAP-1981)


Se o imóvel estava cadastrado com a categoria "ADEFINIR". ***==O email nao será disparado==***  

Quando o imóvel fica nesta categoria, ele não se enquadra no disparo de voucher, precisa inserir para que ele entre na regra de negócio. Já ajustamos e agora o disparo de voucher funcionará corretamente 

**Para os próximos:**


1. Uma vez identificado que o email (em casos isolados) não está sendo disparado
2. Acesse no menu Sapro: Operacional >> Implantação >> Editar propriedade
3. Selecione o imóvel
4. Verifique o campo "Categoria"
5. Caso esteja a categoria **ADEFINIR**, selecione a categoria correspondente (EX ILCJR)
6. Clique em "Salvar"

   \

 ![](/api/attachments.redirect?id=0a9cce87-660d-4a45-95c4-62d350d5ac04)