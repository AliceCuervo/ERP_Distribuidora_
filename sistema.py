
from copy import deepcopy
import heapq
from itertools import count

from dados import (
    produtos,
    pedidos,
    fila_prioridade,
    historico,
    pilha_desfazer
)

# Contador para manter a ordem de chegada
# entre pedidos com a mesma prioridade.
ordem_fila = count()


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def normalizar_codigo(codigo):
    try:
        return int(codigo)
    except (ValueError, TypeError):
        return None


def buscar_produto(codigo):
    codigo = normalizar_codigo(codigo)

    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto

    return None


def buscar_pedido(numero):
    numero = normalizar_codigo(numero)

    for pedido in pedidos:
        if pedido["numero"] == numero:
            return pedido

    return None


def estoque_disponivel(codigo):
    produto = buscar_produto(codigo)

    if produto is None:
        return 0

    reservado = 0

    for pedido in pedidos:
        if (
            pedido["codigo_produto"] == produto["codigo"]
            and pedido["status"] == "Pendente"
        ):
            reservado += pedido["quantidade"]

    return produto["estoque"] - reservado


# ==========================================
# PILHA - REGISTRAR ESTADOS
# ==========================================

def registrar_estado():
    estado = deepcopy((
        produtos,
        pedidos,
        fila_prioridade,
        historico
    ))

    pilha_desfazer.append(estado)


# ==========================================
# CADASTRAR PRODUTO
# ==========================================

def cadastrar_produto(codigo, nome, categoria, preco, estoque):

    codigo = normalizar_codigo(codigo)

    if codigo is None or codigo <= 0:
        return False, "Informe um código válido."

    if buscar_produto(codigo) is not None:
        return False, "Já existe um produto com esse código."

    if nome is None or not str(nome).strip():
        return False, "O nome do produto é obrigatório."

    if categoria is None or not str(categoria).strip():
        return False, "Selecione uma categoria."

    try:
        preco = float(preco)
        estoque = int(estoque)
    except (ValueError, TypeError):
        return False, "Preço ou estoque inválido."

    if preco <= 0:
        return False, "O preço deve ser maior que zero."

    if estoque < 0:
        return False, "O estoque não pode ser negativo."

    produto = {
        "codigo": codigo,
        "nome": str(nome).strip(),
        "categoria": str(categoria).strip(),
        "preco": preco,
        "estoque": estoque
    }

    registrar_estado()

    produtos.append(produto)

    historico.append(
        f"Produto {produto['nome']} cadastrado."
    )

    return True, "Produto cadastrado com sucesso!"


# ==========================================
# LISTAR E FILTRAR PRODUTOS
# ==========================================

def listar_produtos():
    return produtos


def filtrar_por_categoria(categoria):
    resultado = []

    for produto in produtos:
        if produto["categoria"] == categoria:
            resultado.append(produto)

    return resultado


def ordenar_produtos_por_nome():
    return sorted(
        produtos,
        key=lambda produto: produto["nome"].lower()
    )


# ==========================================
# FILA DE PRIORIDADE
# ==========================================

def inserir_na_fila(pedido):
    heapq.heappush(
        fila_prioridade,
        (
            pedido["prioridade"],
            next(ordem_fila),
            pedido
        )
    )


def exibir_fila_prioridade():
    return [
        item[2]
        for item in sorted(fila_prioridade)
    ]


# ==========================================
# CADASTRAR PEDIDO
# ==========================================

def cadastrar_pedido(numero, cliente, produto, quantidade, prioridade):

    numero = normalizar_codigo(numero)
    codigo_produto = normalizar_codigo(produto)

    if numero is None or numero <= 0:
        return False, "Informe um número de pedido válido."

    if buscar_pedido(numero) is not None:
        return False, "Já existe um pedido com esse número."

    if cliente is None or not str(cliente).strip():
        return False, "O nome do cliente é obrigatório."

    if codigo_produto is None:
        return False, "Informe o código numérico do produto."

    produto_encontrado = buscar_produto(codigo_produto)

    if produto_encontrado is None:
        return False, "Este produto não está cadastrado. Verifique o código."

    try:
        quantidade = int(quantidade)
        prioridade = int(prioridade)
    except (ValueError, TypeError):
        return False, "Quantidade ou prioridade inválida."

    if quantidade <= 0:
        return False, "A quantidade deve ser maior que zero."

    if prioridade not in [1, 2, 3]:
        return False, "Prioridade inválida."

    disponivel = estoque_disponivel(codigo_produto)

    if quantidade > disponivel:
        return False, (
            f"Estoque insuficiente! Existem apenas "
            f"{disponivel} unidades disponíveis."
        )

    pedido = {
        "numero": numero,
        "cliente": str(cliente).strip(),
        "codigo_produto": codigo_produto,
        "produto": produto_encontrado["nome"],
        "quantidade": quantidade,
        "prioridade": prioridade,
        "status": "Pendente"
    }

    registrar_estado()

    pedidos.append(pedido)
    inserir_na_fila(pedido)

    historico.append(
        f"Pedido {numero} cadastrado para {cliente.strip()}."
    )

    return True, (
        f"Pedido cadastrado com sucesso! "
        f"Produto: {produto_encontrado['nome']}. "
        f"Estoque disponível para novos pedidos: "
        f"{estoque_disponivel(codigo_produto)} unidades."
    )


