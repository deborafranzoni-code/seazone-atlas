<!-- title: Novo Fechamento via Sapron | url: https://outline.seazone.com.br/doc/novo-fechamento-via-sapron-ITfUrrepgZ | area: Tecnologia -->

# Novo Fechamento via Sapron

Este documento descreve a sequência de ações que devem ser realizadas para a conciliação diária de reservas, despesas e ajustes no Sapron, gerando o fechamento financeiro.

A grande diferença da nova proposta é que ela visa atender às necessidades em tempo real, sem a necessidade de processamento assíncrono diário para consolidação dos valores.

# Escopo de Dados do Fechamento Sapron

O fechamento financeiro envolve a consolidação de dados vindos de diversas fontes, com diferentes contextos e significados dentro da Seazone, conforme a descrição a seguir:

* Receitas, Taxas e Comissões vindas de diárias de reservas realizadas .
* Despesas associadas a uma propriedade gerenciada pela Seazone, e seus reembolsos.
* Repasses de valores a um Proprietário de Imóvel.
* Repasses de valores a um Anfitrião.
* Taxas de implantação associadas a uma propriedade gerenciada pela Seazone.
* Taxas de franquia associadas a um Anfitrião.
* Ajustes financeiros, sejam eles positivos ou negativos, realizados em uma reserva, e consequentemente impactando em suas taxas e comissões.
* Ajustes financeiros, sejam eles positivos ou negativos, associados à contabilidade junto a um Proprietário de Imóvel.
* Ajustes financeiros, sejam eles positivos ou negativos, associados à contabilidade junto a um Anfitrião.


---

# Estrutura de Dados do Novo Fechamento

A nova estrutura de dados para atender ao fechamento financeiro da Seazone é formada por novos tipos de colunas, ajustes em tabelas já existentes e novas tabelas, conforme descrito a seguir:

## Novo tipo: ENUM *transfer_types*

Tipo de transferência a ser realizada, podendo ser entrada ou saída de valor.

```sql
CREATE TYPE transfer_types AS ENUM ('input', 'output');
```

## Novo tipo: ENUM *transfer_categories*

Categoria de transferência a ser realizada, podendo ser diversos valores, conforme o código a seguir.

```sql
CREATE TYPE transfer_categories AS ENUM (
	'host_commission',    -- comissão de diárias destinada ao host
	'seazone_commission', -- comissão de diárias destinada à Seazone
	'ota_commission',     -- comissão de diárias destinada ao OTA
	'partner_commission', -- comissão de diárias destinada ao Parceiro
	'host_payment',       -- pagamento de repasse a um anfitrião
	'owner_payment',      -- pagamento de repasse a um proprietário
 	'partner_payment',      -- pagamento de repasse a um parceiro
	'expense',            -- registro de despesa
	'revenue',            -- registro de receita
	'manual_fit',         -- ajuste manual feito a anfitrião, proprietário ou Seazone
	'reservation_manual_fit', -- ajuste manual feito a uma reserva
	'cleaning_manual_fit',-- ajuste manual feito a uma taxa de limpeza   
	'host_commission_fit', 	  -- ajuste de comissão de diárias de anfitrião
 	'seazone_commission_fit', -- ajuste de comissão de diárias da Seazone
	'partner_commission_fit', -- ajuste de comissão de diárias do Parceiro 
	'refund_expense',     -- reembolso de uma desepesa
	'onboarding_expense', -- despesa de onboarding
	'implantation_fee',   -- taxa de implantação de uma propriedade
	'cleaning_fee',	      -- taxa de limpeza de uma reserva
	'franchise_fee',      -- taxa de franquia associada a um anfritão
	'reservation_revenue',-- recceita a partir de uma reserva 
	'property_revenue' --,   -- receita de uma propriedade
);
```

## Ajuste na Tabela *financial_host_franchise_fee*

Deve ser incluído uma nova coluna de saldo, para não gerar impacto na estrutura atual.

```sql
ALTER TABLE public.financial_host_franchise_fee ADD debit_balance float8 NULL;
```

## Tabela de Extrato de Entradas e Saídas de uma Propriedade: *closing_property_resume*

Extrato com todas as movimentações que empatam diretamente o proprietário do imóvel.

* id: int
* reservation_id: int (FK da reservation_reservation)
* property_id: int (FK da property_property)
* accrual_date: date
* cash_date: date
* value: float
* transfer_type: ENUM transfer_types (deve ser criado)
  * output: Um registro de saída de um valor da conta.
  * input: Um registro de entrada de um valor na conta.
* transfer_category: ENUM transfer_categories (deve ser criado antes)
  * (OUT) expense: registro de uma operação de saída referente à despesa.
  * (IN) property_revenue: registro de um valor de entrada referente aos ganhos de diárias em uma reserva.
  * (OUT) seazone_commission: registro de um valor de saída de comissão paga pelo proprietário à Seazone a partir de uma reserva.
  * (OUT) host_commission: registro de um valor de saída de comissão paga pelo proprietário ao Anfitrião a partir de uma reserva.
  * (IN-OUT) manual_fit: registro de um ajuste manual, que pode ser uma entrada ou saída.
  * (OUT) owner_payment: registro de um valor de saída referente à transferência de um valor ao proprietário por parte da Seazone.
  * (IN) onboarding_expense:  registro de um valor de entrada referente à despesa de configuração e preparação de um imóvel a ser paga ao proprietário.
  * (IN-OUT) reservation_manual_fit: registro de um ajuste manual referente a uma reserva, que pode ser uma entrada ou saída.
  * (IN-OUT) host_commission_fit: registro de um ajuste manual referente a uma comissão paga pelo proprietário a um anfitrião, que pode ser uma entrada ou saída.
  * (IN-OUT) seazone_commission_fit: registro de um ajuste manual referente a uma comissão paga pelo proprietário à Seazone, que pode ser uma entrada ou saída.
  * (OUT) implantation_fee: registro de um valor de saída referente à taxa de implantação de um imóvel.
