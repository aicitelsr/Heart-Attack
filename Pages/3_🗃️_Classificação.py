from functools import partial
from graphviz import Source
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.metrics import classification_report
from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
import pickle

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
                'classe': [],
                'precision': [],
                'recall': [],
                'f1-score': [],
                'support': [],
            }

    accuracy = 0
    support = 0

    for key, value in report.items():
      if key == 'accuracy':
        accuracy = value
      else:
        df_results['classe'].append(key)
        df_results['precision'].append(value['precision'])
        df_results['recall'].append(value['recall'])
        df_results['f1-score'].append(value['f1-score'])
        support = int(value['support'])
        df_results['support'].append(support)

    df_results = pd.DataFrame(df_results)
    df_results.style.format({'precision': '{:.2f}', 'recall': '{:.2f}', 'f1-score': '{:.2f}', 'support': '{:.0f}'})
    st.write(f'''
                <b>Accuracy: {accuracy:.4%}</b><br/>
                Support: {support:.0f}
             ''', unsafe_allow_html=True)
    st.write('')
    st.dataframe(df_results)

def _randomForest(x_train, y_train, x_test, y_test):
    rf = joblib.load('./Models/random_forest_model.pkl.gz')

    pred_train = rf.predict(x_train)
    pred_test = rf.predict(x_test)

    # Gerar resultados
    report_train = classification_report(y_train, pred_train, output_dict=True)
    report_test = classification_report(y_test, pred_test, output_dict=True)

    # st.title('Feature importance do RandomForest')
    
    # Feature importances do RF
    importance = rf.feature_importances_
    feature_importances = pd.Series(importance, index=x_train.columns).sort_values(ascending=False)

    # Mostrar o gráfico de importâncias
    fig, ax = plt.subplots()
    feature_importances.plot.barh(ax=ax)
    ax.set_title('Importância das Características')
    ax.set_xlabel('Importância')
    ax.set_ylabel('Características')
    return report_train, report_test, fig

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

def _catBoost(x_train, y_train, x_test, y_test):
    cb = joblib.load('./Models/catboost_model.pkl.gz')

    pred_train = cb.predict(x_train)
    pred_test = cb.predict(x_test)

    # Avaliando o modelo
    report_train = classification_report(y_train, pred_train, output_dict=True)
    report_test = classification_report(y_test, pred_test, output_dict=True)

    # Feature importances do RF
    importance = cb.feature_importances_
    feature_importances = pd.Series(importance, index=x_train.columns).sort_values(ascending=False)

    # Mostrar o gráfico de importâncias
    fig, ax = plt.subplots()
    feature_importances.plot.barh(ax=ax)
    ax.set_title('Importância das Características')
    ax.set_xlabel('Importância')
    ax.set_ylabel('Características')
    return report_train, report_test, fig

# def _plotConfusionMatrix(y_test, pred):
#     cm = confusion_matrix(y_test, pred)
#     ConfusionMatrixDisplay(confusion_matrix=cm)

#     # Criar a visualização da matriz de confusão
#     fig, ax = plt.subplots(figsize=(8, 6))  # Ajuste o tamanho conforme necessário
#     disp = ConfusionMatrixDisplay(confusion_matrix=cm)
#     disp.plot(ax=ax, cmap='viridis', values_format='d')  # Ajuste o cmap conforme desejado

#     # Adicionar título e rótulos
#     ax.set_title('Matriz de Confusão')
#     ax.set_xlabel('Previsão')
#     ax.set_ylabel('Real')

#     # Exibir a matriz de confusão no Streamlit
#     st.pyplot(fig)
def create_classifier_dict(x_train, y_train, x_test, y_test):
    classifiers = {
        'Random Forest': partial(_randomForest, x_train, y_train, x_test, y_test),
        'CatBoost': partial(_catBoost, x_train, y_train, x_test, y_test),
        'Regressão Logística': partial(_regressaoLogistica, x_train, y_train, x_test, y_test)
    }
    
    return classifiers

def buildPage():
    isBalanced = False
    rawDf = transformData(readDataframe_parquet())
    balancedDf = pd.read_parquet('./data/heart_disease_resampled.parquet')

    df = balancedDf if isBalanced else rawDf

    classifiers = ['Random Forest', 'CatBoost', 'Regressão Logística']    

    df_target = df['HeartDiseaseorAttack']
    st.title('Classificação')
    
    st.subheader('Escolha um modelo de Classificação:')
    left, right = st.columns([3, 1], vertical_alignment='bottom')

    with left:
        classifier = st.selectbox(label='Escolha o modelo', options=classifiers)
    
    with right:
        isBalanced = st.checkbox(label='Balancear dataset')

    confirmButton = st.button('Classificar')

    if confirmButton:
        #  Dropando variaveis
        df = df.drop(['HeartDiseaseorAttack','Education_College 1-3', 'Education_College 4 ou mais', 'Education_Grades 1-8', 'Education_Grades 12 ou GED', 'Education_Grades 9-11', 'MentHlth', 'PhysHlth'], axis=1)

        # Divisão entre treino e teste
        x_train, x_test, y_train, y_test = train_test_split(df, df_target, test_size=0.2, random_state=42)

        # Seleção do Classificador
        classifier_dict = create_classifier_dict(x_train, y_train, x_test, y_test)
        report_train, report_test, fig = classifier_dict[classifier]()

        c1, _, c2, c3 = st.columns([.49, .02, .49, 0.1]) 
    
        with c1:
            st.subheader('Dados de treino')
            _showReport(report_train)
    
        st.write('')

        with c2:
            st.subheader('Dados de teste')
            _showReport(report_test)

        # Features importance
        st.subheader('Feature importance do Modelo:')
        st.pyplot(fig)

    # st.write(df_target.value_counts())

if __name__ == '__main__':
    buildPage()
