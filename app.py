import streamlit as st
import pandas as pd
import numpy as np
import requests

# Função para obter dados meteorológicos
def get_weather_data(api_key, city):
    endpoint = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Ler o arquivo CSV com os dados dos bairros
df_bairros = pd.read_csv('bairros.csv', encoding='utf-8')

# Coordenadas dos bairros selecionados de São Paulo
coordenadas = dict(zip(df_bairros['Bairro'], zip(df_bairros['Latitude'], df_bairros['Longitude'])))

# Chave da API da WeatherAPI
api_key = "94a63f8c79a64d5a822101559241005"

# Função para calcular o risco com base na precipitação
def calcular_risco(precip_mm):
    if precip_mm < 5:
        return 'Baixo'
    elif precip_mm < 8:
        return 'Médio'
    else:
        return 'Alto'

# Configuração da página
st.set_page_config(page_title="METHEORA", page_icon=":zap:", layout="wide")
st.sidebar.image('METHEORA.jpeg', width=200)
st.sidebar.markdown("")
st.sidebar.markdown("")

# Selecionar um bairro
selected_bairro = st.sidebar.selectbox('Selecione um bairro', df_bairros['Bairro'])
# Obter dados meteorológicos
weather_data = get_weather_data(api_key, selected_bairro)

# SIDEBAR ===============================================================

# Apresentar informações meteorológicas
if weather_data:
    
    st.sidebar.markdown("")
    st.sidebar.markdown(f"### {selected_bairro}")
    st.sidebar.markdown(f"**Temperatura:** {weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']} °C")
    st.sidebar.markdown(f"**Chuva:** {weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm']} mm")
    if weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm'] < 1:
        st.sidebar.markdown(f"Risco de incidente: Baixo ")
    elif weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm'] < 2:
        st.sidebar.markdown(f"Risco: Medio")
    else:
        st.sidebar.markdown(f"Risco: Alto")
else:
    st.error("Falha ao obter os dados meteorológicos. Por favor, tente novamente mais tarde.")

# SIDEBAR ====================================================================


st.title("DASHBOARD")
st.markdown("---")

# ====================== Mapa de risco Incidente =======================
fig_mapa = go.Figure()
for bairro in df_bairros['Bairro']:
    weather_data_bairro = get_weather_data(api_key, bairro)
    if weather_data_bairro:
        precip_mm = weather_data_bairro['forecast']['forecastday'][0]['day']['totalprecip_mm']
        risco = calcular_risco(precip_mm)
        fig_mapa.add_trace(
            go.Scattermapbox(
                lat=[coordenadas[bairro][0]],
                lon=[coordenadas[bairro][1]],
                mode='markers',
                marker=dict(
                    size=22,
                    opacity=0.7,
                    color='red' if risco == 'Alto' else ('yellow' if risco == 'Médio' else 'green'),
                ),
                name=bairro,
                text=bairro + '<br>Chuva: ' + str(precip_mm) + ' mm' + '<br>Risco: ' + risco,
            )
        )
fig_mapa.update_layout(
    hovermode='closest',
    mapbox=dict(
        style='carto-darkmatter',
        center=dict(
            lat=-23.5505,
            lon=-46.6333,
        ),
        zoom=10,
    )
    
)
st.plotly_chart(fig_mapa, use_container_width=True)
# ====================== Mapa de risco Incidente =======================




# ====================== graficos =======================



# ====================== graficos =======================




# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Nimbus Tech - © 2024")
