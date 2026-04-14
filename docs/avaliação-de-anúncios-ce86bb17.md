<!-- title: Avaliação de Anúncios | url: https://outline.seazone.com.br/doc/avaliacao-de-anuncios-NLhaZivvJN | area: Tecnologia -->

# Avaliação de Anúncios

O módulo de avaliação de anúncios tem o objetivo de explicitar os anúncios com nota abaixo do esperado no Airbnb. A implementação deste módulo se encontra dentro do repositório api-stays (abrange integração Sheets ↔ AWS e AWS ↔ Stays), pois seu funcionamento está concentrado em um único Lambda ativado pelo Sheets através de uma chamada de API.

Github: [api-stays](https://github.com/Khanto-Tecnologia/api-stays)

## Funcionamento

O módulo de setup groups é executado através de uma chamada do tipo PUT no método listings-evaluation/analysis da API de comunicação com o sheets realizada diretamente na [aba input](/doc/comunicacao-e-dados-aWFByTFvPo).

### Aba Input:

* A nota mínima desejada para os imóveis é posta logo abaixo de "Nota Mínima" e pode ser tanto um número inteiro quanto um número racional (separado por vírgula)
* O processo é executado ao clicar no botão "Executar"
* Após inserir a nota mínima, é bom clicar em alguma outra célula antes de executar o processo, caso contrário pode ser que a célula não atualize propriamente e o processo seja executado utilizando o valor passado
* A data e hora da última execução do processo se encontra em "Última execução"
* O valor abaixo de "Última aquisição de reviews" se refere a data da última aquisição de reviews registrada no Data Lake. A informação pode vir a ser útil caso seja notado algo estranho nos dados de reviews retornados.
* O status e, caso tenha, descrição do erro, da última execução se encontra em "Status última execução"

  ![Untitled](Avaliac%CC%A7a%CC%83o%20de%20Anu%CC%81ncios%20f638bc76cb2c4e7797372a3148779cc8/Untitled.png)

### Aba Output:

* Os dados de reviews dos imóveis com nota abaixo da nóta mínima inserida se encontram na aba Output

 ![Untitled](Avaliac%CC%A7a%CC%83o%20de%20Anu%CC%81ncios%20f638bc76cb2c4e7797372a3148779cc8/Untitled%201.png)