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
                    "horario": "XX:XX",
                    "data": f"{10+i}/08/2025",
                    "local": f"Local {chr(65 + i)}",
                    "descricao": "Descrição do evento",
                    "imagem": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
                    "qntd_ingresos_disponiveis": 0,
                    "preco_ingressos": 0.1
                }
                for i in range(6)
            ]

        if "evento_editar_id" not in st.session_state:
            st.session_state.evento_editar_id = None

        if "evento_remover_id" not in st.session_state:
            st.session_state.evento_remover_id = None

        def salvar_edicao(evento_id, nome, data, local, descricao):
            # MODIFICAR NO BANCO DE DADOS
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
            # REMOVER NO BANCO DE DADOS
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

        # Diálogo de edição
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
        
        horario = 123132###ARRUMAR PRA COLOCAR O INPUT DE HORÁRIO   
        
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
            if st.button("Adicionar Evento", type="primary", use_container_width=True):
                salvarEventoBD(nome, horario, data, qntd_ingresso, descricao, imagem, local, valor_ingresso)


def salvarEventoBD(nome, horario, data, qntd_ingresso, descricao, imagem, local, valor_ingresso):
    conexao = sqlite3.connect('dados.db')
    cursor = conexao.cursor()
    
    cursor.execute('''
        INSERT INTO Eventos (Nome, Horario, Data, Qnt_Ingressos, Descricao, Imagem, Local)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, horario, data, qntd_ingresso, descricao, imagem, local))
    
    evento_id = cursor.lastrowid
    
    conexao.commit()
    
    st.success("Evento adicionado com sucesso!")
    st.session_state.eventos.append({
        "id": evento_id,
        "nome": nome,
        "horario": horario,
        "data": data,
        "qntd_ingresso": qntd_ingresso,
        "descricao": descricao,
        "imagem": imagem,
        "local": local
    })

    for i in range(qntd_ingresso):
        cursor.execute('''
            INSERT INTO Ingressos (Evento_ID, Valor)
            VALUES (?, ?)
        ''', (evento_id, valor_ingresso))
        
        conexao.commit()

def pagina_estatisticas_evento():
    st.header("Estatísticas do Evento")


def pagina_crud_alimentos():
    def salvarAlimentoBD(nome, preco, descricao, imagem):
        pass

    tab1, tab2 = st.tabs(["Editar/Remover Itens", "Adicionar Item"])

    with tab1:
        if "alimentos" not in st.session_state:
            st.session_state.alimentos = [
                {"id": 1, "qntd": 10, "nome": "Hambúrguer", "preco": 20.0, "categoria": "Lanches",
                    "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
                    "descricao": "Hambúrguer artesanal com queijo e bacon."},
                {"id": 2, "qntd": 15, "nome": "Pizza", "preco": 35.0, "categoria": "Lanches",
                    "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
                    "descricao": "Pizza de mussarela com borda recheada."},
                {"id": 3, "qntd": 23, "nome": "Refrigerante", "preco": 5.0, "categoria": "Bebidas",
                    "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
                    "descricao": "Lata 350ml de refrigerante gelado."}
            ]

        if "alimento_editar_id" not in st.session_state:
            st.session_state.alimento_editar_id = None

        if "alimento_remover_id" not in st.session_state:
            st.session_state.alimento_remover_id = None

        def salvar_edicao(alimento_id, nome, preco, qntd, descricao):
            # MODIFICAR NO BANCO DE DADOS
            for e in st.session_state.alimentos:
                if e["id"] == alimento_id:
                    e["nome"] = nome
                    e["preco"] = preco
                    e["qntd"] = qntd
                    e["descricao"] = descricao
                    break
            st.session_state.alimento_editar_id = None
            st.rerun()

        def remover_alimento(alimento_id):
            # REMOVER NO BANCO DE DADOS
            st.session_state.alimentos = [e for e in st.session_state.alimentos if e["id"] != alimento_id]
            st.session_state.alimento_remover_id = None
            st.rerun()

        # necessário?
        categorias = ["Todos"] + sorted(set(item["categoria"] for item in st.session_state.alimentos))
        if "carrinho" not in st.session_state:
            st.session_state.carrinho = {item["nome"]: 0 for item in st.session_state.alimentos}

        filtro = st.selectbox("Filtrar por categoria", categorias)
        itens_filtrados = [item for item in st.session_state.alimentos if filtro == "Todos" or item["categoria"] == filtro]

        for item in itens_filtrados:
            col1, col2 = st.columns([1, 2])
            with col1: st.image(item["img"], width=240)
            with col2:
                st.markdown(f"### {item['nome']}")
                st.caption(f"R$ {item['preco']:.2f}")
                st.caption(f"Quantidade - {item['qntd']}")
                st.write(item["descricao"])
                
                col3, col4 = st.columns(2)
                with col3:
                    if st.button("Editar", use_container_width=True, type='primary', key=f"add_{item['nome']}"):
                        st.session_state.alimento_remover_id = None
                        st.session_state.alimento_editar_id = item["id"]

                with col4:
                    if st.button("Remover", type='secondary', key=f"remove_{item['nome']}"):
                        st.session_state.alimento_editar_id = None
                        st.session_state.alimento_remover_id = item["id"]
        
        # Diálogo de edição
        if st.session_state.alimento_editar_id is not None:
            alimento = next(e for e in st.session_state.alimentos if e["id"] == st.session_state.alimento_editar_id)

            @st.dialog(f"Editar {alimento['nome']}")
            def editar():
                nome = st.text_input("Nome", value=alimento["nome"])
                
                # colocar apenas número
                preco = st.text_input("Preço", value=alimento["preco"])
                qntd = st.text_input("Quantidade", value=alimento["qntd"])
                descricao = st.text_area("Descrição", value=alimento["descricao"])

                if st.button("Salvar alterações", type="primary"):
                    salvar_edicao(alimento["id"], nome, float(preco), qntd, descricao)

            editar()
        
        # Diálogo de confirmar remoção
        if st.session_state.alimento_remover_id is not None:
            alimento = next(e for e in st.session_state.alimentos if e["id"] == st.session_state.alimento_remover_id)

            @st.dialog(f"Remover {alimento['nome']}?")
            def confirmar_remocao():
                st.warning("Tem certeza que deseja remover este alimento?")
                st.write(f"**Alimento:** {alimento['nome']}")
                st.write(f"**Preço:** {alimento['preco']}")
                st.write(f"**Quantidade:** {alimento['qntd']}")
                st.write(f"**Descrição:** {alimento['descricao']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("❌ Cancelar"):
                        st.session_state.alimento_remover_id = None
                        st.rerun()
                with col2:
                    if st.button("🗑️ Confirmar", type="primary"):
                        remover_alimento(alimento["id"])

            confirmar_remocao()
                
            
        with tab2:
            st.header("Adicionar Alimento")

            nome = st.text_input("Nome")
            
            # colocar pra número
            preco = st.text_input("Preço")  
            
            col1, col2 = st.columns(2)
            with col1:
                imagem = st.text_input("Imagem")
                
            with col2:
                st.write("Mostrar imagem")
                    
            descricao = st.text_area("Descrição")

            col3, col4, col5 = st.columns(3)
            with col4:
                if st.button("Adicionar", type="primary", use_container_width=True):
                    salvarAlimentoBD(nome, preco, descricao, imagem)
    

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