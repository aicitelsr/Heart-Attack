import pandas as pd

def readDataframe_csv() -> pd.DataFrame:
    df = pd.read_csv('data/heart_disease.csv', encoding='utf-8', low_memory=False)
    return df

def readDataframe_parquet() -> pd.DataFrame:
    dfp = pd.read_parquet('data/heart_disease.parquet')
    return dfp

def transformData(df: pd.DataFrame) -> pd.DataFrame:
    # Transformando a coluna idade
    _transformAgeData(df)
    _transformIncomeData(df)
    _transformEducationData(df)
    _transformDiabetesData(df)
    _transformBMI(df)
    _transformGenHealth(df)
    
    # Gerando os dummies
    df_d = pd.get_dummies(df)

    # Transformando o formato True e False para binários (0 e 1)
    df_d = df_d.map(lambda x:1 if x is True else (0 if x is False else x))
    return df_d

def transformData2(df: pd.DataFrame) -> pd.DataFrame:
    # Transformando a coluna idade
    _transformAgeData(df)
    _transformIncomeData(df)
    _transformEducationData(df)
    _transformDiabetesData(df)
    _transformBMI(df)
    _transformGenHealth(df)
    dfp2=df
    return dfp2

def _transformAgeData(df: pd.DataFrame) -> pd.DataFrame:
    age = {1:'18-24',2:'25-29',3:'30-34',4:'35-39',5:'40-44',6:'45-49',7:'50-54',8:'55-59',9:'60-64',10:'65-69',11:'70-74',12:'75-79', 13:'Mais de 80'}
    df['Age']= df['Age'].replace(age)
    return df

def _transformIncomeData(df) -> pd.DataFrame:
    income = {1: 'Menos de $10000', 2:'$10000-$14000' , 3:'$15000-$19999', 4:'$20000-$24999', 5:'$25000-$34999', 6:'$35000-$49999', 7:'$50000-$74999', 8:'$75000 ou mais'}
    df['Income']= df['Income'].replace(income)
    return df

def _transformEducationData(df) -> pd.DataFrame:
    education = {1:'Nunca foi a escola (ou apenas foi à pré-escola)', 2:'Grades 1-8', 3:'Grades 9-11',4:'Grades 12 ou GED', 5:'College 1-3', 6:'College 4 ou mais'}
    df['Education'] = df['Education'].replace(education)
    return df

def _transformDiabetesData(df) -> pd.DataFrame:
    diabetes = {0: 'Não possui diabetes', 1:'Pré-diabético', 2:'Diabético'}
    df['Diabetes'] = df['Diabetes'].replace(diabetes)
    return df

def _transformBMI(df) -> pd.DataFrame:
    df['BMI'] = df['BMI'].apply(_categorizeBMI)
    return df

def _categorizeBMI(value):
    if value < 16:
        return 'Abaixo do peso'
    elif 16 <= value < 18.5:
        return 'Peso normal baixo'
    elif 18.5 <= value < 25:
        return 'Peso normal'
    elif 25 <= value < 30:
        return 'Sobrepeso'
    elif 30 <= value < 35:
        return 'Obesidade Grau I'
    elif 35 <= value < 40:
        return 'Obesidade Grau II'
    else:
        return 'Obesidade Grau III'
    
def _transformGenHealth(df) -> pd.DataFrame:
    genHealth = {1:'Execelente', 2:'Boa', 3:'Moderada', 4:'Ruim', 5:'Pobre'}
    df['GenHlth'] = df['GenHlth'].replace(genHealth)  

def removeOutliersFromDf(df) -> pd.DataFrame:
    outliersToRemove = ['BMI', 'MentHlth', 'PhysHlth', 'Age']
    df_cleaned = df.copy()

    for col in outliersToRemove:
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1

        # Definir limites para detectar outliers
        lower_bound = Q1 - 0.70 * IQR
        upper_bound = Q3 + 0.70 * IQR

        # Remover outliers
        df_cleaned = df_cleaned[~((df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound))]
        
    return df_cleaned

