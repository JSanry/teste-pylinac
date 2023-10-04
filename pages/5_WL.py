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
import math

from pylinac.winston_lutz import WinstonLutz, MachineScale

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd


def WL():
    #st.write("Here's our first attempt at using data to create a table:")

    #tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    #r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    unid = st.sidebar.selectbox('Unidade',('ELEKTA_IEC', 'VARIAN_IEC'))
    names =st.sidebar.checkbox('Usar Nome de Arquivos')

    st.title('upload da imagens')
    img_wl = st.file_uploader('upload', accept_multiple_files=True)
    if img_wl is not None:
        wl = WinstonLutz(img_wl,use_filenames=names)
        machine='MachineScale.'+ unid
        wl.analyze(bb_size_mm=5, machine_scale=MachineScale.ELEKTA_IEC)
        data = wl.results_data()
        #if data.passed:
            #st.markdown("### Resultado Passou ")
        #else:
            #st.markdown("### Resultado Não Passou! ")
           
        #st.write("Círculo mínimo tem o diâmetro de" , "%.3f" %data.circle_diameter_mm, "mm")
        #st.write("O centro do círculo ocorre em" , "%.1f" %data.circle_center_x_y[0], ",","%.1f" %data.circle_center_x_y[1])

        wl.save_images("g.png", axis='Gantry')
        wl.save_images("c.png",axis='Collimator')
        wl.save_images("m.png", axis='Couch')
        wl.save_summary("s.png")
        
        img_s= Image.open('s.png')
        st.image(img_s, output_format="auto")

        
        #img_star= Image.open('mystar.png')
        #st.image(img_star, output_format="auto")
        
        t=[[],[],[],[],[],[]]
        soma=[0,0,0,0,0,0]

        for i in range(len(wl.images)):
            G = wl.images[i].gantry_angle
            C = wl.images[i].collimator_angle
            M = wl.images[i].couch_angle
            xV = wl.images[i].cax2bb_vector.x
            yV = wl.images[i].cax2bb_vector.y
            t[0].append(round(G,1))
            t[1].append(round(C,1))
            t[2].append(round(M,1))
            if M != 0:
                x=(round(xV*math.cos(math.radians(M))+yV*math.sin(math.radians(M)),4))
                y=(round(-xV*math.sin(math.radians(M))+yV*math.cos(math.radians(M)),4))
                z="--"
            elif G == 270 or G == 90:
                x="--"
                y=yV
                z=(round(-xV*math.sin(math.radians(G)),4))
            else:
                x=(round(xV,3))
                y=yV
                z="--"
            t[3].append(x)
            t[4].append(y)
            t[5].append(z)

            if x != "--":
                soma[0]+=x
                soma[1]+=1
            soma[2]+=y
            soma[3]+=1
            if z != "--":
                soma[4]+=z
                soma[5]+=1
        t[0].append("--")
        t[1].append("--")
        t[2].append("Média")
        t[3].append(round(soma[0]/soma[1],3))
        t[4].append(round(soma[2]/soma[3],3))
        t[5].append(round(soma[4]/soma[5],3))

        st.write(wl.bb_shift_instructions())

        tb = pd.DataFrame({
        'Gantry': t[0],
        'Colimador': t[1],
        'Mesa': t[2],
        'LAT x (mm)': t[3],
        'LONG y (mm)': t[4],
        'VERT z (mm)': t[5],
        })

        st.dataframe(tb,hide_index=True)

        img_g= Image.open('g.png')
        st.image(img_g, output_format="auto")
        img_c= Image.open('c.png')
        st.image(img_c, output_format="auto")
        img_m= Image.open('m.png')
        st.image(img_m, output_format="auto") 

        st.title('Defenições PDF')
        
        col1, col2 = st.columns(2)
        with col1:
            Unit = st.selectbox('Unidade',('iX', '6EX', 'True Beam'))
        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus'))

        #today = date.today()
        dia = st.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%d_%m_%Y")
        nomepdf = 'WL_' + Unit + '_' + data_teste +'.pdf'
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