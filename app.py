importar streamlit como st
importar sqlite3
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Centro de soporte", layout="wide")

conn = sqlite3.connect("support_hub.db", check_same_thread=False)
c = conn.cursor()

# -----------------------------
# DB
# -----------------------------
c.execute("""
CREAR TABLA SI NO EXISTE tickets (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tipo TEXTO,
TEXTO de prioridad,
tipología TEXTO,
descripción TEXTO,
solución TEXTO,
número_de_ticket TEXTO,
producto TEXTO,
fecha TEXTO
)
""")
conn.commit()

# -----------------------------
# UI
# -----------------------------
st.title("🚀 Centro de soporte")
st.caption("Plataforma corporativa de gestión de tickets")

# -----------------------------
# ID DEL TICKET
# -----------------------------
def generar_ticket_id(last_id):
return f"SH-{str(last_id + 1).zfill(4)}"

# -----------------------------
# FORMA
# -----------------------------
st.subheader("📌 Nuevo Boleto")

c.execute("SELECT COUNT(*) FROM tickets")
contador = c.fetchone()[0]

con st.form("ticket_form"):
col1, col2 = st.columns(2)

tipo = col1.selectbox("Tipo de solicitud", ["Incidencia", "Requerimiento"])
prioridad = col2.selectbox("Prioridad", ["Alta", "Normal", "Baja"])

tipologia = st.selectbox("Tipología", ["Iniciar sesión", "API", "Red", "Sistema", "Otro"])

descripcion = st.text_area("Descripcion")
solucion = st.text_area("Solución")

producto = st.selectbox("Producto / Plataforma", ["Genesys", "CRM", "Telefonía", "Otro"])

enviar = st.form_submit_button("Crear ticket")

si enviar:
ticket_id = generar_ticket_id(count)

c.execute("""
INSERT INTO tickets (tipo, prioridad, tipologia, descripcion, solucion, ticket_num, producto, fecha)
VALORES (?, ?, ?, ?, ?, ?, ?, ?)
""", (tipo, prioridad, tipologia, descripcion, solucion, ticket_id, producto, str(datetime.now())))

conn.commit()

st.success(f"Ticket creado: {ticket_id}")

st.rerun()

# -----------------------------
# PANEL
# -----------------------------
st.divider()
st.subheader("📊 Boletos")

c.execute("SELECT * FROM tickets ORDER BY id DESC")
filas = c.fetchall()

si hay filas:
st.metric("Total Tickets", len(rows))

para r en filas:
con st.expander(f"{r[6]} - {r[1]} ({r[2]})"):
st.write("Tipo:", r[1])
st.write("Prioridad:", r[2])
st.write("Tipología:", r[3])
st.write("Descripción:", r[4])
st.write("Solución:", r[5])
st.write("Producto:", r[7])
st.write("Fecha:", r[8])
demás:
st.info ("Todavía no hay entradas.")
