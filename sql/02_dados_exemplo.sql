-- =============================================================
-- Zoolife — 02_dados_exemplo.sql
-- Dados de exemplo FICTÍCIOS (10 registros por tabela).
-- Rode depois de 01_schema.sql.
-- =============================================================

SET NAMES utf8mb4;
USE clinica;

INSERT INTO empresa (Nome, CNPJ, email, telefone, endereco) VALUES
    ('Clinica Matriz Centro',     '12345678000190', 'centro@example.com',     '2132548790', 'Av. Presidente Vargas, 100'),
    ('Clinica Filial Tijuca',     '98765432000110', 'tijuca@example.com',     '2125698044', 'Praca Saens Pena, 20'),
    ('Clinica Filial Barra',      '45678901000122', 'barra@example.com',      '2130887123', 'Av. das Americas, 500'),
    ('Clinica Filial Copacabana', '23456789000130', 'copacabana@example.com', '2122456789', 'Rua Barata Ribeiro, 300'),
    ('Clinica Filial Botafogo',   '34567890000140', 'botafogo@example.com',   '2138760912', 'Rua Voluntarios, 150'),
    ('Clinica Filial Leblon',     '56789012000155', 'leblon@example.com',     '2124561122', 'Av. Ataulfo de Paiva, 800'),
    ('Clinica Filial Meier',      '67890123000160', 'meier@example.com',      '2134908877', 'Rua Dias da Cruz, 400'),
    ('Clinica Filial Bangu',      '78901234000175', 'bangu@example.com',      '2133214567', 'Rua Silva Cardoso, 200'),
    ('Clinica Filial Ipanema',    '89012345000180', 'ipanema@example.com',    '2125549000', 'Rua Visconde, 100'),
    ('Clinica Filial Madureira',  '90123456000195', 'madureira@example.com',  '2130981515', 'Estrada do Portela, 99');

INSERT INTO cliente (CPF, Nome_Ani, email, End_DESC, End_CEP, Nome_Cli) VALUES
    ('19032343550', 'Zoe Maria', 'cliente01@example.com', 'Rua Flor 69',            '21080345', 'Mariana Alves'),
    ('19063525230', 'Fred',      'cliente02@example.com', 'Rua Niteroi 23',         '21302300', 'Paulo Ribeiro'),
    ('19032308040', 'Marrocos',  'cliente03@example.com', 'Rua Humaita 7',          '22309323', 'Larissa Duarte'),
    ('14178050471', 'Lola',      'cliente04@example.com', 'Rua Francisco',          '21050001', 'Rodrigo Teixeira'),
    ('18939365470', 'Mengo',     'cliente05@example.com', 'Rua Bonjour 123 fundos', '22090045', 'Vanessa Moreira'),
    ('13390381060', 'Musa',      'cliente06@example.com', 'Rua Verdeal 91',         '21050233', 'Eduardo Lopes'),
    ('19216823470', 'Amora',     'cliente07@example.com', 'Rua Ferdora Faz 34',     '19054004', 'Patricia Gomes'),
    ('16210243032', 'Rex',       'cliente08@example.com', 'Rua Puerto Lilás 24',    '21042546', 'Renato Barbosa'),
    ('10134564320', 'Katy',      'cliente09@example.com', 'Rua Parque Molto 01',    '10234000', 'Tatiane Cardoso'),
    ('23309023410', 'Felix',     'cliente10@example.com', 'Rua Recreio Frota 09',   '21050600', 'Marcelo Antunes');

INSERT INTO telefone (NumeroCEL, Cli_CPF) VALUES
    ('21998345671', '19032343550'),
    ('21982451099', '19063525230'),
    ('21976332011', '19032308040'),
    ('21993214588', '14178050471'),
    ('21988445522', '18939365470'),
    ('21975661234', '13390381060'),
    ('21991223040', '19216823470'),
    ('21983441155', '16210243032'),
    ('21974558090', '10134564320'),
    ('21992113476', '23309023410');

-- Cada veterinário vinculado a uma empresa (Empresa_ID é obrigatório).
INSERT INTO veterinario (Vet_ID, Nome, CRMV, Especialidade, CPF, Empresa_ID) VALUES
    (1,  'Dr. Roberto',   1001, 'Cirurgia',     '45561230988', 1),
    (2,  'Dra. Amanda',   1002, 'Dermatologia', '21190834577', 1),
    (3,  'Dra. Fernanda', 1003, 'Oncologia',    '34456712309', 2),
    (4,  'Dr. Lucas',     1004, 'Geral',        '89912345600', 2),
    (5,  'Dr. Pedro',     1005, 'Ortopedia',    '56678901234', 3),
    (6,  'Dra. Camila',   1006, 'Felinos',      '12234456678', 4),
    (7,  'Dr. Thiago',    1007, 'Silvestres',   '78890012345', 5),
    (8,  'Dra. Beatriz',  1008, 'Cardiologia',  '90012234456', 6),
    (9,  'Dr. Marcos',    1009, 'Neurologia',   '23345567789', 7),
    (10, 'Dra. Silvia',   1010, 'Geral',        '67789901123', 8);

