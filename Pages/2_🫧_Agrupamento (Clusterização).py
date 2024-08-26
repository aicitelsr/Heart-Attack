import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as pl
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import seaborn as sns
import numpy as np
from kmodes.kmodes import KModes
from utils import readDataframe_parquet
from utils import transformData
from utils import transformData2
import pickle 
import matplotlib.pyplot as plt
import seaborn as sn

st.title('Agrupamento KModes e KMeans')

dfp = transformData(readDataframe_parquet())
dfp2=transformData2(readDataframe_parquet())

dfp_c= dfp[['Smoker','PhysActivity','Sex','GenHlth_Boa',
       'GenHlth_Execelente', 'GenHlth_Moderada', 'GenHlth_Pobre',
       'GenHlth_Ruim','Age_18-24', 'Age_25-29', 'Age_30-34', 'Age_35-39',
       'Age_40-44', 'Age_45-49', 'Age_50-54', 'Age_55-59', 'Age_60-64',
       'Age_65-69', 'Age_70-74', 'Age_75-79', 'Age_Mais de 80','Fruits', 'Veggies']].copy()

#kmodes
with open('Models\kmodes_modelo.pkl', 'rb') as file:
    kmodes = pickle.load(file)

clusters = kmodes.predict(dfp_c)
dfp_c.loc[:,'Clusters'] = clusters
dfp_c['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack'].copy()

#kmeans
with open('Models\kmeans_modelo.pkl', 'rb') as file:
    kmeans = pickle.load(file)

dfp_c2= dfp[['Smoker','PhysActivity','Sex','GenHlth_Boa',
       'GenHlth_Execelente', 'GenHlth_Moderada', 'GenHlth_Pobre',
       'GenHlth_Ruim','Age_18-24', 'Age_25-29', 'Age_30-34', 'Age_35-39',
       'Age_40-44', 'Age_45-49', 'Age_50-54', 'Age_55-59', 'Age_60-64',
       'Age_65-69', 'Age_70-74', 'Age_75-79', 'Age_Mais de 80','Fruits', 'Veggies']].copy()

cluster2= kmeans.predict(dfp_c2)
dfp_c2['Clusters'] = cluster2
dfp_c2['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack'].copy()

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
    df['GenHlth_Pobre'] = df['GenHlth_Pobre'].replace(saude4)

    frutas = {0:'Não Cosomem Frutas',1:'Consomem Frutas'}
    df['Fruits'] = df['Fruits'].replace(frutas)

    legumes= {0:'Não Consomem Legumes ou Verduras', 1:'Não Consomem Legumes ou Verduras'}
    df['Veggies'] = df['Veggies'].replace(legumes)

    return df

dfp_c=labels(dfp_c)
dfp_c2= labels(dfp_c2)

