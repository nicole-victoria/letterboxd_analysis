#Importações
import kagglehub
import pandas as pd
import ast

#leitura do Dataset
path = kagglehub.dataset_download("sahilislam007/letterbox-movie-classification-dataset")
df = pd.read_csv(path+'/Letterbox Movie Classification Dataset.csv')

# Função que transforma colunas de listas para o tipo lista
def transforma_lista(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            return []  
    return x

#  Aplicação da função
df['Genres'] = df['Genres'].apply(transforma_lista)
df['Studios'] = df['Studios'].apply(transforma_lista)

#cálculo de um índice total de engajamento
df['Engagement'] = (3 * df['Watches'] + 2 * df['Likes'] + 1 * df['Fans'])