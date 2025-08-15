import streamlit as st
import sqlite3
import bcrypt


conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()


def pagina_crud_eventos():
    tab1, tab2 = st.tabs(["Editar/Remover Evento", "Adicionar Evento"])
    with tab1:
        if "eventos" not in st.session_state:
            st.session_state.eventos = [
                {
                    "id": i,
                    "nome": f"Evento {i+1}",
                    "data": f"{10+i}/08/2025",
                    "local": f"Local {chr(65 + i)}",
                    "descricao": "Descrição do evento",
                    "imagem": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png"
                }
                for i in range(6)
            ]

        if "evento_editar_id" not in st.session_state:
            st.session_state.evento_editar_id = None

        if "evento_remover_id" not in st.session_state:
            st.session_state.evento_remover_id = None

        def salvar_edicao(evento_id, nome, data, local, descricao):
            for e in st.session_state.eventos:
                if e["id"] == evento_id:
                    e["nome"] = nome
                    e["data"] = data
                    e["local"] = local
                    e["descricao"] = descricao
                    break
            st.session_state.evento_editar_id = None
            st.rerun()

        def remover_evento(evento_id):
            st.session_state.eventos = [e for e in st.session_state.eventos if e["id"] != evento_id]
            st.session_state.evento_remover_id = None
            st.rerun()

        st.write("### Eventos disponíveis")
        eventos = st.session_state.eventos
        cols = st.columns(3)

        for i, evento in enumerate(eventos):
            with cols[i % 3]:
                st.image(evento["imagem"], use_container_width=True)
                st.markdown(f"**{evento['nome']}**")
                st.caption(f"{evento['data']} - {evento['local']}")

                with st.popover("Ver mais detalhes"):
                    st.image(evento["imagem"], use_container_width=True)
                    st.write(f"**Data:** {evento['data']}")
                    st.write(f"**Local:** {evento['local']}")
                    st.write(evento["descricao"])

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Editar", key=f"editar_{evento['id']}"):
                            st.session_state.evento_editar_id = evento["id"]
                    with col2:
                        if st.button("🗑️ Remover", key=f"remover_{evento['id']}"):
                            st.session_state.evento_remover_id = evento["id"]

        # Dialog de edição
        if st.session_state.evento_editar_id is not None:
            evento = next(e for e in st.session_state.eventos if e["id"] == st.session_state.evento_editar_id)

            @st.dialog(f"Editar {evento['nome']}")
            def editar():
                nome = st.text_input("Nome", value=evento["nome"])
                data = st.text_input("Data", value=evento["data"])
                local = st.text_input("Local", value=evento["local"])
                imagem = st.text_input("Imagem", value=evento["imagem"])
                descricao = st.text_area("Descrição", value=evento["descricao"])

                if st.button("Salvar alterações", type="primary"):
                    salvar_edicao(evento["id"], nome, data, local, imagem, descricao)

            editar()

        # Dialog de confirmação de remoção
        if st.session_state.evento_remover_id is not None:
            evento = next(e for e in st.session_state.eventos if e["id"] == st.session_state.evento_remover_id)

            @st.dialog(f"Remover {evento['nome']}?")
            def confirmar_remocao():
                st.warning("Tem certeza que deseja remover este evento?")
                st.write(f"**Evento:** {evento['nome']}")
                st.write(f"**Data:** {evento['data']}")
                st.write(f"**Local:** {evento['local']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("❌ Cancelar"):
                        st.session_state.evento_remover_id = None
                        st.rerun()
                with col2:
                    if st.button("🗑️ Confirmar remoção", type="primary"):
                        remover_evento(evento["id"])

            confirmar_remocao()


    with tab2:
        st.header("Adicionar Evento")

        nome = st.text_input("Nome")
        
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("Data")
            local = st.text_input("Local")
            
        with col2:
            imagem = st.text_input("Imagem")
        
            with st.popover("Ingressos"):
                col1, col2 = st.columns(2)
                with col1:
                    qntd_ingresso = st.text_input("Qntd de ingressos")
                
                with col2:
                    valor_ingresso = st.text_input("Valor do ingresso")
                
        descricao = st.text_area("Descrição")

        col3, col4, col5 = st.columns(3)
        with col4:
            if st.button("Adicionar Evento", type="primary"):
                salvarEventoBD(nome, data, local, descricao, qntd_ingresso, valor_ingresso)


def salvarEventoBD(nome, data, local, descricao, ingressos):
    pass


def pagina_estatisticas_evento():
    st.header("Estatísticas do Evento")


def pagina_crud_alimentos():
    st.header("CRUD Alimentos")
    

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
    cursor.execute("SELECT Nome, Senha FROM Admins WHERE Email = ?", (email,))

    user_data = cursor.fetchone()

    if user_data is not None:
        nome, senha_bd = user_data
        senha_bytes = senha.encode('utf-8')
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
    cursor.execute("SELECT Nome FROM Admins WHERE Email = ?" (email,))

    resultado = cursor.fetchone() 

    if resultado is not None:
        st.error("Esse email já está cadastrado, utilize outro email ou faça login.")
        pass

    else:
        senha_bytes = senha.encode('utf-8')
        sal = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, sal)

        cursor.execute("INSERT INTO Admins (Nome, Data_Nasc, Email, Senha) VALUES (?, ?, ?, ?)" (nome, data_nascimento, email, senha_hash))
        conexao.commit()

        admin_id = cursor.lastrowid()
        st.session_state.admin_id = admin_id
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
        st.Page(pagina_crud_eventos, title="CRUD Eventos", icon="📋"),
        st.Page(pagina_estatisticas_evento, title="Estatísticas do Evento", icon="📊"),
        st.Page(pagina_crud_alimentos, title="CRUD Alimentos", icon="🍽️"),
        st.Page(pagina_gerenciar_admins, title="Gerenciar Admins", icon="🛠️"),
    ],)
    nav.run()