# Para rodar, usar "python -m streamlit run main.py", caso não rode normalmente

import streamlit as st

st.title("Bem-vindo")
st.divider()

st.markdown("### Login")

usuario = st.text_input("# Usuário")
senha = st.text_input("# Senha")

col1, col2 = st.columns(2)
with col1:
    # Deixar mais longo e colocar cor positiva
    login_button = st.button("Login")

with col2:
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("###### Não possui conta?")
    with col4:
        # Deixar mais longo e colocar cor que não chama atenção
        cadastrar_button = st.button("Cadastrar")