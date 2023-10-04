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

from pylinac.winston_lutz import WinstonLutz, MachineScale

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd


def WL():
    #st.write("Here's our first attempt at using data to create a table:")
    #st.write(pd.DataFrame({
    #    'first column': [1, 2, 3, 4],
    #    'second column': [15, 25, 30, 40]
    #}))

    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    st.title('upload da imagens')
    img_wl = st.file_uploader('upload', accept_multiple_files=True)
    if img_wl is not None:
        wl = WinstonLutz(img_wl,use_filenames=True)
        wl.analyze(bb_size_mm=5, machine_scale=MachineScale.ELEKTA_IEC)
        data = wl.results_data()
        #if data.passed:
            #st.markdown("### Resultado Passou ")
        #else:
            #st.markdown("### Resultado Não Passou! ")
           
        #st.write("Círculo mínimo tem o diâmetro de" , "%.3f" %data.circle_diameter_mm, "mm")
        #st.write("O centro do círculo ocorre em" , "%.1f" %data.circle_center_x_y[0], ",","%.1f" %data.circle_center_x_y[1])
        
        #my_star.save_analyzed_image("mystar.png")
        #img_star= Image.open('mystar.png')
        #st.image(img_star, output_format="auto")
        
        st.title('Defenições PDF')
        
        col1, col2 = st.columns(2)
        with col1:
            Unit = st.selectbox('Unidade',('iX', '6EX', 'True Beam'))
        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus'))

        #today = date.today()
        dia = st.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%d_%m_%Y")
        nomepdf = 'WL_' + Unit + data_teste +'.pdf'
        #Gerar pdf
        printpdf = st.button("Gerar pdf")
        if printpdf:
            #img_logo= Image.open('logoinrad.png')
            wl.publish_pdf(filename="res.pdf",open_file=False, metadata={'Físico': Fis, 'Unidade': Unit})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')      

st.set_page_config(page_title="Winston-Lutz", page_icon="🎯")
st.markdown("# Winston-Lutz 🎯")
st.sidebar.header("Winston-Lutz")
#st.write("""Teste""")

WL()

show_code(WL)
