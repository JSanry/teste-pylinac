from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF

from pylinac.picketfence import PicketFence, MLCArrangement

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd


def PicketFence():

    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.05, max_value=1.5, value=0.15)
    a_tol = st.sidebar.number_input(label='Ação de Tolerancia',step=0.05,format="%.2f",min_value=0.05, max_value=1.5, value=0.1)
    #r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    orient = st.sidebar.selectbox('Orientação',('Left-Right', 'Up-Down'))
    #names =st.sidebar.checkbox('Usar Nome de Arquivos')
    mlc_ar = MLCArrangement(leaf_arrangement=[(80, 10)])
    st.title('upload da imagem')
    pf_img = st.file_uploader('upload')
    if pf_img is not None:
        pf= PicketFence(pf_img, mlc= mlc_ar)
        pf.analyze(tolerance=tol, action_tolerance=a_tol, orientation=orient)
        #st.write(my_star.results())
        data = pf.results_data()
        if data.passed:
            st.markdown("### Resultado Passou ")
        else:
            st.markdown("### Resultado Não Passou! ")
           
        st.write("Porcentagem laminas passando" , "%.3f" %data.percent_leaves_passing, "mm")
        #st.write("O centro do círculo ocorre em" , "%.1f" %data.circle_center_x_y[0], ",","%.1f" %data.circle_center_x_y[1])
        
        pf.save_analyzed_image("pf.png")
        img_res= Image.open('mystar.png')
        st.image(img_res, output_format="auto")

        # Cria MLC Millennium80
        #mlc_Millennium80 = MLCArrangement(leaf_arrangement=[(80, 10)])

        #pf = PicketFence(pfimg, mlc=mlc_Millennium80 )
        #pf.analyze( tolerance=0.15, action_tolerance=0.1, orientation='Left-Right')

        # print results to the console
        #print(pf.results())
        # view analyzed image
        #pf.plot_analyzed_image()
        #pf.plot_histogram()
        #pf.save_analyzed_image("PF.png")
        #Salva PDF
        #pf.plot_leaf_profile(leaf=48, picket=2)
        #pf.publish_pdf(filename="PFtest.pdf",logo="drive/MyDrive/Colab/logoinrad.png",open_file=True, metadata={'Físico': fisico, 'Unidade': 'iX', 'data' : today})
        
        st.title('Defenições PDF')
        
        col1, col2 = st.columns(2)
        with col1:
            Unit = st.selectbox('Unidade',('iX', '6EX', 'True Beam'))
        with col2:
            Fis = st.selectbox('Físico',('Laura', 'Victor', 'Marcus'))


        today = date.today()
        dia = st.date_input("Data de realização do teste:", value= date.today())    
        data_teste = dia.strftime("%d_%m_%Y")
        nomepdf = 'StarShot_' + Unit + Par + data_teste +'.pdf'
        #Gerar pdf
        printpdf = st.button("Gerar pdf")
        if printpdf:
            #img_logo= Image.open('logoinrad.png')
            pf.publish_pdf(filename="res.pdf",open_file=False, metadata={'Físico': Fis, 'Unidade': Unit})
            with open("res.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            st.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name=nomepdf,
                               mime='application/octet-stream')      

st.set_page_config(page_title="Picket Fence", page_icon="🎇")
st.markdown("# Picket Fence 🎇")
st.sidebar.header("Picket Fence")
#st.write("""Teste""")

PicketFence()

show_code(PicketFence)
