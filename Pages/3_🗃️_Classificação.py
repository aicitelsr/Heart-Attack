from graphviz import Source
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint
from sklearn.metrics import classification_report
from catboost import CatBoostClassifier

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image

import streamlit as st
import pandas as pd
import seaborn as sns
from utils import readDataframe_parquet
from utils import transformData
import matplotlib.pyplot as plt

st.title('Classificação')
dfp = transformData(readDataframe_parquet())

# Dropando variáveis que podem não ser útil para a classificação (+ variável target)
dfp_target = dfp['HeartDiseaseorAttack']
dfp= dfp.drop(['HeartDiseaseorAttack','Education_College 1-3', 'Education_College 4 ou mais', 'Education_Grades 1-8', 'Education_Grades 12 ou GED', 'Education_Grades 9-11', 'MentHlth', 'PhysHlth'], axis=1)

# Divisão entre treino e teste
x_train, x_test, y_train, y_test = train_test_split(dfp, dfp_target, test_size=0.2, random_state=42)

def __randomForest():
    rf = RandomForestClassifier(random_state=42, n_jobs=-1, max_depth= 15, n_estimators= 156)
    rf.fit(x_train, y_train)

    # Visualizar três primeiras árvores da floresta
    for i in range(3):
        tree = rf.estimators_[i]
        dot_data = export_graphviz(tree,
                                   feature_names=x_train.columns,
                                   filled=True,
                                   max_depth=2,
                                   impurity=False,
                                   proportion=True,
                                   )
        st.graphviz_chart(dot_data)

    pred = rf.predict(x_test)

    # Streamlit application
    st.title('Feature importance do RandomForest')
    
    # Feature importances do RF
    importance = rf.feature_importances_
    feature_importances = pd.Series(importance, index=x_train.columns).sort_values(ascending=False)

    # Mostrar o gráfico de importâncias
    st.subheader('Importância das Características')
    fig, ax = plt.subplots()
    feature_importances.plot.barh(ax=ax)
    ax.set_title('Importância das Características')
    ax.set_xlabel('Importância')
    ax.set_ylabel('Características')
    st.pyplot(fig)

    st.subheader('Resultados do modelo')
    # Resultados do Modelo
    st.write(classification_report(y_test, pred))

    # Mostrar o gráfico de Matriz de confusão
    st.subheader('Matriz de Confusão')
    __plotConfusionMatrix(pred)

def __tuningRandomForest():
    param_dist = {
        'n_estimators': randint(50, 1000),
        'max_depth': randint(1,20)
        }
    
    rf = RandomForestClassifier()

    rand_search = RandomizedSearchCV(rf, param_distributions=param_dist, n_iter=5, cv=5, random_state=42)
    rand_search.fit(x_train, y_train)

    st.write('Melhores parâmetros: ', rand_search.best_params_)

def __catBoost():
    cb = CatBoostClassifier(random_state=42, verbose=10, max_depth=15, iterations=156)

    cb.fit(x_train, y_train)
    cb_pred = cb.predict(x_test)

    # Avaliando o modelo
    print(classification_report(y_test, cb_pred))

    # Matriz de Confusão
    __plotConfusionMatrix(cb_pred)

def __plotConfusionMatrix(pred):
    cm = confusion_matrix(y_test, pred)
    ConfusionMatrixDisplay(confusion_matrix=cm)

    # Criar a visualização da matriz de confusão
    fig, ax = plt.subplots(figsize=(8, 6))  # Ajuste o tamanho conforme necessário
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(ax=ax, cmap='viridis', values_format='d')  # Ajuste o cmap conforme desejado

    # Adicionar título e rótulos
    ax.set_title('Matriz de Confusão')
    ax.set_xlabel('Previsão')
    ax.set_ylabel('Real')

    # Exibir a matriz de confusão no Streamlit
    st.pyplot(fig)

def buildPage():
    __randomForest()

if __name__ == '__main__':
    buildPage()