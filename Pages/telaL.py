import streamlit as st
import pandas as pd
import plotly.express as px

data_heart = pd.read_parquet('./data/heart_disease.parquet')
st.title('Tela Inicial de Leticia')


def idade(data_heart):
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, float('inf')]
    labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
              '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 ou mais']
    data_heart['Age'] = pd.cut(
        data_heart['Age'], bins=bins, labels=labels, right=False)

# antigo código usando
# def idade():
#     faixa_idade = {
#         1: '18-24',
#         2: '25-29',
#         3: '30-34',
#         4: '35-39',
#         5: '40-44',
#         6: '45-49',
#         7: '50-54',
#         8: '55-59',
#         9: '60-64',
#         10: '65-69',
#         11: '70-74',
#         12: '75-79',
#         13: '80 ou mais'
#     }

#     for indice, valor in faixa_idade.items():
#         for rows in range(len(data_heart.index)):
#             if data_heart.loc[rows, 'Age'] == indice:
#                 data_heart.loc[rows, 'Age'] = f'{valor}'


def telaL():
    st.markdown('<h3>Gráfico de Barras </h3>', unsafe_allow_html=True)

    idade(data_heart)
    data_heart['HeartDiseaseorAttack'] = data_heart['HeartDiseaseorAttack'].astype(
        'category')
    agrupando_idade = data_heart.groupby(
        'Age')['HeartDiseaseorAttack'].value_counts().to_frame().reset_index()
    agrupando_idade.columns = ['Idade', 'DoencaCardiaca', 'Total']
    # contagem_idade.insert(loc=2, column='DoencaCardiaca',
    # value=data_heart['HeartDiseaseorAttack'])
    # data_heart = px.data_heart.

    fig = px.bar(agrupando_idade, x="Idade", y='Total',
                 color="DoencaCardiaca", title="Gráfico Idade x Doença Cardíaca",
                 labels={'value': "Total"},
                 color_discrete_map={0: "#99ccff", 1: "red"})
    st.plotly_chart(fig)


def binario_para_sim_nao(df):
    # Identificar colunas binárias
    colunas_binarias = data_heart.columns[(
        data_heart.eq(0) | data_heart.eq(1)).all()]

    # Crie um dicionário de mapeamento para converter valores binários em 'Sim' e 'Não'
    mapeamento = {0: 'Não', 1: 'Sim'}

    # Use applymap para aplicar o mapeamento apenas às colunas binárias identificadas
    data_heart[colunas_binarias] = data_heart[colunas_binarias].map(
        lambda x: mapeamento.get(x, x))

    return df


def binario_para_genero(df):

    mapeamento = {0: 'Feminino', 1: 'Masculino'}

    df['Sex'] = df['Sex'].map(mapeamento)

    return df


def telaL2():
    st.markdown('<h3>Histograma</h3>', unsafe_allow_html=True)
    binario_para_genero(data_heart)
    binario_para_sim_nao(data_heart)

    colunas_binarias = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 'PhysActivity',
                        'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk']
    coluna = st.selectbox("Selecione uma coluna binária para visualização:",
                          options=colunas_binarias)

    if coluna:
        agrupando_por_sexo = data_heart.groupby(
            'Sex')[coluna].value_counts().to_frame().reset_index()
        agrupando_por_sexo.columns = ['Sexo', coluna, 'Total']

        fig = px.histogram(agrupando_por_sexo, x="Sexo", y="Total",
                           color="Sexo", pattern_shape=coluna, title=f"Gráfico Sexo x {coluna}",
                           labels={'value:': "Total"})
        st.plotly_chart(fig)
    else:
        st.warning("Por favor, selecione uma coluna binária para visualização.")


telaL()
telaL2()
