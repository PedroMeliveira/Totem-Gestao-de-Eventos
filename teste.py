import streamlit as st

# @st.dialog("Cast your vote")
# def vote(item):
#     st.write(f"Why is {item} your favorite?")
#     reason = st.text_input("Because...")
#     if st.button("Submit"):
#         st.session_state.vote = {"item": item, "reason": reason}
#         st.rerun()

# if "vote" not in st.session_state:
#     st.write("Vote for your favorite")
#     if st.button("A"):
#         vote("A")
#     if st.button("B"):
#         vote("B")
# else:
#     f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

# with st.popover("Open popover"):
#     st.markdown("Hello World 👋")
#     name = st.text_input("What's your name?")

# st.write("Your name:", name)

cardapio = [
    {"nome": "Hambúrguer", "preco": 20.0, "categoria": "Lanches", "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png", "descricao": "Hambúrguer artesanal com queijo e bacon."},
    {"nome": "Pizza", "preco": 35.0, "categoria": "Lanches", "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png", "descricao": "Pizza de mussarela com borda recheada."},
    {"nome": "Refrigerante", "preco": 5.0, "categoria": "Bebidas", "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png", "descricao": "Lata 350ml de refrigerante gelado."},
    {"nome": "Suco Natural", "preco": 7.0, "categoria": "Bebidas", "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png", "descricao": "Suco de laranja natural."},
    {"nome": "Sorvete", "preco": 10.0, "categoria": "Sobremesas", "img": "https://user-images.githubusercontent.com/20684618/31289519-9ebdbe1a-aae6-11e7-8f82-bf794fdd9d1a.png", "descricao": "Taça de sorvete com cobertura de chocolate."}
]

categorias = ["Todos"] + sorted(set([item["categoria"] for item in cardapio]))

if "carrinho" not in st.session_state:
    st.session_state.carrinho = {item["nome"]: 0 for item in cardapio}

st.write("## Cardápio")
filtro = st.selectbox("Filtrar por categoria", categorias)

itens_filtrados = [item for item in cardapio if filtro == "Todos" or item["categoria"] == filtro]

for item in itens_filtrados:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(item["img"], width=120)
    with col2:
        st.markdown(f"### {item['nome']}")
        st.caption(f"R$ {item['preco']:.2f}")
        st.write(item["descricao"])
        if st.button("Adicionar ao Carrinho", key=f"add_{item['nome']}"):
            st.session_state.carrinho[item["nome"]] += 1
            st.success(f"{item['nome']} adicionado ao carrinho!")