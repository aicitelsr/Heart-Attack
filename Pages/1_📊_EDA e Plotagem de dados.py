import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
from utils import readDataframe_csv, transformRawDf
from utils import readDataframe_parquet
from utils import removeOutliersFromDf

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

def global_filter(dfp, grafico):
    dfp_labels= transformRawDf(dfp.copy())
   
    dfp = dfp.rename(columns={'Sex': 'Sexo', 'Age': 'Idade'})

    st.sidebar.header("Filtros")

    age_mapping = {1: '18-24', 2: '25-29', 3: '30-34', 4: '35-39', 5: '40-44',
                   6: '45-49', 7: '50-54', 8: '55-59', 9: '60-64', 10: '65-69',
                   11: '70-74', 12: '75-79', 13: '80+'}

    age_values = list(age_mapping.keys())
    age_labels = [age_mapping[i] for i in age_values]

    idade_min, idade_max = st.sidebar.select_slider("Idade:",  options=age_values,
        value=(1, 13),
        format_func=lambda x: age_mapping[x])
    
    sexo_mapping = {0: 'Feminino', 1: 'Masculino'}
    sexo_reverse_mapping = {v: k for k, v in sexo_mapping.items()}

    selected_sex_labels = st.sidebar.multiselect("Sexo: ", options=list(sexo_mapping.values()), default=list(sexo_mapping.values()))
    selected_sex = [sexo_reverse_mapping[label] for label in selected_sex_labels]

    age_range = [age_mapping[i] for i in range(idade_min, idade_max + 1)]
    dfp_labels = dfp_labels[dfp_labels['Idade'].isin(age_range)]
    dfp_labels = dfp_labels[dfp_labels['Sexo'].isin(selected_sex_labels)]

    dfp = dfp[(dfp['Idade'] >= idade_min) & (dfp['Idade'] <= idade_max)]
    dfp = dfp[dfp['Sexo'].isin(selected_sex)]

    return dfp_labels, dfp

def parallel_cateogries(df):
    # dfp_labels= transformRawDf(dfp.copy())
    dfp_labels = df
    st.subheader('Gráfico de Categorias Paralelas')
    colunas = st.multiselect('Colunas (máximo 3)', options=dfp_labels.columns)
    if len(colunas) > 3:
        st.error('Selecione no máximo 3 colunas.', icon='🚨')
    elif len(colunas) >= 2:

        dfp_labels['Problemas cardíacos'] = dfp['HeartDiseaseorAttack'].copy()
        
        grafico = px.parallel_categories(
            dfp_labels, 
            dimensions=colunas,  
            color='Problemas cardíacos', 
            color_continuous_scale=custom_colors
        )
        
        grafico.update_layout(coloraxis_showscale=False, margin=dict(l=100, r=0, t=0, b=25))
        
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.error('Selecione no mínimo duas colunas.', icon='🚨') 
 
def histograms(df):
    # dfp_labels= transformRawDf(dfp.copy())
    dfp_labels = df
    st.subheader('Histograma')

    coluna = st.selectbox('Colunas', options=dfp_labels.columns)

    order = sorted(dfp_labels[coluna].unique())

    grafico = px.histogram(dfp_labels, x=coluna, color='Problemas cardíacos', color_discrete_sequence=selected_colors, category_orders={coluna: order}, title=f'Histograma de {coluna}')
    grafico.update_yaxes(title_text='Frequência')
    st.plotly_chart(grafico, use_container_width=True)

def boxplot(df):
    df = df

    df.rename(columns={'HeartDiseaseorAttack': 'Problemas cardíacos'}, inplace=True)
    # dfp['Problemas cardíacos'] = dfp['HeartDiseaseorAttack'].copy()      
    st.subheader("Gráfico de Boxplot")
    variaveis = ['IMC - Índice de Massa Corporal', 'Saúde mental', 'Saúde física']   
 
    escolha_variavel = st.selectbox('Escolha a Variável para o Boxplot:', options=variaveis)

    df['Problemas cardíacos'] = df['Problemas cardíacos'].map({1.0: 'Com Problemas Cardíacos', 0.0: 'Sem Problemas Cardíacos'})

    color_map = {'Com Problemas Cardíacos': selected_colors[0], 'Sem Problemas Cardíacos': selected_colors[1]} 

    labels = {}  

    if escolha_variavel == 'IMC - Índice de Massa Corporal':

        ordem_categorias = [
            'Abaixo do peso', 'Peso normal baixo', 'Peso normal', 
            'Sobrepeso', 'Obesidade Grau I', 'Obesidade Grau II', 
            'Obesidade Grau III'
        ]

        variavel = 'BMI'
        labels = {'BMI': 'Valores de IMC', 'Problemas cardíacos': 'Problemas Cardíacos'}
        grafico = px.box(
            df, y=variavel, color='Problemas cardíacos',
            color_discrete_map= color_map,
            category_orders={'BMI': ordem_categorias},
            labels=labels
        )

    elif escolha_variavel == 'Saúde mental':
        variavel = 'MentHlth'
        labels = {'MentHlth': 'Dias com a saúde mental ruim', 'Problemas cardíacos': 'Problemas Cardíacos'}

        grafico = px.box(
            df, y=variavel, color='Problemas cardíacos',
            color_discrete_map=color_map,
            labels=labels
        )
    
    else:
        variavel = 'PhysHlth'
        labels = {'PhysHlth': 'Dias com a saúde física ruim', 'Problemas cardíacos': 'Problemas Cardíacos'}

        grafico = px.box(
            df, y=variavel, color='Problemas cardíacos',
            color_discrete_map=color_map,
            labels=labels
        )

    grafico.update_layout(
        margin=dict(l=100, r=0, t=0, b=50),
         yaxis_title=labels.get(variavel, None), 
        showlegend=True,
        legend_title_text='Problemas Cardíacos'
    )


    st.plotly_chart(grafico, use_container_width=True)


def buildPage():
    dataDict()
    profilling()
    filtered_data = global_filter(dfp, 'Boxplot')
    filter_1, filter2 = filtered_data
    parallel_cateogries(filter_1)
    histograms(filter_1)
    boxplot(filter2)


if __name__ == '__main__':
    buildPage()


    