import streamlit as st
import json

# --- FUNCIONES DE LÓGICA (Tus funciones de ferretería) ---

def calcular_materiales(largo, ancho, espesor, uso, precio_saco=15):
    area = largo * ancho
    volumen = area * (espesor / 100)
    # Proporción simple para el ejemplo
    sacos = round(volumen * 7) if uso == "ligero" else round(volumen * 10)
    arena = round(volumen * 0.5, 2)
    total = sacos * precio_saco
    consejo = "Usa malla si es para carga pesada." if uso == "pesado" else "Con acabado liso queda perfecto."
    
    return {"sacos": sacos, "arena": arena, "total": total, "consejo": consejo}

# --- INTERFAZ DE STREAMLIT ---

st.set_page_config(page_title="Ferretería IA - Calculador Pro", page_icon="🏗️")

st.title("🏗️ Calculador de Presupuestos Automático")
st.write("Demostración para dueños de Ferreterías: Presupuestos en segundos.")

# Simulación de Chat
with st.container():
    st.info("💡 **Prueba esto:** 'Quiero hacer un suelo de 5x5 metros con 10cm de espesor para uso pesado'")
    entrada_usuario = st.text_input("¿Qué proyecto tienes en mente?")

if entrada_usuario:
    # Simulamos la extracción de datos (en el MVP real aquí llamarías a la API de Groq/OpenAI)
    # Para la demo, vamos a simular que la IA entendió los datos:
    try:
        # Aquí es donde tu lógica de 'ejecutar_agente_completo' hace su magia
        # Por ahora, simulamos los datos para que el botón funcione sin API Key
        largo, ancho, espesor, uso = 5, 5, 10, "pesado" 
        
        res = calcular_materiales(largo, ancho, espesor, uso)
        
        # MOSTRAR RESULTADOS AL CLIENTE (Lo que el ferretero vende)
        st.success("### ✅ Presupuesto Estimado")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sacos de Cemento", f"{res['sacos']} uds")
        col2.metric("Arena Necesaria", f"{res['arena']} m3")
        col3.metric("Total Inversión", f"${res['total']}")
        
        st.write(f"**Consejo del Experto:** {res['consejo']}")
        
        if st.button("🛒 Enviar pedido por WhatsApp"):
            st.write("Redirigiendo al WhatsApp de la ferretería...")
            
    except Exception as e:
        st.error("Dime las medidas (largo, ancho y espesor) para ayudarte mejor.")

# --- SECCIÓN PARA EL VENDEDOR ---
st.markdown("---")
st.caption("🚀 Esta herramienta aumenta las ventas un 30% al dar presupuestos inmediatos.")
