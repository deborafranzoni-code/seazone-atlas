<!-- title: Extração da base de hospede | url: https://outline.seazone.com.br/doc/extracao-da-base-de-hospede-91eTka7LDb | area: Tecnologia -->

# Extração da base de hospede

O video de execução no Nekt

[video_execução_queries_nekt.mp4 1910x1022](/api/attachments.redirect?id=d5d43488-7537-418f-ac4e-01cc8c61a4cb)


\[QUERY - GUESTS CHECKOUT 7 DAY - GOIANIA\]

```sql
WITH guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email
    FROM "nekt_silver"."sapron_guests_szs_contacts" AS g
),

reservations AS (
    SELECT
        guest_id,
        code AS last_property_code,
        check_out_date,
        city,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY guest_id
            ORDER BY check_out_date DESC
        ) AS rn
    FROM "nekt_silver"."sapron_dim_guests_szs_reservations"
    -- AND (check_in_date BETWEEN DATE '2025-01-01' AND DATE '2025-12-31')
),

szs_guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        r.check_out_date
    FROM guests g
    INNER JOIN reservations r 
        ON g.id = r.guest_id
    WHERE r.rn = 1
      AND r.check_out_date = CURRENT_DATE - INTERVAL '7' DAY
      AND r.status = 'Concluded'
      AND r.city = 'Goiânia'
),

szs_elegible_guests AS (
    SELECT g.*
    FROM szs_guests g
    WHERE NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" b
        WHERE b.email = g.email
    )
    AND NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" c
        WHERE c.phone = g.phone
    )
),

triggers AS (
    SELECT
        phone,
        CAST(expected_date_time AS TIMESTAMP(0)) AS expected_date_time,
        CAST(executed_date_time AS TIMESTAMP(0)) AS executed_date_time,
        type
    FROM "nekt_service"."google_sheets_teste_disparo_disparo"
),

triggers_treated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN executed_date_time IS NULL THEN expected_date_time
            ELSE executed_date_time
        END AS consolidated_date_time
    FROM triggers
),

triggers_consolidated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN type = 'whatsapp' 
                THEN consolidated_date_time + INTERVAL '3' DAY
            ELSE consolidated_date_time + INTERVAL '1' DAY
        END AS contact_notified_at
    FROM triggers_treated
),

dim_trigger AS (
    SELECT
        phone,
        CAST(MAX(contact_notified_at) AS DATE) AS contact_notified_at
    FROM triggers_consolidated
    WHERE type = 'whatsapp'
    GROUP BY phone
),

final_table AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        CASE
            WHEN d.contact_notified_at IS NULL THEN CURRENT_DATE
            WHEN d.contact_notified_at <= CURRENT_DATE THEN CURRENT_DATE
            ELSE d.contact_notified_at
        END AS contact_eligible_at
    FROM szs_elegible_guests g
    LEFT JOIN dim_trigger d 
        ON g.phone = d.phone
)

SELECT *
FROM final_table
WHERE contact_eligible_at <= CURRENT_DATE;
```


\[QUERY - GUESTS CHECKOUT 7 DAY - ESTADO GO - EXCETO GOIÂNIA\]


