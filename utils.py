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
