from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF
import matplotlib.pyplot as plt


import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd

from pylinac import FieldAnalysis, Protocol, Centering, Edge, Normalization, Interpolation, DeviceFieldAnalysis


def show_FA():
    st.markdown("# Field Analysis  🔲 ")


    st.sidebar.header("Field Analysis")
 

    protocol = st.sidebar.selectbox('Protocolo',('VARIAN', 'ELEKTA'))
    col_a, col_b = st.columns(2)
    with col_a:
        a=st.sidebar.number_input(label='Penumbra',step=10.0,format="%.2f",min_value=10.0, max_value=90.0, value=20.0)
    with col_b:
        b=st.sidebar.number_input(label='Penumbra',step=10.0,format="%.2f",min_value=11.0, max_value=100.0, value=80.0)

    ratio_field = st.sidebar.number_input(label='in field ratio',step=0.1,format="%.2f",min_value=0.05, max_value=0.95, value=0.8)

    interpol = st.sidebar.selectbox('Interpolação',('Linear', 'Spline'))
    interpol_res =st.sidebar.number_input(label='Resolução Interpolação',step=0.1,format="%.2f",min_value=0.05, max_value=1.5, value=0.1)
    edge = st.sidebar.selectbox('Detecção borda',('Inflexão Derivada', 'Inflexão Hill', 'FWHM'))

    fff =st.sidebar.checkbox('Campo FFF')

    inv_input = st.sidebar.checkbox (label="Inverted", value= False)

    if protocol=="VARIAN":
        var_protocolo= Protocol.VARIAN
    else:
        var_protocolo= Protocol.ELEKTA

    if interpol == "Linear":
        var_interpol= Interpolation.LINEAR
    else:
        var_interpol= Interpolation.SPLINE
    
    if edge == "Inflexão Derivada":
        var_edge = Edge.INFLECTION_DERIVATIVE
    elif edge == "Inflexão Hill":
        var_edge = Edge.INFLECTION_HILL
    else:
        var_edge = Edge.FWHM

    img_F = st.file_uploader('upload',label_visibility= "hidden")
    
    if img_F is not None:  
        fa=FieldAnalysis(img_F)
        fa.analyze(
        protocol=var_protocolo,
        centering=Centering.BEAM_CENTER,
        penumbra=(a, b),
        interpolation=var_interpol,
        interpolation_resolution_mm= interpol_res,
        edge_detection_method= var_edge,   
        is_FFF=fff,
        in_field_ratio= ratio_field,
        invert= inv_input
        )

        data = fa.results_data()
        
        col1, col2, col3 = st.columns(3)
        with col1:
             st.write("Campo Horizontal:" , "%.3f" %data.field_size_horizontal_mm, "mm")
             st.write("Campo Vertical:" , "%.3f" %data.field_size_vertical_mm, "mm")
        with col2:
             st.write("Planura Horizontal:" , "%.3f" %data.protocol_results["flatness_vertical"])
             st.write("Planura Vertical:" , "%.3f" %data.protocol_results["flatness_horizontal"])
        with col3:
             st.write("Simetria Vertical:" , "%.3f" %data.protocol_results["symmetry_vertical"])
             st.write("Simetria Horizontal:" , "%.3f" %data.protocol_results["symmetry_horizontal"]) 


        #Definições para PDF 
        st.sidebar.header("Definições PDF")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            Unit = st.sidebar.text_input("Digite a máquina", value="Linac" ,placeholder= "Linac")

        with col2:
            Fis = st.sidebar.text_input("Digite o operador", value="Físico" ,placeholder= "Fis")
        
        with col3:
            var_campo = st.sidebar.number_input(label='Tamanho de campo',step=1,min_value=1, max_value=40, value=10)
            Campo= str(var_campo)+'x'+ str(var_campo)

        dia = st.sidebar.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%m-%d-%Y")

        if not Unit or not Fis:
            st.warning("Preencher campos de registro faltantes")
        else:
            nomepdf = 'Field_' + '_'+ Campo +'_' + Unit +'_' + data_teste +'.pdf'
        #Gerar pdf
            fa.publish_pdf(filename="res.pdf",open_file=False, logo="https://raw.githubusercontent.com/JSanry/teste-pylinac/USER/logoN.png", metadata={'Físico': Fis, 'Unidade': Unit, 'Data': data_teste, "Campo": Campo})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            
            st.sidebar.download_button(label="Download PDF",
                            data=PDFbyte,
                            file_name=nomepdf,
                            mime='application/octet-stream')    
        #s_img =st.checkbox('Imagens Separadas')
        #split= s_img

       
        
        
        #if not split:
        #   img_res= Image.open('r.png')
        #   st.image(img_res, output_format="auto")
        
        #else:
        #    img_res1= Image.open('rHorizontal Profile.png')
        #    img_res2= Image.open('rVertical Profile.png')
        #    img_res3= Image.open('rImage.png')

        #    col1, col2, col3 = st.columns(3)
        #    with col1:
        #        st.image(img_res1, output_format="auto")
        #    with col2:
        #        st.image(img_res2, output_format="auto")
        #    with col3:
        #        st.image(img_res3, output_format="auto")     


