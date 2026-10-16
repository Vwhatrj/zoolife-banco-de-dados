-- =============================================================
-- Zoolife — Banco de dados da rede de clínicas veterinárias
-- 01_schema.sql: criação do banco e das 12 tabelas (MariaDB)
-- =============================================================
-- Atenção: apaga e recria o banco `clinica` do zero.

DROP DATABASE IF EXISTS clinica;
CREATE DATABASE clinica CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE clinica;

-- Empresa vem primeiro: veterinario e funcionario dependem dela.
CREATE TABLE empresa (
    Empresa_ID INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nome       VARCHAR(120),
    CNPJ       VARCHAR(14)  UNIQUE,
    email      VARCHAR(100),
    telefone   VARCHAR(15),
    endereco   VARCHAR(120)
);

CREATE TABLE cliente (
    CPF      VARCHAR(11)  NOT NULL PRIMARY KEY,
    Nome_Ani VARCHAR(40),
    email    VARCHAR(40),
    End_DESC VARCHAR(255),
    End_CEP  VARCHAR(40),
    Nome_Cli VARCHAR(80)
);

-- Regra de negócio: todo veterinário está vinculado a uma empresa/filial.
CREATE TABLE veterinario (
    CPF           VARCHAR(11) NOT NULL PRIMARY KEY,
    Vet_ID        INT(11),
    Nome          VARCHAR(60),
    CRMV          INT(20),
    Especialidade VARCHAR(50),
    Empresa_ID    INT         NOT NULL,
    FOREIGN KEY (Empresa_ID) REFERENCES empresa (Empresa_ID)
);

CREATE TABLE telefone (
    Tel_ID    INT(20)     NOT NULL AUTO_INCREMENT PRIMARY KEY,
    NumeroCEL VARCHAR(15),
    Cli_CPF   VARCHAR(11),
    FOREIGN KEY (Cli_CPF) REFERENCES cliente (CPF)
);

CREATE TABLE telefone_vet (
    Tel_ID  INT(11)     NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Num_Cel VARCHAR(15),
    Vet_CPF VARCHAR(11),
    FOREIGN KEY (Vet_CPF) REFERENCES veterinario (CPF)
);

-- Regra de negócio: todo animal tem um dono.
CREATE TABLE animal (
    Animal_ID INT(11)     NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nome      VARCHAR(70),
    Especie   VARCHAR(40),
    Raca      VARCHAR(40),
    MicroChip ENUM('Sim', 'Nao'),
    Sexo      ENUM('F', 'M'),
    Dono_CPF  VARCHAR(11) NOT NULL,
    FOREIGN KEY (Dono_CPF) REFERENCES cliente (CPF)
);

CREATE TABLE vacinacao (
    VacinaID     INT(11)     NOT NULL PRIMARY KEY,
    Nome_Vacina  VARCHAR(40),
    dataApli     DATE,
    Dt_Prox_Dose DATE,
    Animal_ID    INT(11),
    FOREIGN KEY (Animal_ID) REFERENCES animal (Animal_ID)
);

-- Regra de negócio: toda consulta tem exatamente um animal e um veterinário.
CREATE TABLE consulta (
    ConsultaID INT(11)       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data_hora  DATETIME,
    sintomas   VARCHAR(255),
    valor      DECIMAL(10,2),
    Animal_ID  INT(11)       NOT NULL,
    Vet_CPF    VARCHAR(11)   NOT NULL,
    FOREIGN KEY (Animal_ID) REFERENCES animal (Animal_ID),
    FOREIGN KEY (Vet_CPF)   REFERENCES veterinario (CPF)
);

-- Regra de negócio: todo funcionário está vinculado a uma empresa/filial.
CREATE TABLE funcionario (
    Func_ID       INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nome_Completo VARCHAR(80),
    CPF           CHAR(11)      UNIQUE,
    Cargo         VARCHAR(40),
    Salario       DECIMAL(10,2),
    Empresa_ID    INT           NOT NULL,
    FOREIGN KEY (Empresa_ID) REFERENCES empresa (Empresa_ID)
);

-- Consulta (1:1) Pagamento: o UNIQUE impede dois pagamentos para a mesma consulta.
CREATE TABLE pagamento (
    Pagamento_ID    INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Forma_Pagamento ENUM('Pix', 'Cartao', 'Dinheiro', 'Boleto'),
    Valor           DECIMAL(10,2),
    Descricao       VARCHAR(255),
    Data_Pagamento  DATE,
    ConsultaID      INT(11)       NOT NULL UNIQUE,
    FOREIGN KEY (ConsultaID) REFERENCES consulta (ConsultaID)
);

CREATE TABLE medicamento (
    MedicamentoID INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Nome          VARCHAR(100),
    Fabricante    VARCHAR(80),
    Qntd_Estoque  INT,
    Preco         DECIMAL(10,2)
);

-- Regra de negócio: cada receita tem exatamente uma consulta e um medicamento.
CREATE TABLE receita (
    Receita_ID     INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Dosagem        VARCHAR(100),
    Frequencia     VARCHAR(100),
    ConsultaID     INT(11)      NOT NULL,
    Medicamento_ID INT          NOT NULL,
    FOREIGN KEY (ConsultaID)     REFERENCES consulta (ConsultaID),
    FOREIGN KEY (Medicamento_ID) REFERENCES medicamento (MedicamentoID)
);

CREATE TABLE exame (
    Exame_ID   INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tipo_exame VARCHAR(50),
    Resultado  VARCHAR(50),
    data_Exame DATE,
    ConsultaID INT(11),
    FOREIGN KEY (ConsultaID) REFERENCES consulta (ConsultaID)
);
