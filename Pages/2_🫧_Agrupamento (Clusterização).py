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
from sklearn.decomposition import PCA

st.title('Clusterização (Agrupamento)')
st.subheader('k-means e k-modes')

dfp = transformData(readDataframe_parquet())
dfp2= transformData2(readDataframe_parquet())

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

clusters2= kmeans.predict(dfp_c2)
dfp_c2['Clusters'] = clusters2
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

dfp_c_labels=labels(dfp_c.copy())
dfp_c2_labels= labels(dfp_c2.copy())

def grafico1():
    
    st.subheader('Histogramas Relacionados aos Clusters Apenas de Hábitos e Características dos Individuos')

    nome_colunas= ['Problemas Cardíacos','Fumantes',"Pratica Atividade Física",'Sexo','Saúde Boa','Saúde Excelente','Saúde Moderada','Saúde Probre',
                    'Saúde Ruim','Consumo de Frutas','Consumo de Legumes e Verduras']
    colunas=st.selectbox('Colunas', options=nome_colunas, key='histograma')
    col1,col2 = st.columns([0.6,0.4])
    cores_clusters = ['#636EFA', '#19D3F3', '#1f77b4']
    button_input = st.button('Gerar Gráfico')
    with col1:
        
        if button_input:
            st.subheader('Histograma 1')
            fig = px.histogram(dfp_c_labels, x=colunas, color='Clusters', 
                                title=f'Distribuição de {colunas} por Cluster(KModes)',
                                
                                color_discrete_sequence=cores_clusters)
            fig.update_layout(barmode='group')
            fig.update_traces(texttemplate ='%{y}', textposition='auto')
            st.plotly_chart(fig)
        with col2:
            
            if button_input:
                st.subheader('Histograma 2')
                fig = px.histogram(dfp_c2_labels, x=colunas, color='Clusters', 
                                    title=f'Distribuição de {colunas} por Cluster(KMeans)',
                                    
                                    color_discrete_sequence=cores_clusters)
                fig.update_layout(barmode='group')
                fig.update_traces(texttemplate ='%{y}', textposition='auto')
                st.plotly_chart(fig)  
grafico1()

def matrix():

    st.subheader('Matrizes de Confusão Relacionadas a Hábitos e Características dos Individuos')
    nome_colunas=['Problemas Cardíacos','Fumantes',"Pratica Atividade Física",'Sexo','Saúde Boa','Saúde Excelente','Saúde Moderada','Saúde Probre',
                    'Saúde Ruim','Consumo de Frutas','Consumo de Legumes e Verduras']
    colunas=st.selectbox('Colunas', options=nome_colunas, key='matriz')
    button_input = st.button('Gerar Matrizes')

    col1,col2= st.columns(2)
    with col1:
        

        confusion_matrix = pd.crosstab(dfp_c_labels['Clusters'], dfp_c_labels[colunas])
        if button_input:
            plt.figure(figsize=(10, 6))
            sns.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='d')
            plt.title(f'Matriz de Confusão(KModes): {colunas}')
            plt.xlabel('Target')
            plt.ylabel('Cluster')
            st.write('Matriz 1')
            st.pyplot(plt)
    with col2:
        
        confusion_matrix = pd.crosstab(dfp_c2_labels['Clusters'], dfp_c2_labels[colunas])
        if button_input:
            plt.figure(figsize=(10, 6))
            sns.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='d')
            plt.title(f'Matriz de Confusão(KMeans): {colunas}')
            plt.xlabel('Target')
            plt.ylabel('Cluster')
            st.write('Matriz 2')
            st.pyplot(plt)
matrix()
def dispersao():
    st.subheader('Gráficos de Dispersão Apenas de Hábitos e Características dos Individuos')
    col1,col2= st.columns([1.2,0.8])
    cores_clusters = ['#636EFA', '#19D3F3', '#1f77b4']
    with col1:
        st.write('Gráficos de Dispersão dos Clusters com PCA(KModes)')
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(dfp_c)

        
        df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'])
        df_pca['Clusters'] = clusters



        
        fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='Clusters',
                        title='Clusters KModes visualizados em 2D usando PCA',
                        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2','Clusters':'Grupos'},
                        color_continuous_scale=cores_clusters)

       
        fig.update_layout(title='Clusters visualizados em 2D usando PCA',
                        xaxis_title='PCA Component 1',
                        yaxis_title='PCA Component 2')

      
        st.plotly_chart(fig)
    with col2:
        st.write('Gráficos de Dispersão dos Clusters com PCA(KMeans)')
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(dfp_c2)

       
        df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'])
        df_pca['Clusters'] = clusters2



        
        fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='Clusters',
                        title='Clusters KMeans visualizados em 2D usando PCA',
                        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2','Clusters':'Grupos'},
                        color_continuous_scale=cores_clusters)

        
        fig.update_layout(title='Clusters visualizados em 2D usando PCA',
                        xaxis_title='PCA Component 1',
                        yaxis_title='PCA Component 2')

        
        st.plotly_chart(fig)
