CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE IF NOT EXISTS lab.orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    order_timestamp TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    item_count INTEGER NOT NULL,
    subtotal NUMERIC(12, 2) NOT NULL,
    shipping_fee NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    shipping_region VARCHAR(40) NOT NULL,
    shipping_method VARCHAR(20) NOT NULL,
    CONSTRAINT ck_orders_item_count_positive CHECK (item_count > 0),
    CONSTRAINT ck_orders_amounts_non_negative CHECK (subtotal >= 0 AND shipping_fee >= 0 AND total_amount >= 0),
    CONSTRAINT ck_orders_total_matches CHECK (total_amount = subtotal + shipping_fee)
);