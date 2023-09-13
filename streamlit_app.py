import streamlit as st
import openai
from docx import Document

# Configurar la clave de la API de OpenAI
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key
def translate_text(input_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following text to Spanish:\n\n{input_text}\n\nTranslation:",
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=None,
        log_level="info"
    )
    translated_text = response.choices[0].text.strip()
    return translated_text

def read_docx(file):
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def main():
    st.title("Traductor de Documentos con OpenAI")
    
    # Obtener el archivo de entrada del usuario
    input_file = st.file_uploader("Cargar archivo de texto", type=["txt", "docx"])
    
      
    # Traducir el documento si se ha cargado un archivo y se ha ingresado una clave de API
    if st.button("Traducir") and input_file and api_key:
        # Leer el contenido del archivo
        if input_file.type == "txt":
            input_text = input_file.read()
        elif input_file.type == "docx":
            input_text = read_docx(input_file)
        
        # Traducir el texto utilizando la función translate_text()
        translated_text = translate_text(input_text)
        
        # Mostrar el texto traducido al usuario
        st.text_area("Texto traducido", value=translated_text)

if __name__ == "__main__":
    main()
