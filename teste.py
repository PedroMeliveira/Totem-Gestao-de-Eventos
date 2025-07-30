import streamlit as st

# Configurações do mapa de assentos com setores
setores = {
    "VIP": {"cor": "#FFD700", "inicio_row": 0, "rows": 2, "cols": 6},        # Dourado
    "Pista": {"cor": "#4CAF50", "inicio_row": 2, "rows": 3, "cols": 8},     # Verde
    "Camarote": {"cor": "#9C27B0", "inicio_row": 5, "rows": 2, "cols": 5},  # Roxo
}

# Inicializar estado da sessão para seleção
if "selecionado" not in st.session_state:
    st.session_state["selecionado"] = None

if "reservados" not in st.session_state:
    st.session_state["reservados"] = [(0, 2), (2, 5), (6, 4)]  # Exemplo

st.title("🎟️ Mapa de Assentos com Setores Visuais")
st.markdown("Assentos são coloridos por setor. Vermelho = ocupado, Azul = selecionado.")

# Função para renderizar assentos
def render_assento_visual(label, cor, ocupado=False, selecionado=False):
    final_cor = "#f44336" if ocupado else "#2196F3" if selecionado else cor
    html = f"""
    <button style='background-color:{final_cor};
                    border:none;
                    padding:10px;
                    margin:3px;
                    width:45px;
                    border-radius:5px;
                    font-weight:bold;
                    color:white;
                    cursor:pointer;'>
        {label}
    </button>
    """
    st.markdown(html, unsafe_allow_html=True)

# Mapa completo com setores
row_global = 0
for setor, conf in setores.items():
    st.subheader(f"Setor {setor}")
    cor_setor = conf["cor"]
    inicio = conf["inicio_row"]
    rows = conf["rows"]
    cols = conf["cols"]

    for i in range(rows):
        cols_obj = st.columns(cols)
        for j in range(cols):
            row_idx = inicio + i
            col_idx = j
            assento_id = f"{setor[0]}{row_idx + 1}-{j + 1}"
            ocupado = (row_idx, j) in st.session_state["reservados"]
            selecionado = st.session_state["selecionado"] == (row_idx, j)

            with cols_obj[j]:
                if ocupado or selecionado:
                    render_assento_visual(assento_id, cor_setor, ocupado, selecionado)
                else:
                    if st.button(assento_id, key=f"{row_idx}-{j}"):
                        st.session_state["selecionado"] = (row_idx, j)
                        st.rerun()

# Mostrar assento selecionado
if st.session_state["selecionado"]:
    r, c = st.session_state["selecionado"]
    st.success(f"Você selecionou o assento: {r + 1}-{c + 1}")
    if st.button("✅ Confirmar Reserva"):
        st.session_state["reservados"].append((r, c))
        st.session_state["selecionado"] = None
        st.rerun()
