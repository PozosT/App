import sqlite3

conn = sqlite3.connect('competencia.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='submissions'")
tabla_existe = c.fetchone()

if not tabla_existe:
    c.execute('''CREATE TABLE submissions 
                (equipo TEXT, BKS REAL, timestamp DATETIME, 
                 codigo TEXT, archivo_solucion BLOB)''')
    print("Tabla 'submissions' creada exitosamente.")
else:
    print("La tabla 'submissions' ya existe.")

conn.close() 