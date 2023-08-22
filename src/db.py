import sqlite3

connection = sqlite3.Connection('grades.db')
cursor = sqlite3.Cursor(connection)

cursor.execute('CREATE TABLE IF NOT EXISTS Grades (course TEXT PRIMARY KEY, grade REAL, factor REAL)')
connection.commit()

def select(course=None):
    stmt = 'SELECT * FROM Grades WHERE course = ?' if course else 'SELECT * FROM Grades ORDER BY course'
    bind = (course,) if course else ()
    cursor.execute(stmt, bind)
    return cursor.fetchone() if course else cursor.fetchall()

def insert(course, grade, factor):
    cursor.execute('INSERT INTO Grades VALUES(?, ?, ?)', (course, grade, factor))
    connection.commit()

def update(grade, factor, course):
    cursor.execute('UPDATE Grades SET grade = ?, factor = ? WHERE course = ?', (grade, factor, course))
    connection.commit()

def delete(course):
    cursor.execute('DELETE FROM Grades WHERE course = ?', (course,))
    connection.commit()

def avg() -> float:
    cursor.execute('SELECT SUM(Grade*factor)/SUM(factor) FROM Grades')
    return cursor.fetchone()[0]

def credits() -> float:
    cursor.execute('SELECT SUM(factor) FROM Grades')
    return cursor.fetchone()[0]