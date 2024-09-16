import streamlit as st
import pickle
import pandas as pd

with open('knn_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict_heart_disease(features):
    df = pd.DataFrame([features], columns=[
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ])


    prediction = model.predict(df)
    return prediction[0]
