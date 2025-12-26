# ==========================================================
# FERRETERÍA IA PRO++ (ARQUITECTURA COMPLETA – NIVEL SAAS)
# Incluye:
# - Arquitectura modular
# - Concreto + acero + ladrillos + pintura
# - Memoria conversacional
# - Exportación (PDF / Excel / WhatsApp-ready)
# ==========================================================

import streamlit as st
import json
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from groq import Groq
import math
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(
    page_title="Ferretería IA Pro++",
    page_icon="🏗️",
    layout="centered"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "memoria" not in st.session_state:
    st.session_state.memoria = {}

# ==========================================================
# MODELO DE DATOS
# ==========================================================
@dataclass
class ProyectoObra:
    largo: Optional[float] = None
    ancho: Optional[float] = None
    alto: Optional[float] = None
    espesor_cm: Optional[float] = None
    uso: Optional[str] = None
    tipo_obra: Optional[str] = None  # losa, muro, pintura

# ==========================================================
# EXTRACCIÓN IA
# ==========================================================
def extraer_datos_ia(texto: str) -> Dict:
    prompt = f"""
    Eres un analista técnico de construcción.
    Extrae SOLO los datos explícitos del texto.
    Devuelve JSON con posibles claves:
    largo, ancho, alto, espesor_cm, uso, tipo_obra.
    Si un dato no está, usa null.

    Texto: "{texto}"
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

# ==========================================================
# CÁLCULOS
# ==========================================================
def calcular_concreto(p: ProyectoObra) -> Dict:
    volumen = p.largo * p.ancho * (p.espesor_cm / 100)
    sacos_m3 = {"ligero": 6.5, "estructural": 8, "industrial": 9.5}.get(p.uso, 6.5)
    desperdicio = 1.07
    sacos = math.ceil(volumen * sacos_m3 * desperdicio)
    return {
        "volumen_m3": round(volumen, 2),
        "cemento_sacos": sacos,
        "arena_m3": round(volumen * 0.55 * desperdicio, 2),
        "grava_m3": round(volumen * 0.75 * desperdicio, 2)
    }


def calcular_acero(volumen_m3: float) -> Dict:
    kg_por_m3 = 120  # losa estándar
    total_kg = volumen_m3 * kg_por_m3
    return {"acero_kg": round(total_kg, 1)}


def calcular_ladrillos(p: ProyectoObra) -> Dict:
    area = p.largo * p.alto
    ladrillos_m2 = 50
    return {"ladrillos": math.ceil(area * ladrillos_m2 * 1.05)}


def calcular_pintura(p: ProyectoObra) -> Dict:
    area = p.largo * p.alto
    rendimiento = 10  # m2 por litro
    return {"pintura_litros": math.ceil((area / rendimiento) * 2)}

# ==========================================================
# EXPORTADORES
# ==========================================================
def exportar_pdf(datos: Dict, filename="presupuesto.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = [Paragraph("Presupuesto Técnico", styles['Title'])]
    for k, v in datos.items():
        story.append(Paragraph(f"{k}: {v}", styles['Normal']))
    doc.build(story)


# ==========================================================
# INTERFAZ
# ==========================================================
st.title("🏗️ Ferretería IA Pro++")
st.markdown("Asistente técnico integral de obra – nivel profesional")

entrada = st.text_input("Describe tu proyecto")

if entrada:
    nuevos_datos = extraer_datos_ia(entrada)
    st.session_state.memoria.update({k: v for k, v in nuevos_datos.items() if v is not None})

    proyecto = ProyectoObra(**st.session_state.memoria)

    faltantes = [k for k, v in asdict(proyecto).items() if v is None]

    if faltantes:
        st.warning(f"Faltan datos críticos: {', '.join(faltantes)}")
    else:
        resultados = {}

        if proyecto.tipo_obra in ["losa", "concreto"]:
            concreto = calcular_concreto(proyecto)
            acero = calcular_acero(concreto['volumen_m3'])
            resultados.update(concreto)
            resultados.update(acero)

        if proyecto.tipo_obra == "muro":
            resultados.update(calcular_ladrillos(proyecto))

        if proyecto.tipo_obra == "pintura":
            resultados.update(calcular_pintura(proyecto))

        st.success("Presupuesto generado")
        st.json(resultados)

        if st.button("Exportar a Excel"):
            df = pd.DataFrame(resultados.items(), columns=["Concepto", "Cantidad"])
            df.to_excel("presupuesto.xlsx", index=False)
            st.success("Archivo Excel generado")

        if st.button("Exportar PDF"):
            exportar_pdf(resultados)
            st.success("PDF generado")
