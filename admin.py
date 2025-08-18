import os
import bcrypt
import sqlite3
import streamlit as st


conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()


def pagina_crud_eventos():
    tab1, tab2 = st.tabs(["Editar/Remover Evento", "Adicionar Evento"])
    with tab1:
        st.session_state.eventos = []
        conexao = sqlite3.connect('dados.db')
        cursor = conexao.cursor()   
        
        cursor.execute("SELECT ID, Nome, Horario, Data, Descricao, Imagem, Local FROM Eventos")
        eventos_bd = cursor.fetchall()
        
        for evento in eventos_bd:
            cursor.execute("SELECT ID, Cliente_ID, Valor FROM Ingressos WHERE Evento_ID = ?", (evento[0],))
            qntd_ingresso_disponiveis = 0
            ingressos_bd = cursor.fetchall()
            for ingresso in ingressos_bd:
                if ingresso[1] is None:
                    qntd_ingresso_disponiveis += 1
            
            evento_dict = {
                "id": evento[0],
                "nome": evento[1],
                "horario": evento[2],
                "data": evento[3],
                "descricao": evento[4],
                "imagem": evento[5],
                "local": evento[6],
                "qntd_ingresos_disponiveis": qntd_ingresso_disponiveis,
                "preco_ingressos": ingressos_bd[0][2]
            }
            
            st.session_state.eventos.append(evento_dict)

        if "evento_editar_id" not in st.session_state:
            st.session_state.evento_editar_id = None

        if "evento_remover_id" not in st.session_state:
            st.session_state.evento_remover_id = None

        def salvar_edicao(evento_id, nome, data, local, descricao):
            conexao = sqlite3.connect('dados.db')
            cursor = conexao.cursor()
            
            cursor.execute("UPDATE Eventos SET Nome=?, Data=?, Local=?, Descricao=? WHERE ID=?",
                        (nome, data, local, descricao, evento_id))
            
            conexao.commit()
            conexao.close()
            
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

                ###ATUALIZAR COM AS INFORMAÇÕES DO BD, QUAL INFORMAÇÃO QUER Q MUDE

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
        INSERT INTO Eventos (Nome, Horario, Data, Descricao, Imagem, Local)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, horario, data, descricao, imagem, local))
    
    evento_id = cursor.lastrowid
    
    conexao.commit()
    
    for i in range(qntd_ingresso):
        cursor.execute('''
            INSERT INTO Ingressos (Evento_ID, Valor)
            VALUES (?, ?)
        ''', (evento_id, valor_ingresso))
        
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


def pagina_estatisticas_evento():
    st.header("📊 Estatísticas")

    tab1, tab2 = st.tabs(["🍔 Alimentos", "🎟️ Ingressos"])

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    with tab1:
        st.subheader("Lanches mais vendidos")

        cursor.execute("""
            SELECT A.Nome, COUNT(AC.ID) AS Quantidade, SUM(A.Preco) AS Receita
            FROM Alimento_no_Carrinho AC
            JOIN Alimentos A ON AC.Alimento_ID = A.ID
            GROUP BY A.Nome
            ORDER BY Quantidade DESC
        """)
        resultados = cursor.fetchall()

        if resultados:
            for nome, quantidade, receita in resultados:
                st.markdown(f"**{nome}** - Vendidos: {quantidade} | Receita: R$ {receita:.2f}")
        else:
            st.info("Nenhum alimento vendido até agora.")

    with tab2:
        st.subheader("Ingressos por evento")

        # não tem outro jeito de conseguir os ingresso vendidos?
        cursor.execute("""
            SELECT E.Nome, COUNT(I.ID) AS Vendidos, SUM(I.Valor) AS Receita
            FROM Ingressos I
            JOIN Eventos E ON I.Evento_ID = E.ID
            WHERE I.Cliente_ID IS NOT NULL
            GROUP BY E.Nome
            ORDER BY Vendidos DESC
        """)
        resultados = cursor.fetchall()

        if resultados:
            for nome, vendidos, receita in resultados:
                st.markdown(f"**{nome}** - Vendidos: {vendidos} | Receita: R$ {receita:.2f}")
        else:
            st.info("Nenhum ingresso vendido até agora.")

    conexao.close()


