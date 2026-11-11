from repositories import fila_repository
from views.entrada import ler_texto
from controllers.cliente_controller import achar_cliente_por_telefone


def entrar_na_fila():
    print("\n--- Entrar na Fila de espera ---")
    telefone = ler_texto("Telefone do cliente: ")
    cliente = achar_cliente_por_telefone(telefone)

    if not cliente:
        print("Cliente não cadastrado. Use a opção 1 para cadastrar primeiro.")
        return

    if fila_repository.cliente_na_fila(cliente.id):
        print(f"{cliente.nome} já está na fila.")
        return

    fila_repository.entrar(cliente.id)
    posicao = len(fila_repository.listar())
    print(f"Cliente {cliente.nome} entrou na fila! Posição na fila: {posicao}")


def mostrar_fila():
    print("\n=== Fila de atendimento ===")
    fila = fila_repository.listar()
    if not fila:
        print("A fila está vazia.")
        return
    for posicao, item in enumerate(fila, start=1):
        print(f"{posicao}º - {item['nome']}")


def atender_proximo():
    print("\n--- Atender próximo ---")
    nome = fila_repository.chamar_proximo()
    if nome is None:
        print("Ninguém na fila.")
        return
    print(f"Chamando: {nome}!")