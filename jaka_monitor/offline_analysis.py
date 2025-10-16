"""
Script de Análise Offline
Analisa dados já coletados no banco de dados
Útil para gerar análises customizadas para artigos
"""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import sys

# Adicionar path do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config


class OfflineAnalyzer:
    """Analisador de dados offline"""
    
    def __init__(self, db_path: str = None):
        """Inicializa o analisador"""
        self.db_path = db_path or config.DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        
        # Configurar estilo de plots
        sns.set_style("darkgrid")
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 10
    
    def get_data_summary(self):
        """Obtém resumo dos dados disponíveis"""
        print("=" * 70)
        print("RESUMO DOS DADOS COLETADOS")
        print("=" * 70)
        
        # Total de registros
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM robot_data")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM robot_data")
        start_time, end_time = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE severity='critical' OR severity='emergency'")
        critical_events = cursor.fetchone()[0]
        
        print(f"\nRegistros Totais: {total_records}")
        print(f"Período: {start_time} até {end_time}")
        print(f"Total de Eventos: {total_events}")
        print(f"Eventos Críticos: {critical_events}")
        print()
        
        # Eventos por severidade
        cursor.execute("""
            SELECT severity, COUNT(*) 
            FROM events 
            GROUP BY severity
        """)
        
        print("Eventos por Severidade:")
        for severity, count in cursor.fetchall():
            print(f"  {severity.upper()}: {count}")
        
        print("=" * 70)
        print()
    
    def analyze_joint_trends(self, joint_number: int = None, hours: int = 24):
        """
        Analisa tendências de uma junta específica
        
        Args:
            joint_number: Número da junta (1-6), None = todas
            hours: Janela de tempo
        """
        print(f"\nAnalisando tendências das juntas (últimas {hours}h)...")
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        query = """
            SELECT timestamp, joint_number, temperature, current, torque, velocity
            FROM joint_data
            WHERE timestamp >= ?
        """
        
        params = [start_time.isoformat()]
        
        if joint_number:
            query += " AND joint_number = ?"
            params.append(joint_number)
        
        query += " ORDER BY timestamp"
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        if df.empty:
            print("⚠️  Nenhum dado encontrado para o período especificado")
            return
        
        print(f"✓ {len(df)} registros encontrados")
        
        # Estatísticas por junta
        stats = df.groupby('joint_number').agg({
            'temperature': ['mean', 'std', 'min', 'max'],
            'current': ['mean', 'std', 'min', 'max'],
            'torque': ['mean', 'std', 'min', 'max']
        }).round(3)
        
        print("\n📊 ESTATÍSTICAS POR JUNTA:")
        print(stats)
        
        # Criar gráficos
        self._plot_joint_analysis(df, joint_number)
    
    def _plot_joint_analysis(self, df: pd.DataFrame, joint_number: int = None):
        """Cria gráficos de análise das juntas"""
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Converter timestamp para datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        joints_to_plot = [joint_number] if joint_number else range(1, 7)
        
        # Temperatura
        for joint in joints_to_plot:
            joint_df = df[df['joint_number'] == joint]
            axes[0].plot(joint_df['timestamp'], joint_df['temperature'], 
                        label=f'Junta {joint}', marker='o', markersize=3, alpha=0.7)
        
        axes[0].axhline(y=config.THRESHOLDS['joint_temperature_warning'], 
                       color='orange', linestyle='--', label='Limite Alerta', linewidth=2)
        axes[0].axhline(y=config.THRESHOLDS['joint_temperature_critical'], 
                       color='red', linestyle='--', label='Limite Crítico', linewidth=2)
        axes[0].set_ylabel('Temperatura (°C)', fontsize=12)
        axes[0].set_title('Evolução da Temperatura das Juntas', fontsize=14, fontweight='bold')
        axes[0].legend(loc='best', ncol=2)
        axes[0].grid(True, alpha=0.3)
        
        # Corrente
        for joint in joints_to_plot:
            joint_df = df[df['joint_number'] == joint]
            axes[1].plot(joint_df['timestamp'], joint_df['current'].abs(), 
                        label=f'Junta {joint}', marker='o', markersize=3, alpha=0.7)
        
        axes[1].axhline(y=config.THRESHOLDS['joint_current_warning'], 
                       color='orange', linestyle='--', label='Limite Alerta', linewidth=2)
        axes[1].axhline(y=config.THRESHOLDS['joint_current_critical'], 
                       color='red', linestyle='--', label='Limite Crítico', linewidth=2)
        axes[1].set_ylabel('Corrente (A)', fontsize=12)
        axes[1].set_title('Evolução da Corrente das Juntas', fontsize=14, fontweight='bold')
        axes[1].legend(loc='best', ncol=2)
        axes[1].grid(True, alpha=0.3)
        
        # Torque
        for joint in joints_to_plot:
            joint_df = df[df['joint_number'] == joint]
            axes[2].plot(joint_df['timestamp'], joint_df['torque'].abs(), 
                        label=f'Junta {joint}', marker='o', markersize=3, alpha=0.7)
        
        axes[2].axhline(y=config.THRESHOLDS['joint_torque_warning'], 
                       color='orange', linestyle='--', label='Limite Alerta', linewidth=2)
        axes[2].axhline(y=config.THRESHOLDS['joint_torque_critical'], 
                       color='red', linestyle='--', label='Limite Crítico', linewidth=2)
        axes[2].set_xlabel('Data/Hora', fontsize=12)
        axes[2].set_ylabel('Torque', fontsize=12)
        axes[2].set_title('Evolução do Torque das Juntas', fontsize=14, fontweight='bold')
        axes[2].legend(loc='best', ncol=2)
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar
        output_file = f"reports/analise_juntas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs('reports', exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Gráfico salvo: {output_file}")
        
        plt.show()
    
    def detect_wear_patterns(self, hours: int = 24):
        """
        Detecta padrões de desgaste através de análise de tendências
        
        Args:
            hours: Janela de tempo para análise
        """
        print(f"\n🔍 DETECTANDO PADRÕES DE DESGASTE (últimas {hours}h)...")
        print()
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        query = """
            SELECT timestamp, joint_number, temperature, current, torque
            FROM joint_data
            WHERE timestamp >= ?
            ORDER BY timestamp
        """
        
        df = pd.read_sql_query(query, self.conn, params=[start_time.isoformat()])
        
        if df.empty:
            print("⚠️  Nenhum dado disponível")
            return
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Analisar cada junta
        for joint in range(1, 7):
            joint_df = df[df['joint_number'] == joint].sort_values('timestamp')
            
            if len(joint_df) < 10:
                continue
            
            # Dividir em duas metades
            mid = len(joint_df) // 2
            first_half = joint_df.iloc[:mid]
            second_half = joint_df.iloc[mid:]
            
            # Calcular médias
            temp_first = first_half['temperature'].mean()
            temp_second = second_half['temperature'].mean()
            temp_increase = temp_second - temp_first
            
            current_first = first_half['current'].abs().mean()
            current_second = second_half['current'].abs().mean()
            current_increase = current_second - current_first
            
            torque_first = first_half['torque'].abs().mean()
            torque_second = second_half['torque'].abs().mean()
            torque_increase = torque_second - torque_first
            
            # Detectar desgaste significativo
            wear_indicators = []
            
            if temp_increase > 2.0:  # Aumento de >2°C
                wear_indicators.append(f"Temperatura: +{temp_increase:.1f}°C")
            
            if current_increase > 0.3:  # Aumento de >0.3A
                wear_indicators.append(f"Corrente: +{current_increase:.2f}A")
            
            if torque_increase > 0.2:  # Aumento de >0.2
                wear_indicators.append(f"Torque: +{torque_increase:.2f}")
            
            if wear_indicators:
                print(f"⚠️  JUNTA {joint} - Sinais de desgaste detectados:")
                for indicator in wear_indicators:
                    print(f"    • {indicator}")
                print()
    
    def export_for_paper(self, hours: int = 24, output_dir: str = "reports"):
        """
        Exporta dados formatados para uso em artigo científico
        
        Args:
            hours: Janela de tempo
            output_dir: Diretório de saída
        """
        print(f"\n📄 Exportando dados para artigo científico...")
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Estatísticas descritivas
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        query = """
            SELECT joint_number, temperature, current, voltage, torque
            FROM joint_data
            WHERE timestamp >= ?
        """
        
        df = pd.read_sql_query(query, self.conn, params=[start_time.isoformat()])
        
        stats = df.groupby('joint_number').agg({
            'temperature': ['count', 'mean', 'std', 'min', 'max'],
            'current': ['mean', 'std', 'min', 'max'],
            'torque': ['mean', 'std', 'min', 'max']
        }).round(3)
        
        stats_file = os.path.join(output_dir, f'statistics_paper_{timestamp}.csv')
        stats.to_csv(stats_file)
        print(f"✓ Estatísticas salvas: {stats_file}")
        
        # 2. Dados de eventos
        query_events = """
            SELECT severity, event_type, COUNT(*) as count
            FROM events
            WHERE timestamp >= ?
            GROUP BY severity, event_type
        """
        
        df_events = pd.read_sql_query(query_events, self.conn, params=[start_time.isoformat()])
        events_file = os.path.join(output_dir, f'events_summary_{timestamp}.csv')
        df_events.to_csv(events_file, index=False)
        print(f"✓ Resumo de eventos salvo: {events_file}")
        
        # 3. Dados brutos selecionados (amostragem)
        query_raw = """
            SELECT * FROM joint_data
            WHERE timestamp >= ?
            ORDER BY timestamp
        """
        
        df_raw = pd.read_sql_query(query_raw, self.conn, params=[start_time.isoformat()])
        
        # Amostrar (pegar 1 a cada 10 registros para reduzir tamanho)
        df_sampled = df_raw.iloc[::10]
        raw_file = os.path.join(output_dir, f'raw_data_sampled_{timestamp}.csv')
        df_sampled.to_csv(raw_file, index=False)
        print(f"✓ Dados brutos (amostrados) salvos: {raw_file}")
        
        print(f"\n✅ Exportação concluída! Arquivos em: {output_dir}/")
    
    def close(self):
        """Fecha conexão com banco de dados"""
        self.conn.close()


def main():
    """Função principal"""
    print("=" * 70)
    print("ANÁLISE OFFLINE - Sistema de Monitoramento JAKA")
    print("=" * 70)
    
    analyzer = OfflineAnalyzer()
    
    try:
        # 1. Resumo dos dados
        analyzer.get_data_summary()
        
        # 2. Análise de tendências
        print("\n" + "=" * 70)
        analyzer.analyze_joint_trends(hours=24)
        
        # 3. Detecção de desgaste
        print("\n" + "=" * 70)
        analyzer.detect_wear_patterns(hours=24)
        
        # 4. Exportar para artigo
        print("\n" + "=" * 70)
        analyzer.export_for_paper(hours=24)
        
        print("\n" + "=" * 70)
        print("✅ Análise concluída com sucesso!")
        print("=" * 70)
    
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
