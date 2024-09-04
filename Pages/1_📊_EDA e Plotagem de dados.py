import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
from utils import readDataframe_csv, transformRawDf
from utils import readDataframe_parquet
from utils import removeOutliersFromDf
from utils import _categorizeBMI

df = readDataframe_csv()
dfp = readDataframe_parquet()
df_cleaned = removeOutliersFromDf(dfp)

# Quando necessário trabalhar com os dados transformados: transformData(readDatafrase_csv())) ou transformData(readDatafrase_parquet()))
st.title('Análise exploratória dos dados e Plotagens')
custom_colors = ['#19d3f3', '#00abea', '#0082d9', '#0055bb']
selected_colors = [custom_colors[0], custom_colors[-1]]


def dataDict():
     st.subheader("Dicionário de Dados")
     with st.expander('Dicionario de dados'):
        st.write(
        '''
        <table>
            <tr><th>COLUNA DATASET</th><th>DESCRIÇÃO</th></tr>
            <tr><td>HeartDiseaseorAttack</td><td> Indica se a pessoa já teve doença coriorana arterial ou infarto do miocárdio</td></tr>
            <tr><td>HighBP</td><td> Indica se a pessoa tem pressão alta (atestado por um profissional de saúde)</td></tr>
            <tr><td>HighChol</td><td> Indica se a pessoa tem colesterol alto (atestado por um profissional de saúde)</td></tr>
            <tr><td>CholCheck </td><td> Indica se a pessoa fez alguma checagem de colesterol nos últimos 5 anos</td></tr>
            <tr><td>BMI </td><td> IMC - Índice de Massa Corporal</td></tr>
            <tr><td>Smoker </td><td> Indica se a pessoa já fumou mais de 100 cigarros em sua vida (100 cigarros = 5 maços de cigarro)</td></tr>
            <tr><td>Stroke</td><td> Indica se a pessoa já teve algum AVC</td></tr>
            <tr><td>Diabetes</td><td> 0: A pessoa não tem um histórico de diabetes<br> 1: Pré-diabetico <br> 2: Sofre de qualquer tipo de diabetes</td></tr>
            <tr><td>PhysActivity</td><td> Indica se a pessoa faz pelo menos um exercício físico em sua rotina diária</td></tr>
            <tr><td>Fruits</td><td> Indica se a pessoa consome mas de uma fruta por dia</td></tr>
            <tr><td>Veggies</td><td> Indica se a pessoa consome mais de um vegetal por dia</td></tr>
            <tr><td>HvyAlcoholConsump</td><td> Indica se a pessoa consome mais do que 14 drinks por semana</td></tr>
            <tr><td>AnyHealthCare</td><td> Indica se a pessoa tem algum tipo de plano de saúde</td></tr>
            <tr><td>NoDocbcCost</td><td> Indica se a pessoa já quis visitar algum médico mas não conseguiu, devido ao custo</td></tr>
            <tr><td>GenHlth</td><td> Indica o quão bem é a saúde (no geral) da pessoa: <br> Varia de 1 (excelente) a 5 (ruim)</td></tr>
            <tr><td>Menthlth</td><td> Indica o número de dias, dentro de um período de 30, que a pessoa teve uma má saúde mental</td></tr>
            <tr><td>Physhlth</td><tD> Indica o número de dias, dentro de um período de 30, que a pessoa teve uma má saúde física</td></tr>
            <tr><td>Sex</td><td> Indica o sexo da pessoa | Sendo 0 = Feminino e 1 = Masculino</td></tr>
            <tr><td>Age</td><td>Indica a faixa etária da pessoa:
            <br>
	            1 = 18-24
            <br>     
	            2 = 25-29
            <br>
	            3 = 30-34
            <br>
	            4 = 35-39
            <br>
	            5 = 40-44
            <br>
	            6 = 45-49
            <br>
	            7 = 50-54
            <br>
	            8 = 55-59
            <br>
	            9 = 60-64
            <br>
	            10 = 65-69
            <br>
	            11 = 70-74
            <br>
	            12 = 75-79
            <br>
	            13 = 80 ou mais velho</td></tr>
            <br>
            <tr><td>Education</td><td> Indica o grau de escolaridade mais alto completado. Sendo 0 = nunca foi a escola ou jardim de infância e 6 tendo atendido 4 anos de universidade ou mais.</td></tr>
            <tr><td>Income </td><td> Indica o total de renda da casa, variando de:<br> 1 (<= $10.000) à 6 (>= $75.000)</td></tr>
        </table>
        <br>
        ''', unsafe_allow_html=True)

def profilling():
     st.subheader("Data Profilling")
     with st.expander('Proffiling De Dados'):
            
             
         with open("data/eda.html", "r") as file:
                 pagina_html = file.read()

                 
         st.components.v1.html(pagina_html, height = 700, scrolling=True)


