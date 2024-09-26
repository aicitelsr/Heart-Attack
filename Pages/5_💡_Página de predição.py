import streamlit as st
import pickle
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier

with open('Models/catBoostBalanced.pkl', 'rb') as file:
    model = pickle.load(file)

colunas = [
    'Pressão alta', 'Colesterol alto', 'Checagem de colesterol',
    'Fumantes', 'AVC', 'Atividade física', 'Consumo de frutas', 'Consumo de legumes e verduras',
    'Alto consumo de álcool', 'Plano de saúde', 'Não visitou médico por custo', 'Saúde mental',
    'Saúde física', 'Dificuldade de andar', 'Sexo', 'IMC_Abaixo do peso', 'IMC_Obesidade Grau I',
    'IMC_Obesidade Grau II', 'IMC_Obesidade Grau III', 'IMC_Peso normal', 'IMC_Peso normal baixo',
    'IMC_Sobrepeso', 'Diabético_Diabético', 'Diabético_Não possui diabetes', 'Diabético_Pré-diabético',
    'Saúde geral_Boa', 'Saúde geral_Execelente', 'Saúde geral_Moderada', 'Saúde geral_Pobre',
    'Saúde geral_Ruim', 'Idade_18-24', 'Idade_25-29', 'Idade_30-34', 'Idade_35-39', 'Idade_40-44',
    'Idade_45-49', 'Idade_50-54', 'Idade_55-59', 'Idade_60-64', 'Idade_65-69', 'Idade_70-74',
    'Idade_75-79', 'Idade_80+', 'Formação_1-3 Superior', 'Formação_1-8 ano', 'Formação_12 ano/Médio completo',
    'Formação_4+ Superior', 'Formação_9-11 ano', 'Formação_Nunca foi a escola (ou apenas foi à pré-escola)',
    'Renda_10000-$14000', 'Renda_15000-$19999', 'Renda_20000-$24999', 'Renda_25000-$34999',
    'Renda_35000-$49999', 'Renda_50000-$74999', 'Renda_75000+', 'Renda_Menos de 10000'
]


def predict_heart_disease(inputs):
    dados = pd.DataFrame([inputs], columns=colunas)
    prediction = model['model'].predict(dados)
    return prediction


st.title("Predição de Doença Cardíaca")
st.write("Responda as perguntas abaixo para prever doenças cardíacas.")


variaveis = {
    "Pressão Alta": [["Sim", "Não"], "Você possui pressão alta? "],
    "Colesterol Alto": [["Sim", "Não"], "Você possui colesterol alto? "],
    "Check-up de Colesterol": [["Sim", "Não"], "Você checou o nível de colesterol nos últimos 5 anos? "],
    "Fumante": [["Sim", "Não"], "Você tem o hábito de fumar? "],
    "Histórico de AVC": [["Sim", "Não"], "Você tem histórico de AVC? "],
    "Atividade Física": [["Sim", "Não"], "Você possui o hábito de fazer atividade física? "],
    "Consumo de Frutas": [["Sim", "Não"], "Você possui o hábito de consumir frutas? "],
    "Consumo de Vegetais": [["Sim", "Não"], "Você possui o hábito de consumir vegetais?"],
    "Consumo Excessivo de Álcool": [["Sim", "Não"], "Você costuma beber mais de 14 drinks por semana? "],
    "Possui plano de saúde": [["Sim", "Não"], "Você possui alguma tipo de plano de saúde?"],
    "Não vistou o médico recentemente por custo": [["Sim", "Não"], "No útimo anos você quis visitar um médico mas não pôde por custo? "],
    "Saúde Mental nos últimos 30 dias": [("number", 0, 30), "Quantos dias esteve com a saúde mental ruim no último mês? "],
    "Saúde Física nos últimos 30 dias": [("number", 0, 30), "Quantos dias esteve com a saúde física ruim no último mês? "],
    "Dificuldade em Caminhar": [["Sim", "Não"], "Você possui dificuldade de locomoção? "],
    "Sexo": [["Masculino", "Feminino"], "Selecione o sexo: "],
    "IMC": [[
        "Abaixo do peso",
        "Obesidade Grau I",
        "Obesidade Grau II",
        "Obesidade Grau III",
        "Peso normal",
        "Peso normal baixo",
        "Sobrepeso",
    ], "Qual a sua categoria de IMC? "],
    "Faixas de diabetes": [[
        "Diabético",
        "Não possui diabetes",
        "Pré-diabético"], "Em que categoria voce se encaixa?"],
    "Saúde geral": [[
        "Boa",
        "Excelente",
        "Moderada",
        "Muito Ruim",
        "Ruim"
    ], "Em que categoria sua saúde geral se encaixa? "],
    "Faixa Etária": [[
        "18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
        "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 ou mais"], "Qual a faixa etária que você se enquadra? "],
    "Escolaridade": [[
        "Ensino superior (1-3 anos)",
        "Ensino fudamental II",
        "Ensino médio",
        "Ensino superior (4 anos +)",
        "Ensino fundamental I",
        "Nunca foi à escola ou apenas à pré escola",
    ], "Em relação à escolaridade, selecione a categoria que você se enquadra. "],
    "Renda Anual": [[
        "10000 - $14000",
        "15000 - $19999",
        "20000 - $24999",
        "25000 - $34999",
        "35000 - $49999",
        "50000 - $74999",
        "75000+",
        "Menos de $10000"], "Selecione sua faixa salarial anual ($):"]
}


def obter_entrada_usuario(variaveis):
    entrada = []
    for var, opcoes in variaveis.items():
        if var == 'Sexo':
            sexo_selecionado = st.selectbox(opcoes[1], options=opcoes[0])
            entrada.append(1 if sexo_selecionado == "Masculino" else 0)
        elif "Sim" in opcoes[0]:
            entrada.append(1 if st.selectbox(
                opcoes[1], options=opcoes[0]) == "Sim" else 0)
        elif isinstance(opcoes[0], tuple) and opcoes[0][0] == "number":
            valor_num = st.number_input(
                opcoes[1], min_value=opcoes[0][1], max_value=opcoes[0][2], value=0)
            entrada.append(valor_num)
        else:  # isinstance(opcoes, list):
            opcao_selecionada = st.selectbox(opcoes[1], options=opcoes[0])
            for opcao in opcoes[0]:
                entrada.append(1 if opcao == opcao_selecionada else 0)
    return entrada


entrada_usuario = obter_entrada_usuario(variaveis)

if st.button("Fazer Predição"):
    resultado = predict_heart_disease(entrada_usuario)
    if resultado == 1:
        st.write("**Predição de doença cardíaca: SIM**")
        st.write("Com base nos dados fornecidos, você possui **propensão de risco de doença cardíaca**. Recomendamos que você consulte um profissional de saúde para mais orientações.")
    else:
        st.write("**Predição de doença cardíaca: NÃO**")
        st.write("Com base nos dados informados, você possui **pouca propensão em desenvolver doenças cardíacas**. Continue com hábitos saudáveis e faça acompanhamentos médicos regularmente.")
