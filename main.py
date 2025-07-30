# Para rodar, usar "python -m streamlit run main.py", caso não rode normalmente

import streamlit as st

st.title("Bem-vindo")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Quem somos?")

with col2:
    st.markdown("### Login/Cadastrar")

    col3, col4 = st.columns(2)
    with col3:
        login_button = st.button("Login")
        
    with col4:
        cadastrar_button = st.button("Cadastrar")