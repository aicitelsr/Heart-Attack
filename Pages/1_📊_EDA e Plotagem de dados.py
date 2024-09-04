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
custom_colors = ['#636efa', '#4e51d4', '#3936ae', '#211b8a', '#000068']
selected_colors = [custom_colors[0], custom_colors[-2]]


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

# def binario_para_sim_nao(dfp):
    # colunas_binarias = [col for col in df.columns if (dfp[col].eq(0) | dfp[col].eq(1)).all() and col != 'Sex']

    # mapeamento = {0: 'Não', 1: 'Sim'}

    # dfp[colunas_binarias] = dfp[colunas_binarias].map(
    #     lambda x: mapeamento.get(x, x))

    # return dfp
    
# def global_filter(dfp):
#     st.sidebar.header("Filtros Globais")
    
#     # Filtro por Idade
#     selected_age = st.sidebar.multiselect("Filtrar por Faixa Etária", options=dfp['Age'].unique(), default=dfp['Age'].unique())
#     dfp = dfp[dfp['Age'].isin(selected_age)]
    
#     # Filtro por Sexo
#     selected_sex = st.sidebar.multiselect("Filtrar por Sexo", options=dfp['Sex'].unique(), default=dfp['Sex'].unique())
#     dfp = dfp[dfp['Sex'].isin(selected_sex)]
    
#     # Filtro por Doença Cardíaca
#     selected_heart = st.sidebar.multiselect("Filtrar por Doença Cardíaca", options=dfp['HeartDiseaseorAttack'].unique(), default=dfp['HeartDiseaseorAttack'].unique())
#     dfp = dfp[dfp['HeartDiseaseorAttack'].isin(selected_heart)]
    
#     return dfp

def parallel_cateogries():
    dfp_labels= transformRawDf(dfp.copy())
    dfp_labels['Cor'] = dfp['HeartDiseaseorAttack'].copy()
=======

def global_filter(dfp):
    dfp_labels= transformRawDf(dfp.copy())

    st.sidebar.header("Filtros")
    
    # Filtro por Idade
    selected_age = st.sidebar.multiselect("Filtrar idade: ", options=dfp['Age'].unique(), default=dfp['Age'].unique())
    dfp = dfp[dfp['Age'].isin(selected_age)]
    
    # # Filtro por Sexo
    # selected_sex = st.sidebar.multiselect("Filtrar por Sexo", options=dfp_labels['Sexo'].unique(), default=dfp_labels['Sexo'].unique())
    # dfp_labels = dfp_labels[dfp_labels['Sexo'].isin(selected_sex)]
    return dfp

def parallel_cateogries(dfp):
    dfp_labels= transformRawDf(dfp.copy())

>>>>>>> Stashed changes
    st.subheader('Gráfico de Categorias Paralelas')
    colunas = st.multiselect('Colunas (máximo 3)', options=dfp_labels.columns)
    if len(colunas) > 3:
        st.error('Selecione no máximo 3 colunas.', icon='🚨')
        grafico = px.parallel_categories(dfp_labels[colunas], color=dfp_labels['Problemas cardíacos'])

        grafico.update_layout(coloraxis_showscale=False, margin=dict(l=100, r=0, t=0, b=25))
        
        st.plotly_chart(grafico, use_container_width=True)  
    elif len(colunas) >= 2:
        grafico = px.parallel_categories(dfp_labels[colunas], color=dfp_labels['Cor'])
        
        grafico.update_layout(coloraxis_showscale=False, margin=dict(l=100, r=0, t=0, b=25))
        
        st.plotly_chart(grafico, use_container_width=True)
    else:
        st.error('Selecione no mínimo duas colunas.', icon='🚨')
        # if len(colunas) > 3:
        #     st.error('Selecione no máximo 3 colunas.', icon='🚨')
        # elif len(colunas) >=2 and button_input:
        #                 with col2:
        #                         grafico= px.parallel_categories(dfp_labels[colunas], color=dfp_labels['Cor'])

        #                         grafico.update_layout(coloraxis_showscale=False,margin=dict(l=100, r=0, t=0, b=25))

        #                         col2.plotly_chart(grafico, use_container_width=True)         
        # elif len(colunas) < 2:
        #     st.error('Deve haver no mínimo duas colunas', icon='🚨')   
 
def histograms(dfp_labels):
    dfp_labels= transformRawDf(dfp.copy())

    st.subheader('Histograma')

    coluna = st.selectbox('Colunas', options=dfp_labels.columns)

    grafico = px.histogram(dfp_labels, x=coluna, color='Problemas cardíacos')
    st.plotly_chart(grafico, use_container_width=True)

    # with col2:
    #     order = dfp_labels[colunas].value_counts().index.tolist()
    #     grafico= px.histogram(dfp_labels, x=colunas, color='Problemas cardíacos', color_discrete_sequence=selected_colors, category_orders={colunas:order})
    #     grafico.update_layout(bargap=0.1)
    #     col2.plotly_chart(grafico, use_container_width=True)

def boxplot():
    # binario_para_sim_nao(df_cleaned)
    # binario_para_genero(df_cleaned)
    # idade(df_cleaned)

    st.subheader("Gráfico de Boxplot")

    # col1, col2 = st.columns([0.3, 0.7])

    # with st.container():
    variaveis = ['BMI', 'MentHlth', 'PhysHlth']   
    escolha_variavel = st.selectbox('Escolha a Variável para o Boxplot:', options=variaveis)

    grafico = px.box(dfp, y=escolha_variavel, color='HeartDiseaseorAttack')
    st.plotly_chart(grafico, use_container_width=True)



def buildPage():
    dataDict()
    profilling()
    parallel_cateogries()
    dfp_filtered = global_filter(dfp)
    parallel_cateogries(dfp_filtered)
    histograms(dfp_filtered)
    boxplot(dfp_filtered)
    
if __name__ == '__main__':
    buildPage()


    