from collections import deque

servicos = {
    1: {"nome": "Corte de cabelo", "preco": 30.00},
    2: {"nome": "Barba", "preco": 20.00},
    3: {"nome": "Sobrancelha", "preco": 15.00},
    4: {"nome": "Corte de cabelo + Barba + Sobrancelha", "preco": 55.00},
    5: {"nome": "Corte de cabelo + Barba", "preco": 40.00},
}

clientes = []
fila = deque()