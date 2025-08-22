# Developer Guide

This document helps new contributors understand the Utilities Payment project and get a local environment running.

## Setup
1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Run tests to verify the setup:
```bash
pytest
```

## Code Layout
- `utilities_payment/models.py` – Django models for tenants, customers, service points, bills, and payments.
- `utilities_payment/views.py` – DRF views including bill import, tenant metrics, and customer bills.
- `utilities_payment/webhooks.py` – Example webhook handler for payment gateway callbacks.
- `templates/email/` – Plain-text email templates for pay links in English and Greek.
- `sql/schema.sql` – SQL script with the relational schema.
- `docs/` – Project documentation and checklists.

## API Endpoints
The project currently exposes the following APIs:
- `POST /tenants/<tenant_id>/bills/import` – Import bills from a CSV file.
- `GET /tenants/<tenant_id>/metrics` – Retrieve aggregate bill statistics.
- `GET /customers/<customer_id>/bills` – List bills associated with a customer.

## Webhooks
`POST /webhooks/payments/gateway-x` validates incoming events from the payment gateway and updates payment status accordingly. Ensure idempotency by using the gateway event ID.

## Next Steps
The project is a prototype. Future work may include a full customer portal, notification system, and advanced analytics.

