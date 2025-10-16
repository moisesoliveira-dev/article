# Sistema de Monitoramento e Análise - Robô JAKA

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema completo de monitoramento em tempo real para robôs JAKA via MQTT, com detecção de anomalias, análise de desgaste e geração automática de relatórios científicos.

## 📋 Características

### Monitoramento em Tempo Real
- ✅ Conexão MQTT para recepção de dados do robô
- ✅ Interface gráfica intuitiva com PyQt5
- ✅ Visualização em tempo real de todas as juntas
- ✅ Dashboard com score de saúde do robô (0-100%)

### Detecção de Anomalias (Sem IA)
- ✅ Análise de temperatura das juntas e do robô
- ✅ Monitoramento de corrente e sobrecarga
- ✅ Detecção de desvios de posição (folgas mecânicas)
- ✅ Análise de torque e desgaste
- ✅ Verificação de voltagem
- ✅ Análise de tendências temporais

### Sistema de Criticidade Temporal
- ✅ **INFO** (0-30s): Anomalia recente
- ✅ **WARNING** (30-120s): Anomalia persistente
- ✅ **CRITICAL** (120-300s): Situação grave
- ✅ **EMERGENCY** (>300s): Ação imediata necessária

### Banco de Dados
- ✅ SQLite para armazenamento histórico
- ✅ Indexação otimizada para consultas rápidas
- ✅ Estatísticas agregadas para análise

### Geração de Relatórios
- ✅ **Relatório PDF Completo**:
  - Resumo executivo de eventos
  - Estatísticas detalhadas por junta
  - Gráficos de evolução temporal
  - Lista completa de anomalias
  
- ✅ **Exportação Excel**:
  - Dados brutos das juntas
  - Histórico de eventos
  - Estatísticas calculadas
  
- ✅ **Gráficos Inclusos**:
  - Evolução de temperatura
  - Evolução de corrente
  - Evolução de torque/carga
  - Linhas de threshold destacadas

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Passo a Passo

