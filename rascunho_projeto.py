import sys
from collections import deque
from datetime import datetime, date

servicos = {
    1: {"nome": "Corte de cabelo", "preco": 30.00},
    2: {"nome": "Barba", "preco": 20.00},
    3: {"nome": "Sobrancelha", "preco": 15.00},
    4: {"nome": "Corte de cabelo + Barba + Sobrancelha", "preco": 55.00},
    5: {"nome": "Corte de cabelo + Barba", "preco": 40.00},
}

clientes = []
fila = deque()

# ------------------------------------------------------------------
# FUNÇÕES para evitar repetição
# ------------------------------------------------------------------

def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor == "":
            return None  # CORREÇÃO: Enter cancela (antes dava erro com int(""))
        try:
            return int(valor)
        except ValueError:
            print("Digite apenas números inteiros (ou Enter para cancelar).")


def ler_preco(mensagem):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        if valor == "":
            return None
        try:
            preco = float(valor)
            if preco <= 0:
                print("O preço precisa ser maior que zero.")
                continue
            return preco
        except ValueError:
            print("Preço inválido. Exemplo: 25.50")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Este campo não pode ficar vazio.")


def apenas_digitos(telefone):
    return "".join(c for c in telefone if c.isdigit())

def ler_data(mensagem):
    while True:
        texto = ler_texto(mensagem)
        try:
            data = datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa. Exemplo: 25/03/1998")
            continue
        if data > date.today():
            print("A data não pode ser no futuro.")
            continue
        return data

def calcular_idade(nascimento):
        hoje = date.today()
        idade = hoje.year - nascimento.year
        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1
        return idade

def tipo_cliente(cliente):
        idade = calcular_idade(cliente["nascimento"])
        return "Adulto" if idade >= 18 else "Menor de idade"

def achar_cliente_por_telefone(telefone):
    telefone = apenas_digitos(telefone)
    for cliente in clientes:
        if cliente["telefone"] == telefone:
            return cliente
    return None

# ------------------------------------------------------------------
# CLIENTES
# ------------------------------------------------------------------

def cadastrar_cliente():
    print("\n--- CADASTRAR CLIENTE ---")
    nome = ler_texto("Nome do cliente: ")
    telefone = apenas_digitos(ler_texto("Telefone do cliente: "))

    if len(telefone) < 8:
        print("Telefone inválido.")
        return

    if achar_cliente_por_telefone(telefone):
        print("Já existe um cliente com esse telefone.")
        return

    email = ler_texto("Email do cliente: ")
    if "@" not in email or "." not in email:
        print("Email inválido.")
        return
    nascimento = ler_data("Data de nascimento (dd/mm/aaaa): ")

    resposta = input("Tem problema com produto químico? (s/n): ").strip().lower()
    if resposta == "s":
        problema_quimico = ler_texto("Qual produto/problema: ")
    else:
        problema_quimico = "Nenhum"

    clientes.append({
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nascimento": nascimento,
        "problema_quimico": problema_quimico,
        })
    cliente = clientes[-1]
    print(f"Cliente {nome} cadastrado com sucesso! ({tipo_cliente(cliente)})")

def buscar_cliente():
    print("\n--- BUSCAR CLIENTE ---")
    telefone = ler_texto("Telefone do cliente: ")
    cliente = achar_cliente_por_telefone(telefone)

    if cliente:
        idade = calcular_idade(cliente["nascimento"])
        print(f'Nome: {cliente["nome"]}')
        print(f'Telefone: {cliente["telefone"]}')
        print(f'Email: {cliente["email"]}')
        print(f'Data de nascimento: {cliente["nascimento"].strftime("%d/%m/%Y")} (Idade: {idade})')
        print(f'Problema com produto químico: {cliente["problema_quimico"]}')
    else:
        print("Cliente não encontrado.")


# ------------------------------------------------------------------
# FILA DE ESPERA
# ------------------------------------------------------------------

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

# ------------------------------------------------------------------
# SERVIÇOS
# ------------------------------------------------------------------

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

# ------------------------------------------------------------------
# SAIR
# ------------------------------------------------------------------

def sair_sistema():
    print("Encerrando o sistema da Barbearia Abobrinha. Até logo!")
    sys.exit()

# ------------------------------------------------------------------
# MENU
# ------------------------------------------------------------------

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


if __name__ == "__main__":
    menu()