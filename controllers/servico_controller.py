import mysql.connector

from models.servico import Servico
from repositories import servico_repository
from views.entrada import ler_inteiro, ler_preco, ler_texto


def listar_servicos():
    print("\n=== Lista de Serviços ===")
    servicos = servico_repository.listar()
    if not servicos:
        print("Nenhum serviço cadastrado.")
        return
    for s in servicos:
        print(f"ID: {s.id} | {s.nome} | R$ {s.preco:.2f}")


def adicionar_servico():
    print("\n--- Adicionar Serviço ---")
    nome = ler_texto("Nome do serviço: ")
    preco = ler_preco("Preço do serviço: R$ ")
    if preco is None:
        print("Cadastro cancelado.")
        return

    servico_repository.inserir(Servico(nome, preco))
    print("Serviço adicionado com sucesso!")


def alterar_servicos():
    print("\n--- Alterar Serviço ---")
    if not servico_repository.listar():
        print("Nenhum serviço cadastrado.")
        return

    listar_servicos()
    id_servico = ler_inteiro("ID do serviço a alterar (Enter cancela): ")
    if id_servico is None:
        return

    atual = servico_repository.buscar_por_id(id_servico)
    if atual is None:
        print("Serviço não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")

    novo_nome = input(f"Novo nome [{atual.nome}]: ").strip()
    if novo_nome:
        atual.nome = novo_nome

    novo_preco = ler_preco(f"Novo preço [{atual.preco:.2f}]: R$ ")
    if novo_preco is not None:
        atual.preco = novo_preco

    servico_repository.atualizar(atual)
    print("Serviço alterado com sucesso!")


def excluir_servico():
    print("\n--- Excluir Serviço ---")
    if not servico_repository.listar():
        print("Nenhum serviço cadastrado.")
        return

    listar_servicos()
    id_servico = ler_inteiro("ID do serviço a excluir (Enter cancela): ")
    if id_servico is None:
        return

    servico = servico_repository.buscar_por_id(id_servico)
    if servico is None:
        print("Serviço não encontrado.")
        return

    confirmacao = input(f"Excluir '{servico.nome}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        try:
            servico_repository.excluir(id_servico)
            print(f"Serviço '{servico.nome}' excluído com sucesso!")
        except mysql.connector.IntegrityError:
            print("Não é possível excluir: esse serviço já está em agendamentos.")
    else:
        print("Exclusão cancelada.")