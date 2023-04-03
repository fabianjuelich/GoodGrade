import os
import sqlite3

connection = sqlite3.Connection(os.path.join(os.path.dirname(__file__), 'gg.db'))
cursor = sqlite3.Cursor(connection)

cursor.execute('CREATE TABLE IF NOT EXISTS Grades (Modul TEXT PRIMARY KEY, Grade REAL, CP REAL)')
connection.commit()

def select(module=None):
    stmt = 'SELECT * FROM Grades WHERE Module = ?' if module else 'SELECT * FROM Grades'
    bind = (module,) if module else ()
    cursor.execute(stmt, bind)
    return cursor.fetchone() if module else cursor.fetchall()

def insert(module, grade, cp):
    cursor.execute('INSERT INTO Grades VALUES(?, ?, ?)', (module, grade, cp))
    connection.commit()

def avg() -> float:
    cursor.execute('SELECT SUM(Grade*CP)/SUM(CP) FROM Grades')
    return cursor.fetchone()[0]
