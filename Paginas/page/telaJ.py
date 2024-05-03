import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('data/heart_disease.csv')
dfp = pd.read_parquet('data/heart_disease.parquet')
def telaJ():
    
    st.title('Profilling de Dados e Plotagem de Gráficos')
    

    st.write('Inserir o Dicionário aqui talvez ??')
    
    
    st.subheader("Data Profilling")
    
    with st.expander('Proffiling De Dados'):

        # Carregar o conteúdo do arquivo HTML
        with open("data/eda.html", "r") as file:
            pagina_html = file.read()

            # Exibir o conteúdo HTML
        st.components.v1.html(pagina_html, height = 700, scrolling=True)

    st.subheader('Categorias Paralelas')
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
    