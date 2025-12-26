import streamlit as st

# Configuración de la página
st.set_page_config(page_title="IA Agent Factory", page_icon="🤖")

st.title("🤖 Fábrica de Agentes de IA")
st.write("Configura el cerebro de tu negocio en 30 segundos.")

# --- INTERFAZ DE USUARIO ---
with st.sidebar:
    st.header("Configuración")
    nicho = st.text_input("¿Qué negocio tienes?", placeholder="Ej: Clínica Veterinaria")
    tono = st.select_slider("Tono de voz", options=["Muy Formal", "Profesional", "Amistoso", "Divertido"])
    incentivo = st.text_input("Regalo para el cliente", placeholder="Ej: 10% de descuento")

# --- LÓGICA DEL META-AGENTE ---
if st.button("Generar Agente"):
    if nicho:
        # Aquí la IA "ensambla" el resultado
        prompt_final = f"""
        # PROMPT MAESTRO GENERADO
        ROL: Eres un experto en {nicho}.
        TONO: Tu comunicación debe ser {tono}.
        TAREA: Ayuda al cliente y convéncelo de usar este beneficio: {incentivo}.
        RESTRICCIONES: No inventes datos técnicos. Sé breve y humano.
        """
        
        st.success("✅ ¡Agente listo para trabajar!")
        st.subheader("Tu Prompt Maestro:")
        st.code(prompt_final, language="markdown")
        
        st.info("💡 Copia este código en ChatGPT o en tu plataforma de chatbot favorita.")
    else:
        st.error("Por favor, dinos de qué trata tu negocio.")
