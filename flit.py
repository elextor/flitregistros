import streamlit as st
import json
import requests
from pandas import json_normalize
import pandas as pd
import streamlit as st



# Configuración general
st.set_page_config(page_title="Registros", layout="wide")
st.title("Registros FLIT 2025 - consolidado")

# URL de Firebase
geojson_url = "https://callfirebase.firebaseio.com/flitregistrados.json"

# Leer datos y transponer
df = pd.read_json(geojson_url).T

# Crear índice personalizado
df.index = [f"Registro {i+1}" for i in range(len(df))]

# ─────────────────────────────────────
# PROCESAR COLUMNA 'FechaRegistro'
# ─────────────────────────────────────
df['Fecha'] = df['FechaRegistro'].str.slice(0, 10)
hora = df['FechaRegistro'].str.slice(11)

# Limpiar formato de hora y asegurar formato HH:MM:00
hora = hora.str.replace(' a. m.', '', regex=False).str.replace(' p. m.', '', regex=False)
hora = hora.str[:5] + ':00'
df['Hora'] = hora

# Crear columna datetime combinada
df['concatfecha'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'], errors='coerce')

# Convertir columna 'Fecha' a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

# (Opcional) columna con fecha-hora formateada como texto
df['FechaHoraStr'] = df['concatfecha'].dt.strftime('%Y-%m-%d %H:%M:%S')

# ─────────────────────────────────────
# Crear columnas para las métricas horizontales
# ─────────────────────────────────────
conteo = df['seleccionSpinner1'].value_counts()

# Configura las columnas
col1, col2, col3, col4 = st.columns(4)

# METRIC: Total de registros
with col1:
    st.metric(
        label="Total de registros",
        value=str(len(df)),
        delta=100
    )

# METRIC: Primer registro (Fecha más temprana)
with col2:
    primer_registro = df['concatfecha'].min()
    st.metric(
        label="Primer registro ",
        value=primer_registro.strftime('%Y-%m-%d %H:%M:%S'),
        delta=None
    )

# METRIC: Último registro (Fecha más reciente)
with col3:
    ultimo_registro = df['concatfecha'].max()
    st.metric(
        label="Último registro hoy",
        value=ultimo_registro.strftime('%Y-%m-%d %H:%M:%S'),
        delta=None
    )

# METRIC: Conteo de 'seleccionSpinner1'
with col4:
    # Dividimos el conteo en múltiples columnas para que sea horizontal
    rows = len(conteo)
    cols = st.columns(rows)

    for i, (value, count) in enumerate(conteo.items()):
        cols[i].metric(
            label=f"{value}",
            value=str(count),
            delta=None
        )




# ─────────────────────────────────────
# Mostrar el DataFrame
# ─────────────────────────────────────


# Configura las 4 nuevas columnas debajo de las anteriores
col5, col6, col7, col8 = st.columns(4)

# METRIC: Total de registros en las nuevas columnas (por ejemplo)

# Obtén el conteo de la columna 'seleccionSpinner1'
conteo_spinner = df['seleccionSpinner1'].value_counts()
frecuencia_valores = df['seleccionRadio1'].value_counts()
frecuencia_valores_top3 = frecuencia_valores.head(7)

with col5:
    # Dividimos el conteo de los 3 primeros valores en columnas horizontales
    rows = len(frecuencia_valores_top3)
    cols = st.columns(rows)

    for i, (value, count) in enumerate(frecuencia_valores_top3.items()):
        cols[i].metric(
            label=f"{value}",
            value=str(count),
            delta=None
        )

# METRIC: Primer registro (Fecha más temprana) en las nuevas columnas


# METRIC: Total de registros en las nuevas columnas (por ejemplo)

num_registros = df.shape[0]

# Multiplicar por el 30%
resultado = num_registros * 0.30
with col6:
    st.metric(
        label="Leads playstore",
        value=str(resultado)+"%",
        delta=None
    )

# METRIC: Primer registro (Fecha más temprana) en las nuevas columnas

# Convertir el resultado a entero
# Sumar el resultado al número de registros

downloadadata=num_registros+resultado
with col7:
    st.metric(
        label="Descargas playstore",
        value=str(int(downloadadata)),
        delta=None
    )

desersiondownleads=downloadadata-num_registros
with col8:
    st.metric(
        label="Deserción Leads",
        value=str(int(desersiondownleads)),
        delta=-0.6
    )

st.subheader("Datos completos")
st.dataframe(df, use_container_width=True)

# Conteo por fecha
# Asegúrate de que la columna 'Fecha' esté en formato datetime
# Conteo por fecha
conteo_por_fecha = df['Fecha'].dt.date.value_counts().sort_index()

# Convertir el conteo en un DataFrame
conteo_df = conteo_por_fecha.reset_index()
conteo_df.columns = ['Fecha', 'Cantidad de Registros']

# Convertir las fechas al formato 'yyyy-mm-dd' como cadenas
conteo_df['Fecha'] = conteo_df['Fecha'].astype(str)

# Crear una fila con 2 columnas: izquierda vacía y gráfico en la derecha
st.subheader("Cantidad de Registros por Fecha")
st.bar_chart(conteo_df.set_index('Fecha'))

# Colocar el gráfico de líneas en la segunda columna
# Convertir 'solo_fecha' a formato de fecha (si no está ya)
# Convertir 'Fecha' a formato datetime si aún no lo está
# Asegúrate de que 'Fecha' y 'Hora' estén correctamente formateadas
# Asegúrate de que 'Fecha' está en formato datetime



# ─────────────────────────────────────
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=True).encode('utf-8')

csv = convert_df_to_csv(df)

st.download_button(
    label="Descargar como CSV",
    data=csv,
    file_name="registros.csv",
    mime="text/csv",
)