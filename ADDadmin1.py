import sqlite3
import bcrypt

conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()
senha = "123123"
senha_bytes = senha.encode('utf-8')
sal = bcrypt.gensalt()
senha_hash = bcrypt.hashpw(senha_bytes, sal)


cursor.execute("INSERT INTO Admins (Nome, CPF, Data_Nasc, Email, Senha) VALUES (?, ?, ?, ?, ?)",
               ("Admin", "12345678901", "01/01/2000", "admin@admin.com", senha_hash))

conexao.commit()