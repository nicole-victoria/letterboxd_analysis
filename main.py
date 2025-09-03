#importações
import streamlit as st
import graficos as gf
import pandas as pd
from dataset import df
import utils
import graficos as gf
from graficos import grafico_generos, grafico_estudios, grafico_top_idiomas, grafico_notas_idiomas

# Título da página
st.set_page_config(page_title="Análise de Filmes", layout="wide")

# Definicão dos estilos principais do Dashboard
st.markdown("""
    <style>
        .stApp {
            background-color: #202830;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 20px 0;
        }
        .header img {
            height: 70px;
        }
        .header h1 {
            color: #ffffff;
            font-family: 'Arial', sans-serif;
            font-size: 36px;
            margin: 0;
        }
        div[data-testid="stMetricValue"] {
            font-size: 50px;
            font-weight: bold;
            color:#d2700e
        }
            
        div[data-testid="stMetricLabel"] {
            font-size: 30px;
            font-weight: bold;
            color:#d2700e
        }

    </style>

    <div class="header">
        <img src="https://a.ltrbxd.com/logos/letterboxd-decal-dots-pos-rgb-500px.png" alt="Logo">
        <h1>Dashboard de análise de filmes avaliados no Letterboxd</h1>
    </div>
""", unsafe_allow_html=True)

# Definição do sidebar de filtros
st.sidebar.title('Filtros (Visão Geral)')
with st.sidebar.expander('Gêneros'):
    generos_escolhidos = st.multiselect(
        'Selecione os Gêneros',
        sorted(utils.generos),
        sorted(utils.generos)
    )
with st.sidebar.expander('Idiomas Originais'):
    idiomas_escolhidos = st.multiselect(
        'Selecione os Idiomas',
        sorted(utils.idiomas),
        sorted(utils.idiomas)
    )

# DataFrame filtrado
df_filtrado = df[
    df["Genres"].apply(lambda lista: set(lista).issubset(set(generos_escolhidos))) &
    df['Original_language'].apply(lambda idioma: idioma in idiomas_escolhidos)
]

#definição de 3 abas
aba1, aba2, aba3 = st.tabs(['Visão Geral', 'Diretores', 'Rankings'])

with aba1:
    a, met, hist, b = st.columns([1, 2, 6, 1]) 
    with met:
        st.markdown("""
                <div 
                    style='height: 150px;display:flex; align-items:center; justify-content: center;'>  
                </div>""", 
        unsafe_allow_html=True)
        st.metric('Nota Média', f"{df['Average_rating'].mean():.2f}")
    with hist:
        st.plotly_chart(gf.grafico_hist(df_filtrado['Average_rating'], 'Distribuição das avaliações', "Notas média"), use_container_width=True)
    st.write("")


    # Gráfico 2 com os 10 filmes com maior média de avaliação
    top10 = df_filtrado[["Film_title", "Average_rating"]].sort_values("Average_rating", ascending=False).head(10) #criação do DataFrame
    grafico6 = gf.grafico_barras(top10['Average_rating'], top10['Film_title'], 
                                nome_x='Nota Média', nome_y='Título do filme', 
                                rotulo=True, color=['#08a110'], titulo='Top 10 filmes(média de avaliação)')

    # Gráfico 3 com os 10 filmes com menor média de avaliação
    bottom10 = df_filtrado[["Film_title", "Average_rating"]].sort_values("Average_rating", ascending=False).tail(10)
    grafico7 = gf.grafico_barras(x=bottom10['Average_rating'], y=bottom10['Film_title'], 
                                nome_x='Nota Média', nome_y='Título do filme', 
                                rotulo=True, color=['#ba170b'], titulo='Bottom 10 filmes(média de avaliação)')
    
    col1, c, col2 = st.columns([4.75, 0.5, 4.75]) # coloca os dois gráficos lado a lado
    with col1:
        st.plotly_chart(grafico6, use_container_width=True)
    with col2:
        st.plotly_chart(grafico7, use_container_width=True)
    st.write("")

    d, col3, col4 = st.columns([0.5, 2, 7.5]) #divisão dos espaços para o button radio e o gráfico
    with col3:
        st.markdown("""
                <style>
                    div[role="radiogroup"] {
                        background-color: #e3f2fd;
                        padding: 10px;
                        border-radius: 8px;
                    }
                </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
                <div 
                    style=' height: 80px; display:flex; align-items:center;'>
                        <h4 style='color: white; margin-top: 110px; font-size:18px'> Escolha uma métrica:</h4>
                </div>""", 
        unsafe_allow_html=True)
        opcao = st.radio("", ['Watches', 'Likes', 'Fans', 'Engagement'])
        
    df_top25_filmes = df_filtrado.sort_values(opcao, ascending=False).head(25) #definição do DataFrame
    grafico4 = gf.grafico_barras( x=df_top25_filmes[opcao],y=df_top25_filmes['Film_title'],
                                titulo=f'Top 25 Filmes por {opcao}',nome_y='Título', nome_x=opcao, ) #definição do gráfio
    with col4:
        st.plotly_chart(grafico4, use_container_width=True)
    st.write("")


with aba2:
    col10, i, col11 = st.columns([4.75, 0.5, 4.75]) #coloca as tabelas lado a lado
    with col10:
        st.markdown(
        "<h4 style='color: white; text-align: center;font-size:20px'>Top 15 Diretores com Mais Filmes</h3>",
        unsafe_allow_html=True)
        st.dataframe(utils.top15_diretoresFilmes.reset_index(drop=True).style
            .format({'Nota_media': '{:.2f}'})
            .highlight_max(subset='quantidade_filmes', color='lightgreen')
            .highlight_max(subset='Nota_media', color='lightblue')
            .highlight_max(subset='Assistido', color='lightpink'), use_container_width=True)
    with col11:
        st.markdown(
        "<h4 style='color: white; text-align: center; font-size:20px'>Top 15 Diretores Mais Assistidos</h3>",
        unsafe_allow_html=True)
        st.dataframe(utils.top15_diretoresPopular.reset_index(drop=True).style
            .format({'Nota_media': '{:.2f}'})
            .highlight_max(subset='quantidade_filmes', color='lightgreen')
            .highlight_max(subset='Nota_media', color='lightblue')
            .highlight_max(subset='Assistido', color='lightpink'), use_container_width=True)
with aba3:
    col5, e, col6 = st.columns([4.75, 0.5, 4.75]) #coloca os dois gráficos lado a lado
    with col5:
        st.plotly_chart(grafico_generos, use_container_width=True)
        st.plotly_chart(grafico_top_idiomas, use_container_width=True)
    with col6:
        st.plotly_chart(grafico_estudios, use_container_width=True)
        st.plotly_chart(grafico_notas_idiomas, use_container_width=True)
    st.write("")
