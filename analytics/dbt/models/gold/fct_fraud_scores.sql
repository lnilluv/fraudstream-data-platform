select
    trans_num,
    cc_num,
    merchant,
    category,
    amount,
    city,
    state,
    event_unix_time,
    case when is_fraud = 0 then true else false end as flagged_fraud
from {{ ref('stg_transactions') }}
