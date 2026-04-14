<!-- title: Discovery - Pré check-in via Website Seazone | url: https://outline.seazone.com.br/doc/discovery-pre-check-in-via-website-seazone-JdZbQE9WUa | area: Tecnologia -->

# Discovery - Pré check-in via Website Seazone

## Oportunidade

Automatizar o processo de pré check-in utilizando o Website da Seazone como plataforma, centralizando a coleta de documentações e dados relevantes de maneira integrada, visando melhorar a experiência do hóspede e reduzir a carga operacional do franqueado.

## Objetivos do Produto

Automatizar a coleta de informações obrigatórias para o pré check-in, incluindo:

* Horário de chegada do hóspede. 
* Quantidade de pessoas confirmada, conforme dados do sistema Stays. 
* Presença de animais de estimação na hospedagem. 
* Fotos de documentação de todos os hóspedes. 
* Distribuir informações adicionais no momento adequado, como:
  * Senha do Wi-Fi. 
  * Senha da fechadura eletrônica, que é atualizada a cada nova estadia. 

## Fluxo Atual: 

* O franqueado utiliza o sistema Sapron para acessar as informações da plataforma Stays. 
* Por meio do Sapron, o franqueado envia manualmente uma mensagem pelo WhatsApp ao hóspede, solicitando a documentação necessária e compartilhando as informações adicionais, como senhas. 

## Desafios Operacionais e Limitações

A implementação de um pré check-in automatizado diretamente pelo site da Seazone encontra limitações práticas:


1. **Atualização de Dados Sensíveis**: A senha das fechaduras eletrônicas precisariam de atualizações constantes, exigindo processos ágeis e recursos que o time operacional atualmente não possui. A equipe operacional enfrenta limitações tanto em termos de recursos quanto de processos estabelecidos para fazer essas atualizações de forma rápida e eficiente. Sem a implementação desse processo de automação, podemos não alcançar a fluidez esperada e ainda depender da intervenção manual dos franqueados.
2. **Integração com o Sapron:** Mesmo com o recebimento das fotos dos documentos via site, o Sapron necessitaria de adaptações para permitir visualização e acesso dos franqueados a esses documentos. É uma arquitetura que ainda não existe para integrar o website ao Sapron, e demandaria um esforço grande de tecnologia.
3. **Complexidade em Expandir para Reservas de Diferentes OTAs**: A expansão do pré check-in para todos os hóspedes da Seazone, independentemente da OTA onde a reserva foi feita, cria um desafio adicional. Para que o hóspede que efetuou sua reserva por outro OTA que não seja o site Seazone possa acessar os dados de pré check-in pelo site da Seazone, seriam necessárias verificações adicionais, como por e-mail ou código. Essa validação, além de aumentar a complexidade do sistema, poderia gerar confusão para hóspedes vindos de diferentes plataformas.

## Conclusão e Recomendações

Ao analisar o fluxo atual e conduzir entrevistas com stakeholders, é possível concluir que, para evitar sobrecarregar o franqueado e minimizar o uso de múltiplas plataformas (por exemplo, o WhatsApp após a verificação pelo site), a solução mais eficiente seria gerar, diretamente via Sapron, um **link único para o pré check-in**. Esse link, enviado pelo franqueado ao hóspede, daria acesso a um formulário digital, onde o hóspede pode:

* Confirmar os dados necessários.
* Enviar a documentação diretamente, que então passa a ser gerida pela Seazone.
* Acessar todas as demais informações adicionais.

Com isso, o Sapron consolidaria as informações e as disponibilizaria ao franqueado de maneira mais ágil e acessível, otimizando o fluxo de trabalho e proporcionando uma experiência mais eficaz na plataforma.


\