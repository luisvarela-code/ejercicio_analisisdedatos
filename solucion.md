# Pasos a resoolver el ejercicio
### primer paso
una vez que se ejecuto el codico
```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuración
np.random.seed(42)
n_customers = 1000
n_transactions = 15000

print("⚙️ Iniciando generación de datos para OmniLogistics S.A...")

# 1. Generar Clientes (Dimensión)
customer_ids = [f'CUST_{i:04d}' for i in range(n_customers)]
regions = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
segments = ['Corporativo', 'Consumidor', 'Pequeña Empresa']

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'region': np.random.choice(regions, n_customers),
    'segment': np.random.choice(segments, n_customers),
    'signup_date': [datetime(2021, 1, 1) + timedelta(days=random.randint(0, 700)) for _ in range(n_customers)]
})

# 2. Generar Transacciones (Hechos)
products = {
    'Laptop Pro': 1200, 'Monitor 4K': 400, 'Mouse Ergo': 50, 
    'Licencia Software': 150, 'Servidor Rack': 3000, 'Cable HDMI': 15
}

data = []
for _ in range(n_transactions):
    cust_id = np.random.choice(customer_ids)
    # Lógica: Clientes antiguos tienen fechas más variadas
    cust_signup = df_customers.loc[df_customers['customer_id'] == cust_id, 'signup_date'].values[0]
    cust_signup_ts = pd.to_datetime(str(cust_signup))
    
    txn_date = cust_signup_ts + timedelta(days=random.randint(0, 365))
    prod = np.random.choice(list(products.keys()))
    qty = np.random.choice([1, 1, 1, 2, 3, 5, 10], p=[0.4, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05])
    
    # Introducir "ruido" (Devoluciones o errores)
    amount = products[prod] * qty
    if random.random() < 0.02: # 2% de transacciones son devoluciones
        amount = amount * -1
        
    data.append([cust_id, txn_date, prod, qty, amount])

df_transactions = pd.DataFrame(data, columns=['customer_id', 'transaction_date', 'product', 'quantity', 'amount'])

# Exportar a CSV simulando tablas de base de datos
df_customers.to_csv('dim_customers.csv', index=False)
df_transactions.to_csv('fact_transactions.csv', index=False)

print("✅ Datos generados en directorio local: 'dim_customers.csv' y 'fact_transactions.csv'")
```
apareceran dos archivos cvs
