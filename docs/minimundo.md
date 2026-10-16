# Minimundo — Zoolife

Descrição do universo do discurso · versão 2 · 12 tabelas

## 1. Visão geral do sistema

A Zoolife é uma rede de clínicas veterinárias com uma unidade matriz e diversas filiais espalhadas pela cidade. O sistema informatiza o atendimento clínico completo dos animais de estimação, cobrindo desde o cadastro de clientes e seus animais até o registro de consultas, exames, receitas médicas, vacinações e pagamentos.

Na versão atual, o sistema também gerencia as empresas/filiais da rede, os funcionários de cada unidade e os veterinários vinculados a cada clínica, permitindo um controle integrado de toda a operação da rede.

## 2. Entidades do sistema

### 2.1 Empresa
A empresa representa cada clínica ou filial da rede Zoolife. Cada unidade é identificada por um código único (`Empresa_ID`) e possui CNPJ único, nome, e-mail, telefone e endereço. A empresa é a entidade central que conecta veterinários e funcionários às suas respectivas unidades de trabalho.

### 2.2 Cliente
O cliente é o tutor (dono) do animal. É identificado pelo CPF e cadastrado com nome completo, endereço (descrição e CEP) e e-mail. Um cliente pode ter um ou mais números de celular cadastrados separadamente. Um cliente pode possuir um ou mais animais.

### 2.3 Veterinário
O veterinário é o profissional habilitado a realizar consultas. É identificado pelo CPF e possui código interno (`Vet_ID`), nome, número de registro no CRMV e especialidade. Cada veterinário está obrigatoriamente vinculado a uma empresa/filial da rede. Pode ter um ou mais telefones cadastrados.

### 2.4 Funcionário
O funcionário representa a equipe de apoio da clínica (recepcionistas, auxiliares de limpeza, enfermeiros veterinários, gerentes, seguranças etc.). Cada funcionário possui CPF único, nome completo, cargo e salário, e está vinculado a uma empresa/filial. Veterinários e funcionários são entidades distintas no sistema.

### 2.5 Animal
O animal é o paciente da clínica. Deve estar obrigatoriamente vinculado a um cliente (seu dono). Armazena nome, espécie, raça, sexo (F ou M) e se possui microchip implantado. Um cliente pode ter vários animais cadastrados.

### 2.6 Consulta
A consulta registra um atendimento clínico: envolve exatamente um animal e é conduzida por exatamente um veterinário. Armazena data/hora, descrição dos sintomas e valor cobrado. A consulta é a entidade central do atendimento: dela derivam exames, receitas e pagamentos.

### 2.7 Exame
O exame registra um procedimento diagnóstico vinculado a uma consulta. Armazena o tipo do exame (ex.: Hemograma, Raio-X, Eletrocardiograma), o resultado obtido e a data de realização. Uma consulta pode gerar vários exames.

### 2.8 Receita
A receita é a prescrição médica emitida durante uma consulta. Registra a dosagem e a frequência de uso de um medicamento específico. Uma consulta pode gerar várias receitas, cada uma referenciando um medicamento do estoque.

### 2.9 Medicamento
O medicamento representa um item do estoque da clínica. Armazena nome, fabricante, quantidade disponível e preço unitário. Um medicamento pode aparecer em várias receitas ao longo do tempo.

### 2.10 Pagamento
O pagamento registra a quitação financeira de uma consulta. Armazena a forma de pagamento (Pix, Cartão, Dinheiro ou Boleto), o valor pago, uma descrição e a data do pagamento. Cada consulta possui um registro de pagamento associado.

### 2.11 Vacinação
O registro de vacinação documenta a aplicação de uma vacina em um animal. Armazena o nome da vacina, a data de aplicação e a data prevista para a próxima dose. Um animal pode ter vários registros de vacinação ao longo do tempo.

### 2.12 Telefone e Telefone_Vet
Tabelas auxiliares que armazenam os números de celular de clientes e veterinários, respectivamente. Existem como entidades separadas porque tanto clientes quanto veterinários podem ter mais de um número de contato cadastrado.

## 3. Regras de negócio

- Cada cliente é identificado de forma única pelo CPF: não são permitidos dois clientes com o mesmo CPF.
- Cada veterinário é identificado de forma única pelo CPF: não são permitidos dois veterinários com o mesmo CPF.
- Cada funcionário possui CPF único: não são permitidos dois funcionários com o mesmo CPF.
- Cada empresa possui CNPJ único: não são permitidas duas empresas com o mesmo CNPJ.
- Todo veterinário deve estar obrigatoriamente vinculado a uma empresa/filial.
- Todo funcionário deve estar obrigatoriamente vinculado a uma empresa/filial.
- Um cliente pode ter um ou mais telefones de contato cadastrados.
- Um veterinário pode ter um ou mais telefones de contato cadastrados.
- Um cliente pode possuir nenhum, um ou vários animais cadastrados.
- Todo animal deve estar obrigatoriamente vinculado a um cliente (dono).
- Toda consulta deve estar associada a exatamente um animal e a exatamente um veterinário.
- Um animal pode ter zero ou várias consultas ao longo do tempo.
- Um veterinário pode realizar zero ou várias consultas.
- Uma consulta pode gerar zero ou vários exames.
- Uma consulta pode gerar zero ou várias receitas.
- Cada receita está vinculada a exatamente um medicamento e a exatamente uma consulta.
- Cada pagamento está vinculado a exatamente uma consulta, e cada consulta tem no máximo um pagamento.
- Um animal pode ter zero ou vários registros de vacinação.
- O campo MicroChip aceita apenas `'Sim'` ou `'Nao'`.
- O campo Sexo do animal aceita apenas `'F'` (Feminino) ou `'M'` (Masculino).
- `Forma_Pagamento` aceita apenas os valores `'Pix'`, `'Cartao'`, `'Dinheiro'` ou `'Boleto'`.
- Valores monetários (salário, preço, valor da consulta) são armazenados com duas casas decimais.

## 4. Resumo dos relacionamentos

| Relacionamento | Cardinalidade | Significado |
|---|---|---|
| Empresa → veterinario | 1:N | Uma empresa/filial pode ter vários veterinários vinculados. |
| Empresa → funcionario | 1:N | Uma empresa/filial pode ter vários funcionários. |
| Cliente → telefone | 1:N | Um cliente pode ter vários telefones cadastrados. |
| Cliente → animal | 1:N | Um cliente pode ser dono de vários animais. |
| veterinario → telefone_vet | 1:N | Um veterinário pode ter vários telefones cadastrados. |
| veterinario → consulta | 1:N | Um veterinário pode realizar várias consultas. |
| animal → consulta | 1:N | Um animal pode ter várias consultas ao longo do tempo. |
| animal → vacinacao | 1:N | Um animal pode ter vários registros de vacinação. |
| consulta → exame | 1:N | Uma consulta pode gerar vários exames. |
| consulta → receita | 1:N | Uma consulta pode gerar várias receitas. |
| consulta → pagamento | 1:1 | Cada consulta possui um pagamento associado. |
| medicamento → receita | 1:N | Um medicamento pode ser prescrito em várias receitas. |
