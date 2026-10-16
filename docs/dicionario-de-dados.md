# Dicionário de dados — Zoolife

Banco de dados `clinica` (MariaDB) · versão 2 · 12 tabelas

## 1. Introdução

Este documento descreve a estrutura completa do banco de dados do sistema Zoolife na versão 2, que passou de 7 para 12 tabelas. Foram adicionadas as entidades Empresa, Funcionario, Pagamento, Medicamento, Receita e Exame, expandindo o sistema para cobrir a gestão de filiais, funcionários, pagamentos e prontuário clínico completo.

Os nomes das tabelas estão em minúsculas, exatamente como no script [`01_schema.sql`](../sql/01_schema.sql). No MariaDB em Linux, `Consulta` e `consulta` são tabelas diferentes.

## 2. Legenda

| Símbolo | Significado |
|---|---|
| **PK** | Chave primária: identifica unicamente cada registro da tabela |
| **FK** | Chave estrangeira: referencia a chave primária de outra tabela |
| **NOT NULL** | Campo obrigatório: não pode ficar vazio |
| **AI** | AUTO_INCREMENT: valor gerado automaticamente pelo banco |
| **UNIQUE** | Valor único: não pode se repetir, mas pode ser nulo |

## 3. Tabelas

### empresa

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Empresa_ID | INT | PK, NOT NULL, AI | Identificador único da empresa/filial |
| Nome | VARCHAR(120) | — | Nome da clínica ou filial |
| CNPJ | VARCHAR(14) | UNIQUE | CNPJ da empresa; não pode se repetir |
| email | VARCHAR(100) | — | E-mail de contato da empresa |
| telefone | VARCHAR(15) | — | Telefone de contato da empresa |
| endereco | VARCHAR(120) | — | Endereço completo da empresa |

### cliente

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| CPF | VARCHAR(11) | PK, NOT NULL | CPF do cliente; identificador único |
| Nome_Ani | VARCHAR(40) | — | Nome do animal do cliente |
| email | VARCHAR(40) | — | E-mail de contato do cliente |
| End_DESC | VARCHAR(255) | — | Descrição completa do endereço |
| End_CEP | VARCHAR(40) | — | CEP do endereço |
| Nome_Cli | VARCHAR(80) | — | Nome completo do cliente (dono do animal) |

### veterinario

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| CPF | VARCHAR(11) | PK, NOT NULL | CPF do veterinário; identificador único |
| Vet_ID | INT(11) | — | Código interno do veterinário na clínica |
| Nome | VARCHAR(60) | — | Nome completo do veterinário |
| CRMV | INT(20) | — | Número de registro no Conselho Regional de Medicina Veterinária |
| Especialidade | VARCHAR(50) | — | Área de especialização (ex.: Cirurgia, Cardiologia) |
| Empresa_ID | INT | FK → empresa, NOT NULL | Clínica/filial à qual o veterinário está vinculado |

### telefone

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Tel_ID | INT(20) | PK, NOT NULL, AI | Identificador único do telefone do cliente |
| NumeroCEL | VARCHAR(15) | — | Número do celular do cliente |
| Cli_CPF | VARCHAR(11) | FK → cliente | CPF do cliente ao qual o telefone pertence |

### telefone_vet

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Tel_ID | INT(11) | PK, NOT NULL, AI | Identificador único do telefone do veterinário |
| Num_Cel | VARCHAR(15) | — | Número do celular do veterinário |
| Vet_CPF | VARCHAR(11) | FK → veterinario | CPF do veterinário ao qual o telefone pertence |

### animal

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Animal_ID | INT(11) | PK, NOT NULL, AI | Identificador único do animal |
| Nome | VARCHAR(70) | — | Nome do animal |
| Especie | VARCHAR(40) | — | Espécie do animal (ex.: Cachorro, Gato) |
| Raca | VARCHAR(40) | — | Raça do animal |
| MicroChip | ENUM | `'Sim'` / `'Nao'` | Indica se o animal possui microchip de identificação |
| Sexo | ENUM | `'F'` / `'M'` | Sexo do animal (Feminino ou Masculino) |
| Dono_CPF | VARCHAR(11) | FK → cliente, NOT NULL | CPF do cliente dono do animal |

### vacinacao

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| VacinaID | INT(11) | PK, NOT NULL | Identificador único do registro de vacinação |
| Nome_Vacina | VARCHAR(40) | — | Nome da vacina aplicada |
| dataApli | DATE | — | Data em que a vacina foi aplicada |
| Dt_Prox_Dose | DATE | — | Data prevista para a próxima dose |
| Animal_ID | INT(11) | FK → animal | Animal que recebeu a vacinação |

