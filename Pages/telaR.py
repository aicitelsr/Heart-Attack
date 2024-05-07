import pandas as pd
import streamlit as st
import plotly.express as px

def telaR():
    # Carregando os dados do CSV
    def lerDataset():
        dataset = pd.read_csv('data/heart_disease.csv')
        return dataset

    st.title('Histogram Plot')
    dataset = lerDataset()

    # Layout com duas colunas
    col1, col2 = st.columns(2)

    # Widget para seleção da coluna A
    with col1:
        colunaA = st.selectbox(
            'Selecione a primeira coluna binária',
            dataset.columns,
            key='colunaA'
        )

    # Widget para seleção da coluna B
    with col2:
        colunaB = st.selectbox(
            'Selecione a segunda coluna binária',
            dataset.columns,
            key='colunaB'
        )

    # Botão para plotar o gráfico
    plot_button = st.button('Plotar gráfico')

    if plot_button:
        # Convertendo as colunas para tipo booleano
        colunaA_bool = dataset[colunaA].astype(bool)
        colunaB_bool = dataset[colunaB].astype(bool)

        # Calculando a interseção entre as duas colunas
        intersecao = colunaA_bool & colunaB_bool

        # Criando o DataFrame para o Plotly Express
        df_plot = pd.DataFrame({'Interseção': intersecao})

        # Plotando o gráfico de barras agrupadas com Plotly Express
        fig = px.histogram(df_plot, x='Interseção', title='Contagem da Interseção entre ' + colunaA + ' e ' + colunaB)
        st.plotly_chart(fig)


telaR()

