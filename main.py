import streamlit as st

if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "login"

if 'cliente_pagina_selecionada' not in st.session_state:
    st.session_state.cliente_pagina_selecionada = "Meus Ingressos"

if 'admin_pagina_selecionada' not in st.session_state:
    st.session_state.admin_pagina_selecionada = "Selecionar Evento Admin"

if 'evento_admin_selecionado' not in st.session_state:
    st.session_state.evento_admin_selecionado = None


def mudar_pagina(nova_pagina):
    st.session_state.pagina_atual = nova_pagina

def mudar_pagina_cliente(nova_pagina):
    st.session_state.cliente_pagina_selecionada = nova_pagina

def mudar_pagina_admin(nova_pagina):
    st.session_state.admin_pagina_selecionada = nova_pagina

def handle_login(usuario, senha):
    resultado = checarLogin(usuario, senha)
    if resultado == "cliente":
        st.session_state.pagina_atual = "cliente"
    elif resultado == "admin":
        st.session_state.pagina_atual = "admin"
    else:
        st.error("Usuário ou senha incorretos.")

def handle_evento_admin_selecionado():
    if st.session_state.evento_admin_selecionado_box != "Selecione...":
        st.session_state.evento_admin_selecionado = st.session_state.evento_admin_selecionado_box
        st.session_state.admin_pagina_selecionada = "Estatísticas do Evento"


def checarLogin(usuario, senha):
    if usuario == "cliente" and senha == "123":
        return "cliente"
    elif usuario == "admin" and senha == "admin":
        return "admin"
    return None

def pagina_meus_ingressos():
    st.header("Meus Ingressos")

def pagina_area_alimentos():
    st.header("Área de Alimentos")
    tab1, tab2, tab3 = st.tabs(["Cardápio", "Carrinho", "Retirar"])
    
    with tab1:
        st.subheader("Cardápio")
        alimentos = ["Refrigerante", "Pipoca", "Cerveja"]
        for alimento in alimentos:
            with st.expander(alimento):
                st.title(f"Descrição do {alimento}")
                st.write("Preço: R$ 10.00")
                col3, col4 = st.columns(2)
                with col4:
                    st.button(f"Adicionar {alimento} ao carrinho")
    
    with tab2:
        st.subheader("Carrinho")
        itens = [
            {"Alimento": "Refrigerante", "Quantidade": 2},
            {"Alimento": "Pipoca", "Quantidade": 1}
        ]

        st.write("Itens no carrinho:")

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
                if st.button("aumentar", key=f"add_{item}"):
                    # aumentar quantidade
                    pass
            
            with col3:
                if st.button("diminuir", key=f"remove_{item}"):
                    # diminuir quantidade
                    pass

        st.write("---")
        st.button("Finalizar Compra")
            
    with tab3:
        st.subheader("Retirar")
        st.write("Compra 99999")

def pagina_central_eventos():
    st.header("Central de Eventos")

def pagina_selecionar_evento_admin():
    st.header("Selecione um Evento para Gerenciar")

    eventos_disponiveis = ["Show Rock Brasil", "Festival de Cinema", "Conferência Tech"]
    st.selectbox(
        "Escolha um evento",
        ["Selecione..."] + eventos_disponiveis,
        key="evento_admin_selecionado_box",
        on_change=handle_evento_admin_selecionado
    )
    
    st.markdown("---")
    st.button("Criar Novo Evento", on_click=mudar_pagina_admin, args=("CRUD Eventos",))

def pagina_estatisticas_evento():
    if st.session_state.evento_admin_selecionado:
        st.header(f"Estatísticas de {st.session_state.evento_admin_selecionado}")
        st.info("Total de ingressos vendidos: 1500, Receita total: R$ 75.000")
    else:
        st.warning("Nenhum evento selecionado. Por favor, selecione um evento na sidebar.")

