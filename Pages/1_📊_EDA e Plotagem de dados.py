import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/heart_disease.csv')
dfp = pd.read_parquet('data/heart_disease.parquet')

st.title('Análise exploratória dos dados e Plotagens')

def scatterPlot():
    def readDataset():
        dataset = pd.read_csv("data/heart_disease.csv")
        return dataset
    
    # Construção da tela
    st.subheader('Scatter Plot')
    dataset = readDataset()

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox(
            'Selecione uma coluna para o eixo X',
            (dataset.columns),
            placeholder = 'Escolha a coluna desejada...'
        )

        with col2:
            y_axis = st.selectbox(
            'Selecione uma coluna para o eixo Y',
            (dataset.columns),
            placeholder = 'Escolha a coluna desejada...'
        )
            
        plot = st.button('Plotar gráfico')
        
        if plot:
            plot = px.scatter(data_frame=dataset, x=dataset[x_axis], y=dataset[y_axis], trendline="ols")
            st.plotly_chart(plot)


def buildPage():
    scatterPlot()

if __name__ == '__main__':
    buildPage()


    