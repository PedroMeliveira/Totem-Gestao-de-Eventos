import streamlit as st
import sqlite3
import bcrypt


conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()


def pagina_selecionar_evento_admin():
    st.header("Selecionar Evento Admin")


def pagina_estatisticas_evento():
    st.header("Estatísticas do Evento")


def pagina_configurar_area_alimentos():
    st.header("Configurar Área de Alimentos")


def pagina_configurar_central_eventos():
    st.header("Configurar Central de Eventos")


def pagina_configurar_ingresso_especifico():
    st.header("Configurar Ingresso Específico")
    

def pagina_gerenciar_admins():
    st.header("Configurar admins")


def pagina_login():
    st.title("Bem-vindo")
    st.divider()
    st.markdown("### Login")
    email = st.text_input("Email")
    senha_digitada = st.text_input("Senha", type="password")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Login",
            use_container_width=True,
            type="primary",
            on_click=checaLogin,
            args=(email, senha_digitada)
        )


def checaLogin(email, senha):
    ### ARRUMAR PARA TABELA DE ADMINS
    query = "SELECT Nome, Senha FROM Clientes WHERE Email = %s"
    cursor.execute(query, (email,))

    user_data = cursor.fetchone()

    if user_data is not None:
        nome, senha_bd = user_data
        senha_bytes = senha.encode('uft-8')
        if bcrypt.checkpw(senha_bytes, senha_bd):
            st.session_state.nome_admin = nome
            st.session_state.role = "admin"
            pass
        
        else:
            st.error("Senha inválida, tente novamente.")
            pass
    else:
        st.error("Esse email não está cadastrado em nossos sistemas.")
        pass


def pagina_cadastrar():
    st.title("Cadastro")
    st.divider()
    
    nome = st.text_input("Insira seu nome")
    email = st.text_input("Insira seu email")
    data_nascimento = st.date_input("Insira sua data de nascimento")
    senha = st.text_input("Insira sua senha", type="password")
    
    cpf = "1" ### TESTE

    col1, col2, col3= st.columns(3)
    with col1:
        st.button(
            "Cadastro",
            use_container_width=True,
            type="primary",
            on_click=realizaCadastro,
            args=(nome, cpf, email, data_nascimento, senha)
        )
    
    with col3:
        st.button(
            "Voltar ao Dashboard",
            on_click=ir_para_dashboard
        )
        

def realizaCadastro(nome, cpf, email, data_nascimento, senha):
    query = "SELECT Email FROM Clientes WHERE Email = %s"
    cursor.execute(query, (email,))

    resultado = cursor.fetchone() 

    if resultado is not None:
        st.error("Esse email já está cadastrado, utilize outro email ou faça login.")
        pass

    else:
        senha_bytes = bcrypt.senha.encode('utf-8')
        sal = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, sal)

        cursor.execute("INSERT INTO Clientes (Nome, Data_Nasc, Email, Senha) VALUES (?, ?, ?, ?)" (nome, data_nascimento, email, senha_hash))
        conexao.commit()

        cliente_id = cursor.lastrowid()
        st.session_state.cliente_id = cliente_id
        ir_para_dashboard()


def ir_para_dashboard():
    st.session_state.auth_user = "login"
        
        
if "role" not in st.session_state:
    st.session_state.role = None
if "auth_user" not in st.session_state:
    st.session_state.auth_user = "login"


if st.session_state.role is None:
    if st.session_state.auth_user == "login":
        pagina_login()
    elif st.session_state.auth_user == "cadastrar":
        pagina_cadastrar()


elif st.session_state.role == "admin":
    nav = st.navigation([
        st.Page(pagina_selecionar_evento_admin, title="Selecionar Evento Admin", icon="📋"),
        st.Page(pagina_estatisticas_evento, title="Estatísticas do Evento", icon="📊"),
        st.Page(pagina_configurar_area_alimentos, title="Configurar Área de Alimentos", icon="🍽️"),
        st.Page(pagina_configurar_ingresso_especifico, title="Configurar Ingresso Específico", icon="🎫"),
        st.Page(pagina_configurar_central_eventos, title="Configurar Central de Eventos", icon="🛠️"),
        st.Page(pagina_gerenciar_admins, title="Gerenciar Admins", icon="🔧"),
    ],)
    nav.run()