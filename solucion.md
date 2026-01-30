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
## el primero lleva por nombre dim_customers
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/archivos%20generados/generado_1.png?raw=true)
## y el segundo se llama fact_sales
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/archivos%20generados/generado_2.png?raw=true)
# Segundo paso SQL
El segundo paso es hacer uso de la Herramienta SQL para esto utilizaremos el motor gestor de base de datos SQLServer y vamos a hacer los siguientes puntos:
1. crear una base de datos para almacenar toda la información
2. Cargar los archivos CSV generados en tablas temporales
3. Transformar los datos a estructuras dimensionales apropiadas
4. Crear vistas de análisis que combinen información de clientes y ventas
5. Realizar consultas para validar la carga y preparar los datos para análisis
6. por ultimo exportaremos los resultados a un cvs

``` SQL
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
```

![img url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/sql/sql_1.png?raw=true)
![img url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/sql/sql_2.png?raw=true)

# Paso tres analisis y visualizaciones con python
Una vez completada la carga de datos en SQL Server, procedemos al análisis y visualización utilizando Python
``` python
# importar las librerias adecuadas 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import openpyxl as xlsx
from matplotlib.ticker import PercentFormatter


# ============================================
# 1. LECTURA Y PREPARACIÓN DE DATOS
# ============================================

# Leer archivo CSV separado por tabulaciones
datos = pd.read_csv(r'ejercicio_completo\sql\datos.csv', sep='\t')

# Mostrar primeras filas para verificar estructura
print(datos.head())

# Limpieza: eliminar filas con valores nulos en columnas clave
datos = datos.dropna(subset=['customer_id', 'product_name', 'region', 'transaction_date', 'sinup_date', 'status'])


# ============================================
# 2. ANÁLISIS EXPLORATORIO
# ============================================

# Conteo de productos vendidos por región
print(datos.groupby('region')['product_name'].count())

# Región más popular (frecuencia absoluta)
print(datos['region'].value_counts())

# Total de productos vendidos por fecha de transacción (año)
print(datos.groupby('transaction_date')['product_name'].count())

# Total de clientes registrados por fecha de registro (año)
print(datos.groupby('sinup_date')['customer_id'].count())

# Total de ventas por región
print(datos.groupby('region')['product_name'].count())

# Total de ventas por producto
print(datos.groupby('product_name')['product_name'].count())

# Clientes con más ventas (conteo de productos comprados)
print(datos.groupby('customer_id')['product_name'].count())


# ============================================
# 3. VISUALIZACIONES
# ============================================

# Gráfico 1: Barras - Top 5 clientes con más ventas
plt.figure(figsize=(12, 6))
top_5_clientes = datos.groupby('customer_id')['product_name'].count().sort_values(ascending=False).head(5)
top_5_clientes.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Top 5 Clientes con más ventas', fontsize=16, fontweight='bold')
plt.xlabel('Cliente ID', fontsize=12)
plt.ylabel('Cantidad de Productos Vendidos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 2: Pie chart - Top 10 productos más vendidos (distribución porcentual)
plt.figure(figsize=(14, 8))
top_10_productos = datos.groupby('product_name')['product_name'].count().sort_values(ascending=False).head(10)

# Configuración de colores y estilo
colors = plt.cm.Set3(np.linspace(0, 1, len(top_10_productos)))
wedges, texts, autotexts = plt.pie(top_10_productos, 
                                   labels=top_10_productos.index,
                                   autopct='%1.1f%%',
                                   startangle=90,
                                   colors=colors,
                                   shadow=True,
                                   textprops={'fontsize': 10})

# Mejorar legibilidad
plt.setp(autotexts, size=10, weight="bold", color='black')
plt.setp(texts, size=10)
plt.title('Top 10 Productos más Vendidos (Distribución)', fontsize=16, fontweight='bold')
plt.axis('equal')  # Asegurar proporción circular
plt.tight_layout()
plt.show()

# Gráfico 3: Barras - Regiones con más ventas
plt.figure(figsize=(12, 6))
top_10_regiones = datos.groupby('region')['product_name'].count().sort_values(ascending=False)
top_10_regiones.plot(kind='bar', color='salmon', edgecolor='black')
plt.title(' Regiones con más Ventas', fontsize=16, fontweight='bold')
plt.xlabel('Región', fontsize=12)
plt.ylabel('Productos Vendidos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 4: Barras - Top 10 años con más ventas
plt.figure(figsize=(12, 6))
top_10_anos = datos.groupby('transaction_date')['product_name'].count().sort_values(ascending=False).head(10)
top_10_anos.plot(kind='bar', color='gold', edgecolor='black')
plt.title('Top 10 Años con más Ventas', fontsize=16, fontweight='bold')
plt.xlabel('Año', fontsize=12)
plt.ylabel('Productos Vendidos', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 5: Barras - Top 10 productos con más ventas (alternativa al pie chart)
plt.figure(figsize=(12, 6))
top_10_productos = datos.groupby('product_name')['product_name'].count().sort_values(ascending=False).head(10)
top_10_productos.plot(kind='bar', color='seagreen', edgecolor='black')
plt.title('Top 10 Productos con más Ventas', fontsize=16, fontweight='bold')
plt.xlabel('Producto', fontsize=12)
plt.ylabel('Productos Vendidos', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 6: Barras - Top 5 clientes con más registros completos
plt.figure(figsize=(12, 6)) 
top_5_clientes = datos.groupby('customer_id')['customer_id'].count().sort_values(ascending=False).head(5)
top_5_clientes.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Top 5 Clientes con más registros completos', fontsize=16, fontweight='bold')
plt.xlabel('Cliente ID', fontsize=12)
plt.ylabel('Cantidad de Clientes', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 7: Pie chart - Distribución de estatus de clientes
plt.figure(figsize=(14, 8))
status_counts = datos['status'].value_counts()

# Crear gráfico de pastel con separación
plt.pie(status_counts.values, labels=status_counts.index,
        autopct='%1.1f%%', startangle=90,
        colors=plt.cm.Paired.colors,
        explode=[0.05] * len(status_counts))  # Separar ligeramente cada segmento

plt.title('Distribución de Estatus de Clientes', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()
```
Despues de ejecutar nuestro codigo obtenemos los siguientes resultados
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/completo_1.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/completo_2.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/completo_3.png?raw=true)
Y  las graficas visualez serian las siguientes aqui se puede apresiar mejor los datos
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_1.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_2.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_3.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_4.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_5.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_6.png?raw=true)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/visualizacion%20python/Figure_7.png?raw=true)
# paso cuatro completar visualizaciones con power bi
Podemos completar las visualizaciones con power bi.
La tabla es un subconjunto de datos de compras de clientes de la región APAC, que muestra:
- 5 clientes diferentes en la región APAC
- 7 productos diferentes que han comprado
- 21 registros de compra en total
  ![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/analisis_powerbi/Imagen1.png?raw=true)
  - Algunos clientes compran configuraciones completas (servidores + accesorios)
  - Otros se enfocan en infraestructura básica (servidores + monitores)
  - Son visibles patrones de paquetes de productos (ej: Enterprise Server frecuentemente combinado con Monitor 27in)
