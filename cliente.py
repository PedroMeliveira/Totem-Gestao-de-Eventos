import re
import bcrypt
import sqlite3
import streamlit as st
from datetime import date


# PÁGINAS DO CLIENTE


def pagina_meus_ingressos():
    st.header("Meus Ingressos")
    st.write("---")

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT I.ID, E.Nome, E.Data, E.Local
        FROM Ingressos I
        JOIN Eventos E ON I.Evento_ID = E.ID
        WHERE I.Cliente_ID = ?
    """, (st.session_state.cliente_id,))
    ingressos = cursor.fetchall()

    if not ingressos:
        st.info("Você ainda não possui ingressos.")
        return

    @st.dialog("Ingresso Detalhes")
    def info_ingresso(evento, data, local):
        st.write(f"**Evento:** {evento}")
        st.write(f"**Data:** {data}")
        st.write(f"**Local:** {local}")
        if st.button("Fechar"):
            st.rerun()

    for ingresso in ingressos:
        _, evento, data, local = ingresso
        st.write(f"**{evento}** - {data} - {local}")
        if st.button(f"Exibir informações do {evento}"):
            info_ingresso(evento, data, local)
        st.write("---")


def pagina_area_alimentos():
    st.header("Área de Alimentos")
    tab1, tab2, tab3 = st.tabs(["Cardápio", "Carrinho", "Retirar"])

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT Nome, Preco, Categoria, Imagem, Descricao, Quantidade FROM Alimentos")
    linhas = cursor.fetchall()

    cardapio = []

    for l in linhas:
        item = {
            "nome": l[0],
            "preco": l[1],
            "categoria": l[2],
            "img": l[3],
            "descricao": l[4],
            "quantidade": l[5]
        }
        cardapio.append(item)

    with tab1:
        categorias = ["Todos"] + sorted(set(item["categoria"] for item in cardapio))
        if "carrinho" not in st.session_state:
            st.session_state.carrinho = {item["nome"]: 0 for item in cardapio}

        filtro = st.selectbox("Filtrar por categoria", categorias)
        itens_filtrados = [item for item in cardapio if filtro == "Todos" or item["categoria"] == filtro]

        for item in itens_filtrados:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(item["img"], width=250)
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
                    st.write(f"**{item['Alimento']}** - Quantidade: {item['Quantidade']}")
                with col2:
                    if st.button("+", key=f"mais_{item['Alimento']}"):
                        st.session_state.carrinho[item['Alimento']] += 1
                with col3:
                    if st.button("-", key=f"menos_{item['Alimento']}"):
                        st.session_state.carrinho[item['Alimento']] = max(0, st.session_state.carrinho[item['Alimento']] - 1)
            if st.button("Finalizar Compra"):
                st.success("Compra finalizada com sucesso!")

    with tab3:
        st.subheader("Retirar")
        st.write("Compra disponível para retirada.")


def pagina_central_eventos():
    st.header("Central de Eventos")
    tab1, tab2 = st.tabs(["Eventos Disponíveis", "Carrinho"])
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    with tab1:
        cursor.execute("SELECT Nome, Data, Local, Descricao, Imagem FROM Eventos")
        linhas = cursor.fetchall()

        eventos = []

        for l in linhas:
            evento = {
                "nome": l[0],
                "data": l[1],
                "local": l[2],
                "descricao": l[3],
                "imagem": l[4]
            }
            eventos.append(evento)

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
        st.subheader("Carrinho")
        st.info("Carrinho de eventos em construção.")


# LOGIN E CADASTRO


def pagina_login():
    st.title("Bem-vindo")
    st.divider()
    st.markdown("### Login")
    email = st.text_input("Email", key="login_email", autocomplete="off")
    senha_digitada = st.text_input("Senha", type="password", key="login_senha", autocomplete="off")

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
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    
    query = "SELECT ID, Nome, Senha FROM Clientes WHERE Email = ?"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()

    if not email or not senha:
        st.error("Por favor, preencha todos os campos.")
        return

    if user_data is not None:
        cliente_id, nome, senha_bd = user_data
        senha_bytes = senha.encode('utf-8')
        if bcrypt.checkpw(senha_bytes, senha_bd):
            st.session_state.cliente_id = cliente_id
            st.session_state.nome_cliente = nome
            st.session_state.auth_user = "autenticado"
        else:
            st.error("Senha inválida, tente novamente.")
    else:
        st.error("Esse email não está cadastrado em nossos sistemas.")


def ir_para_login():
    st.session_state.auth_user = "login"


def pagina_cadastrar():
    st.title("Cadastro")
    st.divider()
    
    resultado_email = False
    resultado_senha = False
    
    nome = st.text_input("Insira seu nome", key="cadastro_nome", autocomplete="off")

    col1, col2 = st.columns(2)
    with col1:
        cpf = st.text_input("Insira seu CPF", key="cadastro_cpf", autocomplete="off")
    with col2:
        data_nascimento = st.date_input("Insira sua data de nascimento", format='DD/MM/YYYY', min_value=date(1945, 12, 31))
        
    email = st.text_input("Insira seu email", key="cadastro_email", autocomplete="off")
    if len(email) != 0:
        resultado_email = validaEmail(email)
        
    senha = st.text_input("Insira sua senha", type="password", key="cadastro_senha", autocomplete="off")
    if len(senha) != 0:
        resultado_senha = validaSenha(senha)

    col1, col2, col3= st.columns(3)
    with col1:
        def erroCadastro(nome, cpf, email, senha):
            if len(nome) == 0 or len(cpf) == 0 or len(email) == 0 or len(senha) == 0:
                return "Preencha todos os campos"
            return "Algumas informações estão inválidas"
            
        if resultado_email and resultado_senha:
            if st.button("Cadastro", use_container_width=True, type="primary", key="cadastroInfoValidas"):
                realizaCadastro(nome, cpf, email, data_nascimento, senha)
        else:
            if st.button("Cadastro", use_container_width=True, type="primary", key="cadastroInfoInvalidas"):
                mensagem = erroCadastro(nome, cpf, email, senha)
                if mensagem != "":
                    st.error(mensagem)
    
    with col3:
        st.button(
            "Voltar ao Login",
            on_click=ir_para_login,
            use_container_width=True
        )


def validaEmail(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    email_valido = bool(re.match(padrao, email))

    if not email_valido:
        st.error("Insira um email válido. Exemplo: nome@email.com")
        return False
    return True


def validaSenha(senha):
    senha_valida = True
    mensagem = ""

    if len(senha) < 8:
        mensagem += "A senha deve ter 8 ou mais dígitos\n"
        senha_valida = False

    if not re.search(r'[A-Z]', senha):
        mensagem += "\nA senha precisa ter ao menos uma letra maiúscula\n"
        senha_valida = False

    if not re.search(r'[a-z]', senha):
        mensagem += "\nA senha precisa ter ao menos uma letra minúscula\n"
        senha_valida = False

    if not re.search(r'\d', senha):
        mensagem += "\nA senha precisa ter ao menos um dígito\n"
        senha_valida = False

    if not re.search(r'[\W_]', senha):
        mensagem += "\nA senha precisa ter ao menos um carácter especial\n"
        senha_valida = False
    
    if senha_valida:
        return True
    st.error(mensagem)
    return False


def realizaCadastro(nome, cpf, email, data_nascimento, senha):
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    
    cursor.execute("SELECT Email FROM Clientes WHERE Email = ?", (email,))
    resultado = cursor.fetchone() 

    if resultado is not None:
        st.error("Esse email já está cadastrado, utilize outro email ou faça login.")
    else:
        senha_bytes = senha.encode('utf-8')
        sal = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, sal)

        cursor.execute("INSERT INTO Clientes (Nome, CPF, Data_Nasc, Email, Senha) VALUES (?, ?, ?, ?, ?)",
                       (nome, cpf, data_nascimento, email, senha_hash))
        conexao.commit()

        cliente_id = cursor.lastrowid
        st.session_state.cliente_id = cliente_id
        ir_para_login()


# LÓGICA TROCAR DE PÁGINAS AUTENTIFICADORAS


if "auth_user" not in st.session_state:
    st.session_state.auth_user = "login"

if st.session_state.auth_user == "login":
    pagina_login()
elif st.session_state.auth_user == "cadastrar":
    pagina_cadastrar()
elif st.session_state.auth_user == "autenticado":
    nav = st.navigation([
        st.Page(pagina_meus_ingressos, title="Meus Ingressos", icon="🎟️"),
        st.Page(pagina_area_alimentos, title="Área de Alimentos", icon="🍔"),
        st.Page(pagina_central_eventos, title="Central de Eventos", icon="🎉"),
    ])
    nav.run()