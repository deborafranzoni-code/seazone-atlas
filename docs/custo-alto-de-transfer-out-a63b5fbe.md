<!-- title: Custo Alto de transfer-out | url: https://outline.seazone.com.br/doc/custo-alto-de-transfer-out-TPOMlvLkrD | area: Tecnologia -->

# Custo Alto de transfer-out

Incidente iniciado ao percebermos um alto custo de transfer out que iniciava após as migrações que fizemos trazendo aplicações que rodavam em oregon para o servidor de São Paulo 


Identificamos analisando dados do VPC flow logs que a maior parte do tráfego estava saindo para IPs do google


Uma das hipoteses era de que esse volume de dados poderia estar saindo através de uma sincronização que temos com o google hotels e tivemos uma reunião com o time de reservas para 


# Documentação da Integração com o Google Hotels

Este documento detalha o funcionamento das tarefas de integração com a API do Google Hotels, responsáveis por enviar informações sobre propriedades, disponibilidade, tarifas e inventário.

## Visão Geral

A integração é dividida em dois fluxos principais:


1. **Properties Feed (Feed de Propriedades):** Um processo agendado que envia uma lista completa e detalhada de todas as propriedades ativas.
2. **ARI (Availability, Rates, and Inventory):** Mensagens transacionais enviadas com alta frequência para atualizar dados dinâmicos como disponibilidade, preços e restrições de reserva.

Ambos os fluxos geram arquivos XML com base em templates Jinja2 e nos dados das propriedades, que são consultados principalmente de um índice do OpenSearch (para ARI) e do banco de dados (para o Feed de Propriedades).


---

## 1. Properties Feed (Feed de Propriedades)

Este fluxo é responsável por manter o Google atualizado sobre o catálogo de propriedades.

* **Tarefa Celery:** `google_hotels.generate_properties_feed_xml`
* **Frequência de Execução:** Esta é uma tarefa agendada (a frequência é definida na configuração do Celery Beat, por exemplo, diariamente).
* **Arquivo Principal:** `properties_feed.py`

### Funcionamento


1. **Consulta de Dados:** A tarefa consulta o banco de dados para obter todas as propriedades com status `"active"`.
2. **Separação de Propriedades:** As propriedades são divididas em duas categorias:
   * **Vacation Rentals:** Propriedades individuais.
   * **Buildings (Prédios):** Propriedades agrupadas, como em um hotel, identificadas por um `external_property_id`.
3. **Geração de XML:** Dois arquivos XML separados são gerados (`Seazone_local.xml` e `Seazone_local_buildings.xml`) usando o template `properties_feed.xml`.
4. **Dados Enviados no XML:** Para cada propriedade, um conjunto extenso de dados é coletado e formatado, incluindo:
   * **Informações Básicas:** ID, nome, endereço completo, latitude, longitude, telefone.
   * **Conteúdo Detalhado:**
     * **Descrição:** Título e corpo da descrição (formatado de HTML para texto plano).
     * **Imagens:** Até 10 fotos da propriedade com URL, título e dimensões.
     * **Comodidades (Attributes):** Uma lista detalhada de atributos como capacidade de hóspedes, número de quartos/banheiros, ar-condicionado, Wi-Fi, estacionamento, etc.
     * **Avaliações (Reviews):** Comentários de usuários com nota, autor e data.
5. **Validação:** O XML gerado é validado contra um esquema XSD oficial do Google e também é verificado para não exceder o limite de 100MB.
6. **Compressão e Upload:** Os dois arquivos XML são comprimidos em um único arquivo `.zip` (`Seazone_local.xml.zip`) e enviados para um bucket no AWS S3. O Google, por sua vez, busca periodicamente este arquivo do S3 para atualizar seu catálogo.


---

## 2. ARI (Availability, Rates, and Inventory)

O fluxo ARI é responsável por enviar atualizações em tempo real sobre os dados dinâmicos de uma propriedade. As mensagens são pequenas, focadas e enviadas diretamente para a API do Google.

* **Tarefa Principal:** `google_hotels.push_ari_messages`
* **Gatilho:** Esta tarefa pode ser disparada por eventos (ex: uma reserva é criada, um preço é alterado) para uma única propriedade, ou de forma agendada para sincronizar todas as propriedades (`push_all_properties_ari_messages`).
* **Arquivos Principais:** Todo o lógico está contido no diretório `hotels/ari/`.

