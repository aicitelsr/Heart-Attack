import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# função para Carregar o arquivo CSV em um dataframe pandas
def lerDataset():
    dataset = pd.read_csv("heart_disease.csv")
    return dataset

# função para Contar quantidade de linhas x colunas do dataset
def contarDataset(dataset):
    return (f'linhas e colunas: {dataset.shape}')

#  função para Visualizar colunas do dataset
def ColunasDataset(dataset):
    return dataset.columns

# função para conta quantidade de vezes que um elemento aparece na coluna
def RepetDataset(dataset, coluna):
    return dataset[coluna].value_counts()

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

# Interface stremalit
def main():
    # Titulo da tela
    st.title(' Análise exploratória ')

    # chamar minha função ler dataset
    dataset = lerDataset()

    # se o dataset nao estiver vazio
    if lerDataset is not  None:

        # contar quantidade de linhas x colunas
        st.write(contarDataset(dataset))

        # ler colunas do dataset
        st.write(ColunasDataset(dataset))

        # selecionar coluna para conta
        coluna_selecioanda = st.selectbox('Escolha uma coluna', dataset.columns)

        # contar repetição na coluna selecionada
        st.write(f'a frequencia da coluna selecionada é {RepetDataset(dataset,coluna_selecioanda)}')


        # numero de entradas unicas para cada caracteristica numerica
        entradaNumber(dataset)


# executar def main
if __name__ == '__main__':
    main()
