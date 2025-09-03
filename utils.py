
# Importações
import pandas as pd
from dataset import df

# Listas de gêneros e idiomas
generos = sorted({g for generos in df["Genres"] for g in generos})
idiomas = df['Original_language'].unique()

# Criação do DataFrame dos 10 gêneros mais assistidos
df_generos = df.explode('Genres').groupby('Genres', as_index=False)['Watches'].sum()
top_10_generos = df_generos.sort_values('Watches', ascending=False).head(10)

# Criação do DataFrame dos 10 estúdios mais assistidos
df_estudios = df.explode('Studios').groupby('Studios', as_index=False)['Watches'].sum()
top_10_estudios = df_estudios.sort_values('Watches', ascending=False).head(10)

# Criação do DataFrame dos 5 idiomas originais mais populares
top5_idiomas =df["Original_language"].value_counts().nlargest(5)

# DataFrame com os 10 idiomas mais populares
df_top10_idiomas = (
        df[df['Original_language'].isin(df['Original_language'].value_counts().nlargest(10).index)]
        .groupby('Original_language')['Average_rating'].mean()
        .reset_index(name='nota_media')
        .rename(columns={'Original_language': 'idioma_original'})
        .sort_values(by='nota_media', ascending=False)
    ) 

#tabela dos 15 diretores com mais filmes
top15_diretoresFilmes = (
        df[df['Director'].isin(df['Director'].value_counts().nlargest(20).index)]
        .groupby('Director')
        .agg(quantidade_filmes=('Director', 'count'),
            Nota_media=('Average_rating', 'mean'),
            Assistido=('Watches', 'sum'))
        .reset_index()
        .sort_values(by='quantidade_filmes', ascending=False)
    )

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