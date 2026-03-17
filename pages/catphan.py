from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt


from pylinac import CatPhan503, CatPhan504, CatPhan600, CatPhan604

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit.hello.utils import show_code
import pandas as pd


def show_CP():


    st.markdown("# CatPhan ⚪")

    st.sidebar.header("CatPhan")

    type_catphan = st.sidebar.selectbox('CatPhan',('CatPhan503', 'CatPhan504', 'CatPhan600',  'CatPhan604'))
    
    img_cp = st.file_uploader('upload', accept_multiple_files=True, label_visibility= "hidden")

    if len(img_cp)<2:
        st.warning("Selecionar todas as imagens!")
    elif len(img_cp)>=2:
       
        if type_catphan == "CatPhan503":
            cat = CatPhan503(img_cp)

        elif type_catphan == "CatPhan604":
            cat = CatPhan604(img_cp)

        elif type_catphan == "CatPhan504":
            cat = CatPhan504(img_cp)
        else:
            cat = CatPhan600(img_cp)

        cat.analyze()
        st.write(cat.results())

        data = cat.results_data()

        #st.write("Porcentagem laminas passando:" , "%.3f" %data.ctp404.measured_slice_thickness_mm, "mm")



        cat.save_analyzed_image("cp.png")
        img_rescp= Image.open('cp.png')
        st.image(img_rescp, output_format="auto")


       
            
        #Definições para PDF 
        st.sidebar.header("Definições PDF")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.sidebar.text_input("Digite a máquina", value="Versa" ,placeholder= "Linac")

        with col2:
            Fis = st.sidebar.text_input("Digite o operador", value="Físico" ,placeholder= "Fis")

        with col3:
            dia = st.sidebar.date_input("Data de realização do teste:", value= date.today())    
            data_teste = dia.strftime("%m-%d-%Y")

        if not Unit or not Fis:
            st.sidebar.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'CatPhan_' + Unit + '_' + data_teste +'.pdf'
       
        #Gerar pdf
            
            cat.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/USER-EXT/logoP.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.sidebar.success("PDF gerado!")
            st.sidebar.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')
        
            
   

        

       
