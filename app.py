
import streamlit as st

from dados import (
    produtos,
    pedidos,
    fila_prioridade,
    historico,
    categorias
)

from sistema import (
    cadastrar_produto,
    cadastrar_pedido,
    processar_pedido,
    desfazer_ultima_acao,
    ordenar_produtos_por_nome,
    filtrar_por_categoria,
    exibir_fila_prioridade
)


# ==========================================
# CALLBACKS DOS FORMULÁRIOS
# ==========================================

def enviar_cadastro_produto():

    resultado, mensagem = cadastrar_produto(
        st.session_state.get("produto_codigo"),
        st.session_state.get("produto_nome"),
        st.session_state.get("produto_categoria"),
        st.session_state.get("produto_preco"),
        st.session_state.get("produto_estoque")
    )

    st.session_state["feedback_produto"] = (
        resultado,
        mensagem
    )

    if resultado:
        st.session_state["produto_codigo"] = None
        st.session_state["produto_nome"] = ""
        st.session_state["produto_categoria"] = None
        st.session_state["produto_preco"] = None
        st.session_state["produto_estoque"] = None


def enviar_cadastro_pedido():

    resultado, mensagem = cadastrar_pedido(
        st.session_state.get("pedido_numero"),
        st.session_state.get("pedido_cliente"),
        st.session_state.get("pedido_codigo_produto"),
        st.session_state.get("pedido_quantidade"),
        st.session_state.get("pedido_prioridade")
    )

    st.session_state["feedback_pedido"] = (
        resultado,
        mensagem
    )

    if resultado:
        st.session_state["pedido_numero"] = None
        st.session_state["pedido_cliente"] = ""
        st.session_state["pedido_codigo_produto"] = None
        st.session_state["pedido_quantidade"] = None
        st.session_state["pedido_prioridade"] = 1


def processar_proximo_pedido():

    resultado, mensagem = processar_pedido()

    st.session_state["feedback_fila"] = (
        resultado,
        mensagem
    )


def desfazer_operacao():

    resultado, mensagem = desfazer_ultima_acao()

    st.session_state["feedback_desfazer"] = (
        resultado,
        mensagem
    )


# ==========================================
# CONFIGURAÇÕES
# ==========================================

st.set_page_config(
    page_title="ERP Distribuidora",
    layout="wide"
)


# ==========================================
# IDENTIDADE VISUAL
# ==========================================