INSERT INTO telefone_vet (Num_Cel, Vet_CPF) VALUES
    ('21987654321', '45561230988'),
    ('21996541230', '21190834577'),
    ('21981239988', '34456712309'),
    ('21974561029', '89912345600'),
    ('21993445566', '56678901234'),
    ('21988772030', '12234456678'),
    ('21971223344', '78890012345'),
    ('21998556677', '90012234456'),
    ('21982334455', '23345567789'),
    ('21976445588', '67789901123');

INSERT INTO animal (Nome, Especie, Raca, MicroChip, Sexo, Dono_CPF) VALUES
    ('Zoe Maria', 'Cachorro', 'Poodle',           'Sim', 'F', '19032343550'),
    ('Fred',      'Cachorro', 'Golden Retriever', 'Nao', 'M', '19063525230'),
    ('Marrocos',  'Gato',     'Siames',           'Sim', 'M', '19032308040'),
    ('Lola',      'Cachorro', 'Bulldog',          'Sim', 'F', '14178050471'),
    ('Mengo',     'Cachorro', 'Vira-lata',        'Nao', 'M', '18939365470'),
    ('Musa',      'Gato',     'Persa',            'Nao', 'F', '13390381060'),
    ('Amora',     'Cachorro', 'Shih Tzu',         'Sim', 'F', '19216823470'),
    ('Rex',       'Cachorro', 'Pastor Alemao',    'Nao', 'M', '16210243032'),
    ('Katy',      'Gato',     'Frajola',          'Sim', 'F', '10134564320'),
    ('Felix',     'Gato',     'Vira-lata',        'Nao', 'M', '23309023410');

INSERT INTO vacinacao (VacinaID, Nome_Vacina, dataApli, Dt_Prox_Dose, Animal_ID) VALUES
    (1,  'Antirrabica',  '2025-01-15', '2026-01-15', 1),
    (2,  'V10',          '2025-02-10', '2026-02-10', 2),
    (3,  'Gripe Canina', '2025-03-05', '2026-03-05', 3),
    (4,  'Giardia',      '2025-04-20', '2026-04-20', 4),
    (5,  'Antirrabica',  '2025-05-12', '2026-05-12', 5),
    (6,  'V4 Felina',    '2025-06-18', '2026-06-18', 6),
    (7,  'Leishmaniose', '2025-07-22', '2026-07-22', 7),
    (8,  'Antirrabica',  '2025-08-30', '2026-08-30', 8),
    (9,  'V10',          '2025-09-15', '2026-09-15', 9),
    (10, 'V4 Felina',    '2025-10-10', '2026-10-10', 10);

INSERT INTO consulta (data_hora, sintomas, valor, Animal_ID, Vet_CPF) VALUES
    ('2026-06-08 10:00:00', 'Febre e vomito',            150.00, 1,  '45561230988'),
    ('2026-06-08 11:00:00', 'Coceira intensa',           120.00, 2,  '21190834577'),
    ('2026-06-08 13:00:00', 'Manqueira pata traseira',   200.00, 3,  '56678901234'),
    ('2026-06-08 14:00:00', 'Tosse seca',                150.00, 4,  '89912345600'),
    ('2026-06-09 09:00:00', 'Rotina e vacina',           100.00, 5,  '67789901123'),
    ('2026-06-09 10:30:00', 'Apatia e falta de apetite', 180.00, 6,  '12234456678'),
    ('2026-06-09 15:00:00', 'Checkup cardiologico',      250.00, 7,  '90012234456'),
    ('2026-06-10 11:00:00', 'Convulsao',                 300.00, 8,  '23345567789'),
    ('2026-06-10 14:30:00', 'Nodulo no pescoco',         200.00, 9,  '34456712309'),
    ('2026-06-10 16:00:00', 'Corte na orelha - Felix',   150.00, 10, '45561230988');

