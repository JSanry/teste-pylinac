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
from streamlit.hello.utils import show_code
import pandas as pd


def Star_Shot():
    #st.write("Here's our first attempt at using data to create a table:")
    #st.write(pd.DataFrame({
    #    'first column': [1, 2, 3, 4],
    #    'second column': [15, 25, 30, 40]
    #}))

    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    st.title('Upload da imagem')
    star_img = st.file_uploader('upload')
    if star_img is not None:
        my_star = Starshot(star_img, dpi=100, sid=1000)
        my_star.analyze(radius=r, tolerance=tol)
        #st.write(my_star.results())
        data = my_star.results_data()
        if data.passed:
            st.markdown("### Resultado Passou ")
        else:
            st.markdown("### Resultado Não Passou! ")
           
        st.write("Círculo mínimo tem o diâmetro de" , "%.3f" %data.circle_diameter_mm, "mm")
        st.write("O centro do círculo ocorre em" , "%.1f" %data.circle_center_x_y[0], ",","%.1f" %data.circle_center_x_y[1])
        
        my_star.save_analyzed_image("mystar.png")
        img_star= Image.open('mystar.png')
        st.image(img_star, output_format="auto")
        
        st.title('Defenições PDF')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.selectbox('Unidade',('iX', '6EX', 'True Beam'))
        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus'))
        with col3:
            Par = st.selectbox('Parâmetro',('Gantry','Mesa', 'Col' ))

        today = date.today()
        dia = st.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%d_%m_%Y")
        nomepdf = 'StarShot_' + Unit + '_' + Par + '_' + data_teste +'.pdf'
        #Gerar pdf
        printpdf = st.button("Gerar pdf")
        if printpdf:
            #img_logo= Image.open('logoinrad.png')
            my_star.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Parâmetro': Par, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')      
            #teste

st.set_page_config(page_title="StarShot", page_icon="🎇")
logo_img= "https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" 
ycol, xcol = st.columns(2)
with ycol:
    st.markdown("# StarShot 🎇")
with xcol:
    st.image( logo_img, width= 250)
 


st.sidebar.header("StarShot")

Star_Shot()

show_code(Star_Shot)