### Funcionamento

A tarefa `push_ari_messages` executa uma cadeia (chain) de subtarefas para uma determinada `property_id`, garantindo que todas as informações sejam enviadas na ordem correta. Os dados para essas mensagens são buscados de um índice do **OpenSearch**, que funciona como um cache rápido e denormalizado.

A cadeia de tarefas é executada na seguinte ordem:

### 2.1. Inventário (`inventory.py`)

* **Tarefa:** `push_inventory_count`
* **Propósito:** Informar ao Google quantas unidades da propriedade estão disponíveis em cada data.
* **Dados Enviados:** Para cada dia na janela de disponibilidade, envia uma mensagem com a data e a quantidade (`count`). Para aluguéis de temporada, esse valor é `1` (disponível) ou `0` (indisponível).

### 2.2. Disponibilidade (`availability.py`)

* **Tarefa:** `push_availability`
* **Propósito:** Comunicar o status de disponibilidade e as restrições de reserva.
* **Dados Enviados:** Para cada dia, envia mensagens que definem:
  * `**SetMinLOS**` **(Minimum Length of Stay):** A estadia mínima (em noites) para aquela data.
  * `**RestrictionStatus**`**:**
    * `Master`: Se a propriedade está aberta (`Open`) ou fechada (`Close`) para reservas.
    * `Arrival`: Se permite (`Open`) ou não (`Close`) check-in naquela data.
    * `Departure`: Se permite (`Open`) ou não (`Close`) check-out naquela data.

### 2.3. Tarifas (`rate_amount.py`)

* **Tarefa:** `push_rate_amount`
* **Propósito:** Enviar os preços da propriedade.
* **Modelo de Precificação:** Utiliza o modelo **LOS-based pricing** (preço baseado na duração da estadia). O preço da diária pode variar dependendo do número total de noites da reserva.
* **Dados Enviados:** Para cada data de check-in e para cada possível duração de estadia (de `min_stay` até 30 noites), é enviada a **média do preço por noite** (`amount_before_tax`). O Google utiliza essa média e multiplica pelo número de noites para calcular o valor total da estadia.

### 2.4. Taxas e Encargos (`tax_and_fees.py`)

* **Tarefa:** `push_taxes_and_fees`
* **Propósito:** Informar sobre taxas adicionais.
* **Dados Enviados:** Envia o valor da **taxa de limpeza (**`**cleaning_fee**`**)**, que é um valor fixo por estadia.

### 2.5. Cobranças por Hóspedes Extras (`extra_guest_charges.py`)

* **Tarefa:** `push_extra_guest_charges`
* **Propósito:** Definir o custo para hóspedes além da capacidade padrão incluída na tarifa.
* **Dados Enviados:** Envia o valor a ser cobrado por cada adulto ou criança adicional, caso a propriedade possua uma configuração de `extra_guests_value`.


---

## Mensagem de Transação (`transaction.py`)

Embora não faça parte da cadeia ARI principal, a tarefa `push_transaction_property_data` é fundamental para a estrutura da listagem no Google.

* **Propósito:** Definir a relação entre o "hotel" (propriedade ou prédio), os "tipos de quarto" (as unidades individuais) e os "planos de tarifa" (pacotes).
* **Dados Enviados:** Envia uma mensagem que mapeia o `HotelID` para os `RoomID`s e `PackageID`s correspondentes. Na prática, cada unidade é tratada como um "quarto" com seu próprio "pacote de tarifa".

## Janela de Disponibilidade

A quantidade de dias no futuro para os quais os dados de ARI são enviados é controlada por variáveis de ambiente:

* `AVAILABILITY_WINDOW`: Janela padrão (ex: 180 dias).
* `AVAILABILITY_WINDOW_FOR_GOOGLE_HOTELS`: Uma janela estendida (ex: 330 dias) usada para um conjunto específico de propriedades para atender a um requisito do Google.

## Ambiente de Execução

**Importante:** As tarefas ARI só enviam dados para a API do Google quando o ambiente (`ENV`) está configurado como `PRODUCTION`. Em qualquer outro ambiente, a geração do XML ocorre, mas o envio é pulado para evitar o envio de dados de teste.