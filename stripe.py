import streamlit as st
import stripe
import requests

# Configurar la clave secreta de Stripe
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

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

# Campo de entrada para la información de pago
payment_info = st.text_input("Ingrese su información de pago (tarjeta de crédito)")

# Botón para procesar el pago
if st.button("Procesar Pago"):
    try:
        # Crear una carga de pago en Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # Monto en centavos (ejemplo: $10.00)
            currency="usd",
            payment_method_types=["card"],
        )

        # Confirmar el pago
        stripe.PaymentIntent.confirm(payment_intent.id, payment_method=payment_info)

        # Si el pago es exitoso, realizar la traducción del texto
        translation = translate_text(text, lang_from, lang_to)
        if translation:
            st.success(f"Texto traducido: {translation}")
        else:
            st.error("Error al traducir el texto. Verifique su conexión a Internet o intente nuevamente.")

    except stripe.error.CardError as e:
        # Si hay un error con la tarjeta de crédito, mostrar un mensaje de error
        st.error(f"Error al procesar el pago: {e.error.message}")

    except Exception as e:
        # Si hay un error inesperado, mostrar un mensaje de error
        st.error(f"Error inesperado: {str(e)}")
