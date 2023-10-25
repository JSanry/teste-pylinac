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

    #df = conn.read()
    df = conn.read(
    worksheet="database",
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