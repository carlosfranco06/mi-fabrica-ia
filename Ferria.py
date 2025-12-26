import streamlit as st
import json
from typing import Optional, Dict
from dataclasses import dataclass
from groq import Groq

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
st.set_page_config(
    page_title="Ferretería IA Pro+",
    page_icon="🏗️",
    layout="centered"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================================
# MODELOS DE DATOS (FUENTE DE VERDAD)
# ==========================================================
@dataclass
class ProyectoConcreto:
    largo: Optional[float]
    ancho: Optional[float]
    espesor_cm: Optional[float]
    uso: Optional[str]  # ligero / estructural / industrial

# ==========================================================
# EXTRACCIÓN DE DATOS CON IA (ROBUSTA Y CONTROLADA)
# ==========================================================
def extraer_datos_ia(mensaje_usuario: str) -> ProyectoConcreto:
    """
    Extrae dimensiones y tipo de uso SIN inventar valores.
    Si no existen datos claros → null.
    """
    prompt = f"""
    Actúas como un analista técnico de obras civiles.
    Analiza el texto del usuario y extrae:
    - largo (m)
    - ancho (m)
    - espesor_cm (cm)
    - uso (ligero, estructural, industrial)

    Reglas estrictas:
    - NO infieras datos que no estén explícitos.
    - Si un dato no aparece, devuelve null.
    - Responde SOLO en JSON válido.

    Texto: "{mensaje_usuario}"

    Ejemplo:
    {{
      "largo": 6,
      "ancho": 4,
      "espesor_cm": 12,
      "uso": "industrial"
    }}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"}
    )

    data = json.loads(completion.choices[0].message.content)

    return ProyectoConcreto(**data)

# ==========================================================
# VALIDACIONES PROFESIONALES
# ==========================================================
def validar_proyecto(p: ProyectoConcreto) -> list:
    faltantes = []
    if p.largo is None:
        faltantes.append("largo")
    if p.ancho is None:
        faltantes.append("ancho")
    if p.espesor_cm is None:
        faltantes.append("espesor")
    return faltantes

# ==========================================================
# CÁLCULOS AVANZADOS DE CONCRETO
# ==========================================================
def calcular_materiales(p: ProyectoConcreto) -> Dict:
    """
    Fórmulas basadas en práctica real:
    - Dosificación según uso
    - Factor de desperdicio
    """
    volumen = p.largo * p.ancho * (p.espesor_cm / 100)
    desperdicio = 1.07  # 7%

    if p.uso == "industrial":
        sacos_m3 = 9.5
    elif p.uso == "estructural":
        sacos_m3 = 8
    else:
        sacos_m3 = 6.5

    sacos = round(volumen * sacos_m3 * desperdicio)
    arena_m3 = round(volumen * 0.55 * desperdicio, 2)
    grava_m3 = round(volumen * 0.75 * desperdicio, 2)

    precio_saco = 15

    return {
        "volumen_m3": round(volumen, 2),
        "cemento_sacos": sacos,
        "arena_m3": arena_m3,
        "grava_m3": grava_m3,
        "costo_estimado": sacos * precio_saco
    }

# ==========================================================
# INTERFAZ STREAMLIT
# ==========================================================
st.title("🏗️ Asesor Técnico de Ferretería – IA Pro+")
st.markdown("Presupuestos de obra precisos, sin suposiciones ni errores técnicos.")

user_input = st.text_input(
    "Describe tu proyecto:",
    placeholder="Ej: Losa de 8x5 metros, 15 cm de espesor para uso estructural"
)

if user_input:
    with st.spinner("Analizando especificaciones técnicas..."):
        try:
            proyecto = extraer_datos_ia(user_input)
            faltantes = validar_proyecto(proyecto)

            if faltantes:
                st.warning(
                    f"Faltan datos críticos para continuar: **{', '.join(faltantes)}**. "
                    "Por favor indícalos explícitamente."
                )
            else:
                resultado = calcular_materiales(proyecto)

                st.success("### ✅ Cálculo técnico completado")

                c1, c2, c3 = st.columns(3)
                c1.metric("Cemento", f"{resultado['cemento_sacos']} sacos")
                c2.metric("Arena", f"{resultado['arena_m3']} m³")
                c3.metric("Grava", f"{resultado['grava_m3']} m³")

                st.metric("Costo estimado de cemento", f"${resultado['costo_estimado']}")

                with st.expander("Detalle técnico"):
                    st.write(f"- Volumen total: {resultado['volumen_m3']} m³")
                    st.write(f"- Uso declarado: {proyecto.uso}")
                    st.write("- Incluye 7% de desperdicio")

        except Exception:
            st.error("Error al procesar la solicitud. Verifica la configuración del sistema.")
