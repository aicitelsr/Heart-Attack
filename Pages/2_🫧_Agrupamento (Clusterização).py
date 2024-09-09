import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from utils import readDataframe_parquet

import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

def labels(df):
    problema = {0:'Sem Problemas Cardíacos',1:'Com Problemas Cardíacos'}
    df['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack'].replace(problema)

    grupos= {0:'Grupo 0',1:'Grupo 1', 2:'Grupo 2',3:'Grupo 3'}
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

    idade1 = {0:'Não Tem Entre 18-24 Anos',1:'Tem Entre 18-24 Anos'}
    df['Age_18-24'] = df['Age_18-24'].replace(idade1)

    idade2 = {0:'Não Tem Entre 25-29 Anos',1:'Tem Entre 25-29 Anos'}
    df['Age_25-29'] = df['Age_25-29'].replace(idade2)

    idade3 = {0:'Não Tem Entre 30-34 Anos',1:'Tem Entre 30-34 Anos'}
    df['Age_30-34'] = df['Age_30-34'].replace(idade3)

    idade4 = {0:'Não Tem Entre 35-39 Anos',1:'Tem Entre 35-39 Anos'}
    df['Age_35-39'] = df['Age_35-39'].replace(idade4)

    idade5 = {0:'Não Tem Entre 40-44 Anos',1:'Tem Entre 40-44 Anos'}
    df['Age_40-44'] = df['Age_40-44'].replace(idade5)

    idade6 = {0:'Não Tem Entre 45-49 Anos',1:'Tem Entre 45-49 Anos'}
    df['Age_45-49'] = df['Age_45-49'].replace(idade6)

    idade7 = {0:'Não Tem Entre 50-54 Anos',1:'Tem Entre 50-54 Anos'}
    df['Age_50-54'] = df['Age_50-54'].replace(idade7)

    idade8 = {0:'Não Tem Entre 55-59 Anos',1:'Tem Entre 55-59 Anos'}
    df['Age_55-59'] = df['Age_55-59'].replace(idade8)

    idade9 = {0:'Não Tem Entre 60-64 Anos',1:'Tem Entre 60-64 Anos'}
    df['Age_60-64'] = df['Age_60-64'].replace(idade9)
    
    idade10 = {0:'Não Tem Entre 65-69 Anos',1:'Tem Entre 65-69 Anos'}
    df['Age_65-69'] = df['Age_65-69'].replace(idade10)

    idade11 = {0:'Não Tem Entre 70-74 Anos',1:'Tem Entre 70-74 Anos'}
    df['Age_70-74'] = df['Age_70-74'].replace(idade11)

    idade12 = {0:'Não Tem Entre 75-79 Anos',1:'Tem Entre 75-79 Anos'}
    df['Age_75-79'] = df['Age_75-79'].replace(idade12)

    idade13 = {0:'Não Tem Mais de 80 Anos',1:'Tem Mais de 80 Anos'}
    df['Age_Mais de 80'] = df['Age_Mais de 80'].replace(idade13)

    df.rename(columns={'Smoker': 'Fumantes',
        'HeartDiseaseorAttack':'Problemas Cardíacos',
        'PhysActivity': "Pratica Atividade Física",
        'Sex': 'Sexo',
        'GenHlth_Boa': 'Saúde Boa',
        'GenHlth_Execelente': 'Saúde Excelente',
        'GenHlth_Moderada': 'Saúde Moderada',
        'GenHlth_Pobre': 'Saúde Probre',
        'GenHlth_Ruim': 'Saúde Ruim',
        'Fruits': 'Consumo de Frutas',
        'Veggies': 'Consumo de Legumes e Verduras',
        'Age_18-24': 'Idade Entre 18-24',
        'Age_25-29': 'Idade entre 25-29',
        'Age_30_34': 'Idade Entre 30-34',
        'Age_35-39': 'Idade Entre 25-29',
        'Age_40-44': 'Idade Entre 40-44',
        'Age_45-49': 'Idade Entre 45-49',
        'Age_50-54': 'Idade Entre 50-54',
        'Age_55-59': 'Idade Entre 55-59',
        'Age_60-64': 'Idade Entre 60-64',
        'Age_65-69': 'Idade Entre 65-69',
        'Age_70-74': 'Idade Entre 70-74',
        'Age_75-79': 'Idade Entre 75-79',
        'Age_Mais de 80': 'Idade 80+'}, inplace=True)
    return df

def rename_colunas(df):
    df.rename(columns={'Smoker': 'Fumantes',
        'HeartDiseaseorAttack':'Problemas Cardíacos',
        'PhysActivity': "Pratica Atividade Física",
        'Sex': 'Sexo',
        'GenHlth_Boa': 'Saúde Boa',
        'GenHlth_Execelente': 'Saúde Excelente',
        'GenHlth_Moderada': 'Saúde Moderada',
        'GenHlth_Pobre': 'Saúde Probre',
        'GenHlth_Ruim': 'Saúde Ruim',
        'Fruits': 'Consumo de Frutas',
        'Veggies': 'Consumo de Legumes e Verduras',
        'Age_18-24': 'Idade Entre 18-24',
        'Age_25-29': 'Idade entre 25-29',
        'Age_30-34': 'Idade Entre 30-34',
        'Age_35-39': 'Idade Entre 25-29',
        'Age_40-44': 'Idade Entre 40-44',
        'Age_45-49': 'Idade Entre 45-49',
        'Age_50-54': 'Idade Entre 50-54',
        'Age_55-59': 'Idade Entre 55-59',
        'Age_60-64': 'Idade Entre 60-64',
        'Age_65-69': 'Idade Entre 65-69',
        'Age_70-74': 'Idade Entre 70-74',
        'Age_75-79': 'Idade Entre 75-79',
        'Age_Mais de 80': 'Idade 80+'}, inplace=True)
    return df

