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
        # Espera o nome do usuário como primeira mensagem
        nome = await websocket.recv()
        clientes_ws[websocket] = nome
        print(f"[WebSocket] {nome} conectado")

        # Envia histórico para o novo usuário
        for msg in mensagens_anteriores:
            await websocket.send(f"[Histórico] {msg}")

        # Comunicação em tempo real
        async for mensagem in websocket:
            nome_usuario = clientes_ws[websocket]
            texto_formatado = f"{nome_usuario}: {mensagem}"
            mensagens_anteriores.append(texto_formatado)

            # (opcional) limita o histórico a 20 mensagens
            if len(mensagens_anteriores) > 20:
                mensagens_anteriores.pop(0)

            # Envia para todos os clientes
            await asyncio.gather(*[
                c.send(texto_formatado) for c in clientes_ws
            ])
    except:
        pass
    finally:
        nome = clientes_ws.get(websocket, "Desconhecido")
        print(f"[WebSocket] {nome} desconectado")
        clientes_ws.pop(websocket, None)

# Rodar servidores
if __name__ == "__main__":
    threading.Thread(target=iniciar_http, daemon=True).start()
    asyncio.run(websockets.serve(handler_ws, "0.0.0.0", PORTA_WS))
