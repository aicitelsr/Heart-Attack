import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html
from utils import readDataframe_csv
from utils import readDataframe_parquet
from utils import removeOutliersFromDf

df = readDataframe_csv()
dfp = readDataframe_parquet()
df_cleaned = removeOutliersFromDf(dfp)

# Quando necessário trabalhar com os dados transformados: transformData(readDatafrase_csv())) ou transformData(readDatafrase_parquet()))

st.title('Análise exploratória dos dados e Plotagens')

custom_colors = ['#64b59b', '#b7d2b6', '#f0f1ea', '#e6ce9a', '#f49d5b']

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
            
             # Carregar o conteúdo do arquivo HTML
         with open("data/eda.html", "r") as file:
                 pagina_html = file.read()

                 # Exibir o conteúdo HTML
         st.components.v1.html(pagina_html, height = 700, scrolling=True)

def parallel_cateogries():

    st.subheader('Categorias Paralelas')
    col1,col2=st.columns([.3,.7])
    with col1:
        nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                        'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
        colunas = col1.multiselect('Colunas (máximo 5)', options=nomes_colunas, default=['HeartDiseaseorAttack'])

        button_input = st.button('Gerar Gráfico', disabled=(len(colunas) < 2 or len(colunas) > 5))

        if len(colunas) > 5:
            st.error('Selecione no máximo 5 colunas.', icon='🚨')
        elif len(colunas) >=2 and button_input:
                        with col2:
                                grafico= px.parallel_categories(dfp[colunas], color='HeartDiseaseorAttack', color_continuous_scale=custom_colors)

                                grafico.update_layout(coloraxis_showscale=False)

                                col2.plotly_chart(grafico,use_container_width=True)         
        elif len(colunas) < 2:
            st.error('Deve haver no mínimo duas colunas', icon='🚨')                

def histograms():

    st.subheader('Histograma')
    col1,col2=st.columns([.3,.7])

    with col1:
          st.write("Selecione uma coluna para visualizar o histograma:")
          nomes_colunas=['HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                        'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
          
          colunas=col1.selectbox('Colunas', options=nomes_colunas, key='histograma')

    with col2:
        
        selected_colors = [custom_colors[0], custom_colors[-1]]
        grafico= px.histogram(dfp, x=colunas, color='HeartDiseaseorAttack', color_discrete_sequence=selected_colors)
        grafico.update_layout(bargap=0.1)
        col2.plotly_chart(grafico,use_container_width=True)

def boxplot():
    binario_para_sim_nao()
    binario_para_genero()

    st.subheader("Boxplot")
    st.subheader("Filtros")

    col1, col2 = st.columns([0.3, 0.7])

    with st.container():
        variaveis = ['BMI', 'MentHlth, PhysHlth']   
        escolha_variavel = st.selectbox('Escolha a Variável para o Boxplot:', options=variaveis)

        filtros_ativados = escolha_variavel != 'Nenhum'

        filtro_idade = st.checkbox('Filtrar por Idade', disabled=not filtros_ativados)
        filtro_sexo = st.checkbox('Filtrar por Sexo', disabled=not filtros_ativados)
        filtro_nenhum = st.checkbox("Nenhum")

        # Checkbox para selecionar o DataFrame
        show_outliers = st.checkbox('Remover outliers', value=False)
        selected_df = df_cleaned if show_outliers else dfp

        grafico = None 

        if escolha_variavel == 'BMI':
            if filtro_idade:
                grafico = px.box(selected_df, x='Age', y='BMI', color='HeartDiseaseorAttack', title=f'Boxplot de IMC por idade e Doença Cardíaca', color_discrete_sequence=custom_colors, category_orders={'Age': sorted(selected_df['Age'].unique())})
            elif filtro_sexo:
                grafico = px.box(selected_df, x='Sex', y='BMI', color='HeartDiseaseorAttack', title=f'Boxplot de IMC por sexo e Doença Cardíaca', color_discrete_sequence=custom_colors)
            else:
                grafico = px.box(selected_df, y='BMI', color='HeartDiseaseorAttack', title='Boxplot de IMC por Doença Cardíaca', color_discrete_sequence=custom_colors)
        elif escolha_variavel == 'MentHlth, PhysHlth':
            variaveis_para_plotar = ['MentHlth', 'PhysHlth']

            df_melted = selected_df.melt(id_vars=['HeartDiseaseorAttack'], value_vars=variaveis_para_plotar, var_name='Variável', value_name='Valor')

            if filtro_idade:
                df_melted['Age'] = selected_df['Age']
                
                grafico = px.box(df_melted, x='Age', y='Valor', color='HeartDiseaseorAttack', facet_col='Variável', color_discrete_sequence=custom_colors, category_orders={'Age': sorted(selected_df['Age'].unique())}, title='Boxplot de Saúde Mental e Física por Idade')
            elif filtro_sexo:
                df_melted['Sex'] = selected_df['Sex']

                grafico = px.box(df_melted, x='Sex', y='Valor', color='HeartDiseaseorAttack', facet_col='Variável', color_discrete_sequence=custom_colors, title='Boxplot de Saúde Mental e Física por Sexo')
            else:
                
                grafico = px.box(df_melted, y='Valor', color='HeartDiseaseorAttack', facet_col='Variável', color_discrete_sequence=custom_colors, title='Boxplot de Saúde Mental e Física')
                 
        if grafico is not None:
                st.plotly_chart(grafico, use_container_width=True)
        else:
            st.warning('Selecione uma variável e aplique um filtro para visualizar o gráfico.')

def idade():
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, float('inf')]
    labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
              '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 ou mais']
    
    dfp['Age'] = pd.cut(dfp['Age'], bins=bins, labels=labels, right=True)

    return dfp

def binario_para_sim_nao():
    colunas_binarias = [col for col in df.columns if (dfp[col].eq(0) | dfp[col].eq(1)).all() and col != 'Sex']

    mapeamento = {0: 'Não', 1: 'Sim'}

    dfp[colunas_binarias] = dfp[colunas_binarias].map(
        lambda x: mapeamento.get(x, x))

    return dfp


def binario_para_genero():

    mapeamento = {0: 'Feminino', 1: 'Masculino'}

    dfp['Sex'] = dfp['Sex'].map(mapeamento)

    return dfp


def bar_two():
    st.markdown('<h3>Gráfico de Barras </h3>', unsafe_allow_html=True)

    col1,col2=st.columns([.3,.7])

    with col1:

        colunas_binarias = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 'PhysActivity',
                            'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk']
        
        coluna = st.selectbox("Selecione uma coluna binária para visualização:",
                            options=colunas_binarias)

        if coluna:
            agrupando_por_sexo = dfp.groupby('Sex')[coluna].value_counts().to_frame().reset_index()
            agrupando_por_sexo.columns = ['Sexo', coluna, 'Total']
            
            fig = px.histogram(agrupando_por_sexo, x='Sexo', y='Total',
                            color=coluna, barmode='group',
                            color_discrete_map={0: 'lightgray', 1: 'royalblue'},
                            labels={'Total': 'Número de Pessoas', coluna: coluna},
                            height=500)
        else:
            st.warning("Por favor, selecione uma coluna binária para visualização.")
    with col2:
         col2.plotly_chart(fig, use_container_width=True)


def buildPage():
    dataDict()
    profilling()
    parallel_cateogries()
    histograms()
    boxplot()
    bar_two()
    
if __name__ == '__main__':
    buildPage()


    