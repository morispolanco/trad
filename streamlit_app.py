import streamlit as st
import requests
import docx2txt
import os

def translate_document(document, target_language, api_key):
    # Configurar la URL de la API de AI Translate
    url = "https://ai-translate.pro/api/{API_KEY}/en-{target}".format(
        API_KEY=api_key,
        target=target_language
    )

    # Configurar los datos de la solicitud
    data = {
        "text": document
    }

    # Realizar la solicitud POST a la API de AI Translate
    response = requests.post(url, json=data)

    # Resto del código...

def main():
    st.title("Traductor de documentos")

    # Obtener la clave API de AI Translate desde la variable de entorno
    api_key = os.getenv("API_KEY")

    if api_key is None:
        st.write("Por favor, configura la variable de entorno API_KEY con tu clave API de AI Translate.")
        return

    # Cargar el documento
    uploaded_file = st.file_uploader("Cargar documento", type=["docx"])

    if uploaded_file is not None:
        # Leer el contenido del documento
        document = docx2txt.process(uploaded_file)

        # Seleccionar el idioma objetivo
        target_language = st.selectbox("Seleccionar idioma objetivo", ["es", "en", "fr"])

        # Traducir el documento
        if st.button("Traducir"):
            # Traducir el documento utilizando la clave API de AI Translate
            try:
                translated_document = translate_document(document, target_language, api_key)

                # Mostrar el documento traducido
                st.write("Documento traducido:")
                st.write(translated_document)
            except ValueError as e:
                st.write("Error en la traducción del documento:", str(e))

if __name__ == "__main__":
    main()
