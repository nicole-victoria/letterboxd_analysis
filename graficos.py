#importacoes
import plotly.express as px
import pandas as pd 
from dataset import df
from utils import top5_idiomas, df_top10_idiomas, top_10_estudios, top_10_generos

#definicao da paleta de cores do dashboard
paleta = ["#d2700e", '#00e054', '#40bcf4', "#7013A9", "#ce13c8", "#126432", "#202830", "#0facaf"]

# funcao que cria o gráfico de barras   
def grafico_barras(x, y, titulo, nome_x='Eixo X', nome_y='Eixo Y', legenda=None, barmode='group', rotulo=False, color= paleta):
    df_para_plot = pd.DataFrame({nome_x: x, nome_y: y})
    df_para_plot.sort_values(by=nome_x, ascending=False, inplace=True)

    # Adiciona rótulo apenas se especificado na chamada de função
    texto = df_para_plot[nome_x] if rotulo else None

    #criação do gráfico em casos com e sem legenda
    if legenda is not None:
        df_para_plot["Legenda"] = legenda
        fig = px.bar(
            df_para_plot,
            x=nome_x,
            y=nome_y,
            color='Legenda',
            title=titulo,
            barmode=barmode,
            color_discrete_sequence=color,
            text=texto
        )
    else:
        fig = px.bar(
            df_para_plot,
            x=nome_x,
            y=nome_y,
            title=titulo,
            color_discrete_sequence=color,
            text=texto
        )

    # configurações visuais adicionais
    fig.update_layout(
        title={'x':0.5, 
            'xanchor': 'center', 
            'font': {
            'size': 18,           # <-- aumenta o tamanho do título
            'color':' #ffffff',   # opcional: cor do título
            'family': 'Arial'     # opcional: fonte do título
        }},
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    #configurações adicionar quando houver rótulo
    if rotulo:
        fig.update_traces(
            textposition='inside',
            textfont_size=12,
            textfont_color='white',
            texttemplate='%{text:.2f}'
        )
    
    return fig #retorna a figura criada


#função para o gráfico de pizza
def grafico_pizza(x, y, titulo):
    df_para_plot = pd.DataFrame({'Eixo X': x, 'Eixo Y': y})

    #criação do gráfico
    fig = px.pie(df_para_plot, names='Eixo X', values='Eixo Y', title=titulo, color='Eixo X', 
                 color_discrete_sequence=paleta)
    
    #configurações visuais adicionais
    fig.update_layout(
        title={'x':0.5, 
            'xanchor': 'center', 
            'font': {
            'size': 18,          
            'color': '#ffffff',   
            'family': 'Arial'     
        }},
        legend=dict(
            x=0.8,
            y=0.5,
            xanchor='left',
            yanchor='middle',
            font=dict(
            color="white",  # muda a cor da legenda
            size=14)
        ),
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', 
    )

    fig.update_traces(
    textinfo='percent',
    textfont=dict(size=14, color='white'),
    pull=[0.05, 0, 0.05, 0, 0],
    )

    return fig #retorna a figura criada


#função do gráfico de histograma
def grafico_hist(x, titulo, nome_x):
    df_para_plot = pd.DataFrame({nome_x: x})
    #criação do gráfico
    fig  =px.histogram(df_para_plot, x=nome_x, nbins=20, title=titulo, color_discrete_sequence= paleta)

    #configurações visuais adicionais
    fig.update_layout(
        title={'x':0.5, 
            'xanchor': 'center', 
            'font': {
            'size': 18,           # <-- aumenta o tamanho do título
            'color': '#ffffff',   # opcional: cor do título
            'family': 'Arial'     # opcional: fonte do título
        }},
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
    )
    fig.update_traces(
    marker_line_color="white",
    marker_line_width=0.5
    )

    return fig #retorna a figura criada



# "Instâncias dos gráficos"
#----------------------

# Criação do gráfico dos 10 gêneros mais assistidos
grafico_generos = grafico_barras(x=top_10_generos['Watches'], y=top_10_generos['Genres'],
                                titulo= 'Top 10 gêneros mais assistidos', nome_y='Streams', nome_x='Gênero')

# Criação do gráfico dos 10 estúdios mais assistidos
grafico_estudios = grafico_barras(x=top_10_estudios['Watches'], y=top_10_estudios['Studios'],
        titulo= 'Top 10 estúdios com maiores audiências', nome_y='Streams', nome_x='Estúdio')

# Criação do gráfico dos 5 idiomas originais mais populares
grafico_top_idiomas = grafico_pizza(x=top5_idiomas.index, y=top5_idiomas.values,
        titulo='Top 5 Idiomas Originais mais populares' )

# Criação do gráfico dos 10 idiomas populares e nota Média
grafico_notas_idiomas = grafico_barras(
        x=df_top10_idiomas['nota_media'],
        y=df_top10_idiomas['idioma_original'],
        titulo='Top 10 idiomas Originais mais populares e nota média',
        nome_y='Idioma Original',
        nome_x='Nota Média',
        rotulo=True
    )