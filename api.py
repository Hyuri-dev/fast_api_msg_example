from fastapi import FastAPI, Depends, HTTPException, status, Form
from pydantic import BaseModel
import sqlite3
import os
import psycopg2

app = FastAPI()

class Message(BaseModel):
    text: str

def connect_db():
    db = psycopg2.connect("postgresql://example_1ula_user:TS3mlURmO9E3FAnIUWjSugX4nWqwfVKc@dpg-d2tfclnfte5s73a6kbq0-a.oregon-postgres.render.com/example_1ula")
    print("Conectado exitosamente!")
    return db
    

# def get_db():
#     # Establece la conexión a la base de datos
#     db = sqlite3.connect("messages.db")
#     # Crea la tabla si no existe
#     cur = db.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS mensajes (id INTEGER PRIMARY KEY, text TEXT)")
#     db.commit()
#     # Retorna la conexión
#     return db

@app.get("/")
async def root():
    return {"message": "Hello this is API for create Messages"}

@app.get("/all-messages")
async def get_messages():
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM mensajes")
    mensajes = cur.fetchall()
    db.close()
    return [{"id": mensaje[0], "text": mensaje[1]} for mensaje in mensajes]

@app.post("/message")
async def create_message(mensaje: Message):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO mensajes (mensaje_contenido) VALUES (%s) RETURNING mensaje_id", (mensaje.text, ))
    mensaje_id = cursor.fetchone()[0]
    db.commit()
    db.close()
    return {"id": mensaje_id, "text": mensaje.text}

#Endpoint para formularios html ( de prueba )
@app.post("/messages-form")
async def create_message_with_Form(text: str = Form(...)):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO mensajes (mensaje_contenido) VALUES (%s) RETURNING mensaje_id", (text, ))
    mensaje_id = cursor.fetchone()[0]
    db.commit()
    db.close()
    return {"id": mensaje_id, "text": text}

if __name__ == "__main__":
    import uvicorn
    # Se usa 0.0.0.0 para que sea accesible desde el exterior en un servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)





