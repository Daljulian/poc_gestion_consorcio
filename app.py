

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Reemplaza "TU_API_KEY_AQUI" con tu clave real de Google AI
API_KEY = "AIzaSyCvj_Fzl5gc7iuv8zbhBJfnp9dxDASGwfU"
genai.configure(api_key=API_KEY)

app = Flask(__name__)

# La base de conocimiento del consorcio para el LLM
BASE_DE_CONOCIMIENTO = """
- Expensas de Septiembre: 15.000 ARS, vencimiento 25/09/2025.
- Reglamento interno: Se prohíbe el uso de la pileta después de las 22:00 hs. Las multas por ruidos molestos se aplicarán según el artículo 15.
- Cartilla de servicios:
    - Plomero autorizado: Juan Pérez, tel: 11-1234-5678.
    - Electricista de confianza: Pedro Gómez, tel: 11-9876-5432.
"""

# Inicializa el modelo de Gemini
model = genai.GenerativeModel('gemini-pro')

@app.route("/webhook", methods=["POST"])
def webhook():
    mensaje_entrante = request.values.get('Body', '')
    respuesta_twilio = MessagingResponse()

    # Diseñamos el prompt para darle el "rol" y las "reglas" a la IA
    prompt = f"""
    Eres un asistente de consorcio llamado "Consorcio Bot", amable y eficiente. Responde a las preguntas de los vecinos.

    Tienes acceso a la siguiente información:
    {BASE_DE_CONOCIMIENTO}

    Tus funciones principales son:
    1. Si el usuario hace una pregunta sobre expensas, reglamento o servicios, usa la información anterior para responder de forma directa y concisa.
    2. Si el usuario quiere hacer un reclamo o queja, responde con un mensaje amigable pidiendo su nombre, número de unidad y una descripción detallada del problema para registrarlo. No intentes registrar el reclamo tú mismo, solo pide la información.
    3. Si no puedes responder la pregunta o no la entiendes, deriva al usuario al administrador con el mensaje: "Lo siento, no puedo ayudarte con eso en este momento. Por favor, contacta a la administración directamente."

    ---
    Usuario: {mensaje_entrante}
    Consorcio Bot:
    """

    try:
        # Enviamos la consulta al modelo de IA y obtenemos la respuesta
        response_ia = model.generate_content(prompt)

        # Extraemos la respuesta generada por la IA
        respuesta_generada = response_ia.text
        respuesta_twilio.message(respuesta_generada)

    except Exception as e:
        # En caso de error
        print(f"Error al conectar con la API de Google AI: {e}")
        respuesta_twilio.message("Lo siento, hubo un problema. Por favor, inténtalo de nuevo más tarde.")

    return str(respuesta_twilio)

if __name__ == "__main__":
    app.run(debug=True)