def grafico1():
    st.subheader('Histogramas Relacionados a Hábitos e Características dos Individuos')
    dfp_c.rename(columns={
    'HeartDiseaseorAttack':'Problemas Cardíacos',
    'Smoker': 'Fumantes',
    'PhysActivity': "Pratica Atividade Física",
    'Sex': 'Sexo',
    'GenHlth_Boa': 'Saúde Boa',
    'GenHlth_Execelente': 'Saúde Excenlente',
    'GenHlth_Moderada': 'Saúde Moderada',
    'GenHlth_Pobre': 'Saúde Probre',
    'GenHlth_Ruim': 'Saúde Ruim',
    'Fruits': 'Consumo de Frutas',
    'Veggies': 'Consumo de Legumes e Verduras'
}, inplace=True)

    dfp_c2.rename(columns={
    'HeartDiseaseorAttack':'Problemas Cardíacos',
    'Smoker': 'Fumantes',
    'PhysActivity': "Pratica Atividade Física",
    'Sex': 'Sexo',
    'GenHlth_Boa': 'Saúde Boa',
    'GenHlth_Execelente': 'Saúde Excenlente',
    'GenHlth_Moderada': 'Saúde Moderada',
    'GenHlth_Pobre': 'Saúde Probre',
    'GenHlth_Ruim': 'Saúde Ruim',
    'Fruits': 'Consumo de Frutas',
    'Veggies': 'Consumo de Legumes e Verduras'
}, inplace=True)

    
    nome_colunas= ['Problemas Cardíacos','Fumantes',"Pratica Atividade Física",'Sexo','Saúde Boa','Saúde Excenlente','Saúde Moderada','Saúde Probre',
                    'Saúde Ruim','Consumo de Frutas','Consumo de Legumes e Verduras']
    colunas=st.selectbox('Colunas', options=nome_colunas, key='histograma')
    col1,col2 = st.columns(2)
    
    button_input = st.button('Gerar Gráfico')
    with col1:
        
        if button_input:
            st.subheader('Histrograma 1')
            fig = px.histogram(dfp_c, x=colunas, color='Clusters', 
                                title=f'Distribuição de {colunas} por Cluster(KModes)',
                                #labels={'HeartDiseaseorAttack': 'Problemas Cardíacos', 'count':'Quantidade'},
                                color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(barmode='group')
            st.plotly_chart(fig)
        with col2:
            
            if button_input:
                st.subheader('Histrograma 2')
                fig = px.histogram(dfp_c2, x=colunas, color='Clusters', 
                                    title=f'Distribuição de {colunas} por Cluster(KMeans)',
                                    #labels={'HeartDiseaseorAttack': 'Problemas Cardíacos', 'count':'Quantidade'},
                                    color_discrete_sequence=px.colors.qualitative.Vivid)
                fig.update_layout(barmode='group')
                st.plotly_chart(fig)
grafico1()

def matrix():
    dfp_c.rename(columns={
    'HeartDiseaseorAttack':'Problemas Cardíacos',
    'Smoker': 'Fumantes',
    'PhysActivity': "Pratica Atividade Física",
    'Sex': 'Sexo',
    'GenHlth_Boa': 'Saúde Boa',
    'GenHlth_Execelente': 'Saúde Excenlente',
    'GenHlth_Moderada': 'Saúde Moderada',
    'GenHlth_Pobre': 'Saúde Probre',
    'GenHlth_Ruim': 'Saúde Ruim',
    'Fruits': 'Consumo de Frutas',
    'Veggies': 'Consumo de Legumes e Verduras'
}, inplace=True)

    dfp_c2.rename(columns={
    'HeartDiseaseorAttack':'Problemas Cardíacos',
    'Smoker': 'Fumantes',
    'PhysActivity': "Pratica Atividade Física",
    'Sex': 'Sexo',
    'GenHlth_Boa': 'Saúde Boa',
    'GenHlth_Execelente': 'Saúde Excenlente',
    'GenHlth_Moderada': 'Saúde Moderada',
    'GenHlth_Pobre': 'Saúde Probre',
    'GenHlth_Ruim': 'Saúde Ruim',
    'Fruits': 'Consumo de Frutas',
    'Veggies': 'Consumo de Legumes e Verduras'
}, inplace=True)

    st.subheader('Matrizes de Confusão Relacionadas a Hábitos e Características dos Individuos')
    nome_colunas=['Problemas Cardíacos','Fumantes',"Pratica Atividade Física",'Sexo','Saúde Boa','Saúde Excenlente','Saúde Moderada','Saúde Probre',
                    'Saúde Ruim','Consumo de Frutas','Consumo de Legumes e Verduras']
    colunas=st.selectbox('Colunas', options=nome_colunas, key='matriz')
    button_input = st.button('Gerar Matrizes')

    col1,col2= st.columns(2)
    with col1:
        st.write('Matriz 1')

        confusion_matrix = pd.crosstab(dfp_c['Clusters'], dfp_c[colunas])
        if button_input:
            plt.figure(figsize=(10, 6))
            sns.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='d')
            plt.title(f'Matriz de Confusão(KModes): {colunas}')
            plt.xlabel('Target')
            plt.ylabel('Cluster')
            st.pyplot(plt)
    with col2:
        st.write('Matriz 2')
        confusion_matrix = pd.crosstab(dfp_c2['Clusters'], dfp_c2[colunas])
        if button_input:
            plt.figure(figsize=(10, 6))
            sns.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='d')
            plt.title(f'Matriz de Confusão(KMeans): {colunas}')
            plt.xlabel('Target')
            plt.ylabel('Cluster')
            st.pyplot(plt)
matrix()

# # from sklearn.metrics import davies_bouldin_score

# # db_score = davies_bouldin_score(dfp_c, clusters)
# # print(f"Davies-Bouldin Index: {db_score}")


# # db_score2 = davies_bouldin_score(dfp_c2, clusters)
# # print(f"Davies-Bouldin Index: {db_score2}")




