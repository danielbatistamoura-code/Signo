@echo off
title Qual e o seu signo? - Flask + SQLite
cd /d "%~dp0"
echo [1/3] Criando ambiente virtual (se ainda nao existir)...
if not exist venv (
    python -m venv venv
)
echo [2/3] Instalando dependencias...
call venv\Scripts\activate
pip install -r requirements.txt
echo [3/3] Iniciando servidor Flask...
python app.py
pause
