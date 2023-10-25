from urllib.error import URLError

import altair as alt
import pandas as pd
from PIL import Image
from datetime import date
from fpdf import FPDF

from pylinac import Starshot

import streamlit as st
from streamlit.hello.utils import show_code
import pandas as pd
from streamlit_gsheets import GSheetsConnection


def Tabela():

    # Create a connection object.
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    url = "https://docs.google.com/spreadsheets/d/1P5ggeEabQ3_WhO8io1RFwt1UBCJhw1oZzuw9TKfNi-k/edit#gid=0"
    #df = conn.read()
    df = conn.read(
    spreadsheet= url,
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)

    # Print results.
    for row in df.itertuples():
        st.write(f"{row.name} has a :{row.pet}:")
    
st.set_page_config(page_title="registro", page_icon="🎇")



st.sidebar.header("Tabela")

Tabela()

show_code(Tabela)