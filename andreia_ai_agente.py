from flask import Flask, request, jsonify, render_template_string, send_from_directory
import logging
import json
# Importações do seu andreia_ai_agente.py (precisaremos delas depois)
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool, HarmCategory, HarmBlockThreshold
import psycopg2
import psycopg2.extras 
import os
import time
from dotenv import load_dotenv
from decimal import Decimal
from flask_cors import CORS

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API Key do Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("ERRO: A variável de ambiente GEMINI_API_KEY não foi definida no arquivo .env.")
    exit()
genai.configure(api_key=gemini_api_key)

# Parâmetros de conexão ao banco de dados
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT', '5432')

MODEL_GEMINI = "gemini-1.5-pro"

def conectar_db():
    if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
        logging.error("Variáveis de ambiente para conexão com o banco não estão todas definidas.")
        return None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def buscar_produto(nome_produto):
    conn = conectar_db()
    if not conn:
        return {"erro": "Não foi possível conectar ao banco de dados"}
    
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = """
            SELECT 
                descricao, 
                preco, 
                estoque
            FROM produtos 
            WHERE LOWER(descricao) LIKE LOWER(%s)
            """
            cur.execute(query, (f"%{nome_produto}%",))
            resultados = cur.fetchall()
            
            produtos = []
            for row in resultados:
                produto = dict(row)
                if isinstance(produto['preco'], Decimal):
                    produto['preco'] = float(produto['preco'])
                produtos.append(produto)
            
            return produtos
    except Exception as e:
        logging.error(f"Erro ao buscar produto: {e}")
        return {"erro": str(e)}
    finally:
        conn.close()

# Configuração do modelo Gemini
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Criar o modelo
model = genai.GenerativeModel(
    model_name=MODEL_GEMINI,
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Dicionário para armazenar as sessões de chat
chat_sessions = {}

app = Flask(__name__, static_folder='.')
CORS(app)

# --- HTML BÁSICO PARA A PÁGINA DE CHAT (incorporado no Python para simplicidade) ---
CHAT_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat com AndreIA</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f4; }
        #chatbox { width: 100%; max-width: 600px; margin: auto; background-color: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        #messages { list-style-type: none; margin: 0; padding: 20px; height: 400px; overflow-y: scroll; border-bottom: 1px solid #eee; }
        #messages li { padding: 8px 12px; margin-bottom: 10px; border-radius: 20px; line-height: 1.4; }
        #messages li.user { background-color: #007bff; color: white; margin-left: 40px; text-align: right; }
        #messages li.assistant { background-color: #e9e9eb; color: #333; margin-right: 40px; text-align: left; }
        #form { display: flex; padding: 10px; }
        #input { border: 1px solid #ddd; padding: 10px; flex-grow: 1; border-radius: 20px; margin-right: 10px; }
        button { background: #007bff; border: none; color: white; padding: 10px 15px; border-radius: 20px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div id="chatbox">
        <ul id="messages"></ul>
        <form id="form" action="">
            <input id="input" autocomplete="off" placeholder="Digite sua mensagem..." /><button>Enviar</button>
        </form>
    </div>
    <script>
        const form = document.getElementById('form');
        const input = document.getElementById('input');
        const messages = document.getElementById('messages');
        const userId = 'user_' + Math.random().toString(36).substr(2, 9); // ID de usuário simples para esta sessão

        // Adiciona a saudação inicial da AndreIA
        const initialAssistantMsg = document.createElement('li');
        initialAssistantMsg.classList.add('assistant');
        initialAssistantMsg.textContent = "AndreIA: Olá! Aqui é a AndreIA, da Paulo Loja 3 Maxi. Em que posso ajudar?";
        messages.appendChild(initialAssistantMsg);
        window.scrollTo(0, document.body.scrollHeight);

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            if (input.value) {
                const userMessage = input.value;
                addMessage(userMessage, 'user');
                input.value = '';

                const response = await fetch('/chat_message', { // Endpoint para enviar mensagem
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMessage, user_id: userId })
                });
                const data = await response.json();
                addMessage('AndreIA: ' + data.reply, 'assistant');
            }
        });

        function addMessage(text, senderClass) {
            const item = document.createElement('li');
            item.classList.add(senderClass);
            item.textContent = text;
            messages.appendChild(item);
            messages.scrollTop = messages.scrollHeight; // Rola para a última mensagem
        }
    </script>
</body>
</html>
"""

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        session_id = data.get('session_id', 'default')

        if session_id not in chat_sessions:
            chat_sessions[session_id] = model.start_chat(history=[])
            
        chat = chat_sessions[session_id]
        response = chat.send_message(message)

        reply = response.text if response.text else "Desculpe, não consegui processar sua mensagem."
        return jsonify({'response': reply})

    except Exception as e:
        logging.error(f"Erro no processamento do chat: {str(e)}")
        return jsonify({'response': 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.'}), 500

if __name__ == '__main__':
    logging.info("Iniciando servidor Flask para chat com AndreIA na porta 5002...")
    # Usar uma porta diferente do webhook da Evolution para não haver conflito
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 