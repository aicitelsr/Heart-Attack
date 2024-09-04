import streamlit as st
st.title('Matrizes de Confusão')

with st.expander('Matriz de Confusão - Random Forest'):
    st.image('./data/matriz_confusao_rf.png')
with st.expander('Matriz de Confusão - CatBoost'):
    st.image('./data/matriz_confusao_catboost.png')
with st.expander('Matriz de Confusão - Regressão Logística'):
    st.image('./data/matriz_confusao_regressao.png', caption='Matriz de Confusão - Regressão Logística', use_column_width=True)