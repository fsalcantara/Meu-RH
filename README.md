# Sistema de Recursos Humanos (RH)

## Introdução

O Sistema de Recursos Humanos (RH) é uma aplicação desenvolvida em Python para gerenciar informações de funcionários, histórico de emprego, folha de pagamento e contracheques. Ele utiliza um banco de dados SQLite para armazenar dados de forma eficiente e segura.

## Funcionalidades

O sistema oferece as seguintes funcionalidades:

1. **Cadastro de Funcionários:**
   - Nome, email, telefone, CPF, RG, tipo de contratação, salário e passagens diárias podem ser cadastrados para cada funcionário.

2. **Gestão de Funcionários:**
   - Ativação e desativação de funcionários.
   - Listagem de funcionários ativos e inativos.

3. **Histórico de Emprego:**
   - Adição de histórico de emprego para cada funcionário, incluindo nome da empresa, cargo e salário.

4. **Folha de Pagamento:**
   - Cálculo de salários, impostos e benefícios para funcionários contratados como CLT ou PJ.

5. **Contracheque:**
   - Geração de contracheques com base no salário líquido, descontos de impostos e benefícios.

## Requisitos

- Python 3.x
- Bibliotecas: `sqlite3`, `colorama`

## Como Usar

1. **Instalação:**
   - Clone o repositório do projeto utilizando o comando:<br> ```git clone https://github.com/fsalcantara/Sistema-de-Recursos-Humanos.git```.
   - Instale as dependências usando:<br> ```py -m pip install colorama```.

2. **Execução:**
   - Execute `python main.py` no diretório que você fez o clone para iniciar o sistema.
   - Siga as instruções no menu para acessar diferentes funcionalidades.

## Estrutura do Código

- `main.py`: Contém o menu principal e a lógica de interação com o usuário.
- `funcionarios.py`: Define a classe `Funcionario` com métodos para gerenciar funcionários, histórico de emprego e folha de pagamento.
- `database.py`: Gerencia a conexão e operações no banco de dados SQLite.

