from functools import partial
from tkinter import _test
import joblib
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.metrics import classification_report
from catboost import CatBoostClassifier, train
from sklearn.linear_model import LogisticRegression
import pickle
import seaborn as sns

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image

import streamlit as st
import pandas as pd
from utils import readDataframe_parquet
from utils import transformData
import matplotlib.pyplot as plt

def _showReport(report):
    df_results = {
                'Classe': [],
                'Precisão': [],
                'Recall': [],
                'F1-score': [],
                'Suporte': [],
            }

    accuracy = 0
    support = 0

    for key, value in report.items():
      if key == 'accuracy':
        accuracy = value
      else:
        df_results['Classe'].append(key)
        df_results['Precisão'].append(value['precision'])
        df_results['Recall'].append(value['recall'])
        df_results['F1-score'].append(value['f1-score'])
        support = int(value['support'])
        df_results['Suporte'].append(support)

    df_results = pd.DataFrame(df_results)
    df_results.style.format({'Precisão': '{:.2f}%', 'Recall': '{:.2f}%', 'F1-score': '{:.2f}%', 'Suporte': '{:.0f}%'})
    st.write(f'''
                <b>Acurácia: {accuracy:.2%}</b><br/>
                Suporte: {support:.0f}
             ''', unsafe_allow_html=True)
    st.write('')
    
    st.dataframe(df_results, width=1200, height=180)  
    # st.dataframe(df_results)

# KNN model

def __KNN():
    try:
        with open('Models/knn_model_balanced2.pkl', 'rb') as file:
            knn = pickle.load(file)

        model = knn['model']
        report_train = knn['report_train']
        report_test = knn['report_test']
            
        return model, report_train, report_test
    
    except Exception as e:
        st.error(f"Ocorreu um erro com o KNN: {str(e)}")
        return None, None, None, None, None, None

def _regressaoLogistica(x_train, y_train, x_test, y_test):
    # Carregar o modelo com pickle
    with open('Models/regressao2_model.pkl', 'rb') as f:
        logistica = pickle.load(f)

    pred_train = logistica.predict(x_train)
    pred_test = logistica.predict(x_test)

    # Gerar resultados
    report_train = classification_report(y_train, pred_train, output_dict=True)
    report_test = classification_report(y_test, pred_test, output_dict=True)

    coef = logistica.coef_[0]  # Coeficientes do modelo
    feature_importances = pd.Series(coef, index=x_train.columns).sort_values(ascending=False)

    fig, ax = plt.subplots()
    feature_importances.plot.barh(ax=ax)
    fig, ax = plt.subplots(figsize=(10, 8))  # Aumenta o tamanho da figura

    # Plota a importância das características
    feature_importances.plot.barh(ax=ax)

    # Título e rótulos
    ax.set_title('Importância das Características', fontsize=16)
    ax.set_xlabel('Coeficiente', fontsize=14)
    ax.set_ylabel('Características', fontsize=14)

    # Rotaciona as labels do eixo Y para 0 graus (padrão) e ajusta o tamanho da fonte
    ax.tick_params(axis='y', labelsize=12)

    # Ajusta o layout para que as labels não fiquem cortadas
    plt.tight_layout()
        
    return report_train, report_test, fig

def __randomForest():
   with open('./Models/randomForestBalanced.pkl', 'rb') as file:
      data = pickle.load(file)
   
   model = data['model']
   explainer = data['explainer']
   shap_values = data['shap_values']
   x_shap = data['x_shap']
   report_train = data['report_train']
   report_test = data['report_test']

   return model, explainer, shap_values, x_shap, report_train, report_test

def __catBoost():
   with open('./Models/catBoostBalanced.pkl', 'rb') as file:
      data = pickle.load(file)
   
   model = data['model']
   explainer = data['explainer']
   shap_values = data['shap_values']
   x_shap = data['x_shap']
   report_train = data['report_train']
   report_test = data['report_test']

   return model, explainer, shap_values, x_shap, report_train, report_test

def __regressaoLogistica():
   with open('./Models/regressaoBalanced.pkl', 'rb') as file:
      data = pickle.load(file)
   
   model = data['model']
   explainer = data['explainer']
   shap_values = data['shap_values']
   x_shap = data['x_shap']
   report_train = data['report_train']
   report_test = data['report_test']

   return model, explainer, shap_values, x_shap, report_train, report_test

def _featureImportances(shap_values, x_shap):
    fig, ax = plt.subplots()
    shap.summary_plot(shap_values, x_shap, show=False, plot_size=[10,6])
    
    # Ajustes nas labels
    ax.set_xlabel('Valor de SHAP (impacto na previsão do modelo)')
    
    return fig

def _forcePlot(explainer, shap_values, x_shap):
    fig = shap.force_plot(explainer.expected_value, shap_values[1], x_shap.iloc[1, :], figsize=[36,6], matplotlib = True, show=False)
    plt.xticks(rotation=45, ha="right", fontsize=8)  # Rotaciona e diminui o tamanho da fonte
    plt.yticks(fontsize=1)  # Diminui o tamanho da fonte das labels das features
    
    return fig

def buildPage():
    # # Definindo os classificadores disponíveis
    classifiers = {
        'Random Forest': lambda: __randomForest(),
        'CatBoost': lambda: __catBoost(),
        'Regressão Logística': lambda: __regressaoLogistica(),
        'KNN':lambda: __KNN()
    } 

    classifier = st.selectbox('Selecione um modelo de classificação', placeholder="Escolha um modelo...",  options=classifiers)

    if classifier == 'KNN':
        model, report_train, report_test = classifiers[classifier]()
        shap_values, x_shap, explainer = None, None, None
    else:
        model, explainer, shap_values, x_shap, report_train, report_test = classifiers[classifier]()

    # classifier = st.selectbox('Selecione um modelo de classificação', placeholder="Escolha um modelo...",  options=classifiers)
    
    # model, explainer, shap_values, x_shap, report_train, report_test = classifiers[classifier]()


    # Espaço
    st.write('')

    # Tabelas de resultados treino e teste
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Treino')
        _showReport(report_train)
    with col2:        
        st.subheader('Teste')
        _showReport(report_test)

    st.subheader('Plots SHAP:')
    # Feature importances
    with st.expander('Importância das Variáveis'):
        st.pyplot(_featureImportances(shap_values, x_shap))

    # Force Plot
    with st.expander('Força das variáveis'):
        st.pyplot(_forcePlot(explainer, shap_values, x_shap))

if __name__ == '__main__':
    buildPage()