def pagina_configurar_area_alimentos():
    if st.session_state.evento_admin_selecionado:
        st.header(f"Configurar Área de Alimentos - {st.session_state.evento_admin_selecionado}")
        st.subheader("CRUD de Alimentos")
        st.text_input("Nome do Alimento")
        st.number_input("Preço", min_value=0.01, format="%.2f")
        st.text_area("Descrição")
        col_crud_alimentos_1, col_crud_alimentos_2, col_crud_alimentos_3 = st.columns(3)
        with col_crud_alimentos_1: st.button("Adicionar Alimento")
        with col_crud_alimentos_2: st.button("Editar Alimento")
        with col_crud_alimentos_3: st.button("Deletar Alimento")

        st.subheader("Lista de Alimentos")
        st.table({"Alimento": ["Refrigerante", "Pipoca", "Cerveja"], "Preço": ["R$ 5.00", "R$ 10.00", "R$ 12.00"]})
    else:
        st.warning("Nenhum evento selecionado. Por favor, selecione um evento na sidebar.")

def pagina_configurar_central_eventos():
    st.header("Configurar Central de Eventos")
    st.subheader("CRUD de Eventos")
    st.text_input("Nome do Evento")
    st.date_input("Data do Evento")
    st.text_input("Local do Evento")
    col_crud_eventos_1, col_crud_eventos_2, col_crud_eventos_3 = st.columns(3)
    with col_crud_eventos_1: st.button("Adicionar Evento")
    with col_crud_eventos_2: st.button("Editar Evento")
    with col_crud_eventos_3: st.button("Deletar Evento")

    st.subheader("Lista de Eventos Existentes")
    st.table({"Evento": ["Show Rock Brasil", "Festival de Cinema"], "Data": ["2025-08-10", "2025-09-20"]})

def pagina_configurar_ingresso_especifico():
    if st.session_state.evento_admin_selecionado:
        st.header(f"Configurar Ingresso Específico - {st.session_state.evento_admin_selecionado}")
        st.subheader("Tipos de Ingresso")
        st.text_input("Nome do Tipo de Ingresso (Ex: Pista, Camarote)")
        st.number_input("Preço Base", min_value=0.01, format="%.2f", key="preco_ingresso")
        st.number_input("Quantidade Disponível", min_value=1, step=1, key="qtd_ingresso")
        col_ingresso_1, col_ingresso_2, col_ingresso_3 = st.columns(3)
        with col_ingresso_1: st.button("Adicionar Tipo de Ingresso")
        with col_ingresso_2: st.button("Editar Tipo de Ingresso")
        with col_ingresso_3: st.button("Deletar Tipo de Ingresso")

        st.subheader("Lotes de Ingressos")
        st.text_input("Nome do Lote (Ex: Lote 1, Promocional)")
        st.number_input("Preço do Lote", min_value=0.01, format="%.2f", key="preco_lote")
        st.number_input("Quantidade do Lote", min_value=1, step=1, key="qtd_lote")
        st.date_input("Data de Início da Venda")
        st.date_input("Data de Fim da Venda")
        col_lote_1, col_lote_2, col_lote_3 = st.columns(3)
        with col_lote_1: st.button("Adicionar Lote")
        with col_lote_2: st.button("Editar Lote")
        with col_lote_3: st.button("Deletar Lote")

        st.subheader("Lista de Tipos de Ingresso e Lotes")
        st.table({
            "Tipo": ["Pista", "Camarote"],
            "Preço": ["R$ 50.00", "R$ 150.00"],
            "Disponível": ["1000", "200"]
        })
    else:
        st.warning("Nenhum evento selecionado. Por favor, selecione um evento na sidebar.")

def renderizar_login():
    st.title("Bem-vindo")
    st.divider()
    st.markdown("### Login")

    usuario = st.text_input("Usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Login",
            use_container_width=True,
            type="primary",
            on_click=handle_login,
            args=(st.session_state.login_usuario, st.session_state.login_senha)
        )

    with col2:
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("###### Não possui conta?")
        with col4:
            st.button("Cadastrar", use_container_width=True, on_click=mudar_pagina, args=("cadastrar",))

