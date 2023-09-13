import streamlit as st
import requests

def translate_document(document, target_language, api_key):
    # Configurar la URL de la API de AI Translate
    url = "https://ai-translate.pro/api/{API_KEY}/{source}-{target}".format(
        API_KEY=api_key,
        source="en",
        target=target_language
    )

    # Configurar los datos de la solicitud
    data = {
        "text": document
    }

    # Realizar la solicitud POST a la API de AI Translate
    response = requests.post(url, json=data)

    # Obtener la traducción del documento
    translated_document = response.json()["text"]

    return translated_document

def main():
    st.title("Traductor de documentos")

    # Ingresar la clave API de AI Translate
    api_key = st.sidebar.text_input("Clave API de AI Translate")

    # Cargar el documento
    uploaded_file = st.file_uploader("Cargar documento", type=["docx"])

    if uploaded_file is not None:
        # Leer el contenido del documento
        document = docx2txt.process(uploaded_file)

        # Seleccionar el idioma objetivo
        target_language = st.selectbox("Seleccionar idioma objetivo", ["Español", "Francés", "Alemán"])

        # Traducir el documento
        if st.button("Traducir"):
            if api_key:
                # Traducir el documento utilizando la clave API de AI Translate
                translated_document = translate_document(document, target_language, api_key)

                # Mostrar el documento traducido
                st.write("Documento traducido:")
                st.write(translated_document)
            else:
                st.write("Por favor, ingresa tu clave API de AI Translate en la columna izquierda.")

if __name__ == "__main__":
    main()
