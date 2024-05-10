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
df_bairros = pd.read_csv('bairros.csv', encoding='utf-8')

# Coordenadas dos bairros selecionados de São Paulo
coordenadas = dict(zip(df_bairros['Bairro'], zip(df_bairros['Latitude'], df_bairros['Longitude'])))

# Dados fictícios de probabilidade de incidente por bairro
dados_probabilidade = {
    'Bairro': df_bairros['Bairro'],
    'Probabilidade': np.random.rand(len(df_bairros))
}

# Atualizando as probabilidades e categorizando os riscos
risco = []
for prob in dados_probabilidade['Probabilidade']:
    if prob < 0.3:
        risco.append('Baixo')
    elif prob < 0.5:
        risco.append('Médio')
    else:
        risco.append('Alto')

dados_probabilidade['Risco'] = risco

# Cria um DataFrame com os dados de probabilidade
df_probabilidade = pd.DataFrame(dados_probabilidade)

# Contagem de bairros por nível de risco
contagem_risco = df_probabilidade.groupby('Risco').size()

# Identificar os bairros com maior risco
bairros_com_maior_risco = df_probabilidade[df_probabilidade['Risco'] == 'Alto']

# Chave da API da WeatherAPI
api_key = "5c21ddfee4ac422aa8402205241005"

# Configuração da página
st.set_page_config(page_title="METHEORA", page_icon=":zap:", layout="wide")


# SIDEBAR ===============================================================
st.sidebar.image('METHEORA.jpeg', width=200)
st.sidebar.markdown("")
st.sidebar.markdown("")

# Selecionar um bairro
selected_bairro = st.sidebar.selectbox('Selecione um bairro', df_bairros['Bairro'])

# Obter dados meteorológicos
weather_data = get_weather_data(api_key, selected_bairro)

# Apresentar informações meteorológicas
if weather_data:
    st.sidebar.markdown("")
    st.sidebar.markdown(f"### {selected_bairro}")
    st.sidebar.markdown(f"**Temperatura:** {weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']} °C")
    st.sidebar.markdown(f"**Chuva:** {weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm']} mm")
else:
    st.error("Falha ao obter os dados meteorológicos. Por favor, tente novamente mais tarde.")

# SIDEBAR ====================================================================

st.title("DASHBOARD")
st.markdown("---")

# Mapa de Probabilidade de Incidente
fig_mapa = go.Figure()
for bairro, probabilidade, risco in zip(df_probabilidade['Bairro'], df_probabilidade['Probabilidade'], df_probabilidade['Risco']):
        fig_mapa.add_trace(
            go.Scattermapbox(
                lat=[coordenadas[bairro][0]],
                lon=[coordenadas[bairro][1]],
                mode='markers',
                marker=dict(
                    size=12,
                    opacity=0.8,
                    color='red' if risco == 'Alto' else ('yellow' if risco == 'Médio' else 'green'),
                ),
                name=bairro,
                text=bairro + '<br>Probabilidade de Incidente: ' + str(round(probabilidade * 100, 2)) + '%' + '<br>Risco: ' + risco,
            )
        )
fig_mapa.update_layout(
        hovermode='closest',
        mapbox=dict(
            style='carto-darkmatter',  # open-street-map
            center=dict(
                lat=-23.5505,
                lon=-46.6333,
            ),
            zoom=10,
        )
    )
st.plotly_chart(fig_mapa, use_container_width=True)

# Layout do aplicativo
col1, col2 = st.columns([1, 2])

with col1:
    st.bar_chart(contagem_risco)

with col2:
    st.line_chart(df_probabilidade.set_index('Bairro')['Probabilidade'])

st.bar_chart(bairros_com_maior_risco.set_index('Bairro')['Probabilidade'])

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Nimbus Tech - © 2024")