\
```sql
WITH guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email
    FROM "nekt_silver"."sapron_guests_szs_contacts" g
),

reservations AS (
    SELECT
        guest_id,
        code AS last_property_code,
        check_out_date,
        city,
        state,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY guest_id
            ORDER BY check_out_date DESC
        ) AS rn
    FROM "nekt_silver"."sapron_dim_guests_szs_reservations"
),

szs_guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        r.check_out_date
    FROM guests g
    INNER JOIN reservations r
        ON g.id = r.guest_id
    WHERE r.rn = 1
      AND r.check_out_date = current_date - INTERVAL '7' DAY
      AND r.status = 'Concluded'
      AND r.city <> 'Goiânia'
      AND r.state = 'GO'
),

szs_elegible_guests AS (
    SELECT g.*
    FROM szs_guests g
    WHERE NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" b
        WHERE b.email = g.email
    )
    AND NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" c
        WHERE c.phone = g.phone
    )
),

triggers AS (
    SELECT
        phone,
        CAST(expected_date_time AS TIMESTAMP) AS expected_date_time,
        CAST(executed_date_time AS TIMESTAMP) AS executed_date_time,
        type
    FROM "nekt_service"."google_sheets_teste_disparo_disparo"
),

triggers_treated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN executed_date_time IS NULL THEN expected_date_time
            ELSE executed_date_time
        END AS consolidated_date_time
    FROM triggers
),

triggers_consolidated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN type = 'whatsapp'
                THEN consolidated_date_time + INTERVAL '3' DAY
            ELSE consolidated_date_time + INTERVAL '1' DAY
        END AS contact_notified_at
    FROM triggers_treated
),

dim_trigger AS (
    SELECT
        phone,
        CAST(MAX(contact_notified_at) AS DATE) AS contact_notified_at
    FROM triggers_consolidated
    WHERE type = 'whatsapp'
    GROUP BY phone
),

final_table AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        CASE
            WHEN d.contact_notified_at IS NULL THEN current_date
            WHEN d.contact_notified_at <= current_date THEN current_date
            ELSE d.contact_notified_at
        END AS contact_eligible_at
    FROM szs_elegible_guests g
    LEFT JOIN dim_trigger d
        ON g.phone = d.phone
)

SELECT *
FROM final_table
WHERE contact_eligible_at <= current_date;
```


\[QUERY - GUESTS CHECKOUT 7 DAY - ESTADO SP\]


```sql
WITH
  guests AS (
    SELECT
      g.id,
      g.name,
      g.phone,
      g.email
    FROM
      "nekt_silver"."sapron_guests_szs_contacts" AS g
  ),
  reservations AS (
    SELECT
      guest_id,
      code AS last_property_code,
      check_out_date,
      city,
      state,
      status,
      ROW_NUMBER() OVER (
        PARTITION BY
          guest_id
        ORDER BY
          check_out_date DESC
      ) AS rn
    FROM
      "nekt_silver"."sapron_dim_guests_szs_reservations"
      -- FILTRE A CIDADE E DATA DO CHECK OUT E CHECK IN AQUI E O STATUS DA RESERVA
      --AND (check_in_date BETWEEN DATE('2025-01-01') AND DATE('2025-12-31'))
  ),
  szs_guests AS (
    SELECT
      g.id,
      g.name,
      g.phone,
      g.email,
      r.check_out_date
    FROM
      guests AS g
      INNER JOIN reservations AS r ON g.id = r.guest_id
    WHERE
      r.rn = 1
      AND r.check_out_date = CURRENT_DATE - INTERVAL '7' DAY
      AND r.status = 'Concluded'
      AND r.state = 'SP'
  ),
  szs_elegible_guests AS (
    SELECT
      g.*
    FROM
      szs_guests AS g
    WHERE
      NOT EXISTS (
        SELECT
          1
        FROM
          "nekt_silver"."blocked_contacts" AS b
        WHERE
          b.email = g.email
      )
      AND NOT EXISTS (
        SELECT
          1
        FROM
          "nekt_silver"."blocked_contacts" AS c
        WHERE
          c.phone = g.phone
      )
  ),
  triggers AS (
    SELECT
      phone,
      CAST(expected_date_time AS TIMESTAMP(0)) AS expected_date_time,
      CAST(executed_date_time AS TIMESTAMP(0)) AS executed_date_time,
      type
    FROM
      "nekt_service"."google_sheets_teste_disparo_disparo"
  ),
  triggers_treated AS (
    SELECT
      phone,
      type,
      CASE
        WHEN executed_date_time IS NULL THEN expected_date_time
        ELSE executed_date_time
      END AS consolidated_date_time
    FROM
      triggers
  ),
  triggers_consolidated AS (
    SELECT
      phone,
      type,
      CASE
        WHEN type = 'whatsapp' THEN consolidated_date_time + INTERVAL '3' DAY
        ELSE consolidated_date_time + INTERVAL '1' DAY
      END AS contact_notified_at
    FROM
      triggers_treated
  ),
  dim_trigger AS (
    SELECT
      phone,
      CAST((MAX(contact_notified_at)) AS DATE) AS contact_notified_at
    FROM
      triggers_consolidated
    WHERE
      type = 'whatsapp'
    GROUP BY
      1
  ),
  final_table AS (
    SELECT
      g.id,
      g.name,
      g.phone,
      g.email,
      CASE
        WHEN d.contact_notified_at IS NULL THEN CURRENT_DATE
        WHEN d.contact_notified_at <= CURRENT_DATE THEN CURRENT_DATE
        ELSE d.contact_notified_at
      END AS contact_eligible_at
    FROM
      szs_elegible_guests AS g
      LEFT JOIN dim_trigger AS d ON g.phone = d.phone
      --FILTRE O TIPO DA CAMPANHA (EMAIL OU WHATSAPP) AQUI 
  )
SELECT
  *
FROM
  final_table
WHERE
  contact_eligible_at <= CURRENT_DATE
```


