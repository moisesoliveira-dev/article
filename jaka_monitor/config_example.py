# Exemplo de Configuração - config.py
# Copie este arquivo para config.py e ajuste conforme necessário

# ==================== MQTT Configuration ====================
# Configurações da conexão MQTT com o robô JAKA

# Endereço do broker MQTT (servidor)
MQTT_BROKER = "147.1.5.238"  # Alterar para o IP do seu broker

# Porta do broker MQTT (padrão: 1883)
MQTT_PORT = 1883

# Tópico MQTT onde o robô publica os dados
MQTT_TOPIC = "jaka/monitor"

# ID único deste cliente MQTT
MQTT_CLIENT_ID = "jaka-monitor-system"

# Credenciais de autenticação
MQTT_USERNAME = "mqtt"       # Alterar se necessário
MQTT_PASSWORD = "rede@123"   # Alterar se necessário

# Quality of Service (0, 1 ou 2)
MQTT_QOS = 1

# Tempo de keepalive (segundos)
MQTT_KEEPALIVE = 60

# ==================== Database Configuration ====================
# Banco de dados SQLite para armazenar histórico

import os
DB_PATH = os.path.join("data", "jaka_monitor.db")

# ==================== Analysis Configuration ====================
# Limites (thresholds) para detecção de anomalias
# Ajuste conforme especificações do seu robô

THRESHOLDS = {
    # Temperatura das juntas (°C)
    "joint_temperature_warning": 40.0,    # Alerta se >= 40°C
    "joint_temperature_critical": 50.0,   # Crítico se >= 50°C
    
    # Temperatura interna do robô (°C)
    "robot_temp_warning": 45.0,
    "robot_temp_critical": 55.0,
    
    # Corrente das juntas (Amperes)
    "joint_current_warning": 2.0,         # Alerta se >= 2.0A
    "joint_current_critical": 3.0,        # Crítico se >= 3.0A
    
    # Velocidade máxima das juntas (rad/s)
    "joint_velocity_max": 0.6,
    
    # Desvio de posição (graus) - diferença entre comando e real
    "position_deviation_warning": 0.5,    # Possível folga mecânica
    "position_deviation_critical": 1.0,   # Folga significativa
    
    # Torque/Carga das juntas
    "joint_torque_warning": 3.0,
    "joint_torque_critical": 3.5,
    
    # Faixa de voltagem normal (Volts)
    "voltage_low": 48.0,    # Alerta se < 48V
    "voltage_high": 52.0,   # Alerta se > 52V
}

# ==================== Criticality Levels ====================
# Tempo de persistência da anomalia (segundos) para aumentar criticidade
# Quanto mais tempo a anomalia persistir, maior a criticidade

CRITICALITY_TIME_THRESHOLDS = {
    "info": 0,           # 0-30s: Informativo (situação normal)
    "warning": 30,       # 30-120s: Alerta (requer atenção)
    "critical": 120,     # 120-300s: Crítico (problema grave)
    "emergency": 300,    # >300s: Emergência (ação imediata)
}

# ==================== Report Configuration ====================
# Configurações de relatórios e gráficos

REPORTS_DIR = "reports"  # Pasta onde relatórios serão salvos
LOGS_DIR = "logs"        # Pasta de logs do sistema

# Configurações de gráficos
PLOT_STYLE = "seaborn-v0_8-darkgrid"  # Estilo dos gráficos
PLOT_DPI = 150                         # Resolução (DPI) para publicação
PLOT_FIGSIZE = (12, 8)                 # Tamanho padrão (polegadas)

# ==================== Monitoring Configuration ====================
# Parâmetros do monitoramento

# Janela de análise (segundos) - quanto de histórico usar nas análises
ANALYSIS_WINDOW = 60

# Intervalo de salvamento no banco (número de mensagens)
# Salva no banco a cada N mensagens recebidas
SAVE_INTERVAL = 10

# ==================== System Info ====================
SYSTEM_VERSION = "1.0.0"
SYSTEM_NAME = "JAKA Robot Monitoring & Analysis System"

# ==================== Notas de Configuração ====================
# 
# COMO USAR ESTE ARQUIVO:
# 
# 1. Copie este arquivo como "config.py"
# 2. Ajuste os valores conforme sua infraestrutura
# 3. Salve e execute o sistema
#
# VALORES IMPORTANTES A VERIFICAR:
# - MQTT_BROKER: IP do broker MQTT
# - MQTT_TOPIC: Tópico onde o robô publica
# - THRESHOLDS: Limites conforme manual do robô
# - SAVE_INTERVAL: Ajustar conforme frequência de dados
#
# THRESHOLDS SUGERIDOS (baseados em robôs industriais típicos):
# - Temperatura junta: 40°C (warning), 50°C (critical)
# - Corrente: 2A (warning), 3A (critical)
# - Desvio posição: 0.5° (warning), 1.0° (critical)
#
# CRITICIDADE TEMPORAL:
# - 0-30s: Normal
# - 30-120s: Requer atenção
# - 120-300s: Problema sério
# - >300s: Emergência
#
