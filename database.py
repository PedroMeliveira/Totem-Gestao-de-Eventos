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
        Vagas INTEGER,
        
               
               )
''')