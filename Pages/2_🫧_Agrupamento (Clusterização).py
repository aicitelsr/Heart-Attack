import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from utils import readDataframe_parquet
#from PIL import Image
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

st.title('Clusterização K-means e K-modes')
with st.expander('Notas'):
    st.write('Através do método do cotovelo e silhueta foi definido que o melhor número de clusters é 3.\nComo é possível observar há uma suavização da curva no valor de K=3, isso indica que a adição de mais clusters não terá uma melgoria significativa.')
    col1,col2= st.columns(2)
    with col1:
        st.image('data\cotovelo_kmodes.png', caption='Cotovelo do KModes',use_column_width=True)
    with col2:
        st.image('data\cotovelo_kmeans.png', caption='Cotovelo do KMeans',use_column_width=True)
dfp= readDataframe_parquet()
dfp_c = pd.read_parquet('data\clusters_kmodes.parquet')
dfp_c2= pd.read_parquet('data\clusters_kmeans.parquet')
dfp_c= dfp_c.rename(columns={'Cluster':'Clusters'})
dfp_c['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack']
dfp_c2['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack']

def labels(df):
    problema = {0:'Sem Problemas Cardíacos',1:'Com Problemas Cardíacos'}
    df['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack'].replace(problema)

    grupos= {0:'Grupo 0',1:'Grupo 1', 2:'Grupo 2'}
    df['Clusters']= df['Clusters'].replace(grupos)

    fumante = {0:'Não Fuma',1:'Fuma'}
    df['Smoker'] = df['Smoker'].replace(fumante)
    
    atividade_f={0:'Não Pratica Ativades Físicas',1:'Pratica Atividades Físicas'}
    df['PhysActivity'] = df['PhysActivity'].replace(atividade_f)

    sexo = {0:'Mulher',1:'Homem'}
    df['Sex'] = df['Sex'].replace(sexo)

    saude1= {0:'Não Tem uma Boa Saúde',1:'Tem uma boa Saúde'}
    df['GenHlth_Boa']=df['GenHlth_Boa'].replace(saude1)

    saude2= {0:'Não Tem uma Saúde Moderada',1:'Tem uma Saúde Moderada'}
    df['GenHlth_Moderada'] =df['GenHlth_Moderada'].replace(saude2)

    saude3= {0:'Não Tem uma Saúde Execelente',1:'Tem uma Saúde Execelente'}
    df['GenHlth_Execelente'] =df['GenHlth_Execelente'].replace(saude3)

    saude4= {0:'Não Tem Saúde Ruim',1:'Tem uma Saúde Ruim'}
    df['GenHlth_Ruim'] = df['GenHlth_Ruim'].replace(saude4)

    saude5= {0:'Não Tem uma Saúde Podre',1:'Tem uma Saúde Podre'}
    df['GenHlth_Pobre'] = df['GenHlth_Pobre'].replace(saude5)

    frutas = {0:'Não Cosomem Frutas',1:'Consomem Frutas'}
    df['Fruits'] = df['Fruits'].replace(frutas)

    legumes= {0:'Não Consomem Legumes ou Verduras', 1:'Não Consomem Legumes ou Verduras'}
    df['Veggies'] = df['Veggies'].replace(legumes)
    df.rename(columns={
    'Smoker': 'Fumantes',
    'HeartDiseaseorAttack':'Problemas Cardíacos',
    'PhysActivity': "Pratica Atividade Física",
    'Sex': 'Sexo',
    'GenHlth_Boa': 'Saúde Boa',
    'GenHlth_Execelente': 'Saúde Excelente',
    'GenHlth_Moderada': 'Saúde Moderada',
    'GenHlth_Pobre': 'Saúde Probre',
    'GenHlth_Ruim': 'Saúde Ruim',
    'Fruits': 'Consumo de Frutas',
    'Veggies': 'Consumo de Legumes e Verduras'
    }, inplace=True)
    return df

dfp_mca = dfp[['HeartDiseaseorAttack','Smoker','PhysActivity','Sex','GenHlth','Fruits','Veggies']]
dfp_c_labels=labels(dfp_c.copy())
dfp_c2_labels= labels(dfp_c2.copy())

