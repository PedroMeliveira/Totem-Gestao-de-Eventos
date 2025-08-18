import streamlit as st
import sqlite3
import os


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

def carregar_eventos():
    conexao = sqlite3.connect('dados.db')
    cursor = conexao.cursor()   
    
    cursor.execute("SELECT ID, Nome, Horario, Data, Descricao, Imagem, Local FROM Eventos")
    eventos_bd = cursor.fetchall()
    
    eventos = []
    for evento in eventos_bd:
        cursor.execute("SELECT ID, Cliente_ID, Valor FROM Ingressos WHERE Evento_ID = ?", (evento[0],))
        qntd_ingresso_disponiveis = 0
        ingressos_bd = cursor.fetchall()
        for ingresso in ingressos_bd:
            if ingresso[1] is None:
                qntd_ingresso_disponiveis += 1
        
        eventos.append({
            "id": evento[0],
            "nome": evento[1],
            "horario": evento[2],
            "data": evento[3],
            "descricao": evento[4],
            "imagem": evento[5],
            "local": evento[6],
            "qntd_ingresos_disponiveis": qntd_ingresso_disponiveis,
            "preco_ingressos": ingressos_bd[0][2]
        })
        
        return eventos


tab1, tab2 = st.tabs(["Editar/Remover Evento", "Adicionar Evento"])


with tab1:
    if "eventos" not in st.session_state:
        st.session_state.eventos = carregar_eventos()

    if "evento_editar_id" not in st.session_state:
        st.session_state.evento_editar_id = None

    if "evento_remover_id" not in st.session_state:
        st.session_state.evento_remover_id = None

    def salvar_edicao(evento_id, nome, horario, data, descricao, imagem, local, qntd_ingresso, preco_ingresso):
        # MODIFICAR NO BANCO DE DADOS (COLOCAR OS INGRESSOS NO BD)
        for e in st.session_state.eventos:
            if e["id"] == evento_id:
                e["nome"] = nome
                e["horario"] = horario
                e["data"] = data
                e["descricao"] = descricao
                e["imagem"] = imagem
                e["local"] = local
                e["qntd_ingresso"] = qntd_ingresso
                e["preco_ingresso"] = preco_ingresso
                break
            
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE Eventos
            SET Nome=?, Horario=?, Data=?, Descricao=?, Imagem=?, Local=?
            WHERE ID=?
        """, (nome, horario, data, descricao, imagem, local))
        
        conexao.commit()
        conexao.close()
            
        st.session_state.evento_editar_id = None
        st.rerun()

    def remover_evento(evento_id):
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        
        cursor.execute("SELECT Imagem FROM Eventos WHERE ID=?", (evento_id,))
        resultado = cursor.fetchone()
        
        imagem_path = None
        if resultado and resultado[0]:
            imagem_path
            
        cursor.execute("DELETE FROM Eventos WHERE ID=?", (evento_id,))
        conexao.commit()
        conexao.close()
        
        if imagem_path and os.path.exists(imagem_path) and imagem_path != "temp":
            try:
                os.remove(imagem_path)
            except OSError as e:
                st.error(f"Erro ao tentar excluir {imagem_path}")
                
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