from colorama import Fore, Style
from funcionarios import Funcionario
from database import db_manager
import re


def menu():
    print("1. Cadastrar Funcionário")
    print("2. Listar Funcionários Ativos")
    print("3. Listar Funcionários Inativos")
    print("4. Ativar Funcionário")
    print("5. Desativar Funcionário")
    print("6. Obter Contracheque de um Funcionário")
    print("7. Adicionar Histórico de Emprego")
    print("8. Sair")
    return input("Escolha uma opção: ")


def imprimir_mensagem(mensagem, aceito=True):
    if aceito:
        cor = Fore.GREEN
    else:
        cor = Fore.RED

    print(cor + mensagem + Style.RESET_ALL)


def remover_caracteres_especiais(documento):
    # Remove espaços, pontos e traços do documento
    return re.sub(r'[ .-]', '', documento)


def validar_telefone(telefone):
    # Remove espaços, pontos, traços e parênteses do telefone
    telefone = re.sub(r'[ .\-()]', '', telefone)
    # Verifica se há 11 dígitos (considerando o DDD) e se começa com 9 (para celulares)
    return len(telefone) == 11 and telefone[2] == '9'


def validar_email(email):
    # Expressão regular para validar e-mails
    regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex_email, email) is not None


def validar_cpf(cpf):
    cpf = remover_caracteres_especiais(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    peso = [int(digito) for digito in cpf[:-1]]
    # Verifica o primeiro dígito verificador
    soma = sum(a * b for a, b in zip(peso, range(10, 1, -1)))
    resto = soma % 11
    if resto < 2:
        digito_verif_1 = 0
    else:
        digito_verif_1 = 11 - resto
    # Verifica o segundo dígito verificador
    peso.append(digito_verif_1)
    soma = sum(a * b for a, b in zip(peso, range(11, 1, -1)))
    resto = soma % 11
    if resto < 2:
        digito_verif_2 = 0
    else:
        digito_verif_2 = 11 - resto
    # Retorna True se os dígitos verificadores estiverem corretos
    return cpf[-2:] == str(digito_verif_1) + str(digito_verif_2)


def validar_cnpj(cnpj):
    cnpj = remover_caracteres_especiais(cnpj)
    if len(cnpj) != 14:
        return False
    peso_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    peso_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    # Verifica o primeiro dígito verificador
    soma = sum(a * b for a, b in zip(peso_1, map(int, cnpj[:-2])))
    resto = soma % 11
    if resto < 2:
        digito_verif_1 = 0
    else:
        digito_verif_1 = 11 - resto
    # Verifica o segundo dígito verificador
    soma = sum(a * b for a, b in zip(peso_2, map(int, cnpj[:-1])))
    resto = soma % 11
    if resto < 2:
        digito_verif_2 = 0
    else:
        digito_verif_2 = 11 - resto
    # Retorna True se os dígitos verificadores estiverem corretos
    return cnpj[-2:] == str(digito_verif_1) + str(digito_verif_2)


def validar_rg(rg):
    rg = remover_caracteres_especiais(rg)
    # Verifica se há 9 ou 8 dígitos
    return len(rg) == 9 or len(rg) == 8


while True:

    escolha = menu()
    if escolha == '1':
        nome = input("Nome: ")
        email = input("Email: ")
        while not validar_email(email):
            imprimir_mensagem("Email inválido. Por favor, insira um email válido.", aceito=False)
            email = input("Email: ")

        telefone = input("Telefone: ")
        while not validar_telefone(telefone):
            imprimir_mensagem("Telefone inválido. Por favor, insira um telefone válido com DDD e começando com 9.", aceito=False)
            telefone = input("Telefone: ")

        documento = input("CPF ou CNPJ: ")
        documento = re.sub(r'\D', '', documento)  # Remove caracteres não numéricos

        if len(documento) == 11:  # Se tem 11 dígitos, é um CPF
            if not validar_cpf(documento):
                imprimir_mensagem("CPF inválido. Por favor, insira um CPF válido.", aceito=False)
                continue
        elif len(documento) == 14:  # Se tem 14 dígitos, é um CNPJ
            if not validar_cnpj(documento):
                imprimir_mensagem("CNPJ inválido. Por favor, insira um CNPJ válido.", aceito=False)
                continue
        else:
            imprimir_mensagem("Documento inválido. O documento deve ter 11 dígitos para CPF ou 14 dígitos para CNPJ.",
                              aceito=False)
            continue

        rg = input("RG: ")
        if not validar_rg(rg):
            imprimir_mensagem("RG inválido. Por favor, insira um RG válido.", aceito=False)
            continue

        tipo_contratacao = input("Tipo de Contratação (CLT ou PJ): ").upper()
        if tipo_contratacao == 'CLT':
            if len(documento) == 14:  # Verifica se o documento tem o formato correto para CNPJ
                imprimir_mensagem("Não é permitido contratar como CLT utilizando um CNPJ.", aceito=False)
                continue
            elif not validar_cpf(documento):
                imprimir_mensagem("CPF inválido. Por favor, insira um CPF válido.", aceito=False)
                continue
        elif tipo_contratacao == 'PJ':
            if len(documento) != 14 and len(documento):  # Verifica se o documento tem o formato correto para CNPJ
                imprimir_mensagem("CNPJ inválido. Por favor, insira um CNPJ válido.", aceito=False)
                continue

        salario = float(input("Salário: "))
        passagens_diarias = float(input("Valor gasto diariamente em passagens: "))

        # Agora que você tem todos os dados necessários, crie o objeto Funcionario
        funcionario = Funcionario(id, nome, email, telefone, documento, rg, tipo_contratacao, salario,
                                  passagens_diarias)
        funcionario.cadastrar_funcionario()
        imprimir_mensagem(f"Funcionário {nome} cadastrado com sucesso!")

    elif escolha == '2':
        funcionarios = Funcionario.listar_funcionarios(ativos=True)
        if funcionarios:
            for funcionario in funcionarios:
                print(funcionario)
        else:
            imprimir_mensagem("Não existem funcionários ativos cadastrados.", aceito=False)

    elif escolha == '3':
        funcionarios = Funcionario.listar_funcionarios(ativos=False)
        if funcionarios:
            for funcionario in funcionarios:
                print(funcionario)
        else:
            imprimir_mensagem("Não existem funcionários inativos cadastrados.", aceito=False)

    elif escolha == '4':
        id_funcionario = int(input("Digite o ID do funcionário que deseja ativar: "))
        funcionario = Funcionario.buscar_funcionario_por_id(id_funcionario)
        if funcionario:
            funcionario.ativo = True
            funcionario.ativar_funcionario()
            imprimir_mensagem(f"Funcionário {funcionario.nome} ativado com sucesso!")
        else:
            imprimir_mensagem("Funcionário não encontrado.", aceito=False)

    elif escolha == '5':
        id_funcionario = int(input("Digite o ID do funcionário que deseja desativar: "))
        funcionario = Funcionario.buscar_funcionario_por_id(id_funcionario)
        if funcionario:
            funcionario.ativo = False
            funcionario.desativar_funcionario()
            imprimir_mensagem(f"Funcionário {funcionario.nome} desativado com sucesso!")
        else:
            imprimir_mensagem("Funcionário não encontrado.", aceito=False)

    elif escolha == '6':
        id_funcionario = int(input("Digite o ID do funcionário para obter o contracheque: "))
        funcionario = Funcionario.buscar_funcionario_por_id(id_funcionario)
        if funcionario:
            salario = funcionario.salario
            passagens_diarias = funcionario.passagens_diarias
            contracheque = funcionario.gerar_contracheque(salario, passagens_diarias)
            imprimir_mensagem(contracheque)
        else:
            imprimir_mensagem("Funcionário não encontrado.", aceito=False)

    elif escolha == '7':
        id_funcionario = int(input("Digite o ID do funcionário para adicionar histórico de emprego: "))
        funcionario = Funcionario.buscar_funcionario_por_id(id_funcionario)
        if funcionario:
            nome_empresa = input("Nome da Empresa: ")
            cargo = input("Cargo: ")
            salario = float(input("Salário: "))  # Você pode adicionar tratamento de erro aqui

            funcionario.adicionar_historico_emprego(nome_empresa, cargo, salario)
            imprimir_mensagem("Histórico de emprego adicionado com sucesso!")
        else:
            imprimir_mensagem("Funcionário não encontrado.", aceito=False)
        pass

    elif escolha == '8':
        db_manager.close_connection()
        break
