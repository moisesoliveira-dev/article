# 🔧 Guia de Solução de Problemas - JAKA Monitor

## 📋 Índice de Problemas Comuns

1. [Erros de Instalação](#erros-de-instalação)
2. [Problemas de Conexão MQTT](#problemas-de-conexão-mqtt)
3. [Erros na Interface Gráfica](#erros-na-interface-gráfica)
4. [Problemas com Banco de Dados](#problemas-com-banco-de-dados)
5. [Erros na Geração de Relatórios](#erros-na-geração-de-relatórios)
6. [Performance e Otimização](#performance-e-otimização)

---

## 1. Erros de Instalação

### ❌ "Python não é reconhecido"
**Causa**: Python não está instalado ou não está no PATH

**Solução**:
```powershell
# Baixar Python de: https://www.python.org/downloads/
# Durante instalação, marcar "Add Python to PATH"

# Verificar instalação:
python --version
```

### ❌ "pip install falha com erro de permissão"
**Causa**: Falta de permissões administrativas

**Solução**:
```powershell
# Executar PowerShell como Administrador
# OU usar flag --user
pip install -r requirements.txt --user
```

### ❌ "Erro ao instalar PyQt5"
**Causa**: Falta de compiladores C++ no Windows

**Solução**:
```powershell
# Instalar versão pré-compilada
pip install PyQt5 --prefer-binary

# Se ainda falhar, instalar Visual C++ Build Tools:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### ❌ "ModuleNotFoundError: No module named 'paho'"
**Causa**: Dependências não instaladas

**Solução**:
```powershell
# Ativar ambiente virtual primeiro
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

---

## 2. Problemas de Conexão MQTT

### ❌ "Falha na conexão: Servidor indisponível"
**Causa**: Broker MQTT não está acessível

**Diagnóstico**:
```powershell
# Testar conectividade
ping 147.1.5.238

# Testar porta MQTT
Test-NetConnection 147.1.5.238 -Port 1883
```

**Soluções**:
1. Verificar se broker está rodando
2. Verificar firewall
3. Confirmar IP correto em `config.py`

### ❌ "Falha na conexão: Usuário/senha incorretos"
**Causa**: Credenciais inválidas

**Solução**:
```python
# Editar config.py
MQTT_USERNAME = "seu_usuario"  # Verificar com admin do broker
MQTT_PASSWORD = "sua_senha"
```

### ❌ "Conectado mas sem mensagens"
**Causa**: Tópico MQTT incorreto

**Diagnóstico**:
```powershell
# Usar mosquitto_sub para verificar tópico
mosquitto_sub -h 147.1.5.238 -u mqtt -P rede@123 -t "jaka/#" -v
```

**Solução**:
```python
# Ajustar tópico em config.py
MQTT_TOPIC = "jaka/monitor"  # Confirmar com seu sistema
```

### ❌ "Desconexões frequentes"
**Causa**: Rede instável ou keepalive muito curto

**Solução**:
```python
# Aumentar keepalive em config.py
MQTT_KEEPALIVE = 120  # De 60 para 120 segundos
```

---

## 3. Erros na Interface Gráfica

### ❌ "QApplication: no such file or directory"
**Causa**: PyQt5 não instalado corretamente

**Solução**:
```powershell
pip uninstall PyQt5
pip install PyQt5==5.15.9
```

### ❌ "Interface congela ao receber dados"
**Causa**: Thread MQTT travado ou processamento pesado

**Solução Temporária**:
```python
# Aumentar intervalo de salvamento em config.py
SAVE_INTERVAL = 50  # De 10 para 50
```

**Solução Permanente**:
- Verificar logs em `logs/`
- Reiniciar aplicação

### ❌ "Botões não respondem"
**Causa**: Erro não tratado travou a UI

**Diagnóstico**:
```powershell
# Verificar último log
Get-Content logs/system_*.log -Tail 50
```

**Solução**:
- Fechar e reabrir aplicação
- Verificar erro nos logs
- Reportar bug se persistir

### ❌ "Gráficos não aparecem"
**Causa**: Matplotlib não configurado corretamente

**Solução**:
```powershell
pip install matplotlib --upgrade
```

---

## 4. Problemas com Banco de Dados

### ❌ "Database is locked"
**Causa**: Múltiplas instâncias ou arquivo corrompido

**Solução**:
```powershell
# Fechar todas as instâncias do sistema
# Se persistir, deletar e recriar:
Remove-Item data/jaka_monitor.db
# Sistema recriará automaticamente
```

### ❌ "Banco de dados muito grande"
**Causa**: Muitos dados acumulados

**Diagnóstico**:
```powershell
# Verificar tamanho
Get-ChildItem data/jaka_monitor.db | Select-Object Length
```

**Solução**:
```powershell
# Fazer backup
Copy-Item data/jaka_monitor.db data/jaka_monitor_backup.db

# Limpar dados antigos (manual via SQL):
sqlite3 data/jaka_monitor.db
DELETE FROM robot_data WHERE timestamp < datetime('now', '-7 days');
VACUUM;
```

### ❌ "Erro ao consultar dados"
**Causa**: Corrupção de dados

**Solução**:
```powershell
# Verificar integridade
sqlite3 data/jaka_monitor.db "PRAGMA integrity_check;"

# Se corrompido, restaurar backup ou recriar
```

---

## 5. Erros na Geração de Relatórios

### ❌ "Erro ao gerar PDF: No such file 'reportlab'"
**Causa**: ReportLab não instalado

**Solução**:
```powershell
pip install reportlab
```

### ❌ "PDF vazio ou incompleto"
**Causa**: Sem dados no período selecionado

**Diagnóstico**:
```python
# Verificar dados disponíveis
python test_system.py
```

**Solução**:
- Coletar mais dados antes de gerar relatório
- Ou ajustar período (24h -> 1h)

### ❌ "Gráficos não aparecem no PDF"
**Causa**: Arquivos temporários de gráficos não gerados

**Solução**:
```powershell
# Verificar permissões na pasta reports
icacls reports

# Criar manualmente se necessário
mkdir reports
```

### ❌ "Erro ao exportar Excel"
**Causa**: Openpyxl não instalado

**Solução**:
```powershell
pip install openpyxl pandas
```

---

## 6. Performance e Otimização

### ⚠️ "Sistema está lento"
**Causas Possíveis**:
1. Banco de dados muito grande
2. Muitos eventos sendo gerados
3. Intervalo de salvamento muito baixo

**Soluções**:

**1. Otimizar Banco de Dados**:
```powershell
sqlite3 data/jaka_monitor.db "VACUUM; ANALYZE;"
```

**2. Aumentar Intervalo de Salvamento**:
```python
# Em config.py
SAVE_INTERVAL = 20  # De 10 para 20
```

**3. Reduzir Janela de Análise**:
```python
# Em config.py
ANALYSIS_WINDOW = 30  # De 60 para 30 segundos
```

### ⚠️ "Muita memória sendo usada"
**Causa**: Histórico muito grande no analisador

**Solução**:
```python
# Em modules/analyzer.py, linha ~35
self.history = deque(maxlen=50)  # De 100 para 50
```

### ⚠️ "CPU em 100%"
**Causa**: Loop de processamento muito intenso

**Solução**:
```python
# Em main_gui.py, linha ~539
self.ui_timer.start(2000)  # De 1000 para 2000ms
```

---

## 🔍 Ferramentas de Diagnóstico

### Verificar Logs
```powershell
# Ver últimas 50 linhas do log
Get-Content logs/system_*.log -Tail 50

# Buscar erros
Select-String -Path "logs/*.log" -Pattern "ERROR"
```

### Testar Sistema Completo
```powershell
python test_system.py
```

### Testar Apenas Banco de Dados
```python
from modules.database import DatabaseManager
db = DatabaseManager("data/jaka_monitor.db")
stats = db.get_statistics(hours=24)
print(stats)
db.close()
```

### Verificar Conexão MQTT Manualmente
```powershell
# Instalar mosquitto clients
# Testar subscrição:
mosquitto_sub -h 147.1.5.238 -p 1883 -u mqtt -P "rede@123" -t "jaka/monitor"
```

---

## 📞 Checklist de Diagnóstico

Antes de reportar um problema, verificar:

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual ativado
- [ ] Todas as dependências instaladas (`pip list`)
- [ ] config.py existe e está configurado
- [ ] Conexão de rede com broker MQTT
- [ ] Logs verificados em `logs/`
- [ ] Espaço em disco suficiente
- [ ] Permissões de escrita nas pastas
- [ ] Firewall não bloqueando porta 1883
- [ ] Broker MQTT está rodando

---

## 🆘 Comandos Úteis

### Reinstalação Completa
```powershell
# Deletar ambiente virtual
Remove-Item -Recurse -Force venv

# Recriar
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Resetar Sistema
```powershell
# Backup de dados importantes
Copy-Item data/jaka_monitor.db backup/

# Limpar tudo
Remove-Item data/*.db
Remove-Item reports/*
Remove-Item logs/*

# Sistema recriará estrutura na próxima execução
```

### Verificar Dependências
```powershell
pip list | Select-String "paho|PyQt5|pandas|matplotlib|reportlab|openpyxl"
```

---

## 💡 Dicas de Uso

1. **Sempre ative o ambiente virtual antes de executar**
2. **Verifique os logs regularmente**
3. **Faça backup do banco de dados periodicamente**
4. **Ajuste thresholds conforme seu robô específico**
5. **Use o simulador para testar antes de usar com robô real**

---

## 📚 Recursos Adicionais

- **Documentação Completa**: README.md
- **Guia Rápido**: QUICKSTART.md
- **Resumo do Sistema**: SISTEMA_RESUMO.md
- **Logs do Sistema**: `logs/system_*.log`

---

**Última Atualização**: Outubro 2025  
**Versão**: 1.0.0
