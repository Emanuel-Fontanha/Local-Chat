import asyncio
import websockets
import http.server
import socketserver
import threading
import json

PORTA_HTTP = 8080
PORTA_WS = 8000
clientes_ws = {}  # websocket: nome
mensagens_anteriores = []

# Servidor HTTP simples para servir os arquivos estáticos
def iniciar_http():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORTA_HTTP), handler) as httpd:
        print(f"[HTTP] Servidor rodando em http://0.0.0.0:{PORTA_HTTP}")
        httpd.serve_forever()

# Handler do WebSocket
async def handler_ws(websocket):
    try:
        nome = await websocket.recv()
        clientes_ws[websocket] = nome
        print(f"[WebSocket] {nome} conectado")

        # Envia histórico
        for msg in mensagens_anteriores:
            await websocket.send(f"[Histórico] {msg}")

        async for mensagem in websocket:
            nome_usuario = clientes_ws[websocket]
            texto_formatado = f"{nome_usuario}: {mensagem}"
            mensagens_anteriores.append(texto_formatado)

            if len(mensagens_anteriores) > 20:
                mensagens_anteriores.pop(0)

            await asyncio.gather(*[
                c.send(texto_formatado) for c in clientes_ws
            ])
    except:
        pass
    finally:
        nome = clientes_ws.get(websocket, "Desconhecido")
        print(f"[WebSocket] {nome} desconectado")
        clientes_ws.pop(websocket, None)

# Função principal para rodar o WebSocket
async def main():
    print(f"[WebSocket] Servidor rodando em ws://0.0.0.0:{PORTA_WS}")
    async with websockets.serve(handler_ws, "0.0.0.0", PORTA_WS):
        await asyncio.Future()  # mantém o servidor rodando

if __name__ == "__main__":
    threading.Thread(target=iniciar_http, daemon=True).start()
    asyncio.run(main())
