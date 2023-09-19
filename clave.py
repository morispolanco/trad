import streamlit as st
import requests
from docx import Document
from io import BytesIO

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


# Agregar título y texto en la parte superior de la columna
st.sidebar.markdown("# La mejor traducción automática del mundo")
st.sidebar.markdown("Las redes neuronales de AITranslate son capaces de captar hasta los más mínimos matices y reproducirlos en la traducción a diferencia de cualquier otro servicio. Para evaluar la calidad de nuestros modelos de traducción automática, realizamos regularmente pruebas a ciegas. En las pruebas a ciegas, los traductores profesionales seleccionan la traducción más precisa sin saber qué empresa la produjo. AITranslate supera a la competencia por un factor de 3:1. Desde el lanzamiento inicial de AITranslate en 2018, hemos estado desarrollando una generación completamente nueva de redes neuronales (NN). Utilizando un novedoso diseño de NN, las redes de AITranslate aprenden a captar los significados sutiles de las oraciones y traducirlas a un idioma de destino de una manera sin precedentes. Esto ha llevado a una calidad de traducción automática de renombre mundial que supera a todas las principales empresas de tecnología. AITranslate no solo se mantiene al día con las empresas de aprendizaje profundo líderes en el mundo, sino que continúa estableciendo nuevos estándares con sus avances en matemáticas y metodología de redes neuronales. En 2020 y 2021, lanzamos nuevos modelos que pueden transmitir con mayor precisión el significado de las oraciones traducidas, incluso superando el desafío de la jerga profesional específica de la industria con gran éxito. En AITranslate, apenas estamos empezando. Continuaremos utilizando nuestra experiencia en inteligencia artificial y redes neuronales para crear tecnologías que hagan que la comunicación sea más rápida, mejor y más fácil.")


# Campo de entrada para la clave API
secret_key = st.sidebar.text_input("Ingrese su clave API de AI Translate")

# Explicación sobre cómo obtener la clave API
st.sidebar.markdown("Para obtener la clave API de AI Translate, por favor envíe un correo electrónico a info@editorialarje.com.")





# Cargar archivo DOCX
uploaded_file = st.file_uploader("Cargar archivo DOCX", type=["docx"])

# Selección de idiomas
lang_from = st.selectbox("Seleccione el idioma de origen:", ["en", "es"])
lang_to = st.selectbox("Seleccione el idioma de destino:", ["en", "es"])

# Botón para traducir
if st.button("Traducir"):
    if secret_key and uploaded_file is not None:
        # Leer el contenido del archivo DOCX
        docx = Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in docx.paragraphs])

        translation, available_chars = translate_text(text, lang_from, lang_to, secret_key)
        if translation:
            # Crear un nuevo documento DOCX con la traducción
            translated_docx = Document()
            translated_docx.add_paragraph(translation)

            # Guardar el documento DOCX en un objeto BytesIO
            docx_buffer = BytesIO()
            translated_docx.save(docx_buffer)
            docx_buffer.seek(0)

            # Descargar el archivo DOCX
            st.download_button("Descargar traducción", data=docx_buffer, file_name="traduccion.docx")

            st.success("La traducción se ha guardado en el archivo 'traduccion.docx'")
            st.info(f"Caracteres disponibles: {available_chars}")
        else:
            st.error("Error al traducir el texto. Verifique su clave API o intente nuevamente.")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y cargue un archivo DOCX.")
