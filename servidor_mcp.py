import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AsistenteEstudio")

# ---------- TOOL 1: calculadora ----------
@mcp.tool()
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
@mcp.tool()
def guardar_nota(texto: str) -> str:
    """Sirve para guardar una nota en un archivo local. Recibe el texto de la nota."""
    ruta = os.path.join(os.path.dirname(__file__), "notas.txt")
    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")
    return "Nota guardada correctamente."

if __name__ == "__main__":
    mcp.run(transport="stdio")