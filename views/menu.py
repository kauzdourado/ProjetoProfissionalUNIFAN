import sys

from controllers.cliente_controller import cadastrar_cliente, buscar_cliente
from controllers.fila_controller import mostrar_fila, entrar_na_fila, atender_proximo
from controllers.servico_controller import (
    adicionar_servico,
    alterar_servicos,
    listar_servicos,
    excluir_servico,
)


def sair_sistema():
    print("Encerrando o sistema da Barbearia Abobrinha. Até logo!")
    sys.exit()


OPCOES = {
    "1": ("Cadastrar cliente", cadastrar_cliente),
    "2": ("Buscar cliente (telefone)", buscar_cliente),
    "3": ("Mostrar fila", mostrar_fila),
    "4": ("Entrar na fila de espera", entrar_na_fila),
    "5": ("Atender próximo da fila", atender_proximo),
    "6": ("Adicionar serviço", adicionar_servico),
    "7": ("Alterar serviço", alterar_servicos),
    "8": ("Listar serviços", listar_servicos),
    "9": ("Excluir serviço", excluir_servico),
    "0": ("Sair", sair_sistema),
}


def menu():
    while True:
        print("\n======================================")
        print(" Bem-vindo à Barbearia Abobrinha!")
        print("======================================")
        for tecla, (descricao, _) in OPCOES.items():
            print(f"{tecla}. {descricao}")
        print("======================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao in OPCOES:
            OPCOES[opcao][1]()
        else:
            print("\nOpção inválida!")