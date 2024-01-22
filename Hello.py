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


import streamlit as st
from streamlit.logger import get_logger
from PIL import Image
from streamlit_gsheets import GSheetsConnection
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="TESTES Pylinac",
        page_icon="📋",
    )
    #image = Image.open('logoinrad.png')

    #st.image(image, caption='Sunrise by the mountains')
    st.write("# Registro dos Testes  📋")
    st.sidebar.success("Selecione Testes Acima")

    st.markdown(
        """
        Dados registrados dos testes
    """
    )

    # Constantes
    FISICOS = [
        "Manufacturer",
        "Distributor",
        "Wholesaler",
        "Retailer",
        "Service Provider",
    ]
    UNIDADE = [
        "Electronics",
        "Apparel",
        "Groceries",
        "Software",
        "Other",
    ]

    teste_dados = st.selectbox(
        "Escolha o teste",
        [
            "StarShot",
            "WinstonLutz",
            "PicketFence",
            "FieldAnalysis",
        ],
    )

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read(worksheet=teste_dados, usecols=list(range(8)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    action = st.selectbox(
        "Escolha uma ação",
        [
        
            "Ver todos dados",
            #"Dados novo teste",
            "Deletar dado",
        ],
    )

    if action == "Dados novo teste":
        st.markdown("Enter the details of the new vendor below.")
        with st.form(key="teste_form"):
            company_name = st.text_input(label="Company Name*")
            business_type = st.selectbox(
                "Business Type*", options=FISICOS, index=None
            )
            products = st.multiselect("Products Offered", options=UNIDADE)
            onboarding_date = st.date_input(label="Onboarding Date")

            st.markdown("**required*")
            submit_button = st.form_submit_button(label="Submit Vendor Details")

            if submit_button:
                if not company_name or not business_type:
                    st.warning("Ensure all mandatory fields are filled.")
                elif existing_data["Teste"].str.contains(company_name).any():
                    st.warning("A vendor with this company name already exists.")
                else:
                    teste_data = pd.DataFrame(
                        [
                            {
                                "Teste": company_name,
                                "Fisico": business_type,
                                "Aparelho": ", ".join(products),
                                "Dia": onboarding_date.strftime("%Y-%m-%d"),
                            }
                        ]
                    )
                    updated_df = pd.concat([existing_data, teste_data], ignore_index=True)
                    conn.update(worksheet=teste_dados, data=updated_df)
                    st.success("Registro feito!")

    # View All Vendors
    elif action == "Ver todos dados":
        st.dataframe(existing_data,hide_index=True)

    # Delete Vendor
    elif action == "Deletar dado":
        test_to_delete = st.selectbox(
            "Selecionar teste para deletar", options=existing_data["Cod"].tolist()
        )

        if st.button("Delete"):
            existing_data.drop(
                existing_data[existing_data["Cod"] == test_to_delete].index,
                inplace=True,
            )
            conn.update(worksheet=teste_dados, data=existing_data)
            st.success("Teste deletado!")






if __name__ == "__main__":
    run()

#rodar de qualquer lugar
#pip install --upgrade streamlit opencv-python
#streamlit run https://raw.githubusercontent.com/streamlit/demo-self-driving/master/streamlit_app.py
