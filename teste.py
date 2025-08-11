import streamlit as st

# Adicionando conteúdo inicial à sidebar
st.sidebar.title("Minha Sidebar")
st.sidebar.write("Alguns elementos na parte superior.")

# Usando CSS para adicionar margens e empurrar o botão para o final
st.markdown("""
    <style>
        .css-1d391kg .stButton {
            margin-top: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Botão no final
st.sidebar.button("Botão no final")

# https://www.youtube.com/watch?v=lrhT3fGU4aE