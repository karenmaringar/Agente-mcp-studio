from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Carga la API key desde el archivo .env
load_dotenv()

# 2. Crea el modelo (LangChain se conecta a Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

# 3. Envía la pregunta y espera la respuesta
respuesta = llm.invoke("¿Qué es un agente de IA? Responde en 2 frases.")

# 4. Muestra el texto
print(respuesta.content)