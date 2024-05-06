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
def profilling():
    st.write('Inserir o Dicionário aqui talvez ??')
    
    st.subheader("Data Profilling")
    
    with st.expander('Proffiling De Dados'):
            
            # Carregar o conteúdo do arquivo HTML
        with open("data/eda.html", "r") as file:
                pagina_html = file.read()

                # Exibir o conteúdo HTML
        st.components.v1.html(pagina_html, height = 700, scrolling=True)

def parallel_cateogries():

    st.subheader('Categorias Paralelas')
    col1,col2=st.columns([.3,.7])
    with col1:
        nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                        'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
        colunas= col1.multiselect('Colunas',options=nomes_colunas)

        if len(colunas) >=2:
                grafico= px.parallel_categories(dfp[colunas])
                button_input= st.button('Gerar Gráfico')
                pronto = st.success('Gráfico Pronto Para Ser Gerado', icon='✅')
                if button_input:
                        with st.empty():
                             pronto.empty()
                        with col2:
                                col2.plotly_chart(grafico,use_container_width=True)         
        if len(colunas) <=1:
            st.error('Deve Haver no Mínimo Duas Colunas', icon='🚨')                    
                            
                    
    

def histograms():
    st.subheader('Histogramas')
    col1,col2=st.columns([.3,.7])
    with col1:
          nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                       'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
          colunas=col1.selectbox('Colunas', options=nomes_colunas, key='histograma')
          grafico= px.histogram(dfp,x=colunas, color='HeartDiseaseorAttack')
    with col2:
        col2.plotly_chart(grafico,use_container_width=True)
def boxplot():
    st.subheader("Gráfico de Caixa - Boxplot")
    col1,col2= st.columns([.3,.7])
    with col1:
          nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                       'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
          colunas=col1.selectbox('Colunas', options=nomes_colunas, key='boxplot')
          grafico= px.box(dfp, x=colunas)
    with col2:
        col2.plotly_chart(grafico,use_container_width=True)
def buildPage():
    profilling()
    parallel_cateogries()
    histograms()
    boxplot()
    scatterPlot()

if __name__ == '__main__':
    buildPage()