import streamlit as st


def show_home():
    st.sidebar.header("Sobre")
    
    st.sidebar.write("Projeto de  TCR em desenvolvimento por João Rivera")

    EMAIL='joaogrsantiago@gmail.com'
    url = "http://lattes.cnpq.br/6384119064417868"

    st.markdown("# Home")
    st.write(
        """
        Bem vindo,

        Este site tem como objetivo ser uma interface prática de análise de alguns testes da radioterapia 
        do Task Group 142, implementado a partir das bibliotecas Pylinac e Streamlit.
        
        Este projeto é fruto de um Trabalho de Conclusão de Residência de Física Médica em Radioterapia no instuto HCFMUSP, 
        em desenvolvimento por João Rivera.
        """)
    
    st.markdown("*Links:*")
    
    
    col1,col2, col3 = st.columns(spec=[0.35,0.2,0.3])
    with col2:
        st.link_button("Pylinac", "https://pylinac.readthedocs.io/en/latest/") 
        st.link_button("Streamlit", "https://docs.streamlit.io/")
    with col3:
        st.write("📫", EMAIL)
        st.write("📄 Currículo [Lattes](%s)" % url)
    with col1:
        st.image( htp, width= 220)
