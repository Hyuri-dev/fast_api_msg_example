
import os
from dotenv import load_dotenv
load_dotenv()
import libsql


url = os.getenv("URL")
auth_token = os.getenv("TOKEN")
database = "tutorial"

if not url or not auth_token:
  raise ValueError("Faltan variables de entorno TURSO_DB_URL o TURSO_AUTH_TOKEN")

conn = libsql.connect(database =database,sync_url=url, auth_token=auth_token)
conn.sync()

conn.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT);")
conn.execute("INSERT INTO messages(message) VALUES('hola');")

conn.sync()

print(conn.execute("SELECT * FROM messages").fetchall())