def pagina_crud_alimentos():
    def salvarAlimentoBD(nome, preco, descricao, imagem, categoria, qntd):
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        
        cursor.execute('''
            INSERT INTO Alimentos (Nome, Preco, Descricao, Categoria, Imagem, Quantidade)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, preco, descricao, categoria, "temp", qntd))
        
        alimento_id = cursor.lastrowid

        if imagem:
            ext = os.path.splitext(imagem.name)[1]
            imagem_path = os.path.join("imagens/alimentos", f"alimento_{alimento_id}{ext}")
            
            with open(imagem_path, "wb") as f:
                f.write(imagem.getbuffer())
            
            cursor.execute("UPDATE Alimentos SET Imagem=? WHERE ID=?", (imagem_path, alimento_id))

        conexao.commit()
        conexao.close()


    def carregar_alimentos():
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        
        cursor.execute("SELECT ID, Nome, Preco, Descricao, Categoria, Imagem, Quantidade FROM Alimentos")
        dados = cursor.fetchall()
        conexao.close()

        alimentos = []
        for linha in dados:
            alimentos.append({
                "id": linha[0],
                "nome": linha[1],
                "preco": linha[2],
                "descricao": linha[3],
                "categoria": linha[4],
                "imagem": linha[5],
                "qntd": linha[6]
            })
            
        return alimentos


    tab1, tab2 = st.tabs(["Editar/Remover Itens", "Adicionar Item"])


    with tab1:
        if "alimentos" not in st.session_state:
            st.session_state.alimentos = carregar_alimentos()

        if "alimento_editar_id" not in st.session_state:
            st.session_state.alimento_editar_id = None

        if "alimento_remover_id" not in st.session_state:
            st.session_state.alimento_remover_id = None
        
        categorias_unicas = sorted(list(set(item['categoria'] for item in st.session_state.alimentos)))
        todas_categorias = ["Todas as Categorias"] + categorias_unicas
        
        st.subheader("Filtrar por Categoria")
        filtro_categoria = st.selectbox("", todas_categorias)
        
        st.markdown("---")

        alimentos_filtrados = st.session_state.alimentos
        
        if filtro_categoria != "Todas as Categorias":
            alimentos_filtrados = [item for item in alimentos_filtrados if item['categoria'] == filtro_categoria]
        
        if not alimentos_filtrados:
            st.info("Nenhum alimento encontrado com os filtros aplicados.")

        def salvar_edicao(alimento_id, nome, preco, qntd, imagem, descricao, categoria):
            for e in st.session_state.alimentos:
                if e["id"] == alimento_id:
                    e["nome"] = nome
                    e["preco"] = preco
                    e["qntd"] = qntd
                    e["imagem"] = imagem
                    e["descricao"] = descricao
                    e["categoria"] = categoria
                    break

            conexao = sqlite3.connect("dados.db")
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE Alimentos
                SET Nome=?, Preco=?, Descricao=?, Imagem=?, Categoria=?
                WHERE ID=?
            """, (nome, preco, descricao, imagem, categoria, alimento_id))
            conexao.commit()
            conexao.close()

            st.session_state.alimento_editar_id = None
            st.rerun()

        def remover_alimento(alimento_id):
            conexao = sqlite3.connect("dados.db")
            cursor = conexao.cursor()
            
            cursor.execute("SELECT Imagem FROM Alimentos WHERE ID=?", (alimento_id,))
            resultado = cursor.fetchone()
            
            imagem_path = None
            if resultado and resultado[0]:
                imagem_path = resultado[0]

            cursor.execute("DELETE FROM Alimentos WHERE ID=?", (alimento_id,))
            conexao.commit()
            conexao.close()

            if imagem_path and os.path.exists(imagem_path) and imagem_path != "temp":
                try:
                    os.remove(imagem_path)
                except OSError as e:
                    st.error(f"Erro ao tentar excluir {imagem_path}")

            st.session_state.alimentos = [e for e in st.session_state.alimentos if e["id"] != alimento_id]
            st.session_state.alimento_remover_id = None
            st.rerun()

        for item in alimentos_filtrados:
            col1, col2 = st.columns([1, 2])
            with col1:
                if item.get("imagem") and os.path.exists(item["imagem"]):
                    st.image(item["imagem"], width=250)
            with col2:
                st.markdown(f"### {item['nome']}")
                st.caption(f"R$ {item['preco']:.2f}")
                st.caption(f"Quantidade - {item['qntd']}")
                st.caption(f"Categoria - {item.get('categoria', 'Não definida')}")
                st.write(item["descricao"])

                col3, col4 = st.columns(2)
                with col3:
                    if st.button("Editar", use_container_width=True, type='primary', key=f"edit_{item['id']}"):
                        st.session_state.alimento_remover_id = None
                        st.session_state.alimento_editar_id = item["id"]

                with col4:
                    if st.button("Remover", type='secondary', key=f"remove_{item['id']}"):
                        st.session_state.alimento_editar_id = None
                        st.session_state.alimento_remover_id = item["id"]

        # Diálogo de edição
        if st.session_state.alimento_editar_id is not None:
            alimento = next(e for e in st.session_state.alimentos if e["id"] == st.session_state.alimento_editar_id)

            @st.dialog(f"Editar {alimento['nome']}")
            def editar():
                nome = st.text_input("Nome", value=alimento["nome"])
                preco = st.number_input("Preço", value=float(alimento["preco"]), step=0.5)
                qntd = st.number_input("Quantidade", value=int(alimento["qntd"]), step=1)
                categoria = st.selectbox("Categoria", 
                                        ["Bebida", "Entrada", "Combos", "Principais"],
                                        index=["Bebida", "Entrada", "Combos", "Principais"].index(alimento.get("categoria", "Bebida")))
                descricao = st.text_area("Descrição", value=alimento["descricao"])

                st.write("Imagem atual:")
                if alimento.get("imagem") and os.path.exists(alimento["imagem"]):
                    st.image(alimento["imagem"], width=250)

                uploaded_file = st.file_uploader("Alterar imagem", 
                                                type=["jpg", "jpeg", "png"],
                                                key=f"edit_img_{alimento['id']}")
                imagem_path = alimento["imagem"]
                
                if uploaded_file:
                    os.makedirs("imagens/alimentos", exist_ok=True)
                    imagem_path = os.path.join("imagens/alimentos", uploaded_file.name)
                    
                    with open(imagem_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                        
                    st.image(imagem_path, caption="Nova imagem", width=250)

                if st.button("Salvar alterações", type="primary"):
                    salvar_edicao(alimento["id"], nome, preco, qntd, imagem_path, descricao, categoria)

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
                st.write(f"**Categoria:** {alimento.get('categoria', 'Não definida')}")
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

        if "chave" not in st.session_state:
            st.session_state.chave = 0

        nome = st.text_input("Nome", key=f"nome_{st.session_state.chave}")
        preco = st.number_input("Preço", min_value=0.0, step=0.5, key=f"preco_{st.session_state.chave}")
        qntd = st.number_input("Quantidade", min_value=1, step=1, key=f"qntd_{st.session_state.chave}")
        categoria = st.selectbox("Categoria", 
                                ["Bebida", "Entrada", "Combos", "Principais"], 
                                key=f"categoria_{st.session_state.chave}")

        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader("Upload da imagem", 
                                            type=["jpg", "jpeg", "png"], 
                                            key=f"file_{st.session_state.chave}")

        with col2:
            if uploaded_file:
                st.image(uploaded_file, caption="Pré-visualização", width=300)

        descricao = st.text_area("Descrição", key=f"desc_{st.session_state.chave}")

        col3, col4, col5 = st.columns(3)
        
        with col4:
            if st.button("Adicionar", type="primary", use_container_width=True):
                if not nome or preco is None or qntd is None or not categoria or not descricao:
                    st.warning("Por favor, preencha todos os campos.")
                    
                else:
                    salvarAlimentoBD(nome, preco, descricao, uploaded_file, categoria, qntd)
                    st.session_state.alimentos = carregar_alimentos()
                    st.session_state.chave += 1
                    st.rerun()
    

def pagina_gerenciar_admins():
    st.header("👤 Gerenciar Administradores")
    tab1, tab2 = st.tabs(["✏️ Editar/Remover", "➕ Adicionar"])

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    with tab1:
        st.subheader("Administradores Cadastrados")

        cursor.execute("SELECT ID, Nome, Email, Senha FROM Admins")
        admins = cursor.fetchall()

        if not admins:
            st.info("Nenhum administrador cadastrado.")
        else:
            for admin in admins:
                admin_id, nome_atual, email_atual, senha_atual = admin

                with st.expander(f"{nome_atual} ({email_atual})"):
                    novo_nome = st.text_input("Nome", value=nome_atual, key=f"nome_{admin_id}")
                    novo_email = st.text_input("Email", value=email_atual, key=f"email_{admin_id}")
                    nova_senha = st.text_input("Senha (deixe em branco para não alterar)", type="password", key=f"senha_{admin_id}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Salvar Alterações", key=f"salvar_{admin_id}"):
                            if nova_senha.strip():
                                senha_bytes = nova_senha.encode('utf-8')
                                sal = bcrypt.gensalt()
                                senha_hash = bcrypt.hashpw(senha_bytes, sal)
                                cursor.execute("UPDATE Admins SET Nome=?, Email=?, Senha=? WHERE ID=?",
                                               (novo_nome, novo_email, senha_hash, admin_id))
                            else:
                                cursor.execute("UPDATE Admins SET Nome=?, Email=? WHERE ID=?",
                                               (novo_nome, novo_email, admin_id))
                            conexao.commit()
                            st.success("Administrador atualizado com sucesso!")
                            st.rerun()

                    with col2:
                        if st.button("Remover", key=f"remover_{admin_id}"):
                            cursor.execute("DELETE FROM Admins WHERE ID=?", (admin_id,))
                            conexao.commit()
                            st.warning("Administrador removido com sucesso!")
                            st.rerun()

    with tab2:
        st.subheader("Adicionar Novo Administrador")

        with st.form("form_add_admin"):
            nome = st.text_input("Nome", key="novo_admin_nome")
            email = st.text_input("Email", key="novo_admin_email")
            senha = st.text_input("Senha", type="password", key="novo_admin_senha")
            submit = st.form_submit_button("Adicionar")

            if submit:
                if not nome or not email or not senha:
                    st.error("Preencha todos os campos.")
                else:
                    # Verifica se já existe
                    cursor.execute("SELECT ID FROM Admins WHERE Email=?", (email,))
                    if cursor.fetchone():
                        st.error("Já existe um administrador com esse email.")
                    else:
                        senha_bytes = senha.encode('utf-8')
                        sal = bcrypt.gensalt()
                        senha_hash = bcrypt.hashpw(senha_bytes, sal)

                        cursor.execute("INSERT INTO Admins (Nome, Email, Senha) VALUES (?, ?, ?)",
                                       (nome, email, senha_hash))
                        conexao.commit()
                        st.success("Administrador adicionado com sucesso!")
                        st.rerun()

    conexao.close()


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
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    query = "SELECT ID, Nome, Senha FROM Admins WHERE Email = ?"
    cursor.execute(query, (email,))
    admin_data = cursor.fetchone()

    if not email or not senha:
        st.error("Por favor, preencha todos os campos.")
        return

    if admin_data is not None:
        admin_id, nome, senha_bd = admin_data
        senha_bytes = senha.encode("utf-8")

        if bcrypt.checkpw(senha_bytes, senha_bd):
            st.session_state.admin_id = admin_id
            st.session_state.nome_admin = nome
            st.session_state.auth_admin = "autenticado"
        else:
            st.error("Senha inválida, tente novamente.")
    else:
        st.error("Esse email não está cadastrado como administrador.")


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
    st.session_state.auth_admin = "login"
        
        

if "auth_admin" not in st.session_state:
    st.session_state.auth_admin = "login"


if st.session_state.auth_admin == "login":
    pagina_login()

elif st.session_state.auth_admin == "autenticado":
    nav = st.navigation([
        st.Page(pagina_crud_eventos, title="CRUD Eventos", icon="📋"),
        st.Page(pagina_estatisticas_evento, title="Estatísticas do Evento", icon="📊"),
        st.Page(pagina_crud_alimentos, title="CRUD Alimentos", icon="🍽️"),
        st.Page(pagina_gerenciar_admins, title="Gerenciar Admins", icon="🛠️"),
    ],)
    nav.run()