"""
Simulador de Cenários de Falhas - Robô JAKA
Gera dados realistas de diferentes tipos de falhas para análise científica

Autor: Sistema JAKA Monitor
Data: Outubro 2025
Propósito: Geração de dados para artigos científicos
"""

import json
import time
import random
import math
from datetime import datetime
import paho.mqtt.client as mqtt
from typing import Dict, List, Callable
import argparse

# Importar configurações
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class FaultScenario:
    """Classe base para cenários de falha"""
    
    def __init__(self, name: str, description: str, duration: int):
        self.name = name
        self.description = description
        self.duration = duration  # segundos
        self.start_time = None
        self.elapsed = 0
        
    def apply(self, base_data: dict) -> dict:
        """Aplica a falha aos dados base"""
        if self.start_time is None:
            self.start_time = time.time()
        
        self.elapsed = time.time() - self.start_time
        return base_data
    
    def is_complete(self) -> bool:
        """Verifica se o cenário completou"""
        return self.elapsed >= self.duration
    
    def get_progress(self) -> float:
        """Retorna progresso (0.0 a 1.0)"""
        return min(self.elapsed / self.duration, 1.0)


class BearingWearScenario(FaultScenario):
    """
    Cenário 1: Desgaste de Rolamento (Bearing Wear)
    
    Sintomas:
    - Aumento gradual de temperatura
    - Aumento de vibração (ruído na corrente)
    - Pequeno aumento no torque
    - Posição pode ter pequenos desvios
    
    Causa: Desgaste do rolamento da junta
    """
    
    def __init__(self, joint_number: int, duration: int = 300):
        super().__init__(
            name=f"Desgaste de Rolamento - Junta {joint_number}",
            description="Simulação de desgaste progressivo do rolamento causando aquecimento e vibração",
            duration=duration
        )
        self.joint = joint_number
        self.base_temp_increase = 0
        self.vibration_amplitude = 0
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        # Temperatura aumenta gradualmente (até +15°C)
        self.base_temp_increase = progress * 15.0
        
        # Vibração aumenta (ruído na corrente)
        self.vibration_amplitude = progress * 0.3  # Amplitude da variação de corrente
        
        # Aplicar ao joint específico
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Temperatura: aumento gradual + pequenas oscilações
            temp_variation = random.gauss(0, 1.0) * progress
            joint_data[1] += self.base_temp_increase + temp_variation
            
            # Corrente: ruído aumentado (vibração)
            current_noise = random.gauss(0, self.vibration_amplitude)
            joint_data[0] += current_noise
            
            # Torque: leve aumento por atrito
            joint_data[7] += progress * 0.5
            
            # Pequenos desvios de posição (folga)
            if random.random() < 0.3:  # 30% das leituras
                position_dev = random.gauss(0, progress * 0.1)
                if "joint_actual_position" in base_data:
                    base_data["joint_actual_position"][self.joint - 1] += position_dev
        
        return base_data


class MotorOverheatingScenario(FaultScenario):
    """
    Cenário 2: Superaquecimento do Motor
    
    Sintomas:
    - Temperatura elevada rapidamente
    - Corrente aumentada (motor forçado)
    - Temperatura ambiente também aumenta
    - Torque irregular
    
    Causa: Obstrução de ventilação ou sobrecarga contínua
    """
    
    def __init__(self, joint_number: int, duration: int = 240):
        super().__init__(
            name=f"Superaquecimento do Motor - Junta {joint_number}",
            description="Motor superaquecido por obstrução de ventilação ou sobrecarga",
            duration=duration
        )
        self.joint = joint_number
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Temperatura sobe rapidamente (até +25°C)
            temp_increase = progress * 25.0
            # Pico de temperatura não-linear (exponencial)
            temp_factor = 1 - math.exp(-progress * 3)
            joint_data[1] += temp_increase * temp_factor
            
            # Corrente aumentada (motor esforçado)
            joint_data[0] *= (1 + progress * 0.4)
            
            # Torque irregular
            torque_variation = random.gauss(0, progress * 1.0)
            joint_data[7] += torque_variation
            
            # Temperatura ambiente também sobe
            if len(monitor_data) > 2:
                monitor_data[2] += progress * 8.0  # Temperatura do robô
        
        return base_data


