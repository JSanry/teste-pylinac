import streamlit as st


def show_home():
    st.sidebar.header("About")
    st.link_button("Linkedin", "https://streamlit.io/gallery")
    st.write("Em desenvolvimento projeto de TCR por João Rivera")


    st.header("Home")
    st.write(
        """
        Bem vindo,

        Esta site tem como objetivo ser uma interface prática de análise de alguns testes da radioterapia 
        do TG 142, implementando a partir das bibliotecas Pylinac e Streamlit.
        
                
        """
    )