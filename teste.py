import streamlit as st

# Título da aplicação
st.title("Exemplo de Fontes no Streamlit")

# Texto em fontes diferentes
st.markdown("<h3 style='font-family:sans-serif;'>Texto com fonte Sans Serif</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='font-family:monospace;'>Texto com fonte Monospace</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='font-family:serif;'>Texto com fonte Serif</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='font-family:courier;'>Texto com fonte Courier</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='font-family:arial;'>Texto com fonte Arial</h3>", unsafe_allow_html=True)