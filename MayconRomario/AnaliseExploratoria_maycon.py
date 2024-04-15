import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Função para carregar os dados
def carregar_dados(caminho_dados):
    dados = pd.read_csv(caminho_dados)
    return dados


def main():
    st.title('Analise exploratoria dos dados com streamilit')

    # carregar os dados
    caminho_dados = 'dataset/heart_disease_health_indicators_BRFSS2015.csv'
    dados = carregar_dados(caminho_dados)

    # Visualização das primeiras linhas do DataFrame
    st.subheader('visualização das primeiras linhas do dataframe:')
    st.write(dados.head())

    # resumo estatistico
    st.subheader('Resumo estatistico do dataframe:')
    st.write(dados.describe())

    # histograma
    st.subheader('Histograma:')
    colunas_numericas = dados.select_dtypes(include='number').columns
    for coluna in colunas_numericas:
        plt.hist(dados[coluna])
        st.pyplot()

    # matriz de correlaçao
    st.subheader('Matriz de correlação:')
    matriz_correlação = dados.corr()
    sns.heatmap(matriz_correlação, annot=True)
    st.pyplot()

if __name__ == "__main__":
    main()