* description: string
* source_table: string
* source_id: integer
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_owner_resume (
	id bigserial NOT NULL,
	reservation_id int8 NULL,
	property_id int8 NULL,
	accrual_date date NULL,
	cash_date date NULL,
	value float8 NULL,
	transfer_type public.transfer_types NOT NULL,
	transfer_category public.transfer_categories NOT NULL,
	description varchar(1024) NULL,
	source_table varchar(255) NULL,
	source_id int8 NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_owner_resume_pkey PRIMARY KEY (id),
	CONSTRAINT closing_owner_resume_fk_property_id
		FOREIGN KEY (property_id) 
		REFERENCES public.property_property(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT closing_owner_resume_fk_reservation_id 
		FOREIGN KEY (reservation_id) 
		REFERENCES public.reservation_reservation(id) DEFERRABLE INITIALLY DEFERRED
);
```

## Tabela de Extrato de Entradas e Saídas de um Anfitrião: *closing_host_resume*

Extrato com todas as movimentações que empatam diretamente o anfitrião.

* id: int
* reservation_id: int (FK da reservation_reservation)
* property_id: int (FK da property_property)
* host_id: int (FK da account_host)
* accrual_date: date
* cash_date: date
* value: float
* transfer_type: ENUM transfer_types (deve ser criado)
  * output: Um registro de saída de um valor da conta.
  * input: Um registro de entrada de um valor na conta.
* transfer_category: ENUM transfer_categories
  * (IN) host_commission: registro de valor de entrada vindo de comissão obtida a partir de uma reserva.
  * (IN) cleaning_fee: registro de um valor de entrada referente à taxa de limpeza de um imóvel.
  * (OUT) expense: registro de um valor de saída referente à despesa de um imóvel.
  * (IN) refund_expense:  registro de um valor de entrada referente ao reembolso de uma despesa de um imóvel.
  * (IN) onboarding_expense:  registro de um valor de entrada referente à despesa de configuração e preparação de um imóvel a ser paga ao anfitrião.
  * (OUT) franchise_fee: registro do valor de saída referente à taxa de franquia de um anfitrião com a Seazone.
  * (IN-OUT) cleaning_manual_fit:  registro de um valor de ajuste em taxa de limpeza, que pode ser uma entrada ou saída.
  * (IN-OUT) manual_fit: registro de um ajuste manual, que pode ser uma entrada ou saída.
  * (IN-OUT) host_commission_fit: registro de um ajuste manual referente a uma comissão recebida pelo host, que pode ser uma entrada ou saída.
  * (OUT) host_payment: registro de um valor de saída referente à transferência de um valor ao anfitrião por parte da Seazone.
* description: string
* source_table: string
* source_id: integer
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_host_resume (
	id bigserial NOT NULL,
	reservation_id int8 NULL,
	property_id int8 NULL,
	host_id int8 NULL,	
	accrual_date date NULL,
	cash_date date NULL,
	value float8 NULL,
	transfer_type public.transfer_types NOT NULL,
	transfer_category public.transfer_categories NOT NULL,
	description varchar(1024) NULL,
	source_table varchar(255) NULL,
	source_id int8 NULL,	
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_host_resume_pkey PRIMARY KEY (id),
	CONSTRAINT closing_host_resume_fk_property_id
		FOREIGN KEY (property_id) 
		REFERENCES public.property_property(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT closing_host_resume_fk_host_id
		FOREIGN KEY (host_id) 
		REFERENCES public.account_host(id) DEFERRABLE INITIALLY DEFERRED,		
	CONSTRAINT closing_host_resume_fk_reservation_id 
		FOREIGN KEY (reservation_id) 
		REFERENCES public.reservation_reservation(id) DEFERRABLE INITIALLY DEFERRED
);
```

## Tabela de Extrato de Entradas e Saídas da Seazone: *closing_seazone_resume*

Extrato com todas as movimentações que empatam diretamente a Seazone.

* id: int
* reservation_id: int (FK da reservation_reservation)
* property_id: int (FK da property_property)
* accrual_date: date
* cash_date: date
* value: float
* transfer_type: ENUM transfer_types (deve ser criado)
  * output: Um registro de saída de um valor da conta.
  * input: Um registro de entrada de um valor na conta.
* transfer_category: ENUM transfer_categories
  * (IN) host_payment: registro de um valor de entrada referente à transferência de um valor ao anfitrião por parte da Seazone.
  * (IN) owner_payment: registro de um valor de entrada referente à transferência de um valor ao proprietário por parte da Seazone.
  * (IN) implantation_fee: registro de um valor de entrada referente à taxa de implantação de um imóvel recebido pela Seazone.
  * (IN-OUT) reservation_manual_fit: registro de um ajuste manual referente a uma reserva, que pode ser uma entrada ou saída.
  * (IN-OUT) manual_fit: registro de um ajuste manual, que pode ser uma entrada ou saída, feito junto a um anfitrião ou proprietário.
  * (IN-OUT) seazone_commission_fit: registro de um ajuste manual referente a uma comissão recebida pela Seazone, que pode ser uma entrada ou saída.
  * (IN) seazone_commission: registro de valor de entrada vindo de comissão obtida a partir de uma reserva.
  * (IN) expense: registro de um valor de entrada referente a uma despesa paga pela Seazone.
  * (IN) reservation_revenue: registro de um valor de entrada referente à receita total recebida pela Seazone por conta de uma reserva.mpl
  * (OUT) property_revenue: registro de um valor de saída referente à receita paga a um imóvel por conta de uma reserva.
  * (OUT) cleaning_fee: registro de um valor de saída referente à taxa de limpeza de uma reserva paga a um anfitrião.
  * (IN) refund_expense: registro de um valor de entrada referente ao reembolso de uma despesa feito a um anfitrião ou proprietário.
  * (IN) debited_expense: registro de um valor de entrada referente a uma despesa que foi paga pela Seazone e deve ser descontada do anfitrião.
  * (OUT) onboarding_expense: registro de um valor de entrada referente à despesa de preparação de um imóvel paga pela Seazone a ser descontada do anfitrião.
  * (IN) franchise_fee: registro de um valor de entrada referente à taxa de franquia a ser paga pelo anfitrião à Seazone.
* description: string
* source_table: string
* source_id: integer
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_seazone_resume (
	id bigserial NOT NULL,
	reservation_id int8 NULL,
	property_id int8 NULL,
	accrual_date date NULL,
	cash_date date NULL,
	value float8 NULL,
	transfer_type public.transfer_types NOT NULL,
	transfer_category public.transfer_categories NOT NULL,
	description varchar(1024) NULL,
	source_table varchar(255) NULL,
	source_id int8 NULL,	
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_seazone_resume_pkey PRIMARY KEY (id),
	CONSTRAINT closing_seazone_resume_fk_property_id
		FOREIGN KEY (property_id) 
		REFERENCES public.property_property(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT closing_seazone_resume_fk_reservation_id 
		FOREIGN KEY (reservation_id) 
		REFERENCES public.reservation_reservation(id) DEFERRABLE INITIALLY DEFERRED
);
```

## Tabela de Saldo de uma Propriedade: *closing_property_balance*

Saldo de uma propriedade em uma data de referência.

* id: int
* property_id: int (FK da property_property)
* date_ref: date
* value: float
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_property_balance (
	id bigserial NOT NULL,
	property_id int8 NULL,
	date_ref date NULL,
	value float8 NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_property_balance_pkey PRIMARY KEY (id),
	CONSTRAINT closing_property_balance_fk_property_id
		FOREIGN KEY (property_id) 
		REFERENCES public.property_property(id) DEFERRABLE INITIALLY DEFERRED
);
```

## Tabela de Saldo de um Anfitrião: *closing_host_balance*

Saldo de um anfitrião em uma data de referência.

* id: int
* host_id: int (FK da account_host)
* date_ref: date
* value: float
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_host_balance (
	id bigserial NOT NULL,
	host_id int8 NULL,
	date_ref date NULL,
	value float8 NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_host_balance_pkey PRIMARY KEY (id),
	CONSTRAINT closing_host_balance_fk_host_id
		FOREIGN KEY (host_id) 
		REFERENCES public.account_host(id) DEFERRABLE INITIALLY DEFERRED
);
```

## Tabela de Extrato de Entradas e Saídas de um Parceiro: *closing_partner_resume*

Extrato com todas as movimentações que empatam diretamente o parceiro.

* id: int
* reservation_id: int (FK da reservation_reservation)
* property_id: int (FK da property_property)
* partner_id: int (FK da account_partner)
* accrual_date: date
* cash_date: date
* value: float
* transfer_type: ENUM transfer_types (deve ser criado)
  * output: Um registro de saída de um valor da conta.
  * input: Um registro de entrada de um valor na conta.
* transfer_category: ENUM transfer_categories
  * (IN) partner_commission: registro de valor de entrada vindo de comissão obtida a partir de uma reserva.
  * (OUT) partner_payment: registro de um valor de saída referente à transferência de um valor ao anfitrião por parte da Seazone.
* description: string
* source_table: string
* source_id: integer
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_partner_resume (
	id bigserial NOT NULL,
	reservation_id int8 NULL,
	property_id int8 NULL,
	partner_id int8 NULL,	
	accrual_date date NULL,
	cash_date date NULL,
	value float8 NULL,
	transfer_type public.transfer_types NOT NULL,
	transfer_category public.transfer_categories NOT NULL,
	description varchar(1024) NULL,
	source_table varchar(255) NULL,
	source_id int8 NULL,	
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_partner_resume_pkey PRIMARY KEY (id),
	CONSTRAINT closing_partner_resume_fk_property_id
		FOREIGN KEY (property_id) 
		REFERENCES public.property_property(id) DEFERRABLE INITIALLY DEFERRED,
	CONSTRAINT closing_partner_resume_fk_partner_id
		FOREIGN KEY (partner_id) 
		REFERENCES public.account_partner(id) DEFERRABLE INITIALLY DEFERRED,		
	CONSTRAINT closing_partner_resume_fk_reservation_id 
		FOREIGN KEY (reservation_id) 
		REFERENCES public.reservation_reservation(id) DEFERRABLE INITIALLY DEFERRED
); 
```

## Tabela de Saldo de um Parceiro: *closing_partner_balance*

Saldo de um anfitrião em uma data de referência.

* id: int
* partner_id: int (FK da account_partner)
* date_ref: date
* value: float
* created_at: timestamp
* update_at: timestamp

```sql
CREATE TABLE closing_partner_balance (
	id bigserial NOT NULL,
	partner_id int8 NULL,
	date_ref date NULL,
	value float8 NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT closing_partner_balance_pkey PRIMARY KEY (id),
	CONSTRAINT closing_partner_balance_fk_host_id
		FOREIGN KEY (partner_id) 
		REFERENCES public.account_partner(id) DEFERRABLE INITIALLY DEFERRED
);
```


---

# Fluxo para Geração do Fechamento em Tempo Real

Para que o novo fechamento ocorra de forma automatizada e em tempo real, é necessário que a cada manipulação de um dado (inserção, alteração ou exclusão) que impacte diretamente o fechamento, o processamento de tal registro seja realizado de forma a se calcular seu impacto no  fechamento. Isso deve ocorrer por meio de *workers*, *triggers* e funções de cálculos implementadas nas tabelas que impactam o fechamento. As tabelas são:

* ***reservation_reservation:*** a tabela que descreve as reservas ocorridas na Seazone. Em caso de inserção, alteração ou exclusão de uma reserva com status ativa (Concluded, No-Show), a função de cálculo de comissões deve ser executada.
* ***financial_expenses:*** a tabela que descreve as despesas de uma propriedade registradas na Seazone. Em caso de inserção, alteração ou exclusão de uma despesa aprovada (status Approved), a função de cálculo de despesas deve ser executada.
* ***financial_host_manual_fit:*** a tabela que descreve os ajustes positivos ou negativos associados a um anfitrião. Em caso de inserção, alteração ou exclusão de um ajuste, a função de cálculo de ajuste deve ser executada.
* ***financial_property_manual_fit:*** a tabela que descreve os ajustes positivos ou negativos associados a uma propriedade. Em caso de inserção, alteração ou exclusão de um ajuste, a função de cálculo de ajuste deve ser executada.
* ***financial_cleaning_fee_manual_fit:*** a tabela que descreve os ajustes positivos ou negativos associados à taxa de limpeza de uma reserva. Em caso de inserção, alteração ou exclusão de um ajuste, a função de cálculo de ajuste deve ser executada.
* ***financial_reservation_manual_fit:*** a tabela que descreve os ajustes positivos ou negativos associados a uma reserva. Em caso de inserção, alteração ou exclusão de um ajuste, a função de cálculo de ajuste deve ser executada.
* ***financial_host_property_ted:*** a tabela que descreve os repasses financeiros feito a um anfitrião. Em caso de inserção, alteração ou exclusão de um repasse, a função de cálculo de repasse deve ser executada.
* ***financial_owner_property_ted:*** a tabela que descreve os repasses financeiros feito a um proprietário. Em caso de inserção, alteração ou exclusão de um repasse, a função de cálculo de repasse deve ser executada.
* ***financial_host_franchise_fee_payments:*** a tabela que descreve os pagamento de taxas de franquia de anfitriões da Seazone. Em caso de inserção, alteração ou exclusão de um repasse, a função de cálculo de taxa de franquia cobrada deve ser executada.
* ***property_handover_details:*** a tabela que descreve os pagamento de taxas de implantação de imóveis da Seazone. Em caso de inserção, alteração ou exclusão de um repasse, a função de cálculo de taxa de implantação deve ser executada.
* ***property_property:*** a tabela que descreve as configurações de um imóvel, incluindo seu anfitrião e as taxas a serem consideradas em reservas para o proprietário, para o anfitrião e para a Seazone. Em caso de alteração dessas informações, a função que atualiza as reservas futuras para esses novos dados deve ser executada.

# Algoritmo e Regras de Negócio sobre a tabela *reservation_reservation*

Esta tabela é responsável por armazenar os dados sobre as reservas realizadas em propriedades gerenciados pela Seazone. Ela possui impacto direto em todas as tabelas relacionadas ao fechamento financeiro.

## Regras de Negócio

* Apenas reservas com status `Concluded` ou `No-Show` podem gerar comissões.
* Apenas reservas com atributo `is_blocking = false` podem gerar comissões.
* Se uma reserva possuir extensão (early ou late), as taxas de limpeza estarão em cada reserva separadamente e deverão ser contabilizadas separadamente.
* O dia da fatura depende de qual OTA a reserva está associada. Há OTA's que pagam no mesmo mes da reserva e há OTA's que pagam no mês seguinte à reserva.

## Trigger sobre a tabela *reservation_reservation*

### Código de Criação da Trigger para Calcular Comissões e Receitas

```sql
CREATE TRIGGER reservation_changes
  AFTER INSERT or UPDATE
  ON reservation_reservation
  FOR EACH ROW
  EXECUTE PROCEDURE calculate_commissions();
```

### Função para Calcular Comissões e Receitas

```sql
-- DROP FUNCTION public.calculate_commissions();

CREATE OR REPLACE FUNCTION public.calculate_commissions()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare

  	reserv_id INTEGER;
  	checkin_date DATE;
  	checkout_date DATE;
  	break_date DATE;
		is_able BOOLEAN;
		saldo_mes FLOAT;
  	saldo_anterior FLOAT;
  	saldo_final FLOAT;
  	month_ref DATE;
  	last_month DATE;

 	com_rec RECORD;

  	com_cursor CURSOR (reservation_id integer, checkin_date date, checkout_date date) for
    WITH dates AS (
      SELECT date_trunc('day', dd)::date AS date
      FROM generate_series (checkin_date, checkout_date, '1 day'::interval) dd
    )
    select
      rr.id as reservation_id,
	  rr.code as code,
      d.date as accrual_date,
      CASE
          WHEN ros.payment_delay = 0 then d.date
          else (d.date + interval '1 month')::date
      end as cash_date,
      rr.property_id,
      rr.host_id,
      rr.ota_id,
      (rr.check_out_date - rr.check_in_date) as dias,
      (daily_net_value * rr.seazone_fee)::float / (rr.check_out_date - rr.check_in_date)::float as seazone_commission,
      (rr.daily_net_value * rr.host_fee)::float / (rr.check_out_date - rr.check_in_date)::float as host_commission,
      (daily_net_value)::float / (rr.check_out_date - rr.check_in_date)::float as property_revenue,
      rr.property_fee as property_fee,
      rr.host_fee as host_fee,
      rr.seazone_fee
      FROM reservation_reservation rr
      left join dates d
      on d.date between rr.check_in_date and (rr.check_out_date - 1)
      join reservation_ota_setup ros on ros.ota_id = rr.ota_id
      where is_blocking is false
      and rr.status in ('Concluded', 'No-Show')
      and rr.id = reservation_id;

	com_cursor_v3 CURSOR (reservation_id integer, checkin_date date, checkout_date date) for
      with dates as (
           select q.id, q.start_date::date,
          case when check_out_date < start_date::date + 31 then check_out_date else q.start_date::date + 30 end end_date
          from (select id, check_in_date, check_out_date, generate_series(check_in_date::date, check_out_date::date, interval '30 day') as start_date FROM reservation_reservation rr
            where is_blocking is false
            and rr.status in ('Concluded', 'No-Show')
            and rr.id = reservation_id) q 
      )
      select
            rr.id as reservation_id,
      	  rr.code as code,
            rr.check_in_date,
            d.end_date as accrual_date,
            CASE
                WHEN ros.payment_delay = 0 then d.end_date
                else (d.end_date + interval '1 month')::date
            end as cash_date,
            rr.property_id,
            rr.host_id,
            rr.ota_id,
            rr.daily_net_value,
            (d.end_date - d.start_date) as dias,
            (daily_net_value * rr.seazone_fee) * ((d.end_date - d.start_date)::float / (rr.check_out_date - rr.check_in_date))::float as seazone_commission,
            (rr.daily_net_value * rr.host_fee) * ((d.end_date - d.start_date)::float / (rr.check_out_date - rr.check_in_date))::float as host_commission,
            (daily_net_value) * ((d.end_date - d.start_date)::float / (rr.check_out_date - rr.check_in_date))::float as property_revenue,
            rr.property_fee as property_fee,
            rr.host_fee as host_fee,
            rr.seazone_fee
            FROM reservation_reservation rr
            left join dates d
            on d.id = rr.id
            join reservation_ota_setup ros on ros.ota_id = rr.ota_id
            where is_blocking is false
            and rr.status in ('Concluded', 'No-Show')
            and rr.id = reservation_id;

      cleaning_rec RECORD;

      cleaning_cursor CURSOR (reservation_id integer) for
      	select
    		rr.id as reservation_id,
		  	rr.code as code,
    		rr.property_id,
    		rr.host_id,
    		rr.ota_id,
    		rr.check_out_date as accrual_date,
    		CASE
    	        WHEN ros.payment_delay = 0 then rr.check_out_date
    	        else (rr.check_out_date + interval '1 month')::date
    	    end as cash_date,
    		(rr.check_out_date - rr.check_in_date) as dias,
    		rr.cleaning_fee_value,
    		rr.net_cleaning_fee as cleaning_commission,
    		rr.ota_comission as ota_commission,
    		rr.total_price,
    		rr.ota_fee,
    		(rr.has_late_extension or rr.has_early_extension) as has_extension
    	FROM reservation_reservation rr
    	join reservation_ota_setup ros on ros.id = rr.ota_id
    	where rr.is_blocking is false
    		and rr.status in ('Concluded', 'No-Show')
    		and rr.net_cleaning_fee > 0
    		and rr.id = reservation_id;

begin
	reserv_id := NEW.id;
	checkin_date := NEW.check_in_date;
	checkout_date := NEW.check_out_date;
	is_able := false;
 	-- Data de referência para o início do fechamento 3.0
  	break_date := '2025-05-01';

	if (TG_OP = 'INSERT') OR (TG_OP = 'DELETE') then
		is_able := true;
	else if (TG_OP = 'UPDATE') then
			if (NEW.check_in_date <> OLD.check_in_date) OR (NEW.check_out_date <> OLD.check_out_date) 
				OR (NEW.total_price <> OLD.total_price) OR (NEW.daily_net_value <> OLD.daily_net_value)
				OR (NEW.ota_comission <> OLD.ota_comission) OR (NEW.net_cleaning_fee <> OLD.net_cleaning_fee)
				OR (NEW.status <> OLD.status) OR (NEW.conciliada <> OLD.conciliada)
				OR (NEW.is_early_extension <> OLD.is_early_extension) OR (NEW.host_id <> OLD.host_id)
				OR (NEW.cleaning_fee_value <> OLD.cleaning_fee_value) OR (NEW.property_id <> OLD.property_id)
				OR (NEW.is_late_extension <> OLD.is_late_extension) OR (NEW.ota_id <> OLD.ota_id)
				OR (NEW.property_fee <> OLD.property_fee) OR (NEW.seazone_fee <> OLD.seazone_fee)
				OR (NEW.host_fee <> OLD.host_fee) then
				is_able := true;
			end if;
		end if;
	end if;

	if (is_able is true) then
		
    	if (NEW.is_blocking is false) then
		
           -- Comando para analisar se é uma reserva já conciliada
           if (TG_OP = 'UPDATE') and (OLD.conciliada is true) and (NEW.conciliada is true) and (OLD.ota_id <> 1) then
              raise notice '-------- Reserva ID % já conciliada e não pode ser alterada -------------', NEW.id;
           else
                if (TG_OP <> 'INSERT') then
                	raise notice '-------- Exclusão dos registros de comissão de reserva e ajustes -------------';
                	DELETE FROM closing_property_resume where reservation_id = reserv_id and transfer_category in ('property_revenue', 'seazone_commission',  'host_commission');
                	DELETE FROM closing_host_resume where reservation_id = reserv_id  and transfer_category in ('host_commission', 'cleaning_fee');
                	DELETE FROM closing_seazone_resume where reservation_id	= reserv_id  and transfer_category in ('property_revenue', 'seazone_commission', 'cleaning_fee', 'ota_commission' , 'reservation_revenue');
                  	DELETE FROM closing_ota_commission where reservation_id = reserv_id;

					if (TG_OP = 'DELETE' or NEW.status = 'Canceled') then
	                	DELETE FROM financial_reservation_manual_fit where reservation_id = reserv_id;
						DELETE FROM financial_cleaning_fee_manual_fit where reservation_id = reserv_id;
					else 
						UPDATE financial_reservation_manual_fit set updated_at = now() where reservation_id = reserv_id;
	                end if;
                end if;								
		
        		raise notice '-------- Inserção de registros de comissão de reserva -------------';

    			if (NEW.check_in_date < break_date) then 
            		open com_cursor(reserv_id, checkin_date, checkout_date);
    			else 
    				    open com_cursor_v3(reserv_id, checkin_date, checkout_date);
    			end if;
		
	          	loop
    				if (NEW.check_in_date < break_date) then 
            			fetch com_cursor into com_rec;
    				else 
    					    fetch com_cursor_v3 into com_rec;
    				end if;
		            		
            		exit when not found;
            		-- Inserir receita PROPERTY
            		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
            		VALUES (
            			com_rec.reservation_id, com_rec.property_id, com_rec.accrual_date, com_rec.cash_date, com_rec.property_revenue, 'input', 'property_revenue', CONCAT('Receita - reserva: ', com_rec.code), 'reservation_reservation', com_rec.reservation_id, now(), now());
            		-- Inserir comissao paga pela PROPERTY à SEAZONE
            		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
            		VALUES (
            			com_rec.reservation_id, com_rec.property_id, com_rec.accrual_date, com_rec.cash_date, com_rec.seazone_commission, 'output', 'seazone_commission', CONCAT('seazone_fee = ', com_rec.seazone_fee, ' seazone commission = ', com_rec.seazone_commission), 'reservation_reservation', com_rec.reservation_id, now(), now());
            		-- Inserir comissao paga pela PROPERTY ao HOST
            		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
            		VALUES (
            			com_rec.reservation_id, com_rec.property_id, com_rec.accrual_date, com_rec.cash_date, com_rec.host_commission, 'output', 'host_commission', CONCAT('host_fee = ', com_rec.host_fee, ' host commission = ', com_rec.host_commission), 'reservation_reservation', com_rec.reservation_id, now(), now());

            		-- Inserir comissao recebida HOST
            		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
            		VALUES (com_rec.reservation_id, com_rec.property_id, com_rec.host_id, com_rec.accrual_date, com_rec.cash_date, com_rec.host_commission, 'input', 'host_commission', CONCAT('Comissão - reserva: ', com_rec.code), 'reservation_reservation', com_rec.reservation_id, now(), now());

            		-- Inserir comissao recebida SEAZONE
            		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
            		VALUES (
            			com_rec.reservation_id, com_rec.property_id, com_rec.accrual_date, com_rec.cash_date, com_rec.seazone_commission, 'input', 'seazone_commission', CONCAT('Comissão - reserva: ', com_rec.code), 'reservation_reservation', com_rec.reservation_id, now(), now());
            		-- Inserir receita paga à PROPERTY
            		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
            		VALUES (
            			com_rec.reservation_id, com_rec.property_id, com_rec.accrual_date, com_rec.cash_date, com_rec.property_revenue , 'output', 'property_revenue', CONCAT('Receita paga - reserva: ', com_rec.code), 'reservation_reservation', com_rec.reservation_id, now(), now());
		
	            end loop;
		
	    		if (NEW.check_in_date < break_date) then 
	    				close com_cursor;
	    		else 
	    				close com_cursor_v3;
	    		end if;
	
	            raise notice '-------- Inserção de registros de transferencia -------------';
	            open cleaning_cursor(reserv_id);
	
	            loop
	                fetch cleaning_cursor into cleaning_rec;
	                exit when not found;
	
	                if new.status in ('Concluded', 'No-Show') then
	                    -- Inserir taxa de limpeza recebida HOST
	                    INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
	                    VALUES (
	                      cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.host_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.cleaning_commission, 'input', 'cleaning_fee', CONCAT('Taxa Limpeza - reserva: ', cleaning_rec.code), 'reservation_reservation', cleaning_rec.reservation_id, now(), now());
	
	                    -- Inserir taxa de limpeza paga ao HOST
	                    INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
	                    VALUES (
	                      cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.cleaning_commission, 'output', 'cleaning_fee', CONCAT('Taxa de limpeza paga - reserva: ', cleaning_rec.code), 'reservation_reservation', cleaning_rec.reservation_id, now(), now());
	                end if;
		
	                -- Inserir comissao OTA
	                INSERT INTO closing_ota_commission(reservation_id, property_id, ota_id, accrual_date, cash_date, value, fee, created_at, updated_at) VALUES (
	                  cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.ota_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.ota_commission, cleaning_rec.ota_fee, now(), now());
	
	                -- Inserir receita da reserva recebida pela SEAZONE
	                INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
	                VALUES (
	                  cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.total_price, 'input', 'reservation_revenue', CONCAT('Receita total - reserva: ', cleaning_rec.code), 'reservation_reservation', cleaning_rec.reservation_id, now(), now());
	                -- Inserir taxa de limpeza paga a OTA
	                INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at)
	                VALUES (
	                  cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.ota_commission, 'output', 'ota_commission', CONCAT('Comissão OTA - reserva: ', cleaning_rec.code), 'reservation_reservation', cleaning_rec.reservation_id, now(), now());
	
	            end loop;
	            close cleaning_cursor;
		
	    		if OLD.host_id <> NEW.host_id then
    				perform calculate_host_balance(OLD.host_id, OLD.check_in_date);
	    		end if;

				perform calculate_host_balance(NEW.host_id, NEW.check_in_date);
		
	            if OLD.property_id <> NEW.property_id then
						perform calculate_property_balance(OLD.property_id, OLD.check_in_date);
				end if;
	
				perform calculate_property_balance(NEW.property_id, NEW.check_in_date);
		
          	end if;
	      end if;
	end if;

  RETURN new;

END;
$function$
;
```


---

### Código de Criação da Trigger para Calcular Taxa de Limpeza

```sql
CREATE TRIGGER reservation_changes_cleaning_fee
  AFTER INSERT or UPDATE
  ON reservation_reservation
  FOR EACH ROW
  EXECUTE PROCEDURE calculate_cleaning_fee();
```

### Função para Calcular Taxa de Limpeza

```sql
-- DROP FUNCTION public.calculate_cleaning_fee();

CREATE OR REPLACE FUNCTION public.calculate_cleaning_fee()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare

  cleaning_rec RECORD;
 
  cleaning_cursor CURSOR (reservation_id integer) for
  	select 
		rr.id as reservation_id, 
		rr.property_id, 
		rr.host_id, 
		rr.ota_id, 	
		rr.check_out_date as accrual_date, 
		CASE
	        WHEN ros.payment_delay = 0 then rr.check_out_date
	        else (rr.check_out_date + interval '1 month')::date
	    end as cash_date,
		(rr.check_out_date - rr.check_in_date) as dias, 
		rr.cleaning_fee_value, 
		rr.net_cleaning_fee as cleaning_commission, 
		rr.ota_comission as ota_commission, 
		rr.total_price,
		rr.ota_fee,
		(rr.has_late_extension or rr.has_early_extension) as has_extension
	FROM reservation_reservation rr 
	join reservation_ota_setup ros on ros.id = rr.ota_id
	where rr.is_blocking is false 
		and rr.status in ('Concluded', 'No-Show')
		and rr.net_cleaning_fee > 0
		and rr.id = reservation_id;		

begin

	if (NEW.is_blocking is false) then

  -- Comando para analisar se é uma reserva já conciliada
  --if (TG_OP = 'UPDATE') and (OLD.conciliada is true) then 
  --    raise notice '-------- Reserva ID % já conciliada e não pode ser alterada -------------', NEW.id;
  -- else 
        raise notice '-------- Exclusão de registros de taxa de limpeza e OTA -------------';
        if (TG_OP <> 'INSERT') then 
        		-- Comando para excluir os registros relacionados à taxa de limpeza e ota
        		DELETE FROM closing_host_cleaning_fee where reservation_id = NEW.id;		
        		DELETE FROM closing_ota_commission where reservation_id = NEW.id;
        end if;
        
    		raise notice '-------- Inserção de registros de transferencia -------------';
    	
    		open cleaning_cursor(NEW.id);
    	 
    		loop
    			fetch cleaning_cursor into cleaning_rec;
    			exit when not found;
    		
    			if new.status in ('Concluded', 'No-Show') then
    				-- Inserir taxa de limpeza do HOST	 
    				INSERT INTO closing_host_cleaning_fee (reservation_id, property_id, host_id, accrual_date, cash_date, value, has_extension, created_at, updated_at) VALUES ( 
    					cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.host_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.cleaning_commission, cleaning_rec.has_extension, now(), now());
    	
    				-- Inserir taxa de limpeza recebida HOST	 
    				INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
    				VALUES ( 
    					cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.host_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.cleaning_commission, 'input', 'cleaning_fee', 'Taxa de limpeza a partir de uma reserva', 'reservation_reservation', cleaning_rec.reservation_id, now(), now());		
    	
    				-- Inserir taxa de limpeza paga ao HOST	 
    				INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
    				VALUES ( 
    					cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.cleaning_commission, 'output', 'cleaning_fee', 'Taxa de limpeza paga a um anfitrião', 'reservation_reservation', cleaning_rec.reservation_id, now(), now()); 				
    			end if;
    		
    			-- Inserir comissao OTA
    			INSERT INTO closing_ota_commission(reservation_id, property_id, ota_id, accrual_date, cash_date, value, fee, created_at, updated_at) VALUES ( 
    				cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.ota_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.ota_commission, cleaning_rec.ota_fee, now(), now()); 
    						
    			-- Inserir receita da reserva recebida pela SEAZONE	 
    			INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
    			VALUES ( 
    				cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.total_price, 'input', 'reservation_revenue', 'Receita total recebida pela Seazone a partir de uma reserva', 'reservation_reservation', cleaning_rec.reservation_id, now(), now()); 		
    			-- Inserir taxa de limpeza paga a OTA
    			INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
    			VALUES ( 
    				cleaning_rec.reservation_id, cleaning_rec.property_id, cleaning_rec.accrual_date, cleaning_rec.cash_date, cleaning_rec.ota_commission, 'output', 'ota_commission', 'Comissão para à OTA para uma reserva', 'reservation_reservation', cleaning_rec.reservation_id, now(), now()); 		
    			
    		end loop;
    		close cleaning_cursor;

    	    raise notice '-------- Fim de Execução -------------';
      end if;
  -- end if;		
	
  RETURN new;
  
END;
$function$
;
```


---

# Algoritmo e Regras de Negócio sobre a tabela *financial_expenses*

Esta tabela é responsável por armazenar os dados sobre as despesas associadas a propriedades gerenciados pela Seazone. Ela possui impacto direto em todas as tabelas relacionadas ao fechamento financeiro.

## Algoritmo de Processamento de Despesas

```bash
function processing_expenses(expense_id INTEGER)
 
  excluir despesa das tabelas de fechamento (caso seja um UPDATE)
      closing_seazone_resume, closing_host_resume, closing_property_resume 
      com transfer_category = DEBITED_EXPENSE
  excluir reembolsos de despesa das tabelas de fechamento (caso seja um UPDATE)
      closing_seazone_resume, closing_host_resume, closing_property_resume 
      com transfer_category = REFUND_EXPENSE
      
  identificar quem pagou pela despesa: Seazone, Host ou Proprietário
  Se foi pago pela Seazone então
     inserir registro de despesa em closing_seazone_resume como DEBITED_EXPENSE (output)
  Se foi pago pelo Host então
     identificar o ID do Host
     inserir registro de despesa em closing_host_resume como DEBITED_EXPENSE (output)
  Se foi pago pelo Proprietário então
   inserir registro de despesa em closing_property_resume como DEBITED_EXPENSE (output)

  identificar quem recebeu pela despesa: Seazone, Host ou Proprietário
  Se foi recebido pela Seazone então
     inserir registro de despesa em closing_seazone_resume como REFUND_EXPENSE (input)
  Se foi recebido pelo Host então
     identificar o ID do Host
     inserir registro de despesa em closing_host_resume como REFUND_EXPENSE (input)
  Se foi recebido pelo Proprietário então
   inserir registro de despesa em closing_property_resume como REFUND_EXPENSE (input)

end
```

## Regras de Negócio

* O dia da fatura de uma despesa será dia data de aprovação. Caso ela esteja vazia, usaremos a data do registro da despesa.
* Apenas despesas com status `Approved` podem ser processadas.

## Trigger sobre a tabela *financial_expenses*

### Código de Criação da Trigger

```sql
DROP TRIGGER IF EXISTS financial_expenses_changes
  ON financial_expenses;
  
CREATE TRIGGER financial_expenses_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_expenses
  FOR EACH ROW
  EXECUTE PROCEDURE register_expenses();
```

### Função para Calcular Valores de Despesas

```sql
-- DROP FUNCTION public.register_expenses();

CREATE OR REPLACE FUNCTION public.register_expenses()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	fe_id INTEGER;
	old_prop_id INTEGER;
	ac_date DATE;
	descrip VARCHAR(1200);
	valor_despesa FLOAT;
  	expense_record RECORD;

begin

	fe_id := NEW.id;

	raise notice '-------- Inserção de registro de despesa de ID % -------------', fe_id;

 	select into expense_record fe.id, fe.property_id, fe.reason, expense_status, paid_by, approval_date, register_date, 
		value, CAST(concat(fe.reason, ': ', fe.description) as varchar(1000)) as description, 
		fe.received_by, received_by_user, paid_by_user, fe.received_by_user, paid_host.id paid_host_id, 
		received_host.id received_host_id
	from financial_expenses fe 
	left join account_host paid_host on paid_host.user_id = fe.paid_by_user 
	left join account_host received_host on received_host.user_id = fe.received_by_user 
	where fe.id = fe_id;

	descrip := CONCAT('Paid to: ',expense_record.received_by_user,' - ', expense_record.description);
	
 	-- Regra de negócio que usa a data de registro para despesas de antes de 2024	
	if date(expense_record.register_date) <= '2023-12-31' then 
		ac_date = date(expense_record.register_date at time zone 'America/Sao_Paulo');
	else 
		ac_date = date(coalesce(expense_record.approval_date at time zone 'America/Sao_Paulo', expense_record.register_date at time zone 'America/Sao_Paulo'));
	end if;
	if (TG_OP = 'DELETE') or (expense_record.expense_status <> 'Approved') or (expense_record.paid_by is null) or (expense_record.received_by is null) or (expense_record.property_id is null) then 
		valor_despesa := 0;		
		raise notice '-------- Delete reembolsos % -------------', expense_record.id;
		DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
		DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
		DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
		DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
		DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
		DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';

	else 
		valor_despesa = expense_record.value;				
	
		-- Seção de despesas
		case 
	    when expense_record.paid_by = 'Owner' then
			DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
			DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';

			update closing_property_resume 
			set accrual_date = ac_date,
				cash_date = ac_date, 
				value = valor_despesa,
				description = descrip,
	            property_id = expense_record.property_id, 
				updated_at = now()
			where source_id = fe_id and source_table = 'financial_expenses' and transfer_category = 'debited_expense';    		
		
	    	if not found then
	    		if valor_despesa > 0 then 
	    			INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
	    			VALUES (null, expense_record.property_id, ac_date, ac_date, valor_despesa, 'output', 'debited_expense', descrip, 'financial_expenses', expense_record.id,now(), now());								    	
	    		end if;
	    	end if;
		 when expense_record.paid_by = 'Host' then	 
			DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
			DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
 
		  	update closing_host_resume 
			set accrual_date = ac_date,
				cash_date = ac_date,
				host_id = expense_record.paid_host_id,
				value = valor_despesa,
				description = descrip, 
	            property_id = expense_record.property_id,
				updated_at = now()
			where source_id = fe_id and source_table = 'financial_expenses' and transfer_category = 'debited_expense';    		
		
	    	if not found then
	    		if valor_despesa > 0 then
		    		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		    		VALUES (null, expense_record.property_id, expense_record.paid_host_id, ac_date, ac_date, valor_despesa, 'output', 'debited_expense', descrip, 'financial_expenses', expense_record.id, now(), now());								
		    	end if;
	    	end if;
	    	
	    when expense_record.paid_by = 'Seazone' then
			DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';
			DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'debited_expense';

			update closing_seazone_resume 
			set accrual_date = ac_date,
				cash_date = ac_date,
				value = valor_despesa,
				description = descrip, 
	            property_id = expense_record.property_id,
				updated_at = now()
			where source_id = fe_id and source_table = 'financial_expenses' and transfer_category = 'debited_expense';    		
	
	    	if not found then     
	    		if valor_despesa > 0 then
		    		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		    		VALUES (null, expense_record.property_id, ac_date, ac_date, valor_despesa, 'output', 'debited_expense', descrip, 'financial_expenses', expense_record.id,now(), now());								
		    	end if;
	    	end if;
	    else 
			raise notice '-------- Registro de despesa sem paid_by -------------';    		
		end case; 
	
		descrip := CONCAT('Received from: ',expense_record.paid_by_user,' - ', expense_record.description);
		
		-- Seção de reembolsos
		if (expense_record.reason not like 'Account_%') and (expense_record.reason <> 'Seazone_Charges') then 
			CASE
		    when expense_record.received_by = 'Owner' then	
				DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
				DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';		

				update closing_property_resume 
				set accrual_date = ac_date,
					cash_date = ac_date,
					value = valor_despesa,
					description = descrip, 
		            property_id = expense_record.property_id,
					updated_at = now()
				where source_id = fe_id and source_table = 'financial_expenses' and transfer_category = 'refund_expense';    		
			
				if not found then   
					if valor_despesa > 0 then
			    		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
			    		VALUES (null, expense_record.property_id, ac_date, ac_date, valor_despesa, 'input', 'refund_expense', descrip, 'financial_expenses', expense_record.id,now(), now());								
			    	end if;
		    	end if;

		  	when expense_record.received_by = 'Host' then
				DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
				DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';

				update closing_host_resume 
				set accrual_date = ac_date,
					cash_date = ac_date,
					host_id = expense_record.received_host_id,
					value = valor_despesa,
					description = descrip,
		            property_id = expense_record.property_id, 
					updated_at = now()
				where source_id = fe_id and source_table = 'financial_expenses' and transfer_category = 'refund_expense';    		
		
				if not found then 	
					if valor_despesa > 0 then
			    		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
			    		VALUES (null, expense_record.property_id, expense_record.received_host_id, ac_date, ac_date, valor_despesa, 'input', 'refund_expense', descrip, 'financial_expenses', expense_record.id, now(), now());								
			    	end if;
		    	end if;

		  	when expense_record.received_by = 'Seazone' then
				DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
				DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';

				update closing_seazone_resume 
				set accrual_date = ac_date,
					cash_date = ac_date,
					value = valor_despesa,
					description = descrip,
		            property_id = expense_record.property_id, 
					updated_at = now()
		    	where source_id = fe_id and source_table = 'financial_expenses' and transfer_category = 'refund_expense';    		
		
		    	if not found then     	
		    		if valor_despesa > 0 then
			    		raise notice '-------- Insert de reembolso de Seazone % -------------', expense_record.id;
			    		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
			    		VALUES (null, expense_record.property_id, ac_date, ac_date, valor_despesa, 'input', 'refund_expense', descrip, 'financial_expenses', expense_record.id,now(), now());								
			    	end if;
		    	end if;

		      else 
					raise notice '-------- Registro de despesa sem received_by -------------';    		  	
			end case; 	
		else 
			raise notice '-------- Delete reembolsos % -------------', expense_record.id;
			DELETE from closing_seazone_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
			DELETE from closing_host_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense';
			DELETE from closing_property_resume where source_table = 'financial_expenses' and source_id = expense_record.id and transfer_category = 'refund_expense'; 	
		end if;
	end if; 
	 		
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```


---

# Algoritmo e Regras de Negócio sobre a tabela *financial_host_manual_fit*

Esta tabela é responsável por armazenar os dados sobre ajustes positivos ou negativos associados ao fechamento financeiro de um Host.

## Algoritmo de Processamento de Ajustes Manuais de Host

```bash
function processing_host_manual_fit(host_manual_fit_id INTEGER)
 
  excluir ajuste de closing_host_resume (caso seja um UPDATE)
       com transfer_category = MANUAL_FIT
  excluir ajuste com valor invertido de closing_seazone_resume (caso seja UPDATE)
      com transfer_category = MANUAL_FIT
      
  inserir registro de ajuste em closing_host_resume como MANUAL_FIT (input/output)
  inserir registro reverso de ajuste em closing_seazone_resume como MANUAL_FIT

end
```

## Regras de Negócio

* É preciso identificar se o ajuste é positivo ou negativo. Se for positivo, então deve ser lançado um registro negativo na tabela de extrato da Seazone. Se for negativo, então deve ser lançado um registro positivo na tabela de extrato da Seazone.

## Trigger sobre a tabela *financial_host_manual_fit*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS host_manual_fit_changes
  ON financial_host_manual_fit;
  
CREATE TRIGGER host_manual_fit_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_host_manual_fit
  FOR EACH ROW
  EXECUTE PROCEDURE register_host_manual_fit();	
```

### Função para calcular valores e tipos de ajustes manuais

```sql
CREATE OR REPLACE FUNCTION public.register_host_manual_fit()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	seazone_type public.transfer_types;
	host_type public.transfer_types;	

begin

	-- Comando para excluir os registros relacionados à propriedade
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 
		raise notice '-------- Exclusão dos registros de ajuste manual -------------';
		DELETE FROM closing_host_resume where transfer_category in ('manual_fit') and source_table = 'financial_host_manual_fit' and source_id = OLD.id;
		DELETE FROM closing_seazone_resume where transfer_category in ('manual_fit')  and source_table = 'financial_host_manual_fit' and source_id = OLD.id;
	end if;

	raise notice '-------- Inserção de registros de ajuste manual -------------';

	if NEW.is_adding is true then	
			seazone_type := 'output';
			host_type := 'input';		
	else
			seazone_type := 'input';
			host_type := 'output';		
	end if; 

	-- raise notice '-------- Registro de ajuste manual do HOST % -------------', mfit_record.id;
	INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
	VALUES (null, NEW.property_id, NEW.host_id, NEW.date_ref, NEW.date_ref, NEW.value, host_type, 'manual_fit', NEW.description, 'financial_host_manual_fit', NEW.id, now(), now());										

	-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', mfit_record.id;
	INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
	VALUES (null, NEW.property_id, NEW.date_ref, NEW.date_ref, NEW.value, seazone_type, 'manual_fit', NEW.description, 'financial_host_manual_fit', NEW.id, now(), now());										
	 		
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

PAREI AQUI!!!

# Trigger sobre a tabela *financial_property_manual_fit*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS property_manual_fit_changes
  ON financial_property_manual_fit;
  
CREATE TRIGGER property_manual_fit_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_property_manual_fit
  FOR EACH ROW
  EXECUTE PROCEDURE register_property_manual_fit();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_property_manual_fit();

CREATE OR REPLACE FUNCTION public.register_property_manual_fit()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	prop_id INTEGER;
	old_prop_id INTEGER;
	seazone_type public.transfer_types;
	property_type public.transfer_types;	

begin
	-- Comando para excluir os registros relacionados à propriedade
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 
		old_prop_id := OLD.property_id;
		raise notice '-------- Exclusão dos registros de ajuste manual -------------';
		DELETE FROM closing_property_resume where property_id = old_prop_id and transfer_category in ('manual_fit') and source_table = 'financial_property_manual_fit' and source_id = OLD.id;
		DELETE FROM closing_seazone_resume where property_id = old_prop_id and transfer_category in ('manual_fit')  and source_table = 'financial_property_manual_fit' and source_id = OLD.id;
	end if;

	prop_id := NEW.property_id;
		
	raise notice '-------- Inserção de registros de ajuste manual -------------';

	if prop_id is not null then
	
		if NEW.is_adding is true then	
				seazone_type := 'output';
				property_type := 'input';		
		else
				seazone_type := 'input';
				property_type := 'output';		
		end if; 
	
		-- raise notice '-------- Registro de ajuste manual do PROPERTY % -------------', NEW.id;
		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, NEW.property_id, NEW.date_ref, NEW.date_ref, NEW.value, property_type, 'manual_fit', NEW.description, 'financial_property_manual_fit', NEW.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, NEW.property_id, NEW.date_ref, NEW.date_ref, NEW.value, seazone_type, 'manual_fit', NEW.description, 'financial_property_manual_fit', NEW.id, now(), now());										
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *financial_cleaning_fee_manual_fit*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS cleaning_fee_manual_fit_changes
  ON financial_cleaning_fee_manual_fit;
  
CREATE TRIGGER cleaning_fee_manual_fit_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_cleaning_fee_manual_fit
  FOR EACH ROW
  EXECUTE PROCEDURE register_cleaning_fee_manual_fit();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
CREATE OR REPLACE FUNCTION public.register_cleaning_fee_manual_fit()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	res_id INTEGER;
	old_res_id INTEGER;
	seazone_type public.transfer_types;
	host_type public.transfer_types;

	clean_record RECORD;
   
    clean_cursor CURSOR (res_id integer) for
    	select fcfmf.id, fcfmf.reservation_id, rr.property_id, rr.host_id, fcfmf.date_ref, fcfmf.value, fcfmf.description, fcfmf.is_adding,
		CASE
	            WHEN ros.payment_delay = 0 then fcfmf.date_ref
	            else (fcfmf.date_ref + interval '1 month')::date
	        end as cash_date
		from financial_cleaning_fee_manual_fit fcfmf  
		join reservation_reservation rr on fcfmf.reservation_id = rr.id
		join reservation_ota_setup ros on rr.ota_id = ros.ota_id		
		where fcfmf.reservation_id = res_id and rr.status in ('Concluded', 'No-Show') and rr.is_blocking is false;

begin

	-- Comando para excluir os registros relacionados ao host
    if (TG_OP = 'INSERT') then 		
    	old_res_id := NEW.reservation_id;
    else
        old_res_id := OLD.reservation_id;
    end if; 
	raise notice '-------- Exclusão dos registros de ajuste manual de taxa de limpeza -------------';
	DELETE FROM closing_host_resume where reservation_id = old_res_id and transfer_category in ('cleaning_manual_fit') and source_table = 'financial_cleaning_fee_manual_fit';
	DELETE FROM closing_seazone_resume where reservation_id = old_res_id and transfer_category in ('cleaning_manual_fit')  and source_table = 'financial_cleaning_fee_manual_fit';

	res_id := NEW.reservation_id;
	
	raise notice '-------- Inserção de registros de ajuste manual de taxa de limpeza -------------';

	open clean_cursor(res_id);
 
	loop
		fetch clean_cursor into clean_record;
		exit when not found;
		
		if clean_record.is_adding is true then	
			seazone_type := 'output';
			host_type := 'input';		
		else
			seazone_type := 'input';
			host_type := 'output';		
		end if; 

		-- raise notice '-------- Registro de ajuste manual do HOST % -------------', NEW.id;
		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (clean_record.reservation_id, clean_record.property_id, clean_record.host_id, clean_record.date_ref, clean_record.cash_date, clean_record.value, host_type, 'cleaning_manual_fit', clean_record.description, 'financial_cleaning_fee_manual_fit', clean_record.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (clean_record.reservation_id, clean_record.property_id, clean_record.date_ref, clean_record.cash_date, clean_record.value, seazone_type, 'cleaning_manual_fit', clean_record.description, 'financial_cleaning_fee_manual_fit', clean_record.id, now(), now());										
	 		
	end loop;
	
	close clean_cursor;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *financial_reservation_manual_fit*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS reservation_manual_fit_changes
  ON financial_reservation_manual_fit;
 
CREATE TRIGGER reservation_manual_fit_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_reservation_manual_fit
  FOR EACH ROW
  EXECUTE PROCEDURE register_reservation_manual_fit();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_reservation_manual_fit();

CREATE OR REPLACE FUNCTION public.register_reservation_manual_fit()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	res_id INTEGER;
	old_res_id INTEGER;
	seazone_type public.transfer_types;
	property_type public.transfer_types;

	res_record RECORD;
    -- na query checa se a data do ajuste é antes ou depois do inicio do fechamento 3.0. No 2.0 a data de accrual/cash_date é a data do ajuste. No 3.0 o accrual/cash_date deve ser a data de checkout da reserva
    res_cursor CURSOR (res_id integer) for
		select frmf.id, frmf.reservation_id, rr.code, rr.property_id, rr.seazone_fee, rr.host_fee, rr.host_id, 
				frmf.date_ref as new_date_ref, frmf.value, concat(frmf.problem_type,': ', frmf.description) as description, frmf.is_adding,
	    		CASE
	            WHEN ros.payment_delay = 0 then frmf.date_ref
	            else (frmf.date_ref + interval '1 month')::date
	        end as cash_date
			from financial_reservation_manual_fit frmf  
			join reservation_reservation rr on frmf.reservation_id = rr.id
			join reservation_ota_setup ros on rr.ota_id = ros.ota_id		
			where frmf.reservation_id = res_id and rr.status in ('Concluded', 'No-Show') and rr.is_blocking is false;    
    
begin

	-- Comando para excluir os registros relacionados à propriedade
	if (TG_OP = 'INSERT') then 		
    	old_res_id := NEW.reservation_id;
    else
        old_res_id := OLD.reservation_id;
    end if; 
	raise notice '-------- Exclusão dos registros de ajuste manual de reserva -------------';
	DELETE FROM closing_property_resume where reservation_id = old_res_id and transfer_category in ('reservation_manual_fit', 'commission_fit', 'host_commission_fit', 'seazone_commission_fit') and source_table = 'financial_reservation_manual_fit';
	DELETE FROM closing_seazone_resume where reservation_id = old_res_id and transfer_category in ('reservation_manual_fit', 'commission_fit', 'seazone_commission_fit') and source_table = 'financial_reservation_manual_fit';
	DELETE FROM closing_host_resume where reservation_id = old_res_id and transfer_category in ('commission_fit', 'host_commission_fit')  and source_table = 'financial_reservation_manual_fit';	

	res_id := NEW.reservation_id;
	
	raise notice '-------- Inserção de registros de ajuste manual de reserva -------------';

	open res_cursor(res_id);
 
	loop
		fetch res_cursor into res_record;
		exit when not found;
	
		if res_record.is_adding is true then	
			seazone_type := 'output';
			property_type := 'input';		
		else
			seazone_type := 'input';
			property_type := 'output';		
		end if; 
	
		-- raise notice '-------- Registro de ajuste manual de PROPERTY % -------------', NEW.id;		
		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value, property_type, 'reservation_manual_fit', res_record.description, 'financial_reservation_manual_fit', res_record.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value, seazone_type, 'reservation_manual_fit', res_record.description, 'financial_reservation_manual_fit', res_record.id, now(), now());										
	
		-- raise notice '-------- Registro de estorno de comissao da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.seazone_fee, property_type, 'seazone_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());										

		-- raise notice '-------- Registro de estorno de comissao da HOST % -------------', NEW.id;
		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.host_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.host_fee, property_type, 'host_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());										

		-- raise notice '-------- Registro de estorno para PROPERTY de comissao paga ao HOST e SEAZONE % -------------', NEW.id;
		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.host_fee, seazone_type, 'host_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());

    	INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.seazone_fee, seazone_type, 'seazone_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());
	
	end loop;
	
	close res_cursor;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *financial_host_property_ted*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS host_property_ted_changes
  ON financial_host_property_ted;
 
