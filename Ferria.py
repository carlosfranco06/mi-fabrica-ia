# ==========================================================
# FERRETERÍA IA PRO+++ – PLATAFORMA COMERCIAL COMPLETA (SAAS)
# Incluye:
# - Autenticación y roles
# - Normativas por país
# - Prompts endurecidos
# - WhatsApp Business API (Twilio-ready)
# - Precios dinámicos
# - Base para producto comercial
# ==========================================================

import streamlit as st
import json
import math
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from groq import Groq
import pandas as pd
# PDF opcional: reportlab no viene instalado por defecto en Streamlit Cloud
# Se importa de forma segura para evitar crash
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_OK = True
except ModuleNotFoundError:
    REPORTLAB_OK = False

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(page_title="Ferretería IA Pro+++", page_icon="🏗️", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================================
# AUTENTICACIÓN SIMPLE (ESCALABLE A AUTH0 / FIREBASE)
# ==========================================================
USUARIOS = {
    "admin": {"password": "admin123", "rol": "admin"},
    "vendedor": {"password": "ventas123", "rol": "ventas"},
    "cliente": {"password": "cliente123", "rol": "cliente"}
}

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario is None:
    st.subheader("Ingreso al sistema")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if u in USUARIOS and USUARIOS[u]["password"] == p:
            st.session_state.usuario = {"nombre": u, "rol": USUARIOS[u]["rol"]}
            st.experimental_rerun()
        else:
            st.error("Credenciales inválidas")
    st.stop()

# ==========================================================
# NORMATIVAS POR PAÍS
# ==========================================================
NORMATIVAS = {
    "Argentina": {"acero_kg_m3": 120, "desperdicio": 1.07},
    "Brasil": {"acero_kg_m3": 110, "desperdicio": 1.05},
    "México": {"acero_kg_m3": 125, "desperdicio": 1.08}
}

pais = st.selectbox("País de la obra", list(NORMATIVAS.keys()))

# ==========================================================
# MODELO DE OBRA
# ==========================================================
@dataclass
class Proyecto:
    largo: Optional[float] = None
    ancho: Optional[float] = None
    alto: Optional[float] = None
    espesor_cm: Optional[float] = None
    uso: Optional[str] = None
    tipo_obra: Optional[str] = None

# ==========================================================
# IA – PROMPT ENDURECIDO
# ==========================================================
def extraer_datos_ia(texto: str) -> Dict:
    prompt = f"""
    Eres un ingeniero civil. Extrae solo datos explícitos.
    PROHIBIDO inferir.
    Devuelve JSON con:
    largo, ancho, alto, espesor_cm, uso, tipo_obra.
    Usa null si no aparece.

    Texto: {texto}
    """
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(r.choices[0].message.content)

# ==========================================================
# PRECIOS DINÁMICOS (EDITABLE POR ADMIN)
# ==========================================================
PRECIOS = {
    "cemento_saco": 15,
    "arena_m3": 18,
    "grava_m3": 22,
    "acero_kg": 1.2,
    "ladrillo": 0.6,
    "pintura_litro": 4
}

if st.session_state.usuario["rol"] == "admin":
    st.subheader("Gestión de precios")
    for k in PRECIOS:
        PRECIOS[k] = st.number_input(k, value=float(PRECIOS[k]))

# ==========================================================
# CÁLCULOS
# ==========================================================
def calcular_concreto(p: Proyecto) -> Dict:
    norm = NORMATIVAS[pais]
    vol = p.largo * p.ancho * (p.espesor_cm / 100)
    sacos_m3 = {"ligero": 6.5, "estructural": 8, "industrial": 9.5}.get(p.uso, 6.5)
    sacos = math.ceil(vol * sacos_m3 * norm["desperdicio"])
    arena = vol * 0.55 * norm["desperdicio"]
    grava = vol * 0.75 * norm["desperdicio"]
    acero = vol * norm["acero_kg_m3"]

    costo = (
        sacos * PRECIOS["cemento_saco"] +
        arena * PRECIOS["arena_m3"] +
        grava * PRECIOS["grava_m3"] +
        acero * PRECIOS["acero_kg"]
    )

    return {
        "volumen_m3": round(vol, 2),
        "cemento_sacos": sacos,
        "arena_m3": round(arena, 2),
        "grava_m3": round(grava, 2),
        "acero_kg": round(acero, 1),
        "total_usd": round(costo, 2)
    }

# ==========================================================
# WHATSAPP (PLACEHOLDER REAL)
# ==========================================================
def enviar_whatsapp(mensaje: str):
    # Aquí se integra Twilio / WhatsApp Business API
    pass

# ==========================================================
# UI PRINCIPAL
# ==========================================================
st.title("Ferretería IA Pro+++ – Plataforma Comercial")

entrada = st.text_input("Describe la obra")

if entrada:
    datos = extraer_datos_ia(entrada)
    if "memoria" not in st.session_state:
        st.session_state.memoria = {}
    st.session_state.memoria.update({k: v for k, v in datos.items() if v is not None})

    proyecto = Proyecto(**st.session_state.memoria)
    faltantes = [k for k, v in asdict(proyecto).items() if v is None]

    if faltantes:
        st.warning(f"Faltan datos: {', '.join(faltantes)}")
    else:
        resultado = calcular_concreto(proyecto)
        st.success("Presupuesto generado")
        st.json(resultado)

        if st.button("Enviar por WhatsApp"):
            enviar_whatsapp(str(resultado))

        if st.button("Exportar Excel"):
            pd.DataFrame(resultado.items(), columns=["Concepto", "Valor"]).to_excel("presupuesto.xlsx", index=False)
            st.success("Excel generado")
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