dfp= readDataframe_parquet()
dfp_c = pd.read_parquet('data\clusters_kmodes.parquet')
dfp_c2= pd.read_parquet('data\clusters_kmeans.parquet')
dfp_c= dfp_c.rename(columns={'Cluster':'Clusters'})
dfp_c['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack']
dfp_c2['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack']
dfp_c_labels=labels(dfp_c.copy())
dfp_c2_labels= labels(dfp_c2.copy())

st.title('Clusterização K-means e K-modes')
with st.expander('Notas'):
    st.write('Através do método do cotovelo e silhueta foi definido que o melhor número de clusters é 4.')
    col1,col2= st.columns(2)
    with col1:
        st.image('data\cotovelo_kmodes.png', caption='Cotovelo do KModes',use_column_width=True)
        st.image('data\silhouette_score_kmodes.png', caption='Silhouette Score KModes',use_column_width=True)
    with col2:
        st.image('data\cotovelo_kmeans.png', caption='Cotovelo do KMeans',use_column_width=True)
        st.image('data\silhouette_score_kmeans.png', caption='Silhouette Score KMeans',use_column_width=True)

with st.expander('Analise dos Clusters (KModes)'):
    
    col1,col2=st.columns([0.3,0.7])
    with col1:
        analise_cluster_kmodes=dfp_c.copy().groupby('Clusters').mean() * 100
        analise_cluster_kmodes = rename_colunas(analise_cluster_kmodes)
        for cluster in analise_cluster_kmodes.index:
            st.subheader(f"Cluster {cluster} KModes")

            
            st.dataframe(analise_cluster_kmodes.loc[cluster].reset_index().rename(columns={'index':'Característica',cluster: 'Percentual (%)', 0:'Grupo 0'}))

    with col2:
            for cluster in analise_cluster_kmodes.index: 
                fig = px.bar(analise_cluster_kmodes.loc[cluster].reset_index(), x='index', y=cluster, 
                            labels={'index': 'Característica', cluster: 'Percentual (%)'},
                            title=f"Distribuição de Características no Cluster {cluster} (KModes)")
                st.plotly_chart(fig)

            
    st.subheader("Resumo Geral dos Percentuais dos Clusters")
    analise_cluster_kmodes_transposed = analise_cluster_kmodes.T
    analise_cluster_kmodes_transposed.columns = [f'Grupo {i}' for i in range(len(analise_cluster_kmodes_transposed.columns))]
    st.table(analise_cluster_kmodes_transposed)

with st.expander('Analise dos Clusters (KMeans)'):
    
    col1,col2=st.columns([0.3,0.7])
    with col1:
        analise_cluster_kmeans=dfp_c2.copy().groupby('Clusters').mean() * 100
        analise_cluster_kmeans = rename_colunas(analise_cluster_kmeans)
        for cluster in analise_cluster_kmeans.index:
            st.subheader(f"Cluster {cluster} KMeans")

            
            st.dataframe(analise_cluster_kmeans.loc[cluster].reset_index().rename(columns={'index':'Característica',cluster: 'Percentual (%)'}))

    with col2:
            for cluster in analise_cluster_kmeans.index: 
                fig = px.bar(analise_cluster_kmeans.loc[cluster].reset_index(), x='index', y=cluster, 
                            labels={'index': 'Característica', cluster: 'Percentual (%)'},
                            title=f"Distribuição de Características no Cluster {cluster} (KMeans)")
                st.plotly_chart(fig)

            
    st.subheader("Resumo Geral dos Percentuais dos Clusters")
    analise_cluster_kmeans_transposed = analise_cluster_kmodes.T
    analise_cluster_kmeans_transposed.columns = [f'Grupo {i}' for i in range(len(analise_cluster_kmeans_transposed.columns))]
    st.table(analise_cluster_kmeans_transposed)


dfp_c_labels=labels(dfp_c.copy())
dfp_c2_labels= labels(dfp_c2.copy())

def grafico1():
    st.subheader('Histogramas Relacionados aos Clusters Apenas de Hábitos e Características dos Individuos')

    
    nome_colunas = ['Problemas Cardíacos', 'Fumantes', "Pratica Atividade Física", 'Sexo', 'Saúde Boa',
                    'Saúde Excelente', 'Saúde Moderada', 'Saúde Probre', 'Saúde Ruim',
                    'Consumo de Frutas', 'Consumo de Legumes e Verduras','Idade Entre 18-24','Idade entre 25-29','Idade Entre 30-34',
                    'Idade Entre 35-39','Idade Entre 40-44','Idade Entre 45-49','Idade Entre 50-54','Idade Entre 55-59','Idade Entre 60-64',
                    'Idade Entre 65-69','Idade Entre 70-74','Idade Entre 75-79','Idade 80+']

   
    colunas = st.selectbox('Colunas', options=nome_colunas, key='histograma')
    
    
    col1, col2 = st.columns(2)
    
    
    cores_clusters = {'Grupo 0': '#636EFA', 'Grupo 1': '#19D3F3', 'Grupo 2': '#1f77b4','Grupo 3':'#00FA9A'}
    
   
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
    
    
    cores_clusters = {'Grupo 0': '#636EFA', 'Grupo 1': '#19D3F3', 'Grupo 2': '#1f77b4', 'Grupo 3':'#00FA9A'}
    
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







