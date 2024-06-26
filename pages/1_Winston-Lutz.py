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


def WL():
    #st.write("Here's our first attempt at using data to create a table:")

    #tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    bib_size = st.sidebar.number_input(label='Bib Size mm',step=0.5,format="%.1f",min_value=0.1, max_value=15.0, value=2.0)
    unid = st.sidebar.selectbox('Unidade',('VARIAN', 'ELEKTA'))
    names =st.sidebar.checkbox('Usar Nome de Arquivos', value= True)

    
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
        #Calula e plota tabela deslocamentos cada imagem
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
                if unid == 'VARIAN':    #coordenadas VARIAN 
                    x=(round(-xV*math.cos(math.radians(M))-yV*math.sin(math.radians(M)),4))
                else:   #coordenadas ELEKTA
                    x=(round(xV*math.cos(math.radians(M))+yV*math.sin(math.radians(M)),4))
                y=(round(-xV*math.sin(math.radians(M))+yV*math.cos(math.radians(M)),4))
                z="--"
            #elif G == 270 or G == 90:
            else:
                x=(round(-xV*math.cos(math.radians(G)),4))
                y=yV
                z=(round(-xV*math.sin(math.radians(G)),4))
            #else:
            #    x=(round(xV,3))
            #    y=yV
            #    z="--"
            t[3].append(x)
            t[4].append(y)
            t[5].append(z)

            if x != "--" and x != 0:
                soma[0]+=x
                soma[1]+=1
            soma[2]+=y
            soma[3]+=1
            if z != "--" and z != 0:
                soma[4]+=z
                soma[5]+=1
        t[0].append("--")
        t[1].append("--")
        t[2].append("Média")
        t[3].append(round(soma[0]/soma[1],2))
        t[4].append(round(soma[2]/soma[3],2))
        try:
            t[5].append(round(soma[4]/soma[5],2))
        except:
            t[5].append(round(soma[4],2))
        tb = pd.DataFrame({
        'Gantry': t[0],
        'Colimador': t[1],
        'Mesa': t[2],
        'LAT x (mm)': t[3],
        'LONG y (mm)': t[4],
        'VERT z (mm)': t[5],
        })

        

        img_g= Image.open('g.png')
        st.image(img_g, output_format="auto")
        img_c= Image.open('c.png')
        st.image(img_c, output_format="auto")
        img_m= Image.open('m.png')
        st.image(img_m, output_format="auto") 

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
            nomepdf = 'WL_' + Unit + '_' + data_teste +'.pdf'
        #Gerar pdf

            wl.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream') 

        st.dataframe(tb,hide_index=True)
            
   
st.set_page_config(page_title="Winston-Lutz", page_icon="🎯")

logo_img= "https://raw.githubusercontent.com/JSanry/teste-pylinac/main/logoinrad.png" 
st.logo(logo_img)

col1, col2, col3, col4, col5 = st.columns(spec=[0.16,0.16,0.2,0.19,0.2])
with col1:
    if st.button("📋Registro"):
        st.switch_page("Hello.py")
with col2:
    if st.button("🎇Star Shot"):
        st.switch_page("pages/0_StarShot.py")
with col3:
    if st.button("🎯Winston-Lutz"):
        st.switch_page("pages/1_Winston-Lutz.py")
with col4:
    if st.button("🚧Picket Fence"):
        st.switch_page("pages/2_Picket_Fence.py")
with col5:
    if st.button("🔲Field Analysis"):
        st.switch_page("pages/3_Field_Analysis.py")
st.header('', divider="blue")
st.markdown("# Winston-Lutz 🎯")


st.sidebar.header("Winston-Lutz")
#st.write("""Teste""")

WL()

show_code(WL)
