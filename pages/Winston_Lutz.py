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

from pylinac.winston_lutz import WinstonLutz, MachineScale

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd


def show_WL():
    st.markdown("# Winston-Lutz 🎯")


    st.sidebar.header("Winston-Lutz")

    #tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    bib_size = st.sidebar.number_input(label='Bib Size mm',step=0.5,format="%.1f",min_value=0.1, max_value=15.0, value=2.0)
    unid = st.sidebar.selectbox('Unidade',('VARIAN', 'ELEKTA'))
    names =st.sidebar.checkbox('Usar Nome de Arquivos', value= True)

    
    st.sidebar.header("Coordenadas Inicias")
    VRT = st.sidebar.number_input(label='VRT',step=0.5,format="%.1f",min_value=-100.0, max_value=100.0, value=0.0)
    LNG = st.sidebar.number_input(label='LNG',step=0.5,format="%.1f",min_value=-100.0, max_value=100.0, value=0.0)
    LAT = st.sidebar.number_input(label='LAT',step=0.5,format="%.1f",min_value=-100.0, max_value=100.0, value=0.0)

    #col =st.sidebar.checkbox('Imagens Colimador')


    img_wl = st.file_uploader('upload', accept_multiple_files=True, label_visibility= "hidden")
    if len(img_wl)<2:
        st.warning("Selecionar todas as imagens!")
    elif len(img_wl)>=2:
        wl = WinstonLutz(img_wl,use_filenames=names)
        if unid == 'VARIAN':
            wl.analyze(bb_size_mm=bib_size, machine_scale= MachineScale.VARIAN_IEC)
        else:
            wl.analyze(bb_size_mm=bib_size, machine_scale= MachineScale.ELEKTA_IEC)
        data = wl.results_data() 

        wl.save_images("g.png", axis='Gantry')
        wl.save_images("c.png",axis='Collimator')
        wl.save_images("m.png", axis='Couch')
        wl.save_summary("s.png")
        
        img_s= Image.open('s.png')
        st.image(img_s, output_format="auto")

        inst= wl.bb_shift_instructions(couch_vrt=VRT, couch_lng=LNG, couch_lat=LAT)
        st.write(inst)
    
        

        img_g= Image.open('g.png')
        st.image(img_g, output_format="auto")
        img_c= Image.open('c.png')
        st.image(img_c, output_format="auto")
        img_m= Image.open('m.png')
        st.image(img_m, output_format="auto") 

    
        #Definições para PDF 
        st.sidebar.header("Definições PDF")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.sidebar.text_input("Digite a máquina", value="Linac" ,placeholder= "Linac")

        with col2:
            Fis = st.sidebar.text_input("Digite o operador", value="Físico" ,placeholder= "Fis")

        with col3:
            dia = st.sidebar.date_input("Data de realização do teste:", value= date.today())    
            data_teste = dia.strftime("%m-%d-%Y")

        if not Unit or not Fis:
            st.sidebar.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'WL_' + Unit + '_' + data_teste +'.pdf'
       
        #Gerar pdf
            
            wl.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.sidebar.success("PDF gerado!")
            st.sidebar.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')
            

