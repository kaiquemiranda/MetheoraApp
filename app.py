import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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

# Ler o arquivo CSV com os dados dos bairros no github
df_bairros = pd.read_csv('https://metheora.s3.us-east-2.amazonaws.com/2024-04-PLUVIOMETRIA.csv?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAIaCXVzLWVhc3QtMiJGMEQCIGltCzJsMyiVRGdc%2FH0iOm7ZcDAxhJ%2Bog2fu3rhk8Ov8AiA0CX622QWNgxpBtQh%2BVUK4zaGiQ3kHACjsCVvqJYQS%2BirkAgh7EAAaDDczMDMzNTIzMjM3NCIMy4PrnyCTJ5acaKeqKsECKjkRCbqAoUWVhJ0%2FHkg9qtvQCtXWtLyewG3bXh6TCBh56dc0XDRRw%2FgZub00tsqHS5uLLHHY%2FCvG3cePL%2FYe3bqIFn1b3N7mBhXmHBbUI4HEKwGdjMD8CnUr0mXeUPhvGOMd4vN7PMHlhq5emSL1nOOg07nj39NJE3YhoN15tEcHXm7ePEAeQeh1CHe0wE3rr%2Ffolt%2FNncOp%2FximamU%2BUJ7BZf2o9BcTX7jSrlTyLwH9YCIWmaNre14eQ%2BR40pyNiMh3t%2F%2B4iG0XfpcCifsDbsJ6lR5aJg1HfoA%2BpWe9g%2BonajcnE8QM7m6Kr97mBOsAtKoIL3GGO0IUYZ1%2FX9qP0YLH1gWcKSDCvBSqojoo5zUMCsB1iBtyYfpvXltHO7dZpvhdJbXFvnu22WlQMTGHig7%2BnwGNw%2FPQGUUG95kKM%2FymMJGEvrIGOrQCdy3z208dLOxarnoGHWV7zqEB1y8gpdsjDll4QmSX9vwLqbat5A%2BmkaN6m0BOPJ236BSXGZF0HPWAVwOu764yAxTo15nWGS2cmQFPm%2FjHE3esxdidDu1ATuvIAM4LGpHvTmKQ4LuL8kBg%2FxTdxCNTnTsiaTKmOLEHw7o7EJKC%2BzximHEU8t9KwX2V5BIaWC9UJD39zb65i0yMR3Ty4I5WBwcYOsKnt5vKcX9F%2BOIXvmDvtQjpLc%2BRKze46A0YgGp3Ie4VwfGoy6tsNxrGZ7mKHVXFpQa2QvMKe%2B0bTPjvILNfSRp%2BrW%2Fdi9q%2BTsTw3wCGuoLtz6Rb4fso3Up3EH9DBVU1VNHy9B5bSrKo1N8jLjOGVGHjekQNA59K5IiSM01fPz9lEVrh47cuT7wqv%2F9SNWqn2yc%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240523T180320Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Credential=ASIA2UC27IF3BZMIUDNQ%2F20240523%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=7c106bd7d68b5ed500fd56d5512ffdb4ba20208d1411d941f35f0dafb95e2598', encoding='utf-8')

# Coordenadas dos bairros selecionados de São Paulo
coordenadas = dict(zip(df_bairros['Bairro'], zip(df_bairros['Latitude'], df_bairros['Longitude'])))

# Chave da API da WeatherAPI
api_key = "94a63f8c79a64d5a822101559241005"


# Função para calcular o risco com base na precipitação
def calcular_risco(precip_mm):
    if precip_mm < 1:
        return 'Baixo'
    elif precip_mm < 2:
        return 'Médio'
    else:
        return 'Alto'

# Configuração da página
st.set_page_config(page_title="METHEORA",page_icon=":lightning:", layout="wide")
st.sidebar.image('logoMetheora.png', width=350)
#st.sidebar.markdown("<h1 style='text-align: center; margin-top: -60px; margin-bottom: 40px;'>METHEORA</h1>", unsafe_allow_html=True)

# Selecionar um bairro
selected_bairro = st.sidebar.selectbox('Selecione um bairro', df_bairros['Bairro'])
# Obter dados meteorológicos
weather_data = get_weather_data(api_key, selected_bairro)


# ================== METRICS =============================================
st.markdown(f"<h1 style='text-align: center; margin-top: -60px; margin-bottom: 40px;'>{selected_bairro}</h1>", unsafe_allow_html=True)
# Apresentar informações meteorológicas
if weather_data:
    forecast = weather_data['forecast']['forecastday'][0]['day']
    total_precip_mm = forecast['totalprecip_mm']
    daily_chance_of_rain = forecast['daily_chance_of_rain']
    temperatura =  forecast['avgtemp_c']
    st.sidebar.markdown("")
    coluna1, coluna2, coluna3, coluna4 = st.columns([1,1,1,1])
    coluna1.metric(label='**TEMPERATURA** ', value=f'{temperatura}°C', delta=f'{np.random.randint(-2,4)}°C')
    coluna2.metric(label="**CHUVA ESPERADA**", value=f'{total_precip_mm}mm')
    coluna3.metric(label="**PROBABILIDADE DE CHUVA**", value=f'{daily_chance_of_rain}%')  
    with coluna4:
        if total_precip_mm < 1:
            st.metric(label="**RISCO DE INCIDENTE**", value='Baixo')
        elif total_precip_mm < 2:
            st.metric(label="**RISCO DE INCIDENTE**", value='Médio')
        else:
            st.metric(label="**RISCO DE INCIDENTE**", value='Alto')
else:
    st.error("Falha ao obter os dados meteorológicos. Por favor, tente novamente mais tarde.")

# ================== METRICS =============================================




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
                text= bairro + '<br>Chuva prevista: ' + str(precip_mm) + ' mm' + '<br>Risco de incidente: ' + risco,
                
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
    height=590  # Defina a altura desejada aqui
)
st.plotly_chart(fig_mapa, use_container_width=True)
# ====================== Mapa de risco Incidente =======================

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

# Layout do aplicativo
col1, col2 = st.columns([1, 1])
col3, col4 = st.columns([1, 1])
   

with col1:
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
        fig_Precip = px.bar(df_plot, x='Dia', y='Precipitação (mm)', title=f'Precipitação por dia no bairro {selected_bairro}')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig_Precip, use_container_width=True)

with col2:
    # Calcular a precipitação total por bairro
    bairros['Precipitação Total'] = bairros.iloc[:, 1:-1].sum(axis=1)
    # Selecionar os 10 bairros com maior precipitação total
    top_5_bairros = bairros.nlargest(5, 'Precipitação Total')
    # Criar o gráfico de pizza com Plotly Express
    fig_pizza = px.pie(top_5_bairros, names='Bairro', values='Precipitação Total', title='Bairros com Maior Precipitação Total no Mês')
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_pizza, use_container_width=True)

with col3:
    # Gráfico de linha com dados aleatórios
    dados_aleatorios_linha = np.random.rand(len(df_bairros))
    fig_linha = go.Figure(data=go.Scatter(x=df_bairros['Bairro'], y=dados_aleatorios_linha))
    st.plotly_chart(fig_linha, use_container_width=True)

with col4:
    # Gráfico de barras com dados aleatórios
    dados_aleatorios_barra = np.random.rand(len(df_bairros))
    fig_barra = go.Figure(data=[go.Bar(x=df_bairros['Bairro'], y=dados_aleatorios_barra, marker_color='#FF4B4B')])
    st.plotly_chart(fig_barra, use_container_width=True)





# ====================== graficos ============================================================================




# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Nimbus Tech - © 2024")
