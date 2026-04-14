<!-- title: Sanetização da base de hospedes | url: https://outline.seazone.com.br/doc/sanetizacao-da-base-de-hospedes-UXTm1chCqv | area: Tecnologia -->

# Sanetização da base de hospedes

🔎 **FASE 1 — AUDITORIA COMPLETA**

***O  relatório  completo será restrito para as pessoas envolvidas no projeto devido aos dados sensíveis*.** 


Objetivo:

* Ver qual telefone está duplicado
* Quantas vezes ele aparece
* Quais usuários compartilham
* Se é phone1 ou phone2
* CPF/CNPJ para avaliar conflito real


🚨 Analisar tamanho das tabelas account_user e account_guess


`SELECT schemaname, relname AS tabela, n_live_tup AS registros_estimados, pg_size_pretty(pg_total_relation_size(relid)) AS tamanho_total, pg_size_pretty(pg_relation_size(relid)) AS tamanho_dados, pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS tamanho_indices`

`FROM pg_stat_user_tables`

`ORDER BY pg_total_relation_size(relid) DESC;`


[https://docs.google.com/spreadsheets/d/1GkH7Yi-GFTDMBhVRPopbWMpY6zPSo2tt7MM43JPGaS8/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1GkH7Yi-GFTDMBhVRPopbWMpY6zPSo2tt7MM43JPGaS8/edit?usp=sharing)


✅ 1️⃣ Relatório detalhado de duplicidade 

## 🎯 query deve monstrar 

Para cada telefone duplicado:

* 📞 O número
* 🔢 Quantas vezes ele aparece
* 👤 Quem são os usuários
* 🧾 CPF/CNPJ
* 📌 Se está em phone_number1 ou phone_number2


**- Queries do relatório completo:**  **28484 rows duplicados.** 

[Planilha completo](https://docs.google.com/spreadsheets/d/1-FdIytIXJDf7Fh6uLp_Gvcv-e_2GVHEqG-cm6Q6xCZA/edit?usp=sharing) (Acesso restrito)


```sql
WITH phones AS ( SELECT u.id, u.first_name, u.last_name, u.email, u.cpf, u.cnpj,
regexp_replace(u.phone_number1, '\D', '', 'g') 
AS phone FROM public.account_user u WHERE u.phone_number1 IS NOT NULL

UNION ALL

SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email,
    u.cpf,
    u.cnpj,
    regexp_replace(u.phone_number2, '\D', '', 'g') AS phone
FROM public.account_user u
WHERE u.phone_number2 IS NOT NULL
)

SELECT phone, COUNT(\*) AS total_ocorrencias, COUNT(DISTINCT id) AS total_usuarios,
-- Lista IDs
STRING_AGG(DISTINCT id::text, ', ') AS usuarios_ids,

-- Lista nomes
STRING_AGG(DISTINCT first_name || ' ' || last_name, ' | ') AS nomes,

-- Lista CPFs
STRING_AGG(DISTINCT cpf, ', ') AS cpfs,

-- Lista CNPJs
STRING_AGG(DISTINCT cnpj, ', ') AS cnpjs
FROM phones WHERE phone <> '' 
GROUP BY phone HAVING COUNT(*) > 1 
ORDER BY total_ocorrencias 
DESC LIMIT 20;  -- para teste
```


\
🔎 **FASE 2 — PLANO DE SANETIZAÇÃO**


Monstrar exatamente quem será considerado "duplicado" e removido.


```sql

WITH phones AS ( SELECT id, created_at, regexp_replace(phone_number1, '\\D', '', 'g') 
AS phone FROM public.account_user WHERE phone_number1 IS NOT NULL
UNION ALL

SELECT id, created_at,
       regexp_replace(phone_number2, '\D', '', 'g') AS phone
FROM public.account_user
WHERE phone_number2 IS NOT NULL
),

ranked AS ( SELECT \*, ROW_NUMBER() OVER ( PARTITION BY phone ORDER BY created_at ASC ) 
AS rn FROM phones WHERE phone <> '' )

SELECT \* FROM ranked WHERE rn > 1 ORDER BY phone, created_at;
```


💾 BACKUP OBRIGATÓRIO


```sql
CREATE TABLE backup_account_user_duplicados AS SELECT * FROM public.account_user
 WHERE id IN ( -- cole aqui os ids da query anterior (rn > 1) );
 
 CREATE INDEX ON backup_account_user_duplicados(id);
```

` `