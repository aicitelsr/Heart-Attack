import streamlit as st
import pandas as pd
df = pd.read_csv('data/heart_disease.csv')
def telaJ():
    
    st.title('Tela Inicial de Julio')
    

    st.dataframe(df.head())
    
    
    st.title("Data Profilling")
        
        # Carregar o conteúdo do arquivo HTML
    with open("data/eda.html", "r") as file:
        pagina_html = file.read()

        # Exibir o conteúdo HTML
    st.components.v1.html(pagina_html, height = 700, scrolling=True)

    