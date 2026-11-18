# Qual é o seu signo? — Flask + SQL

Aplicação web completa em **Python (Flask)** com banco de dados **SQLite (`signos.db`)** já incluído e populado no repositório para visualização imediata no Git.

## Como rodar (1 clique no Windows)
Dê um duplo clique no arquivo **`iniciar.bat`**. Ele cria o ambiente virtual, instala o Flask, inicia o servidor e abre o navegador automaticamente em `http://127.0.0.1:5000`.

## Como rodar manualmente no terminal

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000` ou `http://localhost:5000` no navegador.

## Estrutura

```text
signo-flask/
├── app.py              # rotas Flask + lógica de cálculo do signo + abertura automática do navegador
├── schema.sql          # criação da tabela `submissions`
├── signos.db           # banco de dados SQLite pré-criado para aparecer no Git
├── iniciar.bat         # atalho automático para rodar no Windows
├── requirements.txt    # dependências Python (Flask)
├── .gitignore          # ignora venv/ e __pycache__/, mantendo signos.db visível no Git
├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── templates/
    └── index.html
```
