import os
import re
import bcrypt
import sqlite3
import streamlit as st
from datetime import date


# PÁGINAS DO CLIENTE

def sidebar_perfil():
    with st.sidebar:
        if "cliente_id" in st.session_state:
            st.markdown("#### 👤 Meu Perfil")
            nome = st.session_state.get("nome_cliente", "-")
            email = st.session_state.get("email_cliente", "-")
            st.write(f"**Nome:** {nome}")
            st.write(f"**Email:** {email}")
            st.divider()
            if st.button("Sair", type='primary', use_container_width=True):
                for k in [
                    "cliente_id",
                    "nome_cliente",
                    "email_cliente",
                    "auth_user",
                ]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.session_state.auth_user = "login"
                st.rerun()

def pagina_meus_ingressos():
    sidebar_perfil()
    st.header("Meus Ingressos")
    st.write("---")

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT I.ID, E.Nome, E.Data, E.Local
        FROM Ingressos I
        JOIN Eventos E ON I.Evento_ID = E.ID
        WHERE I.Cliente_ID = ?
        ORDER BY E.Data
    """,
        (st.session_state.cliente_id,),
    )
    ingressos = cursor.fetchall()
    conexao.close()

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

    for _, evento, data, local in ingressos:
        st.write(f"**{evento}** — {data} — {local}")
        if st.button(f"Exibir informações de {evento}"):
            info_ingresso(evento, data, local)
        st.write("---")


def pagina_area_alimentos():
    sidebar_perfil()
    st.header("Área de Alimentos")
    tab1, tab2, tab3 = st.tabs(["Cardápio", "Carrinho", "Retirar"])

    with tab1:
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT ID, Nome, Preco, Categoria, Imagem, Descricao, Quantidade FROM Alimentos")
        linhas = cursor.fetchall()
        conexao.close()

        cardapio = []

        for l in linhas:
            cardapio.append({
                "id": l[0],
                "nome": l[1],
                "preco": float(l[2]),
                "categoria": l[3],
                "img": l[4],
                "descricao": l[5],
                "quantidade": int(l[6]),
            })

        categorias = ["Todos"] + sorted(set(item["categoria"] for item in cardapio))

        filtro = st.selectbox("Filtrar por categoria", categorias)

        itens_filtrados = [item for item in cardapio if filtro == "Todos" or item["categoria"] == filtro]

        if not itens_filtrados:
            st.info("Nenhum item para a categoria selecionada.")
            
        for item in itens_filtrados:
            col1, col2 = st.columns([1, 2])

            with col1:

                if item["img"] and os.path.exists(item["img"]):
                    st.image(item["img"], width=250)

            with col2:
                st.markdown(f"### {item['nome']}")
                st.caption(f"R$ {item['preco']:.2f}")
                st.write(item["descricao"])
                st.caption(f"Estoque: {item['quantidade']}")
                if st.button("Adicionar ao Carrinho", type="primary", key=f"add_{item['id']}"):
                    add_alimento_to_cart(st.session_state.cliente_id, item["id"], 1)
                    st.success(f"{item['nome']} adicionado ao carrinho!")
                    st.rerun()

    with tab2:
        st.subheader("Carrinho")
        itens = get_cart_alimentos(st.session_state.cliente_id)
        if not itens:
            st.info("Carrinho de alimentos vazio.")

        else:
            total = 0.0
            for alimento_id, nome, preco, qtd, img, desc in itens:
                total += preco * qtd
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.write(f"**{nome}** — Quantidade: {qtd}")
                    st.caption(f"R$ {preco:.2f} cada")

                with col2:
                    if st.button("+", key=f"mais_{alimento_id}"):
                        add_alimento_to_cart(st.session_state.cliente_id, alimento_id, 1)
                        st.rerun()

                with col3:
                    if st.button("-", key=f"menos_{alimento_id}"):
                        remove_one_alimento_from_cart(st.session_state.cliente_id, alimento_id)
                        st.rerun()

                with col4:
                    st.write(f"R$ {preco * qtd:.2f}")

            st.markdown(f"### Total alimentos: R$ {total:.2f}")

    # Tab 3 — Retirar (placeholder)
    with tab3:
        st.subheader("Retirar")
        st.write("Compra disponível para retirada após confirmação da compra na aba **Central de Eventos → Carrinho**.")


def pagina_central_eventos():
    sidebar_perfil()
    st.header("Central de Eventos")
    tab1, tab2 = st.tabs(["Eventos Disponíveis", "Carrinho"])

    with tab1:
        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT ID, Nome, Data, Local, Descricao, Imagem FROM Eventos ORDER BY Data")
        linhas = cursor.fetchall()
        conexao.close()

        eventos = []

        for l in linhas:
            eventos.append({
                "id": l[0],
                "nome": l[1],
                "data": l[2],
                "local": l[3],
                "descricao": l[4],
                "imagem": l[5],
            })

        st.write("### Eventos disponíveis")
        if not eventos:
            st.info("Nenhum evento disponível no momento.")

        else:
            cols = st.columns(3)
            for i, evento in enumerate(eventos):
                with cols[i % 3]:
                    if evento["imagem"] and os.path.exists(evento["imagem"]):
                        st.image(evento["imagem"], use_container_width=True)

                    st.markdown(f"**{evento['nome']}**")
                    st.caption(f"{evento['data']} — {evento['local']}")

                    @st.dialog(evento["nome"])
                    def detalhes_dialog(e=evento):
                        if e["imagem"] and os.path.exists(e["imagem"]):
                            st.image(e["imagem"], use_container_width=True)

                        st.write(f"**Data:** {e['data']}")
                        st.write(f"**Local:** {e['local']}")
                        st.write(e["descricao"])

                        if st.button("Participar", type="primary"):
                            resultado = add_event_ticket_to_cart(st.session_state.cliente_id, e["id"])
                            if resultado:
                                st.success(f"{e['nome']} foi adicionado ao carrinho!")
                            else:
                                st.warning("Ingressos esgotados para este evento.")
                            st.rerun()

                    if st.button("Ver mais detalhes", type="primary", key=f"det_{evento['id']}"):
                        detalhes_dialog()

    with tab2:
        st.subheader("Carrinho")
        ingressos = get_cart_ingressos(st.session_state.cliente_id)
        total_ing = 0.0
        if not ingressos:
            st.info("Carrinho de ingressos vazio.")
        else:
            for evento_id, nome, data, local, qtde, valor in ingressos:
                total_ing += float(valor) * qtde
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{nome}** — {data} — {local}")
                    st.caption(f"{qtde} x R$ {float(valor):.2f}")
                with col2:
                    if st.button("Remover 1", key=f"menos_ing_{evento_id}"):
                        remove_one_ingresso_from_cart(st.session_state.cliente_id, evento_id)
                        st.rerun()
                    if st.button("Adicionar 1", key=f"mais_ing_{evento_id}"):
                        add_event_ticket_to_cart(st.session_state.cliente_id, evento_id) 
                        st.rerun()
                with col3:
                    st.write(f"R$ {float(valor) * qtde:.2f}")

        # alimentos (mostrar resumo aqui também)
        itens_al = get_cart_alimentos(st.session_state.cliente_id)
        total_al = sum(float(preco) * qtd for _, _, preco, qtd, _, _ in itens_al) if itens_al else 0.0

        st.markdown("---")
        st.markdown(f"### Total ingressos: R$ {total_ing:.2f}")

        # with st.form("finalizar_compra_form"):
        #     confirmar = st.form_submit_button("Finalizar Compra", use_container_width=True)
        #     if confirmar:
        #         if not ingressos and not itens_al:
        #             st.warning("Seu carrinho está vazio.")
        #         else:
        #             finalizar_compra(st.session_state.cliente_id)
        #             st.success("Compra finalizada com sucesso! Seus ingressos já estão disponíveis em **Meus Ingressos**.")
        #             st.rerun()



# FUNÇÕES CARRINHO

def get_carrinho(cliente_id):
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT ID FROM Carrinhos WHERE Cliente_ID = ?", (cliente_id,))
    carrinho_id = cursor.fetchone()
    conexao.close()
     
    if carrinho_id:
        return carrinho_id[0]
    
    else:
        raise ValueError(f"InInconsistência de dados: Carrinho não encontrado para o cliente_id {cliente_id}")



def add_alimento_to_cart(cliente_id, alimento_id, qtd = 1):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    
    cursor.execute(
        "SELECT ID FROM Alimento_no_Carrinho WHERE Carrinho_ID = ? AND Alimento_ID = ?", (carrinho_id, alimento_id)
        )
    alimento_presente = cursor.fetchone()
    
    if alimento_presente:
        cursor.execute(
            "UPDATE Alimento_no_Carrinho SET Quantidade = Quantidade + ? WHERE Carrinho_ID = ? AND Alimento_ID = ?",
            (qtd, carrinho_id, alimento_id)
            )
    
    else:
        cursor.execute(
            "INSERT INTO Alimento_no_Carrinho (Carrinho_ID, Alimento_ID, Quantidade) VALUES (?, ?, ?)",
            (carrinho_id, alimento_id, qtd)
            )
    
    conexao.commit()
    conexao.close()
    
    for _ in range(qtd):
        cursor.execute(
            "INSERT INTO Alimento_no_Carrinho (Carrinho_ID, Alimento_ID) VALUES (?, ?)",
            (carrinho_id, alimento_id),
        )
    conexao.commit()
    conexao.close()


def remove_one_alimento_from_cart(cliente_id, alimento_id):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    # apaga apenas um registro desse alimento
    cursor.execute(
        """
        DELETE FROM Alimento_no_Carrinho
        WHERE ID = (
            SELECT ID FROM Alimento_no_Carrinho
            WHERE Carrinho_ID = ? AND Alimento_ID = ?
            LIMIT 1
        )
        """,
        (carrinho_id, alimento_id),
    )
    conexao.commit()
    conexao.close()


def clear_alimentos_cart(cliente_id):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Alimento_no_Carrinho WHERE Carrinho_ID = ?", (carrinho_id,))
    conexao.commit()
    conexao.close()


def get_cart_alimentos(cliente_id):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT A.ID, A.Nome, A.Preco, COUNT(AC.ID) AS Quantidade, A.Imagem, A.Descricao
        FROM Alimento_no_Carrinho AC
        JOIN Alimentos A ON AC.Alimento_ID = A.ID
        WHERE AC.Carrinho_ID = ?
        GROUP BY A.ID, A.Nome, A.Preco, A.Imagem, A.Descricao
        ORDER BY A.Nome
        """,
        (carrinho_id,),
    )
    rows = cursor.fetchall()
    conexao.close()
    return rows


