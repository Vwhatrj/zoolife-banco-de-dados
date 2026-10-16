-- =============================================================
-- Zoolife — 03_consultas.sql
-- Exemplos de consulta e manipulação de dados.
-- Rode depois de 01_schema.sql e 02_dados_exemplo.sql.
-- O UPDATE e o DELETE do final alteram os dados; para voltar ao
-- estado original, rode 01 e 02 de novo.
-- =============================================================

USE clinica;

-- 1. WHERE + ORDER BY: gatos atendidos pela rede, em ordem alfabética
SELECT Nome, Raca, Sexo
FROM animal
WHERE Especie = 'Gato'
ORDER BY Nome;

-- 2. LIKE: veterinárias (nome começa com "Dra.")
SELECT Nome, Especialidade, CRMV
FROM veterinario
WHERE Nome LIKE 'Dra.%'
ORDER BY Nome;

-- 3. ORDER BY + LIMIT: as 3 consultas mais caras
SELECT ConsultaID, data_hora, sintomas, valor
FROM consulta
ORDER BY valor DESC, data_hora
LIMIT 3;

-- 4. JOIN: agenda de consultas com animal, tutor e veterinário
SELECT c.data_hora,
       a.Nome     AS animal,
       cl.Nome_Cli AS tutor,
       v.Nome     AS veterinario,
       c.valor
FROM consulta c
JOIN animal a       ON a.Animal_ID = c.Animal_ID
JOIN cliente cl     ON cl.CPF      = a.Dono_CPF
JOIN veterinario v  ON v.CPF       = c.Vet_CPF
ORDER BY c.data_hora;

-- 5. Operadores aritméticos: valor parado em estoque por medicamento
SELECT Nome,
       Qntd_Estoque,
       Preco,
       Qntd_Estoque * Preco AS valor_em_estoque
FROM medicamento
ORDER BY valor_em_estoque DESC;

-- 6. Operadores aritméticos: custo anual de cada funcionário (12 salários + 13º)
SELECT Nome_Completo, Cargo, Salario, Salario * 13 AS custo_anual
FROM funcionario
WHERE Salario >= 2500
ORDER BY custo_anual DESC, Nome_Completo;

-- 7. JOIN + agregação: faturamento por filial
SELECT e.Nome              AS filial,
       COUNT(p.Pagamento_ID) AS consultas,
       SUM(p.Valor)          AS faturamento
FROM pagamento p
JOIN consulta c    ON c.ConsultaID = p.ConsultaID
JOIN veterinario v ON v.CPF        = c.Vet_CPF
JOIN empresa e     ON e.Empresa_ID = v.Empresa_ID
GROUP BY e.Empresa_ID, e.Nome
ORDER BY faturamento DESC;

-- 8. LEFT JOIN: filiais que ainda não têm veterinário vinculado
SELECT e.Nome AS filial
FROM empresa e
LEFT JOIN veterinario v ON v.Empresa_ID = e.Empresa_ID
WHERE v.CPF IS NULL
ORDER BY e.Nome;

-- 9. Datas: vacinas com próxima dose já vencida em 30/06/2026
SELECT a.Nome AS animal,
       va.Nome_Vacina,
       va.Dt_Prox_Dose,
       DATEDIFF('2026-06-30', va.Dt_Prox_Dose) AS dias_em_atraso
FROM vacinacao va
JOIN animal a ON a.Animal_ID = va.Animal_ID
WHERE va.Dt_Prox_Dose < '2026-06-30'
ORDER BY va.Dt_Prox_Dose;

-- -------------------------------------------------------------
-- Manipulação de dados
-- -------------------------------------------------------------

-- UPDATE: reajuste de 10% nos medicamentos da fabricante VetFarma
UPDATE medicamento
SET Preco = Preco * 1.10
WHERE Fabricante = 'VetFarma';

SELECT Nome, Fabricante, Preco FROM medicamento WHERE Fabricante = 'VetFarma';

-- DELETE: remove do estoque os medicamentos que nunca foram receitados
DELETE FROM medicamento
WHERE MedicamentoID NOT IN (SELECT Medicamento_ID FROM receita);

SELECT MedicamentoID, Nome FROM medicamento ORDER BY MedicamentoID;
