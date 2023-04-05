import os
import sqlite3

connection = sqlite3.Connection(os.path.join(os.path.dirname(__file__), 'grades.db'))
cursor = sqlite3.Cursor(connection)

cursor.execute('CREATE TABLE IF NOT EXISTS Grades (Module TEXT PRIMARY KEY, Grade REAL, CP REAL)')
connection.commit()

def select(module=None):
    stmt = 'SELECT * FROM Grades WHERE Module = ?' if module else 'SELECT * FROM Grades ORDER BY Module'
    bind = (module,) if module else ()
    cursor.execute(stmt, bind)
    return cursor.fetchone() if module else cursor.fetchall()

def insert(module, grade, cp):
    cursor.execute('INSERT INTO Grades VALUES(?, ?, ?)', (module, grade, cp))
    connection.commit()

def delete(module):
    cursor.execute('DELETE FROM Grades WHERE Module = ?', (module,))
    connection.commit()

def avg() -> float:
    cursor.execute('SELECT SUM(Grade*CP)/SUM(CP) FROM Grades')
    return cursor.fetchone()[0]
