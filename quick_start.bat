@echo off
REM Quick start para Windows
REM Instala dependências e executa o pipeline

echo.
echo ====================================================================
echo        Sistema Completo de Deteccao de Anomalias - Quick Start
echo ====================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao esta instalado ou nao esta no PATH
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/3] Treinando modelo...
python treinar_modelo_anomalia.py
if errorlevel 1 (
    echo ERRO ao treinar modelo
    pause
    exit /b 1
)

echo.
echo [3/3] Gerando dados de teste...
python gerar_carga_anomala.py

echo.
echo ====================================================================
echo Tudo pronto! Iniciando servidor...
echo.
echo Acesse: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo ====================================================================
echo.

python app.py

pause
