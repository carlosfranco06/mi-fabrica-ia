import streamlit as st
import json
from groq import Groq

# 1. Configuración de la App
st.set_page_config(page_title="Ferretería IA Pro", page_icon="🏗️", layout="centered")

# 2. Conexión con la IA (Configura tu API Key en los secretos de Streamlit)
# Para probar localmente puedes poner: client = Groq(api_key="TU_KEY_AQUI")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def extraer_datos_ia(mensaje_usuario):
    prompt = f"""
    Eres un extractor de datos técnico. Analiza el mensaje: "{mensaje_usuario}"
    Extrae: largo (m), ancho (m), espesor (cm) y uso (ligero/pesado).
    Responde ÚNICAMENTE en formato JSON. Si falta un dato, pon null.
    Ejemplo: {{"largo": 5, "ancho": 2, "espesor": 10, "uso": "pesado"}}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def calcular_presupuesto(datos):
    largo = datos['largo']
    ancho = datos['ancho']
    espesor = datos['espesor']
    uso = datos['uso'] or "ligero" # Default por seguridad
    
    volumen = largo * ancho * (espesor / 100)
    sacos = round(volumen * 10) if uso == "pesado" else round(volumen * 7)
    arena = round(volumen * 0.5, 2)
    total = sacos * 15 # Precio por saco
    
    return {"sacos": sacos, "arena": arena, "total": total}

# --- INTERFAZ DE USUARIO PROFESIONAL ---
st.title("🏗️ Asesor Técnico de Ferretería")
st.markdown("Genera presupuestos precisos mediante lenguaje natural.")

user_input = st.text_input("Describe tu proyecto:", placeholder="Ej: Quiero un piso de 6x4 metros con 12cm de grosor para un camión")

if user_input:
    with st.spinner("IA analizando especificaciones técnicas..."):
        try:
            # Paso 1: Extracción real con IA
            datos = extraer_datos_ia(user_input)
            
            # Paso 2: Validación de datos nulos
            faltantes = [k for k, v in datos.items() if v is None and k != 'uso']
            
            if faltantes:
                st.warning(f"🔎 Me faltan algunos detalles para ser preciso: **{', '.join(faltantes)}**. ¿Podrías indicarlos?")
            else:
                # Paso 3: Cálculo y Visualización
                res = calcular_presupuesto(datos)
                
                st.success("### ✅ Presupuesto Técnico Generado")
                
                # Diseño de tarjetas profesionales
                c1, c2, c3 = st.columns(3)
                c1.metric("Cemento", f"{res['sacos']} sacos")
                c2.metric("Arena", f"{res['arena']} m3")
                c3.metric("Total Est.", f"${res['total']}")
                
                # Resumen técnico para el ferretero
                with st.expander("Ver detalles técnicos del cálculo"):
                    st.write(f"- **Área total:** {datos['largo'] * datos['ancho']} m2")
                    st.write(f"- **Espesor:** {datos['espesor']} cm")
                    st.write(f"- **Resistencia:** Uso {datos['uso']}")

                st.button("📲 Enviar presupuesto a mi WhatsApp")
                
        except Exception as e:
            st.error("Hubo un error al conectar con el cerebro de IA. Revisa tu API Key.")
