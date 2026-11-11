-- PROJETO: BARBEARIA ABOBRINHA

CREATE DATABASE IF NOT EXISTS barbearia_abobrinha;
USE barbearia_abobrinha;

-- 1. TABELAS (DDL)

CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Barbeiro (
    id_barbeiro INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Servico (
    id_servico INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS Agendamento (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    data_atendimento DATE NOT NULL,
    horario TIME NOT NULL,
    id_cliente INT NOT NULL,
    id_barbeiro INT NOT NULL,
    id_servico INT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_barbeiro) REFERENCES Barbeiro(id_barbeiro)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (id_barbeiro, data_atendimento, horario)
);

CREATE TABLE IF NOT EXISTS Lista_Espera (
    id_espera INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    data_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Aguardando','Chamado','Cancelado')
        DEFAULT 'Aguardando' NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT
);


-- 2. DADOS DE TESTE (DML)

INSERT INTO Cliente (nome, telefone) VALUES
('Joao Silva', '74999990001'),
('Maria Santos', '74999990002'),
('Pedro Oliveira', '74999990003');

INSERT INTO Barbeiro (nome, especialidade) VALUES
('Carlos Souza', 'Corte masculino'),
('Rafael Lima', 'Barba e acabamento');

INSERT INTO Servico (nome, preco) VALUES
('Corte de cabelo', 30.00),
('Barba', 20.00),
('Sobrancelha', 15.00),
('Corte + Barba + Sobrancelha', 55.00),
('Corte + Barba', 40.00);

INSERT INTO Agendamento
(data_atendimento, horario, id_cliente, id_barbeiro, id_servico)
VALUES
('2026-10-15', '09:00', 1, 1, 1),
('2026-10-15', '10:00', 2, 2, 2),
('2026-10-16', '14:00', 3, 1, 5);

INSERT INTO Lista_Espera (id_cliente) VALUES (1), (3);

-- 3. CONSULTAS (SELECT)

-- Serviços e preços
SELECT * FROM Servico;

-- Buscar cliente
SELECT * FROM Cliente
WHERE telefone = '74999990001';

-- Agendamentos completos (INNER JOIN)
SELECT c.nome AS cliente, b.nome AS barbeiro,
       s.nome AS servico, s.preco,
       a.data_atendimento, a.horario
FROM Agendamento a
INNER JOIN Cliente c ON c.id_cliente = a.id_cliente
INNER JOIN Barbeiro b ON b.id_barbeiro = a.id_barbeiro
INNER JOIN Servico s ON s.id_servico = a.id_servico;

-- Total por cliente (SUM, GROUP BY, HAVING)
SELECT c.nome, SUM(s.preco) AS total_previsto
FROM Agendamento a
INNER JOIN Cliente c ON c.id_cliente = a.id_cliente
INNER JOIN Servico s ON s.id_servico = a.id_servico
GROUP BY c.id_cliente, c.nome
HAVING SUM(s.preco) > 0;

-- Agendamentos por barbeiro (LEFT JOIN e COUNT)
SELECT b.nome, COUNT(a.id_agendamento) AS quantidade
FROM Barbeiro b
LEFT JOIN Agendamento a ON a.id_barbeiro = b.id_barbeiro
GROUP BY b.id_barbeiro, b.nome;

-- Fila de espera (FIFO)
SELECT c.nome, e.data_entrada, e.status
FROM Lista_Espera e
INNER JOIN Cliente c ON c.id_cliente = e.id_cliente
WHERE e.status = 'Aguardando'
ORDER BY e.data_entrada, e.id_espera;

-- Subconsulta: serviços acima da média
SELECT nome, preco FROM Servico
WHERE preco > (SELECT AVG(preco) FROM Servico);

-- 4. VIEW

CREATE OR REPLACE VIEW vw_agendamentos_detalhados AS
SELECT c.nome AS cliente, c.telefone, b.nome AS barbeiro,
       s.nome AS servico, s.preco,
       a.data_atendimento, a.horario
FROM Agendamento a
INNER JOIN Cliente c ON c.id_cliente = a.id_cliente
INNER JOIN Barbeiro b ON b.id_barbeiro = a.id_barbeiro
INNER JOIN Servico s ON s.id_servico = a.id_servico;

SELECT * FROM vw_agendamentos_detalhados;

-- 5. UPDATE: alterar preço
UPDATE Servico SET preco = 32.00
WHERE id_servico = 1;

ALTER TABLE Cliente
    ADD COLUMN email VARCHAR(100),
    ADD COLUMN data_nascimento DATE,
    ADD COLUMN problema_quimico VARCHAR(100) NOT NULL DEFAULT 'Nenhum';

-- completa os clientes de teste que já existiam (senão a idade quebra)
UPDATE Cliente
SET email = CONCAT(LOWER(REPLACE(nome, ' ', '.')), '@email.com'),
    data_nascimento = '1990-01-01'
WHERE id_cliente > 0 AND data_nascimento IS NULL;


-- 6. TESTES DE RESTRIÇÕES
-- Execute cada teste separadamente para ver o erro.

-- FK: cliente inexistente
-- INSERT INTO Agendamento
-- (data_atendimento, horario, id_cliente, id_barbeiro, id_servico)
-- VALUES ('2026-10-20', '11:00', 999, 1, 1);

-- UNIQUE: telefone duplicado
-- INSERT INTO Cliente (nome, telefone)
-- VALUES ('Cliente Repetido', '74999990001');

-- CHECK: preço negativo
-- INSERT INTO Servico (nome, preco)
-- VALUES ('Servico invalido', -5.00);

-- UNIQUE: horário ocupado
-- INSERT INTO Agendamento
-- (data_atendimento, horario, id_cliente, id_barbeiro, id_servico)
-- VALUES ('2026-10-15', '09:00', 2, 1, 2);