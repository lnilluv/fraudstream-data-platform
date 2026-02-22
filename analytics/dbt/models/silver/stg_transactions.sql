with source_transactions as (
    select *
    from {{ source('bronze', 'transactions_raw') }}
),
normalized as (
    select
        cast(trans_num as varchar) as trans_num,
        cast(unix_time as bigint) as event_unix_time,
        cast(cc_num as varchar) as cc_num,
        cast(merchant as varchar) as merchant,
        cast(category as varchar) as category,
        cast(amt as double) as amount,
        cast(is_fraud as integer) as is_fraud,
        cast(city as varchar) as city,
        cast(state as varchar) as state
    from source_transactions
)
select *
from normalized
