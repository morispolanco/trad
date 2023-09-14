import streamlit as st
import requests
import docx2txt

def translate_document(document, target_language):
    # Obtener la clave API de los secrets de Streamlit
    api_key = st.secrets["API_KEY"]

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
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        response_json = response.json()
        if "translated_text" in response_json:
            translated_document = response_json["translated_text"]
            return translated_document
        else:
            raise ValueError("La respuesta de la API no contiene el campo 'translated_text'")
    else:
        raise ValueError("Error en la solicitud a la API de AI Translate")

def main():
    st.title("Traductor de documentos")

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
                translated_document = translate_document(document, target_language)

                # Mostrar el documento traducido
                st.write("Documento traducido:")
                st.write(translated_document)
            except ValueError as e:
                st.write("Error en la traducción del documento:", str(e))

if __name__ == "__main__":
    main()
