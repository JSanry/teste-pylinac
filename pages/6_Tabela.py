import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd



def Tabela():
    # Display Title and Description
    st.title("Registro de Testes")

    # Constants
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
            "Teste",
            "Star",
        ],
    )

    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read(worksheet=teste_dados, usecols=list(range(4)), ttl=5)
    existing_data = existing_data.dropna(how="all")

    action = st.selectbox(
        "Escolha uma ação",
        [
            "Dados novo teste",
            "Ver todos dados",
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
        st.dataframe(existing_data)

    # Delete Vendor
    elif action == "Deletar dado":
        test_to_delete = st.selectbox(
            "Selecionar teste para deletar", options=existing_data["Teste"].tolist()
        )

        if st.button("Delete"):
            existing_data.drop(
                existing_data[existing_data["Teste"] == test_to_delete].index,
                inplace=True,
            )
            conn.update(worksheet=teste_dados, data=existing_data)
            st.success("Teste deletado!")

st.sidebar.header("Tabela")
#st.write("""Teste""")

Tabela()

#show_code(Tabela)
