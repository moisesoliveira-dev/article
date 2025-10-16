"""
Módulo de Gerenciamento de Banco de Dados
Armazena todos os dados recebidos e eventos detectados
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os


class DatabaseManager:
    """Gerencia o banco de dados SQLite para armazenamento de dados do robô"""
    
    def __init__(self, db_path: str):
        """
        Inicializa o gerenciador do banco de dados
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Conecta ao banco de dados"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
    
    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        cursor = self.conn.cursor()
        
        # Tabela principal de dados do robô
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS robot_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                robot_id INTEGER,
                robot_name TEXT,
                task_state INTEGER,
                task_mode INTEGER,
                enabled BOOLEAN,
                powered_on INTEGER,
                emergency_stop INTEGER,
                protective_stop INTEGER,
                on_soft_limit INTEGER,
                robot_temp REAL,
                ambient_temp REAL,
                current_tool_id INTEGER,
                tcp_velocity REAL,
                json_data TEXT
            )
        """)
        
        # Tabela de dados das juntas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS joint_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                robot_data_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                joint_number INTEGER,
                position REAL,
                actual_position REAL,
                velocity REAL,
                current REAL,
                temperature REAL,
                voltage REAL,
                torque REAL,
                error_status REAL,
                FOREIGN KEY (robot_data_id) REFERENCES robot_data(id)
            )
        """)
        
        # Tabela de eventos/anomalias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                severity TEXT,
                joint_number INTEGER,
                description TEXT,
                value REAL,
                threshold REAL,
                duration REAL,
                resolved BOOLEAN DEFAULT 0,
                resolved_at DATETIME
            )
        """)
        
        # Tabela de posições TCP
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tcp_positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                robot_data_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                x REAL,
                y REAL,
                z REAL,
                rx REAL,
                ry REAL,
                rz REAL,
                actual_x REAL,
                actual_y REAL,
                actual_z REAL,
                actual_rx REAL,
                actual_ry REAL,
                actual_rz REAL,
                FOREIGN KEY (robot_data_id) REFERENCES robot_data(id)
            )
        """)
        
        # Tabela de estatísticas agregadas (para performance)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                period_start DATETIME,
                period_end DATETIME,
                joint_number INTEGER,
                avg_temperature REAL,
                max_temperature REAL,
                avg_current REAL,
                max_current REAL,
                avg_velocity REAL,
                max_velocity REAL,
                avg_torque REAL,
                max_torque REAL
            )
        """)
        
        # Índices para melhor performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_robot_data_timestamp ON robot_data(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_joint_data_timestamp ON joint_data(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_resolved ON events(resolved)")
        
        self.conn.commit()
    
    def insert_robot_data(self, data: Dict[str, Any]) -> int:
        """
        Insere dados completos do robô
        
        Args:
            data: Dicionário com os dados do robô
            
        Returns:
            ID do registro inserido
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO robot_data (
                robot_id, robot_name, task_state, task_mode, enabled,
                powered_on, emergency_stop, protective_stop, on_soft_limit,
                robot_temp, ambient_temp, current_tool_id, tcp_velocity, json_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("ID"),
            data.get("NOME"),
            data.get("task_state"),
            data.get("task_mode"),
            data.get("enabled"),
            data.get("powered_on"),
            data.get("emergency_stop"),
            data.get("protective_stop"),
            data.get("on_soft_limit"),
            data.get("monitor_data", [None, None, None])[2] if len(data.get("monitor_data", [])) > 2 else None,
            data.get("monitor_data", [None, None, None, None])[3] if len(data.get("monitor_data", [])) > 3 else None,
            data.get("current_tool_id"),
            data.get("curr_tcp_trans_vel"),
            json.dumps(data)
        ))
        
        robot_data_id = cursor.lastrowid
        
        # Inserir dados das juntas
        self._insert_joint_data(robot_data_id, data)
        
        # Inserir posições TCP
        self._insert_tcp_position(robot_data_id, data)
        
        self.conn.commit()
        return robot_data_id
    
    def _insert_joint_data(self, robot_data_id: int, data: Dict[str, Any]):
        """Insere dados individuais das juntas"""
        cursor = self.conn.cursor()
        
        monitor_data = data.get("monitor_data", [])
        if len(monitor_data) > 5 and isinstance(monitor_data[5], list):
            joint_positions = data.get("joint_position", [])
            joint_actual_positions = data.get("joint_actual_position", [])
            joint_velocities = data.get("instVel", [])
            
            for i, joint_monitor in enumerate(monitor_data[5]):
                if isinstance(joint_monitor, list) and len(joint_monitor) >= 8:
                    cursor.execute("""
                        INSERT INTO joint_data (
                            robot_data_id, joint_number, position, actual_position,
                            velocity, current, temperature, voltage, torque, error_status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        robot_data_id,
                        i + 1,
                        joint_positions[i] if i < len(joint_positions) else None,
                        joint_actual_positions[i] if i < len(joint_actual_positions) else None,
                        joint_velocities[i] if i < len(joint_velocities) else None,
                        joint_monitor[0],  # current
                        joint_monitor[1],  # temperature
                        joint_monitor[2],  # voltage
                        joint_monitor[7],  # torque
                        joint_monitor[3]   # error_status
                    ))
    
    def _insert_tcp_position(self, robot_data_id: int, data: Dict[str, Any]):
        """Insere posição TCP"""
        cursor = self.conn.cursor()
        
        position = data.get("position", [])
        actual_position = data.get("actual_position", [])
        
        if len(position) >= 6:
            cursor.execute("""
                INSERT INTO tcp_positions (
                    robot_data_id, x, y, z, rx, ry, rz,
                    actual_x, actual_y, actual_z, actual_rx, actual_ry, actual_rz
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                robot_data_id,
                position[0], position[1], position[2],
                position[3], position[4], position[5],
                actual_position[0] if len(actual_position) > 0 else None,
                actual_position[1] if len(actual_position) > 1 else None,
                actual_position[2] if len(actual_position) > 2 else None,
                actual_position[3] if len(actual_position) > 3 else None,
                actual_position[4] if len(actual_position) > 4 else None,
                actual_position[5] if len(actual_position) > 5 else None,
            ))
    
    def insert_event(self, event_type: str, severity: str, description: str, 
                    joint_number: Optional[int] = None, value: Optional[float] = None,
                    threshold: Optional[float] = None, duration: Optional[float] = None):
        """
        Insere um evento/anomalia
        
        Args:
            event_type: Tipo do evento
            severity: Severidade (info, warning, critical, emergency)
            description: Descrição do evento
            joint_number: Número da junta (se aplicável)
            value: Valor medido
            threshold: Limiar ultrapassado
            duration: Duração da anomalia em segundos
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO events (
                event_type, severity, joint_number, description,
                value, threshold, duration
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (event_type, severity, joint_number, description, value, threshold, duration))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_data(self, minutes: int = 60) -> List[Dict]:
        """Obtém dados recentes do robô"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM robot_data
            WHERE timestamp >= datetime('now', '-' || ? || ' minutes')
            ORDER BY timestamp DESC
        """, (minutes,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_joint_data_range(self, start_time: str, end_time: str, joint_number: Optional[int] = None) -> List[Dict]:
        """Obtém dados das juntas em um intervalo de tempo"""
        cursor = self.conn.cursor()
        
        if joint_number is not None:
            cursor.execute("""
                SELECT * FROM joint_data
                WHERE timestamp BETWEEN ? AND ?
                AND joint_number = ?
                ORDER BY timestamp
            """, (start_time, end_time, joint_number))
        else:
            cursor.execute("""
                SELECT * FROM joint_data
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp, joint_number
            """, (start_time, end_time))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_events(self, severity: Optional[str] = None, resolved: Optional[bool] = None,
                   hours: int = 24) -> List[Dict]:
        """Obtém eventos registrados"""
        cursor = self.conn.cursor()
        
        query = """
            SELECT * FROM events
            WHERE timestamp >= datetime('now', '-' || ? || ' hours')
        """
        params = [hours]
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        
        if resolved is not None:
            query += " AND resolved = ?"
            params.append(1 if resolved else 0)
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self, hours: int = 24) -> Dict[int, Dict[str, float]]:
        """Calcula estatísticas das juntas"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                joint_number,
                AVG(temperature) as avg_temp,
                MAX(temperature) as max_temp,
                AVG(current) as avg_current,
                MAX(current) as max_current,
                AVG(ABS(velocity)) as avg_velocity,
                MAX(ABS(velocity)) as max_velocity,
                AVG(torque) as avg_torque,
                MAX(torque) as max_torque
            FROM joint_data
            WHERE timestamp >= datetime('now', '-' || ? || ' hours')
            GROUP BY joint_number
        """, (hours,))
        
        stats = {}
        for row in cursor.fetchall():
            stats[row[0]] = {
                'avg_temp': row[1],
                'max_temp': row[2],
                'avg_current': row[3],
                'max_current': row[4],
                'avg_velocity': row[5],
                'max_velocity': row[6],
                'avg_torque': row[7],
                'max_torque': row[8]
            }
        
        return stats
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
