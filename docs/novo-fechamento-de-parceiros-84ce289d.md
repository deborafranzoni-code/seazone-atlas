<!-- title: Novo Fechamento de Parceiros | url: https://outline.seazone.com.br/doc/novo-fechamento-de-parceiros-qT3le1ozyI | area: Tecnologia -->

# Novo Fechamento de Parceiros

Este documento descreve a sequência de ações que devem ser realizadas para a realização do fluxo de fechamento financeiro de parceiros via plataforma Sapron.

# Fluxo para Fechamento Financeiro

Existem dois fluxos, de crédito e de débito, que deve seguir as seguintes dinâmicas:

## Fluxo de Crédito

Os créditos a serem associados a um parceiro para uma determinada reserva deve atender aos seguinte critérios:

* O parceiro precisa ter indicado o imóvel na qual a reserva foi realizada.
* A indicação do parceiro para o imóvel precisa estar dentro do prazo de validade (ou ser uma indicação de um parceiro premium, que não requer prazo de validade).

## Fluxo de Débito

Os débitos a serem associados a um parceiro são provenientes de um resgate efetuado via plataforma Sapron.


---

# Estrutura de Dados do Fechamento de Parceiro

A nova estrutura de dados para atender ao fechamento financeiro de parceiros da Seazone é formada pelas seguintes tabelas e seus respectivos impactos no fluxo de fechamento:

## Tabela *partners_indications_property*

Associa um imóvel a um parceiro, responsável pela sua indicação. As seguintes regras de negócio se aplicam:

* `status`: o status ==Won== indica que a indicação foi bem sucedida.
* `status_changed_date`: indica a data de início para valer o cálculo de comissão de um parceiro.
* `due_date`: indica a data de término/expiração do tempo de comissionamento de um parceiro para um imóvel. Seu valor sendo ==NULL== indica que o tempo é ilimitado, ou seja, sem data de expiração.
* `commission`: valor numérico que indica em percentual o valor de comissão a ser calculado para uma reserva no imóvel (ex: 0.02 indica 2% de comissão).

## Tabela *financial_partner_withdraw*

Registra o pagamento de um resgate de valor solicitado por um parceiro:

* `status`: o status ==Paid== indica que o pagamento foi realizado com sucesso.
* `date_paid`: indica a data em que o pagamento do resgate foi realizado pela Seazone.
* `partner_id`: ID do parceiro que recebeu tal pagamento.
* `value`: valor monetário pago ao parceiro.

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
  * (IN-OUT) partner_commission_fit: registro de um ajuste manual referente a uma comissão recebida pelo parceiro, que pode ser uma entrada ou saída.
  * (OUT) partner_payment: registro de um valor de saída referente à transferência de um valor ao parceiro por parte da Seazone.
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

# Trigger sobre a tabela *financial_partner_withdraw*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS partner_withdraw_changes
  ON financial_partner_withdraw;
 
CREATE TRIGGER partner_withdraw_changes
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
	new_partner_id INTEGER;
	old_partner_id INTEGER;

