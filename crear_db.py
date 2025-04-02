import sqlite3

# Crear/conectar base de datos
conn = sqlite3.connect('competencia.db')
c = conn.cursor()

# Crear tabla
c.execute('''CREATE TABLE IF NOT EXISTS submissions 
            (equipo TEXT, 
             BKS REAL, 
             timestamp DATETIME, 
             codigo TEXT, 
             archivo_solucion BLOB)''')

# Insertar algunos datos de ejemplo
datos_ejemplo = [
    ('Equipo A', 15.5, '2024-03-20 10:00:00', 'print("Hola")', None),
    ('Equipo B', 16.2, '2024-03-20 11:00:00', 'print("Mundo")', None)
]

c.executemany('''INSERT INTO submissions 
                 (equipo, BKS, timestamp, codigo, archivo_solucion) 
                 VALUES (?, ?, ?, ?, ?)''', datos_ejemplo)

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos creada exitosamente!") 