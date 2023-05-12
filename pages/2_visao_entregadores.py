# libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
from pandas import Timestamp
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Entregadores', page_icon='🚚', layout='wide')

# ========================================================================#
#                             Funções                                    #
# ========================================================================#


def top_delivers(df1, top_esc):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
           .groupby(['City', 'Delivery_person_ID'])
           .mean()
           .sort_values(['City', 'Time_taken(min)'], ascending=top_esc).reset_index())

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux01, df_aux02, df_aux03]
                    ).reset_index(drop=True)

    return df3


def country_maps(df1):

    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                 .groupby(['City', 'Road_traffic_density'])
                 .median()
                 .reset_index())

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

    folium_static(map, width=1024, height=600)


def order_share_by_week(df1):
    df_aux01 = (df1.loc[:, ['ID', 'week_of_year']]
                .groupby('week_of_year')
                .count()
                .reset_index())
    df_aux02 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                .groupby('week_of_year')
                .nunique()
                .reset_index())

    df_aux = pd.merge(df_aux01, df_aux02, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return fig


def order_by_week(df1):
    # criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = (df1.loc[:, ['ID', 'week_of_year']]
              .groupby('week_of_year')
              .count()
              .reset_index())
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig


def traffic_order_city(df1):

    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .count()
                 .reset_index())

    fig = px.scatter(df_aux, x='City', y='Road_traffic_density',
                     size='ID', color='City')
    return fig


def traffic_order_share(df1):

    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
              .groupby('Road_traffic_density')
              .count()
              .reset_index())

    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    return fig


def order_metric(df1):

    cols = ['ID', 'Order_Date']
    # seleção de linhas
    df_aux = (df1.loc[:, cols]
              .groupby('Order_Date')
              .count()
              .reset_index())
    # desenhar o gráfico de barras
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig


def clean_code(df1):
    """Essa função tem a responsabilidade de limpar o dataframe
        Tipos de limpeza:
        1. Remoção de NaN
        2. Mudança do tipo da coluna de dados 
        3. Remoção de espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna do tempo ( remoção da variável de texto)

        Input: Dataframe
        Output: Dataframe  

    """

    # 1. Convertendo a coluna Age de texto para números
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 2. Convertendo a coluna Ratings de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(
        float)

    # 3. Convetendo a coluna order_date de textp para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 4. Convertendo multiple_deliveries de texto para número inteiro
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 5. Removendo os espaços em branco dentro de strings/texto/object
    # df1 = df1.reset_index(drop=true)
    # for i in range(len(df1)):
    # df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

    # 6. Removendo os espaços em branco dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:,
                                                 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # 7. Limpando a coluna de Time Taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(
        lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# ========================================================================#
#                Início da estrutura lógica do código                    #
# ========================================================================#


# import dataset
df = pd.read_csv('dataset/train.csv')
df1 = clean_code(df)

# ===================================================================================#
#                             Barra lateral                                         #
# ===================================================================================#
st.header('Marketplace - Visão Entregadores')

#image_path = r'C:\Users\luanG\Desktop\Comunidade DS\Repos\portfolios_projetos\imagem2.jpg'

image = Image.open('imagem2.jpg')
st.sidebar.image(image, width=220)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.Timestamp(2022, 4, 13).to_pydatetime(),
    min_value=pd.Timestamp(2022, 2, 11),
    max_value=pd.Timestamp(2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ===================================================================================#
#                           Layout do Streamlit                                     #
# ===================================================================================#

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
    with st.container():
        st.title('Overall Metrics')

        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:

            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior de idade', maior_idade)

        with col2:

            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor de idade', menor_idade)

        with col3:

            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)

        with col4:

            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)

    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_avg_ratings_per_deliver = (df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                                          .groupby('Delivery_person_ID')
                                          .mean()
                                          .reset_index())
            st.dataframe(df_avg_ratings_per_deliver)

        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_avg_ratings_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                         .groupby('Road_traffic_density')
                                         .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            # mudança de colunas
            df_avg_ratings_by_traffic.columns = [
                'delivery_mean', 'delivery_std']

            # resetar o index
            df_avg_ratings_by_traffic = df_avg_ratings_by_traffic.reset_index()
            st.dataframe(df_avg_ratings_by_traffic)

            st.markdown('##### Avaliação média por clima')
            df_avg_ratings_by_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                         .groupby('Weatherconditions')
                                         .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            # mudança de colunas
            df_avg_ratings_by_weather.columns = [
                'delivery_mean', 'delivery_std']

            # resetar o index
            df_avg_ratings_by_weather = df_avg_ratings_by_weather.reset_index()
            st.dataframe(df_avg_ratings_by_weather)

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3 = top_delivers(df1, top_esc = False)
            st.dataframe(df3)

        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3 = top_delivers(df1, top_esc = False)
            st.dataframe(df3)