def grafico1():
    st.subheader('Histogramas Relacionados aos Clusters Apenas de Hábitos e Características dos Individuos')

    
    nome_colunas = ['Problemas Cardíacos', 'Fumantes', "Pratica Atividade Física", 'Sexo', 'Saúde Boa',
                    'Saúde Excelente', 'Saúde Moderada', 'Saúde Probre', 'Saúde Ruim',
                    'Consumo de Frutas', 'Consumo de Legumes e Verduras']

   
    colunas = st.selectbox('Colunas', options=nome_colunas, key='histograma')
    
    
    col1, col2 = st.columns(2)
    
    
    cores_clusters = {'Grupo 0': '#636EFA', 'Grupo 1': '#19D3F3', 'Grupo 2': '#1f77b4'}
    
   
    button_input = st.button('Gerar Gráfico')
    
    if button_input:
        with col1:
            st.subheader('Histograma 1 KModes')
            
            
            fig = px.histogram(dfp_c_labels, x=colunas, color='Clusters', 
                               title=f'Distribuição de {colunas} por Cluster (KModes)',
                               color_discrete_map=cores_clusters,
                               category_orders={'Clusters': ['Grupo 0', 'Grupo 1', 'Grupo 2']})  
            fig.update_layout(barmode='group',yaxis_title='Quantidade')
            fig.update_traces(texttemplate='%{y}', textposition='auto')
            st.plotly_chart(fig)

        with col2:
            st.subheader('Histograma 2 KMeans')
            order = dfp_c2_labels[colunas].value_counts().index.tolist()
            
            fig = px.histogram(dfp_c2_labels, x=colunas, color='Clusters', 
                               title=f'Distribuição de {colunas} por Cluster (KMeans)',
                               color_discrete_map=cores_clusters,
                               category_orders={'Clusters': ['Grupo 0', 'Grupo 1', 'Grupo 2']})  
            fig.update_layout(barmode='group',yaxis_title='Quantidade')
            fig.update_traces(texttemplate='%{y}', textposition='auto')
            st.plotly_chart(fig)
 
grafico1()


def dispersao():
    st.subheader('Gráficos de Dispersão Apenas de Hábitos e Características dos Individuos')
    
    
    cores_clusters = {'Grupo 0': '#636EFA', 'Grupo 1': '#19D3F3', 'Grupo 2': '#1f77b4'}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write('Gráficos de Dispersão dos Clusters com PCA (KModes)')
        
        
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(dfp_c)
        df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'])
        df_pca['Clusters'] = dfp_c['Clusters'].map(lambda x: f'Grupo {x}')  
        
       
        fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='Clusters',
                        title='Clusters KModes visualizados em 2D usando PCA',
                        color_discrete_map=cores_clusters,
                        category_orders={'Clusters': ['Grupo 0', 'Grupo 1', 'Grupo 2']})  
        
        fig.update_layout(xaxis_title='PCA Componente 1',
                          yaxis_title='PCA Componente 2')
        
        st.plotly_chart(fig)
    
    with col2:
        st.write('Gráficos de Dispersão dos Clusters com PCA (KMeans)')
        
        
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(dfp_c2)
        df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'])
        df_pca['Clusters'] = dfp_c2['Clusters'].map(lambda x: f'Grupo {x}')
        
       
        fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='Clusters',
                        title='Clusters KMeans visualizados em 2D usando PCA',
                        color_discrete_map=cores_clusters,
                        category_orders={'Clusters': ['Grupo 0', 'Grupo 1', 'Grupo 2']})  
        
        fig.update_layout(xaxis_title='PCA Componente 1',
                          yaxis_title='PCA Componente 2')
        
        st.plotly_chart(fig)

dispersao()

import prince
import pandas as pd
import plotly.express as px
import streamlit as st




def mapa_calor(df1,df2):
    st.subheader('Mapas de Calor (HeatMaps)')
    col1,col2= st.columns(2)
    df_cluster_corr = df1.corr()
    df_cluster_corr2 = df2.corr()
    
    with col1:
        st.write('Heatmap de Correlação KModes')
        plt.figure(figsize=(10,8))
        sns.heatmap(df_cluster_corr, annot=False, cmap='coolwarm', linewidths=0.5)
        plt.title("Heatmap de Correlação entre Variáveis de Hábitos e Características dos Individuos")
        st.pyplot(plt)
        
    with col2:
        st.write('Heatmap de Correlação KMeans')
        plt.figure(figsize=(10,8))
        sns.heatmap(df_cluster_corr2, annot=False, cmap='coolwarm', linewidths=0.5)
        plt.title("Heatmap de Correlação entre Variáveis de Hábitos e Características dos Individuos")
        st.pyplot(plt)
mapa_calor(dfp_c,dfp_c2)







