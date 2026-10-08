import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langchain_mcp_adapters.client import MultiServerMCPClient   # MCP (1)
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

RUTA_SERVIDOR = os.path.join(os.path.dirname(__file__), "servidor_mcp.py")

async def main():
    # ---------- MCP: conectar con el servidor ----------
    cliente = MultiServerMCPClient({                         # MCP (2)
        "estudio": {
            "command": sys.executable,       # el Python de tu venv
            "args": [RUTA_SERVIDOR],         # lanza servidor_mcp.py
            "transport": "stdio",
        }
    })
    tools = await cliente.get_tools()                        # MCP (3)
    print("Tools cargadas desde el servidor MCP:", [t.name for t in tools])

    # ---------- MODELO ----------
    # Deja aquí el modelo que SÍ te funciona
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", timeout=120, max_retries=2)
    # ---------- MEMORIA ----------
    memoria = InMemorySaver()

    # ---------- AGENTE ----------
    agente = create_agent(
        model=llm,
        tools=tools,                                         # Tools que vienen del servidor
        system_prompt="Eres un asistente de estudio amable. Responde en español y de forma breve.",
        checkpointer=memoria,
    )
    config: RunnableConfig = {"configurable": {"thread_id": "conversacion-1"}}

    # ---------- CONVERSACIÓN ----------
    print("Asistente de estudio (MCP) listo. Escribe 'salir' para terminar.\n")
    while True:
        texto = await asyncio.to_thread(input, "Tú: ")
        if texto.strip().lower() == "salir":
            print("¡Hasta luego!")
            break
        if texto.strip() == "":
            continue

        resultado = await agente.ainvoke(
            {"messages": [{"role": "user", "content": texto}]},
            config=config,
        )
        for m in resultado["messages"]:
            if m.type == "ai" and m.tool_calls:
                print("   🔧 Tool MCP usada:", m.tool_calls[0]["name"])
        print("Agente:", resultado["messages"][-1].text, "\n")

asyncio.run(main())