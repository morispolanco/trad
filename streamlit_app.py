import streamlit as st
import requests
import json
import os

def translate_text(text, source_lang, target_lang, api_key):
    # Configurar la URL de la API de AI Translate
    url = f"https://ai-translate.pro/api/{api_key}/{source_lang}-{target_lang}"

    # Configurar los datos de la solicitud
    data = {
        "text": text
    }

    # Realizar la solicitud POST a la API de AI Translate
    response = requests.post(url, json=data)

    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener la respuesta JSON
        json_response = response.json()

        # Comprobar si la respuesta JSON tiene la clave "result"
        if "result" in json_response:
            # Obtener el texto traducido
            translated_text = json_response["result"]

            return translated_text
        else:
            raise ValueError("La respuesta JSON no tiene la clave 'result'")
    else:
        raise ValueError("Error en la solicitud a la API de AI Translate")

def main():
    st.title("Traductor de documentos")

    # Ingresar la clave API de AI Translate
    api_key = os.getenv["api_key"]

    # Ingresar el texto a traducir
    text = st.text_area("Texto a traducir")

    # Seleccionar el idioma de origen y destino
    source_lang = st.selectbox("Idioma de origen", ["en", "es"])
    target_lang = st.selectbox("Idioma de destino", ["en", "es"])

    # Traducir el texto
    if st.button("Traducir"):
        if api_key:
            # Traducir el texto utilizando la clave API de AI Translate
            try:
                translated_text = translate_text(text, source_lang, target_lang, api_key)

                # Mostrar el texto traducido
                st.write("Texto traducido:")
                st.write(translated_text)
            except ValueError as e:
                st.write("Error en la traducción del texto:", str(e))
        else:
            st.write("Por favor, ingresa tu clave API de AI Translate en los secrets de Streamlit.")

if __name__ == "__main__":
    main()