def transformRawDf(df) -> pd.DataFrame:
    problema = {0:'Sem Problemas Cardíacos',1:'Com Problemas Cardíacos'}
    df['HeartDiseaseorAttack'] = df['HeartDiseaseorAttack'].replace(problema)

    fumante = {0:'Não Fumante',1:'Fumante'}
    df['Smoker'] = df['Smoker'].replace(fumante)
    
    atividade_f={0:'Não Pratica Ativades Físicas',1:'Pratica Atividades Físicas'}
    df['PhysActivity'] = df['PhysActivity'].replace(atividade_f)

    sexo = {0:'Feminino', 1:'Masculino'}
    df['Sex'] = df['Sex'].replace(sexo)

    saude= {1:'Ruim', 2:'Razoável', 3:'Boa', 4:'Muito boa', 5:'Excelente'}
    df['GenHlth']=df['GenHlth'].replace(saude)

    frutas = {0:'Não Consomem Frutas',1:'Consomem Frutas'}
    df['Fruits'] = df['Fruits'].replace(frutas)

    legumes= {0:'Não Consomem Legumes ou Verduras', 1:'Consomem Legumes ou Verduras'}
    df['Veggies'] = df['Veggies'].replace(legumes)

    pressaoAlta = {0: 'Não possui pressão alta', 1: 'Possui pressão alta'}
    df['HighBP'] = df['HighBP'].replace(pressaoAlta)

    colesterolAlto = {0: 'Não possui colesteral alto', 1: 'Possui colesteral alto'}
    df['HighChol'] = df['HighChol'].replace(colesterolAlto)

    checagemColesterol = {0: 'Não fez checagem de Colesterol', 1: 'Fez checagem de Colesterol'}
    df['CholCheck'] = df['CholCheck'].replace(colesterolAlto)

    avc = {0: 'Nunca teve um AVC', 1: 'Já teve um AVC'}
    df['Stroke'] = df['Stroke'].replace(avc)

    altoConsumoDeAlcool = {0: 'Baixo consumo de álcool', 1: 'Alto consumo de álcool'}
    df['HvyAlcoholConsump'] = df['HvyAlcoholConsump'].replace(altoConsumoDeAlcool)

    planoSaude = {0: 'Não possui plano de saúde', 1: 'Possui plano de saúde'}
    df['AnyHealthcare'] = df['AnyHealthcare'].replace(planoSaude)

    medicoCusto = {0: 'Não visitou', 1: 'Visitou'}
    df['NoDocbcCost'] = df['NoDocbcCost'].replace(medicoCusto)

    dificuldadeAndar = {0: 'Não possui dificuldade de andar', 1: 'Possui dificuldade de andar'}
    df['DiffWalk'] = df['DiffWalk'].replace(dificuldadeAndar)

    diabetico = {0: 'Não possui um histórico de diabetes', 1: 'Pré-diabético', 2: 'Sofre de algum tipo de diabete'}
    df['Diabetes'] = df['Diabetes'].replace(diabetico)

    df['BMI'] = df['BMI'].apply(_categorizeBMI)
    age = {1:'18-24',2:'25-29',3:'30-34',4:'35-39',5:'40-44',6:'45-49',7:'50-54',8:'55-59',9:'60-64',10:'65-69',11:'70-74',12:'75-79', 13:'80+'}
    df['Age']= df['Age'].replace(age)
    
    df.rename(columns={
    'Smoker': 'Fumantes',
    'Age': 'Idade',
    'HeartDiseaseorAttack':'Problemas cardíacos',
    'PhysActivity': "Atividade física",
    'Sex': 'Sexo',
    'GenHlth': 'Saúde geral',
    'Fruits': 'Consumo de frutas',
    'Veggies': 'Consumo de legumes e verduras',
    'HighBP': 'Pressão alta',
    'HighChol': 'Colesterol alto',
    'BMI': 'IMC - Índice de Massa Corporal',
    'CholCheck': 'Checagem de Colesterol',
    'Stroke': 'AVC',
    'HvyAlcoholConsump': 'Alto Consumo de álcool',
    'AnyHealthcare': 'Plano de saúde',
    'NoDocbcCost': 'Não visitou médico por custo',
    'MentHlth': 'Saúde mental',
    'PhysHlth': 'Saúde física',
    'DiffWalk': 'Dificuldade de andar',
    'Income': 'Renda',
    'Education': 'Formação',
    'Diabetes': 'Diabético'
    }, inplace=True)
    
    return df

