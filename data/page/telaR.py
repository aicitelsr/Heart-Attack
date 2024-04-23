import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Função para exibir o boxplot da coluna selecionada
def exibir_boxplot(dataset, coluna_selecionada):
    # Verificar se a coluna selecionada existe no dataset
    if coluna_selecionada in dataset.columns:
        # Criar o gráfico de boxplot para a coluna selecionada
        fig, ax = plt.subplots(figsize=(12, 6))
        dataset[coluna_selecionada].plot(kind='box', ax=ax)
        ax.set_ylabel('Valor')
        ax.set_title(f'Boxplot da coluna "{coluna_selecionada}"')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.error('A coluna selecionada não existe no dataset.')

# função para Carregar o arquivo CSV em um dataframe pandas
def lerDataset():
    dataset = pd.read_csv("data/heart_disease.csv")
    return dataset

# função para Contar quantidade de linhas x colunas do dataset
def contarDataset(dataset):
    return dataset.shape

#  função para Visualizar colunas do dataset
def ColunasDataset(dataset):
    return dataset.columns

# função para conta quantidade de vezes que um elemento aparece na coluna
def RepetDataset(dataset, coluna):
    return dataset[coluna].value_counts()

# ler conteudo de uma coluna
def ConteudoColuna(dataset,coluna):
    # Obter os valores da coluna como uma lista
    valores = dataset[coluna].tolist()
    
    # Limitar a exibição a até 6 valores
    valores_limitados = valores[:10]

    # Criar uma lista de strings formatadas para cada par chave-valor
    formatado = [f"{index}: {valor}\n" for index, valor in enumerate(valores_limitados)]
    
    # Juntar as strings formatadas em uma única string separada por quebras de linha
    return '\n'.join(formatado)

# olhar cinco prmeiras linhas
def primeiras(dataset):
    return dataset.head()

# olhar cinco ultimas linhas
def ultimas(dataset):
    return dataset.tail()



# função para ler quantidade de entradas unicas numericas
def entradaNumber(datset):
    # selecionar colunas numericas
    numeral_colunas = datset.select_dtypes(include='number')

    # calcular o numero de valores unicos em cada coluna
    unique_values = numeral_colunas.nunique().sort_values()

    # Cria um gráfico de barras com os valores únicos por coluna
    unique_values.plot.bar(logy=True, figsize=(15, 4), title="Unique values per feature")
    
    # Configurações adicionais do gráfico
    plt.xlabel("Feature")
    plt.ylabel("Unique Values")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Exibe o gráfico
    plt.show()

# Função para exibir o dicionario de texto
def ler_arquivo_txt(caminho_arquivo="data/dicionario.txt"):
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    return conteudo

# Interface stremalit
def main():
    # Titulo da tela
    st.title(' Análise exploratória ')

    # chamar minha função ler dataset
    dataset = lerDataset()

    # se o dataset nao estiver vazio
    if lerDataset is not  None:

        # contar quantidade de linhas x colunas
        st.write('Linha e colunas do dataset')
        st.write(contarDataset(dataset))

        # ler colunas do dataset
        st.write('Todas colunas do dataset')
        st.write(ColunasDataset(dataset))

        # selecionar coluna para conta
        st.write('Visualizar uma coluna:')
        coluna_selecionada = st.selectbox('Escolha uma coluna', dataset.columns)

        # contar repetição na coluna selecionada
        st.write(f'a frequencia da coluna selecionada é:') 
        st.write(f' \n {RepetDataset(dataset,coluna_selecionada)} ')
        # ler conteudo da coluna
        st.write('conteudo da coluna selecionada:')
        st.write(f'\n {ConteudoColuna(dataset,coluna_selecionada)}')

        # dicionario de termos tecnicos do dataset
        st.title(f'Dicionario informativo')

        #chamar def que ler o dicionario
        dicionario = ler_arquivo_txt()
        st.write(dicionario)

    
        st.write('As cinco primeiras linhas:')
        st.write(primeiras(dataset))

        st.write('As cinco últimas linhas:')
        st.write(ultimas(dataset))

        st.write('verificar existencia de valores nulos ')
        st.write(dataset.isnull().sum())

        st.write('verificar tipo de dados ')
        st.write(dataset.dtypes)

        st.write('Informações estatísticas')
        st.write(dataset.describe())

        st.write('Entendendo melhor as informações com plot')
        # Entendendo melhor as informações com plot
        if st.button('Exibir Boxplot'):
            exibir_boxplot(dataset, coluna_selecionada)

        st.write('Filtrar dados aparti de um intervalo')
        st.write(dataset[dataset[coluna_selecionada] >= 40]) # exemplo para coluna BMI


        # GRAFICO
        # numero de entradas unicas para cada caracteristica numerica 
        entradaNumber(dataset)

# executar def main
if __name__== '__main__':
    main()
