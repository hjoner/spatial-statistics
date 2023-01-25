import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import streamlit as st
import pydeck as pdk
import json
import datetime

from dateutil import parser

from icone import atribui_icone
from cor import atribui_cor, atribui_cor_compara
from sjoin import contagem #, contagem2

st.set_page_config(layout="wide")

st.sidebar.title("MAT02040 - ESTATÍSTICA ESPACIAL")
st.sidebar.info(
    """
   Professora: Márcia Helena Barbian
    """
)

st.sidebar.title("Avaliação 1")
st.sidebar.info(
    """
    Aluno: Henrique Joner \n
    Cartão: 00300659 \n
    Repositório: https://github.com/hjoner/MAT02040
    """
)

@st.cache
def carregar_dados():
    df = pd.read_csv(r"Traffic_Crashes_10000.csv")

    return df


@st.cache
def contar(df,gdf):
    x = contagem(df, gdf)
    return x


def app():

    
    st.markdown("<h1 style='text-align: center; color: black;'>Acidentes de Trânsito em Chicago</h1>", unsafe_allow_html=True)
    st.markdown(
    """ Painel de Seleção
    """)
    
    
    # Aplicação de Filtros
    col1, col2, col3 = st.columns([1,1,1])
    col4, col5, col6 = st.columns([2,2,2])

    valor = st.slider('Faixa Horária:', 0, 23, (0, 23))
    inverso = st.checkbox('Inverter Faixa Horária')
    if inverso:
        intervalo_0 = 0
        intervalo_1 = valor[0]
        intervalo_2 = valor[1]
        intervalo_24 = 24
    
    else:
        intervalo_1 = valor[0]
        intervalo_2 = valor[1]

    with col1:
        linhas = st.number_input('Limite de Observações:', value = 100, step = 1)

    with col4:
        dt_inicio = st.date_input(
        "Data Início",
        datetime.date(2020, 1, 1))
        dt_inicio = pd.Timestamp(dt_inicio)
        
    
    with col5:
        dt_fim = st.date_input(
        "Data Fim",
        datetime.date(2022, 12, 31))
        dt_fim = pd.Timestamp(dt_fim)


    
    linhas = int(linhas)
   
    df  = carregar_dados()
    st.write(df.shape)
    df = df.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lng'})
    df.columns = df.columns.str.lower()
    df.crash_date = pd.to_datetime(df.crash_date, format='%m/%d/%Y %I:%M:%S %p')
    
    df = df[(df['crash_date'] > dt_inicio) & (df['crash_date'] < dt_fim) ].reset_index(drop=True)
    df = df.fillna(0)


    
    injury = list(df['most_severe_injury'].unique())
    
    with col2:
        options = st.multiselect('Selecione o nível de gravidade', injury, injury[0])
    df = df[df['most_severe_injury'].isin(options)].reset_index(drop=True)

    iluminacao = list(df['lighting_condition'].unique())
    with col3:
        options2 = st.multiselect('Selecione o nível de iluminação', iluminacao, iluminacao[0])
    df = df[df['lighting_condition'].isin(options2)].reset_index(drop=True)

    if inverso:
        df = df[(df['crash_hour'] > intervalo_2)  |  (df['crash_hour'] < intervalo_1)].reset_index(drop=True)
 
    else:
        df = df[(df['crash_hour'] > intervalo_1)  &  (df['crash_hour'] < intervalo_2)].reset_index(drop=True)
    
    with col6:
        options3 = st.multiselect('Selecione a camada', ['Pontos', 'Hexagonos', 'Bairros', 'Setores'], ['Pontos'])

    # Atribui o icone de acordo com cada classe.
    df = df.reset_index(drop = True)
    df = df[:linhas].reset_index(drop=True)
    df = atribui_icone(df)



    # Características das camadas
    hexlayer = pdk.Layer(
        'HexagonLayer',
        df,
        get_position=['lng', 'lat'],
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,                 
        coverage=0.99)
    
    icon_layer = pdk.Layer(
    type="IconLayer",
    data=df,
    get_icon="icone",
    get_size=5,
    size_scale=5, 
    get_position=["lng","lat"],
    pickable=True,
)
    # 3D Switch
    col7, col8, col9, col10, col11, col12 = st.columns([3,3,3,3,3,3])
    with col7:
        st.write('Dimensão:')
        b1 = st.button('3D')
    elevacao = "0"
    with col8:
        multiplicador = st.number_input('Elevação:', value = 5, step = 1)
    if b1:
        elevacao = "properties.fatos * %s" % multiplicador
        
    
  
    # Contagem de fatos por polígono.
    if 'Setores' in options3:
        precincts = gpd.read_file("Precincts.geojson")
        precincts = contar(df, precincts)

        precincts = atribui_cor(precincts)
        precincts = json.loads(precincts.to_json())
        geojson = pdk.Layer(
        "GeoJsonLayer",
        precincts,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation= elevacao,
        get_fill_color="[properties.cor1, properties.cor2, properties.cor3 ]",

    )


    if 'Bairros' in options3:
        bairros = gpd.read_file("bairros_chicago.geojson")
        bairros = bairros.rename(columns = {'pri_neigh' : 'full_text'})
        bairros = contar(df, bairros)
        bairros = atribui_cor(bairros)
        bairros = json.loads(bairros.to_json())
        geojson_b = pdk.Layer(
        "GeoJsonLayer",
        bairros,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation= elevacao,
        get_fill_color="[properties.cor1, properties.cor2, properties.cor3 ]",
    )
        

   
    # Define o view state inicial
    view_state =  pdk.ViewState(latitude=41.881832, longitude=-87.623177, zoom=10, max_zoom=16, pitch=60, bearing=50)


    # Renderização

    camadas = []
    if 'Pontos' in options3:
        camadas.append(icon_layer)
        hover = "<b>Gravidade</b> {most_severe_injury}"
    if 'Hexagonos' in options3:
        camadas.append(hexlayer)
        hover = "<b>Gravidade:</b> {most_severe_injury}"
    if 'Setores' in options3:
        camadas.append(geojson)
        hover ="<b>Contagem:</b> {fatos}"
    if 'Bairros' in options3:
        camadas.append(geojson_b)
        hover ="<b>Contagem:</b> {fatos}"
    if 'Quadras' in options3:
        camadas.append(geojson_c)
        hover ="<b>Contagem:</b> {fatos}"
    st.pydeck_chart(pdk.Deck(layers=camadas, initial_view_state=view_state, tooltip={"html":hover,"style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }}))
    

    # GRAVIDADE POR HORA
    colunas = list(df['most_severe_injury'].unique())
    colunas.append('Hora')
    d = pd.DataFrame(np.zeros((24, len(colunas))), columns = colunas)
    x = 0
    while x < len(d):
        d['Hora'][x] = x
        x += 1
    colunas.remove('Hora')
    for i in d['Hora']:
        for c in colunas:
            df1 = df[(df['most_severe_injury'] == c) & (df['crash_hour'] == i)]
            d[c][i] = df1.shape[0]
    chart_data = d[colunas]
    st.markdown("<h2 style ='text-align: center; color: black;'>Gravidade por Hora</h2>", unsafe_allow_html=True)
    st.area_chart(chart_data)

    # ILUMINAÇÃO POR HORA
    colunas = list(df['lighting_condition'].unique())
    colunas.append('Hora')
    d = pd.DataFrame(np.zeros((24, len(colunas))), columns = colunas)
    x = 0
    while x < len(d):
        d['Hora'][x] = x
        x += 1
    colunas.remove('Hora')
    for i in d['Hora']:
        for c in colunas:
            df1 = df[(df['lighting_condition'] == c) & (df['crash_hour'] == i)]
            d[c][i] = df1.shape[0]
    chart_data = d[colunas]
    st.markdown("<h2 style='text-align: center; color: black;'>Iluminação por Hora</h2>", unsafe_allow_html=True)
    st.bar_chart(chart_data)

    # FATOS POR DIA DA SEMANA
    colunas = list(df['crash_day_of_week'].unique())
    colunas.append('Hora')
    d = pd.DataFrame(np.zeros((24, len(colunas))), columns = colunas)
    x = 0
    while x < len(d):
        d['Hora'][x] = x
        x += 1
    colunas.remove('Hora')
    for i in d['Hora']:
        for c in colunas:
            df1 = df[(df['crash_day_of_week'] == c) & (df['crash_hour'] == i)]
            d[c][i] = df1.shape[0]
    chart_data = d[colunas]
    st.markdown("<h2 style='text-align: center; color: black;'>Fatos por Dia da Semana</h2>", unsafe_allow_html=True)
    st.bar_chart(chart_data)

    col13, col14, col15 = st.columns([4,4,4])
    with col14:
        b2 = st.button('Comparativo')
    if b2:
        cut = int(len(df) / 2)
        df1 = df[:cut]
        df2 = df[cut:]
        if 'Setores' in options3:
            gdf = gpd.read_file("Precincts.geojson")
            
        else:
            gdf = gpd.read_file("bairros_chicago.geojson")
            gdf = gdf.rename(columns = {'pri_neigh' : 'full_text'})
        df3_ = contar(df1,gdf)
        df1_ = df3_.copy()
        df2_ = contar(df2,gdf)

        gdf2 = df2_
        
        gdf2['fatos'] = (df2_['fatos'] / (df1_['fatos']+0.01)) -1
        gdf2['fatos'] = gdf2['fatos'].fillna(0)
        x = 0
        while x < len(gdf2):
            if gdf2['fatos'][x] > 1:
                gdf2['fatos'][x] = 1
            if gdf2['fatos'][x] < -1:
                gdf2['fatos'][x] = -1
            x +=1 
        if 'Setores' in options3:

            #gdf2 = contar(df, gdf2)

            gdf2 = atribui_cor_compara(gdf2)
            gdf2 = json.loads(gdf2.to_json())
            geojson = pdk.Layer(
            "GeoJsonLayer",
            gdf2,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation= elevacao,
            get_fill_color="[properties.cor1, properties.cor2, properties.cor3 ]",

        )

            st.pydeck_chart(pdk.Deck(layers=geojson, initial_view_state=view_state, tooltip={"html":hover,"style": {
            "backgroundColor": "steelblue",
            "color": "white"
   }}))
        if 'Bairros' in options3:
            gdf2 = atribui_cor_compara(gdf2)
            gdf2 = json.loads(gdf2.to_json())
            geojson = pdk.Layer(
            "GeoJsonLayer",
            gdf2,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation= elevacao,
            get_fill_color="[properties.cor1, properties.cor2, properties.cor3 ]",

        )

            st.pydeck_chart(pdk.Deck(layers=geojson, initial_view_state=view_state, tooltip={"html":hover,"style": {
            "backgroundColor": "steelblue",
            "color": "white"
   }}))

app()
