"""
Script de Exemplo - Análise Rápida de Dados JAKA
Copie e adapte este script para suas análises personalizadas
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Configurações
DB_PATH = "data/jaka_monitor.db"
OUTPUT_DIR = "analises"

# Criar diretório de saída
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===============================================
# PARTE 1: CONEXÃO E VISÃO GERAL
# ===============================================

print("=" * 70)
print("📊 ANÁLISE RÁPIDA - SISTEMA JAKA MONITOR")
print("=" * 70)

# Conectar ao banco
conn = sqlite3.connect(DB_PATH)

# Verificar dados disponíveis
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM robot_data")
total_registros = cursor.fetchone()[0]

cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM robot_data")
inicio, fim = cursor.fetchone()

cursor.execute("SELECT COUNT(*) FROM events")
total_eventos = cursor.fetchone()[0]

print(f"\n📈 Dados Disponíveis:")
print(f"   • Total de Registros: {total_registros:,}")
print(f"   • Período: {inicio} até {fim}")
print(f"   • Total de Eventos: {total_eventos}")

if total_registros == 0:
    print("\n⚠️  Nenhum dado encontrado! Execute o sistema de monitoramento primeiro.")
    exit()

print("\n")

# ===============================================
# PARTE 2: ANÁLISE DAS JUNTAS
# ===============================================

print("🔧 ANÁLISE DAS JUNTAS (últimas 24h)")
print("-" * 70)

# Carregar dados das juntas
query_joints = """
    SELECT 
        joint_number as junta,
        ROUND(AVG(temperature), 2) as temp_media,
        ROUND(MAX(temperature), 2) as temp_max,
        ROUND(MIN(temperature), 2) as temp_min,
        ROUND(AVG(current), 3) as corrente_media,
        ROUND(MAX(current), 3) as corrente_max,
        ROUND(AVG(torque), 2) as torque_medio,
        COUNT(*) as amostras
    FROM joint_data
    WHERE timestamp >= datetime('now', '-24 hours')
    GROUP BY joint_number
    ORDER BY joint_number
"""

df_stats = pd.read_sql_query(query_joints, conn)

if not df_stats.empty:
    print(df_stats.to_string(index=False))
    print()
    
    # Salvar tabela
    df_stats.to_csv(f"{OUTPUT_DIR}/estatisticas_juntas.csv", index=False)
    print(f"✅ Tabela salva em: {OUTPUT_DIR}/estatisticas_juntas.csv")
else:
    print("⚠️  Nenhum dado de juntas nas últimas 24h")

print("\n")

# ===============================================
# PARTE 3: ANÁLISE DE EVENTOS/ANOMALIAS
# ===============================================

print("⚠️  ANOMALIAS DETECTADAS")
print("-" * 70)

query_events = """
    SELECT 
        severity,
        event_type,
        COUNT(*) as quantidade,
        ROUND(AVG(duration), 2) as duracao_media_seg
    FROM events
    WHERE timestamp >= datetime('now', '-24 hours')
    GROUP BY severity, event_type
    ORDER BY 
        CASE severity
            WHEN 'emergency' THEN 1
            WHEN 'critical' THEN 2
            WHEN 'warning' THEN 3
            ELSE 4
        END,
        quantidade DESC
"""

df_events = pd.read_sql_query(query_events, conn)

if not df_events.empty:
    print(df_events.to_string(index=False))
    print()
    
    # Salvar
    df_events.to_csv(f"{OUTPUT_DIR}/resumo_eventos.csv", index=False)
    print(f"✅ Eventos salvos em: {OUTPUT_DIR}/resumo_eventos.csv")
else:
    print("✓ Nenhuma anomalia detectada nas últimas 24h")

print("\n")

# ===============================================
# PARTE 4: GRÁFICOS
# ===============================================

print("📈 GERANDO GRÁFICOS...")
print("-" * 70)

# Carregar dados temporais
query_temporal = """
    SELECT 
        timestamp,
        joint_number,
        temperature,
        current,
        torque
    FROM joint_data
    WHERE timestamp >= datetime('now', '-24 hours')
    ORDER BY timestamp
