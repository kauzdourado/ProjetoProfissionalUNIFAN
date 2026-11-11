from database.dados import fila
from views.entrada import ler_texto
from controllers.cliente_controller import achar_cliente_por_telefone


def entrar_na_fila():
    print("\n--- Entrar na Fila de espera ---")
    telefone = ler_texto("Telefone do cliente: ")
    cliente = achar_cliente_por_telefone(telefone)

    if not cliente:
        print("Cliente não cadastrado. Use a opção 1 para cadastrar primeiro.")
        return

    if cliente in fila:
        print(f"{cliente['nome']} já está na fila.")
        return

    fila.append(cliente)
    print(f"Cliente {cliente['nome']} entrou na fila! Posição na fila: {len(fila)}")


def mostrar_fila():
    print("\n=== Fila de atendimento ===")
    if not fila:
        print("A fila está vazia.")
        return
    for posicao, cliente in enumerate(fila, start=1):
        print(f"{posicao}º - {cliente['nome']}")


def atender_proximo():
    print("\n--- Atender próximo ---")
    if not fila:
        print("Ninguém na fila.")
        return
    cliente = fila.popleft()
    print(f"Chamando: {cliente['nome']}!")