import streamlit as st


import streamlit as st

st.title("Cadastro de Usuário")

# Entrada de dados
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

# Botão de cadastro
if st.button("Cadastrar"):
    # Verificação de senha
    if len(senha) < 6:
        st.error("A senha deve ter pelo menos 6 caracteres.")
    elif not any(char.isdigit() for char in senha):
        st.error("A senha deve conter pelo menos um número.")
    elif not any(char.isupper() for char in senha):
        st.error("A senha deve conter pelo menos uma letra maiúscula.")
    elif not any(char.islower() for char in senha):
        st.error("A senha deve conter pelo menos uma letra minúscula.")
    else:
        st.success("Usuário cadastrado com sucesso!")

# tab1, tab2 = st.tabs(["Editar/Remover Itens", "Adicionar Item"])

# with tab1:
#     st.session_state.alimentos = [
#         {"nome": "Hambúrguer", "preco": 20.0, "categoria": "Lanches",
#             "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
#             "descricao": "Hambúrguer artesanal com queijo e bacon."},
#         {"nome": "Pizza", "preco": 35.0, "categoria": "Lanches",
#             "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
#             "descricao": "Pizza de mussarela com borda recheada."},
#         {"nome": "Refrigerante", "preco": 5.0, "categoria": "Bebidas",
#             "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png",
#             "descricao": "Lata 350ml de refrigerante gelado."}
#     ]

#     if "alimento_editar_id" not in st.session_state:
#         st.session_state.alimento_editar_id = None

#     if "alimento_remover_id" not in st.session_state:
#         st.session_state.alimento_remover_id = None


#     ## arrumar
#     def salvar_edicao(alimento_id, nome, preco, descricao):
#         for e in st.session_state.alimentos:
#             if e["id"] == alimento_id:
#                 e["nome"] = nome
#                 e["preco"] = preco
#                 e["descricao"] = descricao
#                 break
#         st.session_state.alimento_editar_id = None
#         st.rerun()

#     ## arrumar
#     def remover_alimento(alimento_id):
#         st.session_state.alimentos = [e for e in st.session_state.alimentos if e["id"] != alimento_id]
#         st.session_state.alimento_remover_id = None
#         st.rerun()

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
#             st.write(item["descricao"])
            
#             col3, col4 = st.columns(2)
#             with col3:
#                 if st.button("Editar", use_container_width=True, type='primary', key=f"add_{item['nome']}"):
#                     st.session_state.carrinho[item['nome']] += 1
#                     st.success(f"{item['nome']} adicionado ao carrinho!")

#             with col4:
#                 if st.button("Remover", type='secondary', key=f"remove_{item['nome']}"):
#                     pass

# with tab2:
#     pass