"""

df_temporal = pd.read_sql_query(query_temporal, conn)

if not df_temporal.empty:
    # Converter timestamp
    df_temporal['timestamp'] = pd.to_datetime(df_temporal['timestamp'])
    
    # ========== GRÁFICO 1: TEMPERATURA ==========
    fig1, ax1 = plt.subplots(figsize=(14, 6))
    
    for joint in range(1, 7):
        data = df_temporal[df_temporal['joint_number'] == joint]
        if not data.empty:
            ax1.plot(data['timestamp'], data['temperature'], 
                    label=f'Junta {joint}', marker='o', markersize=2, alpha=0.7)
    
    ax1.axhline(y=40, color='orange', linestyle='--', label='Limite Alerta', linewidth=2)
    ax1.axhline(y=50, color='red', linestyle='--', label='Limite Crítico', linewidth=2)
    ax1.set_xlabel('Tempo', fontsize=12)
    ax1.set_ylabel('Temperatura (°C)', fontsize=12)
    ax1.set_title('Evolução da Temperatura das Juntas - Últimas 24h', 
                  fontsize=14, fontweight='bold')
    ax1.legend(loc='best', ncol=4)
    ax1.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/grafico_temperatura.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Gráfico de temperatura: {OUTPUT_DIR}/grafico_temperatura.png")
    plt.close()
    
    # ========== GRÁFICO 2: CORRENTE ==========
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    
    for joint in range(1, 7):
        data = df_temporal[df_temporal['joint_number'] == joint]
        if not data.empty:
            ax2.plot(data['timestamp'], data['current'].abs(), 
                    label=f'Junta {joint}', marker='o', markersize=2, alpha=0.7)
    
    ax2.axhline(y=2.0, color='orange', linestyle='--', label='Limite Alerta', linewidth=2)
    ax2.axhline(y=3.0, color='red', linestyle='--', label='Limite Crítico', linewidth=2)
    ax2.set_xlabel('Tempo', fontsize=12)
    ax2.set_ylabel('Corrente (A)', fontsize=12)
    ax2.set_title('Evolução da Corrente das Juntas - Últimas 24h', 
                  fontsize=14, fontweight='bold')
    ax2.legend(loc='best', ncol=4)
    ax2.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/grafico_corrente.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Gráfico de corrente: {OUTPUT_DIR}/grafico_corrente.png")
    plt.close()
    
    # ========== GRÁFICO 3: BOXPLOT DE TEMPERATURA ==========
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    
    df_temporal.boxplot(column='temperature', by='joint_number', ax=ax3)
    ax3.set_xlabel('Número da Junta', fontsize=12)
    ax3.set_ylabel('Temperatura (°C)', fontsize=12)
    ax3.set_title('Distribuição de Temperatura por Junta', fontsize=14, fontweight='bold')
    plt.suptitle('')  # Remove título padrão do pandas
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/boxplot_temperatura.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Boxplot de temperatura: {OUTPUT_DIR}/boxplot_temperatura.png")
    plt.close()
    
    # ========== GRÁFICO 4: HEATMAP DE CORRELAÇÃO ==========
    # Correlação entre temperatura, corrente e torque
    pivot_temp = df_temporal.pivot_table(values='temperature', 
                                         index='timestamp', 
                                         columns='joint_number')
    pivot_current = df_temporal.pivot_table(values='current', 
                                            index='timestamp', 
                                            columns='joint_number')
    pivot_torque = df_temporal.pivot_table(values='torque', 
                                           index='timestamp', 
                                           columns='joint_number')
    
    # Criar DataFrame combinado
    combined = pd.DataFrame()
    for col in pivot_temp.columns:
        combined[f'Temp_J{col}'] = pivot_temp[col]
        combined[f'Curr_J{col}'] = pivot_current[col]
        combined[f'Torq_J{col}'] = pivot_torque[col]
    
    fig4, ax4 = plt.subplots(figsize=(12, 10))
    sns.heatmap(combined.corr(), annot=False, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax4)
    ax4.set_title('Matriz de Correlação - Temperatura, Corrente e Torque', 
                  fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/heatmap_correlacao.png", dpi=300, bbox_inches='tight')
    print(f"   ✓ Heatmap de correlação: {OUTPUT_DIR}/heatmap_correlacao.png")
    plt.close()
    
else:
    print("⚠️  Nenhum dado temporal disponível")

print("\n")

# ===============================================
# PARTE 5: ESTATÍSTICAS AVANÇADAS
# ===============================================

print("📊 ESTATÍSTICAS AVANÇADAS")
print("-" * 70)

if not df_temporal.empty:
    # Estatísticas descritivas completas
    stats_completas = df_temporal.groupby('joint_number')[['temperature', 'current', 'torque']].describe()
    
    # Salvar
    stats_completas.to_csv(f"{OUTPUT_DIR}/estatisticas_completas.csv")
    print(f"✅ Estatísticas completas salvas em: {OUTPUT_DIR}/estatisticas_completas.csv")
    
    # Correlações
    print("\n🔗 CORRELAÇÕES POR JUNTA:")
    for joint in range(1, 7):
        joint_data = df_temporal[df_temporal['joint_number'] == joint]
        if len(joint_data) > 1:
            corr = joint_data[['temperature', 'current', 'torque']].corr()
            print(f"\n   Junta {joint}:")
            print(f"      Temp vs Corrente: {corr.loc['temperature', 'current']:.3f}")
            print(f"      Temp vs Torque:   {corr.loc['temperature', 'torque']:.3f}")
            print(f"      Corrente vs Torque: {corr.loc['current', 'torque']:.3f}")

print("\n")

# ===============================================
# PARTE 6: EXPORTAÇÃO COMPLETA
# ===============================================

print("💾 EXPORTANDO DADOS COMPLETOS...")
print("-" * 70)

# Exportar todas as tabelas
tabelas = ['robot_data', 'joint_data', 'events', 'tcp_positions']

for tabela in tabelas:
    try:
        df = pd.read_sql_query(f"SELECT * FROM {tabela} WHERE timestamp >= datetime('now', '-24 hours')", conn)
        if not df.empty:
            df.to_csv(f"{OUTPUT_DIR}/{tabela}_completo.csv", index=False)
            print(f"   ✓ {tabela}: {len(df)} registros → {OUTPUT_DIR}/{tabela}_completo.csv")
    except Exception as e:
        print(f"   ⚠️  Erro ao exportar {tabela}: {e}")

print("\n")

# ===============================================
# PARTE 7: RESUMO FINAL
# ===============================================

print("=" * 70)
print("✅ ANÁLISE CONCLUÍDA!")
print("=" * 70)
print(f"\n📁 Todos os arquivos foram salvos em: {OUTPUT_DIR}/")
print("\nArquivos gerados:")
print("   • estatisticas_juntas.csv - Estatísticas agregadas")
print("   • resumo_eventos.csv - Resumo de anomalias")
print("   • grafico_temperatura.png - Evolução temporal")
print("   • grafico_corrente.png - Evolução de corrente")
print("   • boxplot_temperatura.png - Distribuição de temperatura")
print("   • heatmap_correlacao.png - Matriz de correlação")
print("   • estatisticas_completas.csv - Estatísticas detalhadas")
print("   • [tabela]_completo.csv - Dados brutos exportados")

print("\n💡 Dicas:")
print("   • Use os arquivos .csv no Excel ou Python para análises adicionais")
print("   • Os gráficos .png estão em 300 DPI (prontos para publicação)")
print("   • Modifique este script para suas necessidades específicas")

print("\n🎓 Para artigos científicos:")
print("   • Documente o período de coleta")
print("   • Cite as configurações usadas (thresholds)")
print("   • Mantenha backup dos dados brutos")

print("\n" + "=" * 70)

# Fechar conexão
conn.close()

print("\n✨ Script executado com sucesso!")