def labels(df):
    problema = {0:'Sem Problemas Cardíacos',1:'Com Problemas Cardíacos'}
    df['HeartDiseaseorAttack'] = df['HeartDiseaseorAttack'].replace(problema)

    grupos= {0:'Grupo 0',1:'Grupo 1', 2:'Grupo 2',3:'Grupo 3'}
    df['Clusters']= df['Clusters'].replace(grupos)

    fumante = {0:'Não Fuma',1:'Fuma'}
    df['Smoker'] = df['Smoker'].replace(fumante)
    
    atividade_f={0:'Não Pratica Ativades Físicas',1:'Pratica Atividades Físicas'}
    df['PhysActivity'] = df['PhysActivity'].replace(atividade_f)

    sexo = {0:'Mulher',1:'Homem'}
    df['Sex'] = df['Sex'].replace(sexo)

    saude1= {0:'Não Tem uma Boa Saúde',1:'Tem uma boa Saúde'}
    df['GenHlth_Boa']=df['GenHlth_Boa'].replace(saude1)

    saude2= {0:'Não Tem uma Saúde Moderada',1:'Tem uma Saúde Moderada'}
    df['GenHlth_Moderada'] =df['GenHlth_Moderada'].replace(saude2)

    saude3= {0:'Não Tem uma Saúde Execelente',1:'Tem uma Saúde Execelente'}
    df['GenHlth_Execelente'] =df['GenHlth_Execelente'].replace(saude3)

    saude4= {0:'Não Tem Saúde Ruim',1:'Tem uma Saúde Ruim'}
    df['GenHlth_Ruim'] = df['GenHlth_Ruim'].replace(saude4)

    saude5= {0:'Não Tem uma Saúde Podre',1:'Tem uma Saúde Podre'}
    df['GenHlth_Pobre'] = df['GenHlth_Pobre'].replace(saude5)

    frutas = {0:'Não Cosomem Frutas',1:'Consomem Frutas'}
    df['Fruits'] = df['Fruits'].replace(frutas)

    legumes= {0:'Não Consomem Legumes ou Verduras', 1:'Não Consomem Legumes ou Verduras'}
    df['Veggies'] = df['Veggies'].replace(legumes)

    idade1 = {0:'Não Tem Entre 18-24 Anos',1:'Tem Entre 18-24 Anos'}
    df['Age_18-24'] = df['Age_18-24'].replace(idade1)

    idade2 = {0:'Não Tem Entre 25-29 Anos',1:'Tem Entre 25-29 Anos'}
    df['Age_25-29'] = df['Age_25-29'].replace(idade2)

    idade3 = {0:'Não Tem Entre 30-34 Anos',1:'Tem Entre 30-34 Anos'}
    df['Age_30-34'] = df['Age_30-34'].replace(idade3)

    idade4 = {0:'Não Tem Entre 35-39 Anos',1:'Tem Entre 35-39 Anos'}
    df['Age_35-39'] = df['Age_35-39'].replace(idade4)

    idade5 = {0:'Não Tem Entre 40-44 Anos',1:'Tem Entre 40-44 Anos'}
    df['Age_40-44'] = df['Age_40-44'].replace(idade5)

    idade6 = {0:'Não Tem Entre 45-49 Anos',1:'Tem Entre 45-49 Anos'}
    df['Age_45-49'] = df['Age_45-49'].replace(idade6)

    idade7 = {0:'Não Tem Entre 50-54 Anos',1:'Tem Entre 50-54 Anos'}
    df['Age_50-54'] = df['Age_50-54'].replace(idade7)

    idade8 = {0:'Não Tem Entre 55-59 Anos',1:'Tem Entre 55-59 Anos'}
    df['Age_55-59'] = df['Age_55-59'].replace(idade8)

    idade9 = {0:'Não Tem Entre 60-64 Anos',1:'Tem Entre 60-64 Anos'}
    df['Age_60-64'] = df['Age_60-64'].replace(idade9)
    
    idade10 = {0:'Não Tem Entre 65-69 Anos',1:'Tem Entre 65-69 Anos'}
    df['Age_65-69'] = df['Age_65-69'].replace(idade10)

    idade11 = {0:'Não Tem Entre 70-74 Anos',1:'Tem Entre 70-74 Anos'}
    df['Age_70-74'] = df['Age_70-74'].replace(idade11)

    idade12 = {0:'Não Tem Entre 75-79 Anos',1:'Tem Entre 75-79 Anos'}
    df['Age_75-79'] = df['Age_75-79'].replace(idade12)

    idade13 = {0:'Não Tem Mais de 80 Anos',1:'Tem Mais de 80 Anos'}
    df['Age_Mais de 80'] = df['Age_Mais de 80'].replace(idade13)

    df.rename(columns={'Smoker': 'Fumantes',
        'HeartDiseaseorAttack':'Problemas Cardíacos',
        'PhysActivity': "Pratica Atividade Física",
        'Sex': 'Sexo',
        'GenHlth_Boa': 'Saúde Boa',
        'GenHlth_Execelente': 'Saúde Excelente',
        'GenHlth_Moderada': 'Saúde Moderada',
        'GenHlth_Pobre': 'Saúde Pobre',
        'GenHlth_Ruim': 'Saúde Ruim',
        'Fruits': 'Consumo de Frutas',
        'Veggies': 'Consumo de Legumes e Verduras',
        'Age_18-24': 'Idade Entre 18-24',
        'Age_25-29': 'Idade entre 25-29',
        'Age_30_34': 'Idade Entre 30-34',
        'Age_35-39': 'Idade Entre 25-29',
        'Age_40-44': 'Idade Entre 40-44',
        'Age_45-49': 'Idade Entre 45-49',
        'Age_50-54': 'Idade Entre 50-54',
        'Age_55-59': 'Idade Entre 55-59',
        'Age_60-64': 'Idade Entre 60-64',
        'Age_65-69': 'Idade Entre 65-69',
        'Age_70-74': 'Idade Entre 70-74',
        'Age_75-79': 'Idade Entre 75-79',
        'Age_Mais de 80': 'Idade 80+'}, inplace=True)
    return df