Esta tabla sirve como una vista a nivel micro que el código de Python agrega en información a nivel macro (clientes principales, productos principales, tendencias regionales, etc.). El código toma este tipo de datos de transacciones y los transforma en visualizaciones que muestran patrones comerciales generales.
Descripción del Gráfico:
Este es un gráfico de barras agrupadas que muestra:
- Variable principal: Suma de total_amount (monto total/ingresos)
- Agrupación primaria: Por product_name (6 productos diferentes)
- Segmentación: Por acquisition_channel (3 canales de adquisición)
- Escala: De 0 a 10M (millones de unidades monetarias)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/analisis_powerbi/Imagen2.png?raw=true)
Es una gráfica circular se muestra la distribución porcentual por canal de adquisición, representando:
Tres segmentos principales:
- Distributor: Segmento más grande (~35.6%)
- Direct Sales: Segmento mediano (~32.7%)
- Online Web: Segmento muy pequeño (~0.03%)
La gráfica visualiza cómo se reparte el total (probablemente de ventas o ingresos) entre estos tres canales de distribución, donde Distributor y Direct Sales dominan la participación, mientras que Online Web es mínima.
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/analisis_powerbi/Imagen3.png?raw=true)
Esta es una gráfica de barras agrupadas que muestra valores numéricos (en miles) para:
Estructura:
- Eje X: Los 6 productos diferentes
- Eje Y: Valores numéricos en escala de miles (K)
- Grupos de barras: 3 barras por producto (una por cada canal)

Productos mostrados:
- Monitor 27in
- Enterprise Server
- Gaming Laptop
- Ethernet Cable
- USB-C Dock
- Mechanical Keyboard

Canales representados (colores diferentes):
- Direct Sales (Ventas Directas)
- Distributor (Distribuidor)
- Online Web (Ventas Online)
Observaciones:
 - Los valores son relativamente similares entre canales para cada producto
 - Online Web muestra algunos valores ligeramente más altos en ciertos productos
 - Ethernet Cable tiene los valores más bajos en Direct Sales y Distributor
 - Mechanical Keyboard tiene el valor más alto en Online Web (3.55K)
![image url](https://github.com/luisvarela-code/ejercicio_analisisdedatos/blob/main/analisis_powerbi/Imagen4.png?raw=true)








