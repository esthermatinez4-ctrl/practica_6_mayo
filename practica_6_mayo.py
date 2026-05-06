import sqlite3
import requests
conexion = sqlite3.connect("api_chuck.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chistes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT UNIQUE,
    texto TEXT NOT NULL
)
""")

conexion.commit()

print("\nObteniendo chiste de la API...")
url = "https://api.chucknorris.io/jokes/random"
respuesta = requests.get(url).json()

api_id = respuesta["id"]
texto = respuesta["value"]

print("Chiste obtenido:")
print(texto)

cursor.execute("""
INSERT OR IGNORE INTO chistes (api_id, texto)
VALUES (?, ?)
""", (api_id, texto))

conexion.commit()

print("\nChistes guardados en la base de datos:")
cursor.execute("SELECT id, texto FROM chistes")
filas = cursor.fetchall()

for fila in filas:
    print(f"{fila[0]} → {fila[1]}")

print("\nMODIFICAR UN CHISTE")
id_mod = input("Introduce el ID del chiste que quieres modificar: ")
nuevo_texto = input("Introduce el nuevo texto del chiste: ")

cursor.execute("""
UPDATE chistes
SET texto = ?
WHERE id = ?
""", (nuevo_texto, id_mod))

conexion.commit()

print("\nChiste modificado correctamente.")

print("\nEstado final de la tabla:")
cursor.execute("SELECT id, texto FROM chistes")
for fila in cursor.fetchall():
    print(f"{fila[0]} → {fila[1]}")

conexion.close()
