import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()  # Chame o método create_tables na inicialização

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT,
                            email TEXT,
                            telefone TEXT,
                            cpf TEXT,
                            rg TEXT,
                            tipo_contratacao TEXT,
                            salario REAL,
                            passagens_diarias INTEGER,
                            ativo INTEGER DEFAULT 1
                            )''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS historico_emprego (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            funcionario_id INTEGER,
                            nome_empresa TEXT,
                            cargo TEXT,
                            salario REAL,
                            FOREIGN KEY(funcionario_id) REFERENCES funcionarios(id)
                            )''')

        self.conn.commit()

    def close_connection(self):
        self.conn.close()

db_manager = DatabaseManager('rh_database.db')
db_manager.create_tables()
