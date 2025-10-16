"""
Interface Gráfica Principal usando PyQt5
Dashboard de monitoramento em tempo real
"""
import sys
import os
from datetime import datetime
from typing import Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QTextEdit, QGroupBox, QGridLayout, 
                            QTableWidget, QTableWidgetItem, QTabWidget, QProgressBar,
                            QMessageBox, QFileDialog, QStatusBar, QSplitter)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QPalette
import logging

# Importar módulos do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from modules.mqtt_client import MQTTClient
from modules.database import DatabaseManager
from modules.analyzer import AnomalyDetector
from modules.report_generator import ReportGenerator


class MonitorThread(QThread):
    """Thread para processar dados MQTT sem bloquear a UI"""
    new_data = pyqtSignal(dict)
    anomaly_detected = pyqtSignal(list)
    connection_status = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.mqtt_client = None
        self.analyzer = AnomalyDetector()
        self.db_manager = None
        self.running = False
        self.message_counter = 0
    
    def setup(self, db_manager: DatabaseManager):
        """Configura o thread com o gerenciador de banco"""
        self.db_manager = db_manager
    
    def run(self):
        """Executa o thread de monitoramento"""
        self.running = True
        
        try:
            # Criar cliente MQTT
            self.mqtt_client = MQTTClient(
                broker=config.MQTT_BROKER,
                port=config.MQTT_PORT,
                topic=config.MQTT_TOPIC,
                client_id=config.MQTT_CLIENT_ID,
                username=config.MQTT_USERNAME,
                password=config.MQTT_PASSWORD,
                qos=config.MQTT_QOS,
                keepalive=config.MQTT_KEEPALIVE
            )
            
            # Configurar callback
            self.mqtt_client.set_message_callback(self.process_message)
            
            # Conectar e iniciar
            self.mqtt_client.connect()
            self.connection_status.emit(True)
            self.mqtt_client.start()
            
            # Manter thread ativo
            while self.running:
                self.msleep(100)
        
        except Exception as e:
            logging.error(f"Erro no thread de monitoramento: {e}")
            self.connection_status.emit(False)
    
    def process_message(self, data: dict):
        """Processa mensagem recebida do MQTT"""
        try:
            # Emitir dados para UI
            self.new_data.emit(data)
            
            # Analisar anomalias
            anomalies = self.analyzer.analyze(data)
            
            if anomalies:
                self.anomaly_detected.emit(anomalies)
            
            # Salvar no banco de dados
            self.message_counter += 1
            if self.message_counter % config.SAVE_INTERVAL == 0:
                if self.db_manager:
                    self.db_manager.insert_robot_data(data)
                    
                    # Registrar anomalias
                    for anomaly in anomalies:
                        # Calcular criticidade temporal
                        anomaly_key = f"{anomaly.get('type')}_{anomaly.get('joint', 0)}"
                        severity, duration = self.analyzer.calculate_criticality(
                            anomaly_key, anomaly.get('severity', 'info')
                        )
                        
                        self.db_manager.insert_event(
                            event_type=anomaly.get('type', 'unknown'),
                            severity=severity,
                            description=anomaly.get('description', ''),
                            joint_number=anomaly.get('joint'),
                            value=anomaly.get('value'),
                            threshold=anomaly.get('threshold'),
                            duration=duration
                        )
        
        except Exception as e:
            logging.error(f"Erro ao processar mensagem: {e}")
    
    def stop(self):
        """Para o thread"""
        self.running = False
        if self.mqtt_client:
            self.mqtt_client.stop()


