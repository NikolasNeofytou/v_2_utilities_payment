# Utilities Payment SaaS Draft

This repository contains early drafts for a multi-tenant utilities payment platform.

For in-depth instructions, see the [User Guide](docs/user_guide.md) and [Developer Guide](docs/developer_guide.md).

## Contents
- `sql/schema.sql` – PostgreSQL schema for core entities.
- `utilities_payment/models.py` – Django models describing tenants, customers, bills and payments.
- `utilities_payment/webhooks.py` – Sample DRF view to handle payment gateway callbacks.
- `templates/email/pay_link_en.txt` – English email template for a one-click pay link.
- `templates/email/pay_link_el.txt` – Greek email template for a one-click pay link.
- `docs/pilot_checklist.md` – Checklist to prepare a pilot with a ΔΕΥΑ.

- `docs/user_guide.md` – How utility staff can import bills and view metrics.
- `docs/developer_guide.md` – Setup instructions and code overview for contributors.


## Bill Import API
`POST /tenants/<tenant_id>/bills/import`

Upload a CSV file via multipart form using the `file` field. Required columns:

`customer_id`, `meter_id`, `period_start`, `period_end`, `due_date`, `amount_due`.

Optional columns include `address`, `currency`, and `gateway`.

Example response:

```
{
  "created": 10,
  "errors": []
}
```


## Admin Metrics
`GET /tenants/<tenant_id>/metrics`

Returns aggregate bill statistics for a tenant:

```
{
  "total_bills": 25,
  "paid_bills": 20,
  "total_amount_due": "500.00",
  "paid_amount": "400.00",
  "outstanding_amount": "100.00"
}
```

## Customer Bills
`GET /customers/<customer_id>/bills`

Returns a list of bills for a given customer:

```
[
  {
    "id": 1,
    "service_point": "MTR123",
    "period_start": "2024-01-01",
    "period_end": "2024-01-31",
    "due_date": "2024-02-15",
    "amount_due": "50.00",
    "status": "pending"
  }
]
```


## Development
Run tests with:

```bash
pytest
```