\
\[QUERY - GUESTS CHECKOUT 7 DAY - ANITÁPOLIS - VST\]


```sql
WITH guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email
    FROM "nekt_silver"."sapron_guests_szs_contacts" AS g
),

reservations AS (
    SELECT
        guest_id,
        code AS last_property_code,
        check_out_date,
        city,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY guest_id
            ORDER BY check_out_date DESC
        ) AS rn
    FROM "nekt_silver"."sapron_dim_guests_szs_reservations"
),

szs_guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        r.check_out_date
    FROM guests AS g
    INNER JOIN reservations AS r 
        ON g.id = r.guest_id
    WHERE r.rn = 1
      AND r.check_out_date = CURRENT_DATE - INTERVAL '7' DAY
      AND r.status = 'Concluded'
      AND r.city = 'Anitápolis'
      AND r.last_property_code LIKE 'VST%'
),

szs_elegible_guests AS (
    SELECT g.*
    FROM szs_guests AS g
    WHERE NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" AS b
        WHERE b.email = g.email
    )
    AND NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" AS c
        WHERE c.phone = g.phone
    )
),

triggers AS (
    SELECT
        phone,
        CAST(expected_date_time AS TIMESTAMP) AS expected_date_time,
        CAST(executed_date_time AS TIMESTAMP) AS executed_date_time,
        type
    FROM "nekt_service"."google_sheets_teste_disparo_disparo"
),

triggers_treated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN executed_date_time IS NULL THEN expected_date_time
            ELSE executed_date_time
        END AS consolidated_date_time
    FROM triggers
),

triggers_consolidated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN type = 'whatsapp' 
                THEN consolidated_date_time + INTERVAL '3' DAY
            ELSE consolidated_date_time + INTERVAL '1' DAY
        END AS contact_notified_at
    FROM triggers_treated
),

dim_trigger AS (
    SELECT
        phone,
        CAST(MAX(contact_notified_at) AS DATE) AS contact_notified_at
    FROM triggers_consolidated
    WHERE type = 'whatsapp'
    GROUP BY phone
),

final_table AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        CASE
            WHEN d.contact_notified_at IS NULL THEN CURRENT_DATE
            WHEN d.contact_notified_at <= CURRENT_DATE THEN CURRENT_DATE
            ELSE d.contact_notified_at
        END AS contact_eligible_at
    FROM szs_elegible_guests AS g
    LEFT JOIN dim_trigger AS d 
        ON g.phone = d.phone
)

SELECT *
FROM final_table
WHERE contact_eligible_at <= CURRENT_DATE;
```


\[QUERY - GUESTS CHECKOUT 7 DAY - ESTADO BA\]