def listar_pedidos():
    return pedidos


# ==========================================
# ALTERAR PEDIDOS
# ==========================================

def alterar_pedido(
    numero,
    cliente=None,
    produto=None,
    quantidade=None,
    prioridade=None
):

    pedido = buscar_pedido(numero)

    if pedido is None:
        return False, "Pedido não encontrado."

    if pedido["status"] != "Pendente":
        return False, "Somente pedidos pendentes podem ser alterados."

    novo_codigo = pedido["codigo_produto"]

    if produto is not None:
        novo_codigo = normalizar_codigo(produto)

        if novo_codigo is None:
            return False, "Informe um código de produto válido."

        if buscar_produto(novo_codigo) is None:
            return False, "Produto não encontrado."

    try:
        nova_quantidade = (
            pedido["quantidade"]
            if quantidade is None
            else int(quantidade)
        )

        nova_prioridade = (
            pedido["prioridade"]
            if prioridade is None
            else int(prioridade)
        )

    except (ValueError, TypeError):
        return False, "Quantidade ou prioridade inválida."

    if nova_quantidade <= 0:
        return False, "A quantidade deve ser maior que zero."

    if nova_prioridade not in [1, 2, 3]:
        return False, "Prioridade inválida."

    if cliente is not None and not str(cliente).strip():
        return False, "O nome do cliente é obrigatório."

    produto_novo = buscar_produto(novo_codigo)

    disponivel = estoque_disponivel(novo_codigo)

    if novo_codigo == pedido["codigo_produto"]:
        disponivel += pedido["quantidade"]

    if nova_quantidade > disponivel:
        return False, (
            f"Estoque insuficiente! Existem apenas "
            f"{disponivel} unidades disponíveis."
        )

    registrar_estado()

    # Retira o pedido da fila antes de atualizar sua prioridade.
    fila_prioridade[:] = [
        item
        for item in fila_prioridade
        if item[2] is not pedido
    ]

    heapq.heapify(fila_prioridade)

    if cliente is not None:
        pedido["cliente"] = str(cliente).strip()

    pedido["codigo_produto"] = novo_codigo
    pedido["produto"] = produto_novo["nome"]
    pedido["quantidade"] = nova_quantidade
    pedido["prioridade"] = nova_prioridade

    inserir_na_fila(pedido)

    historico.append(
        f"Pedido {numero} alterado."
    )

    return True, "Pedido alterado com sucesso!"


# ==========================================
# REMOVER PEDIDOS
# ==========================================

def remover_pedido(numero):

    pedido = buscar_pedido(numero)

    if pedido is None:
        return False, "Pedido não encontrado."

    registrar_estado()

    pedidos.remove(pedido)

    fila_prioridade[:] = [
        item
        for item in fila_prioridade
        if item[2] is not pedido
    ]

    heapq.heapify(fila_prioridade)

    historico.append(
        f"Pedido {numero} removido."
    )

    return True, "Pedido removido com sucesso!"


def filtrar_pedidos_por_status(status):

    resultado = []

    for pedido in pedidos:
        if pedido["status"].lower() == status.lower():
            resultado.append(pedido)

    return resultado


# ==========================================
# PROCESSAR PEDIDOS
# ==========================================

def processar_pedido():

    if not fila_prioridade:
        return False, "Não existem pedidos na fila."

    pedido = fila_prioridade[0][2]

    produto = buscar_produto(pedido["codigo_produto"])

    if produto is None:
        return False, "O produto deste pedido não foi encontrado."

    if produto["estoque"] < pedido["quantidade"]:
        return False, "Estoque insuficiente para processar este pedido."

    registrar_estado()

    heapq.heappop(fila_prioridade)

    produto["estoque"] -= pedido["quantidade"]
    pedido["status"] = "Processado"

    historico.append(
        f"Pedido {pedido['numero']} processado. "
        f"{pedido['quantidade']} unidades de "
        f"{produto['nome']} retiradas do estoque."
    )

    return True, (
        f"Pedido {pedido['numero']} processado com sucesso! "
        f"Estoque restante de {produto['nome']}: "
        f"{produto['estoque']}."
    )


# ==========================================
# HISTÓRICO
# ==========================================

def exibir_historico():
    return historico


# ==========================================
# PILHA - DESFAZER OPERAÇÕES
# ==========================================

def desfazer_ultima_acao():

    if not pilha_desfazer:
        return False, "Não existem ações para desfazer."

    estado = pilha_desfazer.pop()

    (
        produtos_estado,
        pedidos_estado,
        fila_estado,
        historico_estado
    ) = estado

    produtos[:] = produtos_estado
    pedidos[:] = pedidos_estado
    fila_prioridade[:] = fila_estado
    historico[:] = historico_estado

    heapq.heapify(fila_prioridade)

    historico.append("Última operação desfeita.")

    return True, "Operação desfeita com sucesso!"