INSERT INTO funcionario (Nome_Completo, CPF, Cargo, Salario, Empresa_ID) VALUES
    ('Ana Costa',    '10293847561', 'Recepcionista',    2500.00, 1),
    ('Carlos Souza', '09812345672', 'Auxiliar Limpeza', 1800.00, 1),
    ('Beto Silva',   '83746509123', 'Gerente',          4500.00, 2),
    ('Diana Lima',   '74658392014', 'Recepcionista',    2500.00, 2),
    ('Elaine Reis',  '56473829105', 'Enfermeira Vet',   3200.00, 3),
    ('Fabio Nunes',  '38475610296', 'Enfermeiro Vet',   3200.00, 4),
    ('Gisele Faria', '91827364507', 'Recepcionista',    2500.00, 5),
    ('Helio Rocha',  '27364519808', 'Seguranca',        2200.00, 6),
    ('Igor Mendes',  '46573829109', 'Auxiliar Limpeza', 1800.00, 7),
    ('Julia Pires',  '65748392010', 'Recepcionista',    2500.00, 8);

INSERT INTO pagamento (Forma_Pagamento, Valor, Descricao, Data_Pagamento, ConsultaID) VALUES
    ('Pix',      150.00, 'Consulta Emergencia',    '2026-06-08', 1),
    ('Cartao',   120.00, 'Consulta Dermato',       '2026-06-08', 2),
    ('Dinheiro', 200.00, 'Consulta Ortopedia',     '2026-06-08', 3),
    ('Pix',      150.00, 'Consulta Clinica Geral', '2026-06-08', 4),
    ('Cartao',   100.00, 'Consulta de Rotina',     '2026-06-09', 5),
    ('Boleto',   180.00, 'Consulta Especialista',  '2026-06-09', 6),
    ('Pix',      250.00, 'Consulta Cardio',        '2026-06-09', 7),
    ('Cartao',   300.00, 'Consulta Neuro',         '2026-06-10', 8),
    ('Pix',      200.00, 'Consulta Onco',          '2026-06-10', 9),
    ('Dinheiro', 150.00, 'Atendimento Felix',      '2026-06-10', 10);

INSERT INTO medicamento (Nome, Fabricante, Qntd_Estoque, Preco) VALUES
    ('Antibiotico Pet',      'VetFarma',    50,  45.90),
    ('Anti-inflamatorio',    'SaudeAnimal', 30,  32.50),
    ('Pomada Cicatrizante',  'CuraVet',     20,  25.00),
    ('Vermifugo Plus',       'VetFarma',    100, 15.00),
    ('Shampoo Sarna',        'PeleBoa',     15,  60.00),
    ('Colirio Lubrificante', 'OlhoPet',     40,  40.00),
    ('Vitamina C',           'SaudeAnimal', 80,  22.00),
    ('Anticonvulsivante',    'NeuroVet',    25,  120.00),
    ('Suplemento Articular', 'OrtoPet',     35,  95.00),
    ('Soro Reidratante',     'CuraVet',     200, 10.00);

INSERT INTO receita (Dosagem, Frequencia, ConsultaID, Medicamento_ID) VALUES
    ('1 comprimido',      'De 12 em 12 horas', 1,  1),
    ('Aplicar no local',  '2 vezes ao dia',    2,  5),
    ('Meio comprimido',   'De 8 em 8 horas',   3,  2),
    ('2 ml',              'Uma vez ao dia',    4,  7),
    ('1 dose unica',      'Apenas hoje',       5,  4),
    ('Reidratacao lenta', 'Continuo',          6,  10),
    ('1 comprimido',      'A cada 24 horas',   7,  9),
    ('2 gotas',           'De 12 em 12 horas', 8,  8),
    ('Passar na ferida',  '3 vezes ao dia',    9,  3),
    ('Limpar e aplicar',  'Diariamente',       10, 3);

INSERT INTO exame (tipo_exame, Resultado, data_Exame, ConsultaID) VALUES
    ('Hemograma',         'Alterado - Infeccao', '2026-06-08', 1),
    ('Raspado de Pele',   'Negativo para Sarna', '2026-06-08', 2),
    ('Raio-X Pata',       'Fratura Leve',        '2026-06-08', 3),
    ('Ultrassom Torax',   'Normal',              '2026-06-08', 4),
    ('Exame de Fezes',    'Negativo',            '2026-06-09', 5),
    ('Glicemia',          'Baixa',               '2026-06-09', 6),
    ('Eletrocardiograma', 'Arritmia Leve',       '2026-06-09', 7),
    ('Tomografia',        'Normal',              '2026-06-10', 8),
    ('Biopsia Nodulo',    'Benigno',             '2026-06-10', 9),
    ('Coagulograma',      'Normal',              '2026-06-10', 10);
