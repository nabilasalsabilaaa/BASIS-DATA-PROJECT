CREATE KEYSPACE IF NOT EXISTS ecommerce_store 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE ecommerce_store;

CREATE TABLE IF NOT EXISTS orders_by_user (
    user_id text,
    order_date timestamp,
    order_id text,
    product_name text,
    price double,
    PRIMARY KEY (user_id, order_date)
) WITH CLUSTERING ORDER BY (order_date DESC);

CREATE TABLE IF NOT EXISTS purchases_by_product (
    product_name text,
    order_date timestamp,
    user_id text,
    order_id text,
    PRIMARY KEY (product_name, order_date)
) WITH CLUSTERING ORDER BY (order_date ASC);