CREATE TRIGGER host_property_ted_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_host_property_ted
  FOR EACH ROW
  EXECUTE PROCEDURE register_host_property_ted();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
CREATE OR REPLACE FUNCTION public.register_host_property_ted()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	new_host_id INTEGER;
	old_host_id INTEGER;

begin

	-- Comando para excluir os registros relacionados à propriedade
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 		
    	old_host_id := OLD.host_id; 
	    raise notice '-------- Exclusão dos registros de repasse de host -------------';
	    DELETE FROM closing_host_resume where host_id = old_host_id and transfer_category in ('host_payment') and source_table = 'financial_host_property_ted' and source_id = OLD.id;
	    DELETE FROM closing_seazone_resume where transfer_category in ('host_payment')  and source_table = 'financial_host_property_ted' and source_id = OLD.id;
    end if;

	new_host_id := NEW.host_id;

	raise notice '-------- Inserção de registros de repasse de host -------------';

	if new_host_id is not null then
	
		-- raise notice '-------- Registro de ajuste manual do HOST % -------------', NEW.id;
		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.host_id, NEW.payment_date, NEW.date_ref, NEW.value, 'output', 'host_payment', CONCAT('Pagamento ao Anfitrião referente ao mês: ', new.date_ref) , 'financial_host_property_ted', NEW.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.payment_date, NEW.date_ref, NEW.value, 'input', 'host_payment', CONCAT('Pagamento ao Anfitrião ID ', NEW.host_id, ' referente ao mês: ', new.date_ref), 'financial_host_property_ted', NEW.id, now(), now());										
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *financial_owner_property_ted*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS owner_property_ted_changes
  ON financial_owner_property_ted;
 
