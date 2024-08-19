import streamlit as st
st.title('Agrupamento')


import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as pl
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import seaborn as sns
import numpy as np
from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
import prince

dfp= pd.read_parquet('C:\VScode\Projetos3\data\heart_disease.parquet')

age = {1:'18-24',2:'25-29',3:'30-34',4:'35-39',5:'40-44',6:'45-49',7:'50-54',8:'55-59',9:'60-64',10:'65-69',11:'70-74',12:'75-79', 13:'Mais de 80'}
dfp['Age']= dfp['Age'].replace(age)




income = {1: 'Menos de 10000', 2:'10000-$14000' , 3:'15000-$19999', 4:'20000-$24999', 5:'25000-$34999', 6:'35000-$49999', 7:'50000-$74999', 8:'75000 ou mais'}
dfp['Income']= dfp['Income'].replace(income)




education = {1:'Nunca foi a escola (ou apenas foi à pré-escola)', 2:'Grades 1-8', 3:'Grades 9-11',4:'Grades 12 ou GED', 5:'College 1-3', 6:'College 4 ou mais'}
dfp['Education'] = dfp['Education'].replace(education)



diabetes = {0: 'Não possui diabetes', 1:'Pré-diabético', 2:'Diabético'}
dfp['Diabetes'] = dfp['Diabetes'].replace(diabetes)


# In[ ]:


def categorizar_bmi(valor):
    if valor < 16:
        return 'Abaixo do peso'
    elif 16 <= valor < 18.5:
        return 'Peso normal baixo'
    elif 18.5 <= valor < 25:
        return 'Peso normal'
    elif 25 <= valor < 30:
        return 'Sobrepeso'
    elif 30 <= valor < 35:
        return 'Obesidade Grau I'
    elif 35 <= valor < 40:
        return 'Obesidade Grau II'
    else:
        return 'Obesidade Grau III'

dfp['BMI'] = dfp['BMI'].apply(categorizar_bmi)

saude_geral={1:'Execelente',2:'Boa',3:'Moderada',4:'Ruim',5:'Pobre'}
dfp['GenHlth'] = dfp['GenHlth'].replace(saude_geral)


dfp_d= pd.get_dummies(dfp)


dfp_d = dfp_d.map(lambda x: 1 if x is True else (0 if x is False else x))


dfp_c= dfp_d[['Smoker','PhysActivity','Sex','GenHlth_Boa',
       'GenHlth_Execelente', 'GenHlth_Moderada', 'GenHlth_Pobre',
       'GenHlth_Ruim','Age_18-24', 'Age_25-29', 'Age_30-34', 'Age_35-39',
       'Age_40-44', 'Age_45-49', 'Age_50-54', 'Age_55-59', 'Age_60-64',
       'Age_65-69', 'Age_70-74', 'Age_75-79', 'Age_Mais de 80','Fruits', 'Veggies']]

# cotovelo
# valores=[]
# #n_clusters: Número de clusters desejado.
# #init: Método de inicialização dos centroids ('Huang' é o padrão, mas você também pode usar 'Cao').
# #n_init: Número de vezes que o algoritmo será rodado com diferentes centroides iniciais.
# #verbose: Controle da verbosidade (0 para nenhum, 1 para output detalhado).
# for i in range(1,6):
#     km= KModes(n_clusters=i, init='Huang', n_init=5, verbose=0, max_iter=10)
#     km.fit_predict(dfp_c)
#     valores.append(km.cost_)
# valores


# plt.figure(figsize=(10, 6))
# plt.plot(range(1,6), valores, marker='o', linestyle='--', color='b')
# plt.xlabel('Número de Clusters')
# plt.ylabel('Custo')
# plt.title('Gráfico do Cotovelo para K-Modes')
# plt.xticks(range(1,6))
# plt.grid(True)
# plt.show()


kmodes = KModes(n_clusters=3, init='Huang', n_init=5, verbose=0, max_iter=10)
clusters = kmodes.fit_predict(dfp_c)
dfp_c['Cluster'] = clusters


for feature in dfp_c.columns:
    if feature != 'Cluster':
        
        fig = px.histogram(dfp_c, x=feature, color='Cluster', 
                           title=f'Distribuição de {feature} por Cluster',
                           labels={feature: feature},
                           color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(barmode='group')
        st.ploplotly_chart(fig)

dfp_c2= dfp[['Smoker','PhysActivity','Sex',
       'GenHlth','Age','Fruits', 'Veggies']]

numericas=[]
categoricas=[]
for i in dfp_c2.columns:
    if dfp_c2[i].dtypes=='float64':
        numericas.append(i)
    elif dfp_c2[i].dtypes=='object':
        categoricas.append(i)

categoricas_indices = [dfp_c2.columns.get_loc(col) for col in categoricas]
categoricas_indices

kproto = KPrototypes(n_clusters=3, init='Huang', verbose=0, max_iter=10)
cluster2= kproto.fit_predict(dfp_c2,categorical=categoricas_indices)

dfp_c2['Clusters']= cluster2


for feature in dfp_c2.columns:
    if feature != 'Clusters':
        
        fig = px.histogram(dfp_c2, x=feature, color='Clusters', 
                           title=f'Distribuição de {feature} por Cluster',
                           labels={feature: feature},
                           color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(barmode='group')
        st.ploplotly_chart(fig)


# from sklearn.metrics import davies_bouldin_score

# db_score = davies_bouldin_score(dfp_c, clusters)
# print(f"Davies-Bouldin Index: {db_score}")


# db_score2 = davies_bouldin_score(dfp_c2, clusters)
# print(f"Davies-Bouldin Index: {db_score2}")


# # In[ ]:




