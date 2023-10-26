from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd
from streamlit_gsheets import GSheetsConnection


def incluir(dados):
        db.cursor.execute("""
		    INSERT INTO Dados(DadosUnidade, DadosFisico, DadosResultado) 
		    VALUES (?, ? ,?)""", (dados.unidade, dados.fisico, dados.resultado))
        db.con.commit()
    
class dados:
     def __init__(self, unidade, fisico, resultado):
        self.unidade = unidade
        self.fisico  = fisico
        self.resultado = resultado


def Tabela():

    
    with st.form(key="Registrar"):
        input_unid=  st.text_input(label="unidade")
        input_ope=  st.text_input(label="operador")
        input_res=  st.text_input(label="resultado")
        input_button_submit = st.form_submit_button("registrar")
      
    if input_button_submit:
        dados.undidade = input_unid
        dados.ope = input_ope
        dados.res = input_res

        incluir(dados)
    
    
    st.dataframe(db)


    
st.set_page_config(page_title="Tabela", page_icon="🗂")

# Create a connection object.
conn = st.experimental_connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1P5ggeEabQ3_WhO8io1RFwt1UBCJhw1oZzuw9TKfNi-k/edit#gid=0"
db = conn.read(
    spreadsheet= url,
    ttl= 0, #"10m",
    usecols=[0, 1, 2],
    nrows=4,)

st.sidebar.header("Tabela 🗂")

Tabela()

show_code(Tabela)