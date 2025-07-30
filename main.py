# Para rodar, usar "python -m streamlit run main.py", caso não rode normalmente

import streamlit as st

# Iniciar telas
if 'telaLogin' not in st.session_state:
    st.session_state.telaLogin = True
    
if 'telaCadastrar' not in st.session_state:
    st.session_state.telaCadastrar = False
    
if 'telaCliente' not in st.session_state:
    st.session_state.telaCliente = False
    
if 'telaAdmin' not in st.session_state:
    st.session_state.telaAdmin = False  
    
    
def checarLogin(usuario, senha):
    # Valida informações no banco de dados e, caso sucesso, retorne se é admin ou cliente
    sucesso = True # temporário
    cliente = True # temporário
    admin = False # temporário
    if sucesso:
        if cliente:
            return "cliente"
        elif admin:
            return "admin"
    return None
        
if st.session_state.telaLogin:
    st.title("Bem-vindo")
    st.divider()
    st.markdown("### Login")
    
    usuario = st.text_input("## Usuário")
    senha = st.text_input("## Senha", type="password")

    col1, col2 = st.columns(2)
    
    with col1:
        # Deixar mais longo e colocar cor positiva
        login_button = st.button("Login")
        if login_button:
            resultado = checarLogin(usuario, senha)
            if resultado == "cliente":
                st.session_state.telaCliente = True
                st.session_state.telaLogin = False
            elif resultado == "admin":
                st.session_state.telaAdmin = True
                st.session_state.telaLogin = False
            else:
                st.error("Usuário ou senha incorretos.")

    with col2:
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("###### Não possui conta?")
        with col4:
            # Deixar mais longo e colocar cor que não chama atenção
            cadastrar_button = st.button("Cadastrar")
            if cadastrar_button:
                st.session_state.telaLogin = False
                st.session_state.telaCadastrar = True

elif st.session_state.telaCadastrar:
    st.title("Cadastrar")

elif st.session_state.telaCliente:
    st.title("Tela Cliente")

elif st.session_state.telaAdmin:
    st.title("Tela Admin")