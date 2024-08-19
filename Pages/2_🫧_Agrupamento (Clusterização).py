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
from utils import readDataframe_parquet
from utils import transformData

dfp = transformData(readDataframe_parquet())

dfp_c= dfp[['Smoker','PhysActivity','Sex','GenHlth_Boa',
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
        st.plotly_chart(fig)

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
        st.plotly_chart(fig)


# from sklearn.metrics import davies_bouldin_score

# db_score = davies_bouldin_score(dfp_c, clusters)
# print(f"Davies-Bouldin Index: {db_score}")


# db_score2 = davies_bouldin_score(dfp_c2, clusters)
# print(f"Davies-Bouldin Index: {db_score2}")


# # In[ ]:




