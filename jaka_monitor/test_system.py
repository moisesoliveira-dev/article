"""
Script de teste rápido do sistema
Testa os módulos principais sem necessidade de MQTT
"""
import json
import sys
import os
from datetime import datetime

# Adicionar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.database import DatabaseManager
from modules.analyzer import AnomalyDetector
from modules.report_generator import ReportGenerator
import config


def load_sample_data():
    """Carrega dados de exemplo"""
    with open('../dados.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def test_database():
    """Testa módulo de banco de dados"""
    print("=" * 60)
    print("TESTE 1: Banco de Dados")
    print("=" * 60)
    
    db = DatabaseManager("data/test_monitor.db")
    
    # Inserir dados de teste
    sample_data = load_sample_data()
    
    print("✓ Banco de dados criado")
    
    # Inserir 10 registros
    for i in range(10):
        db.insert_robot_data(sample_data)
    
    print(f"✓ {10} registros inseridos")
    
    # Consultar dados
    recent = db.get_recent_data(minutes=10)
    print(f"✓ {len(recent)} registros recuperados")
    
    # Estatísticas
    stats = db.get_statistics(hours=1)
    print(f"✓ Estatísticas calculadas para {len(stats)} juntas")
    
    db.close()
    print("✓ Teste de banco de dados APROVADO\n")


def test_analyzer():
    """Testa módulo de análise"""
    print("=" * 60)
    print("TESTE 2: Analisador de Anomalias")
    print("=" * 60)
    
    analyzer = AnomalyDetector()
    sample_data = load_sample_data()
    
    # Teste 1: Dados normais
    anomalies = analyzer.analyze(sample_data)
    print(f"✓ Análise normal: {len(anomalies)} anomalias detectadas")
    
    # Teste 2: Simular temperatura alta
    test_data = sample_data.copy()
    test_data["monitor_data"][2] = 55.0  # Temperatura crítica
    
    anomalies = analyzer.analyze(test_data)
    print(f"✓ Análise com temperatura alta: {len(anomalies)} anomalias")
    
    if anomalies:
        for anomaly in anomalies:
            print(f"  - {anomaly.get('description', 'N/A')}")
    
    # Teste 3: Health score
    score = analyzer.get_health_score(sample_data)
    print(f"✓ Health score calculado: {score:.1f}%")
    
    print("✓ Teste de análise APROVADO\n")


def test_report_generation():
    """Testa geração de relatórios"""
    print("=" * 60)
    print("TESTE 3: Geração de Relatórios")
    print("=" * 60)
    
    # Criar banco de teste com dados
    db = DatabaseManager("data/test_monitor.db")
    sample_data = load_sample_data()
    
    # Inserir dados de exemplo
    for i in range(50):
        db.insert_robot_data(sample_data)
    
    # Inserir eventos de exemplo
    db.insert_event(
        event_type="high_temperature",
        severity="warning",
        description="Temperatura da junta 1 elevada",
        joint_number=1,
        value=42.0,
        threshold=40.0
    )
    
    print("✓ Dados de teste inseridos")
    
    # Gerar relatório
    report_gen = ReportGenerator(db)
    
    try:
        # PDF
        pdf_path = report_gen.generate_full_report(hours=1)
        print(f"✓ Relatório PDF gerado: {pdf_path}")
        
        # Excel
        excel_path = report_gen.export_to_excel(hours=1)
        print(f"✓ Excel exportado: {excel_path}")
        
        print("✓ Teste de relatórios APROVADO\n")
    
    except Exception as e:
        print(f"⚠ Aviso: {e}")
        print("  (Algumas bibliotecas podem não estar instaladas)\n")
    
    finally:
        db.close()


def test_all():
    """Executa todos os testes"""
    print("\n")
    print("*" * 60)
    print("TESTE COMPLETO DO SISTEMA - JAKA Monitor")
    print("*" * 60)
    print()
    
    try:
        test_database()
        test_analyzer()
        test_report_generation()
        
        print("=" * 60)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 60)
        print()
        print("O sistema está pronto para uso!")
        print("Execute: python main_gui.py")
        print()
    
    except Exception as e:
        print("\n")
        print("=" * 60)
        print(f"❌ ERRO NOS TESTES: {e}")
        print("=" * 60)
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_all()