CREATE TRIGGER owner_property_ted_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_owner_property_ted
  FOR EACH ROW
  EXECUTE PROCEDURE register_owner_property_ted();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_owner_property_ted();

CREATE OR REPLACE FUNCTION public.register_owner_property_ted()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	new_property_id INTEGER;
	old_property_id INTEGER;

begin

	-- Comando para excluir os registros relacionados à propriedade
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 
		old_property_id := OLD.property_id;
		raise notice '-------- Exclusão dos registros de repasse de propriedade -------------';
		DELETE FROM closing_property_resume where property_id = old_property_id and transfer_category in ('owner_payment') and source_table = 'financial_owner_property_ted' and source_id = OLD.id;
		DELETE FROM closing_seazone_resume where property_id = old_property_id and transfer_category in ('owner_payment')  and source_table = 'financial_owner_property_ted' and source_id = OLD.id;
	end if;

	new_property_id := NEW.property_id;

	if new_property_id is not null then
		raise notice '-------- Inserção de registros de repasse de propriedade -------------';
	
		-- raise notice '-------- Registro de ajuste manual do PROPERTY % -------------', NEW.id;
		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, NEW.property_id, NEW.payment_date, NEW.date_ref, NEW.value, 'output', 'owner_payment', CONCAT('Pagamento ao Proprietário referente ao mês: ', new.date_ref) , 'financial_owner_property_ted', NEW.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, NEW.property_id, NEW.payment_date, NEW.date_ref, NEW.value, 'input', 'owner_payment', CONCAT('Pagamento ao Proprietario referente ao mês: ', new.date_ref), 'financial_owner_property_ted', NEW.id, now(), now());										
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *property_handover_details*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS property_handover_details_changes
  ON property_handover_details;
 
