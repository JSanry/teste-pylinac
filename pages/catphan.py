from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt


from pylinac import CatPhan503, CatPhan504, CatPhan600

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit.hello.utils import show_code
import pandas as pd


def show_CP():


    st.markdown("# CatPhan 🚧")

    type_catphan = st.sidebar.selectbox('CatPhan',('503', '504', '600'))
    
    img_cp = st.file_uploader('upload', accept_multiple_files=True, label_visibility= "hidden")

    if img_cp is not None:
        if type_catphan == "503":
            CP = CatPhan503(img_cp)
        elif type_catphan == "504":
            CP = CatPhan504(img_cp)
        else:
            CP = CatPhan600(img_cp)

        CP.analyze()
        st.write(CP.results())



        

        st.title('Defenições PDF')
            
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.selectbox('Unidade',('CT', 'True Beam'), index= None)
        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus'), index= None)
        with col3:
            dia = st.date_input("Data de realização do teste:", value= date.today())    
            data_teste = dia.strftime("%d_%m_%Y")

        if not Unit or not Fis:
            st.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'CP_' + Unit + '_' + data_teste +'.pdf'
            #Gerar pdf

            CP.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download PDF",
                                data=PDFbyte,
                                file_name=nomepdf,
                                mime='application/octet-stream') 
    
            
   

        

       
