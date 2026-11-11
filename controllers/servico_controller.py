from database.dados import servicos
from views.entrada import ler_inteiro, ler_preco, ler_texto


def listar_servicos():
    print("\n=== Lista de Serviços ===")
    if not servicos:
        print("Nenhum serviço cadastrado.")
        return
    for id_servico, dados in servicos.items():
        print(f"ID: {id_servico} | {dados['nome']} | R$ {dados['preco']:.2f}")


def adicionar_servico():
    print("\n--- Adicionar Serviço ---")
    nome = ler_texto("Nome do serviço: ")
    preco = ler_preco("Preço do serviço: R$ ")
    if preco is None:
        print("Cadastro cancelado.")
        return

    novo_id = max(servicos) + 1 if servicos else 1
    servicos[novo_id] = {"nome": nome, "preco": preco}
    print("Serviço adicionado com sucesso!")


def alterar_servicos():
    print("\n--- Alterar Serviço ---")
    if not servicos:
        print("Nenhum serviço cadastrado.")
        return

    listar_servicos()
    id_servico = ler_inteiro("ID do serviço a alterar (Enter cancela): ")
    if id_servico is None:
        return
    if id_servico not in servicos:
        print("Serviço não encontrado.")
        return

    atual = servicos[id_servico]
    print("Deixe em branco para manter o valor atual.")

    novo_nome = input(f"Novo nome [{atual['nome']}]: ").strip()
    if novo_nome:
        atual["nome"] = novo_nome

    novo_preco = ler_preco(f"Novo preço [{atual['preco']:.2f}]: R$ ")
    if novo_preco is not None:
        atual["preco"] = novo_preco

    print("Serviço alterado com sucesso!")


def excluir_servico():
    print("\n--- Excluir Serviço ---")
    if not servicos:
        print("Nenhum serviço cadastrado.")
        return

    listar_servicos()
    id_servico = ler_inteiro("ID do serviço a excluir (Enter cancela): ")
    if id_servico is None:
        return
    if id_servico not in servicos:
        print("Serviço não encontrado.")
        return

    nome = servicos[id_servico]["nome"]
    confirmacao = input(f"Excluir '{nome}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        del servicos[id_servico]
        print(f"Serviço '{nome}' excluído com sucesso!")
    else:
        print("Exclusão cancelada.")