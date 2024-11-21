import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Análisis de Ventas", layout="wide")

# Título del proyecto
st.title(" Aplicación de Análisis de Ventas")

# Sección para cargar datos
st.sidebar.header("Cargar archivo de datos")
uploaded_file = st.sidebar.file_uploader("Subir archivo CSV", type="csv")

if uploaded_file:
    # Carga de datos
    df = pd.read_csv(uploaded_file)
    
    # Validación de columnas
    columnas_requeridas = ["Sucursal", "Producto", "Año", "Mes", "Unidades_vendidas", "Ingreso_total", "Costo_total"]
    if all(col in df.columns for col in columnas_requeridas):
        
        # Cálculos de métricas
        df["Precio_promedio"] = df["Ingreso_total"] / df["Unidades_vendidas"]
        df["Margen_promedio"] = (df["Ingreso_total"] - df["Costo_total"]) / df["Ingreso_total"]
        df["Mes_anio"] = df["Año"].astype(str) + "-" + df["Mes"].astype(str).str.zfill(2)
        
        # Selector de sucursal
        sucursales = ["Todas"] + sorted(df["Sucursal"].unique())
        sucursal_seleccionada = st.sidebar.selectbox("Seleccionar Sucursal", sucursales)
        
        if sucursal_seleccionada != "Todas":
            df = df[df["Sucursal"] == sucursal_seleccionada]
       
    
        # Mostrar datos agrupados por producto
        st.header(f"Datos de {sucursal_seleccionada}")
        productos = df["Producto"].unique()
        
        for producto in productos:
            df_producto = df[df["Producto"] == producto]
            precio_promedio = df_producto["Precio_promedio"].mean()
            margen_promedio = df_producto["Margen_promedio"].mean()
            unidades_vendidas = df_producto["Unidades_vendidas"].sum()
            
            st.subheader(producto)
            col1, col2, col3 = st.columns(3)
            col1.metric("Precio Promedio", f"${precio_promedio:.2f}", delta=f"${precio_promedio:.2f}" if precio_promedio > 0 else f"-${abs(precio_promedio):.2f}")
            col2.metric("Margen Promedio", f"{margen_promedio:.0%}", delta=f"{margen_promedio:.0%}")
            col3.metric("Unidades Vendidas", f"{unidades_vendidas:,.0f}", delta=f"{unidades_vendidas:,.0f}")
            
            # Gráfico de evolución
            st.write(f"**Evolución de Ventas Mensual - {producto}**")
            df_producto_grouped = df_producto.groupby("Mes_anio").sum(numeric_only=True)
            df_producto_grouped = df_producto_grouped.sort_index()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Graficar barras de ventas mensuales
            ax.bar(df_producto_grouped.index, df_producto_grouped["Unidades_vendidas"], color="purple", label="Ventas")
            
            
            # Agregar línea de tendencia
            x = np.arange(len(df_producto_grouped))
            z = np.polyfit(x, df_producto_grouped["Unidades_vendidas"], 1)
            p = np.poly1d(z)
            ax.plot(df_producto_grouped.index, p(x), label="Tendencia", color="red", linestyle="--")
            
            # Rotar etiquetas del eje X
            ax.set_xticks(range(0, len(df_producto_grouped), max(1, len(df_producto_grouped)//12)))
            ax.set_xticklabels(df_producto_grouped.index[::max(1, len(df_producto_grouped)//12)], rotation=45, ha="right")
            
            # Configuración adicional del gráfico
            ax.set_title(f"Evolución de Ventas de {producto}")
            ax.set_xlabel("Año-Mes")
            ax.set_ylabel("Unidades Vendidas")
            ax.legend()
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            
            st.pyplot(fig)
    else:
        st.error("El archivo CSV no contiene las columnas requeridas.")
else:
    st.write("Por favor, suba un archivo CSV para comenzar.")
    st.write("Urbani Juan Pablo - 59064 - C5.")