def rename_colunas(df):
    df.rename(columns={'Smoker': 'Fumantes',
        'HeartDiseaseorAttack':'Problemas Cardíacos',
        'PhysActivity': "Pratica Atividade Física",
        'Sex': 'Sexo',
        'GenHlth_Boa': 'Saúde Boa',
        'GenHlth_Execelente': 'Saúde Excelente',
        'GenHlth_Moderada': 'Saúde Moderada',
        'GenHlth_Pobre': 'Saúde Pobre',
        'GenHlth_Ruim': 'Saúde Ruim',
        'Fruits': 'Consumo de Frutas',
        'Veggies': 'Consumo de Legumes e Verduras',
        'Age_18-24': 'Idade Entre 18-24',
        'Age_25-29': 'Idade entre 25-29',
        'Age_30-34': 'Idade Entre 30-34',
        'Age_35-39': 'Idade Entre 25-29',
        'Age_40-44': 'Idade Entre 40-44',
        'Age_45-49': 'Idade Entre 45-49',
        'Age_50-54': 'Idade Entre 50-54',
        'Age_55-59': 'Idade Entre 55-59',
        'Age_60-64': 'Idade Entre 60-64',
        'Age_65-69': 'Idade Entre 65-69',
        'Age_70-74': 'Idade Entre 70-74',
        'Age_75-79': 'Idade Entre 75-79',
        'Age_Mais de 80': 'Idade 80+'}, inplace=True)
    return df