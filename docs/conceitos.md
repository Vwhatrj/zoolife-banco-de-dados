# Conceitos do projeto — Zoolife

O que são o dicionário de dados, o minimundo e o DER, para que servem e como se aplicam ao Zoolife.

## Parte 1 — Dicionário de dados

### O que é?
O dicionário de dados é um documento técnico que descreve de forma detalhada e organizada toda a estrutura do banco de dados. Funciona como um "manual de referência": reúne em um só lugar as informações sobre as tabelas e seus campos.

De forma simples, é como um glossário que explica cada "gaveta" (tabela) e cada "compartimento" (campo) do banco: o que guarda, qual o formato, se é obrigatório e como se conecta com outras tabelas.

### Para que serve?
- Documentar o projeto para que qualquer pessoa entenda a estrutura sem precisar abrir o sistema.
- Facilitar a manutenção e a evolução do banco de dados no futuro.
- Comunicar a estrutura técnica do sistema para professores, clientes ou outros desenvolvedores.
- Evitar erros de interpretação sobre o significado de cada campo.
- Servir como base para criar consultas SQL, relatórios e novas funcionalidades.

### O que contém?
Cada entrada descreve um campo de uma tabela com:

- **Campo:** o nome exato da coluna no banco (ex.: `CPF`, `Animal_ID`, `Forma_Pagamento`).
- **Tipo:** o formato do dado: `INT` (número inteiro), `VARCHAR` (texto), `DATE` (data), `DECIMAL` (valor monetário), `ENUM` (lista fixa de opções) etc.
- **Restrições:** as regras do campo: PK, FK, NOT NULL, AUTO_INCREMENT, UNIQUE.
- **Descrição:** explicação em linguagem simples do que aquele campo representa no sistema.

### Como se aplica ao Zoolife?
O [dicionário de dados](dicionario-de-dados.md) do Zoolife documenta as 12 tabelas do banco: cliente, veterinario, telefone, telefone_vet, animal, vacinacao, consulta, empresa, funcionario, pagamento, medicamento, receita e exame.

Por exemplo, na tabela `pagamento`, o campo `Forma_Pagamento` é do tipo `ENUM` e aceita apenas `'Pix'`, `'Cartao'`, `'Dinheiro'` ou `'Boleto'`. Essa restrição está documentada para que qualquer desenvolvedor saiba o que pode ser inserido nesse campo sem precisar inspecionar o banco.

Outro exemplo: o campo `CNPJ` da tabela `empresa` tem a restrição `UNIQUE`, o que garante que nenhuma empresa seja cadastrada duas vezes com o mesmo CNPJ.

## Parte 2 — Minimundo

### O que é?
O minimundo (também chamado de universo do discurso) é um texto em linguagem natural que descreve o contexto real do sistema antes de qualquer diagrama ou tabela. Ele conta a "história" do sistema: quem são os envolvidos, o que fazem e quais regras regem as relações entre eles.

É o ponto de partida de toda a modelagem. A partir dele, identificam-se as entidades, os atributos e os relacionamentos que precisarão existir.

### Para que serve?
- Definir o escopo do sistema: o que ele deve e o que não precisa controlar.
- Identificar as entidades principais (as tabelas que serão criadas).
- Levantar os atributos de cada entidade (os campos das tabelas).
- Estabelecer as regras de negócio, como cardinalidades (1:1, 1:N, N:N).
- Servir como base para o Diagrama Entidade-Relacionamento (DER).
- Justificar as decisões de modelagem para professores e clientes.

### O que contém?
- **Contexto geral:** descrição do negócio ou organização que o sistema vai atender.
- **Entidades:** os "objetos" do mundo real que o sistema precisa conhecer.
- **Atributos:** as características de cada entidade que precisam ser armazenadas.
- **Regras de negócio:** restrições e comportamentos esperados do sistema.
- **Relacionamentos:** como as entidades se conectam e em qual proporção (cardinalidade).

### Como se aplica ao Zoolife?
O [minimundo](minimundo.md) do Zoolife descreve uma rede de clínicas com matriz e filiais. A partir do texto, foram identificadas 12 entidades, suas características e as regras que as conectam, como o fato de que um veterinário deve estar vinculado a uma empresa, ou de que uma consulta pode gerar exames, receitas e um pagamento.

Sem o minimundo, seria difícil justificar por que existem tabelas como `empresa` e `funcionario` separadas de `veterinario`, ou por que `receita` e `exame` são entidades distintas derivadas da consulta.

### Diferença entre minimundo e dicionário de dados
- **Minimundo:** escrito antes da modelagem, em linguagem natural. Responde: "o que o sistema precisa representar?"
- **Dicionário de dados:** produzido depois da modelagem, em linguagem técnica. Responde: "como o banco de dados está estruturado?"

Junto com o DER e o script SQL, esses dois documentos formam a documentação completa do banco de dados do projeto.

## Parte 3 — DER (Diagrama Entidade-Relacionamento)

### O que é?
O DER é uma representação gráfica da estrutura do banco de dados. Ele mostra as entidades do sistema, seus atributos e como elas se relacionam, usando uma notação padronizada com formas geométricas.

### Elementos do DER
- **Retângulo:** representa uma entidade (tabela). Ex.: cliente, animal, consulta.
- **Elipse:** representa um atributo de uma entidade. Ex.: Nome, CPF, Especialidade.
- **Losango:** representa um relacionamento entre entidades. Ex.: "Possui", "Realiza", "Atende".
- **Linhas:** conectam entidades e relacionamentos.
- **1 e N nas linhas:** indicam a cardinalidade.

### Como ler a cardinalidade?
- **1:1 (um para um):** um registro A se relaciona com exatamente um registro B. Ex.: uma consulta tem um pagamento.
- **1:N (um para muitos):** um registro A pode se relacionar com vários registros B. Ex.: um cliente pode ter vários animais.
- **N:N (muitos para muitos):** vários registros A se relacionam com vários registros B; normalmente resolve-se com uma tabela intermediária.

### Como se aplica ao Zoolife?
O DER do Zoolife apresenta 12 entidades ligadas por relacionamentos como "Possui", "Realiza" e "Atende". Por exemplo:

- `empresa` se conecta a `veterinario` pelo relacionamento "Possui", com cardinalidade 1:N: uma empresa possui vários veterinários.
- `consulta` se conecta a `exame`, `receita` e `pagamento`: a consulta é o centro do atendimento clínico.
- `animal` se conecta a `consulta` pelo relacionamento "Atende" e a `vacinacao` pelo relacionamento "Possui".

O DER é produzido depois do minimundo e serve de base para o script SQL que cria as tabelas. O diagrama do modelo está no [README](../README.md#modelo-de-dados).
