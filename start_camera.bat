@echo off
title ASCII Camera Real-Time Renderer
echo Inicializando ambiente...
:: O comando 'mode' ajusta o tamanho da janela e buffer para o mesmo tamanho,
:: o que esconde a barra de rolagem lateral e deixa a tela perfeita.
mode con: cols=120 lines=45

cd /d "%~dp0ascii_camera"
python main.py
pause