def add_event_ticket_to_cart(cliente_id, evento_id):
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    # ingresso livre (não vendido) e não presente em nenhum carrinho
    cursor.execute(
        """
        SELECT I.ID
        FROM Ingressos I
        LEFT JOIN Ingresso_no_Carrinho IC ON IC.Ingresso_ID = I.ID
        WHERE I.Evento_ID = ? AND I.Cliente_ID IS NULL AND IC.ID IS NULL
        LIMIT 1
        """,
        (evento_id,),
    )
    row = cursor.fetchone()
    if not row:
        conexao.close()
        return False
    ingresso_id = row[0]
    carrinho_id = get_carrinho(cliente_id)
    cursor.execute(
        "INSERT INTO Ingresso_no_Carrinho (Carrinho_ID, Ingresso_ID) VALUES (?, ?)",
        (carrinho_id, ingresso_id),
    )
    conexao.commit()
    conexao.close()
    return True


def get_cart_ingressos(cliente_id):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT E.ID, E.Nome, E.Data, E.Local, COUNT(IC.ID) AS Qtde, I.Valor
        FROM Ingresso_no_Carrinho IC
        JOIN Ingressos I ON IC.Ingresso_ID = I.ID
        JOIN Eventos E ON I.Evento_ID = E.ID
        WHERE IC.Carrinho_ID = ?
        GROUP BY E.ID, E.Nome, E.Data, E.Local, I.Valor
        ORDER BY E.Data
        """,
        (carrinho_id,),
    )
    rows = cursor.fetchall()
    conexao.close()
    return rows


def remove_one_ingresso_from_cart(cliente_id, evento_id):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()
    # pega um ingresso desse evento que esteja no carrinho e remove
    cursor.execute(
        """
        SELECT IC.ID
        FROM Ingresso_no_Carrinho IC
        JOIN Ingressos I ON IC.Ingresso_ID = I.ID
        WHERE IC.Carrinho_ID = ? AND I.Evento_ID = ?
        LIMIT 1
        """,
        (carrinho_id, evento_id),
    )
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM Ingresso_no_Carrinho WHERE ID = ?", (row[0],))
        conexao.commit()
    conexao.close()


def finalizar_compra(cliente_id):
    carrinho_id = get_carrinho(cliente_id)
    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    # Ingressos: pegar todos do carrinho
    cursor.execute(
        """
        SELECT Ingresso_ID FROM Ingresso_no_Carrinho
        WHERE Carrinho_ID = ?
        """,
        (carrinho_id,),
    )
    ingresso_ids = [r[0] for r in cursor.fetchall()]
    if ingresso_ids:
        cursor.executemany(
            "UPDATE Ingressos SET Cliente_ID = ? WHERE ID = ? AND Cliente_ID IS NULL",
            [(cliente_id, iid) for iid in ingresso_ids],
        )
        cursor.execute(
            "DELETE FROM Ingresso_no_Carrinho WHERE Carrinho_ID = ?", (carrinho_id,)
        )

    # Alimentos: limpar carrinho
    cursor.execute("DELETE FROM Alimento_no_Carrinho WHERE Carrinho_ID = ?", (carrinho_id,))

    conexao.commit()
    conexao.close()


# CARRINHO DE COMPRAS

def pagina_carrinho():
    st.title("Carrinho de Compras")
    st.divider()
    
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


# LOGIN E CADASTRO


def pagina_login():
    st.title("Bem-vindo")

    with st.form("login_form"):
        st.markdown("### Login")
        email = st.text_input("Email", key="login_email", autocomplete="off")
        senha_digitada = st.text_input("Senha", type="password", key="login_senha", autocomplete="off")
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Login", use_container_width=True, type="primary")
        with col2:
            cadastrar = st.form_submit_button("Ir para Cadastro", use_container_width=True)

    if cadastrar:
        st.session_state.auth_user = "cadastrar"
        st.rerun()

    if submit:
        checaLogin(email, senha_digitada)


def checaLogin(email, senha):
    if not email or not senha:
        st.error("Por favor, preencha todos os campos.")
        return

    conexao = sqlite3.connect("dados.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT ID, Nome, Email, Senha FROM Clientes WHERE Email = ?", (email,))
    dados = cursor.fetchone()
    conexao.close()

    if dados is None:
        st.error("Esse email não está cadastrado em nossos sistemas.")
        return

    cliente_id, nome, email_bd, senha_bd = dados
    senha_bytes = senha.encode("utf-8")
    try:
        resultado = bcrypt.checkpw(senha_bytes, senha_bd)
    except Exception:
        resultado = False

    if resultado:
        st.session_state.cliente_id = cliente_id
        st.session_state.nome_cliente = nome
        st.session_state.email_cliente = email_bd
        st.session_state.auth_user = "autenticado"
        st.rerun()
    else:
        st.error("Senha inválida, tente novamente.")


def ir_para_login():
    st.session_state.auth_user = "login"


def pagina_cadastrar():
    st.title("Cadastro")
    st.divider()

    with st.form("cadastro_form"):
        nome = st.text_input("Nome completo", key="cadastro_nome", autocomplete="off")

        # CPF apenas dígitos
        cpf_raw = st.text_input("CPF (apenas números)", key="cadastro_cpf", autocomplete="off", help="Será salvo somente com dígitos.")
        # Sanitiza visualmente (mantém só dígitos)
        cpf = re.sub(r"\\D", "", cpf_raw)

        col1, col2 = st.columns(2)
        with col1:
            data_nascimento = st.date_input("Data de nascimento", format="DD/MM/YYYY", min_value=date(1945, 12, 31))
        with col2:
            email = st.text_input("Email", key="cadastro_email", autocomplete="off")
        senha = st.text_input("Senha", type="password", key="cadastro_senha", autocomplete="off")

        col3, col4 = st.columns(2)
        with col3:
            enviar = st.form_submit_button("Cadastrar", use_container_width=True, type="primary")
        with col4:
            voltar = st.form_submit_button("Voltar ao Login", use_container_width=True)

    if voltar:
        ir_para_login()
        st.rerun()

    if enviar:
        if not nome or not cpf or not email or not senha:
            st.error("Preencha todos os campos")
            return
        if not validaEmail(email) or not validaSenha(senha):
            return

        conexao = sqlite3.connect("dados.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT Email FROM Clientes WHERE Email = ?", (email,))
        existe = cursor.fetchone()
        if existe:
            st.error("Esse email já está cadastrado, utilize outro email ou faça login.")
            conexao.close()
            return

        senha_bytes = senha.encode("utf-8")
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt)

        cursor.execute(
            "INSERT INTO Clientes (Nome, CPF, Data_Nasc, Email, Senha) VALUES (?, ?, ?, ?, ?)",
            (nome, cpf, str(data_nascimento), email, senha_hash),
        )
        conexao.commit()
        cliente_id = cursor.lastrowid
        conexao.close()

        st.session_state.cliente_id = cliente_id
        st.session_state.nome_cliente = nome
        st.session_state.email_cliente = email
        ir_para_login()
        st.rerun()


# Funções de validação Login/Cadastro
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


# LÓGICA TROCAR DE PÁGINAS AUTENTIFICADORAS

if "auth_user" not in st.session_state:
    st.session_state.auth_user = "login"

if st.session_state.auth_user == "login":
    pagina_login()

elif st.session_state.auth_user == "cadastrar":
    pagina_cadastrar()

elif st.session_state.auth_user == "autenticado":
    nav = st.navigation([
        st.Page(pagina_central_eventos, title="Central de Eventos", icon="🎉"),
        st.Page(pagina_area_alimentos, title="Área de Alimentos", icon="🍔"),
        st.Page(pagina_meus_ingressos, title="Meus Ingressos", icon="🎟️"),
        st.Page(pagina_carrinho, title="Carrinho de Compras", icon="🛒"),
    ])
    nav.run()