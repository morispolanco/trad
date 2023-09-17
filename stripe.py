import streamlit as st
import stripe
import requests

# Configurar la clave secreta de Stripe
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Título de la aplicación
st.title("Aplicación de Pago y Traducción")

# Campo de entrada para la información de pago
payment_info = st.text_input("Ingrese su información de pago (tarjeta de crédito)")

# Botón para procesar el pago
if st.button("Procesar Pago"):
    try:
        # Crear una carga de pago en Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # Monto en centavos (10 dólares)
            currency="usd",
            payment_method_types=["card"],
        )

        # Confirmar el pago
        stripe.PaymentIntent.confirm(payment_intent.id, payment_method=payment_info)

        # Si el pago es exitoso, redirigir a la aplicación de traducción
        if payment_intent.status == "succeeded":
            st.success("Pago exitoso. Redirigiendo a la aplicación de traducción...")
            translation_url = f"{BASE_URL}/translate"
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={translation_url}">', unsafe_allow_html=True)

    except Exception as e:
        # Si hay un error, mostrar un mensaje de error
        st.error(f"Error al procesar el pago: {str(e)}")
