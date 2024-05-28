import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import streamlit_shadcn_ui as ui

# Função para obter dados meteorológicos
def get_weather_data(api_key, city):
    endpoint = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Ler o arquivo CSV com os dados dos bairros no github
bairros_coordenas = pd.read_csv('https://raw.githubusercontent.com/kaiquemiranda/DataLakeMetheora/main/Bairros.csv', encoding='utf-8')

# Coordenadas dos bairros selecionados de São Paulo
coordenadas = dict(zip(bairros_coordenas['Bairro'], zip(bairros_coordenas['Latitude'], bairros_coordenas['Longitude'])))

# Chave da API da WeatherAPI
api_key = "94a63f8c79a64d5a822101559241005"

# Função para calcular o risco com base na precipitação
def calcular_risco(precip_mm):
    if precip_mm < 8:
        return 'Baixo'
    elif precip_mm < 20:
        return 'Médio'
    else:
        return 'Alto'


# Configuração da página
st.set_page_config(page_title="METHEORA", page_icon=":lightning:", layout="wide")
st.sidebar.image('logoMetheora.png', width=350)
st.sidebar.markdown("<h1 style='text-align: center; margin-top: -80px; margin-bottom: 40px;'>METHEORA</h1>", unsafe_allow_html=True)

# Selecionar um bairro
selected_bairro = st.sidebar.selectbox('Selecione um bairro', bairros_coordenas['Bairro'])
# Obter dados meteorológicos
weather_data = get_weather_data(api_key, selected_bairro)

# ================== METRICS =============================================
st.markdown(f"<h1 style='text-align: center; margin-top: -60px; margin-bottom: 40px;'>{selected_bairro}</h1>", unsafe_allow_html=True)
# Apresentar informações meteorológicas
if weather_data:
    current_weather = weather_data['current']
    forecast = weather_data['forecast']['forecastday'][0]['day']
    total_precip_mm = forecast['totalprecip_mm']
    daily_chance_of_rain = forecast['daily_chance_of_rain']
    temperatura = current_weather['temp_c']
    st.sidebar.markdown("")
    coluna1, coluna2, coluna3, coluna4 = st.columns([1, 1, 1, 1])
    with coluna1:
        ui.metric_card(title='TEMPERATURA', content=f'{temperatura}°C')
    with coluna2:
        ui.metric_card(title="CHUVA PREVISTA", content=f'{total_precip_mm}mm')
    with coluna3:
        ui.metric_card(title="CHANCE DE CHUVA", content=f'{daily_chance_of_rain}%')
    with coluna4:
        if total_precip_mm < 8:
            ui.metric_card(title="RISCO DE INCIDENTE", content='Baixo')
        elif total_precip_mm < 20:
            ui.metric_card(title="RISCO DE INCIDENTE", content='Médio')
        else:
            ui.metric_card(title="RISCO DE INCIDENTE", content='Alto')
else:
    st.error("Falha ao obter os dados meteorológicos. Por favor, tente novamente mais tarde.")

# ================== METRICS =============================================

# ====================== Mapa de risco Incidente =======================
fig_mapa = go.Figure()
bairros_risco_alto = []
for bairro in bairros_coordenas['Bairro']:
    weather_data_bairro = get_weather_data(api_key, bairro)
    if weather_data_bairro:
        precip_mm = weather_data_bairro['forecast']['forecastday'][0]['day']['totalprecip_mm']
        risco = calcular_risco(precip_mm)
        if risco == 'Alto':
            bairros_risco_alto.append(bairro)
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

st.markdown("---")
# ==================== tema do mapa =================================
st.markdown("Tema do mapa")
switch_value = ui.switch(default_checked=False, label="Dark", key="switch1")
tema = 'carto-darkmatter' if switch_value == True else 'open-street-map'
# ==================== tema do mapa ==================================
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
    height=690  # altura do mapa
)

st.plotly_chart(fig_mapa, use_container_width=True)
# ====================== Mapa de risco Incidente =======================

# Exibir alerta dialog se houver bairros com risco alto
if bairros_risco_alto:
    bairros_str = ", ".join(bairros_risco_alto)
    st.sidebar.warning(f'Bairros com risco de incidente: {bairros_str}',icon="⚠️")


#  ========================================================================================
# Carregar os dados
bairros = pd.read_csv('https://raw.githubusercontent.com/kaiquemiranda/DataLakeMetheora/main/2024-04-PLUVIOMETRIA.csv', encoding='latin1', sep=';')
# ==================== Limpeza ===========================================================
colunas_para_excluir = ['Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34', 'Unnamed: 35']
bairros = bairros.drop(columns=colunas_para_excluir)
bairros = bairros.dropna()
# Transformar os dados para que os valores de precipitação sejam numéricos
for col in bairros.columns[1:-1]:  # Ignorar a coluna 'Bairro' e a última coluna 'TOTAL'
    bairros[col] = bairros[col].str.replace(',', '.').astype(float)

# ================= Limpeza ===============================================================

# ====================== graficos ============================================================

# Seleção de bairro no Streamlit
bairro_seleconado = st.selectbox('Selecione um bairro', bairros['Bairro']) 
if bairro_seleconado:
    # Filtrar os dados do bairro selecionado
    dados_bairro = bairros[bairros['Bairro'] == bairro_seleconado].iloc[0, 1:-1]  # Ignorar a coluna 'Bairro' e a última coluna 'TOTAL'

    # Criar um DataFrame para Plotly Express
    df_plot = pd.DataFrame({
        'Dia': dados_bairro.index,
        'Precipitação (mm)': dados_bairro.values
    })
    # Criar o gráfico de barras
    fig_Precip = px.bar(df_plot, x='Dia', y='Precipitação (mm)', title=f'Precipitação por dia no bairro {bairro_seleconado}')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_Precip, use_container_width=True)

# Layout do aplicativo
col1, col2 = st.columns([2, 1])
with col1:
    # Gráfico de barras com dados aleatórios
    dados_aleatorios_barra = np.random.rand(len(bairros_coordenas))
    fig_barra = go.Figure(data=[go.Line(x=bairros_coordenas['Bairro'], y=dados_aleatorios_barra, marker_color='#FF4B4B')])
    st.plotly_chart(fig_barra, use_container_width=True)
    
with col2:
    # Calcular a precipitação total por bairro
    bairros['Precipitação Total'] = bairros.iloc[:, 1:-1].sum(axis=1)
    # Selecionar os 10 bairros com maior precipitação total
    top_5_bairros = bairros.nlargest(5, 'Precipitação Total')
    # Criar o gráfico de pizza com Plotly Express
    fig_pizza = px.pie(top_5_bairros, names='Bairro', values='Precipitação Total', title='Bairros com Maior Precipitação (mm)')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_pizza, use_container_width=True)


# ====================== graficos ============================================================================

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; '>Desenvolvido por Nimbus Tech - © 2024</p>", unsafe_allow_html=True)