def renderizar_cadastro():
    st.title("Cadastrar Novo Usuário")
    st.button("Voltar para Login", on_click=mudar_pagina, args=("login",))

def renderizar_cliente():
    st.sidebar.title("Menu do Cliente")
    st.sidebar.write("---")

    opcoes_cliente = ["Meus Ingressos", "Área de Alimentos", "Central de Eventos"]
    
    selected_option = st.sidebar.radio(
        "Navegar", opcoes_cliente, index=opcoes_cliente.index(st.session_state.cliente_pagina_selecionada)
    )
    if selected_option != st.session_state.cliente_pagina_selecionada:
        st.session_state.cliente_pagina_selecionada = selected_option
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.title("Informações Pessoais")
    st.sidebar.write("Nome: Cliente Exemplo")
    st.sidebar.button("Sair", on_click=mudar_pagina, args=("login",))

    if st.session_state.cliente_pagina_selecionada == "Meus Ingressos":
        pagina_meus_ingressos()
    elif st.session_state.cliente_pagina_selecionada == "Área de Alimentos":
        pagina_area_alimentos()
    elif st.session_state.cliente_pagina_selecionada == "Central de Eventos":
        pagina_central_eventos()

def renderizar_admin():
    st.sidebar.title("Menu do Administrador")

    if st.session_state.evento_admin_selecionado:
        st.sidebar.subheader(f"Gerenciando: {st.session_state.evento_admin_selecionado}")
        opcoes_admin = [
            "Estatísticas do Evento",
            "Configurar Área de Alimentos",
            "Configurar Ingresso Específico",
            "Configurar Central de Eventos",
            "Selecionar Outro Evento"
        ]
        if st.sidebar.button("Estatísticas do Evento"):
            mudar_pagina_admin("Estatísticas do Evento")
        if st.sidebar.button("Configurar Área de Alimentos"):
            mudar_pagina_admin("Configurar Área de Alimentos")
        if st.sidebar.button("Configurar Ingresso Específico"):
            mudar_pagina_admin("Configurar Ingresso Específico")
        if st.sidebar.button("Configurar Central de Eventos"):
            mudar_pagina_admin("Configurar Central de Eventos")
        if st.sidebar.button("Selecionar Outro Evento"):
            st.session_state.evento_admin_selecionado = None
            mudar_pagina_admin("Selecionar Evento Admin")

    else:
        opcoes_admin = ["Selecionar Evento Admin", "Configurar Central de Eventos"]
        if st.sidebar.button("Selecionar Evento Admin"):
            mudar_pagina_admin("Selecionar Evento Admin")
        if st.sidebar.button("Configurar Central de Eventos"):
            mudar_pagina_admin("Configurar Central de Eventos")
    
    st.sidebar.markdown("---")
    st.sidebar.button("Sair (Admin)", on_click=mudar_pagina, args=("login",))
    
    if st.session_state.admin_pagina_selecionada == "Selecionar Evento Admin":
        pagina_selecionar_evento_admin()
    elif st.session_state.admin_pagina_selecionada == "Estatísticas do Evento":
        pagina_estatisticas_evento()
    elif st.session_state.admin_pagina_selecionada == "Configurar Área de Alimentos":
        pagina_configurar_area_alimentos()
    elif st.session_state.admin_pagina_selecionada == "Configurar Central de Eventos":
        pagina_configurar_central_eventos()
    elif st.session_state.admin_pagina_selecionada == "Configurar Ingresso Específico":
        pagina_configurar_ingresso_especifico()


if st.session_state.pagina_atual == "login":
    renderizar_login()
elif st.session_state.pagina_atual == "cadastrar":
    renderizar_cadastro()
elif st.session_state.pagina_atual == "cliente":
    renderizar_cliente()
elif st.session_state.pagina_atual == "admin":
    renderizar_admin()