import streamlit as st
import requests

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Función para traducir texto
def translate_text(text, lang_from, lang_to, secret_key):
    url = f"{BASE_URL}/{secret_key}/{lang_from}-{lang_to}"
    headers = {'Content-Type': 'application/json'}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()["result"]
        available_chars = response.json()["available_chars"]
        return result, available_chars
    else:
        return None, None

# Título de la aplicación
st.title("AI Translate")

# Explicación sobre cómo obtener la clave API
st.sidebar.markdown("Para obtener la clave API de AI Translate, por favor envíe un correo electrónico a info@editorialarje.com.")
st.sidebar.markdown("Máximo número de caracteres por documento: 6,000.")

# Campo de entrada para la clave API
secret_key = st.sidebar.text_input("Ingrese su clave API de AI Translate")

# Campo de entrada para el texto a traducir
text_to_translate = st.text_area("Ingrese el texto a traducir")

# Selección de idiomas
lang_from = st.selectbox("Seleccione el idioma de origen:", ["en", "es"])
lang_to = st.selectbox("Seleccione el idioma de destino:", ["en", "es"])

# Botón para traducir
if st.button("Traducir"):
    if secret_key and text_to_translate:
        translation, available_chars = translate_text(text_to_translate, lang_from, lang_to, secret_key)
        if translation:
            st.write("Texto traducido:")
            st.write(translation)
            st.info(f"Caracteres disponibles: {available_chars}")
        else:
            st.error("Error al traducir el texto. Verifique su clave API o intente nuevamente.")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y el texto a traducir.")
