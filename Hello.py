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



import os
import streamlit as st
#from streamlit.logger import get_logger
from PIL import Image
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from streamlit_navigation_bar import st_navbar
#from streamlit_extras.colored_header import colored_header
from streamlit_extras.dataframe_explorer import dataframe_explorer



import pages as pg


st.set_page_config( page_title="Testes Pylinac",
        page_icon="📋",initial_sidebar_state="collapsed")

pages = ["StarShot", "Winston-Lutz", "Picket Fence", "Field Analysis", "Registro"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "logo.svg")
styles = {
    "nav": {
        #"background-color": "#e4e7ff", 
        "background-color": "#0099cc",
        "justify-content": "left",
        "primary-color": "#001cff"
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        #"color": "var(--text-color)",
        "color": "#0099cc",
        "font-weight": "bold",
        "padding": "14px",
    }
}
options = {
    "show_menu": True,
    "show_sidebar": True,
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
)

functions = {
    "Home": pg.show_home,
    "StarShot": pg.show_SS,
    "Winston-Lutz": pg.show_WL,
    "Picket Fence":pg.show_PF,
    "Field Analysis":pg.show_FA,
    "Registro":pg.show_registro,
}



go_to = functions.get(page)
if go_to:
    go_to()


    
#with st.sidebar:
#    st.write("Em desenvolvimento por João Rivera")
    