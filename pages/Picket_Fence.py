from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt
import base64
import requests

#mod = "https://raw.githubusercontent.com/JSanry/teste-pylinac/main/picketfence.txt"
#mod_text = requests.get(mod)
#mod = "/mount/src/teste-pylinac/picketfence.txt"
#import pylinac.picketfence
#with open(mod_text,'r') as writer_file:
#    contents_to_write = writer_file.read()
#with open(pylinac.picketfence.__file__,'w') as file_to_overwrite:
#    file_to_overwrite.write(contents_to_write)

from pylinac.picketfence import PicketFence, MLCArrangement, MLC

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit.hello.utils import show_code
import pandas as pd


def show_PF():


    st.markdown("# Picket Fence 🚧")

    st.sidebar.header("Picket Fence")
    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.05, max_value=1.5, value=0.15)
    a_tol = st.sidebar.number_input(label='Ação de Tolerancia',step=0.05,format="%.2f",min_value=0.05, max_value=1.5, value=0.1)
    #r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    orient = st.sidebar.selectbox('Orientação',('Left-Right', 'Up-Down'))
    mlc = st.sidebar.selectbox('MLC',('Millennium80', 'Millennium','HD Millennium','B Mod','MLCI','Halcyon Distal','Halcyon Proximal','Agility'))
    prof =st.sidebar.checkbox('Plotar profile pior lamina')
    #names =st.sidebar.checkbox('Usar Nome de Arquivos')
    #mlc_ar = MLC.MILLENNIUM
    
    pfimg = st.file_uploader(label='upload', label_visibility = "hidden")
    
    if pfimg is not None:
        #mlc_Millennium80 = MLCArrangement(leaf_arrangement=[(80, 10)])
        
        if mlc== 'Millennium80':
            mlc_setup= MLCArrangement(leaf_arrangement=[(80, 10)])
        elif mlc == 'Millennium':
            mlc_setup= MLC.MILLENNIUM
        elif mlc == 'HD Millennium':
            mlc_setup= MLC.HD_MILLENNIUM
        elif mlc == 'B Mod':
            mlc_setup= MLC.BMOD
        elif mlc == 'Agility':
            mlc_setup= MLC.AGILITY    
        elif mlc == 'MLCI':
            mlc_setup= MLC.MLCI
        elif mlc == 'Halcyon Distal':
            mlc_setup= MLC.HALCYON_DISTAL
        elif mlc == 'Halcyon Proximal':
            mlc_setup= MLC.HALCYON_PROXIMAL

        pf = PicketFence(pfimg, mlc=mlc_setup )
        #pf = PicketFence(pf_img)
        pf.analyze(tolerance=tol, action_tolerance=a_tol, orientation=orient)
        #st.write(my_star.results())
        data = pf.results_data()
        if data.passed:
            st.markdown("### Resultado Passou ")
        else:
            st.markdown("### Resultado Não Passou! ")
           
        st.write("Porcentagem laminas passando:" , "%.3f" %data.percent_leaves_passing, "%")
        st.write("Erro absoluto médio:" , "%.3f" %data.absolute_median_error_mm, "mm")
        st.write("O erro máximo é:" , "%.3f" %data.max_error_mm, "mm, na lamina", "%.0f" %data.max_error_leaf, " no picket", "%.0f" %data.max_error_picket)
        
       
        
        pf.save_analyzed_image("pf.png")
        img_res= Image.open('pf.png')
        st.image(img_res, output_format="auto")

        if prof:
            pf.save_leaf_profile('profile.png', leaf=data.max_error_leaf, picket=data.max_error_picket)
            img_prof= Image.open('profile.png')
            st.image(img_prof, output_format="auto")
        
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
            nomepdf = 'PF_' + Unit + '_' + data_teste +'.pdf'
       
        #Gerar pdf
            
            pf.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/USER-JABS/logoDOR.png" , metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.sidebar.success("PDF gerado!")
            st.sidebar.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')
        
        
        
        


        

