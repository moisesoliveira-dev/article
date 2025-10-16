"""
Módulo de Análise de Dados e Detecção de Anomalias
Detecta padrões de desgaste sem uso de IA
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque
import statistics
import config


class AnomalyDetector:
    """Detecta anomalias e sinais de desgaste nos dados do robô"""
    
    def __init__(self):
        """Inicializa o detector de anomalias"""
        # Histórico recente para análise de tendências
        self.history = deque(maxlen=100)
        
        # Rastreamento de anomalias ativas
        self.active_anomalies = {}  # {anomaly_key: start_time}
        
        # Baseline para comparação
        self.baseline = {
            'joint_temps': [23.0] * 6,
            'joint_currents': [0.0] * 6,
            'robot_temp': 26.0,
        }
        
    def analyze(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analisa os dados do robô e detecta anomalias
        
        Args:
            data: Dados completos do robô
            
        Returns:
            Lista de anomalias detectadas
        """
        anomalies = []
        
        # Adicionar aos histórico
        self.history.append({
            'timestamp': datetime.now(),
            'data': data
        })
        
        # Análise de temperatura
        anomalies.extend(self._check_temperatures(data))
        
        # Análise de corrente
        anomalies.extend(self._check_currents(data))
        
        # Análise de voltagem
        anomalies.extend(self._check_voltages(data))
        
        # Análise de torque
        anomalies.extend(self._check_torques(data))
        
        # Análise de posição
        anomalies.extend(self._check_position_deviation(data))
        
        # Análise de estados críticos
        anomalies.extend(self._check_critical_states(data))
        
        # Análise de tendências
        anomalies.extend(self._check_trends())
        
        # Atualizar baseline
        self._update_baseline(data)
        
        return anomalies
    
    def _check_temperatures(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica temperaturas das juntas e do robô"""
        anomalies = []
        monitor_data = data.get("monitor_data", [])
        
        # Temperatura do robô
        if len(monitor_data) > 2:
            robot_temp = monitor_data[2]
            if robot_temp >= config.THRESHOLDS["robot_temp_critical"]:
                anomalies.append({
                    'type': 'high_robot_temperature',
                    'severity': 'critical',
                    'value': robot_temp,
                    'threshold': config.THRESHOLDS["robot_temp_critical"],
                    'description': f'Temperatura do robô crítica: {robot_temp:.1f}°C'
                })
            elif robot_temp >= config.THRESHOLDS["robot_temp_warning"]:
                anomalies.append({
                    'type': 'high_robot_temperature',
                    'severity': 'warning',
                    'value': robot_temp,
                    'threshold': config.THRESHOLDS["robot_temp_warning"],
                    'description': f'Temperatura do robô elevada: {robot_temp:.1f}°C'
                })
        
        # Temperaturas das juntas
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            for i, joint_data in enumerate(monitor_data[5]):
                if isinstance(joint_data, list) and len(joint_data) > 1:
                    temp = joint_data[1]
                    joint_num = i + 1
                    
                    if temp >= config.THRESHOLDS["joint_temperature_critical"]:
                        anomalies.append({
                            'type': 'high_joint_temperature',
                            'severity': 'critical',
                            'joint': joint_num,
                            'value': temp,
                            'threshold': config.THRESHOLDS["joint_temperature_critical"],
                            'description': f'Junta {joint_num}: Temperatura crítica {temp:.1f}°C'
                        })
                    elif temp >= config.THRESHOLDS["joint_temperature_warning"]:
                        anomalies.append({
                            'type': 'high_joint_temperature',
                            'severity': 'warning',
                            'joint': joint_num,
                            'value': temp,
                            'threshold': config.THRESHOLDS["joint_temperature_warning"],
                            'description': f'Junta {joint_num}: Temperatura elevada {temp:.1f}°C'
                        })
        
        return anomalies
    
    def _check_currents(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica correntes das juntas"""
        anomalies = []
        monitor_data = data.get("monitor_data", [])
        
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            for i, joint_data in enumerate(monitor_data[5]):
                if isinstance(joint_data, list) and len(joint_data) > 0:
                    current = abs(joint_data[0])
                    joint_num = i + 1
                    
                    if current >= config.THRESHOLDS["joint_current_critical"]:
                        anomalies.append({
                            'type': 'high_joint_current',
                            'severity': 'critical',
                            'joint': joint_num,
                            'value': current,
                            'threshold': config.THRESHOLDS["joint_current_critical"],
                            'description': f'Junta {joint_num}: Corrente crítica {current:.2f}A (possível sobrecarga)'
                        })
                    elif current >= config.THRESHOLDS["joint_current_warning"]:
                        anomalies.append({
                            'type': 'high_joint_current',
                            'severity': 'warning',
                            'joint': joint_num,
                            'value': current,
                            'threshold': config.THRESHOLDS["joint_current_warning"],
                            'description': f'Junta {joint_num}: Corrente elevada {current:.2f}A'
                        })
        
        return anomalies
    
    def _check_voltages(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica voltagens das juntas"""
        anomalies = []
        monitor_data = data.get("monitor_data", [])
        
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            for i, joint_data in enumerate(monitor_data[5]):
                if isinstance(joint_data, list) and len(joint_data) > 2:
                    voltage = joint_data[2]
                    joint_num = i + 1
                    
                    if voltage < config.THRESHOLDS["voltage_low"]:
                        anomalies.append({
                            'type': 'low_voltage',
                            'severity': 'warning',
                            'joint': joint_num,
                            'value': voltage,
                            'threshold': config.THRESHOLDS["voltage_low"],
                            'description': f'Junta {joint_num}: Voltagem baixa {voltage:.1f}V'
                        })
                    elif voltage > config.THRESHOLDS["voltage_high"]:
                        anomalies.append({
                            'type': 'high_voltage',
                            'severity': 'warning',
                            'joint': joint_num,
                            'value': voltage,
                            'threshold': config.THRESHOLDS["voltage_high"],
                            'description': f'Junta {joint_num}: Voltagem alta {voltage:.1f}V'
                        })
        
        return anomalies
    
    def _check_torques(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica torques/cargas das juntas"""
        anomalies = []
        monitor_data = data.get("monitor_data", [])
        
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            for i, joint_data in enumerate(monitor_data[5]):
                if isinstance(joint_data, list) and len(joint_data) > 7:
                    torque = abs(joint_data[7])
                    joint_num = i + 1
                    
                    if torque >= config.THRESHOLDS["joint_torque_critical"]:
                        anomalies.append({
                            'type': 'high_torque',
                            'severity': 'critical',
                            'joint': joint_num,
                            'value': torque,
                            'threshold': config.THRESHOLDS["joint_torque_critical"],
                            'description': f'Junta {joint_num}: Torque crítico {torque:.2f} (possível desgaste mecânico)'
                        })
                    elif torque >= config.THRESHOLDS["joint_torque_warning"]:
                        anomalies.append({
                            'type': 'high_torque',
                            'severity': 'warning',
                            'joint': joint_num,
                            'value': torque,
                            'threshold': config.THRESHOLDS["joint_torque_warning"],
                            'description': f'Junta {joint_num}: Torque elevado {torque:.2f}'
                        })
        
        return anomalies
    
    def _check_position_deviation(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica desvios entre posição comandada e real"""
        anomalies = []
        
        joint_position = data.get("joint_position", [])
        joint_actual = data.get("joint_actual_position", [])
        
        for i in range(min(len(joint_position), len(joint_actual))):
            deviation = abs(joint_position[i] - joint_actual[i])
            joint_num = i + 1
            
            if deviation >= config.THRESHOLDS["position_deviation_critical"]:
                anomalies.append({
                    'type': 'position_deviation',
                    'severity': 'critical',
                    'joint': joint_num,
                    'value': deviation,
                    'threshold': config.THRESHOLDS["position_deviation_critical"],
                    'description': f'Junta {joint_num}: Desvio de posição crítico {deviation:.3f}° (possível folga mecânica)'
                })
            elif deviation >= config.THRESHOLDS["position_deviation_warning"]:
                anomalies.append({
                    'type': 'position_deviation',
                    'severity': 'warning',
                    'joint': joint_num,
                    'value': deviation,
                    'threshold': config.THRESHOLDS["position_deviation_warning"],
                    'description': f'Junta {joint_num}: Desvio de posição {deviation:.3f}°'
                })
        
        return anomalies
    
    def _check_critical_states(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica estados críticos do sistema"""
        anomalies = []
        
        if data.get("emergency_stop", 0) == 1:
            anomalies.append({
                'type': 'emergency_stop',
                'severity': 'emergency',
                'description': 'PARADA DE EMERGÊNCIA ATIVADA'
            })
        
        if data.get("protective_stop", 0) == 1:
            anomalies.append({
                'type': 'protective_stop',
                'severity': 'critical',
                'description': 'Parada de proteção ativada'
            })
        
        if data.get("on_soft_limit", 0) == 1:
            anomalies.append({
                'type': 'soft_limit',
                'severity': 'warning',
                'description': 'Limite de software atingido'
            })
        
        if not data.get("enabled", False):
            anomalies.append({
                'type': 'robot_disabled',
                'severity': 'info',
                'description': 'Robô desabilitado'
            })
        
        return anomalies
    
    def _check_trends(self) -> List[Dict[str, Any]]:
        """Analisa tendências de aumento em parâmetros críticos"""
        anomalies = []
        
        if len(self.history) < 30:  # Precisa de pelo menos 30 amostras
            return anomalies
        
        # Analisar tendência de temperatura
        recent_temps = []
        for entry in list(self.history)[-30:]:
            monitor_data = entry['data'].get('monitor_data', [])
            if len(monitor_data) > 2:
                recent_temps.append(monitor_data[2])
        
        if len(recent_temps) >= 30:
            # Verificar se há tendência de aumento
            first_half_avg = statistics.mean(recent_temps[:15])
            second_half_avg = statistics.mean(recent_temps[15:])
            
            if second_half_avg > first_half_avg + 3:  # Aumento de 3°C
                anomalies.append({
                    'type': 'temperature_trend',
                    'severity': 'warning',
                    'value': second_half_avg,
                    'description': f'Tendência de aumento de temperatura detectada: {first_half_avg:.1f}°C → {second_half_avg:.1f}°C'
                })
        
        return anomalies
    
    def _update_baseline(self, data: Dict[str, Any]):
        """Atualiza baseline com valores normais (quando não há anomalias severas)"""
        monitor_data = data.get("monitor_data", [])
        
        # Só atualiza baseline se não houver estados críticos
        if data.get("emergency_stop", 0) == 0 and data.get("protective_stop", 0) == 0:
            # Atualizar temperatura do robô
            if len(monitor_data) > 2:
                robot_temp = monitor_data[2]
                if robot_temp < config.THRESHOLDS["robot_temp_warning"]:
                    self.baseline['robot_temp'] = robot_temp
    
    def calculate_criticality(self, anomaly_key: str, current_severity: str) -> Tuple[str, float]:
        """
        Calcula o nível de criticidade baseado na duração da anomalia
        
        Args:
            anomaly_key: Identificador único da anomalia
            current_severity: Severidade atual
            
        Returns:
            Tupla (severidade ajustada, duração em segundos)
        """
        now = datetime.now()
        
        if anomaly_key not in self.active_anomalies:
            # Nova anomalia
            self.active_anomalies[anomaly_key] = now
            return current_severity, 0.0
        
        # Anomalia persistente
        start_time = self.active_anomalies[anomaly_key]
        duration = (now - start_time).total_seconds()
        
        # Escalonar severidade baseado na duração
        if duration >= config.CRITICALITY_TIME_THRESHOLDS["emergency"]:
            adjusted_severity = "emergency"
        elif duration >= config.CRITICALITY_TIME_THRESHOLDS["critical"]:
            adjusted_severity = "critical"
        elif duration >= config.CRITICALITY_TIME_THRESHOLDS["warning"]:
            adjusted_severity = "warning"
        else:
            adjusted_severity = current_severity
        
        return adjusted_severity, duration
    
    def clear_anomaly(self, anomaly_key: str):
        """Remove uma anomalia da lista de ativas"""
        if anomaly_key in self.active_anomalies:
            del self.active_anomalies[anomaly_key]
    
    def get_health_score(self, data: Dict[str, Any]) -> float:
        """
        Calcula um score de saúde geral do robô (0-100)
        
        Args:
            data: Dados do robô
            
        Returns:
            Score de saúde (100 = perfeito, 0 = crítico)
        """
        score = 100.0
        
        # Penalizações por temperatura
        monitor_data = data.get("monitor_data", [])
        if len(monitor_data) > 2:
            robot_temp = monitor_data[2]
            if robot_temp > config.THRESHOLDS["robot_temp_warning"]:
                score -= 10
            if robot_temp > config.THRESHOLDS["robot_temp_critical"]:
                score -= 20
        
        # Penalizações por juntas
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            for joint_data in monitor_data[5]:
                if isinstance(joint_data, list) and len(joint_data) > 7:
                    # Temperatura
                    if joint_data[1] > config.THRESHOLDS["joint_temperature_warning"]:
                        score -= 3
                    if joint_data[1] > config.THRESHOLDS["joint_temperature_critical"]:
                        score -= 5
                    
                    # Corrente
                    if abs(joint_data[0]) > config.THRESHOLDS["joint_current_warning"]:
                        score -= 2
                    if abs(joint_data[0]) > config.THRESHOLDS["joint_current_critical"]:
                        score -= 5
                    
                    # Torque
                    if abs(joint_data[7]) > config.THRESHOLDS["joint_torque_warning"]:
                        score -= 2
                    if abs(joint_data[7]) > config.THRESHOLDS["joint_torque_critical"]:
                        score -= 5
        
        # Penalizações por estados críticos
        if data.get("emergency_stop", 0) == 1:
            score -= 50
        if data.get("protective_stop", 0) == 1:
            score -= 30
        
        return max(0.0, min(100.0, score))
