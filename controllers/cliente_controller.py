from datetime import date

from models.cliente import Cliente
from repositories import cliente_repository
from views.entrada import ler_texto, ler_data, apenas_digitos


def calcular_idade(nascimento):
    hoje = date.today()
    idade = hoje.year - nascimento.year
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1
    return idade


def tipo_cliente(cliente):
    idade = calcular_idade(cliente.nascimento)
    return "Adulto" if idade >= 18 else "Menor de idade"


def achar_cliente_por_telefone(telefone):
    telefone = apenas_digitos(telefone)
    return cliente_repository.buscar_por_telefone(telefone)


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

    cliente = Cliente(nome, telefone, email, nascimento, problema_quimico)
    cliente_repository.inserir(cliente)
    print(f"Cliente {nome} cadastrado com sucesso! ({tipo_cliente(cliente)})")


def buscar_cliente():
    print("\n--- BUSCAR CLIENTE ---")
    telefone = ler_texto("Telefone do cliente: ")
    cliente = achar_cliente_por_telefone(telefone)

    if cliente:
        idade = calcular_idade(cliente.nascimento)
        print(f"Nome: {cliente.nome}")
        print(f"Telefone: {cliente.telefone}")
        print(f"Email: {cliente.email}")
        print(f'Data de nascimento: {cliente.nascimento.strftime("%d/%m/%Y")} (Idade: {idade})')
        print(f"Problema com produto químico: {cliente.problema_quimico}")
    else:
        print("Cliente não encontrado.")