```sql
WITH guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email
    FROM "nekt_silver"."sapron_guests_szs_contacts" g
),

reservations AS (
    SELECT
        guest_id,
        code AS last_property_code,
        check_out_date,
        state,
        city,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY guest_id
            ORDER BY check_out_date DESC
        ) AS rn
    FROM "nekt_silver"."sapron_dim_guests_szs_reservations"
),

szs_guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        r.check_out_date
    FROM guests g
    INNER JOIN reservations r 
        ON g.id = r.guest_id
    WHERE r.rn = 1
      AND r.check_out_date = current_date - INTERVAL '7' DAY
      AND r.status = 'Concluded'
      AND r.state = 'BA'
),

szs_elegible_guests AS (
    SELECT g.*
    FROM szs_guests g
    WHERE NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" b
        WHERE b.email = g.email
    )
    AND NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" c
        WHERE c.phone = g.phone
    )
),

triggers AS (
    SELECT
        phone,
        CAST(expected_date_time AS TIMESTAMP) AS expected_date_time,
        CAST(executed_date_time AS TIMESTAMP) AS executed_date_time,
        type
    FROM "nekt_service"."google_sheets_teste_disparo_disparo"
),

triggers_treated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN executed_date_time IS NULL THEN expected_date_time
            ELSE executed_date_time
        END AS consolidated_date_time
    FROM triggers
),

triggers_consolidated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN type = 'whatsapp' 
                THEN consolidated_date_time + INTERVAL '3' DAY
            ELSE consolidated_date_time + INTERVAL '1' DAY
        END AS contact_notified_at
    FROM triggers_treated
),

dim_trigger AS (
    SELECT
        phone,
        CAST(MAX(contact_notified_at) AS DATE) AS contact_notified_at
    FROM triggers_consolidated
    WHERE type = 'whatsapp'
    GROUP BY phone
),

final_table AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        CASE
            WHEN d.contact_notified_at IS NULL THEN current_date
            WHEN d.contact_notified_at <= current_date THEN current_date
            ELSE d.contact_notified_at
        END AS contact_eligible_at
    FROM szs_elegible_guests g
    LEFT JOIN dim_trigger d 
        ON g.phone = d.phone
)

SELECT *
FROM final_table
WHERE contact_eligible_at <= current_date;
```


\
\[QUERY GUESTS CHECKOUT 7 DAY\]\[FLORIANOPOLIS\]\[EXCETO ALGUNS IMOVEIS\]


```sql
WITH guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email
    FROM "nekt_silver"."sapron_guests_szs_contacts" AS g
),

reservations AS (
    SELECT
        guest_id,
        code AS last_property_code,
        check_out_date,
        state,
        city,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY guest_id
            ORDER BY check_out_date DESC
        ) AS rn
    FROM "nekt_silver"."sapron_dim_guests_szs_reservations"
),

szs_guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        r.check_out_date
    FROM guests g
    INNER JOIN reservations r 
        ON g.id = r.guest_id
    WHERE r.rn = 1
        AND r.check_out_date = current_date - INTERVAL '7' day
        AND r.status = 'Concluded'
        AND r.city = 'Florianópolis'
        AND r.last_property_code NOT LIKE 'SPJ%'
        AND r.last_property_code NOT LIKE 'DJB%'
        AND r.last_property_code NOT LIKE 'RCA%'
        AND r.last_property_code NOT LIKE 'ILC%'
        AND r.last_property_code NOT LIKE 'RDT%'
),

szs_elegible_guests AS (
    SELECT g.*
    FROM szs_guests g
    WHERE NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" b
        WHERE b.email = g.email
    )
    AND NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" c
        WHERE c.phone = g.phone
    )
),

triggers AS (
    SELECT
        phone,
        CAST(expected_date_time AS timestamp) AS expected_date_time,
        CAST(executed_date_time AS timestamp) AS executed_date_time,
        type
    FROM "nekt_service"."google_sheets_teste_disparo_disparo"
),

triggers_treated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN executed_date_time IS NULL THEN expected_date_time
            ELSE executed_date_time
        END AS consolidated_date_time
    FROM triggers
),

triggers_consolidated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN type = 'whatsapp' THEN consolidated_date_time + INTERVAL '3' day
            ELSE consolidated_date_time + INTERVAL '1' day
        END AS contact_notified_at
    FROM triggers_treated
),

dim_trigger AS (
    SELECT
        phone,
        CAST(MAX(contact_notified_at) AS date) AS contact_notified_at
    FROM triggers_consolidated
    WHERE type = 'whatsapp'
    GROUP BY phone
),

final_table AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        CASE
            WHEN d.contact_notified_at IS NULL THEN current_date
            WHEN d.contact_notified_at <= current_date THEN current_date
            ELSE d.contact_notified_at
        END AS contact_eligible_at
    FROM szs_elegible_guests g
    LEFT JOIN dim_trigger d 
        ON g.phone = d.phone
)

SELECT *
FROM final_table
WHERE contact_eligible_at <= current_date;
```