class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        
        # Configurar logging
        self.setup_logging()
        
        # Inicializar componentes
        self.db_manager = DatabaseManager(config.DB_PATH)
        self.report_generator = ReportGenerator(self.db_manager)
        
        # Thread de monitoramento
        self.monitor_thread = MonitorThread()
        self.monitor_thread.setup(self.db_manager)
        self.monitor_thread.new_data.connect(self.update_data)
        self.monitor_thread.anomaly_detected.connect(self.handle_anomaly)
        self.monitor_thread.connection_status.connect(self.update_connection_status)
        
        # Dados atuais
        self.current_data = None
        self.health_score = 100.0
        
        # Configurar UI
        self.init_ui()
        
        # Timer para atualizar UI
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui)
        self.ui_timer.start(1000)  # Atualizar a cada 1 segundo
    
    def setup_logging(self):
        """Configura sistema de logging"""
        os.makedirs(config.LOGS_DIR, exist_ok=True)
        log_file = os.path.join(config.LOGS_DIR, f"system_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle(f"{config.SYSTEM_NAME} v{config.SYSTEM_VERSION}")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Cabeçalho
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Abas
        tabs = QTabWidget()
        tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        tabs.addTab(self.create_joints_tab(), "Juntas")
        tabs.addTab(self.create_events_tab(), "Eventos")
        tabs.addTab(self.create_reports_tab(), "Relatórios")
        main_layout.addWidget(tabs)
        
        # Barra de status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Sistema iniciado. Aguardando conexão MQTT...")
        
        # Aplicar estilo
        self.apply_style()
    
    def create_header(self) -> QWidget:
        """Cria o cabeçalho com informações gerais"""
        header = QGroupBox("Status do Sistema")
        layout = QGridLayout()
        
        # Status de conexão
        self.conn_status_label = QLabel("● Desconectado")
        self.conn_status_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
        layout.addWidget(QLabel("Conexão MQTT:"), 0, 0)
        layout.addWidget(self.conn_status_label, 0, 1)
        
        # Score de saúde
        layout.addWidget(QLabel("Saúde do Robô:"), 0, 2)
        self.health_score_label = QLabel("100%")
        self.health_score_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.health_score_label, 0, 3)
        
        # Barra de progresso de saúde
        self.health_bar = QProgressBar()
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(100)
        self.health_bar.setTextVisible(True)
        layout.addWidget(self.health_bar, 1, 0, 1, 4)
        
        # Botões de controle
        self.start_btn = QPushButton("Iniciar Monitoramento")
        self.start_btn.clicked.connect(self.start_monitoring)
        layout.addWidget(self.start_btn, 2, 0)
        
        self.stop_btn = QPushButton("Parar Monitoramento")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn, 2, 1)
        
        header.setLayout(layout)
        return header
    
    def create_dashboard_tab(self) -> QWidget:
        """Cria aba do dashboard principal"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Informações do robô
        robot_info = QGroupBox("Informações do Robô")
        robot_layout = QGridLayout()
        
        self.robot_id_label = QLabel("N/A")
        self.robot_name_label = QLabel("N/A")
        self.robot_temp_label = QLabel("N/A")
        self.task_state_label = QLabel("N/A")
        
        robot_layout.addWidget(QLabel("ID:"), 0, 0)
        robot_layout.addWidget(self.robot_id_label, 0, 1)
        robot_layout.addWidget(QLabel("Nome:"), 0, 2)
        robot_layout.addWidget(self.robot_name_label, 0, 3)
        robot_layout.addWidget(QLabel("Temperatura:"), 1, 0)
        robot_layout.addWidget(self.robot_temp_label, 1, 1)
        robot_layout.addWidget(QLabel("Estado:"), 1, 2)
        robot_layout.addWidget(self.task_state_label, 1, 3)
        
        robot_info.setLayout(robot_layout)
        layout.addWidget(robot_info)
        
        # Posição TCP
        tcp_info = QGroupBox("Posição TCP (Tool Center Point)")
        tcp_layout = QGridLayout()
        
        self.tcp_x_label = QLabel("0.0")
        self.tcp_y_label = QLabel("0.0")
        self.tcp_z_label = QLabel("0.0")
        self.tcp_rx_label = QLabel("0.0")
        self.tcp_ry_label = QLabel("0.0")
        self.tcp_rz_label = QLabel("0.0")
        
        tcp_layout.addWidget(QLabel("X:"), 0, 0)
        tcp_layout.addWidget(self.tcp_x_label, 0, 1)
        tcp_layout.addWidget(QLabel("mm"), 0, 2)
        tcp_layout.addWidget(QLabel("Y:"), 1, 0)
        tcp_layout.addWidget(self.tcp_y_label, 1, 1)
        tcp_layout.addWidget(QLabel("mm"), 1, 2)
        tcp_layout.addWidget(QLabel("Z:"), 2, 0)
        tcp_layout.addWidget(self.tcp_z_label, 2, 1)
        tcp_layout.addWidget(QLabel("mm"), 2, 2)
        
        tcp_layout.addWidget(QLabel("Rx:"), 0, 3)
        tcp_layout.addWidget(self.tcp_rx_label, 0, 4)
        tcp_layout.addWidget(QLabel("°"), 0, 5)
        tcp_layout.addWidget(QLabel("Ry:"), 1, 3)
        tcp_layout.addWidget(self.tcp_ry_label, 1, 4)
        tcp_layout.addWidget(QLabel("°"), 1, 5)
        tcp_layout.addWidget(QLabel("Rz:"), 2, 3)
        tcp_layout.addWidget(self.tcp_rz_label, 2, 4)
        tcp_layout.addWidget(QLabel("°"), 2, 5)
        
        tcp_info.setLayout(tcp_layout)
        layout.addWidget(tcp_info)
        
        # Criar splitter para dividir log e alertas
        splitter = QSplitter(Qt.Horizontal)
        
        # Log de eventos em tempo real
        events_log = QGroupBox("Log de Eventos (Tempo Real)")
        events_layout = QVBoxLayout()
        self.events_text = QTextEdit()
        self.events_text.setReadOnly(True)
        events_layout.addWidget(self.events_text)
        events_log.setLayout(events_layout)
        splitter.addWidget(events_log)
        
        # Painel de Anomalias Ativas
        anomalies_panel = QGroupBox("⚠ Anomalias Detectadas")
        anomalies_layout = QVBoxLayout()
        self.anomalies_text = QTextEdit()
        self.anomalies_text.setReadOnly(True)
        self.anomalies_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFF3CD;
                border: 2px solid #FFC107;
                font-family: 'Courier New';
                font-size: 11px;
            }
        """)
        anomalies_layout.addWidget(self.anomalies_text)
        
        # Botão para limpar alertas
        clear_anomalies_btn = QPushButton("Limpar Anomalias")
        clear_anomalies_btn.clicked.connect(self.clear_anomalies)
        anomalies_layout.addWidget(clear_anomalies_btn)
        
        anomalies_panel.setLayout(anomalies_layout)
        splitter.addWidget(anomalies_panel)
        
        # Definir proporções do splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        widget.setLayout(layout)
        return widget
    
    def create_joints_tab(self) -> QWidget:
        """Cria aba com informações das juntas"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Tabela de juntas
        self.joints_table = QTableWidget()
        self.joints_table.setColumnCount(7)
        self.joints_table.setHorizontalHeaderLabels([
            "Junta", "Posição (°)", "Velocidade", "Corrente (A)", 
            "Temperatura (°C)", "Voltagem (V)", "Torque"
        ])
        self.joints_table.setRowCount(6)
        
        # Preencher com dados padrão
        for i in range(6):
            self.joints_table.setItem(i, 0, QTableWidgetItem(f"Junta {i+1}"))
            for j in range(1, 7):
                self.joints_table.setItem(i, j, QTableWidgetItem("N/A"))
        
        layout.addWidget(self.joints_table)
        widget.setLayout(layout)
        return widget
    
    def create_events_tab(self) -> QWidget:
        """Cria aba de histórico de eventos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Botão para atualizar
        refresh_btn = QPushButton("Atualizar Eventos")
        refresh_btn.clicked.connect(self.load_events)
        layout.addWidget(refresh_btn)
        
        # Tabela de eventos
        self.events_table = QTableWidget()
        self.events_table.setColumnCount(5)
        self.events_table.setHorizontalHeaderLabels([
            "Data/Hora", "Severidade", "Tipo", "Descrição", "Duração (s)"
        ])
        
        layout.addWidget(self.events_table)
        widget.setLayout(layout)
        return widget
    
    def create_reports_tab(self) -> QWidget:
        """Cria aba de geração de relatórios"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Botões de geração
        pdf_btn = QPushButton("Gerar Relatório PDF Completo")
        pdf_btn.clicked.connect(self.generate_pdf_report)
        layout.addWidget(pdf_btn)
        
        excel_btn = QPushButton("Exportar Dados para Excel")
        excel_btn.clicked.connect(self.export_excel)
        layout.addWidget(excel_btn)
        
        # Área de informações
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml("""
        <h2>Geração de Relatórios</h2>
        <p>Este sistema permite gerar relatórios detalhados para análise:</p>
        <ul>
            <li><b>Relatório PDF:</b> Documento completo com gráficos, estatísticas e lista de eventos</li>
            <li><b>Exportação Excel:</b> Dados brutos em planilha para análise customizada</li>
        </ul>
        <p>Os relatórios são salvos na pasta: <code>reports/</code></p>
        <p>Os gráficos incluem:</p>
        <ul>
            <li>Evolução de temperatura das juntas</li>
            <li>Evolução de corrente das juntas</li>
            <li>Evolução de torque/carga das juntas</li>
        </ul>
        """)
        layout.addWidget(info_text)
        
        widget.setLayout(layout)
        return widget
    
    def apply_style(self):
        """Aplica estilo visual à aplicação"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
    
    def start_monitoring(self):
        """Inicia o monitoramento"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.monitor_thread.start()
        self.log_event("Sistema de monitoramento iniciado", "info")
        self.status_bar.showMessage("Conectando ao broker MQTT...")
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.monitor_thread.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.conn_status_label.setText("● Desconectado")
        self.conn_status_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
        self.log_event("Sistema de monitoramento parado", "info")
        self.status_bar.showMessage("Monitoramento parado")
    
    def update_connection_status(self, connected: bool):
        """Atualiza status da conexão"""
        if connected:
            self.conn_status_label.setText("● Conectado")
            self.conn_status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
            self.status_bar.showMessage("Conectado ao broker MQTT - Recebendo dados")
        else:
            self.conn_status_label.setText("● Erro")
            self.conn_status_label.setStyleSheet("color: orange; font-weight: bold; font-size: 14px;")
            self.status_bar.showMessage("Erro na conexão MQTT")
    
    def update_data(self, data: dict):
        """Atualiza interface com novos dados"""
        self.current_data = data
        
        # Atualizar informações do robô
        self.robot_id_label.setText(str(data.get("ID", "N/A")))
        self.robot_name_label.setText(data.get("NOME", "N/A"))
        
        monitor_data = data.get("monitor_data", [])
        if len(monitor_data) > 2:
            temp = monitor_data[2]
            self.robot_temp_label.setText(f"{temp:.1f}°C")
            
            # Colorir baseado na temperatura
            if temp >= config.THRESHOLDS["robot_temp_critical"]:
                self.robot_temp_label.setStyleSheet("color: red; font-weight: bold;")
            elif temp >= config.THRESHOLDS["robot_temp_warning"]:
                self.robot_temp_label.setStyleSheet("color: orange; font-weight: bold;")
            else:
                self.robot_temp_label.setStyleSheet("color: green;")
        
        # Estado da tarefa
        task_states = {0: "Desconhecido", 1: "Iniciando", 2: "Executando", 3: "Pausado", 4: "IDLE", 5: "Erro"}
        self.task_state_label.setText(task_states.get(data.get("task_state", 0), "Desconhecido"))
        
        # Posição TCP
        position = data.get("actual_position", [0]*6)
        if len(position) >= 6:
            self.tcp_x_label.setText(f"{position[0]:.2f}")
            self.tcp_y_label.setText(f"{position[1]:.2f}")
            self.tcp_z_label.setText(f"{position[2]:.2f}")
            self.tcp_rx_label.setText(f"{position[3]:.2f}")
            self.tcp_ry_label.setText(f"{position[4]:.2f}")
            self.tcp_rz_label.setText(f"{position[5]:.2f}")
        
        # Atualizar tabela de juntas
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_positions = data.get("joint_actual_position", [])
            joint_velocities = data.get("instVel", [])
            
            for i, joint_data in enumerate(monitor_data[5]):
                if isinstance(joint_data, list) and len(joint_data) >= 8:
                    self.joints_table.setItem(i, 1, QTableWidgetItem(f"{joint_positions[i]:.2f}" if i < len(joint_positions) else "N/A"))
                    self.joints_table.setItem(i, 2, QTableWidgetItem(f"{joint_velocities[i]:.3f}" if i < len(joint_velocities) else "N/A"))
                    
                    # Corrente
                    current_item = QTableWidgetItem(f"{abs(joint_data[0]):.3f}")
                    if abs(joint_data[0]) >= config.THRESHOLDS["joint_current_critical"]:
                        current_item.setBackground(QColor(255, 0, 0, 100))
                    elif abs(joint_data[0]) >= config.THRESHOLDS["joint_current_warning"]:
                        current_item.setBackground(QColor(255, 165, 0, 100))
                    self.joints_table.setItem(i, 3, current_item)
                    
                    # Temperatura
                    temp_item = QTableWidgetItem(f"{joint_data[1]:.1f}")
                    if joint_data[1] >= config.THRESHOLDS["joint_temperature_critical"]:
                        temp_item.setBackground(QColor(255, 0, 0, 100))
                    elif joint_data[1] >= config.THRESHOLDS["joint_temperature_warning"]:
                        temp_item.setBackground(QColor(255, 165, 0, 100))
                    self.joints_table.setItem(i, 4, temp_item)
                    
                    self.joints_table.setItem(i, 5, QTableWidgetItem(f"{joint_data[2]:.1f}"))
                    self.joints_table.setItem(i, 6, QTableWidgetItem(f"{abs(joint_data[7]):.2f}"))
    
    def update_ui(self):
        """Atualização periódica da UI"""
        if self.current_data:
            # Calcular score de saúde
            self.health_score = self.monitor_thread.analyzer.get_health_score(self.current_data)
            self.health_score_label.setText(f"{self.health_score:.0f}%")
            self.health_bar.setValue(int(self.health_score))
            
            # Colorir barra baseado no score
            if self.health_score >= 80:
                color = "#4CAF50"  # Verde
            elif self.health_score >= 50:
                color = "#FFA500"  # Laranja
            else:
                color = "#F44336"  # Vermelho
            
            self.health_bar.setStyleSheet(f"""
                QProgressBar::chunk {{
                    background-color: {color};
                }}
            """)
    
    def handle_anomaly(self, anomalies: list):
        """Trata anomalias detectadas"""
        for anomaly in anomalies:
            severity = anomaly.get('severity', 'info')
            description = anomaly.get('description', 'Anomalia detectada')
            
            self.log_event(description, severity)
            
            # Mostrar no painel de anomalias ao invés de popup
            self.show_anomaly_in_panel(anomaly)
    
    def log_event(self, message: str, severity: str = "info"):
        """Adiciona evento ao log visual"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Cores por severidade
        colors = {
            'info': '#0000FF',
            'warning': '#FFA500',
            'critical': '#FF4500',
            'emergency': '#FF0000'
        }
        
        color = colors.get(severity, '#000000')
        
        html = f'<span style="color: {color};"><b>[{timestamp}]</b> {message}</span><br>'
        self.events_text.insertHtml(html)
        
        # Auto-scroll
        scrollbar = self.events_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def show_anomaly_in_panel(self, anomaly: dict):
        """Mostra anomalia no painel de alertas"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        severity = anomaly.get('severity', 'info')
        description = anomaly.get('description', 'Anomalia detectada')
        value = anomaly.get('value', 'N/A')
        threshold = anomaly.get('threshold', 'N/A')
        joint = anomaly.get('joint', '')
        
        # Ícones e cores por severidade
        severity_config = {
            'emergency': {'icon': '🔴', 'label': 'EMERGÊNCIA', 'color': '#DC143C'},
            'critical': {'icon': '🟠', 'label': 'CRÍTICO', 'color': '#FF4500'},
            'warning': {'icon': '🟡', 'label': 'ALERTA', 'color': '#FFA500'},
            'info': {'icon': 'ℹ️', 'label': 'INFO', 'color': '#0000FF'}
        }
        
        config = severity_config.get(severity, severity_config['info'])
        
        # Formatar mensagem
        joint_info = f" [Junta {joint}]" if joint else ""
        value_info = f"\n   Valor: {value} | Limite: {threshold}" if value != 'N/A' else ""
        
        html = f'''
        <div style="border-left: 4px solid {config['color']}; padding: 8px; margin: 5px 0; background-color: white;">
            <b style="color: {config['color']};">[{timestamp}] {config['icon']} {config['label']}{joint_info}</b><br>
            <span style="margin-left: 10px;">{description}</span>{value_info}
        </div>
        '''
        
        self.anomalies_text.insertHtml(html)
        
        # Auto-scroll
        scrollbar = self.anomalies_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Fazer o painel piscar se for crítico ou emergência
        if severity in ['critical', 'emergency']:
            self.flash_anomaly_panel()
    
    def flash_anomaly_panel(self):
        """Faz o painel de anomalias piscar para chamar atenção"""
        # Criar efeito de flash alterando o estilo temporariamente
        original_style = self.anomalies_text.styleSheet()
        flash_style = """
            QTextEdit {
                background-color: #FFE5E5;
                border: 3px solid #FF0000;
                font-family: 'Courier New';
                font-size: 11px;
            }
        """
        
        self.anomalies_text.setStyleSheet(flash_style)
        
        # Restaurar estilo original após 500ms
        QTimer.singleShot(500, lambda: self.anomalies_text.setStyleSheet(original_style))
    
    def clear_anomalies(self):
        """Limpa o painel de anomalias"""
        self.anomalies_text.clear()
        self.status_bar.showMessage("Painel de anomalias limpo")
    
    def load_events(self):
        """Carrega eventos do banco de dados"""
        events = self.db_manager.get_events(hours=24)
        
        self.events_table.setRowCount(len(events))
        
        for i, event in enumerate(events):
            timestamp = datetime.fromisoformat(event['timestamp']).strftime("%d/%m/%Y %H:%M:%S")
            self.events_table.setItem(i, 0, QTableWidgetItem(timestamp))
            self.events_table.setItem(i, 1, QTableWidgetItem(event.get('severity', 'N/A')))
            self.events_table.setItem(i, 2, QTableWidgetItem(event.get('event_type', 'N/A')))
            self.events_table.setItem(i, 3, QTableWidgetItem(event.get('description', 'N/A')))
            self.events_table.setItem(i, 4, QTableWidgetItem(f"{event.get('duration', 0):.1f}"))
        
        self.status_bar.showMessage(f"{len(events)} eventos carregados")
    
    def generate_pdf_report(self):
        """Gera relatório PDF"""
        try:
            self.status_bar.showMessage("Gerando relatório PDF...")
            pdf_path = self.report_generator.generate_full_report(hours=24)
            
            QMessageBox.information(self, "Sucesso", f"Relatório gerado:\n{pdf_path}")
            self.status_bar.showMessage(f"Relatório PDF gerado: {pdf_path}")
            
            # Abrir pasta
            os.startfile(os.path.dirname(pdf_path))
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório: {e}")
            self.status_bar.showMessage("Erro ao gerar relatório")
    
    def export_excel(self):
        """Exporta dados para Excel"""
        try:
            self.status_bar.showMessage("Exportando para Excel...")
            excel_path = self.report_generator.export_to_excel(hours=24)
            
            QMessageBox.information(self, "Sucesso", f"Dados exportados:\n{excel_path}")
            self.status_bar.showMessage(f"Dados exportados: {excel_path}")
            
            # Abrir pasta
            os.startfile(os.path.dirname(excel_path))
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar: {e}")
            self.status_bar.showMessage("Erro ao exportar dados")
    
    def closeEvent(self, event):
        """Trata fechamento da janela"""
        if self.monitor_thread.running:
            self.monitor_thread.stop()
            self.monitor_thread.wait()
        
        self.db_manager.close()
        event.accept()


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
