import sqlite3

conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clientes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
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
        Qnt_Ingressos INTEGER
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ingresso (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_ID INTEGER,
        Evento_ID INTEGER NOT NULL,
        FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID),
        FOREIGN KEY (Evento_ID) REFERENCES Eventos(ID)
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alimentos (
        
               
               
               )


''')