\
\[QUERY GUESTS CHECKOUT 7 DAY\]\[IMOVEIS ESPECIFICOS POR CODIGO\]


\
```sql
WITH guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email
    FROM "nekt_silver"."sapron_guests_szs_contacts" g
),

reservations AS (
    SELECT
        guest_id,
        code AS last_property_code,
        check_out_date,
        state,
        city,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY guest_id
            ORDER BY check_out_date DESC
        ) AS rn
    FROM "nekt_silver"."sapron_dim_guests_szs_reservations"
),

szs_guests AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        r.check_out_date
    FROM guests g
    INNER JOIN reservations r 
        ON g.id = r.guest_id
    WHERE r.rn = 1
      AND r.check_out_date = DATE_ADD('day', -7, CURRENT_DATE)
      AND r.status = 'Concluded'
      AND (
            r.last_property_code LIKE 'SPJ%' OR
            r.last_property_code LIKE 'DJB%' OR
            r.last_property_code LIKE 'RCA%' OR
            r.last_property_code LIKE 'ILC%' OR
            r.last_property_code LIKE 'RDT%'
      )
),

szs_elegible_guests AS (
    SELECT g.*
    FROM szs_guests g
    WHERE NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" b
        WHERE b.email = g.email
    )
    AND NOT EXISTS (
        SELECT 1
        FROM "nekt_silver"."blocked_contacts" c
        WHERE c.phone = g.phone
    )
),

triggers AS (
    SELECT
        phone,
        CAST(expected_date_time AS TIMESTAMP) AS expected_date_time,
        CAST(executed_date_time AS TIMESTAMP) AS executed_date_time,
        type
    FROM "nekt_service"."google_sheets_teste_disparo_disparo"
),

triggers_treated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN executed_date_time IS NULL 
                THEN expected_date_time
            ELSE executed_date_time
        END AS consolidated_date_time
    FROM triggers
),

triggers_consolidated AS (
    SELECT
        phone,
        type,
        CASE
            WHEN type = 'whatsapp' 
                THEN DATE_ADD('day', 3, consolidated_date_time)
            ELSE DATE_ADD('day', 1, consolidated_date_time)
        END AS contact_notified_at
    FROM triggers_treated
),

dim_trigger AS (
    SELECT
        phone,
        CAST(MAX(contact_notified_at) AS DATE) AS contact_notified_at
    FROM triggers_consolidated
    WHERE type = 'whatsapp'
    GROUP BY phone
),

final_table AS (
    SELECT
        g.id,
        g.name,
        g.phone,
        g.email,
        CASE
            WHEN d.contact_notified_at IS NULL THEN CURRENT_DATE
            WHEN d.contact_notified_at <= CURRENT_DATE THEN CURRENT_DATE
            ELSE d.contact_notified_at
        END AS contact_eligible_at
    FROM szs_elegible_guests g
    LEFT JOIN dim_trigger d 
        ON g.phone = d.phone
)

SELECT *
FROM final_table
WHERE contact_eligible_at <= CURRENT_DATE;
```