class PowerSupplyDegradationScenario(FaultScenario):
    """
    Cenário 3: Degradação da Fonte de Alimentação
    
    Sintomas:
    - Voltagem instável (quedas e picos)
    - Corrente com variações
    - Temperatura levemente elevada
    - Possíveis paradas de proteção
    
    Causa: Capacitores degradados ou problema na fonte
    """
    
    def __init__(self, duration: int = 360):
        super().__init__(
            name="Degradação da Fonte de Alimentação",
            description="Fonte de alimentação com componentes degradados causando instabilidade",
            duration=duration
        )
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            # Afetar todas as juntas
            for i, joint_data in enumerate(monitor_data[5]):
                # Voltagem instável (quedas de até -4V)
                voltage_drop = random.gauss(0, progress * 2.0)
                joint_data[2] += voltage_drop  # Voltage
                
                # Corrente com ripple aumentado
                current_ripple = random.gauss(0, progress * 0.2)
                joint_data[0] += current_ripple
                
                # Temperatura sobe levemente por instabilidade
                joint_data[1] += progress * 3.0
        
        return base_data


class MechanicalWearScenario(FaultScenario):
    """
    Cenário 4: Desgaste Mecânico da Transmissão
    
    Sintomas:
    - Folgas na posição (backlash)
    - Torque irregular
    - Pequeno aumento de corrente
    - Ruído (simulado por variação)
    
    Causa: Desgaste de engrenagens ou redutor
    """
    
    def __init__(self, joint_number: int, duration: int = 400):
        super().__init__(
            name=f"Desgaste Mecânico - Junta {joint_number}",
            description="Desgaste de engrenagens causando folgas e irregularidades",
            duration=duration
        )
        self.joint = joint_number
        self.backlash = 0
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        # Folga aumenta progressivamente (até 1.5 graus)
        self.backlash = progress * 1.5
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Desvio de posição (folga/backlash)
            if "joint_actual_position" in base_data:
                backlash_error = random.uniform(-self.backlash, self.backlash)
                base_data["joint_actual_position"][self.joint - 1] += backlash_error
            
            # Torque irregular (picos e vales)
            if random.random() < 0.4:
                torque_spike = random.choice([-1, 1]) * progress * 1.2
                joint_data[7] += torque_spike
            
            # Corrente levemente aumentada
            joint_data[0] *= (1 + progress * 0.15)
            
            # Temperatura sobe por atrito
            joint_data[1] += progress * 5.0
        
        return base_data


class CableConnectionIssueScenario(FaultScenario):
    """
    Cenário 5: Problema em Conexão de Cabo
    
    Sintomas:
    - Leituras intermitentes (valores anormais esporádicos)
    - Picos de corrente momentâneos
    - Possíveis perdas de comunicação
    
    Causa: Cabo desgastado ou conexão solta
    """
    
    def __init__(self, joint_number: int, duration: int = 180):
        super().__init__(
            name=f"Problema de Conexão - Junta {joint_number}",
            description="Cabo ou conector com mau contato causando leituras intermitentes",
            duration=duration
        )
        self.joint = joint_number
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Falhas intermitentes (10% + progress * 20%)
            if random.random() < (0.1 + progress * 0.2):
                # Pico de corrente
                joint_data[0] *= random.uniform(1.5, 3.0)
                
                # Leitura incorreta de temperatura
                if random.random() < 0.5:
                    joint_data[1] += random.uniform(-10, 20)
                
                # Voltagem anormal
                joint_data[2] += random.uniform(-5, 5)
        
        return base_data


