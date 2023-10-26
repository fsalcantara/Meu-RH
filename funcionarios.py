from database import db_manager


class Funcionario:
    def __init__(self, id_funcionario, nome, email, telefone, documento, rg, tipo_contratacao, salario, passagens_diarias):
        self.id = id_funcionario
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.documento = documento
        self.rg = rg
        self.tipo_contratacao = tipo_contratacao
        self.salario = salario
        self.passagens_diarias = passagens_diarias
        self.ativo = True
        pass


    def cadastrar_funcionario(self):
        query = '''INSERT INTO funcionarios (nome, email, telefone, cpf, rg, tipo_contratacao, 
        salario, passagens_diarias)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        values = (self.nome, self.email, self.telefone, self.documento, self.rg, self.tipo_contratacao, self.salario,
                  self.passagens_diarias)

        db_manager.cur.execute(query, values)
        db_manager.conn.commit()

    def obter_ultimo_id_inserido(self):
        db_manager.cur.execute("SELECT last_insert_rowid()")
        return db_manager.cur.fetchone()[0]

    def cadastrar_historico_emprego(self, nome_empresa, cargo, salario):
        query = '''INSERT INTO historico_emprego (funcionario_id, nome_empresa, cargo, salario)
                   VALUES (?, ?, ?, ?)'''
        funcionario_id = self.obter_ultimo_id_inserido()
        values = (funcionario_id, nome_empresa, cargo, salario)

        db_manager.cur.execute(query, values)
        db_manager.conn.commit()

    @staticmethod
    def listar_funcionarios(ativos=True):
        if ativos:
            db_manager.cur.execute('''SELECT * FROM funcionarios WHERE ativo=1''')
        else:
            db_manager.cur.execute('''SELECT * FROM funcionarios WHERE ativo=0''')
        return db_manager.cur.fetchall()

    @staticmethod
    def buscar_funcionario_por_id(id_funcionario):
        db_manager.cur.execute("SELECT * FROM funcionarios WHERE id=?", (id_funcionario,))
        resultado = db_manager.cur.fetchone()
        if resultado:
            id_funcionario, nome, email, telefone, documento, rg, tipo_contratacao, salario, passagens_diarias, ativo = resultado
            funcionario = Funcionario(id_funcionario, nome, email, telefone, documento, rg, tipo_contratacao, salario, passagens_diarias)

            return funcionario
        else:
            return None

    def desativar_funcionario(self):
        db_manager.cur.execute('''UPDATE funcionarios SET ativo=0 WHERE id=?''', (self.id,))
        db_manager.conn.commit()

    def ativar_funcionario(self):
        # Verifica se o funcionário tem um ID válido antes de ativar
        if self.id is not None:
            print(self.id)
            # Atualize o status ativo do funcionário no banco de dados usando o ID
            db_manager.cur.execute('''UPDATE funcionarios SET ativo=1 WHERE id=?''', (self.id,))
            db_manager.conn.commit()
            print(f"Funcionário {self.nome} ativado com sucesso!")
        else:
            print("Erro: Funcionário não tem um ID válido.")

    def calcular_salario(self):
        if self.tipo_contratacao == 'CLT':
            salario_liquido = self.salario - self.calcular_impostos() + self.calcular_beneficios()
        elif self.tipo_contratacao == 'PJ':
            taxa_por_hora = self.salario  # A variável 'salario' representa a taxa por hora para PJ
            horas_trabalhadas = 160  # Número de horas trabalhadas por mês
            salario_liquido = taxa_por_hora * horas_trabalhadas

        return salario_liquido

    def calcular_impostos(self):
        # Lógica para calcular impostos
        if self.tipo_contratacao == 'CLT':
            return 0.2 * self.salario  # 20% do salário base (em reais)
        else:
            return 0  # Empresa não paga imposto para PJ

    def adicionar_historico_emprego(self, nome_empresa, cargo, salario):
        query = '''INSERT INTO historico_emprego (funcionario_id, nome_empresa, cargo, salario)
                   VALUES (?, ?, ?, ?)'''
        values = (self.id, nome_empresa, cargo, salario)

        db_manager.cur.execute(query, values)
        db_manager.conn.commit()

    def calcular_beneficios(self):
        if self.tipo_contratacao == 'CLT':
            vale_transporte = self.passagens_diarias * 2 * 4
            vale_alimentacao = 300
            vale_refeicao = 250

            return vale_alimentacao + vale_refeicao + vale_transporte
        else:
            return 0  # Não há benefícios para PJ

    def calcular_contracheque(self, salario, passagens_diarias):
        salario_base = salario
        beneficio_passagens = passagens_diarias * 2  # Valor total das passagens (ida e volta)
        salario_total = salario_base + beneficio_passagens

        # desconto de 20%
        desconto_impostos = salario_total * 0.2

        contracheque = salario_total - desconto_impostos

        return contracheque

    def gerar_contracheque(self, salario, passagens_diarias):
        salario_liquido = self.calcular_contracheque(salario, passagens_diarias)
        beneficios = self.calcular_beneficios()  # Calcular benefícios com base nos atributos do próprio objeto

        contracheque = f"Contracheque para {self.nome}:\n"
        contracheque += f"Salário Líquido: R$ {salario_liquido:.2f}\n"
        contracheque += f"Impostos: R$ {salario_liquido * 0.2:.2f}\n"  # Supondo 20% de impostos
        contracheque += f"Benefícios: R$ {beneficios:.2f}\n"  # Adicionando o valor dos benefícios
        contracheque += f"Salário Bruto: R$ {(salario_liquido + salario_liquido * 0.2 + beneficios):.2f}\n"

        return contracheque
