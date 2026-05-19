import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Support Hub", layout="wide")

conn = sqlite3.connect("support_hub.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    prioridad TEXT,
    tipologia TEXT,
    descripcion TEXT,
    solucion TEXT,
    ticket_num TEXT,
    producto TEXT,
    fecha TEXT
)
""")
conn.commit()

st.title("Support Hub")
st.subheader("Nuevo Ticket")

c.execute("SELECT COUNT(*) FROM tickets")
count = c.fetchone()[0]

def ticket_id():
    return f"SH-{str(count+1).zfill(4)}"

with st.form("f"):
    tipo = st.selectbox("Tipo de solicitud", ["Incidencia", "Requerimiento"])
    prioridad = st.selectbox("Prioridad", ["Alta", "Normal", "Baja"])
    tipologia = st.selectbox("Tipología", ["Login", "API", "Red", "Sistema", "Otro"])
    descripcion = st.text_area("Descripción")
    solucion = st.text_area("Solución")
    producto = st.selectbox("Producto", ["Genesys", "CRM", "Telefonía", "Otro"])

    if st.form_submit_button("Crear"):
        c.execute(
            "INSERT INTO tickets (tipo, prioridad, tipologia, descripcion, solucion, ticket_num, producto, fecha) VALUES (?,?,?,?,?,?,?,?)",
            (tipo, prioridad, tipologia, descripcion, solucion, ticket_id(), producto, str(datetime.now()))
        )
        conn.commit()
        st.rerun()

st.divider()
st.subheader("Tickets")

c.execute("SELECT * FROM tickets ORDER BY id DESC")
for r in c.fetchall():
    with st.expander(f"{r[6]} - {r[1]}"):
        st.write("Prioridad:", r[2])
        st.write("Tipología:", r[3])
        st.write("Descripción:", r[4])
        st.write("Solución:", r[5])
        st.write("Producto:", r[7])
