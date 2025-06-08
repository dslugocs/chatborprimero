import streamlit as st
import requests

# 1. Configuración inicial
st.set_page_config(page_title="mi primer chat bot", page_icon="🤖")

st.title("🤖 mi primer chat bot")
st.markdown("Selecciona un modelo, escribe tu mensaje y conversa con el LLM.")

# 2. Clave API
API_KEY = st.secrets.get("GROQ_API_KEY")

if not API_KEY:
    st.error("Falta la clave API. Define 'GROQ_API_KEY' en .streamlit/secrets.toml")
    st.stop()

# 3. Modelos actuales disponibles en Groq (Junio 2025)
modelos_disponibles = {
    "LLaMA 3 8B": "llama3-8b-8192",
    "LLaMA 3 70B": "llama3-70b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 7B IT": "gemma-7b-it"
}

# 4. Selección del modelo
modelo_nombre = st.selectbox("Selecciona un modelo:", list(modelos_disponibles.keys()))
modelo_id = modelos_disponibles[modelo_nombre]

# 5. Entrada del usuario
mensaje_usuario = st.text_area("Escribe tu mensaje:", height=150)

# 6. Función para enviar mensaje a Groq
def generar_respuesta(modelo, mensaje):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": modelo,
        "messages": [{"role": "user", "content": mensaje}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# 7. Lógica del botón
if st.button("Enviar"):
    if not mensaje_usuario.strip():
        st.warning("Por favor, escribe un mensaje.")
    else:
        with st.spinner("Generando respuesta..."):
            respuesta = generar_respuesta(modelo_id, mensaje_usuario)
        st.markdown("### 💬 Respuesta:")
        st.write(respuesta)

