-- Simplified database schema for utilities payment platform

CREATE TABLE tenant (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255)
);

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenant(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(30)
);

CREATE TABLE service_point (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenant(id) ON DELETE CASCADE,

    customer_id INTEGER REFERENCES customer(id) ON DELETE CASCADE,

    meter_id VARCHAR(100) NOT NULL,
    address VARCHAR(255)
);

CREATE TABLE bill (
    id SERIAL PRIMARY KEY,
    service_point_id INTEGER REFERENCES service_point(id) ON DELETE CASCADE,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    due_date DATE NOT NULL,
    amount_due NUMERIC(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'EUR',
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE bill_line (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bill(id) ON DELETE CASCADE,
    line_type VARCHAR(50) NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    total NUMERIC(10,2) NOT NULL
);

CREATE TABLE payment_intent (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bill(id) ON DELETE CASCADE,
    gateway VARCHAR(50) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    pay_link_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP
);

CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    intent_id INTEGER REFERENCES payment_intent(id) ON DELETE CASCADE,
    gateway_charge_id VARCHAR(255) NOT NULL,
    captured_at TIMESTAMP NOT NULL,
    method VARCHAR(20) NOT NULL,
    fee NUMERIC(10,2) NOT NULL,
    net NUMERIC(10,2) NOT NULL
);

CREATE TABLE notification (
    id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bill(id) ON DELETE CASCADE,
    channel VARCHAR(20) NOT NULL,
    template_id VARCHAR(100) NOT NULL,
    sent_at TIMESTAMP DEFAULT NOW(),
    delivery_status VARCHAR(20) DEFAULT 'pending',
    opened_at TIMESTAMP,
    clicked_at TIMESTAMP
);

CREATE TABLE reconciliation_entry (
    id SERIAL PRIMARY KEY,
    payout_id VARCHAR(255) NOT NULL,
    amount_gross NUMERIC(10,2) NOT NULL,
    amount_net NUMERIC(10,2) NOT NULL,
    fees NUMERIC(10,2) NOT NULL,
    date DATE NOT NULL,
    matched BOOLEAN DEFAULT FALSE
);
