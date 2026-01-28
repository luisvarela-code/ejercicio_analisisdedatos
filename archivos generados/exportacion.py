import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE SEMILLA PARA REPRODUCIBILIDAD ---
np.random.seed(99)
random.seed(99)

# --- PARÁMETROS ---
n_customers = 2000
n_transactions = 25000

print("Generando datos simulados de TechSupply Retail Group...")

# 1. GENERACIÓN DE DIMENSIÓN CLIENTE (dim_customers)
customer_ids = [f'CUST_{i:04d}' for i in range(n_customers)]
regions = ['North_America', 'EMEA', 'APAC', 'LATAM']
channels = ['Direct Sales', 'Distributor', 'Online Web']

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'region': np.random.choice(regions, n_customers, p=[0.4, 0.3, 0.2, 0.1]),
    'acquisition_channel': np.random.choice(channels, n_customers),
    'signup_date': [datetime(2022, 1, 1) + timedelta(days=random.randint(0, 730)) for _ in range(n_customers)]
})

# 2. GENERACIÓN DE HECHOS TRANSACCIONALES (fact_sales)
products = {
    'Enterprise Server': 4500, 'Gaming Laptop': 1500, 'Mechanical Keyboard': 120, 
    'USB-C Dock': 180, 'Monitor 27in': 350, 'Ethernet Cable': 25
}

data = []
for _ in range(n_transactions):
    cust_id = np.random.choice(customer_ids)
    # Fecha de transacción posterior al registro del cliente
    cust_signup = df_customers.loc[df_customers['customer_id'] == cust_id, 'signup_date'].values[0]
    cust_signup_ts = pd.to_datetime(str(cust_signup))
    
    txn_date = cust_signup_ts + timedelta(days=random.randint(0, 365))
    
    # Selección de producto
    prod_name = np.random.choice(list(products.keys()))
    base_price = products[prod_name]
    qty = np.random.choice([1, 2, 3, 5, 10, 20], p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
    
    # Cálculo de monto (con posibilidad de descuento aleatorio o devolución)
    final_amount = base_price * qty
    
    # 3% de probabilidad de devolución (monto negativo)
    status = 'Completed'
    if random.random() < 0.03:
        final_amount = final_amount * -1
        status = 'Returned'
        
    data.append([cust_id, txn_date, prod_name, qty, final_amount, status])

df_sales = pd.DataFrame(data, columns=['customer_id', 'transaction_date', 'product_name', 'quantity', 'total_amount', 'status'])

# Guardar archivos
df_customers.to_csv('dim_customers.csv', index=False)
df_sales.to_csv('fact_sales.csv', index=False)

print("✅ ÉXITO: Archivos 'dim_customers.csv' y 'fact_sales.csv' creados en el directorio actual.")