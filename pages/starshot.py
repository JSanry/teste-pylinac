# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF

from pylinac import Starshot

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit.hello.utils import show_code
import pandas as pd


def show_SS():
   
    st.markdown("# StarShot 🎇")

    st.sidebar.header("Star Shot")

    #Parametros analise
    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=2.0, value=0.8)
    r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    dpi_inp = st.sidebar.number_input(label='DPI',step=1.0 ,format="%.1f",min_value=80.0, max_value=200.0, value=100.0)
    sid_inp = st.sidebar.number_input(label='SID (mm)',step=1.0 ,format="%.1f",min_value=700.0, max_value=1900.0, value=1000.0)
    r_input = st.sidebar.checkbox (label="Recursivo", value= True)
    multiple = st.sidebar.checkbox (label="Multiplas imagens", value= False)

    Logo =st.sidebar.checkbox( label= 'Logo no PDF', value= True)

    #upload imagem
    #analise da imagem

    if multiple:
        star_img = st.file_uploader('upload', accept_multiple_files=True, label_visibility= "hidden")
    else:
        star_img = st.file_uploader(label="upload", label_visibility= "hidden")

    if star_img is not None and not(multiple):
        my_star = Starshot(star_img, dpi=dpi_inp, sid=sid_inp)
        my_star.analyze(radius=r, tolerance=tol, recursive=r_input)
        data = my_star.results_data()

        if data.passed:
            st.markdown("### Resultado Passou ")
        else:
            st.markdown("### Resultado Não Passou! ")

        #Resultados  
    
        st.write("Círculo mínimo tem o diâmetro de" , "%.3f" %data.circle_diameter_mm, "mm")
        st.write("O centro do círculo ocorre em" , "%.1f" %data.circle_center_x_y[0], ",","%.1f" %data.circle_center_x_y[1])
        
        #Mostra imagens
        my_star.save_analyzed_image("mystar.png")
        img_star= Image.open('mystar.png')
        st.image(img_star, output_format="auto")
        
        #Definições para PDF e Registro
        st.title('Defenições PDF')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.selectbox('Unidade',('iX', '6EX', 'True Beam',"Outra opção..."), index= None)
            if Unit == "Outra opção...":
                Unit = st.text_input("Digite a Unidade...")

        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus', "Outra opção..."),index= None)
            if Fis == "Outra opção...":
                Fis = st.text_input("Digite o operador...")

        with col3:
            Par = st.selectbox('Parâmetro',('Gantry','Mesa', 'Col' ),index= None)

        dia = st.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%m-%d-%Y")

        if not Unit or not Par or not Fis:
            st.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'StarShot_' + Unit + '_' + Par + '_' + data_teste +'.pdf'
       
        #Gerar pdf
            if Logo:      
                my_star.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Parâmetro': Par, 'Data': data_teste, 'Raio Analise':r})
            else:
                my_star.publish_pdf(filename="res.pdf",open_file=False, metadata={'Físico': Fis, 'Unidade': Unit, 'Parâmetro': Par, 'Data': data_teste, 'Raio Analise':r})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.success("PDF gerado!")
            st.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')   
        
    
    elif star_img is not None and multiple and len(star_img)>=2:
        my_star = Starshot.from_multiple_images(star_img,dpi=dpi_inp, sid=sid_inp)
        my_star.analyze(radius=r, tolerance=tol, recursive=r_input)
        data = my_star.results_data()

        if data.passed:
            st.markdown("### Resultado Passou ")
        else:
            st.markdown("### Resultado Não Passou! ")

        #Resultados  
    
        st.write("Círculo mínimo tem o diâmetro de" , "%.3f" %data.circle_diameter_mm, "mm")
        st.write("O centro do círculo ocorre em" , "%.1f" %data.circle_center_x_y[0], ",","%.1f" %data.circle_center_x_y[1])
        
        #Mostra imagens
        my_star.save_analyzed_image("mystar.png")
        img_star= Image.open('mystar.png')
        st.image(img_star, output_format="auto")
        
        #Definições para PDF 
        st.sidebar.header("Definições PDF")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.sidebar.selectbox('Unidade',('iX', '6EX', 'True Beam',"Outra opção..."), index= None)
            if Unit == "Outra opção...":
                Unit = st.sidebar.text_input("Digite a Unidade...")

        with col2:
            Fis = st.sidebar.text_input("Físico", value="Físico" ,placeholder= "Fis")

        with col3:
            Par = st.sidebar.selectbox('Parâmetro',('Gantry','Mesa', 'Col' ),index= None)

        dia = st.sidebar.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%m-%d-%Y")

        if not Unit or not Par or not Fis:
            st.sidebar.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'StarShot_' + Unit + '_' + Par + '_' + data_teste +'.pdf'
       
        #Gerar pdf
            if Logo:      
                my_star.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Parâmetro': Par, 'Data': data_teste, 'Raio Analise':r})
            else:
                my_star.publish_pdf(filename="res.pdf",open_file=False, metadata={'Físico': Fis, 'Unidade': Unit, 'Parâmetro': Par, 'Data': data_teste, 'Raio Analise':r})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.sidebar.success("PDF gerado!")
            st.sidebar.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')   
        
       




        


