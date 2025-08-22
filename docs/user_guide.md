# User Guide

Welcome to the Utilities Payment platform. This guide explains how utility staff can upload bills, monitor collections, and view customer information.

## Importing Bills
1. Create a CSV file with the required columns:
   - `customer_id`
   - `meter_id`
   - `period_start`
   - `period_end`
   - `due_date`
   - `amount_due`
2. Send a `POST /tenants/<tenant_id>/bills/import` request with the CSV in the `file` field of a multipart form.
3. The response reports how many bills were created and any row‑level errors.

Example using `curl`:
```bash
curl -F "file=@bills.csv" http://localhost:8000/tenants/1/bills/import
```

## Viewing Metrics
Use `GET /tenants/<tenant_id>/metrics` to retrieve aggregate bill counts and outstanding balances.

Example response:
```json
{
  "total_bills": 25,
  "paid_bills": 20,
  "total_amount_due": "500.00",
  "paid_amount": "400.00",
  "outstanding_amount": "100.00"
}
```

## Checking Customer Bills
`GET /customers/<customer_id>/bills` returns every bill for a given customer.

Example response:
```json
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

## Pay‑Link Emails
The platform can send customers a one‑time pay link by email. Templates are located in `templates/email/` in both English and Greek. When a customer clicks the link, they are taken directly to a hosted checkout to pay the bill.