1. **Clone ou baixe o projeto**
```bash
cd jaka_monitor
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## 📊 Uso

### Iniciar o Sistema

```bash
python main_gui.py
```

### Interface Principal

1. **Iniciar Monitoramento**: Clique no botão "Iniciar Monitoramento"
2. **Dashboard**: Visualize status em tempo real
3. **Juntas**: Tabela detalhada de todas as 6 juntas
4. **Eventos**: Histórico de anomalias detectadas
5. **Relatórios**: Gere PDFs e exporte para Excel

### Configuração MQTT

Edite o arquivo `config.py` para ajustar os parâmetros de conexão:

```python
MQTT_BROKER = "147.1.5.238"      # Endereço do broker
MQTT_PORT = 1883                 # Porta MQTT
MQTT_TOPIC = "jaka/monitor"      # Tópico de dados
MQTT_USERNAME = "mqtt"           # Usuário
MQTT_PASSWORD = "rede@123"       # Senha
```

### Ajustar Thresholds

Os limites de detecção podem ser customizados em `config.py`:

```python
THRESHOLDS = {
    "joint_temperature_warning": 40.0,    # °C
    "joint_temperature_critical": 50.0,   # °C
    "joint_current_warning": 2.0,         # A
    "joint_current_critical": 3.0,        # A
    # ... outros parâmetros
}
```

## 📁 Estrutura do Projeto

```
jaka_monitor/
│
├── config.py                 # Configurações centralizadas
├── main_gui.py              # Interface gráfica principal
├── requirements.txt         # Dependências Python
├── README.md               # Este arquivo
│
├── modules/                # Módulos do sistema
│   ├── __init__.py
│   ├── mqtt_client.py     # Cliente MQTT
│   ├── database.py        # Gerenciamento do banco de dados
│   ├── analyzer.py        # Detecção de anomalias
│   └── report_generator.py # Geração de relatórios
│
├── data/                   # Banco de dados (gerado automaticamente)
│   └── jaka_monitor.db
│
├── reports/                # Relatórios gerados (PDF/Excel)
│
└── logs/                   # Logs do sistema
```

## 🔍 Parâmetros Monitorados

### Por Junta (6 juntas):
- Posição (graus)
- Velocidade (rad/s)
- Corrente (A)
- Temperatura (°C)
- Voltagem (V)
- Torque/Carga
- Desvio de posição

### Sistema Geral:
- Temperatura interna do robô
- Temperatura ambiente
- Posição TCP (X, Y, Z, Rx, Ry, Rz)
- Estados (emergency_stop, protective_stop, etc.)
- I/O digital e analógico
- Comunicações industriais (Modbus, PROFINET, EtherNet/IP)

## 📈 Análise de Desgaste

O sistema detecta sinais de desgaste através de:

1. **Aumento de Temperatura**: Indica atrito excessivo ou sobrecarga
2. **Corrente Elevada**: Sugere resistência mecânica aumentada
3. **Desvio de Posição**: Possível folga ou desgaste em engrenagens
4. **Torque Anormal**: Pode indicar desgaste de componentes
5. **Tendências Temporais**: Aumento gradual de parâmetros

### Níveis de Criticidade

A criticidade aumenta automaticamente baseada no tempo de persistência da anomalia:

- ⚪ **INFO** (0-30s): Monitorar
- 🟡 **WARNING** (30-120s): Atenção necessária
- 🟠 **CRITICAL** (120-300s): Problema grave
- 🔴 **EMERGENCY** (>300s): Ação imediata

## 📄 Relatórios

### Relatório PDF
Inclui:
- Cabeçalho com informações do sistema
- Resumo de eventos por severidade
- Tabela de estatísticas das juntas
- Gráficos de evolução temporal
- Lista detalhada de eventos

### Exportação Excel
Inclui 3 abas:
1. **Dados das Juntas**: Todos os dados brutos
2. **Eventos**: Histórico completo de anomalias
3. **Estatísticas**: Médias e máximos por junta

## 🛠️ Solução de Problemas

### Erro de Conexão MQTT
- Verifique se o broker está acessível
- Confirme usuário e senha
- Teste conectividade de rede

### Problemas com PyQt5
```bash
# Windows - pode precisar de ferramentas C++
pip install PyQt5 --prefer-binary
```

### Banco de Dados Corrompido
```bash
# Deletar e será recriado
rm data/jaka_monitor.db
```

## 🎯 Uso para Artigos Científicos

Este sistema foi projetado especificamente para pesquisa acadêmica:

1. **Dados Comprováveis**: Todos os dados são armazenados com timestamp
2. **Gráficos Científicos**: Alta resolução (150 DPI) prontos para publicação
3. **Exportação Flexível**: Excel para análises estatísticas adicionais
4. **Metodologia Clara**: Detecção baseada em regras (não-IA) é explicável
5. **Rastreabilidade**: Logs completos de todas as operações

### Exemplo de Metodologia para Artigo

> "O sistema de monitoramento coleta dados em tempo real via MQTT a cada X segundos. 
> A detecção de anomalias utiliza thresholds baseados nas especificações do fabricante 
> (temperatura crítica: 50°C, corrente crítica: 3A). A criticidade é escalada 
> temporalmente, classificando anomalias persistentes por mais de 300 segundos como 
> emergenciais. Dados são armazenados em banco SQLite para análise histórica."

## 📚 Referências

- [Documentação JAKA](https://www.jaka.com/)
- [Protocolo MQTT](https://mqtt.org/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

## 📝 Licença

MIT License - Livre para uso acadêmico e comercial.

## 👤 Autor

Sistema desenvolvido para monitoramento e análise de robôs industriais JAKA.

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique os logs em `logs/`
2. Consulte a documentação no arquivo `jaka_robot_data.md`
3. Revise as configurações em `config.py`

---

**Versão**: 1.0.0  
**Data**: Outubro 2025  
**Status**: ✅ Produção
