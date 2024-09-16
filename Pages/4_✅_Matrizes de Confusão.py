import streamlit as st
st.title('Matrizes de Confusão')

with st.expander('Matriz de Confusão - Random Forest'):
    st.image('./data/matriz_confusao_rf.png', caption='Matriz de Confusão - Random Forest', use_column_width=True)
with st.expander('Matriz de Confusão - CatBoost'):
    st.image('./data/matriz_confusao_catboost.png', caption='Matriz de Confusão - Regressão CatBoost', use_column_width=True)
with st.expander('Matriz de Confusão - Regressão Logística'):
    st.image('./data/matriz_confusao_regressao.png', caption='Matriz de Confusão - Regressão Logística', use_column_width=True)
with st.expander('Matriz de Confusão - KNN'):
    st.image('./data/matriz_confusao_catboost.png', caption='Matriz de Confusão - KNN', use_column_width=True)