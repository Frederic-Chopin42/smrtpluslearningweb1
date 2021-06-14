import sqlite3

connection = sqlite3.connect("smrtpluslearning.db")

cursor = connection.cursor()

#cursor.execute('''CREATE TABLE IF NOT EXISTS Todolist (content TEXT)''')
cursor.execute("SELECT * FROM Todolist")

print(cursor.fetchall())

connection.commit()
connection.close()