class LubricationDeficiencyScenario(FaultScenario):
    """
    Cenário 6: Deficiência de Lubrificação
    
    Sintomas:
    - Aumento progressivo de temperatura
    - Torque aumentado (atrito)
    - Corrente elevada
    - Pequenas vibrações
    
    Causa: Falta ou degradação do lubrificante
    """
    
    def __init__(self, joint_number: int, duration: int = 450):
        super().__init__(
            name=f"Deficiência de Lubrificação - Junta {joint_number}",
            description="Falta de lubrificação causando atrito excessivo e aquecimento",
            duration=duration
        )
        self.joint = joint_number
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Temperatura aumenta por atrito (até +18°C)
            friction_temp = progress * 18.0
            # Não-linear: acelera no final
            temp_factor = math.pow(progress, 1.5)
            joint_data[1] += friction_temp * temp_factor
            
            # Torque aumentado significativamente
            joint_data[7] *= (1 + progress * 0.6)
            
            # Corrente aumentada (motor compensa atrito)
            joint_data[0] *= (1 + progress * 0.35)
            
            # Vibração (ruído na corrente)
            vibration = random.gauss(0, progress * 0.25)
            joint_data[0] += vibration
        
        return base_data


class EncoderDriftScenario(FaultScenario):
    """
    Cenário 7: Deriva do Encoder
    
    Sintomas:
    - Erro crescente na posição
    - Diferença entre posição comandada e real
    - Corrente aumenta (correção constante)
    
    Causa: Encoder desalinhado ou danificado
    """
    
    def __init__(self, joint_number: int, duration: int = 300):
        super().__init__(
            name=f"Deriva do Encoder - Junta {joint_number}",
            description="Encoder com deriva causando erros de posicionamento",
            duration=duration
        )
        self.joint = joint_number
        self.accumulated_error = 0
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        # Erro acumulado (deriva)
        self.accumulated_error += random.gauss(0.05, 0.02) * progress
        
        if "joint_actual_position" in base_data:
            # Adicionar deriva à posição real
            base_data["joint_actual_position"][self.joint - 1] += self.accumulated_error
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Corrente aumenta (controlador tenta compensar)
            joint_data[0] *= (1 + progress * 0.2)
            
            # Temperatura sobe levemente
            joint_data[1] += progress * 4.0
        
        return base_data


class OverloadContinuousScenario(FaultScenario):
    """
    Cenário 8: Sobrecarga Contínua
    
    Sintomas:
    - Corrente muito elevada
    - Temperatura alta em múltiplas juntas
    - Torque no limite
    - Possível thermal shutdown
    
    Causa: Carga muito acima da especificação
    """
    
    def __init__(self, duration: int = 200):
        super().__init__(
            name="Sobrecarga Contínua",
            description="Robô operando acima da capacidade nominal",
            duration=duration
        )
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            # Afetar principalmente juntas 1, 2 e 3 (base)
            for i in [0, 1, 2]:
                joint_data = monitor_data[5][i]
                
                # Corrente muito alta
                joint_data[0] *= (1 + progress * 0.8)
                
                # Temperatura crítica
                joint_data[1] += progress * 22.0
                
                # Torque no limite
                joint_data[7] *= (1 + progress * 0.7)
            
            # Temperatura geral do robô
            if len(monitor_data) > 2:
                monitor_data[2] += progress * 15.0
        
        return base_data


class VibrationResonanceScenario(FaultScenario):
    """
    Cenário 9: Ressonância Mecânica
    
    Sintomas:
    - Vibração periódica (oscilação na corrente/torque)
    - Temperatura oscilante
    - Amplitude aumenta com tempo
    
    Causa: Frequência de operação próxima à frequência natural
    """
    
    def __init__(self, joint_number: int, duration: int = 250):
        super().__init__(
            name=f"Ressonância Mecânica - Junta {joint_number}",
            description="Vibração ressonante causando oscilações crescentes",
            duration=duration
        )
        self.joint = joint_number
        self.frequency = random.uniform(2, 5)  # Hz
        
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        
        progress = self.get_progress()
        
        # Onda senoidal com amplitude crescente
        vibration = math.sin(self.elapsed * self.frequency * 2 * math.pi)
        amplitude = progress * 1.5
        
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_data = monitor_data[5][self.joint - 1]
            
            # Corrente oscilante
            joint_data[0] += vibration * amplitude * 0.5
            
            # Torque oscilante
            joint_data[7] += vibration * amplitude
            
            # Temperatura oscila levemente
            joint_data[1] += abs(vibration) * progress * 8.0
        
        return base_data