def global_filter(dfp):

    dfp_labels= transformRawDf(dfp.copy())
    st.write(dfp_labels)
    st.sidebar.header("Filtros")

    # Filtro por Idade
    selected_age = st.sidebar.multiselect("Filtrar por idade: ", options=dfp_labels['Idade'].unique(), default=dfp_labels['Idade'].unique())
    dfp_labels = dfp_labels[dfp_labels['Idade'].isin(selected_age)]

    # # Filtro por Sexo
    # selected_sex = st.sidebar.multiselect("Filtrar por Sexo", options=dfp_labels['Sexo'].unique(), default=dfp_labels['Sexo'].unique())
    # dfp_labels = dfp_labels[dfp_labels['Sexo'].isin(selected_sex)]

    return dfp

def parallel_cateogries(dfp):
    dfp_labels= transformRawDf(dfp.copy())

    st.subheader('Gráfico de Categorias Paralelas')
    colunas = st.multiselect('Colunas (máximo 3)', options=dfp_labels.columns)
    if len(colunas) > 3:
        st.error('Selecione no máximo 3 colunas.', icon='🚨')
    elif len(colunas) >= 2:
        dfp_labels['Cor'] = dfp['HeartDiseaseorAttack'].copy()
         
        grafico = px.parallel_categories(dfp_labels[colunas], color=dfp_labels['Cor'], color_continuous_scale=selected_colors)
        
        grafico.update_layout(coloraxis_showscale=False, margin=dict(l=100, r=0, t=0, b=25))
        
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.error('Selecione no mínimo duas colunas.', icon='🚨') 
 
def histograms(dfp_labels):
    dfp_labels= transformRawDf(dfp.copy())

    st.subheader('Histograma')

    coluna = st.selectbox('Colunas', options=dfp_labels.columns)

    order = sorted(dfp_labels[coluna].unique())

    grafico = px.histogram(dfp_labels, x=coluna, color='Problemas cardíacos', color_discrete_sequence=selected_colors, category_orders={coluna: order}, title=f'Histograma de {coluna}')
    grafico.update_yaxes(title_text='Frequência')
    st.plotly_chart(grafico, use_container_width=True)

    # with col2:
    #     order = dfp_labels[colunas].value_counts().index.tolist()
    #     grafico= px.histogram(dfp_labels, x=colunas, color='Problemas cardíacos', color_discrete_sequence=selected_colors, category_orders={colunas:order})
    #     grafico.update_layout(bargap=0.1)
    #     col2.plotly_chart(grafico, use_container_width=True)

def boxplot(dfp):
    dfp_labels = transformRawDf(dfp.copy())

    dfp_labels['Cor'] = dfp['HeartDiseaseorAttack'].copy()      
    st.subheader("Gráfico de Boxplot")
    variaveis = ['IMC - Índice de Massa Corporal', 'Saúde mental', 'Saúde física']   
 
    escolha_variavel = st.selectbox('Escolha a Variável para o Boxplot:', options=variaveis)

    dfp['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack'].map({1.0: 'Com problemas Cardíacos', 0.0: 'Sem problemas Cardíacos'})

    color_map = {'Com problemas Cardíacos': selected_colors[0], 'Sem problemas Cardíacos': selected_colors[1]} 

    if escolha_variavel == 'IMC - Índice de Massa Corporal':
        dfp['Categoria IMC'] = dfp['BMI'].apply(_categorizeBMI)

        ordem_categorias = [
            'Abaixo do peso', 'Peso normal baixo', 'Peso normal', 
            'Sobrepeso', 'Obesidade Grau I', 'Obesidade Grau II', 
            'Obesidade Grau III'
        ]

        variavel = 'Categoria IMC'
        labels = {'Categoria IMC': 'Categorias de IMC', 'HeartDiseaseorAttack': 'Problemas Cardíacos'}

        grafico = px.box(
            dfp, y=variavel, color='HeartDiseaseorAttack',
            color_discrete_map= color_map,
            category_orders={'Categoria IMC': ordem_categorias},
            labels=labels
        )

    elif escolha_variavel == 'Saúde mental':
        variavel = 'MentHlth'
        labels = {'MentHlth': 'Dias com a saúde mental ruim', 'HeartDiseaseorAttack': 'Problemas Cardíacos'}

        grafico = px.box(
            dfp, y=variavel, color='HeartDiseaseorAttack',
            color_discrete_map=color_map,
            labels=labels
        )
    
    else:
        variavel = 'PhysHlth'
        labels = {'PhysHlth': 'Dias com a saúde física ruim', 'HeartDiseaseorAttack': 'Problemas Cardíacos'}

        grafico = px.box(
            dfp, y=variavel, color='HeartDiseaseorAttack',
            color_discrete_map=color_map,
            labels=labels
        )

    grafico.update_layout(
        margin=dict(l=100, r=0, t=0, b=50),
        yaxis_title=None,
        showlegend=True,
        legend_title_text='Problemas Cardíacos'
    )


    st.plotly_chart(grafico, use_container_width=True)


def buildPage():
    dfp_filtered = global_filter(dfp)
    dataDict()
    profilling()
    parallel_cateogries(dfp_filtered)
    histograms(dfp_filtered)
    boxplot(dfp_filtered)

if __name__ == '__main__':
    buildPage()


    