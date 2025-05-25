import sqlite3

conn = sqlite3.connect('competencia.db')
c = conn.cursor()

c.execute("SELECT equipo, archivo_solucion FROM submissions WHERE archivo_solucion IS NOT NULL")
resultados = c.fetchall()

for idx, (equipo, archivo_blob) in enumerate(resultados):
    if archivo_blob:
        nombre_archivo = f"{equipo}_{idx}.bin"
        with open(nombre_archivo, "wb") as f:
            f.write(archivo_blob)
        print(f"Archivo guardado: {nombre_archivo}")

conn.close() 