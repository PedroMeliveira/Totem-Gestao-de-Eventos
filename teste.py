import streamlit as st

# def pagina_crud_eventos():
#     tab1, tab2 = st.tabs(["Editar/Remover Evento", "Adicionar Evento"])
#     with tab1:
#         st.session_state.eventos = []
#         conexao = sqlite3.connect('dados.db')
#         cursor = conexao.cursor()

#         cursor.execute("SELECT ID, Nome, Horario, Data, Descricao, Imagem, Local FROM Eventos")
#         eventos_bd = cursor.fetchall()

#         for evento in eventos_bd:
#             cursor.execute("SELECT ID, Cliente_ID, Valor FROM Ingressos WHERE Evento_ID = ?", (evento[0],))
#             qntd_ingresso_disponiveis = 0
#             ingressos_bd = cursor.fetchall()
#             for ingresso in ingressos_bd:
#                 if ingresso[1] is None:
#                     qntd_ingresso_disponiveis += 1

#             evento_dict = {
#                 "id": evento[0],
#                 "nome": evento[1],
#                 "horario": evento[2],
#                 "data": evento[3],
#                 "descricao": evento[4],
#                 "imagem": evento[5],
#                 "local": evento[6],
#                 "qntd_ingresos_disponiveis": qntd_ingresso_disponiveis,
#                 "preco_ingressos": ingressos_bd[0][2] if ingressos_bd else 0
#             }

#             st.session_state.eventos.append(evento_dict)

#         if "evento_editar_id" not in st.session_state:
#             st.session_state.evento_editar_id = None

#         if "evento_remover_id" not in st.session_state:
#             st.session_state.evento_remover_id = None

#         def salvar_edicao(evento_id, nome, data, local, imagem, descricao):
#             # Atualiza no session_state
#             for e in st.session_state.eventos:
#                 if e["id"] == evento_id:
#                     e["nome"] = nome
#                     e["data"] = data
#                     e["local"] = local
#                     e["imagem"] = imagem
#                     e["descricao"] = descricao
#                     break

#             # Atualiza no banco
#             conexao = sqlite3.connect("dados.db")
#             cursor = conexao.cursor()
#             cursor.execute("""
#                 UPDATE Eventos
#                 SET Nome=?, Data=?, Local=?, Imagem=?, Descricao=?
#                 WHERE ID=?
#             """, (nome, data, local, imagem, descricao, evento_id))
#             conexao.commit()
#             conexao.close()

#             st.session_state.evento_editar_id = None
#             st.rerun()

#         def remover_evento(evento_id):
#             conexao = sqlite3.connect("dados.db")
#             cursor = conexao.cursor()
#             cursor.execute("DELETE FROM Eventos WHERE ID=?", (evento_id,))
#             conexao.commit()
#             conexao.close()

#             st.session_state.eventos = [e for e in st.session_state.eventos if e["id"] != evento_id]
#             st.session_state.evento_remover_id = None
#             st.rerun()

#         st.write("### Eventos disponíveis")
#         eventos = st.session_state.eventos
#         cols = st.columns(3)

#         for i, evento in enumerate(eventos):
#             with cols[i % 3]:
#                 if evento["imagem"] and os.path.exists(evento["imagem"]):
#                     st.image(evento["imagem"], use_container_width=True)
#                 st.markdown(f"**{evento['nome']}**")
#                 st.caption(f"{evento['data']} - {evento['local']}")

#                 with st.popover("Ver mais detalhes"):
#                     if evento["imagem"] and os.path.exists(evento["imagem"]):
#                         st.image(evento["imagem"], use_container_width=True)
#                     st.write(f"**Data:** {evento['data']}")
#                     st.write(f"**Local:** {evento['local']}")
#                     st.write(evento["descricao"])

#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if st.button("✏️ Editar", key=f"editar_{evento['id']}"):
#                             st.session_state.evento_editar_id = evento["id"]
#                     with col2:
#                         if st.button("🗑️ Remover", key=f"remover_{evento['id']}"):
#                             st.session_state.evento_remover_id = evento["id"]

