import streamlit as st
import stripe

# Configurar las claves de API de Stripe
stripe.api_key = 'your_stripe_secret_key'
stripe.api_version = '2020-08-27'

# Página de inicio
def home():
    st.title('Bienvenido a la aplicación de suscripción')
    st.write('Aquí puedes suscribirte para acceder a la aplicación de traducción.')

    # Obtener los planes de suscripción disponibles desde Stripe
    plans = stripe.Price.list(active=True, type='recurring')

    # Mostrar los planes de suscripción en un formulario
    selected_plan = st.selectbox('Selecciona un plan de suscripción:', options=[(plan.id, plan.nickname) for plan in plans.data])

    # Botón de suscripción
    if st.button('Suscribirse'):
        # Crear una sesión de checkout en Stripe
        session = stripe.checkout.Session.create(
            success_url='http://localhost:8501/translate',
            cancel_url='http://localhost:8501/',
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': selected_plan,
                'quantity': 1,
            }],
        )

        # Redirigir al usuario a la página de checkout de Stripe
        st.redirect(session.url)

# Página de traducción
def translate():
    st.title('Aplicación de traducción')
    st.write('Aquí puedes utilizar la aplicación de traducción.')

    # Lógica de la aplicación de traducción
    # ...

# Enrutamiento de páginas
if __name__ == '__main__':
    page = st.sidebar.selectbox('Selecciona una página:', options=['Inicio', 'Traducción'])

    if page == 'Inicio':
        home()
    elif page == 'Traducción':
        translate()
