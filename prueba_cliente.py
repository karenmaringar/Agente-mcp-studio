import asyncio
from fastmcp import Client

async def main():
    # El cliente lanza servidor_mcp.py por su cuenta y se conecta a él
    async with Client("servidor_mcp.py") as cliente:
        tools = await cliente.list_tools()
        print("Tools del servidor:", [t.name for t in tools])

        resultado = await cliente.call_tool("calculadora", {"expresion": "3*4"})
        print("3*4 =", resultado.data)

asyncio.run(main())