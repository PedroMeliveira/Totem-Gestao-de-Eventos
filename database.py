import sqlite3

conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clientes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        CPF TEXT NOT NULL,
        Data_Nasc TEXT NOT NULL,
        Email TEXT NOT NULL,
        Senha BLOB NOT NULL
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Admins (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        CPF TEXT NOT NULL,
        Data_Nasc TEXT NOT NULL,
        Email TEXT NOT NULL,
        Senha BLOB NOT NULL
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Eventos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Horario TEXT NOT NULL,
        Data TEXT NOT NULL,
        Qnt_Ingressos INTEGER NOT NULL,
        Descricao TEXT NOT NULL,
        Imagem TEXT NOT NULL,
        Local TEXT NOT NULL
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ingressos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_ID INTEGER,
        Evento_ID INTEGER NOT NULL,
        Valor FLOAT NOT NULL,
        FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID),
        FOREIGN KEY (Evento_ID) REFERENCES Eventos(ID)
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alimentos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Preco FLOAT NOT NULL,
        Categoria TEXT NOT NULL,
        Imagem TEXT NOT NULL,
        Descricao TEXT NOT NULL
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Carrinhos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_ID INTEGER NOT NULL,
        FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID)
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alimento_no_Carrinho (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Carrinho_ID INTEGER NOT NULL,
        Alimento_ID INTEGER NOT NULL,
        FOREIGN KEY (Carrinho_ID) REFERENCES Carrinhos(ID),
        FOREIGN KEY (Alimento_ID) REFERENCES Alimentos(ID)
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ingresso_no_Carrinho (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Carrinho_ID INTEGER NOT NULL,
        Ingresso_ID INTEGER NOT NULL,
        FOREIGN KEY (Carrinho_ID) REFERENCES Carrinhos(ID),
        FOREIGN KEY (Ingresso_ID) REFERENCES Ingressos(ID)
        )
''')