dispersao()
def dispersao_all(df):
    st.subheader('Gráficos de Dispersão com Mais Variáveis')
    cores_clusters = ['#636EFA', '#19D3F3', '#1f77b4']
    with st.expander('Colunas Não Utilizadas'):
        st.write('Todas as colunas foram utlizadas exceto:[HeartDiseaseorAttack,Income_10000-14000, Income_15000-19999, Income_20000-24999,Income_25000-34999, Income_35000-49999, Income_50000-74999,Income_75000 ou mais, Income_Menos de 10000,Education_College 1-3, Education_College 4 ou mais,Education_Grades 1-8, Education_Grades 12 ou GED]')
        
    dfp_sem_colunas= df.drop(['HeartDiseaseorAttack','Income_$10000-$14000', 'Income_$15000-$19999', 'Income_$20000-$24999',
       'Income_$25000-$34999', 'Income_$35000-$49999', 'Income_$50000-$74999',
       'Income_$75000 ou mais', 'Income_Menos de $10000','Education_College 1-3', 'Education_College 4 ou mais',
       'Education_Grades 1-8', 'Education_Grades 12 ou GED',
       'Education_Grades 9-11','MentHlth', 'PhysHlth'],axis=1).copy()
    
    dfp_sem_colunas2= df.drop(['HeartDiseaseorAttack','Income_$10000-$14000', 'Income_$15000-$19999', 'Income_$20000-$24999',
       'Income_$25000-$34999', 'Income_$35000-$49999', 'Income_$50000-$74999',
       'Income_$75000 ou mais', 'Income_Menos de $10000','Education_College 1-3', 'Education_College 4 ou mais',
       'Education_Grades 1-8', 'Education_Grades 12 ou GED',
       'Education_Grades 9-11','MentHlth', 'PhysHlth'],axis=1).copy()
    
    dfp_kmodes=dfp_sem_colunas
    dfp_kmeans = dfp_sem_colunas2

    with open('C:\VScode\Projetos3\Models\kmodes_modelo2.pkl', 'rb') as file:
        kmodes = pickle.load(file)
    clusters = kmodes.predict(dfp_kmodes)
    dfp_kmodes.loc[:,'Clusters'] = clusters

    
    with open('C:\VScode\Projetos3\Models\kmeans_modelo2.pkl','rb') as file:
        kmeans = pickle.load(file)
    clusters2= kmeans.predict(dfp_kmeans)
    dfp_kmeans.loc[:,'Clusters'] = clusters2

    col1,col2= st.columns(2)

    with col1:
        st.write('Gráficos de Dispersão dos Clusters com PCA(KModes)')
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(dfp_kmodes)

        
        df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'])
        df_pca['Clusters'] = clusters



        
        fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='Clusters',
                        title='Clusters KModes visualizados em 2D usando PCA',
                        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2','Clusters':'Grupos'},
                        color_continuous_scale=cores_clusters)

       
        fig.update_layout(title='Clusters visualizados em 2D usando PCA',
                        xaxis_title='PCA Component 1',
                        yaxis_title='PCA Component 2')

      
        st.plotly_chart(fig)
    with col2:
        st.write('Gráficos de Dispersão dos Clusters com PCA(KMeans)')
        pca = PCA(n_components=2)
        df_pca = pca.fit_transform(dfp_kmeans)

       
        df_pca = pd.DataFrame(df_pca, columns=['PCA1', 'PCA2'])
        df_pca['Clusters'] = clusters2



        
        fig = px.scatter(df_pca, x='PCA1', y='PCA2', color='Clusters',
                        title='Clusters KMeans visualizados em 2D usando PCA',
                        labels={'PCA1': 'PCA Component 1', 'PCA2': 'PCA Component 2','Clusters':'Grupos'},
                        color_continuous_scale=cores_clusters)

        
        fig.update_layout(title='Clusters visualizados em 2D usando PCA',
                        xaxis_title='PCA Component 1',
                        yaxis_title='PCA Component 2')

        
        st.plotly_chart(fig)
dispersao_all(dfp)


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
# # from sklearn.metrics import davies_bouldin_score

# # db_score = davies_bouldin_score(dfp_c, clusters)
# # print(f"Davies-Bouldin Index: {db_score}")


# # db_score2 = davies_bouldin_score(dfp_c2, clusters)
# # print(f"Davies-Bouldin Index: {db_score2}")




