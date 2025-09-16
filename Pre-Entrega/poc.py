!pip install python-dotenv
!pip install google-generativeai
import google.generativeai as genai
import os

# --- 1. CONFIGURACIÓN ---
# Reemplaza con tu clave de Google AI
API_KEY = "TU_API_KEY_AQUI"
genai.configure(api_key=API_KEY)

# --- 2. BASE DE CONOCIMIENTO (PROMPT) ---
BASE_DE_CONOCIMIENTO = """
- Expensas de Septiembre: 15.000 ARS, vencimiento 25/09/2025.
- Reglamento interno: Se prohíbe el uso de la pileta después de las 22:00 hs. Las multas por ruidos molestos se aplicarán según el artículo 15.
- Cartilla de servicios:
    - Plomero autorizado: Juan Pérez, tel: 11-1234-5678.
    - Electricista de confianza: Pedro Gómez, tel: 11-9876-5432.
"""

# Las instrucciones que le das a la IA para que actúe como tu asistente
PROMPT_INSTRUCCIONES = """
Eres un asistente de consorcio llamado "Consorcio Bot", amable y eficiente. Responde a las preguntas de los vecinos.

Tienes acceso a la siguiente información:
{base_de_conocimiento}

Tus funciones principales son:
1. Si el usuario hace una pregunta sobre expensas, reglamento o servicios, usa la información anterior para responder de forma directa y concisa.
2. Si el usuario quiere hacer un reclamo o queja, responde con un mensaje amigable pidiendo su nombre, número de unidad y una descripción detallada del problema para registrarlo. No intentes registrar el reclamo tú mismo, solo pide la información.
3. Si no puedes responder la pregunta o no la entiendes, deriva al usuario al administrador con el mensaje: "Lo siento, no puedo ayudarte con eso en este momento. Por favor, contacta a la administración directamente."

---
Usuario: {mensaje_del_usuario}
Consorcio Bot:
"""

# --- 3. PRUEBA DEL CONCEPTO ---
def probar_poc(pregunta_del_usuario):
    """Función para probar la respuesta de la IA a una pregunta."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Le damos a la IA el prompt con la pregunta del usuario
        prompt_completo = PROMPT_INSTRUCCIONES.format(
            base_de_conocimiento=BASE_DE_CONOCIMIENTO,
            mensaje_del_usuario=pregunta_del_usuario
        )
        
        # Generamos la respuesta
        response = model.generate_content(prompt_completo)
        
        # Imprimimos el resultado para verificar la respuesta
        print(f"Pregunta del Usuario: {pregunta_del_usuario}")
        print("-" * 50)
        print(f"Respuesta de la IA:\n{response.text}")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de que tu clave de API sea correcta y el modelo de IA esté configurado.")

# --- EJECUTAR LAS PRUEBAS ---
if __name__ == "__main__":
    # Prueba 1: Un reclamo
    probar_poc("Quiero hacer un reclamo, la luz del pasillo no funciona.")

    # Prueba 2: Una pregunta administrativa
    probar_poc("¿Cuándo vencen las expensas de septiembre?")

    # Prueba 3: Una pregunta sobre servicios
    probar_poc("¿Tienen el número de un plomero de confianza?")

    # Prueba 4: Una pregunta que no puede responder
    probar_poc("¿Quién ganó el partido de fútbol anoche?")