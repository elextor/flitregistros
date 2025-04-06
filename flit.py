import streamlit as st
import json
import requests
from pandas import json_normalize
import pandas as pd
import streamlit as st




# Configuración de la app
st.set_page_config(page_title="Registros", layout="wide")

st.title("Registros FLIT 2025 - consolidado")

# Cargar los datos desde la URL
geojson_url = "https://callfirebase.firebaseio.com/flitregistrados.json"
df = pd.read_json(geojson_url).T

# Crear un índice personalizado
df.index = [f"Registro {i+1}" for i in range(len(df))]

# Mostrar la cantidad total de registros
st.metric(label="Total de registros", value=len(df))

# Mostrar el DataFrame
st.subheader("Datos completos")
st.dataframe(df, use_container_width=True)

# Opción para descargar el DataFrame como CSV
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