CREATE TRIGGER property_handover_details_changes
  AFTER INSERT or UPDATE or DELETE
  ON property_handover_details
  FOR EACH ROW
  EXECUTE PROCEDURE register_property_implantation_fee();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_property_implantation_fee();

CREATE OR REPLACE FUNCTION public.register_property_implantation_fee()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	
	new_property_id INTEGER;
	old_property_id INTEGER;
	counter INTEGER;
	total_loop INTEGER;
	fee_value FLOAT8;	
	negative_value BOOLEAN;
	prop_start_date DATE;

begin	

	-- Comando para excluir os registros relacionados à propriedade
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 
		old_property_id := OLD.property_id;
		raise notice '-------- Exclusão dos registros de taxa de implantação -------------';
		DELETE FROM closing_property_resume where property_id = old_property_id and transfer_category in ('implantation_fee') and source_table = 'property_handover_details' and source_id = OLD.id;
		DELETE FROM closing_seazone_resume where property_id = old_property_id and transfer_category in ('implantation_fee')  and source_table = 'property_handover_details' and source_id = OLD.id;
	end if;

	new_property_id := NEW.property_id;

	raise notice '-------- Inserção de registros de taxa de implantação -------------';

	if new_property_id is not null then
		negative_value := false;
		total_loop := 1;	
		fee_value := NEW.implantation_fee_total_value;
		select contract_start_date from property_property into prop_start_date where id = NEW.property_id;

		case 
			when new.implantation_fee_total_value = 0 then
				negative_value := false;
			when new.payment_method = 'Installments' then
				total_loop := new.payment_installments;
				fee_value := NEW.implantation_fee_total_value / new.payment_installments;		
  			when new.payment_method in ('PIX', 'On_Budget', 'Credit_Card', 'Bank_Slip') then
				negative_value := true;		
			else -- do nothing
		end case;
	
		counter := 0;
		
		while counter < total_loop loop
			
			-- raise notice '-------- Registro de taxa de implantação do PROPERTY % -------------', NEW.id;
			INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
			VALUES (null, NEW.property_id, date(prop_start_date), date(prop_start_date + interval '1 month' * counter), abs(fee_value), 'output', 'implantation_fee', CONCAT(new.payment_method, ': Pagamento de Taxa de Implantação'), 'property_handover_details', NEW.id, now(), now());										
		
			if negative_value then
				-- raise notice '-------- Registro de taxa de implantação do PROPERTY % -------------', NEW.id;
				INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
				VALUES (null, NEW.property_id, date(prop_start_date), date(prop_start_date + interval '1 month' * counter), abs(fee_value), 'input', 'implantation_fee', CONCAT(new.payment_method, ': Estorno de Pagamento de Taxa de Implantação'), 'property_handover_details', NEW.id, now(), now());													
			else 
				-- raise notice '-------- Registro de taxa de implantação da SEAZONE % -------------', NEW.id;
				INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
				VALUES (null, NEW.property_id, date(prop_start_date), date(prop_start_date + interval '1 month' * counter), abs(fee_value), 'input', 'implantation_fee', CONCAT(new.payment_method, ': Recebimento de Taxa de Implantação'), 'property_handover_details', NEW.id, now(), now());													
			end if;	
			counter := counter + 1;
		end loop;
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *closing_property_resume*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS closing_property_resume_changes
  ON closing_property_resume;
 
