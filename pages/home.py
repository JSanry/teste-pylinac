import streamlit as st


def show_home():
    st.sidebar.header("About")
    
    st.write("Projeto de  TCR em desenvolvimento por João Rivera")


    st.header("Home")
    st.write(
        """
        Bem vindo,

        Esta site tem como objetivo ser uma interface prática de análise de alguns testes da radioterapia 
        do TG 142, implementando a partir das bibliotecas Pylinac e Streamlit.
        Este projeto é fruto de um Trabalho de Conclusão de Residência de Física Médica em Radioterapia, 
        em desenvolvimento por João Rivera.
        """)
    st.markdown("Links")