class ScenarioSimulator:
    """Gerenciador de simulação de cenários"""
    
    def __init__(self, broker: str, port: int, topic: str):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None
        self.scenarios: List[FaultScenario] = []
        self.current_scenario_index = 0
        self.normal_operation_time = 30  # segundos de operação normal entre cenários
        self.in_normal_operation = True
        self.normal_start_time = None
        
    def add_scenario(self, scenario: FaultScenario):
        """Adiciona um cenário à sequência"""
        self.scenarios.append(scenario)
        
    def connect_mqtt(self):
        """Conecta ao broker MQTT"""
        self.client = mqtt.Client(client_id="fault_scenario_simulator")
        self.client.connect(self.broker, self.port, 60)
        print(f"✓ Conectado ao broker MQTT: {self.broker}:{self.port}")
        
    def generate_base_data(self) -> dict:
        """Gera dados base normais do robô"""
        base_data = {
            "ID": 1,
            "NOME": "JAKA_MiniCobo",
            "task_state": 2,  # Executando
            "task_mode": 1,
            "enabled": True,
            "powered_on": 1,
            "emergency_stop": 0,
            "protective_stop": 0,
            "on_soft_limit": 0,
            "monitor_data": [
                1,  # enabled
                1,  # powered_on
                35.0,  # robot_temp
                25.0,  # ambient_temp
                12,    # current_tool_id
                [  # Joint data (6 juntas)
                    [1.2, 28.0, 48.5, 0, 0, 0, 0, 2.1],  # current, temp, voltage, ...
                    [1.3, 29.0, 48.3, 0, 0, 0, 0, 2.3],
                    [1.1, 27.5, 48.6, 0, 0, 0, 0, 2.0],
                    [0.9, 26.0, 48.7, 0, 0, 0, 0, 1.8],
                    [0.8, 25.5, 48.8, 0, 0, 0, 0, 1.5],
                    [0.7, 25.0, 48.9, 0, 0, 0, 0, 1.3]
                ]
            ],
            "joint_actual_position": [0.0, 45.0, -30.0, 0.0, 90.0, 0.0],
            "actual_position": [200.5, 150.3, 300.8, 0.0, 90.0, 0.0],
            "instVel": [0.1, 0.12, 0.08, 0.05, 0.03, 0.02]
        }
        return base_data
    
    def run(self, interval: float = 2.0):
        """Executa a simulação"""
        try:
            print("\n" + "="*70)
            print("SIMULADOR DE CENÁRIOS DE FALHAS - ROBÔ JAKA")
            print("="*70)
            print(f"\nTotal de cenários: {len(self.scenarios)}")
            print(f"Intervalo de publicação: {interval}s")
            print(f"Tempo de operação normal entre cenários: {self.normal_operation_time}s\n")
            
            for i, scenario in enumerate(self.scenarios, 1):
                print(f"{i}. {scenario.name}")
                print(f"   └─ {scenario.description}")
                print(f"   └─ Duração: {scenario.duration}s\n")
            
            print("="*70)
            print("Iniciando simulação...")
            print("Pressione Ctrl+C para parar\n")
            
            while self.current_scenario_index < len(self.scenarios):
                if self.in_normal_operation:
                    # Período de operação normal
                    if self.normal_start_time is None:
                        self.normal_start_time = time.time()
                        scenario_num = self.current_scenario_index + 1
                        print(f"\n{'─'*70}")
                        print(f"⏸️  OPERAÇÃO NORMAL (antes do cenário {scenario_num})")
                        print(f"{'─'*70}")
                    
                    elapsed = time.time() - self.normal_start_time
                    
                    if elapsed >= self.normal_operation_time:
                        # Fim da operação normal, iniciar cenário
                        self.in_normal_operation = False
                        self.normal_start_time = None
                        
                        scenario = self.scenarios[self.current_scenario_index]
                        print(f"\n{'='*70}")
                        print(f"🔴 CENÁRIO {self.current_scenario_index + 1}: {scenario.name}")
                        print(f"{'='*70}")
                        print(f"Descrição: {scenario.description}")
                        print(f"Duração: {scenario.duration}s")
                        print(f"{'─'*70}\n")
                    else:
                        # Publicar dados normais
                        base_data = self.generate_base_data()
                        self.publish_data(base_data)
                        print(f"⏸️  Operação Normal: {int(elapsed)}/{self.normal_operation_time}s", end='\r')
                
                else:
                    # Executando cenário de falha
                    scenario = self.scenarios[self.current_scenario_index]
                    base_data = self.generate_base_data()
                    
                    # Aplicar falha
                    modified_data = scenario.apply(base_data)
                    
                    # Publicar
                    self.publish_data(modified_data)
                    
                    # Mostrar progresso
                    progress = scenario.get_progress() * 100
                    print(f"🔴 Cenário {self.current_scenario_index + 1}: {progress:.1f}% | "
                          f"{int(scenario.elapsed)}/{scenario.duration}s", end='\r')
                    
                    # Verificar se completou
                    if scenario.is_complete():
                        print(f"\n✓ Cenário {self.current_scenario_index + 1} concluído!\n")
                        self.current_scenario_index += 1
                        self.in_normal_operation = True
                
                time.sleep(interval)
            
            print("\n" + "="*70)
            print("✅ SIMULAÇÃO COMPLETA!")
            print("="*70)
            print("\nTodos os cenários foram executados.")
            print(f"Total de cenários: {len(self.scenarios)}")
            print("\n💾 Dados foram enviados para o sistema de monitoramento.")
            print("📊 Use os scripts de análise para gerar relatórios.\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Simulação interrompida pelo usuário")
        finally:
            if self.client:
                self.client.disconnect()
    
    def publish_data(self, data: dict):
        """Publica dados no MQTT"""
        payload = json.dumps(data)
        self.client.publish(self.topic, payload)


