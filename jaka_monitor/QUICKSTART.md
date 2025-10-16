# Guia de Início Rápido - Sistema JAKA Monitor

## ⚡ Instalação Rápida (Windows)

1. **Abra o PowerShell nesta pasta**
2. **Execute os comandos abaixo:**

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar o sistema
python main_gui.py
```

## 🎯 Primeiro Uso

### 1. Verificar Conexão MQTT

Antes de iniciar, confirme em `config.py`:
- Broker: `147.1.5.238`
- Porta: `1883`
- Tópico: `jaka/monitor`

### 2. Iniciar Interface

```powershell
python main_gui.py
```

### 3. Conectar ao Robô

1. Clique em **"Iniciar Monitoramento"**
2. Aguarde a conexão (indicador ficará verde)
3. Dados começarão a aparecer automaticamente

### 4. Testar sem Robô Real

Se não tiver acesso ao robô JAKA:

```powershell
# Em um terminal separado, execute o simulador
python test_simulator.py
```

Isso enviará dados simulados para o sistema testar.

## 📊 Funcionalidades Principais

### Dashboard (Aba 1)
- ✅ Status de conexão em tempo real
- ✅ Score de saúde do robô (0-100%)
- ✅ Informações gerais (ID, nome, temperatura)
- ✅ Posição TCP atual
- ✅ Log de eventos em tempo real

### Juntas (Aba 2)
- ✅ Tabela com todas as 6 juntas
- ✅ Valores destacados em cores:
  - 🟢 Verde = Normal
  - 🟡 Amarelo = Alerta
  - 🔴 Vermelho = Crítico

### Eventos (Aba 3)
- ✅ Histórico de todas as anomalias
- ✅ Filtros por severidade
- ✅ Exportável

### Relatórios (Aba 4)
- ✅ **PDF Completo**: Gráficos + estatísticas + eventos
- ✅ **Excel**: Dados brutos para análise

## 🔧 Ajustes Comuns

### Mudar Intervalo de Salvamento

Em `config.py`:
```python
SAVE_INTERVAL = 10  # Salvar a cada 10 mensagens
```

### Ajustar Thresholds

Em `config.py`:
```python
THRESHOLDS = {
    "joint_temperature_warning": 40.0,   # Alterar conforme necessário
    "joint_temperature_critical": 50.0,
    # ...
}
```

### Alterar Janela de Análise

Em `config.py`:
```python
ANALYSIS_WINDOW = 60  # Segundos
```

## 📁 Onde Encontrar os Dados

- **Banco de Dados**: `data/jaka_monitor.db`
- **Relatórios PDF**: `reports/relatorio_completo_*.pdf`
- **Exportações Excel**: `reports/dados_exportados_*.xlsx`
- **Logs do Sistema**: `logs/system_*.log`
- **Gráficos Temporários**: `reports/*_graph_*.png`

## ❗ Problemas Comuns

### "Não consigo conectar ao MQTT"
- Verifique se o broker está acessível
- Teste com: `ping 147.1.5.238`
- Confirme usuário/senha em `config.py`

### "Interface não abre"
- Verifique instalação do PyQt5:
```powershell
pip install PyQt5 --force-reinstall
```

### "Erro ao gerar PDF"
- Instale reportlab:
```powershell
pip install reportlab --upgrade
```

### "ModuleNotFoundError"
- Certifique-se que o ambiente virtual está ativo
- Reinstale dependências:
```powershell
pip install -r requirements.txt --force-reinstall
```

## 🎓 Para Artigos Científicos

### Coletar Dados por 24h

1. Inicie o sistema
2. Deixe rodando
3. Após 24h, gere relatório PDF
4. Exporte Excel para análises adicionais

### Gráficos para Publicação

Os gráficos são gerados em alta resolução (150 DPI) e podem ser usados diretamente em papers.

### Dados Estatísticos

Acesse o banco de dados diretamente:
```python
import sqlite3
conn = sqlite3.connect('data/jaka_monitor.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM statistics")
```

## 📞 Checklist de Verificação

Antes de iniciar coleta de dados:

- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Conexão MQTT configurada
- [ ] Thresholds ajustados
- [ ] Espaço em disco suficiente (mín. 1GB)
- [ ] Sistema testado com simulador

## ⏱️ Tempo Estimado

- **Instalação**: 5 minutos
- **Configuração**: 10 minutos
- **Primeiro teste**: 2 minutos
- **Coleta 24h**: Automático

## 🚀 Próximos Passos

1. ✅ Instalar e testar com simulador
2. ✅ Conectar ao robô real
3. ✅ Coletar dados por período desejado
4. ✅ Gerar relatórios
5. ✅ Analisar resultados
6. ✅ Usar dados no artigo

---

**Dica**: Mantenha o sistema rodando em segundo plano para coleta contínua de dados!