CREATE TRIGGER closing_property_resume_changes
  AFTER INSERT or UPDATE or DELETE
  ON closing_property_resume
  FOR EACH ROW
  EXECUTE PROCEDURE register_property_balance();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_property_balance();

CREATE OR REPLACE FUNCTION public.register_property_balance()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
  multiplier INTEGER;
  saldo_anterior FLOAT;
  month_ref DATE;

begin
	 if (NEW.transfer_category is NULL OR NEW.transfer_category not in ('host_commission', 'seazone_commission', 'property_revenue')) AND (OLD.transfer_category is NULL OR OLD.transfer_category not in ('host_commission', 'seazone_commission', 'property_revenue')) then
		month_ref := NEW.cash_date;
		if NEW.cash_date > OLD.cash_date OR NEW.cash_date is null then
			month_ref := OLD.cash_date;
		end if;
		raise notice '-------- CPR: Atualizando o saldo do imovel % a partir do mes % -------------', coalesce(NEW.property_id, OLD.property_id), month_ref;

		if OLD.property_id <> NEW.property_id then
				perform calculate_property_balance(OLD.property_id, OLD.cash_date);
		end if;

		perform calculate_property_balance(NEW.property_id, NEW.cash_date);

		raise notice '-------- Fim de Execução -------------';
	 end if;

	RETURN new;

