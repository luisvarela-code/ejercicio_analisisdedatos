# ejercicio_analisisdedatos
#### OmniLogistics S.A. está enfrentando una paradoja financiera: mientras nuestros ingresos brutos alcanzan máximos históricos, el margen de beneficio neto por cliente está en declive.
#### La Problemática: La Dirección Ejecutiva sospecha que estamos incurriendo en un "Costo de Adquisición" (CAC) alto para atraer clientes que realizan una única compra y luego abandonan (Churn), o cuyo valor de vida (CLV) no justifica la inversión.
# Objetivo
Como líder técnico de datos, debes construir un pipeline analítico que transforme datos transaccionales crudos en inteligencia de negocio para:
- Limpiar y estructurar los datos transaccionales brutos.
- Segmentar la base de clientes utilizando técnicas estadísticas avanzadas (no solo reglas de negocio).
- Entregar un Dashboard interactivo que permita al equipo de Marketing identificar a quién deben enviar campañas de fidelización.
## Aprovisionamiento de Datos (Fase 0)
La empresa no posee un Data Lake estructurado para este ejercicio. Se te proporcionan scripts de extracción del sistema legacy.
##### Instrucción: Ejecuta el siguiente script de Python en tu entorno local. Esto simulará la extracción de datos y generará dos archivos planos: dim_customers.csv y fact_transactions.csv.
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
## FASE I: Modelado y Limpieza (SQL)
Objetivo: Crear una "Analytical Base Table" (ABT) limpia y lista para modelos de ML.
Aunque puedes usar SQL estándar (DuckDB, SQLite, BigQuery), queremos evaluar tu capacidad de pensar en arquitectura modular (al estilo dbt).
Debes crear una Tabla Analítica de Clientes (Customer ABT) que resuma el comportamiento histórico de cada usuario.
1. Limpieza (Staging): Escribe una consulta que limpie fact_transactions.
- Identifica y gestiona las devoluciones (montos negativos).
- Debes decidir: ¿Las excluyes o las sumas algebraicamente para obtener el "Net Revenue"? Justifica tu decisión.
2. Agregación (Marts): Genera una tabla final fct_customer_rfm con una fila por cliente que contenga:
  - monetary: Ingresos netos totales.
  - frequency: Número de transacciones válidas.
  - recency: Días transcurridos desde la última compra hasta la fecha máxima del dataset ("Hoy").
  - avg_ticket: Ticket promedio.
    
Bonus Point: Estructura tu query usando CTEs (Common Table Expressions) nombrados como with staging as (...), with intermediate as (...), simulando capas de dbt.
## FASE II: Segmentación Avanzada (Python)
#### Objetivo: Segmentación no supervisada.
1. Carga la tabla fct_customer_rfm generada en el paso anterior.
2. Pre-procesamiento:
   - Analiza la distribución de las variables.
   - Aplica StandardScaler (Scikit-learn) para normalizar los datos.
3. Modelado:
   - Utiliza el algoritmo K-Means.
   - Determina un número óptimo de clusters (3 o 4) basado en tu criterio de negocio.
4. Interpretación:
   - Asigna nombres a los clusters (Ej: "VIP", "En Riesgo", "Low Value").
   - Exporta el dataset final con la columna cluster_label.
## Visualización de Impacto (Power BI)
##### Objetivo: Dashboard Operativo para Gerencia de Ventas.
Crea un reporte de una página que responda: ¿Dónde estamos perdiendo dinero?
1. Visuales Clave:
   - Matriz de Dispersión: Recency vs. Monetary, coloreado por Cluster.
   - KPIs: Ventas Totales, Ticket Promedio, y una métrica calculada de "Churn Rate" (clientes con > 90 días sin compra).
2. Filtros:
   - Permite filtrar por Region y Segment (datos de dim_customers).
3. Interacción:
   - El dashboard debe permitir hacer "Drill-down" o filtrado cruzado al seleccionar un cluster.
