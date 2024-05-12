import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
#df_bairros = pd.read_csv('bairros.csv', encoding='utf-8')
df_bairros = pd.read_csv('https://raw.githubusercontent.com/kaiquemiranda/MetheoraApp/main/Bairros.csv', encoding='utf-8')

# Coordenadas dos bairros selecionados de São Paulo
coordenadas = dict(zip(df_bairros['Bairro'], zip(df_bairros['Latitude'], df_bairros['Longitude'])))

# Chave da API da WeatherAPI
api_key = "94a63f8c79a64d5a822101559241005"

# Função para calcular o risco com base na precipitação
def calcular_risco(precip_mm):
    if precip_mm < 2:
        return 'Baixo'
    elif precip_mm < 3:
        return 'Médio'
    else:
        return 'Alto'

# Configuração da página
st.set_page_config(page_title="METHEORA",page_icon=":lightning:", layout="wide")
st.sidebar.image('logo.png', width=240)
st.sidebar.markdown("<h1 style='text-align: center; margin-top: -40px; margin-left: -20px'>METHEORA</h1>",
    unsafe_allow_html=True)
st.sidebar.markdown("")

# Selecionar um bairro
selected_bairro = st.sidebar.selectbox('Selecione um bairro', df_bairros['Bairro'])
# Obter dados meteorológicos
weather_data = get_weather_data(api_key, selected_bairro)

# SIDEBAR ===============================================================

# Apresentar informações meteorológicas
if weather_data:
    
    st.sidebar.markdown("")
    #st.sidebar.markdown(f"### {selected_bairro}")
    st.sidebar.markdown(f"**Temperatura:** {weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']} °C &#9925;")
    st.sidebar.markdown(f"**Chuva prevista:** {weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm']} mm")
    if weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm'] < 1:
        st.sidebar.markdown(f"**Risco de incidente:** Baixo")
    elif weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm'] < 2:
        st.sidebar.markdown(f"**Risco de incidente:** Medio")
    else:
        st.sidebar.markdown(f"**Risco de incidente:** Alto")
else:
    st.error("Falha ao obter os dados meteorológicos. Por favor, tente novamente mais tarde.")

# SIDEBAR ====================================================================


st.markdown(
    "<h1 style='text-align: center;'>DASHBOARD</h1>",
    unsafe_allow_html=True
)

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
                    size=27,
                    opacity=0.6,
                    color='red' if risco == 'Alto' else ('orange' if risco == 'Médio' else 'green'),
                ),
                name=bairro,
                text=bairro + '<br>Chuva prevista: ' + str(precip_mm) + ' mm' + '<br>Risco de incidente: ' + risco,
            )
        )
st.markdown(" ")
tema_mapa = st.sidebar.radio("Tema do mapa:", ('Dark', 'Light'))
tema = 'open-street-map' if tema_mapa == 'Light' else 'carto-darkmatter'
fig_mapa.update_layout(
    hovermode='closest',
    mapbox=dict(
        style=tema,
        center=dict(
            lat=-23.5505,
            lon=-46.6333,
        ),
        zoom=10,
    ),
    height=690  # Defina a altura desejada aqui
)
st.plotly_chart(fig_mapa, use_container_width=True)
# ====================== Mapa de risco Incidente =======================


# ====================== graficos =======================

# Layout do aplicativo
if selected_bairro:
    col1, col2 = st.columns([2, 1])
    col3, col4 = st.columns([1, 2])

    
    with col1:
        # Gráfico de linha com dados aleatórios
        dados_aleatorios_linha = np.random.rand(len(df_bairros))
        fig_linha = go.Figure(data=go.Scatter(x=df_bairros['Bairro'], y=dados_aleatorios_linha))
        st.plotly_chart(fig_linha, use_container_width=True)

    with col2:
        # Gráfico de barras com dados aleatórios
        dados_aleatorios_barra = np.random.rand(len(df_bairros))
        fig_barra = go.Figure(data=[go.Bar(x=df_bairros['Bairro'], y=dados_aleatorios_barra, marker_color='#FF4B4B')])
        st.plotly_chart(fig_barra, use_container_width=True)

    with col3:
        # Gráfico de dispersão em 3D com dados aleatórios
        dados_aleatorios_dispersao_3d_x = np.random.rand(len(df_bairros))
        dados_aleatorios_dispersao_3d_y = np.random.rand(len(df_bairros))
        dados_aleatorios_dispersao_3d_z = np.random.rand(len(df_bairros))
        fig_dispersao_3d = go.Figure(data=[go.Scatter3d(x=dados_aleatorios_dispersao_3d_x, y=dados_aleatorios_dispersao_3d_y, z=dados_aleatorios_dispersao_3d_z, mode='markers')])
        st.plotly_chart(fig_dispersao_3d, use_container_width=True)

    with col4:
        # Gráfico de área com dados aleatórios
        dados_aleatorios_area = np.random.rand(len(df_bairros))
        fig_area = go.Figure(data=[go.Scatter(x=df_bairros['Bairro'], y=dados_aleatorios_area, fill='tozeroy')])
        st.plotly_chart(fig_area, use_container_width=True)



# ====================== graficos =======================




# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Nimbus Tech - © 2024")