END;
$function$
;
```

# Trigger sobre a tabela *closing_host_resume*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS closing_host_resume_changes
  ON closing_host_resume;
 
CREATE TRIGGER closing_host_resume_changes
  AFTER INSERT or UPDATE or DELETE
  ON closing_host_resume
  FOR EACH ROW
  EXECUTE PROCEDURE register_host_balance();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_host_balance();

CREATE OR REPLACE FUNCTION public.register_host_balance()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	multiplier INTEGER;
	saldo_anterior FLOAT;
	month_ref DATE;	

begin

if (TG_OP = 'DELETE') then

    if OLD.transfer_type = 'output' then
    	multiplier := -1;
    end if;
	-- raise notice '-------- DELETE: Atualizando o saldo % -------------', OLD.id;
	UPDATE closing_host_balance cb SET value = value - (OLD.value * multiplier)
	from (select id from closing_host_balance
		WHERE host_id = OLD.host_id AND date_ref >= date_trunc('month', OLD.cash_date) FOR UPDATE SKIP LOCKED) as sub
	where cb.id = sub.id;

else
	if NEW.transfer_category not in ('host_commission', 'cleaning_fee') then
		multiplier := 1;
	    if NEW.transfer_type = 'output' then
	        multiplier := -1;
	    end if;
	
     	month_ref := date_trunc('month', NEW.cash_date);

		UPDATE closing_host_balance cb SET updated_at = now(), value = value + (NEW.value * multiplier)
		from (select id from closing_host_balance
			WHERE host_id = NEW.host_id AND date_ref = month_ref FOR UPDATE SKIP LOCKED) as sub
		where cb.id = sub.id;


		if not found then
			-- Obtendo saldo do mês anterior ao registro
	        select value from closing_host_balance into saldo_anterior where host_id = NEW.host_id and date_ref < month_ref order by date_ref desc limit 1;
	        -- Inserindo o saldo do mes do registro
	        raise notice '-------- Inserindo o saldo do mes % = % -------------', month_ref, coalesce(saldo_anterior,0);
	        INSERT INTO closing_host_balance (host_id, date_ref, value, created_at, updated_at)
	        VALUES (NEW.host_id, month_ref, coalesce(saldo_anterior,0) + (NEW.value * multiplier), now(), now());
		end if;

		UPDATE closing_host_balance cb SET updated_at = now(), value = value + (NEW.value * multiplier)
		from (select id from closing_host_balance
			WHERE host_id = NEW.host_id AND date_ref > month_ref FOR UPDATE SKIP LOCKED) as sub
		where cb.id = sub.id;
	
	    if (TG_OP = 'UPDATE') then
		 	multiplier := 1;
	        if OLD.transfer_type = 'output' then
	            multiplier := -1;
	        end if;
	        month_ref := date_trunc('month', OLD.cash_date);
	
	        -- Atualizando o saldo dos meses
			UPDATE closing_host_balance cb SET updated_at = now(), value = value - (OLD.value * multiplier)
			from (select id from closing_host_balance
				WHERE host_id = OLD.host_id AND date_ref >= month_ref FOR UPDATE SKIP LOCKED) as sub
			where cb.id = sub.id;
	    end if;
  	end if;  	
end if;
raise notice '-------- Fim de Execução -------------';

RETURN new;

END;
$function$
;
```

# Trigger sobre a tabela *financial_host_franchise_fee_payment*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS franchise_fee_payment_changes
  ON financial_host_franchise_fee_payment;

CREATE TRIGGER franchise_fee_payment_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_host_franchise_fee_payment
  FOR EACH ROW
  EXECUTE PROCEDURE register_host_franchise_fee_payment();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_host_franchise_fee_payment();

CREATE OR REPLACE FUNCTION public.register_host_franchise_fee_payment()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
	
begin
	-- Comando para excluir os registros relacionados ao pagamento do Host
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 
		raise notice '-------- Exclusão dos registros de pagamento de taxa de franquia -------------';
		DELETE FROM closing_host_resume where host_id = OLD.host_id and transfer_category in ('franchise_fee') and source_table = 'financial_host_franchise_fee_payment' and source_id = OLD.id;
        DELETE FROM closing_seazone_resume where transfer_category in ('franchise_fee') and source_table = 'financial_host_franchise_fee_payment' and source_id = OLD.id;
		UPDATE financial_host_franchise_fee SET debit_balance = debit_balance + OLD.value where host_id = OLD.host_id;
	end if;
		
	raise notice '-------- Inserção de registros de pagamento de taxa de franquia % -------------', NEW.id;

	if NEW.host_id is not null and NEW.payment_method = 'commission_abatement' then
	
		INSERT INTO closing_host_resume (reservation_id, host_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, NEW.host_id, null, NEW.payment_date, NEW.date_ref, NEW.value, 'output', 'franchise_fee', CONCAT('Taxa de Franquia: ', NEW.ID, ' Forma de Pagamento: ', NEW.payment_method), 'financial_host_franchise_fee_payment', NEW.id, now(), now());										

		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.payment_date, NEW.date_ref, NEW.value, 'input', 'franchise_fee', CONCAT('Taxa de Franquia: ', NEW.ID, ' Host: ', NEW.host_id), 'financial_host_franchise_fee_payment', NEW.id, now(), now());										

    UPDATE financial_host_franchise_fee SET debit_balance = debit_balance - NEW.value where host_id = NEW.host_id;
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *property_property*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS property_property_changes
  ON property_property;