begin

	-- Comando para excluir os registros relacionados ao parceiro
	if (TG_OP = 'UPDATE') or (TG_OP = 'DELETE') then 		
    	old_partner_id := OLD.partner_id; 
	    raise notice '-------- Exclusão dos registros de repasse de partner -------------';
	    DELETE FROM closing_partner_resume where partner_id = old_partner_id and transfer_category in ('partner_payment') and source_table = 'financial_partner_withdraw' and source_id = OLD.id;
	    DELETE FROM closing_seazone_resume where transfer_category in ('partner_payment')  and source_table = 'financial_partner_withdraw' and source_id = OLD.id;
    end if;

	new_partner_id := NEW.partner_id;

	raise notice '-------- Inserção de registros de repasse de parceiro -------------';

	if new_partner_id is not null and NEW.status = 'Paid' then
	
		-- raise notice '-------- Registro de ajuste manual do HOST % -------------', NEW.id;
		INSERT INTO closing_partner_resume (reservation_id, property_id, partner_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.partner_id, NEW.date_paid, NEW.date_paid, NEW.value, 'output', 'partner_payment', CONCAT('Pagamento ao Parceiro referente ao resgate pago em: ', NEW.date_paid) , 'financial_partner_withdraw', NEW.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (null, null, NEW.date_paid, NEW.date_paid, NEW.value, 'input', 'partner_payment', CONCAT('Pagamento ao Parceiro ID ', NEW.partner_id, ' referente ao resgate de: ', NEW.date_paid), 'financial_partner_withdraw', NEW.id, now(), now());										
	 		
	end if;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *financial_reservation_manual_fit*

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
	property_transfer_type public.transfer_types;

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
	DELETE FROM closing_seazone_resume where reservation_id = old_res_id and transfer_category in ('reservation_manual_fit', 'commission_fit', 'seazone_commission_fit', 'partner_commission_fit') and source_table = 'financial_reservation_manual_fit';
	DELETE FROM closing_host_resume where reservation_id = old_res_id and transfer_category in ('commission_fit', 'host_commission_fit')  and source_table = 'financial_reservation_manual_fit';
	DELETE FROM closing_partner_resume where reservation_id = old_res_id and transfer_category in ('partner_commission_fit')  and source_table = 'financial_reservation_manual_fit';	

	res_id := NEW.reservation_id;
	
	raise notice '-------- Inserção de registros de ajuste manual de reserva -------------';

	open res_cursor(res_id);
 
	loop
		fetch res_cursor into res_record;
		exit when not found;
	
		if res_record.is_adding is true then	
			seazone_type := 'output';
			property_transfer_type := 'input';		
		else
			seazone_type := 'input';
			property_transfer_type := 'output';		
		end if; 
	
		-- raise notice '-------- Registro de ajuste manual de PROPERTY % -------------', NEW.id;		
		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value, property_transfer_type, 'reservation_manual_fit', res_record.description, 'financial_reservation_manual_fit', res_record.id, now(), now());										

		-- raise notice '-------- Registro de ajuste manual da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value, seazone_type, 'reservation_manual_fit', res_record.description, 'financial_reservation_manual_fit', res_record.id, now(), now());										
	
		-- raise notice '-------- Registro de estorno de comissao da SEAZONE % -------------', NEW.id;
		INSERT INTO closing_seazone_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.seazone_fee, property_transfer_type, 'seazone_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());										

		-- raise notice '-------- Registro de estorno de comissao da HOST % -------------', NEW.id;
		INSERT INTO closing_host_resume (reservation_id, property_id, host_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.host_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.host_fee, property_transfer_type, 'host_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());										

		-- raise notice '-------- Registro de estorno para PROPERTY de comissao paga ao HOST e SEAZONE % -------------', NEW.id;
		INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.host_fee, seazone_type, 'host_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());

    	INSERT INTO closing_property_resume (reservation_id, property_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id, created_at, updated_at) 
		VALUES (res_record.reservation_id, res_record.property_id, res_record.new_date_ref, res_record.cash_date, res_record.value * res_record.seazone_fee, seazone_type, 'seazone_commission_fit', CONCAT('Ajuste Comissão - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id, now(), now());

		-- raise notice '-------- Registro de ajuste de comissao paga ao PARTNER % -------------', NEW.id;
		insert into closing_partner_resume (created_at, updated_at, partner_id, property_id, reservation_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id)
			select now(), now(), p.partner_id, r.property_id, r.id, res_record.new_date_ref, res_record.cash_date, (res_record.value * p.commission), property_transfer_type, 'partner_commission_fit', CONCAT('Ajuste de Comissao de Parceiro = ', p.commission, ' - reserva ', res_record.code)_, 'financial_reservation_manual_fit', res_record.id
			from reservation_reservation r
			join partners_indications_property p on p.property_id = r.property_id and p.status = 'Won'
			where r.id = res_record.reservation_id and (p.due_date is null or res_record.new_date_ref <= p.due_date);

		-- raise notice '-------- Registro de estorno da ccomissao da SEAZONE % -------------', NEW.id;
		insert into closing_seazone_resume (created_at, updated_at, property_id, reservation_id, accrual_date, cash_date, value, transfer_type, transfer_category, description, source_table, source_id)
			select now(), now(), r.property_id, r.id, res_record.new_date_ref, res_record.cash_date, (res_record.value * p.commission), seazone_type, 'partner_commission', CONCAT('Ajuste de Comissao de Parceiro = ', p.commission, ' - reserva ', res_record.code), 'financial_reservation_manual_fit', res_record.id
			from reservation_reservation r
			join partners_indications_property p on p.property_id = r.property_id and p.status = 'Won'
			where r.id = res_record.reservation_id and (p.due_date is null or res_record.new_date_ref <= p.due_date);
	
	end loop;
	
	close res_cursor;
	
	raise notice '-------- Fim de Execução -------------';
	
	RETURN new;
  
END;
$function$
;
```

# Trigger sobre a tabela *closing_partner_resume*

### Código da Trigger

```sql
DROP TRIGGER IF EXISTS closing_partner_resume_changes
  ON closing_partner_resume;
 
CREATE TRIGGER closing_partner_resume_changes
  AFTER INSERT or UPDATE or DELETE
  ON closing_partner_resume
  FOR EACH ROW
  EXECUTE PROCEDURE register_partner_balance();
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