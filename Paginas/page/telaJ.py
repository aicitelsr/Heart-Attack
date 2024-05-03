import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('data/heart_disease.csv')
dfp = pd.read_parquet('data/heart_disease.parquet')
def telaJ():
    
    st.title('Tela Inicial de Julio')
    

    st.dataframe(df.head())
    
    
    st.title("Data Profilling")
        
        # Carregar o conteúdo do arquivo HTML
    with open("data/eda.html", "r") as file:
        pagina_html = file.read()

        # Exibir o conteúdo HTML
    st.components.v1.html(pagina_html, height = 700, scrolling=True)

    st.title('Categorias Paralelas')
    nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                       'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
    colunas= st.multiselect('Colunas',options=nomes_colunas)
    if len(colunas) > 4:
        st.error('Por Favor Insira ')
    else:
        if len(colunas) >=2:
            grafico= px.parallel_categories(dfp[colunas])
            button_input= st.button('Gerar Gráfico')
            if button_input:
                st.plotly_chart(grafico)
    