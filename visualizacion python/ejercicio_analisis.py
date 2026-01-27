import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import openpyxl as xlsx
from matplotlib.ticker import PercentFormatter


# 1. Leer el archivo de datos
datos = pd.read_csv(r'ejercicio_completo\sql\datos.csv', sep='\t')

# ver las filas del dataframe
print(datos.head())

# limpoar datos
datos = datos.dropna(subset=['customer_id', 'product_name', 'region', 'transaction_date', 'sinup_date', 'status'])
# analisisde datos
# ver la region del cliente con mas productos
print(datos.groupby('region')['product_name'].count())

# ver la region mas popular en  la venta de productos
print(datos['region'].value_counts())

# ver el total de los productos mas vendidos por año
print(datos.groupby('transaction_date')['product_name'].count())

# ver el total de clientes registrados por año
print(datos.groupby('sinup_date')['customer_id'].count())

# ver el total de ventas por año
print(datos.groupby('transaction_date')['product_name'].count())

# ver el total de ventas por region
print(datos.groupby('region')['product_name'].count())

# ver el total de ventas por producto
print(datos.groupby('product_name')['product_name'].count())

# ver los nombres de los clientes con mas ventas
print(datos.groupby('customer_id')['product_name'].count())

# visualizaciones

# grafica de barras top 5 de los clientes con mas ventas 
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

# grafica  barra de pastel  top 10 de los productos mas vendidos
plt.figure(figsize=(14, 8))
top_10_productos = datos.groupby('product_name')['product_name'].count().sort_values(ascending=False).head(10)

# Crear la gráfica de pastel con porcentajes
colors = plt.cm.Set3(np.linspace(0, 1, len(top_10_productos)))
wedges, texts, autotexts = plt.pie(top_10_productos, 
                                   labels=top_10_productos.index,
                                   autopct='%1.1f%%',
                                   startangle=90,
                                   colors=colors,
                                   shadow=True,
                                   textprops={'fontsize': 10})

# Mejorar la legibilidad
plt.setp(autotexts, size=10, weight="bold", color='black')
plt.setp(texts, size=10)
plt.title('Top 10 Productos más Vendidos (Distribución)', fontsize=16, fontweight='bold')
plt.axis('equal')  # Para que sea un círculo perfecto
plt.tight_layout()
plt.show()


# grafica de barras top 10 de las regiones con mas ventas
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

# grafica de barras top 10 de los años con mas ventas
plt.figure(figsize=(12, 6))
top_10_anos = datos.groupby('year')['product_name'].count().sort_values(ascending=False).head(10)
top_10_anos.plot(kind='bar', color='gold', edgecolor='black')
plt.title('Top 10 Años con más Ventas', fontsize=16, fontweight='bold')
plt.xlabel('Año', fontsize=12)
plt.ylabel('Productos Vendidos', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# grafica de barras top 10 de los productos con mas ventas
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

# top 5 de los clientes y su estatus con mas registros completos 
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

# historigrama comparativo de los estatus de los clientes 
plt.figure(figsize=(14, 8))
status_counts = datos['status'].value_counts()

# Crear gráfico de pastel
plt.pie(status_counts.values, labels=status_counts.index,
        autopct='%1.1f%%', startangle=90,
        colors=plt.cm.Paired.colors,
        explode=[0.05] * len(status_counts))

plt.title('Distribución de Estatus de Clientes', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()



