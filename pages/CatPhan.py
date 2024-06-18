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

#import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
#from fpdf import FPDF
import math

from pylinac import CatPhan503, CatPhan504, CatPhan600 

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd


def show_CP():
    st.markdown("# CatPhan 🎯")


    st.sidebar.header("CatPhan")

    #tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    #bib_size = st.sidebar.number_input(label='Bib Size mm',step=0.5,format="%.1f",min_value=0.1, max_value=15.0, value=2.0)
    type_catphan = st.sidebar.selectbox('CatPhan',('503', '504', '600'))
    #names =st.sidebar.checkbox('Usar Nome de Arquivos', value= True)

    
    #VRT = st.sidebar.number_input(label='VRT',step=0.5,format="%.1f",min_value=-100.0, max_value=100.0, value=0.0)
    #LNG = st.sidebar.number_input(label='LNG',step=0.5,format="%.1f",min_value=-100.0, max_value=100.0, value=0.0)
    #LAT = st.sidebar.number_input(label='LAT',step=0.5,format="%.1f",min_value=-100.0, max_value=100.0, value=0.0)

    #col =st.sidebar.checkbox('Imagens Colimador')


    img_cp = st.file_uploader('upload', accept_multiple_files=True, label_visibility= "hidden")
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
        Unit = st.selectbox('Unidade',('iX', '6EX', 'True Beam'), index= None)
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

        #st.dataframe(tb,hide_index=True)
            

