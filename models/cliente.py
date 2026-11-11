class Cliente:
    def __init__(self, nome, telefone, email, nascimento,
                 problema_quimico="Nenhum", id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.nascimento = nascimento
        self.problema_quimico = problema_quimico