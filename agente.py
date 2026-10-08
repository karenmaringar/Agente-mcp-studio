from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver   # MEMORIA (1)
from langchain_core.runnables import RunnableConfig

load_dotenv()

# ---------- TOOL 1: calculadora ----------
@tool
def calculadora(expresion: str) -> str:
    """Sirve para hacer operaciones matemáticas. Recibe una expresión como '25 * 4' o '20 + 30'."""
    permitidos = "0123456789+-*/(). "
    if not all(c in permitidos for c in expresion):
        return "Error: solo se permiten números y los operadores + - * / ( )"
    try:
        return str(eval(expresion, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

# ---------- TOOL 2: guardar_nota ----------
@tool
def guardar_nota(texto: str) -> str:
    """Sirve para guardar una nota en un archivo local. Recibe el texto de la nota."""
    with open("notas.txt", "a", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")
    return "Nota guardada correctamente."

# ---------- MODELO ----------
# Deja aquí el modelo que SÍ te funcionó en el paso anterior
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", timeout=120, max_retries=2)

# ---------- MEMORIA ----------
memoria = InMemorySaver()                                # MEMORIA (2)

# ---------- AGENTE ----------
agente = create_agent(
    model=llm,
    tools=[calculadora, guardar_nota],
    system_prompt="Eres un asistente de estudio amable. Responde en español y de forma breve.",
    checkpointer=memoria,                                # MEMORIA (3)
)

# ---------- FUNCIÓN para preguntar ----------
config: RunnableConfig = {"configurable": {"thread_id": "conversacion-1"}}   # MEMORIA (4)

def preguntar(texto):
    resultado = agente.invoke(
        {"messages": [{"role": "user", "content": texto}]},
        config,                                          # MEMORIA (5)
    )
    for m in resultado["messages"]:
        if m.type == "ai" and m.tool_calls:
            print("   🔧 Tool usada:", m.tool_calls[0]["name"])
    print("Agente:", resultado["messages"][-1].text)

# ---------- CONVERSACIÓN EN LA TERMINAL ----------
print("Asistente de estudio listo. Escribe 'salir' para terminar.\n")

while True:
    texto = input("Tú: ")
    if texto.strip().lower() == "salir":
        print("¡Hasta luego!")
        break
    if texto.strip() == "":
        continue
    preguntar(texto)
    print()