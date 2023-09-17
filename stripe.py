import streamlit as st
import requests

# Obtener la clave pública de Stripe desde los secrets de Streamlit
stripe_publishable_key = st.secrets["STRIPE_KEY"]

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Función para traducir texto
def translate_text(text, lang_from, lang_to):
    url = f"{BASE_URL}/{lang_from}-{lang_to}"
    headers = {'Content-Type': 'application/json'}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()["result"]
        return result
    else:
        return None

# Título de la aplicación
st.title("Traductor de Texto")

# Entrada de texto
text = st.text_area("Ingrese el texto a traducir")

# Selección de idiomas
lang_from = st.selectbox("Seleccione el idioma de origen:", ["en", "es"])
lang_to = st.selectbox("Seleccione el idioma de destino:", ["en", "es"])

# Botón para traducir
if st.button("Traducir"):
    translation = translate_text(text, lang_from, lang_to)
    if translation:
        st.success(f"Texto traducido: {translation}")
    else:
        st.error("Error al traducir el texto. Verifique su conexión a Internet o intente nuevamente.")

# Mostrar clave pública de Stripe
st.write("Clave pública de Stripe:")
st.write(stripe_publishable_key)
