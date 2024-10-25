from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt


from pylinac import LasVegas

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit.hello.utils import show_code
import pandas as pd


def show_LV():


    st.markdown("# Las Vegas 🎲")

    st.sidebar.header("Las Vegas")
    low_th = st.sidebar.number_input(label='low contrast threshold',step=0.05,format="%.3f",min_value=0.001, max_value=0.099, value=0.010)
    hg_th = st.sidebar.number_input(label='high  contrast threshold',step=0.05,format="%.2f",min_value=0.01, max_value=1.50, value=0.05)
    ssd_auto = st.sidebar.checkbox(label= 'SSD auto', value=True)
    if ssd_auto:
        ssd_input= "auto"
    else:
        ssd_input = st.sidebar.number_input(label='SDD (mm)',step=1.0 ,format="%.1f",min_value=700.0, max_value=1900.0, value=1000.0)

    
    img_lv = st.file_uploader('upload', label_visibility= "hidden")

    if img_lv is not None:  
        las= LasVegas(img_lv)
        las.analyze(low_contrast_threshold=low_th, high_contrast_threshold= hg_th, ssd=ssd_input)

        las.save_analyzed_image("img_lv_a")
        img_reslv= Image.open('img_lv_a')
        st.image(img_reslv, output_format="auto")


        st.title('Defenições PDF')
            
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.selectbox('Unidade',('iX', 'True Beam'), index= None)
        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus'), index= None)
        with col3:
            dia = st.date_input("Data de realização do teste:", value= date.today())    
            data_teste = dia.strftime("%d_%m_%Y")

        if not Unit or not Fis:
            st.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'LasVegas_' + Unit + '_' + data_teste +'.pdf'

            las.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download PDF",
                                data=PDFbyte,
                                file_name=nomepdf,
                                mime='application/octet-stream') 
        
            
   

        

       
