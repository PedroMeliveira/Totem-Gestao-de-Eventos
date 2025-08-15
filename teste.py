import streamlit as st
import sqlite3



# def salvarAlimentoBD(nome, preco, descricao, imagem):
#     pass

# tab1, tab2 = st.tabs(["Editar/Remover Itens", "Adicionar Item"])

# with tab1:
#     if "alimentos" not in st.session_state:
#         st.session_state.alimentos = [
#             {"id": 1, "qntd": 10, "nome": "Hambúrguer", "preco": 20.0, "categoria": "Lanches",
#                 "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
#                 "descricao": "Hambúrguer artesanal com queijo e bacon."},
#             {"id": 2, "qntd": 15, "nome": "Pizza", "preco": 35.0, "categoria": "Lanches",
#                 "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
#                 "descricao": "Pizza de mussarela com borda recheada."},
#             {"id": 3, "qntd": 23, "nome": "Refrigerante", "preco": 5.0, "categoria": "Bebidas",
#                 "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
#                 "descricao": "Lata 350ml de refrigerante gelado."}
#         ]

#     if "alimento_editar_id" not in st.session_state:
#         st.session_state.alimento_editar_id = None

#     if "alimento_remover_id" not in st.session_state:
#         st.session_state.alimento_remover_id = None

#     def salvar_edicao(alimento_id, nome, preco, qntd, descricao):
#         # MODIFICAR NO BANCO DE DADOS
#         for e in st.session_state.alimentos:
#             if e["id"] == alimento_id:
#                 e["nome"] = nome
#                 e["preco"] = preco
#                 e["qntd"] = qntd
#                 e["descricao"] = descricao
#                 break
#         st.session_state.alimento_editar_id = None
#         st.rerun()

#     def remover_alimento(alimento_id):
#         # REMOVER NO BANCO DE DADOS
#         st.session_state.alimentos = [e for e in st.session_state.alimentos if e["id"] != alimento_id]
#         st.session_state.alimento_remover_id = None
#         st.rerun()

#     # necessário?
#     categorias = ["Todos"] + sorted(set(item["categoria"] for item in st.session_state.alimentos))
#     if "carrinho" not in st.session_state:
#         st.session_state.carrinho = {item["nome"]: 0 for item in st.session_state.alimentos}

#     filtro = st.selectbox("Filtrar por categoria", categorias)
#     itens_filtrados = [item for item in st.session_state.alimentos if filtro == "Todos" or item["categoria"] == filtro]

#     for item in itens_filtrados:
#         col1, col2 = st.columns([1, 2])
#         with col1: st.image(item["img"], width=240)
#         with col2:
#             st.markdown(f"### {item['nome']}")
#             st.caption(f"R$ {item['preco']:.2f}")
#             st.caption(f"Quantidade - {item['qntd']}")
#             st.write(item["descricao"])
            
#             col3, col4 = st.columns(2)
#             with col3:
#                 if st.button("Editar", use_container_width=True, type='primary', key=f"add_{item['nome']}"):
#                     st.session_state.alimento_remover_id = None
#                     st.session_state.alimento_editar_id = item["id"]

#             with col4:
#                 if st.button("Remover", type='secondary', key=f"remove_{item['nome']}"):
#                     st.session_state.alimento_editar_id = None
#                     st.session_state.alimento_remover_id = item["id"]
    
#     # Diálogo de edição
#     if st.session_state.alimento_editar_id is not None:
#         alimento = next(e for e in st.session_state.alimentos if e["id"] == st.session_state.alimento_editar_id)

#         @st.dialog(f"Editar {alimento['nome']}")
#         def editar():
#             nome = st.text_input("Nome", value=alimento["nome"])
            
#             # colocar apenas número
#             preco = st.text_input("Preço", value=alimento["preco"])
#             qntd = st.text_input("Quantidade", value=alimento["qntd"])
#             descricao = st.text_area("Descrição", value=alimento["descricao"])

#             if st.button("Salvar alterações", type="primary"):
#                 salvar_edicao(alimento["id"], nome, float(preco), qntd, descricao)

#         editar()
    
#     # Diálogo de confirmar remoção
#     if st.session_state.alimento_remover_id is not None:
#         alimento = next(e for e in st.session_state.alimentos if e["id"] == st.session_state.alimento_remover_id)

#         @st.dialog(f"Remover {alimento['nome']}?")
#         def confirmar_remocao():
#             st.warning("Tem certeza que deseja remover este alimento?")
#             st.write(f"**Alimento:** {alimento['nome']}")
#             st.write(f"**Preço:** {alimento['preco']}")
#             st.write(f"**Quantidade:** {alimento['qntd']}")
#             st.write(f"**Descrição:** {alimento['descricao']}")

#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button("❌ Cancelar"):
#                     st.session_state.alimento_remover_id = None
#                     st.rerun()
#             with col2:
#                 if st.button("🗑️ Confirmar", type="primary"):
#                     remover_alimento(alimento["id"])

#         confirmar_remocao()
            
        
#     with tab2:
#         st.header("Adicionar Alimento")

#         nome = st.text_input("Nome")
        
#         # colocar pra número
#         preco = st.text_input("Preço")  
        
#         col1, col2 = st.columns(2)
#         with col1:
#             imagem = st.text_input("Imagem")
            
#         with col2:
#             st.write("Mostrar imagem")
                
#         descricao = st.text_area("Descrição")

#         col3, col4, col5 = st.columns(3)
#         with col4:
#             if st.button("Adicionar", type="primary", use_container_width=True):
#                 salvarAlimentoBD(nome, preco, descricao, imagem)