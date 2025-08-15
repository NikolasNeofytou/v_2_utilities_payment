# Utilities Payment SaaS Draft

This repository contains early drafts for a multi-tenant utilities payment platform.

## Contents
- `sql/schema.sql` – PostgreSQL schema for core entities.
- `utilities_payment/models.py` – Django models describing tenants, customers, bills and payments.
- `utilities_payment/webhooks.py` – Sample DRF view to handle payment gateway callbacks.
- `templates/email/pay_link_en.txt` – English email template for a one-click pay link.
- `templates/email/pay_link_el.txt` – Greek email template for a one-click pay link.
- `docs/pilot_checklist.md` – Checklist to prepare a pilot with a ΔΕΥΑ.

## Development
Run tests with:

```bash
pytest
```
