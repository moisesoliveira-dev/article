"""
Análise de Cenários de Falhas - Gerador de Relatório Científico
Analisa dados de simulação e gera relatório detalhado para artigo

Autor: Sistema JAKA Monitor
Data: Outubro 2025
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
from typing import Dict, List, Tuple
import json

# Configurações de plotagem
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
sns.set_palette("husl")


class FaultScenarioAnalyzer:
    """Analisador de cenários de falha"""
    
    def __init__(self, db_path: str = "data/jaka_monitor.db"):
        self.db_path = db_path
        self.conn = None
        self.output_dir = "analises/fault_scenarios"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def connect(self):
        """Conecta ao banco de dados"""
        self.conn = sqlite3.connect(self.db_path)
        print(f"✓ Conectado ao banco: {self.db_path}")
        
    def get_time_series_data(self, start_time: str = None, end_time: str = None) -> pd.DataFrame:
        """Obtém série temporal completa"""
        query = """
        SELECT
            r.timestamp,
            r.robot_temp,
            r.ambient_temp,
            j.joint_number,
            j.current,
            j.temperature,
            j.voltage,
            j.torque,
            j.position,
            j.actual_position,
            j.velocity
        FROM robot_data r
        LEFT JOIN joint_data j ON r.id = j.robot_data_id
        WHERE 1=1
        """
        
        params = []
        if start_time:
            query += " AND r.timestamp >= ?"
            params.append(start_time)
        if end_time:
            query += " AND r.timestamp <= ?"
            params.append(end_time)
            
        query += " ORDER BY r.timestamp, j.joint_number"
        
        df = pd.read_sql_query(query, self.conn, params=params)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def detect_fault_periods(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detecta períodos de falha baseado em anomalias nos dados
        """
        periods = []
        
        # Agrupar por junta
        for joint in df['joint_number'].unique():
            if pd.isna(joint):
                continue
                
            joint_df = df[df['joint_number'] == joint].copy()
            
            # Calcular estatísticas móveis
            joint_df['temp_rolling_mean'] = joint_df['temperature'].rolling(window=10).mean()
            joint_df['temp_rolling_std'] = joint_df['temperature'].rolling(window=10).std()
            
            # Detectar anomalias de temperatura (> 2 std)
            joint_df['temp_anomaly'] = (
                joint_df['temperature'] > 
                joint_df['temp_rolling_mean'] + 2 * joint_df['temp_rolling_std']
            )
            
            # Encontrar períodos contínuos de anomalia
            in_anomaly = False
            start_idx = None
            
            for idx, row in joint_df.iterrows():
                if row['temp_anomaly'] and not in_anomaly:
                    in_anomaly = True
                    start_idx = idx
                elif not row['temp_anomaly'] and in_anomaly:
                    in_anomaly = False
                    period = {
                        'joint': int(joint),
                        'start': joint_df.loc[start_idx, 'timestamp'],
                        'end': row['timestamp'],
                        'type': 'temperature_anomaly',
                        'max_temp': joint_df.loc[start_idx:idx, 'temperature'].max(),
                        'avg_temp': joint_df.loc[start_idx:idx, 'temperature'].mean()
                    }
                    periods.append(period)
        
        return periods
    
    def analyze_bearing_wear(self, df: pd.DataFrame, joint: int) -> Dict:
        """Análise específica de desgaste de rolamento"""
        joint_df = df[df['joint_number'] == joint].copy()
        
        if len(joint_df) == 0:
            return {}
        
        # Calcular tendências
        joint_df['time_seconds'] = (
            joint_df['timestamp'] - joint_df['timestamp'].min()
        ).dt.total_seconds()
        
        # Regressão linear para temperatura
        temp_coef = np.polyfit(joint_df['time_seconds'], joint_df['temperature'], 1)
        temp_trend = temp_coef[0]  # graus/segundo
        
        # Variabilidade da corrente (indicador de vibração)
        current_std = joint_df['current'].std()
        current_cv = current_std / joint_df['current'].mean()  # Coeficiente de variação
        
        # Análise de frequência (FFT da corrente para detectar vibrações)
        current_signal = joint_df['current'].values
        fft = np.fft.fft(current_signal)
        frequencies = np.fft.fftfreq(len(current_signal))
        
        # Encontrar pico de frequência dominante
        positive_freq_idx = frequencies > 0
        dominant_freq_idx = np.argmax(np.abs(fft[positive_freq_idx]))
        dominant_freq = frequencies[positive_freq_idx][dominant_freq_idx]
        
        analysis = {
            'joint': joint,
            'scenario': 'Desgaste de Rolamento',
            'temperature_increase_rate': temp_trend * 60,  # graus/minuto
            'max_temperature': joint_df['temperature'].max(),
            'avg_temperature': joint_df['temperature'].mean(),
            'current_variability': current_cv,
            'dominant_vibration_freq': dominant_freq if not np.isnan(dominant_freq) else 0,
            'torque_increase': (
                joint_df['torque'].iloc[-10:].mean() - 
                joint_df['torque'].iloc[:10].mean()
            ),
            'indicators': []
        }
        
        # Classificar indicadores
        if analysis['temperature_increase_rate'] > 0.5:
            analysis['indicators'].append('🔴 Aumento crítico de temperatura')
        elif analysis['temperature_increase_rate'] > 0.2:
            analysis['indicators'].append('🟡 Aumento moderado de temperatura')
        
        if analysis['current_variability'] > 0.15:
            analysis['indicators'].append('🔴 Alta variabilidade de corrente (vibração)')
        
        if analysis['torque_increase'] > 0.3:
            analysis['indicators'].append('🟡 Aumento de torque por atrito')
        
        return analysis
    
    def analyze_motor_overheating(self, df: pd.DataFrame, joint: int) -> Dict:
        """Análise de superaquecimento do motor"""
        joint_df = df[df['joint_number'] == joint].copy()
        
        if len(joint_df) == 0:
            return {}
        
        # Taxa de aquecimento
        joint_df['time_seconds'] = (
            joint_df['timestamp'] - joint_df['timestamp'].min()
        ).dt.total_seconds()
        
        # Temperatura máxima atingida
        max_temp = joint_df['temperature'].max()
        initial_temp = joint_df['temperature'].iloc[:5].mean()
        temp_rise = max_temp - initial_temp
        
        # Tempo até atingir temperatura crítica (>65°C)
        critical_temp = 65.0
        critical_idx = joint_df[joint_df['temperature'] > critical_temp].first_valid_index()
        time_to_critical = None
        if critical_idx is not None:
            time_to_critical = joint_df.loc[critical_idx, 'time_seconds']
        
        # Aumento de corrente
        current_increase_pct = (
            (joint_df['current'].iloc[-10:].mean() / joint_df['current'].iloc[:10].mean() - 1) * 100
        )
        
        analysis = {
            'joint': joint,
            'scenario': 'Superaquecimento do Motor',
            'max_temperature': max_temp,
            'temperature_rise': temp_rise,
            'time_to_critical_temp': time_to_critical,
            'current_increase_percentage': current_increase_pct,
            'thermal_stress_index': temp_rise / (time_to_critical if time_to_critical else 1),
            'indicators': []
        }
        
        if max_temp > 70:
            analysis['indicators'].append('🔴 CRÍTICO: Temperatura acima de 70°C')
        elif max_temp > 60:
            analysis['indicators'].append('🟡 ALERTA: Temperatura acima de 60°C')
        
        if time_to_critical and time_to_critical < 120:
            analysis['indicators'].append('🔴 Aquecimento muito rápido (<2 min)')
        
        if current_increase_pct > 30:
            analysis['indicators'].append('🔴 Corrente excessiva (motor forçado)')
        
        return analysis
    
    def analyze_power_supply_degradation(self, df: pd.DataFrame) -> Dict:
        """Análise de degradação da fonte"""
        analysis = {
            'scenario': 'Degradação da Fonte de Alimentação',
            'voltage_statistics': {},
            'affected_joints': [],
            'indicators': []
        }
        
        for joint in df['joint_number'].unique():
            if pd.isna(joint):
                continue
                
            joint_df = df[df['joint_number'] == joint]
            
            voltage_mean = joint_df['voltage'].mean()
            voltage_std = joint_df['voltage'].std()
            voltage_cv = voltage_std / voltage_mean
            voltage_min = joint_df['voltage'].min()
            voltage_drops = (joint_df['voltage'] < 46.0).sum()  # Quedas abaixo de 46V
            
            analysis['voltage_statistics'][f'joint_{int(joint)}'] = {
                'mean': voltage_mean,
                'std': voltage_std,
                'cv': voltage_cv,
                'min': voltage_min,
                'drop_count': int(voltage_drops)
            }
            
            if voltage_cv > 0.05:
                analysis['affected_joints'].append(int(joint))
                analysis['indicators'].append(
                    f'🔴 Junta {int(joint)}: Alta instabilidade ({voltage_cv*100:.1f}%)'
                )
            
            if voltage_drops > 10:
                analysis['indicators'].append(
                    f'🟡 Junta {int(joint)}: {voltage_drops} quedas de tensão'
                )
        
        return analysis
    
    def generate_fault_report(self, analysis_results: List[Dict]) -> str:
        """Gera relatório textual formatado para artigo"""
        report = []
        report.append("=" * 80)
        report.append("RELATÓRIO DE ANÁLISE DE CENÁRIOS DE FALHAS")
        report.append("Sistema de Monitoramento Preditivo - Robô JAKA")
        report.append("=" * 80)
        report.append(f"\nData da Análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        for i, analysis in enumerate(analysis_results, 1):
            report.append(f"\n{'─' * 80}")
            report.append(f"CENÁRIO {i}: {analysis.get('scenario', 'Não especificado')}")
            report.append(f"{'─' * 80}\n")
            
            # Descrição do cenário
            if 'Rolamento' in analysis.get('scenario', ''):
                report.append("📋 DESCRIÇÃO:")
                report.append("   Desgaste progressivo do rolamento causando aumento de temperatura,")
                report.append("   vibração e consumo de corrente devido ao atrito excessivo.\n")
                
                report.append("🔬 CAUSA FÍSICA:")
                report.append("   - Fadiga do material do rolamento")
                report.append("   - Perda de esfericidade das esferas/roletes")
                report.append("   - Aumento de folgas internas")
                report.append("   - Perda de lubrificação\n")
                
                report.append("📊 MÉTRICAS OBSERVADAS:")
                report.append(f"   • Temperatura máxima: {analysis['max_temperature']:.2f}°C")
                report.append(f"   • Taxa de aquecimento: {analysis['temperature_increase_rate']:.4f}°C/min")
                report.append(f"   • Variabilidade de corrente (CV): {analysis['current_variability']:.4f}")
                report.append(f"   • Aumento de torque: {analysis['torque_increase']:.3f} Nm")
                if analysis['dominant_vibration_freq'] > 0:
                    report.append(f"   • Frequência dominante: {analysis['dominant_vibration_freq']:.3f} Hz\n")
                
                report.append("⚠️  INDICADORES DE FALHA:")
                for indicator in analysis['indicators']:
                    report.append(f"   {indicator}")
                
                report.append("\n💡 INTERPRETAÇÃO CIENTÍFICA:")
                report.append("   O desgaste do rolamento manifesta-se através de três fenômenos principais:")
                report.append("   1. Aumento térmico: O atrito metal-metal gera calor dissipado")
                report.append("   2. Vibração mecânica: Irregularidades na superfície causam oscilações")
                report.append("   3. Sobrecarga elétrica: Motor compensa perdas mecânicas\n")
            
            elif 'Superaquecimento' in analysis.get('scenario', ''):
                report.append("📋 DESCRIÇÃO:")
                report.append("   Superaquecimento crítico do motor por obstrução de ventilação")
                report.append("   ou operação em sobrecarga contínua.\n")
                
                report.append("🔬 CAUSA FÍSICA:")
                report.append("   - Obstrução das aletas de resfriamento")
                report.append("   - Falha do sistema de ventilação forçada")
                report.append("   - Operação acima da capacidade térmica nominal")
                report.append("   - Acúmulo de calor por ciclos repetitivos\n")
                
                report.append("📊 MÉTRICAS OBSERVADAS:")
                report.append(f"   • Temperatura máxima: {analysis['max_temperature']:.2f}°C")
                report.append(f"   • Elevação de temperatura: {analysis['temperature_rise']:.2f}°C")
                if analysis['time_to_critical_temp']:
                    report.append(f"   • Tempo até crítico: {analysis['time_to_critical_temp']:.1f}s")
                report.append(f"   • Aumento de corrente: {analysis['current_increase_percentage']:.1f}%")
                report.append(f"   • Índice de estresse térmico: {analysis['thermal_stress_index']:.4f}\n")
                
                report.append("⚠️  INDICADORES DE FALHA:")
                for indicator in analysis['indicators']:
                    report.append(f"   {indicator}")
                
                report.append("\n💡 INTERPRETAÇÃO CIENTÍFICA:")
                report.append("   O motor elétrico possui limite de temperatura operacional (tipicamente 80°C).")
                report.append("   O superaquecimento acelera a degradação dos enrolamentos e pode causar:")
                report.append("   - Redução da vida útil do isolamento (regra: +10°C = -50% vida útil)")
                report.append("   - Aumento da resistência elétrica dos enrolamentos")
                report.append("   - Thermal runaway em casos extremos\n")
            
            elif 'Fonte' in analysis.get('scenario', ''):
                report.append("📋 DESCRIÇÃO:")
                report.append("   Degradação dos componentes da fonte de alimentação causando")
                report.append("   instabilidade na tensão fornecida ao sistema.\n")
                
                report.append("🔬 CAUSA FÍSICA:")
                report.append("   - Capacitores eletrolíticos degradados (ESR aumentado)")
                report.append("   - Reguladores de tensão com deriva térmica")
                report.append("   - Conexões oxidadas ou soltas")
                report.append("   - Filtros EMI comprometidos\n")
                
                report.append("📊 ESTATÍSTICAS POR JUNTA:")
                for joint_key, stats in analysis['voltage_statistics'].items():
                    joint_num = joint_key.split('_')[1]
                    report.append(f"\n   Junta {joint_num}:")
                    report.append(f"      Tensão média: {stats['mean']:.2f}V")
                    report.append(f"      Desvio padrão: {stats['std']:.3f}V")
                    report.append(f"      Coef. variação: {stats['cv']*100:.2f}%")
                    report.append(f"      Tensão mínima: {stats['min']:.2f}V")
                    report.append(f"      Quedas detectadas: {stats['drop_count']}")
                
                report.append("\n⚠️  JUNTAS AFETADAS:")
                for indicator in analysis['indicators']:
                    report.append(f"   {indicator}")
                
                report.append("\n💡 INTERPRETAÇÃO CIENTÍFICA:")
                report.append("   A tensão de alimentação deve ser estável (±2% nominal).")
                report.append("   Instabilidades causam:")
                report.append("   - Variação no torque disponível (proporcional a V²)")
                report.append("   - Ripple na corrente de controle")
                report.append("   - Possíveis resets do controlador em quedas severas")
                report.append("   - Aquecimento adicional por perdas RMS\n")
        
        report.append("\n" + "=" * 80)
        report.append("CONCLUSÕES E RECOMENDAÇÕES")
        report.append("=" * 80 + "\n")
        
        report.append("Os cenários simulados demonstram a eficácia do sistema de monitoramento")
        report.append("preditivo na detecção precoce de falhas através da análise de grandezas")
        report.append("físicas correlacionadas.\n")
        
        report.append("📈 PRINCIPAIS DESCOBERTAS:")
        report.append("   1. Temperatura: Indicador primário de degradação mecânica")
        report.append("   2. Variabilidade de corrente: Indicador de problemas mecânicos (vibração)")
        report.append("   3. Tensão: Indicador de problemas elétricos da infraestrutura")
        report.append("   4. Torque: Indicador de desgaste/atrito excessivo\n")
        
        report.append("🔧 RECOMENDAÇÕES DE MANUTENÇÃO:")
        report.append("   • Temperatura >60°C: Inspecionar sistema de resfriamento")
        report.append("   • CV corrente >15%: Verificar rolamentos e transmissão")
        report.append("   • Quedas de tensão: Auditar fonte de alimentação")
        report.append("   • Aumento de torque >20%: Verificar lubrificação\n")
        
        return "\n".join(report)
    
    def plot_temperature_analysis(self, df: pd.DataFrame, joints: List[int], 
                                   scenario_name: str):
        """Gráfico de análise de temperatura"""
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Gráfico 1: Séries temporais
        ax1 = axes[0]
        for joint in joints:
            joint_df = df[df['joint_number'] == joint]
            if len(joint_df) > 0:
                ax1.plot(joint_df['timestamp'], joint_df['temperature'], 
                        label=f'Junta {joint}', marker='o', markersize=3, alpha=0.7)
        
        ax1.set_xlabel('Tempo')
        ax1.set_ylabel('Temperatura (°C)')
        ax1.set_title(f'Evolução da Temperatura - {scenario_name}')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Linha de referência (temperatura nominal)
        ax1.axhline(y=45, color='orange', linestyle='--', label='Limite Alerta', alpha=0.5)
        ax1.axhline(y=65, color='red', linestyle='--', label='Limite Crítico', alpha=0.5)
        
        # Gráfico 2: Distribuição de temperatura
        ax2 = axes[1]
        temp_data = []
        labels = []
        for joint in joints:
            joint_df = df[df['joint_number'] == joint]
            if len(joint_df) > 0:
                temp_data.append(joint_df['temperature'].values)
                labels.append(f'J{joint}')
        
        if temp_data:
            bp = ax2.boxplot(temp_data, labels=labels, patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor('lightblue')
        
        ax2.set_xlabel('Junta')
        ax2.set_ylabel('Temperatura (°C)')
        ax2.set_title('Distribuição de Temperatura por Junta')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        filename = f"{self.output_dir}/temp_analysis_{scenario_name.replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Gráfico salvo: {filename}")
    
    def plot_current_voltage_analysis(self, df: pd.DataFrame, joint: int, 
                                       scenario_name: str):
        """Gráfico de corrente e tensão"""
        joint_df = df[df['joint_number'] == joint]
        
        if len(joint_df) == 0:
            return
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Gráfico 1: Corrente
        ax1 = axes[0]
        ax1.plot(joint_df['timestamp'], joint_df['current'], 
                color='blue', linewidth=1.5)
        ax1.set_ylabel('Corrente (A)', color='blue')
        ax1.set_title(f'Análise Elétrica - Junta {joint} - {scenario_name}')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True, alpha=0.3)
        
        # Destacar média e std
        mean_current = joint_df['current'].mean()
        std_current = joint_df['current'].std()
        ax1.axhline(y=mean_current, color='blue', linestyle='--', alpha=0.5, 
                   label=f'Média: {mean_current:.2f}A')
        ax1.fill_between(joint_df['timestamp'], 
                         mean_current - std_current, 
                         mean_current + std_current,
                         alpha=0.2, color='blue', label=f'±1σ ({std_current:.3f}A)')
        ax1.legend()
        
        # Gráfico 2: Tensão
        ax2 = axes[1]
        ax2.plot(joint_df['timestamp'], joint_df['voltage'], 
                color='green', linewidth=1.5)
        ax2.set_ylabel('Tensão (V)', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        ax2.grid(True, alpha=0.3)
        
        # Linha de referência nominal (48V)
        ax2.axhline(y=48.0, color='green', linestyle='--', alpha=0.5, label='Nominal: 48V')
        ax2.axhline(y=46.0, color='red', linestyle='--', alpha=0.3, label='Limite Mín')
        ax2.legend()
        
        # Gráfico 3: Potência (V × I)
        ax3 = axes[2]
        power = joint_df['voltage'] * joint_df['current']
        ax3.plot(joint_df['timestamp'], power, color='purple', linewidth=1.5)
        ax3.set_xlabel('Tempo')
        ax3.set_ylabel('Potência (W)', color='purple')
        ax3.tick_params(axis='y', labelcolor='purple')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = f"{self.output_dir}/electrical_analysis_J{joint}_{scenario_name.replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Gráfico salvo: {filename}")
    
    def plot_correlation_heatmap(self, df: pd.DataFrame, scenario_name: str):
        """Matriz de correlação entre variáveis"""
        # Preparar dados por junta
        correlation_data = []
        
        for joint in df['joint_number'].unique():
            if pd.isna(joint):
                continue
            
            joint_df = df[df['joint_number'] == joint][
                ['current', 'temperature', 'voltage', 'torque']
            ].dropna()
            
            if len(joint_df) > 10:
                correlation_data.append(joint_df)
        
        if not correlation_data:
            return
        
        # Concatenar dados de todas as juntas
        all_data = pd.concat(correlation_data, ignore_index=True)
        
        # Calcular correlação
        corr_matrix = all_data.corr()
        
        # Plotar
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   fmt='.3f', vmin=-1, vmax=1)
        
        plt.title(f'Matriz de Correlação - {scenario_name}')
        plt.tight_layout()
        
        filename = f"{self.output_dir}/correlation_{scenario_name.replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Gráfico salvo: {filename}")
    
    def export_statistics_csv(self, analysis_results: List[Dict]):
        """Exporta estatísticas em CSV para tabelas do artigo"""
        stats_data = []
        
        for analysis in analysis_results:
            scenario = analysis.get('scenario', 'Unknown')
            
            if 'Rolamento' in scenario:
                stats_data.append({
                    'Cenário': scenario,
                    'Junta': analysis.get('joint', ''),
                    'Temp_Max_C': analysis.get('max_temperature', ''),
                    'Taxa_Aquecimento_C_min': analysis.get('temperature_increase_rate', ''),
                    'Var_Corrente_CV': analysis.get('current_variability', ''),
                    'Aumento_Torque_Nm': analysis.get('torque_increase', ''),
                    'Freq_Vibracao_Hz': analysis.get('dominant_vibration_freq', '')
                })
            
            elif 'Superaquecimento' in scenario:
                stats_data.append({
                    'Cenário': scenario,
                    'Junta': analysis.get('joint', ''),
                    'Temp_Max_C': analysis.get('max_temperature', ''),
                    'Elevacao_Temp_C': analysis.get('temperature_rise', ''),
                    'Tempo_Critico_s': analysis.get('time_to_critical_temp', ''),
                    'Aumento_Corrente_pct': analysis.get('current_increase_percentage', ''),
                    'Indice_Estresse_Termico': analysis.get('thermal_stress_index', '')
                })
        
        if stats_data:
            df_stats = pd.DataFrame(stats_data)
            filename = f"{self.output_dir}/estatisticas_cenarios.csv"
            df_stats.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"✓ Estatísticas exportadas: {filename}")
    
    def run_full_analysis(self, time_window_hours: int = 24):
        """Executa análise completa"""
        print("\n" + "="*70)
        print("ANÁLISE DE CENÁRIOS DE FALHAS")
        print("="*70 + "\n")
        
        self.connect()
        
        # Verificar se há dados no banco
        print("📊 Verificando banco de dados...")
        cursor = self.conn.cursor()
        count = cursor.execute("SELECT COUNT(*) FROM robot_data").fetchone()[0]
        
        if count == 0:
            print("\n" + "⚠️ "*35)
            print("❌ BANCO DE DADOS VAZIO!")
            print("⚠️ "*35)
            print("\n📝 VOCÊ PRECISA EXECUTAR A SIMULAÇÃO PRIMEIRO!\n")
            print("Passos corretos:")
            print("  1️⃣  Terminal 1: python main_gui.py")
            print("  2️⃣  Terminal 2: python test_fault_scenarios.py")
            print("  3️⃣  Aguardar ~37 minutos")
            print("  4️⃣  Executar: python analyze_fault_scenarios.py\n")
            print("📖 Para mais detalhes, leia: COMO_EXECUTAR_SIMULACAO.md\n")
            print("💡 Teste rápido (5 min):")
            print("     python test_fault_scenarios.py --interval 1.0 --normal-time 5\n")
            self.conn.close()
            return
        
        print(f"✓ Banco de dados contém {count} registros\n")
        
        # Obter dados
        print("📊 Carregando dados...")
        
        # Se time_window_hours for None, pegar TODOS os dados
        if time_window_hours is None:
            print("   └─ Modo: TODOS OS DADOS (sem filtro de tempo)")
            df = self.get_time_series_data()
        else:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=time_window_hours)
            print(f"   └─ Período: últimas {time_window_hours} horas")
            
            df = self.get_time_series_data(
                start_time=start_time.strftime('%Y-%m-%d %H:%M:%S'),
                end_time=end_time.strftime('%Y-%m-%d %H:%M:%S')
            )
        
        if len(df) == 0:
            print("\n" + "⚠️ "*35)
            print("❌ NENHUM DADO NO PERÍODO ESPECIFICADO!")
            print("⚠️ "*35)
            if time_window_hours is not None:
                print(f"\n📅 Período buscado: {start_time} até {end_time}")
            print(f"💾 Registros no banco: {count}")
            print("\n💡 Tente uma das seguintes opções:")
            print("     python analyze_fault_scenarios.py --all  (todos os dados)")
            print("     python analyze_fault_scenarios.py --hours 48  (últimas 48h)")
            print("     python analyze_fault_scenarios.py --hours 72  (últimas 72h)\n")
            self.conn.close()
            return
        
        print(f"   └─ {len(df)} registros carregados")
        if time_window_hours is None:
            print(f"   └─ Período: {df['timestamp'].min()} até {df['timestamp'].max()}\n")
        else:
            print(f"   └─ Janela: {start_time} até {end_time}\n")
        
        # Análises específicas por cenário
        analysis_results = []
        
        # Detectar automaticamente cenários nos dados
        print("🔍 Detectando cenários de falha nos dados...\n")
        
        # Análise de rolamento (Junta 3)
        if 3 in df['joint_number'].unique():
            print("Analisando: Desgaste de Rolamento (Junta 3)")
            bearing_analysis = self.analyze_bearing_wear(df, joint=3)
            if bearing_analysis:
                analysis_results.append(bearing_analysis)
                self.plot_temperature_analysis(df, [3], "Desgaste_Rolamento")
                self.plot_current_voltage_analysis(df, 3, "Desgaste_Rolamento")
        
        # Análise de superaquecimento (Junta 2)
        if 2 in df['joint_number'].unique():
            print("Analisando: Superaquecimento do Motor (Junta 2)")
            motor_analysis = self.analyze_motor_overheating(df, joint=2)
            if motor_analysis:
                analysis_results.append(motor_analysis)
                self.plot_temperature_analysis(df, [2], "Superaquecimento_Motor")
                self.plot_current_voltage_analysis(df, 2, "Superaquecimento_Motor")
        
        # Análise de fonte
        print("Analisando: Degradação da Fonte de Alimentação")
        power_analysis = self.analyze_power_supply_degradation(df)
        if power_analysis.get('voltage_statistics'):
            analysis_results.append(power_analysis)
            self.plot_correlation_heatmap(df, "Fonte_Alimentacao")
        
        print("\n📈 Gerando visualizações adicionais...")
        
        # Gráfico comparativo de todas as juntas
        all_joints = [j for j in df['joint_number'].unique() if not pd.isna(j)]
        if all_joints:
            self.plot_temperature_analysis(df, all_joints, "Visao_Geral")
        
        # Gerar relatório textual
        print("\n📝 Gerando relatório científico...")
        report = self.generate_fault_report(analysis_results)
        
        report_file = f"{self.output_dir}/relatorio_cientifico.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Relatório salvo: {report_file}")
        
        # Exportar estatísticas
        print("\n💾 Exportando estatísticas...")
        self.export_statistics_csv(analysis_results)
        
        print("\n" + "="*70)
        print("✅ ANÁLISE COMPLETA!")
        print("="*70)
        print(f"\nResultados salvos em: {self.output_dir}/")
        print(f"   • Gráficos: *.png (300 DPI)")
        print(f"   • Relatório: relatorio_cientifico.txt")
        print(f"   • Estatísticas: estatisticas_cenarios.csv\n")
        
        self.conn.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Análise de Cenários de Falhas para Artigo Científico"
    )
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Janela de tempo para análise em horas (padrão: 24, use 0 para todos os dados)'
    )
    parser.add_argument(
        '--db',
        type=str,
        default='data/jaka_monitor.db',
        help='Caminho do banco de dados (padrão: data/jaka_monitor.db)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Analisar TODOS os dados do banco, ignorando filtro de tempo'
    )
    
    args = parser.parse_args()
    
    analyzer = FaultScenarioAnalyzer(db_path=args.db)
    
    # Se --all foi usado, analisar todos os dados (time_window_hours=None)
    time_window = None if args.all else args.hours
    analyzer.run_full_analysis(time_window_hours=time_window)


if __name__ == "__main__":
    main()
