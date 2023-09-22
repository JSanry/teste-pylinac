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

from pylinac import Starshot
#my_star = Starshot.from_demo_image()
#my_star.analyze(radius=0.85, tolerance=0.8)

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd


def StarShot():
    st.write("Here's our first attempt at using data to create a table:")
    st.write(pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [15, 25, 30, 40]
    }))

    #st.text_input("Tolerance", key="tolerancia")
    tol = st.sidebar.number_input(label='Tolerancia',step=0.05,format="%.2f",min_value=0.2, max_value=0.95, value=0.8)
    r = st.sidebar.number_input(label='Raio',step=0.05,format="%.2f",min_value=0.19, max_value=0.96, value=0.5)
    st.title('upload da imagem')
    star_img = st.file_uploader('upload')
    if star_img is not None:
        my_star = Starshot(star_img, dpi=100, sid=1000)
        my_star.analyze(radius=r, tolerance=tol)
        st.write(my_star.results())
        my_star.save_analyzed_image("mystar.png")
        img_star= Image.open('mystar.png')
        st.image(img_star, output_format="auto")
        my_star.publish_pdf(filename=nomepdf)
        #st.download_button('Download binary file', nome.pdf)
        #st

        

st.set_page_config(page_title="StarShot", page_icon="🎇")
st.markdown("# StarShot 🎇")
st.sidebar.header("StarShotFrame Demo")
st.write(
    """Teste"""
)

StarShot()

show_code(StarShot)
