import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Support Hub", layout="wide")

conn = sqlite3.connect("support_hub.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS incidencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descripcion TEXT,
    solucion TEXT,
    categoria TEXT,
    prioridad TEXT,
    estado TEXT,
    creador TEXT,
    fecha TEXT
)
""")
conn.commit()

st.title("🚀 Support Hub")
st.caption("Gestión de incidencias y base de conocimiento")

with st.expander("➕ Nueva incidencia"):
    with st.form("incidencia"):
        col1, col2 = st.columns(2)
        titulo = col1.text_input("Título del problema")
        categoria = col2.selectbox("Categoría", ["Login", "API", "Red", "Telefonía", "Otro"])
        descripcion = st.text_area("Descripción")
        solucion = st.text_area("Solución")
        col3, col4, col5 = st.columns(3)
        prioridad = col3.selectbox("Prioridad", ["Baja", "Media", "Alta"])
        estado = col4.selectbox("Estado", ["Abierto", "En progreso", "Documentado", "Cerrado"])
        creador = col5.text_input("Creado por")

        if st.form_submit_button("Guardar"):
            c.execute(
                "INSERT INTO incidencias (titulo, descripcion, solucion, categoria, prioridad, estado, creador, fecha) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (titulo, descripcion, solucion, categoria, prioridad, estado, creador, str(datetime.now()))
            )
            conn.commit()
            st.success("Guardado correctamente")

c.execute("SELECT * FROM incidencias ORDER BY id DESC")
rows = c.fetchall()

cols = ["id","titulo","descripcion","solucion","categoria","prioridad","estado","creador","fecha"]
df = pd.DataFrame(rows, columns=cols)

col1, col2, col3 = st.columns(3)
col1.metric("Total", len(df))
col2.metric("Abiertas", len(df[df["estado"] == "Abierto"]))
col3.metric("Documentadas", len(df[df["estado"] == "Documentado"]))

st.divider()
st.subheader("Incidencias")
if not df.empty:
    st.dataframe(df[["titulo","categoria","prioridad","estado","creador","fecha"]], use_container_width=True)

    for _, row in df.iterrows():
        with st.expander(row["titulo"]):
            st.write("Descripción:", row["descripcion"])
            st.write("Solución:", row["solucion"])
            st.write("Categoría:", row["categoria"])
            st.write("Prioridad:", row["prioridad"])
            st.write("Estado:", row["estado"])
            st.write("Creado por:", row["creador"])
            st.write("Fecha:", row["fecha"])
else:
    st.info("No hay incidencias todavía.")
