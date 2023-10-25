
from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF

from pylinac import Starshot

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd

import controles.dadoscontroler as dadoscontroler
import models.Dados as dados

def Registro():
    with st.form(key="Registrar"):
        input_unid=  st.text_input(label="unidade")
        input_ope=  st.text_input(label="operador")
        input_res=  st.text_input(label="resultado")
        input_button_submit = st.form_submit_button("registrar")
      
    if input_button_submit:
        dados.undidade = input_unid
        dados.ope = input_ope
        dados.res = input_res

        dadoscontroler.incluir(dados)

st.set_page_config(page_title="registro", page_icon="🎇")



st.sidebar.header("Registro")

Registro()

show_code(Registro)