st.markdown("""
<style>

    /* Fundo principal */
    .stApp {
        background-color: #F7F9FC;
        color: #263445;
    }

    /* Menu lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5EAF0;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #24364B;
        font-weight: 600;
    }

    /* Navegação lateral */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 10px 12px;
        border-radius: 7px;
        margin-bottom: 4px;
        transition: background-color 0.2s ease;
    }

    /* Esconder círculos de seleção */
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
        display: none;
    }

    /* Opção selecionada */
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background-color: #EAF1F8;
        color: #24558A;
        font-weight: 600;
    }

    /* Efeito ao passar o mouse */
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: #F0F4F8;
    }

    /* Indicadores do painel */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF0;
        padding: 22px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }

    /* Títulos dos indicadores */
    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 14px;
        font-weight: 500;
    }

    /* Valores dos indicadores */
    [data-testid="stMetricValue"] {
        color: #1E293B;
        font-size: 30px;
        font-weight: 600;
    }

    /* Botões */
    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #3267A8;
        color: #FFFFFF;
        border: none;
        border-radius: 7px;
        font-weight: 600;
        padding: 8px 18px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #244F85;
        color: #FFFFFF;
        border: none;
    }

    /* Tabelas */
    [data-testid="stDataFrame"] {
        border: 1px solid #E5EAF0;
        border-radius: 8px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# CABEÇALHO
# ==========================================

st.title("ERP Distribuidora")

st.caption(
    "Sistema de gestão de produtos, estoque e pedidos"
)

st.sidebar.title("Distribuidora")

st.sidebar.caption(
    "Gestão de produtos e pedidos"
)

st.sidebar.divider()


# ==========================================
# MENU PRINCIPAL
# ==========================================

aba = st.sidebar.radio(
    "Menu principal",
    [
        "Início",
        "Cadastrar produto",
        "Cadastrar pedido",
        "Produtos cadastrados",
        "Pedidos cadastrados",
        "Fila de prioridade",
        "Histórico e desfazer"
    ]
)


# ==========================================
# INÍCIO
# ==========================================

if aba == "Início":

    st.subheader("Visão geral")

    st.caption(
        "Acompanhe os principais dados da distribuidora."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Produtos cadastrados",
        value=len(produtos)
    )

    col2.metric(
        label="Pedidos registrados",
        value=len(pedidos)
    )

    col3.metric(
        label="Pedidos na fila",
        value=len(fila_prioridade)
    )

    st.divider()

    st.caption(
        "Utilize o menu lateral para acessar as funções do sistema."
    )


# ==========================================
# CADASTRAR PRODUTO
# ==========================================

elif aba == "Cadastrar produto":

    with st.container(border=True):

        st.subheader("Novo produto")

        st.caption(
            "Informe os dados do produto para adicioná-lo ao estoque."
        )

        st.divider()

        with st.form("form_produto"):

            codigo = st.number_input(
                "Código do produto",
                min_value=1,
                value=None,
                step=1,
                placeholder="Digite o código",
                key="produto_codigo"
            )

            nome = st.text_input(
                "Nome do produto",
                placeholder="Digite o nome do produto",
                key="produto_nome"
            )

            categoria = st.selectbox(
                "Categoria",
                options=categorias,
                index=None,
                placeholder="Selecione ou digite uma categoria",
                accept_new_options=True,
                key="produto_categoria"
            )

            preco = st.number_input(
                "Preço",
                min_value=0.01,
                value=None,
                step=0.01,
                placeholder="Digite o preço",
                key="produto_preco"
            )

            estoque = st.number_input(
                "Quantidade em estoque",
                min_value=0,
                value=None,
                step=1,
                placeholder="Digite a quantidade",
                key="produto_estoque"
            )

            st.form_submit_button(
                "Cadastrar produto",
                width="stretch",
                on_click=enviar_cadastro_produto
            )

    feedback = st.session_state.pop(
        "feedback_produto",
        None
    )

    if feedback is not None:

        resultado, mensagem = feedback

        if resultado:
            st.success(mensagem)
        else:
            st.error(mensagem)


# ==========================================
# CADASTRAR PEDIDO
# ==========================================

elif aba == "Cadastrar pedido":

    with st.container(border=True):

        st.subheader("Novo pedido")

        st.caption(
            "Informe os dados do cliente e do pedido para registrá-lo no sistema."
        )

        st.divider()

        if not produtos:

            st.warning(
                "Cadastre pelo menos um produto antes de criar pedidos."
            )

        else:

            with st.form("form_pedido"):

                numero = st.number_input(
                    "Número do pedido",
                    min_value=1,
                    value=None,
                    step=1,
                    placeholder="Digite o número do pedido",
                    key="pedido_numero"
                )

                cliente = st.text_input(
                    "Nome do cliente",
                    placeholder="Digite o nome do cliente",
                    key="pedido_cliente"
                )

                codigo_produto = st.number_input(
                    "Código do produto",
                    min_value=1,
                    value=None,
                    step=1,
                    placeholder="Digite o código do produto",
                    key="pedido_codigo_produto"
                )

                quantidade = st.number_input(
                    "Quantidade solicitada",
                    min_value=1,
                    value=None,
                    step=1,
                    placeholder="Digite a quantidade",
                    key="pedido_quantidade"
                )

                prioridade = st.selectbox(
                    "Prioridade",
                    [1, 2, 3],
                    format_func=lambda x: {
                        1: "Alta",
                        2: "Média",
                        3: "Baixa"
                    }[x],
                    key="pedido_prioridade"
                )

                st.form_submit_button(
                    "Cadastrar pedido",
                    width="stretch",
                    on_click=enviar_cadastro_pedido
                )

    feedback = st.session_state.pop(
        "feedback_pedido",
        None
    )

    if feedback is not None:

        resultado, mensagem = feedback

        if resultado:
            st.success(mensagem)
        else:
            st.error(mensagem)


# ==========================================
# PRODUTOS CADASTRADOS
# ==========================================

elif aba == "Produtos cadastrados":

    st.subheader("Produtos cadastrados")

    if produtos:

        categorias_produtos = []

        for produto in produtos:

            categoria = produto["categoria"]

            if categoria not in categorias_produtos:
                categorias_produtos.append(categoria)

        categorias_produtos.insert(0, "Todas")

        categoria_selecionada = st.selectbox(
            "Filtrar por categoria",
            categorias_produtos
        )

        if categoria_selecionada == "Todas":

            produtos_filtrados = produtos

        else:

            produtos_filtrados = filtrar_por_categoria(
                categoria_selecionada
            )

        st.write(
            f"Total de produtos encontrados: {len(produtos_filtrados)}"
        )

        if categoria_selecionada == "Todas":

            for categoria in categorias_produtos[1:]:

                st.markdown(f"### {categoria}")

                produtos_categoria = filtrar_por_categoria(
                    categoria
                )

                st.dataframe(
                    produtos_categoria,
                    width="stretch"
                )

        else:

            st.dataframe(
                produtos_filtrados,
                width="stretch"
            )

        st.divider()

        st.subheader("Relatório geral ordenado por nome")

        produtos_ordenados = ordenar_produtos_por_nome()

        st.dataframe(
            produtos_ordenados,
            width="stretch"
        )

    else:

        st.warning("Nenhum produto cadastrado.")


# ==========================================
# PEDIDOS CADASTRADOS
# ==========================================

elif aba == "Pedidos cadastrados":

    st.subheader("Pedidos cadastrados")

    if pedidos:

        pedidos_exibicao = []

        for pedido in pedidos:

            pedidos_exibicao.append({
                "Número do pedido": pedido["numero"],
                "Cliente": pedido["cliente"],
                "Produto": pedido["produto"],
                "Quantidade": pedido["quantidade"],
                "Prioridade": {
                    1: "Alta",
                    2: "Média",
                    3: "Baixa"
                }[pedido["prioridade"]],
                "Status": pedido["status"]
            })

        st.write(f"Total de pedidos: {len(pedidos)}")

        st.dataframe(
            pedidos_exibicao,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("Nenhum pedido cadastrado.")


# ==========================================
# FILA DE PRIORIDADE
# ==========================================

elif aba == "Fila de prioridade":

    st.subheader("Fila de pedidos")

    if fila_prioridade:

        fila_exibicao = []

        fila_ordenada = exibir_fila_prioridade()

        for pedido in fila_ordenada:

            fila_exibicao.append({
                "Número do pedido": pedido["numero"],
                "Cliente": pedido["cliente"],
                "Produto": pedido["produto"],
                "Quantidade": pedido["quantidade"],
                "Prioridade": {
                    1: "Alta",
                    2: "Média",
                    3: "Baixa"
                }[pedido["prioridade"]]
            })

        st.dataframe(
            fila_exibicao,
            width="stretch",
            hide_index=True
        )

        st.button(
            "Processar próximo pedido",
            width="stretch",
            on_click=processar_proximo_pedido
        )

    else:

        st.info("Não existem pedidos na fila.")

    feedback = st.session_state.pop(
        "feedback_fila",
        None
    )

    if feedback is not None:

        resultado, mensagem = feedback

        if resultado:
            st.success(mensagem)
        else:
            st.error(mensagem)


# ==========================================
# HISTÓRICO E DESFAZER
# ==========================================

elif aba == "Histórico e desfazer":

    st.subheader("Histórico de operações")

    if historico:

        for item in reversed(historico):
            st.write("•", item)

    else:

        st.info("Nenhuma operação registrada.")

    st.divider()

    st.button(
        "Desfazer última operação",
        width="stretch",
        on_click=desfazer_operacao
    )

    feedback = st.session_state.pop(
        "feedback_desfazer",
        None
    )

    if feedback is not None:

        resultado, mensagem = feedback

        if resultado:
            st.success(mensagem)
        else:
            st.warning(mensagem)
