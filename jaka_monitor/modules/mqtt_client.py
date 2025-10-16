"""
Módulo de Conexão MQTT
Recebe dados do robô via MQTT
"""
import json
import logging
from typing import Callable, Optional
import paho.mqtt.client as mqtt
from datetime import datetime


class MQTTClient:
    """Cliente MQTT para receber dados do robô JAKA"""
    
    def __init__(self, broker: str, port: int, topic: str, client_id: str,
                 username: Optional[str] = None, password: Optional[str] = None,
                 qos: int = 1, keepalive: int = 60):
        """
        Inicializa o cliente MQTT
        
        Args:
            broker: Endereço do broker MQTT
            port: Porta do broker
            topic: Tópico para subscrever
            client_id: ID do cliente
            username: Usuário MQTT (opcional)
            password: Senha MQTT (opcional)
            qos: Quality of Service
            keepalive: Tempo de keepalive em segundos
        """
        self.broker = broker
        self.port = port
        self.topic = topic
        self.qos = qos
        self.keepalive = keepalive
        
        # Callback para processar mensagens
        self.message_callback: Optional[Callable] = None
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        # Criar cliente MQTT
        self.client = mqtt.Client(client_id=client_id)
        
        # Configurar autenticação se fornecida
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Configurar callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        # Estado
        self.connected = False
        self.message_count = 0
        self.last_message_time = None
        self.connection_time = None
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback chamado quando conecta ao broker"""
        if rc == 0:
            self.connected = True
            self.connection_time = datetime.now()
            self.logger.info(f"[OK] Conectado ao broker MQTT: {self.broker}:{self.port}")
            
            # Subscrever ao tópico
            result = client.subscribe(self.topic, self.qos)
            self.logger.info(f"[OK] Subscrito ao tópico: {self.topic} (QoS {self.qos})")
        else:
            self.connected = False
            error_messages = {
                1: "Protocolo incorreto",
                2: "ID do cliente rejeitado",
                3: "Servidor indisponível",
                4: "Usuário/senha incorretos",
                5: "Não autorizado"
            }
            error_msg = error_messages.get(rc, f"Código de erro desconhecido: {rc}")
            self.logger.error(f"[ERRO] Falha na conexão: {error_msg}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback chamado quando desconecta do broker"""
        self.connected = False
        if rc == 0:
            self.logger.info("Desconectado do broker MQTT")
        else:
            self.logger.warning(f"Desconexão inesperada (código {rc}). Tentando reconectar...")
    
    def _on_message(self, client, userdata, msg):
        """Callback chamado quando recebe uma mensagem"""
        try:
            self.message_count += 1
            self.last_message_time = datetime.now()
            
            # Decodificar JSON
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
            
            # Log básico
            self.logger.debug(f"Mensagem recebida #{self.message_count} ({len(payload)} bytes)")
            
            # Chamar callback personalizado se configurado
            if self.message_callback:
                self.message_callback(data)
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar JSON: {e}")
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {e}")
    
    def set_message_callback(self, callback: Callable):
        """
        Define a função callback para processar mensagens
        
        Args:
            callback: Função que receberá os dados (dict)
        """
        self.message_callback = callback
    
    def connect(self):
        """Conecta ao broker MQTT"""
        try:
            self.logger.info(f"Conectando ao broker {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, self.keepalive)
        except Exception as e:
            self.logger.error(f"Erro ao conectar: {e}")
            raise
    
    def start(self):
        """Inicia o loop de processamento (non-blocking)"""
        self.client.loop_start()
        self.logger.info("Loop MQTT iniciado")
    
    def stop(self):
        """Para o loop e desconecta"""
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Cliente MQTT encerrado")
    
    def publish(self, topic: str, payload: dict, qos: int = 1):
        """
        Publica uma mensagem em um tópico
        
        Args:
            topic: Tópico de destino
            payload: Dados a enviar (dict)
            qos: Quality of Service
        """
        try:
            json_payload = json.dumps(payload)
            result = self.client.publish(topic, json_payload, qos)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.debug(f"Mensagem publicada em {topic}")
            else:
                self.logger.error(f"Falha ao publicar mensagem (código {result.rc})")
        except Exception as e:
            self.logger.error(f"Erro ao publicar: {e}")
    
    def get_status(self) -> dict:
        """Retorna status da conexão MQTT"""
        return {
            'connected': self.connected,
            'broker': f"{self.broker}:{self.port}",
            'topic': self.topic,
            'message_count': self.message_count,
            'last_message': self.last_message_time.isoformat() if self.last_message_time else None,
            'connection_time': self.connection_time.isoformat() if self.connection_time else None
        }
