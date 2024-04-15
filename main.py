import Pages.telaJ as pgj
import Pages.telaL as pgl
import Pages.telaM as pgm
import Pages.telaR as pgr
import streamlit as st
escolha = st.sidebar.selectbox('Selecione Algo', options=('Tela L','Tela J', 'Tela M','Tela R'))
if escolha == 'Tela L':
    pgl.telaL()
if escolha == 'Tela J':
    pgj.telaJ()
if escolha == 'Tela M':
    pgm.telaM()
if escolha == 'Tela R':
    pgr.telaR()