CREATE TRIGGER property_property_changes
  AFTER UPDATE
  ON property_property
  FOR EACH ROW
  EXECUTE PROCEDURE change_property_property();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.change_property_property();

CREATE OR REPLACE FUNCTION public.change_property_property()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

begin

   if (TG_OP = 'UPDATE') then
      if OLD.host_id <> NEW.host_id OR OLD.comission_fee <> NEW.comission_fee OR OLD.host_reservation_comission_fee <> NEW.host_reservation_comission_fee then
          raise notice '-------- UPDATE reservas PROPERTY %: HOST: % COMISSAO PROPERTY: %  COMISSAO HOST: % -------------', NEW.id, NEW.host_id, NEW.comission_fee, NEW.host_reservation_comission_fee;
          UPDATE reservation_reservation SET host_id = NEW.host_id, property_fee = NEW.comission_fee, host_fee = NEW.host_reservation_comission_fee, seazone_fee = (NEW.comission_fee - NEW.host_reservation_comission_fee) where property_id = NEW.id AND check_in_date >= date_trunc('day', now());
      end if;          
      raise notice '-------- Fim de Execução -------------';
   end if;

   RETURN new;

END;
$function$
;
```

# Trigger sobre a tabela *closing_property_resume*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS closing_partner_resume_commission
  ON closing_property_resume;
 
CREATE TRIGGER closing_partner_resume_commission
  AFTER INSERT or UPDATE or DELETE
  ON closing_property_resume
  FOR EACH ROW
  EXECUTE PROCEDURE register_partner_commission();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
-- DROP FUNCTION public.register_host_balance();

CREATE OR REPLACE FUNCTION register_partner_commission()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare
	multiplier INTEGER;
	saldo_anterior FLOAT;
	month_ref DATE;	

begin

Se um registro de reserva
    Se delete
        apagar registros da tabela de parceiro
    Se update
        apagar registros da tabela de parceiro
        calcular comissao daquela reserva
    Se insert
        calcular comissao daquela reserva
        
raise notice '-------- Fim de Execução -------------';

RETURN new;

END;
$function$
;
```

# Trigger sobre a tabela *financial_partner_withdraw*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS partnet_withdraw_changes
  ON financial_partner_withdraw;
 
CREATE TRIGGER partnet_withdraw_changes
  AFTER INSERT or UPDATE or DELETE
  ON financial_partner_withdraw
  FOR EACH ROW
  EXECUTE PROCEDURE register_partner_withdraw();
```

### Função para calcular valores e tipos de ajustes manuais

```sql
CREATE OR REPLACE FUNCTION register_partner_withdraw()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$

declare

begin

	-- Comando para excluir os registros relacionados ao pagamento do parceiro
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 		
	    raise notice '-------- Exclusão dos registros de repasse de partner -------------';
	    DELETE FROM closing_partner_resume where partner_id = OLD.partner_id and transfer_category in ('partner_payment') and source_table = 'financial_partner_withdraw' and source_id = OLD.id;
	    DELETE FROM closing_seazone_resume where transfer_category in ('partner_payment')  and source_table = 'financial_partner_withdraw' and source_id = OLD.id;
    end if;

	raise notice '-------- Inserção de registros de repasse de partner -------------';

	if NEW.partner_id is not null then
	
		-- raise notice '-------- Registro de pagamento de PARTNER % -------------', NEW.id;
		INSERT INTO closing_partner_resume (reservation_id, property_id, partner_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.partner_id, NEW.date_paid, NEW.date_paid, NEW.value, 'output', 'partner_payment', CONCAT('Pagamento ao Parceiro referente ao mês: ', NEW.date_paid) , 'financial_partner_withdraw', NEW.id, now(), now());										

		-- raise notice '-------- Registro de pagamento de PARTNER % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.date_paid, NEW.NEW.date_paid, NEW.value, 'input', 'partner_payment', CONCAT('Pagamento ao Parceiro ID ', NEW.partner_id, ' referente ao mês: ', NEW.date_paid), 'financial_partner_withdraw', NEW.id, now(), now());										
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# 

# [Conversão de Dados do Fechamento v1 para o Fechamento v2 (de-para)](/doc/conversao-de-dados-do-fechamento-v1-para-o-fechamento-v2-de-para-DyPBLAKQzm)

### Tabela de Extrato da Propriedade: 

| **Elemento Fechamento V1** | **Elemento Fechamento V2** | **Tipo** | **Observação** |
|----|----|----|----|
| proper_pay_property_daily_transfer | closing_property_resume | Tabela | - |
| value | value | Coluna | - |
| description | description | Coluna | - |
| date | cash_date | Coluna | - |
| accrual_date | accrual_date | Coluna | - |
| cash_date | cash_date | Coluna | - |
| property_id | property_id | Coluna | - |
| type | transfer_category | Coluna | - |
| (sinal do campo value) | transfer_type | Coluna | * *input* indica valor positivo
* *output* indica valor negativo |

### Categorias de Itens do Extrato de Propriedade: 

| **Fechamento V1** | **Fechamento V2** | **Descrição** |
|----|----|----|
| expenses | debited_expense | Despesas lançadas |
| revenue | property_revenue | Receita da propriedade recebida pela diária |
| host_commission | host_commission | Comissão a ser paga ao Anfitrião |
| seazone_commission | seazone_commission | Comissão a ser paga à Seazone |
|    | host_commission_fit | Ajuste de comissão por conta de um ajuste manual da reserva, que impacta as comissões do Anfitrião |
|    | seazone_commission_fit | Ajuste de comissão por conta de um ajuste manual da reserva, que impacta as comissões daSeazone |
| ted | owner_payment | Repasse feito à propriedade |
| reservation_manual_fit | reservation_manual_fit | Ajuste manual de reserva |
| manual_fit | manual_fit | Ajuste manual feito diretamente à propriedade |
| refund | refund_expense | Reembolso de despesa |
| implantation_fee | implantation_fee | Taxa de implantação de propriedade |

### [Tabela de Saldo da Propriedade:](/doc/tabela-de-saldo-da-propriedade-QqcnYQZBbc) 

| **Elemento Fechamento V1** | **Elemento Fechamento V2** | **Tipo** |
|----|----|----|
| proper_pay_property_daily_balance | closing_property_balance | Tabela |
| property_id | property_id | Coluna |
| date_ref | date_ref | Coluna |
| value | value | Coluna |

Um ponto de diferença entre as versões é que no fechamento V1 o saldo era calculado diariamente. Já no fechamento V2 ele é calculado mensalmente.

### Tabela de Extrato do Anfitrião: 

| **Elemento Fechamento V1** | **Elemento Fechamento V2** | **Tipo** | **Observação** |
|----|----|----|----|
| proper_pay_host_daily_transfer | closing_host_resume | Tabela | - |
| value | value | Coluna | - |
| description | description | Coluna | - |
| date | cash_date | Coluna | - |
| accrual_date | accrual_date | Coluna | - |
| cash_date | cash_date | Coluna | - |
| host_id | host_id | Coluna |    |
| property_id | property_id | Coluna | - |
| type | transfer_category | Coluna | - |
| (sinal do campo value) | transfer_type | Coluna | * *input* indica valor positivo
* *output* indica valor negativo |
| reservation_id | reservation_id | Coluna |    |

### Categorias de Itens do Extrato de Anfitrião: 

| **Fechamento V1** | **Fechamento V2** | **Descrição** |
|----|----|----|
| debited_expenses | debited_expense | Despesas lançadas |
| onboarding_expenses | debited_expense | Despesas de implantação lançadas ao Anfitrião. |
| commission | host_commission | Comissão a ser paga ao Anfitrião |
|    | host_commission_fit | Ajuste de comissão por conta de um ajuste manual da reserva, que impacta as comissões do Anfitrião |
| cleaning_fee | cleaning_fee | Taxa de limpeza a ser paga ao Anfitrião |
| cleaning_manual_fit | cleaning_manual_fit | Ajuste manual de taxa de limpeza |
| ted | host_payment | Repasse feito ao anfitrião |
| manual_fit | manual_fit | Ajuste manual feito diretamente ao anfitrião |
| refund_expenses | refund_expense | Reembolso de despesa |
| franchise_fee | franchise_fee | Taxa de franquia paga pelo anfitrião |

### Tabela de Saldo do Anfitrião: 

| **Elemento Fechamento V1** | **Elemento Fechamento V2** | **Tipo** |
|----|----|----|
| proper_pay_host_daily_balance | closing_host_balance | Tabela |
| host_id | host_id | Coluna |
| date_ref | date_ref | Coluna |
| value | value | Coluna |

Um ponto de diferença entre as versões é que no fechamento V1 o saldo era calculado diariamente. Já no fechamento V2 ele é calculado mensalmente.

### Tabela de Receita da Propriedade: 

| **Elemento Fechamento V1** | **Elemento Fechamento V2** | **Tipo** | **Observação** |    |
|----|----|----|----|----|
| proper_pay_property_daily_revenue | closing_property_resume | Tabela | - |    |
| daily_net_value | value | Coluna | - |    |
| accrual_date | accrual_date | Coluna | - |    |
| cash_date | cash_date | Coluna | - |    |
| property_id | property_id | Coluna | - |    |
| listing_id | - | Coluna | Não há no novo fechamento |    |
| code | - | Coluna | Não há no novo fechamento |    |
| is_extension | - | Coluna | Não há no novo fechamento |    |
| - | transfer_category | Coluna | 'property_resume' |    |
| (sinal do campo value) | transfer_type | Coluna | * *input* indica valor positivo
* *output* indica valor negativo |    |

```bash
// Consulta às receitas de um imóvel no fechamento V1
select * from proper_pay_property_daily_revenue where property_id = XXXX;

// Consulta às receitas de um imóvel no fechamento V2
select * from closing_property_resume 
where property_id = XXXX and transfer_category = 'property_revenue';
```


\