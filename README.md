# AndreIA - Assistente Virtual da Farmácia Paulo Loja 3 Maxi

## 📝 Descrição
AndreIA é uma assistente virtual especializada em atendimento farmacêutico, desenvolvida para a Farmácia Paulo Loja 3 Maxi. Ela utiliza a API do Google Gemini para fornecer um atendimento inteligente e personalizado aos clientes.

## 🚀 Funcionalidades

### Atendimento ao Cliente
- Consulta de produtos e preços
- Verificação de estoque
- Informações sobre medicamentos
- Sugestões de produtos complementares
- Histórico de compras do cliente

### Interface Web
- Design moderno e minimalista
- Tema escuro para melhor visualização
- Interface responsiva (desktop e mobile)
- Chat em tempo real
- Histórico de conversas

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.11+
- Flask (servidor web)
- Google Generative AI (Gemini 1.5 Pro)
- PostgreSQL (banco de dados)
- psycopg2 (conexão com banco de dados)
- python-dotenv (variáveis de ambiente)

### Frontend
- HTML5
- CSS3 (design moderno e responsivo)
- JavaScript (interatividade e comunicação com backend)
- Web Sockets (chat em tempo real)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/brunoharkin/agente_max.git
cd agente_max
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o arquivo `.env`:
```env
GEMINI_API_KEY=sua_chave_api_aqui
DB_HOST=localhost
DB_NAME=farmacia
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_PORT=5432
PORT=5000
```

## 🚀 Executando o Projeto

1. Ative o ambiente virtual:
```bash
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Inicie o servidor:
```bash
python andreia_ai_agente.py
```

3. Acesse a interface web:
- Local: http://localhost:5000
- Rede: http://[IP_DO_SERVIDOR]:5000

## 💬 Uso da Interface

1. Ao acessar, você verá a interface de chat com uma mensagem de boas-vindas
2. Digite sua mensagem no campo de texto
3. Pressione Enter ou clique no botão de envio
4. A AndreIA responderá com as informações solicitadas

## 🔒 Segurança
- Autenticação via API Key do Google Gemini
- Conexão segura com banco de dados
- Proteção contra injeção SQL
- Validação de entrada de dados
- Tratamento de erros robusto

## 🤝 Contribuição
Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores
- Bruno Harkin - Desenvolvimento inicial

## 📞 Suporte
Para suporte e dúvidas, entre em contato através:
- Email: [seu-email@exemplo.com]
- Issues do GitHub: [https://github.com/brunoharkin/agente_max/issues]
