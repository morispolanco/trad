import openai
import streamlit as st
import PyPDF2
from reportlab.pdfgen import canvas

def translate_document(document, target_language, api_key):
    # Dividir el documento en páginas
    pages = document.getNumPages()
    
    # Traducir cada página utilizando OpenAI
    translated_pages = []
    for page_num in range(pages):
        page = document.getPage(page_num)
        page_text = page.extractText()
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=page_text,
            max_tokens=100,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None,
            n=1,
            log_level="info",
            api_key=api_key
        )
        translated_text = response.choices[0].text.strip()
        translated_pages.append(translated_text)
    
    # Generar un nuevo archivo PDF con el texto traducido
    translated_pdf = canvas.Canvas("translated_document.pdf")
    for translated_page in translated_pages:
        translated_pdf.drawString(100, 100, translated_page)
        translated_pdf.showPage()
    translated_pdf.save()
    
    return "translated_document.pdf"

def main():
    st.title("Traductor de Documentos PDF")
    
    # Obtener el archivo PDF del usuario
    pdf_file = st.file_uploader("Cargar archivo PDF", type=["pdf"])
    
    # Obtener el idioma de destino del usuario
    target_language = st.selectbox("Seleccione el idioma de destino", ["Español", "Francés", "Alemán"])
    
    # Obtener la clave de API del usuario
    api_key = st.text_input("Ingrese su clave de API de OpenAI")
    
    # Mapear el idioma de destino seleccionado al código de idioma correspondiente
    language_code = ""
    if target_language == "Español":
        language_code = "es"
    elif target_language == "Francés":
        language_code = "fr"
    elif target_language == "Alemán":
        language_code = "de"
    
    # Traducir el documento si se ha cargado un archivo, se ha seleccionado un idioma de destino y se ha ingresado una clave de API
    if st.button("Traducir") and pdf_file and language_code and api_key:
        # Leer el contenido del archivo PDF utilizando la biblioteca PyPDF2
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        
        # Traducir el documento utilizando la función translate_document()
        translated_document = translate_document(pdf_reader, language_code, api_key)
        
        # Mostrar el enlace de descarga del documento traducido al usuario
        st.markdown(f"Descargar el documento traducido: [translated_document.pdf](./{translated_document})")

if __name__ == "__main__":
    main()