#         # Diálogo de edição
#         if st.session_state.evento_editar_id is not None:
#             evento = next(e for e in st.session_state.eventos if e["id"] == st.session_state.evento_editar_id)

#             @st.dialog(f"Editar {evento['nome']}")
#             def editar():
#                 nome = st.text_input("Nome", value=evento["nome"])
#                 data = st.text_input("Data", value=evento["data"])
#                 local = st.text_input("Local", value=evento["local"])
#                 descricao = st.text_area("Descrição", value=evento["descricao"])

#                 st.write("Imagem atual:")
#                 if evento["imagem"] and os.path.exists(evento["imagem"]):
#                     st.image(evento["imagem"], width=250)

#                 uploaded_file = st.file_uploader("Alterar imagem", type=["jpg", "jpeg", "png"],
#                                                  key=f"edit_img_{evento['id']}")
#                 imagem_path = evento["imagem"]  # mantém a antiga
#                 if uploaded_file:
#                     imagem_path = os.path.join("imagens/eventos", uploaded_file.name)
#                     with open(imagem_path, "wb") as f:
#                         f.write(uploaded_file.getbuffer())
#                     st.image(imagem_path, caption="Nova imagem", use_container_width=True)

#                 if st.button("Salvar alterações", type="primary"):
#                     salvar_edicao(evento["id"], nome, data, local, imagem_path, descricao)

#             editar()

#         # Dialog de confirmação de remoção
#         if st.session_state.evento_remover_id is not None:
#             evento = next(e for e in st.session_state.eventos if e["id"] == st.session_state.evento_remover_id)

#             @st.dialog(f"Remover {evento['nome']}?")
#             def confirmar_remocao():
#                 st.warning("Tem certeza que deseja remover este evento?")
#                 st.write(f"**Evento:** {evento['nome']}")
#                 st.write(f"**Data:** {evento['data']}")
#                 st.write(f"**Local:** {evento['local']}")

#                 col1, col2 = st.columns(2)
#                 with col1:
#                     if st.button("❌ Cancelar"):
#                         st.session_state.evento_remover_id = None
#                         st.rerun()
#                 with col2:
#                     if st.button("🗑️ Confirmar remoção", type="primary"):
#                         remover_evento(evento["id"])

#             confirmar_remocao()

#     with tab2:
#         st.header("Adicionar Evento")

#         nome = st.text_input("Nome")
#         horario = st.text_input("Horário")  # ajuste depois para st.time_input se quiser
#         col1, col2 = st.columns(2)
#         with col1:
#             data = st.date_input("Data")
#             local = st.text_input("Local")
#         with col2:
#             uploaded_file = st.file_uploader("Upload da imagem", type=["jpg", "jpeg", "png"])
#             imagem_path = None
#             if uploaded_file:
#                 imagem_path = os.path.join("imagens/eventos", uploaded_file.name)
#                 with open(imagem_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 st.image(imagem_path, caption="Pré-visualização", use_container_width=True)

#             with st.popover("Ingressos"):
#                 qntd_ingresso = st.number_input("Qntd de ingressos", min_value=1, step=1)
#                 valor_ingresso = st.number_input("Valor do ingresso", min_value=0.0, step=0.5)

#         descricao = st.text_area("Descrição")

#         col3, col4, col5 = st.columns(3)
#         with col4:
#             if st.button("Adicionar Evento", type="primary", use_container_width=True):
#                 salvarEventoBD(nome, horario, data, qntd_ingresso, descricao, imagem_path, local, valor_ingresso)


# def salvarEventoBD(nome, horario, data, qntd_ingresso, descricao, imagem, local, valor_ingresso):
#     conexao = sqlite3.connect('dados.db')
#     cursor = conexao.cursor()

#     cursor.execute('''
#         INSERT INTO Eventos (Nome, Horario, Data, Descricao, Imagem, Local)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (nome, horario, str(data), descricao, imagem, local))

#     evento_id = cursor.lastrowid
#     conexao.commit()

