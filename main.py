#importações
import streamlit as st
import graficos as gf
import pandas as pd
import ast
import kagglehub

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
        .element-container .stPlotlyChart {
        border-radius: 20px;
        overflow: hidden;
        }
        

    </style>

    <div class="header">
        <img src="https://a.ltrbxd.com/logos/letterboxd-decal-dots-pos-rgb-500px.png" alt="Logo">
        <h1>Dashboard de análise de filmes avaliados no Letterboxd</h1>
    </div>
""", unsafe_allow_html=True)

#leitura do Dataset
path = kagglehub.dataset_download("sahilislam007/letterbox-movie-classification-dataset")
df = pd.read_csv(path+'/Letterbox Movie Classification Dataset.csv')


#Gráfico 1 com a distribuição das notas
grafico1 = gf.grafico_hist(df['Average_rating'], 'Distribuição das avaliações', "Notas média")
a, centro, b = st.columns([1.5, 7, 1.5])  
with centro:
    st.plotly_chart(grafico1, use_container_width=True)
st.write("")


# Gráfico 2 com os 10 filmes com maior média de avaliação
top10 = df[["Film_title", "Average_rating"]].sort_values("Average_rating", ascending=False).head(10) #criação do DataFrame
grafico6 = gf.grafico_barras(top10['Average_rating'], top10['Film_title'], 
                             nome_x='Nota Média', nome_y='Título do filme', 
                             rotulo=True, color=['#08a110'], titulo='Top 10 filmes(média de avaliação)')

# Gráfico 3 com os 10 filmescom menor média de avaliação
bottom10 = df[["Film_title", "Average_rating"]].sort_values("Average_rating", ascending=False).tail(10)
grafico7 = gf.grafico_barras(x=bottom10['Average_rating'], y=bottom10['Film_title'], 
                             nome_x='Nota Média', nome_y='Título do filme', 
                             rotulo=True, color=['#ba170b'], titulo='Bottom 10 filmes(média de avaliação)')
col1, c, col2 = st.columns([4.75, 0.5, 4.75]) # coloca os dois gráficos lado a lado
with col1:
    st.plotly_chart(grafico6, use_container_width=True)
with col2:
    st.plotly_chart(grafico7, use_container_width=True)
st.write("")

# Gráfico 4 mutável
df['Engajamento'] = (3 * df['Watches'] + 2 * df['Likes'] + 1 * df['Fans'])#cálculo de um índice total de engajamento
df_engajados=df[['Film_title', 'Watches', 'Likes', 'Fans', 'Engajamento']]# criação do DataFrame de engajamento
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
    opcao = st.radio("", ['Watches', 'Likes', 'Fans', 'Engajamento'])

df_top25_filmes = df_engajados.sort_values(opcao, ascending=False).head(25) #definição do DataFrame
grafico4 = gf.grafico_barras( x=df_top25_filmes[opcao],y=df_top25_filmes['Film_title'],
                             titulo=f'Top 25 Filmes por {opcao}',nome_y='Título', nome_x=opcao, ) #definição do gráfio
with col4:
    st.plotly_chart(grafico4, use_container_width=True)
st.write("")


#gráfico 5 com os 10 gêneros mais assistidos
df_generos = (df[['Genres', 'Watches']].dropna(subset=['Genres'])
              .query("Genres.str.lower() != 'unknown'", engine='python').copy()
)
df_generos['Genres'] = df_generos['Genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x) #transforma o tipo da coluna em lista
df_generos = df_generos.explode('Genres').groupby('Genres', as_index=False)['Watches'].sum()
top_10_generos = df_generos.sort_values('Watches', ascending=False).head(10)
grafico5 = gf.grafico_barras(x=top_10_generos['Watches'], y=top_10_generos['Genres'],
                             titulo= 'Top 10 gêneros mais assistidos', nome_y='Streams', nome_x='Gênero') #definição do gráfico

#gráfico 6 com os 10 estúdios com maiores audiências 
df_estudios = (df[['Studios', 'Watches']].dropna(subset=['Studios'])
              .query("Studios.str.lower() != 'unknown'", engine='python').copy()
)
df_estudios['Studios'] = df_estudios['Studios'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)#transforma o tipo da coluna em lista
df_estudios = df_estudios.explode('Studios').groupby('Studios', as_index=False)['Watches'].sum()
top_10_estudios = df_estudios.sort_values('Watches', ascending=False).head(10)
grafico6 = gf.grafico_barras(x=top_10_estudios['Watches'], y=top_10_estudios['Studios'],
    titulo= 'Top 10 estúdios com maiores audiências', nome_y='Streams', nome_x='Estúdio')

col5, e, col6 = st.columns([4.75, 0.5, 4.75]) #coloca os dois gráficos lado a lado
with col5:
    st.plotly_chart(grafico5, use_container_width=True)
with col6:
    st.plotly_chart(grafico6, use_container_width=True)
st.write("")



# grafico 7 com os 5 idiomas mais populares
top5_idiomas =df["Original_language"].value_counts().nlargest(5)
grafico7 = gf.grafico_pizza(x=top5_idiomas.index, y=top5_idiomas.values,
    titulo='Top 5 Idiomas Originais mais populares' )# definicção do gráfico

# gráfico 8 com os 10 idiomas populares e nota Média
df_top10_idiomas = (
    df[df['Original_language'].isin(df['Original_language'].value_counts().nlargest(10).index)]
    .groupby('Original_language')['Average_rating'].mean()
    .reset_index(name='nota_media')
    .rename(columns={'Original_language': 'idioma_original'})
    .sort_values(by='nota_media', ascending=False)
)  #definicção do DataFrame
grafico8 = gf.grafico_barras(
    x=df_top10_idiomas['nota_media'],
    y=df_top10_idiomas['idioma_original'],
    titulo='Top 10 idiomas Originais mais populares e nota média',
    nome_y='Idioma Original',
    nome_x='Nota Média',
    rotulo=True
) #definição do gráfico
col7, f, col8 = st.columns([4.75, 0.5, 4.75]) #coloca os gráfico lado a lado
with col7:
    st.plotly_chart(grafico7, use_container_width=True)
with col8:
    st.plotly_chart(grafico8, use_container_width=True)
st.write("")



#gráfico 9 dos filmes favoritos + gêneros
df_filmes_generos = (
    df[['Film_title', 'Fans', 'Genres', 'Director']].dropna(subset=['Genres'])
    .query("Genres.str.lower() != 'unknown'", engine='python').copy()
)
df_filmes_generos['Genres'] = df_filmes_generos['Genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df_filmes_generos['Genero_principal'] = df_filmes_generos['Genres'].apply(lambda x: x[0] if isinstance(x, list) and x else None) #pega o gênero principal de cada filme
df_filmes_generos["Film_Director"] = df_filmes_generos["Film_title"] + " (" + df_filmes_generos["Director"] + ")" #criação da nova coluna 
top30_filmes_generos = df_filmes_generos[['Film_Director', 'Genero_principal', 'Fans']].sort_values(by='Fans', ascending=False).head(30)
grafico9 = gf.grafico_barras(x=top30_filmes_generos['Fans'], y=top30_filmes_generos['Film_Director'],
    titulo='Top 20 filmes(diretor) favoritos e seus gêneros',nome_y='Número de fans',nome_x='Título',
    legenda=top30_filmes_generos['Genero_principal']) #definição do gráfico
g, col9, h = st.columns([1, 8, 1])
with col9:
    st.plotly_chart(grafico9, use_container_width=True)
st.write("")

#tabela dos 15 diretores com mais filmes
top15_diretoresFilmes = (
    df[df['Director'].isin(df['Director'].value_counts().nlargest(20).index)]
    .groupby('Director')
    .agg(quantidade_filmes=('Director', 'count'),
         Nota_media=('Average_rating', 'mean'),
         Assistido=('Watches', 'sum'))
    .reset_index()
    .sort_values(by='quantidade_filmes', ascending=False)
)#criação do DataFrame com os 15 com mais filmes

#tabela dos 15 diretores mais assistidos
top15_diretoresPopular = (
    df[df['Director'].isin(df.groupby(["Director"])["Watches"].sum().nlargest(15).index)]
    .groupby('Director')
    .agg(quantidade_filmes=('Director', 'count'),
         Nota_media=('Average_rating', 'mean'),
         Assistido=('Watches', 'sum'))
    .reset_index()
    .sort_values(by='Assistido', ascending=False)
)#criação do DataFrame com os 15 com mais filmes

col10, i, col11 = st.columns([4.75, 0.5, 4.75]) #coloca as tabelas lado a lado
with col10:
    st.markdown(
    "<h4 style='color: white; text-align: center;font-size:20px'>Top 15 Diretores com Mais Filmes</h3>",
    unsafe_allow_html=True)
    st.dataframe(top15_diretoresFilmes.reset_index(drop=True).style
        .format({'Nota_media': '{:.2f}'})
        .highlight_max(subset='quantidade_filmes', color='lightgreen')
        .highlight_max(subset='Nota_media', color='lightblue')
        .highlight_max(subset='Assistido', color='lightpink'), use_container_width=True)
with col11:
    st.markdown(
    "<h4 style='color: white; text-align: center; font-size:20px'>Top 15 Diretores Mais Assistidos</h3>",
    unsafe_allow_html=True)
    st.dataframe(top15_diretoresPopular.reset_index(drop=True).style
        .format({'Nota_media': '{:.2f}'})
        .highlight_max(subset='quantidade_filmes', color='lightgreen')
        .highlight_max(subset='Nota_media', color='lightblue')
        .highlight_max(subset='Assistido', color='lightpink'), use_container_width=True)
    