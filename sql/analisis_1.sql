create database customer_clientes-,
use customers_clientes;

create table stg_clientes(
 customer_id NVARCHAR(50),
 region NVARCHAR(50),
 acquisition_channel NVARCHAR(50),
 signup_date DATE
);

BULK INSERT stg_clientes
FROM 'C:\Users\HP Pavilion\Desktop\tablas\dim_customers.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '0x0d0a',
    CODEPAGE = '65001',
    TABLOCK
);

select * from dim_customers;
select * from ventas;

CREATE VIEW vw_ventas_clientes AS
SELECT
    v.customer_id,
    v.transaction_date,
    v.product_name,
    v.quantity,
    v.total_amount,
    v.status,
    c.region,
    c.acquisition_channel,
    c.signup_date
FROM ventas v
INNER JOIN dim_customers c
    ON v.customer_id = c.customer_id;

select* from  vw_ventas_clientes;