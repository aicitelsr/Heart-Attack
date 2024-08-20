from sklearn.model_selection import train_test_split
import pickle

# dividir em treino e teste

arq5 = open('heart.pkl', 'rb')
arq1 = open('heart.pkl', 'rb')

previsores2_esc = pickle.load(arq5)
alvo = pickle.load(arq1)

x_treino, x_teste, y_treino, y_teste = train_test_split(previsores2_esc, alvo, test_size=0.3, random_state=0)
x_treino.shape

# Modelo de regressão