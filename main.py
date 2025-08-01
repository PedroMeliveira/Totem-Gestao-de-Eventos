# Para rodar, usar "python -m streamlit run main.py", caso não rode normalmente

import streamlit as st

# Iniciar telas
if 'telaLogin' not in st.session_state:
    st.session_state.telaLogin = True

if 'telaCadastrar' not in st.session_state:
    st.session_state.telaCadastrar = False

if 'telaCliente' not in st.session_state:
    st.session_state.telaCliente = False
    st.session_state.cliente_pagina_selecionada = "Selecionar Evento"

if 'telaAdmin' not in st.session_state:
    st.session_state.telaAdmin = False


def checarLogin(usuario, senha):
    # Valida informações no banco de dados e, caso sucesso, retorna se é admin ou cliente
    if usuario == "cliente" and senha == "123":
        return "cliente"
    elif usuario == "admin" and senha == "admin":
        return "admin"
    return None

def pagina_selecionar_evento():
    st.header("Selecione um Evento")

def pagina_meus_ingressos():
    st.header("Meus Ingressos")

def pagina_area_alimentos():
    st.header("Área de Alimentos")

def pagina_central_eventos():
    st.header("Central de Eventos")


# --- Lógica de renderização das telas ---

if st.session_state.telaLogin:
    st.title("Bem-vindo")
    st.divider()
    st.markdown("### Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)

    with col1:
        login_button = st.button("Login", use_container_width=True, type="primary")
        if login_button:
            resultado = checarLogin(usuario, senha)
            if resultado == "cliente":
                st.session_state.telaCliente = True
                st.session_state.telaLogin = False
                st.rerun()
            elif resultado == "admin":
                st.session_state.telaAdmin = True
                st.session_state.telaLogin = False
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    with col2:
        st.markdown("###### Não possui conta?")
        cadastrar_button = st.button("Cadastrar", use_container_width=True)
        if cadastrar_button:
            st.session_state.telaLogin = False
            st.session_state.telaCadastrar = True
            st.rerun()

elif st.session_state.telaCadastrar:
    st.title("Cadastrar Novo Usuário")
    st.write("Formulário de cadastro será implementado aqui.")

    # novo_usuario = st.text_input("Nome de Usuário")
    # nova_senha = st.text_input("Nova Senha", type="password")
    # if st.button("Registrar"):
    #     # Lógica para salvar no banco de dados
    #     st.success("Usuário cadastrado com sucesso!")
    #     st.session_state.telaCadastrar = False
    #     st.session_state.telaLogin = True
    #     st.rerun()

    if st.button("Voltar para Login"):
        st.session_state.telaCadastrar = False
        st.session_state.telaLogin = True
        st.rerun()

elif st.session_state.telaCliente:
    st.sidebar.title("Menu do Cliente")
    opcoes = ["Selecionar Evento", "Meus Ingressos", "Área de Alimentos", "Central de Eventos"]
    st.session_state.cliente_pagina_selecionada = st.sidebar.radio(
        "Navegar", opcoes, index=opcoes.index(st.session_state.cliente_pagina_selecionada)
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("Sair"):
        st.session_state.telaCliente = False
        st.session_state.telaLogin = True
        st.rerun()

    if st.session_state.cliente_pagina_selecionada == "Selecionar Evento":
        pagina_selecionar_evento()
    elif st.session_state.cliente_pagina_selecionada == "Meus Ingressos":
        pagina_meus_ingressos()
    elif st.session_state.cliente_pagina_selecionada == "Área de Alimentos":
        pagina_area_alimentos()
    elif st.session_state.cliente_pagina_selecionada == "Central de Eventos":
        pagina_central_eventos()


elif st.session_state.telaAdmin:
    st.title("Tela do Administrador")
    if st.button("Sair (Admin)"):
        st.session_state.telaAdmin = False
        st.session_state.telaLogin = True
        st.rerun()