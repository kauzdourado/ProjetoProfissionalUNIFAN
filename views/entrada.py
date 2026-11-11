from datetime import datetime, date


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