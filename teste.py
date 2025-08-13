import streamlit as st

st.set_page_config(page_title="Central de Eventos")

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
            descricao = st.text_area("Descrição", value=evento["descricao"])

            if st.button("Salvar alterações", type="primary"):
                salvar_edicao(evento["id"], nome, data, local, descricao)

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
    with col2:
        imagem = st.text_input("Imagem")
        st.write("Preview da imagem")
        
    ingressos = 1 # colocar um popover que vai configurar quantos ingressos vão ter
    local = st.text_input("Local")
    descricao = st.text_area("Descrição")

    if st.button("Adicionar Evento", type="primary"):
        def salvarEventoBD(nome, data, local, descricao, ingressos):
            pass
        
        salvarEventoBD(nome, data, local, descricao, ingressos)