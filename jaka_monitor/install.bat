@echo off
REM Script de instalação automática para Windows
REM Execute este arquivo para configurar o ambiente automaticamente

echo ====================================================================
echo Sistema de Monitoramento JAKA - Instalacao Automatica
echo ====================================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior de: https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python encontrado: 
python --version
echo.

REM Criar ambiente virtual
echo [2/4] Criando ambiente virtual...
if exist venv (
    echo Ambiente virtual ja existe, pulando...
) else (
    python -m venv venv
    echo Ambiente virtual criado com sucesso!
)
echo.

REM Ativar ambiente virtual e instalar dependências
echo [3/4] Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Criar diretórios necessários
echo [4/4] Criando estrutura de diretorios...
if not exist data mkdir data
if not exist reports mkdir reports
if not exist logs mkdir logs
echo.

echo ====================================================================
echo Instalacao concluida com sucesso!
echo ====================================================================
echo.
echo Proximos passos:
echo   1. Edite config.py se necessario (configuracoes MQTT)
echo   2. Execute: python main_gui.py
echo   3. Clique em "Iniciar Monitoramento"
echo.
echo Para testar sem robo real:
echo   - Terminal 1: python main_gui.py
echo   - Terminal 2: python test_simulator.py
echo.
echo Documentacao completa: README.md
echo Guia rapido: QUICKSTART.md
echo ====================================================================
pause
