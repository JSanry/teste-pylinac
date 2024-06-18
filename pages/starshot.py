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

    #Parametros analise
    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.1, max_value=1.0, value=0.8)
    r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)

    Logo =st.sidebar.checkbox( label= 'Logo no PDF', value= True)

    #upload imagem
    #analise da imagem
    star_img = st.file_uploader(label="upload", label_visibility= "hidden")
    if star_img is not None:
        my_star = Starshot(star_img, dpi=100, sid=1000)
        my_star.analyze(radius=r, tolerance=tol)
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
        
        st.title('Registrar dados')
        # Estabelece conexao Google Sheets 
        conn = st.connection("gsheets", type=GSheetsConnection)   

        # Toma dados atuais
        existing_data = conn.read(worksheet="StarShot", usecols=list(range(6)), ttl=5)
        existing_data = existing_data.dropna(how="all")

        #botao registro
        registro_button = st.button("Registrar dados")

        if registro_button:
                #checar se campos necessarios preenchidos
                if not Unit or not Par or not Fis:
                    st.warning("Preencher campos de registro faltantes")
                # condiçao evitar registros repetidos - avaliar melhor forma de fazer
                #elif existing_data["Data"].str.contains(data_teste).any():
                #    st.warning("A vendor with this company name already exists.")
                else:
                    teste_data = pd.DataFrame(
                        [
                            {
                                "Data": data_teste,
                                "Parametro": Par,
                                "Diametro":  "%.3f" %data.circle_diameter_mm,
                                "RaioAnalise": r ,
                                "Aparelho": Unit ,
                                "Fisico": Fis,
                                
                            }
                        ]
                    )
                    updated_df = pd.concat([existing_data, teste_data], ignore_index=True)
                    conn.update(worksheet="StarShot", data=updated_df)
                    st.success("Registro feito!")






        


