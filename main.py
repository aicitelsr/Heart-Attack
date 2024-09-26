import streamlit as st
st.set_page_config(
    page_title='Tela Inicial',
    layout="wide",
    menu_items={
        'About': '''Sistema desenvolvido para as atividades avaliativas do curso de Bacharelado em Sistemas
        de Informação (BSI) da Universidade Federal Rural de Pernambuco.
        Autores: Júlio Santos, Letícia Rodrigues, Marcelo Antonio e Maycon Romário
        '''
    }
)

st.markdown(f'''
    <h1>Avaliação de Modelos de Machine Learning na Previsão de Doenças Cardíacas: Um Estudo Exploratório</h1>
    <br>
    Sistema desenvolvido para as atividades avaliativas da disciplina de PISI3 do curso de Bacharelado em Sistemas
    de Informação (BSI) da Universidade Federal Rural de Pernambuco (UFRPE).
    <br>
    <br>
    Sumário:
    <ul>
            <li>EDA e plotagem de dados.</li>
            <li>Agrupamento</li>
            <li>Classificação</li>
            <li>Matrizes de Confusão</li>
    </ul>
    <br>
    Autores: Júlio Santos, Letícia Rodrigues, Marcelo Antonio e Maycon Romário.
''', unsafe_allow_html=True)
