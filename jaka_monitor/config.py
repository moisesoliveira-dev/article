"""
Configurações do Sistema de Monitoramento JAKA
"""
import os

# ==================== MQTT Configuration ====================
MQTT_BROKER = "147.1.5.238"
MQTT_PORT = 1883
MQTT_TOPIC = "jaka/monitor"
MQTT_CLIENT_ID = "jaka-monitor-system"
MQTT_USERNAME = "mqtt"
MQTT_PASSWORD = "rede@@123"
MQTT_QOS = 1
MQTT_KEEPALIVE = 60

# ==================== Database Configuration ====================
DB_PATH = os.path.join("data", "jaka_monitor.db")

# ==================== Analysis Configuration ====================
# Thresholds para detecção de anomalias
THRESHOLDS = {
    # Temperatura das juntas (°C)
    "joint_temperature_warning": 40.0,
    "joint_temperature_critical": 50.0,
    
    # Temperatura interna do robô (°C)
    "robot_temp_warning": 45.0,
    "robot_temp_critical": 55.0,
    
    # Corrente das juntas (A)
    "joint_current_warning": 2.0,
    "joint_current_critical": 3.0,
    
    # Velocidade das juntas (rad/s)
    "joint_velocity_max": 0.6,
    
    # Variação de posição (graus)
    "position_deviation_warning": 0.5,
    "position_deviation_critical": 1.0,
    
    # Torque/Carga
    "joint_torque_warning": 3.0,
    "joint_torque_critical": 3.5,
    
    # Voltagem (V)
    "voltage_low": 48.0,
    "voltage_high": 52.0,
}

# ==================== Criticality Levels ====================
# Tempo de persistência da anomalia (segundos) para aumentar criticidade
CRITICALITY_TIME_THRESHOLDS = {
    "info": 0,           # 0-30s: Informativo
    "warning": 30,       # 30-120s: Alerta
    "critical": 120,     # 120-300s: Crítico
    "emergency": 300,    # >300s: Emergência
}

# ==================== Report Configuration ====================
REPORTS_DIR = "reports"
LOGS_DIR = "logs"

# Configurações de gráficos
PLOT_STYLE = "seaborn-v0_8-darkgrid"
PLOT_DPI = 150
PLOT_FIGSIZE = (12, 8)

# ==================== Monitoring Configuration ====================
# Janela de análise (segundos)
ANALYSIS_WINDOW = 60  # Analisar últimos 60 segundos

# Intervalo de salvamento no banco (mensagens)
SAVE_INTERVAL = 10  # Salvar a cada 10 mensagens

# ==================== System Info ====================
SYSTEM_VERSION = "1.0.0"
SYSTEM_NAME = "JAKA Robot Monitoring & Analysis System"
