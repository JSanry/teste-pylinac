from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt


from pylinac import ElektaLasVegas, LasVegas

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit.hello.utils import show_code
import pandas as pd


def show_LV():


    st.markdown("# Las Vegas 🎲")

    st.sidebar.header("Las Vegas")
    phantom = st.sidebar.selectbox('Phantom',('LasVegas','ElektaLasVegas'),index= 1)
    low_th = st.sidebar.number_input(label='low contrast threshold',step=0.05,format="%.3f",min_value=0.001, max_value=0.099, value=0.010)
    hg_th = st.sidebar.number_input(label='high  contrast threshold',step=0.05,format="%.2f",min_value=0.01, max_value=1.50, value=0.05)
    vs_th = st.sidebar.number_input(label='visibility threshold',step=1.0,format="%.1f",min_value=1.0, max_value=200.0, value=100.0)
    inv_input = st.sidebar.checkbox(label= 'Invert', value=False)
    ssd_auto = st.sidebar.checkbox(label= 'SSD auto', value=True)
    if ssd_auto:
        ssd_input= "auto"
    else:
        ssd_input = st.sidebar.number_input(label='SDD (mm)',step=1.0 ,format="%.1f",min_value=700.0, max_value=1900.0, value=1000.0)
    
    ang_input = st.sidebar.number_input(label='Angle (°)',step=1.0 ,format="%.1f",min_value=-360.0, max_value=360.0, value=0.0)

    
    img_lv = st.file_uploader('upload', label_visibility= "hidden")

    if img_lv is not None:  
        if phantom == ElektaLasVegas:
            las= ElektaLasVegas(img_lv)
        else:
            las= LasVegas(img_lv)

        las.analyze(low_contrast_threshold=low_th, high_contrast_threshold= hg_th, visibility_threshold= vs_th, ssd=ssd_input, angle_adjustment= ang_input, invert= inv_input)

        las.save_analyzed_image("img_lv_a")
        img_reslv= Image.open('img_lv_a.png')
        st.image(img_reslv, output_format="auto")

        st.sidebar.header("Definições PDF")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.sidebar.text_input("Digite a máquina", value="Linac" ,placeholder= "VersaHD")

        with col2:
            Fis = st.sidebar.text_input("Digite o operador", value="Físico" ,placeholder= "Fis")

        with col3:
            dia = st.sidebar.date_input("Data de realização do teste:", value= date.today())    
            data_teste = dia.strftime("%m-%d-%Y")

        if not Unit or not Fis:
            st.sidebar.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'LasVegas_' + Unit + '_' + data_teste +'.pdf'
       
        #Gerar pdf
            
            las.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/USER-JABS/logoDOR.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.sidebar.success("PDF gerado!")
            st.sidebar.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')
            
      
        
            
   

        

       