def main():
    parser = argparse.ArgumentParser(
        description="Simulador de Cenários de Falhas para Robô JAKA"
    )
    parser.add_argument(
        '--interval', 
        type=float, 
        default=2.0,
        help='Intervalo entre publicações em segundos (padrão: 2.0)'
    )
    parser.add_argument(
        '--normal-time',
        type=int,
        default=30,
        help='Tempo de operação normal entre cenários em segundos (padrão: 30)'
    )
    parser.add_argument(
        '--scenarios',
        type=str,
        default='all',
        help='Cenários a executar: all, bearing, motor, power, etc. (padrão: all)'
    )
    
    args = parser.parse_args()
    
    # Criar simulador
    simulator = ScenarioSimulator(
        broker=config.MQTT_BROKER,
        port=config.MQTT_PORT,
        topic=config.MQTT_TOPIC
    )
    
    simulator.normal_operation_time = args.normal_time
    
    # Adicionar cenários
    print("\n📋 Configurando cenários de falha...")
    
    if args.scenarios == 'all' or 'bearing' in args.scenarios:
        simulator.add_scenario(BearingWearScenario(joint_number=3, duration=180))
    
    if args.scenarios == 'all' or 'motor' in args.scenarios:
        simulator.add_scenario(MotorOverheatingScenario(joint_number=2, duration=150))
    
    if args.scenarios == 'all' or 'power' in args.scenarios:
        simulator.add_scenario(PowerSupplyDegradationScenario(duration=200))
    
    if args.scenarios == 'all' or 'mechanical' in args.scenarios:
        simulator.add_scenario(MechanicalWearScenario(joint_number=1, duration=220))
    
    if args.scenarios == 'all' or 'cable' in args.scenarios:
        simulator.add_scenario(CableConnectionIssueScenario(joint_number=4, duration=120))
    
    if args.scenarios == 'all' or 'lubrication' in args.scenarios:
        simulator.add_scenario(LubricationDeficiencyScenario(joint_number=2, duration=250))
    
    if args.scenarios == 'all' or 'encoder' in args.scenarios:
        simulator.add_scenario(EncoderDriftScenario(joint_number=5, duration=180))
    
    if args.scenarios == 'all' or 'overload' in args.scenarios:
        simulator.add_scenario(OverloadContinuousScenario(duration=140))
    
    if args.scenarios == 'all' or 'vibration' in args.scenarios:
        simulator.add_scenario(VibrationResonanceScenario(joint_number=3, duration=160))
    
    # Conectar e executar
    simulator.connect_mqtt()
    simulator.run(interval=args.interval)


if __name__ == "__main__":
    main()
