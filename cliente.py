import streamlit as st
import sqlite3
import bcrypt
import re


conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()


def pagina_meus_ingressos():
    st.header("Meus Ingressos")
    st.write("---")

    @st.dialog("Ingresso Detalhes")
    def info_ingresso(item):
        st.write(f"Descrição do Ingresso {item}")
        if st.button("Fechar"):
            st.rerun()

    ingressos = [
        {"nome": "Ingresso A", "evento": "Evento X", "data": "25/12/2025"},
        {"nome": "Ingresso B", "evento": "Evento Y", "data": "01/01/2026"}
    ]

    for ingresso in ingressos:
        st.write(f"**{ingresso['nome']}** - {ingresso['evento']} - {ingresso['data']}")
        if st.button(f"Exibir informações do {ingresso['nome']}"):
            info_ingresso(ingresso['nome'])
        st.write("---")


def pagina_area_alimentos():
    st.header("Área de Alimentos")
    tab1, tab2, tab3 = st.tabs(["Cardápio", "Carrinho", "Retirar"])

    with tab1:
        cardapio = [
            {"nome": "Hambúrguer", "preco": 20.0, "categoria": "Lanches",
             "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
             "descricao": "Hambúrguer artesanal com queijo e bacon."},
            {"nome": "Pizza", "preco": 35.0, "categoria": "Lanches",
             "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
             "descricao": "Pizza de mussarela com borda recheada."},
            {"nome": "Refrigerante", "preco": 5.0, "categoria": "Bebidas",
             "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
             "descricao": "Lata 350ml de refrigerante gelado."}
        ]

        categorias = ["Todos"] + sorted(set(item["categoria"] for item in cardapio))
        if "carrinho" not in st.session_state:
            st.session_state.carrinho = {item["nome"]: 0 for item in cardapio}

        filtro = st.selectbox("Filtrar por categoria", categorias)
        itens_filtrados = [item for item in cardapio if filtro == "Todos" or item["categoria"] == filtro]

        for item in itens_filtrados:
            col1, col2 = st.columns([1, 2])
            with col1: st.image(item["img"], width=120)
            with col2:
                st.markdown(f"### {item['nome']}")
                st.caption(f"R$ {item['preco']:.2f}")
                st.write(item["descricao"])
                if st.button("Adicionar ao Carrinho", type='primary', key=f"add_{item['nome']}"):
                    st.session_state.carrinho[item['nome']] += 1
                    st.success(f"{item['nome']} adicionado ao carrinho!")

    with tab2:
        st.subheader("Carrinho")
        itens = [{"Alimento": alimento, "Quantidade": quantidade} for alimento, quantidade in st.session_state.carrinho.items() if quantidade > 0]
        if not itens:
            st.info("Carrinho vazio.")
        else:
            for item in itens:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"""
                    <div style="background-color:#262730; padding:15px; border-radius:10px;">
                        <strong>{item['Alimento']}</strong><br>
                        Quantidade: {item['Quantidade']}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("+", key=f"mais_{item['Alimento']}"):
                        st.session_state.carrinho[item['Alimento']] += 1
                        st.rerun()
                with col3:
                    if st.button("-", key=f"menos_{item['Alimento']}"):
                        st.session_state.carrinho[item['Alimento']] = max(0, st.session_state.carrinho[item['Alimento']] - 1)
                        st.rerun()
            if st.button("Finalizar Compra"):
                st.success("Compra finalizada com sucesso!")

    with tab3:
        st.subheader("Retirar")
        st.write("Compra #99999 disponível para retirada.")


def pagina_central_eventos():
    st.header("Central de Eventos")
    tab1, tab2 = st.tabs(["Eventos Disponíveis", "Carrinho"])
    with tab1:

        eventos = [
            {
                "nome": f"Evento {i+1}",
                "data": f"{10+i}/08/2025",
                "local": "Local X",
                "descricao": "Descrição do evento",
                "imagem": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png"
            }
            for i in range(10)
        ]

        def criar_dialogo(evento):
            @st.dialog(evento["nome"])
            def detalhes():
                st.image(evento["imagem"], use_container_width=True)
                st.write(f"**Data:** {evento['data']}")
                st.write(f"**Local:** {evento['local']}")
                st.write(evento["descricao"])
                if st.button("Participar", type='primary', key=f"participar_{evento['nome']}"):
                    st.success(f"{evento['nome']} foi adicionado ao carrinho!")
            return detalhes
        
        st.write("### Eventos disponíveis")
        cols = st.columns(3)

        for i, evento in enumerate(eventos):
            with cols[i % 3]:
                st.image(evento["imagem"], use_container_width=True)
                st.markdown(f"**{evento['nome']}**")
                st.caption(f"{evento['data']} - {evento['local']}")
                if st.button("Ver mais detalhes", type='primary', key=f"detalhes_{evento['nome']}"):
                    criar_dialogo(evento)()

            if (i + 1) % 3 == 0:
                cols = st.columns(3)

    with tab2:

        # botar pra escolhar o tipo de ingresso

        st.subheader("Carrinho")
        carrinho = [
            {"Evento": "Evento 1", "Data": "10/08/2025", "Local": "Local X"},
            {"Evento": "Evento 2", "Data": "11/08/2025", "Local": "Local Y"}
        ]

        st.write("Itens no carrinho:")

        for item in carrinho:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background-color:#262730; padding:15px; border-radius:10px;">
                    <strong>{item['Evento']}</strong><br>
                    Quantidade: {item['Data']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("aumentar", key=f"add_{item}"):
                    # aumentar quantidade
                    pass
            
            with col3:
                if st.button("diminuir", key=f"remove_{item}"):
                    # diminuir quantidade
                    pass

        st.write("---")
        finalizar = st.button("Finalizar Compra")

        if finalizar:
            st.success("Compra finalizada com sucesso!")


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

    with col2:
        def mudarCadastrar():
            st.session_state.auth_user = "cadastrar"
            
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("###### Não possui conta?")
        with col4:
            st.button("Cadastrar", use_container_width=True, on_click=mudarCadastrar)


def checaLogin(email, senha):
    query = "SELECT Nome, Senha FROM Clientes WHERE Email = %s"
    cursor.execute(query, (email,))

    user_data = cursor.fetchone()

    if user_data is not None:
        nome, senha_bd = user_data
        senha_bytes = senha.encode('uft-8')
        if bcrypt.checkpw(senha_bytes, senha_bd):
            st.session_state.nome_cliente = nome
            st.session_state.role = "cliente"
            pass
        
        else:
            st.error("Senha inválida, tente novamente.")
            pass
    else:
        st.error("Esse email não está cadastrado em nossos sistemas.")
        pass


def ir_para_login():
    st.session_state.auth_user = "login"


def pagina_cadastrar():
    st.title("Cadastro")
    st.divider()
    
    nome = st.text_input("Insira seu nome")

    # só deixar entrar número
    cpf = st.text_input("Insira seu CPF")

    email = st.text_input("Insira seu email")

    data_nascimento = st.date_input("Insira sua data de nascimento")

    senha = st.text_input("Insira sua senha", type="password")

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
            "Voltar ao Login",
            on_click=ir_para_login
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
        ir_para_login()
    
    
    #### email
    
    # else:
    #     padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #     email_valido = bool(re.match(padrao, email))

    #     if not email_valido:
    #         #AVISAR QUE EMAIL FOI ESCRITO ERRADO
    #         pass


    ### senha
    senha_valida = True

    if len(senha) < 8:
        #AVISAR QUE DEVE TER NO MINIMO 8 CARACTER
        senha_valida = False

    if not re.search(r'[A-Z]', senha):
        #AVISAR QUE PRECISA TER UMA LETRA MAISCULA
        senha_valida = False

    if not re.search(r'[a-z]', senha):
        #AVISAR QUE PRECISA TER UMA LETRA MINUSCULA
        senha_valida = False

    if not re.search(r'\d', senha):
        #AVISAR QUE PRECISA TER UM DIGITO
        senha_valida = False

    if not re.search(r'[\W_]', senha):
        #AVISAR QUE PRECISA DE CARACTER ESPECIAL
        senha_valida = False
        

if "role" not in st.session_state:
    st.session_state.role = None
if "auth_user" not in st.session_state:
    st.session_state.auth_user = "login"


if st.session_state.role is None:
    if st.session_state.auth_user == "login":
        pagina_login()
    elif st.session_state.auth_user == "cadastrar":
        pagina_cadastrar()


elif st.session_state.role == "cliente":
    nav = st.navigation([
        st.Page(pagina_meus_ingressos, title="Meus Ingressos", icon="🎟️"),
        st.Page(pagina_area_alimentos, title="Área de Alimentos", icon="🍔"),
        st.Page(pagina_central_eventos, title="Central de Eventos", icon="🎉"),
    ])
    nav.run()