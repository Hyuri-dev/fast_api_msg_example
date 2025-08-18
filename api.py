from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

class Message(BaseModel):
    text: str

def get_db():
    # Establece la conexión a la base de datos
    db = sqlite3.connect("messages.db")
    # Crea la tabla si no existe
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS mensajes (id INTEGER PRIMARY KEY, text TEXT)")
    db.commit()
    # Retorna la conexión
    return db

@app.get("/")
async def root():
    return {"message": "Hello this is API for create Messages"}

@app.get("/message")
async def get_items():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, text FROM mensajes")
    mensajes = cur.fetchall()
    db.close()
    return [{"id": mensaje[0], "text": mensaje[1]} for mensaje in mensajes]

@app.post("/messages")
async def create_item(mensaje: Message):
    db = get_db()
    cursor = db.cursor()
    # CORRECCIÓN: el nombre de la tabla era 'mensaje' en lugar de 'mensajes'
    cursor.execute("INSERT INTO mensajes (text) VALUES (?)", (mensaje.text, ))
    db.commit()
    mensaje_id = cursor.lastrowid
    db.close()
    return {"id": mensaje_id, "text": mensaje.text}

if __name__ == "__main__":
    import uvicorn
    # Se usa 0.0.0.0 para que sea accesible desde el exterior en un servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)