### consulta

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| ConsultaID | INT(11) | PK, NOT NULL, AI | Identificador único da consulta |
| data_hora | DATETIME | — | Data e hora em que a consulta foi realizada |
| sintomas | VARCHAR(255) | — | Descrição dos sintomas apresentados pelo animal |
| valor | DECIMAL(10,2) | — | Valor cobrado pela consulta (R$) |
| Animal_ID | INT(11) | FK → animal, NOT NULL | Animal atendido na consulta |
| Vet_CPF | VARCHAR(11) | FK → veterinario, NOT NULL | Veterinário responsável pela consulta |

### funcionario

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Func_ID | INT | PK, NOT NULL, AI | Identificador único do funcionário |
| Nome_Completo | VARCHAR(80) | — | Nome completo do funcionário |
| CPF | CHAR(11) | UNIQUE | CPF do funcionário; não pode se repetir |
| Cargo | VARCHAR(40) | — | Cargo ocupado (ex.: Recepcionista, Gerente) |
| Salario | DECIMAL(10,2) | — | Salário mensal do funcionário (R$) |
| Empresa_ID | INT | FK → empresa, NOT NULL | Empresa/filial onde o funcionário trabalha |

### pagamento

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Pagamento_ID | INT | PK, NOT NULL, AI | Identificador único do pagamento |
| Forma_Pagamento | ENUM | `'Pix'` / `'Cartao'` / `'Dinheiro'` / `'Boleto'` | Forma de pagamento utilizada |
| Valor | DECIMAL(10,2) | — | Valor pago pela consulta (R$) |
| Descricao | VARCHAR(255) | — | Descrição do pagamento |
| Data_Pagamento | DATE | — | Data em que o pagamento foi realizado |
| ConsultaID | INT(11) | FK → consulta, NOT NULL, UNIQUE | Consulta à qual o pagamento se refere (no máximo um pagamento por consulta) |

### medicamento

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| MedicamentoID | INT | PK, NOT NULL, AI | Identificador único do medicamento |
| Nome | VARCHAR(100) | — | Nome comercial do medicamento |
| Fabricante | VARCHAR(80) | — | Nome do fabricante/laboratório |
| Qntd_Estoque | INT | — | Quantidade disponível em estoque |
| Preco | DECIMAL(10,2) | — | Preço unitário do medicamento (R$) |

### receita

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Receita_ID | INT | PK, NOT NULL, AI | Identificador único da receita médica |
| Dosagem | VARCHAR(100) | — | Dosagem prescrita (ex.: '1 comprimido') |
| Frequencia | VARCHAR(100) | — | Frequência de administração (ex.: 'De 12 em 12 horas') |
| ConsultaID | INT(11) | FK → consulta, NOT NULL | Consulta que gerou esta receita |
| Medicamento_ID | INT | FK → medicamento, NOT NULL | Medicamento prescrito na receita |

### exame

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| Exame_ID | INT | PK, NOT NULL, AI | Identificador único do exame |
| tipo_exame | VARCHAR(50) | — | Tipo do exame realizado (ex.: Hemograma, Raio-X) |
| Resultado | VARCHAR(50) | — | Resultado do exame |
| data_Exame | DATE | — | Data em que o exame foi realizado |
| ConsultaID | INT(11) | FK → consulta | Consulta à qual o exame pertence |

## 4. Relacionamentos

- **cliente (1:N) telefone**: um cliente pode ter vários telefones.
- **cliente (1:N) animal**: um cliente pode ter vários animais.
- **veterinario (1:N) telefone_vet**: um veterinário pode ter vários telefones.
- **empresa (1:N) veterinario**: vários veterinários pertencem a uma empresa/filial.
- **empresa (1:N) funcionario**: uma empresa pode ter vários funcionários.
- **animal (1:N) vacinacao**: um animal pode ter vários registros de vacinação.
- **animal (1:N) consulta**: um animal pode ter várias consultas.
- **veterinario (1:N) consulta**: um veterinário pode realizar várias consultas.
- **consulta (1:1) pagamento**: cada consulta tem no máximo um pagamento (garantido pelo `UNIQUE` em `pagamento.ConsultaID`).
- **consulta (1:N) receita**: uma consulta pode gerar várias receitas.
- **consulta (1:N) exame**: uma consulta pode ter vários exames associados.
- **medicamento (1:N) receita**: um medicamento pode aparecer em várias receitas.
