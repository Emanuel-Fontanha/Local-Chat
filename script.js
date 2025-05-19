let ws;
let nome;

window.onload = () => {
    nome = prompt("Digite seu nome:");
    if (!nome || nome.trim() === "") {
        nome = "Anônimo: ";
    }

    const ipServidor = location.hostname;
    ws = new WebSocket(`ws://${ipServidor}:8000`);

    ws.onopen = () => {
        ws.send(nome); // Envia nome ao conectar
    };

    ws.onmessage = (event) => {
        document.getElementById("chat").value += event.data + "\n";
    };
};

function enviar() {
    const input = document.getElementById("mensagem");
    if (input.value.trim() && ws.readyState === WebSocket.OPEN) {
        ws.send(input.value);
        input.value = "";
    }
}
