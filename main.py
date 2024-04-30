import Paginas.page.telaJ as pgj
import Paginas.page.telaL as pgl
import Paginas.page.telaM as pgm
import Paginas.page.telaR as pgr
import streamlit as st
from streamlit_option_menu import option_menu as om
st.title('Tela Inicial')
with st.sidebar:
    escolha = om(menu_title="Páginas de Análises", options=['Tela L','Tela J','Tela M','Tela R'])
if escolha == 'Tela L':
        pgl.telaL()
if escolha == 'Tela J':
        pgj.telaJ()
if escolha == 'Tela M':
        pgm.telaM()
if escolha == 'Tela R':
        pgr.telaR()