#     for i in range(int(qntd_ingresso)):
#         cursor.execute('''
#             INSERT INTO Ingressos (Evento_ID, Valor)
#             VALUES (?, ?)
#         ''', (evento_id, valor_ingresso))
#     conexao.commit()
#     conexao.close()

#     st.success("Evento adicionado com sucesso!")


# def pagina_estatisticas_evento():
#     st.header("Estatísticas do Evento")

import sqlite3
import os


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
    for row in dados:
        alimentos.append({
            "id": row[0],
            "nome": row[1],
            "preco": row[2],
            "descricao": row[3],
            "categoria": row[4],
            "imagem": row[5],
            "qntd": row[6]
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

    if "edit_success" not in st.session_state:
        st.session_state.edit_success = False

    if st.session_state.edit_success:
        st.success("Alterações salvas com sucesso!")
        st.session_state.edit_success = False
    
    st.markdown("---")
    st.subheader("Filtrar Alimentos")
    
    categorias_unicas = sorted(list(set(item['categoria'] for item in st.session_state.alimentos)))
    todas_categorias = ["Todas as Categorias"] + categorias_unicas
    filtro_categoria = st.selectbox("Filtrar por Categoria", todas_categorias)
    
    st.markdown("---")

    alimentos_filtrados = st.session_state.alimentos
    
    if filtro_categoria != "Todas as Categorias":
        alimentos_filtrados = [item for item in alimentos_filtrados if item['categoria'] == filtro_categoria]
    
    if not alimentos_filtrados:
        st.info("Nenhum alimento encontrado com os filtros aplicados.")

    def salvar_edicao(alimento_id, nome, preco, qntd, imagem, descricao, categoria):
        """Salva as edições de um alimento no banco de dados."""
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
        st.session_state.edit_success = True
        st.rerun()

    def remover_alimento(alimento_id):
        """Remove um alimento do banco de dados e o arquivo de imagem associado."""
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
                st.error(f"Erro: {imagem_path} : {e.strerror}")

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
            descricao = st.text_area("Descrição", value=alimento["descricao"])
            categoria = st.selectbox("Categoria", ["Bebida", "Entrada", "Combos", "Principais"],
                                     index=["Bebida", "Entrada", "Combos", "Principais"].index(alimento.get("categoria", "Bebida")))

            st.write("Imagem atual:")
            if alimento.get("imagem") and os.path.exists(alimento["imagem"]):
                st.image(alimento["imagem"], width=250)

            uploaded_file = st.file_uploader("Alterar imagem", type=["jpg", "jpeg", "png"],
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
    categoria = st.selectbox("Categoria", ["Bebida", "Entrada", "Combos", "Principais"], key=f"categoria_{st.session_state.chave}")

    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload da imagem", type=["jpg", "jpeg", "png"], key=f"file_{st.session_state.chave}")

    with col2:
        if uploaded_file:
            st.image(uploaded_file, caption="Pré-visualização", width=300)

    descricao = st.text_area("Descrição", key=f"desc_{st.session_state.chave}")

    col3, col4, col5 = st.columns(3)
    with col4:
        if st.button("Adicionar", type="primary", use_container_width=True):
            if not nome or preco is None or qntd is None or not categoria or not descricao:
                st.warning("Por favor, preencha todos os campos obrigatórios.")
            else:
                salvarAlimentoBD(nome, preco, descricao, uploaded_file, categoria, qntd)
                st.session_state.alimentos = carregar_alimentos()
                st.session_state.chave += 1
                st.rerun()


# import sqlite3
# import bcrypt

# conexao = sqlite3.connect('dados.db')
# cursor = conexao.cursor()
# senha = "123123"
# senha_bytes = senha.encode('utf-8')
# sal = bcrypt.gensalt()
# senha_hash = bcrypt.hashpw(senha_bytes, sal)


# cursor.execute("INSERT INTO Admins (Nome, CPF, Data_Nasc, Email, Senha) VALUES (?, ?, ?, ?, ?)",
#                ("Admin", "12345678901", "2000-01-01", "admin@admin.com", senha_hash))

# conexao.commit()