"""
Script de Teste - Simulador de Dados JAKA
Útil para testar o sistema sem conexão com o robô real
"""
import json
import time
import random
from datetime import datetime
import paho.mqtt.client as mqtt

# Configurações
MQTT_BROKER = "147.1.5.238"
MQTT_PORT = 1883
MQTT_TOPIC = "jaka/monitor"
MQTT_USERNAME = "mqtt"
MQTT_PASSWORD = "rede@123"

# Carregar dados de exemplo
with open('../dados.json', 'r', encoding='utf-8') as f:
    base_data = json.load(f)


def simulate_wear_pattern(base_value: float, iteration: int, wear_rate: float = 0.01) -> float:
    """
    Simula desgaste gradual em um parâmetro
    
    Args:
        base_value: Valor base
        iteration: Número da iteração
        wear_rate: Taxa de desgaste
    
    Returns:
        Valor com desgaste simulado
    """
    # Adicionar tendência de aumento + ruído
    trend = iteration * wear_rate
    noise = random.uniform(-0.5, 0.5)
    return base_value + trend + noise


def generate_simulated_data(iteration: int, simulate_anomaly: bool = False) -> dict:
    """
    Gera dados simulados do robô
    
    Args:
        iteration: Número da iteração
        simulate_anomaly: Se True, simula condições anormais
    
    Returns:
        Dicionário com dados simulados
    """
    data = base_data.copy()
    
    # Simular dados das juntas
    if len(data["monitor_data"]) > 5 and isinstance(data["monitor_data"][5], list):
        for i, joint_data in enumerate(data["monitor_data"][5]):
            if isinstance(joint_data, list) and len(joint_data) >= 8:
                # Temperatura base + desgaste
                base_temp = 23.0
                joint_data[1] = simulate_wear_pattern(base_temp, iteration, 0.05)
                
                # Se simular anomalia, aumentar temperatura da junta 2
                if simulate_anomaly and i == 1:
                    joint_data[1] += 20.0  # Temperatura crítica
                    joint_data[0] = 2.5    # Corrente alta
                    joint_data[7] = 3.2    # Torque elevado
                
                # Corrente com variação
                joint_data[0] = abs(random.gauss(0.5, 0.3))
                
                # Torque com desgaste
                base_torque = 2.6
                joint_data[7] = simulate_wear_pattern(base_torque, iteration, 0.002)
                
                # Velocidade aleatória
                joint_data[4] = random.uniform(0, 0.3)
    
    # Temperatura do robô
    if len(data["monitor_data"]) > 2:
        base_robot_temp = 26.0
        data["monitor_data"][2] = simulate_wear_pattern(base_robot_temp, iteration, 0.03)
        
        if simulate_anomaly:
            data["monitor_data"][2] += 15.0
    
    # Posições com pequenas variações
    for i in range(len(data["joint_actual_position"])):
        data["joint_actual_position"][i] += random.uniform(-0.1, 0.1)
    
    # TCP com movimento
    data["actual_position"][0] += random.uniform(-2, 2)
    data["actual_position"][1] += random.uniform(-2, 2)
    data["actual_position"][2] += random.uniform(-1, 1)
    
    return data


def main():
    """Função principal do simulador"""
    print("=" * 60)
    print("SIMULADOR DE DADOS JAKA - Teste do Sistema de Monitoramento")
    print("=" * 60)
    print()
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Tópico: {MQTT_TOPIC}")
    print()
    
    # Conectar ao MQTT
    client = mqtt.Client(client_id="jaka-simulator")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    try:
        print("Conectando ao broker MQTT...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        print("✓ Conectado com sucesso!")
        print()
        
        print("Iniciando simulação...")
        print("Pressione Ctrl+C para parar")
        print()
        
        iteration = 0
        anomaly_counter = 0
        
        while True:
            iteration += 1
            
            # A cada 20 mensagens, simular uma anomalia
            simulate_anomaly = (iteration % 20 == 0)
            
            # Gerar dados
            data = generate_simulated_data(iteration, simulate_anomaly)
            
            # Publicar
            payload = json.dumps(data)
            result = client.publish(MQTT_TOPIC, payload, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                status = "⚠️  ANOMALIA" if simulate_anomaly else "✓ Normal"
                robot_temp = data["monitor_data"][2] if len(data["monitor_data"]) > 2 else 0
                
                print(f"[{iteration:04d}] {status} | Temp Robô: {robot_temp:.1f}°C | "
                      f"Enviado {len(payload)} bytes")
                
                if simulate_anomaly:
                    anomaly_counter += 1
            else:
                print(f"✗ Falha ao publicar (código {result.rc})")
            
            # Aguardar antes da próxima mensagem
            time.sleep(2)  # 2 segundos entre mensagens
        
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("Simulação interrompida pelo usuário")
        print(f"Total de mensagens enviadas: {iteration}")
        print(f"Anomalias simuladas: {anomaly_counter}")
        print("=" * 60)
    
    except Exception as e:
        print(f"✗ Erro: {e}")
    
    finally:
        client.loop_stop()
        client.disconnect()
        print("Desconectado do broker")


if __name__ == "__main__":
    main()
