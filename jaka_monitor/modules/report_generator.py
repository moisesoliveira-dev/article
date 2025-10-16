"""
Módulo de Geração de Relatórios
Cria relatórios em PDF e Excel com gráficos e análises
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import matplotlib
matplotlib.use('Agg')  # Backend sem interface gráfica
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import config


class ReportGenerator:
    """Gerador de relatórios em PDF e Excel"""
    
    def __init__(self, db_manager):
        """
        Inicializa o gerador de relatórios
        
        Args:
            db_manager: Instância do DatabaseManager
        """
        self.db = db_manager
        self.reports_dir = config.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Configurar estilo de gráficos
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def generate_full_report(self, hours: int = 24) -> str:
        """
        Gera relatório completo em PDF
        
        Args:
            hours: Janela de tempo para análise
            
        Returns:
            Caminho do arquivo PDF gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = os.path.join(self.reports_dir, f"relatorio_completo_{timestamp}.pdf")
        
        # Criar documento PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilo customizado
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Título
        story.append(Paragraph("Relatório de Monitoramento - Robô JAKA", title_style))
        story.append(Spacer(1, 12))
        
        # Informações do relatório
        info_data = [
            ["Período de Análise:", f"Últimas {hours} horas"],
            ["Data/Hora de Geração:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ["Sistema:", config.SYSTEM_NAME],
            ["Versão:", config.SYSTEM_VERSION]
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Resumo de Eventos
        story.append(Paragraph("1. Resumo de Eventos", heading_style))
        events_summary = self._get_events_summary(hours)
        if events_summary:
            story.append(events_summary)
        story.append(Spacer(1, 12))
        
        # Estatísticas das Juntas
        story.append(Paragraph("2. Estatísticas das Juntas", heading_style))
        stats_table = self._get_statistics_table(hours)
        if stats_table:
            story.append(stats_table)
        story.append(PageBreak())
        
        # Gráficos
        story.append(Paragraph("3. Análise Gráfica", heading_style))
        
        # Gerar e adicionar gráficos
        graph_paths = self._generate_graphs(hours)
        for graph_path in graph_paths:
            if os.path.exists(graph_path):
                img = Image(graph_path, width=6.5*inch, height=4*inch)
                story.append(img)
                story.append(Spacer(1, 12))
        
        # Lista detalhada de eventos
        story.append(PageBreak())
        story.append(Paragraph("4. Lista Detalhada de Eventos", heading_style))
        events_table = self._get_detailed_events_table(hours)
        if events_table:
            story.append(events_table)
        
        # Gerar PDF
        doc.build(story)
        
        return pdf_path
    
    def _get_events_summary(self, hours: int) -> Optional[Table]:
        """Cria tabela resumo de eventos"""
        events = self.db.get_events(hours=hours)
        
        if not events:
            return None
        
        # Contar por severidade
        severity_counts = {
            'info': 0,
            'warning': 0,
            'critical': 0,
            'emergency': 0
        }
        
        for event in events:
            severity = event.get('severity', 'info')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        data = [
            ['Severidade', 'Quantidade', 'Descrição'],
            ['Emergência', str(severity_counts['emergency']), 'Situações críticas que exigem ação imediata'],
            ['Crítico', str(severity_counts['critical']), 'Problemas graves que afetam operação'],
            ['Alerta', str(severity_counts['warning']), 'Situações que requerem atenção'],
            ['Info', str(severity_counts['info']), 'Informações gerais do sistema']
        ]
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def _get_statistics_table(self, hours: int) -> Optional[Table]:
        """Cria tabela com estatísticas das juntas"""
        stats = self.db.get_statistics(hours)
        
        if not stats:
            return None
        
        data = [['Junta', 'Temp Média', 'Temp Máx', 'Corrente Média', 'Corrente Máx', 'Torque Máx']]
        
        for joint_num in sorted(stats.keys()):
            joint_stats = stats[joint_num]
            data.append([
                f"Junta {joint_num}",
                f"{joint_stats.get('avg_temp', 0):.1f}°C",
                f"{joint_stats.get('max_temp', 0):.1f}°C",
                f"{joint_stats.get('avg_current', 0):.2f}A",
                f"{joint_stats.get('max_current', 0):.2f}A",
                f"{joint_stats.get('max_torque', 0):.2f}"
            ])
        
        table = Table(data, colWidths=[1*inch, 1.2*inch, 1.2*inch, 1.3*inch, 1.3*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _get_detailed_events_table(self, hours: int) -> Optional[Table]:
        """Cria tabela detalhada de eventos"""
        events = self.db.get_events(hours=hours)
        
        if not events:
            return None
        
        data = [['Data/Hora', 'Severidade', 'Tipo', 'Descrição']]
        
        for event in events[:50]:  # Limitar a 50 eventos
            timestamp = datetime.fromisoformat(event['timestamp']).strftime("%d/%m %H:%M:%S")
            data.append([
                timestamp,
                event.get('severity', 'N/A'),
                event.get('event_type', 'N/A'),
                event.get('description', 'N/A')[:50] + '...' if len(event.get('description', '')) > 50 else event.get('description', 'N/A')
            ])
        
        table = Table(data, colWidths=[1.2*inch, 1*inch, 1.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _generate_graphs(self, hours: int) -> List[str]:
        """Gera gráficos de análise"""
        graph_paths = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Obter dados
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        # Gráfico 1: Temperaturas das Juntas
        temp_graph = self._plot_joint_temperatures(start_time, end_time, timestamp)
        if temp_graph:
            graph_paths.append(temp_graph)
        
        # Gráfico 2: Correntes das Juntas
        current_graph = self._plot_joint_currents(start_time, end_time, timestamp)
        if current_graph:
            graph_paths.append(current_graph)
        
        # Gráfico 3: Torques das Juntas
        torque_graph = self._plot_joint_torques(start_time, end_time, timestamp)
        if torque_graph:
            graph_paths.append(torque_graph)
        
        return graph_paths
    
    def _plot_joint_temperatures(self, start_time: datetime, end_time: datetime, timestamp: str) -> Optional[str]:
        """Plota temperaturas das juntas ao longo do tempo"""
        data = self.db.get_joint_data_range(start_time.isoformat(), end_time.isoformat())
        
        if not data:
            return None
        
        # Organizar dados por junta
        joint_data = {i: {'times': [], 'temps': []} for i in range(1, 7)}
        
        for row in data:
            joint_num = row['joint_number']
            if joint_num in joint_data:
                joint_data[joint_num]['times'].append(datetime.fromisoformat(row['timestamp']))
                joint_data[joint_num]['temps'].append(row['temperature'])
        
        # Plotar
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for joint_num in range(1, 7):
            if joint_data[joint_num]['times']:
                ax.plot(joint_data[joint_num]['times'], joint_data[joint_num]['temps'],
                       label=f'Junta {joint_num}', marker='o', markersize=2, linewidth=1.5)
        
        # Linha de threshold
        ax.axhline(y=config.THRESHOLDS['joint_temperature_warning'], color='orange',
                  linestyle='--', label='Limite Alerta', linewidth=2)
        ax.axhline(y=config.THRESHOLDS['joint_temperature_critical'], color='red',
                  linestyle='--', label='Limite Crítico', linewidth=2)
        
        ax.set_xlabel('Data/Hora', fontsize=12)
        ax.set_ylabel('Temperatura (°C)', fontsize=12)
        ax.set_title('Evolução da Temperatura das Juntas', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        fig.autofmt_xdate()
        
        plt.tight_layout()
        
        graph_path = os.path.join(self.reports_dir, f'temp_graph_{timestamp}.png')
        plt.savefig(graph_path, dpi=config.PLOT_DPI, bbox_inches='tight')
        plt.close()
        
        return graph_path
    
    def _plot_joint_currents(self, start_time: datetime, end_time: datetime, timestamp: str) -> Optional[str]:
        """Plota correntes das juntas ao longo do tempo"""
        data = self.db.get_joint_data_range(start_time.isoformat(), end_time.isoformat())
        
        if not data:
            return None
        
        # Organizar dados por junta
        joint_data = {i: {'times': [], 'currents': []} for i in range(1, 7)}
        
        for row in data:
            joint_num = row['joint_number']
            if joint_num in joint_data:
                joint_data[joint_num]['times'].append(datetime.fromisoformat(row['timestamp']))
                joint_data[joint_num]['currents'].append(abs(row['current']))
        
        # Plotar
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for joint_num in range(1, 7):
            if joint_data[joint_num]['times']:
                ax.plot(joint_data[joint_num]['times'], joint_data[joint_num]['currents'],
                       label=f'Junta {joint_num}', marker='o', markersize=2, linewidth=1.5)
        
        # Linha de threshold
        ax.axhline(y=config.THRESHOLDS['joint_current_warning'], color='orange',
                  linestyle='--', label='Limite Alerta', linewidth=2)
        ax.axhline(y=config.THRESHOLDS['joint_current_critical'], color='red',
                  linestyle='--', label='Limite Crítico', linewidth=2)
        
        ax.set_xlabel('Data/Hora', fontsize=12)
        ax.set_ylabel('Corrente (A)', fontsize=12)
        ax.set_title('Evolução da Corrente das Juntas', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        fig.autofmt_xdate()
        
        plt.tight_layout()
        
        graph_path = os.path.join(self.reports_dir, f'current_graph_{timestamp}.png')
        plt.savefig(graph_path, dpi=config.PLOT_DPI, bbox_inches='tight')
        plt.close()
        
        return graph_path
    
    def _plot_joint_torques(self, start_time: datetime, end_time: datetime, timestamp: str) -> Optional[str]:
        """Plota torques das juntas ao longo do tempo"""
        data = self.db.get_joint_data_range(start_time.isoformat(), end_time.isoformat())
        
        if not data:
            return None
        
        # Organizar dados por junta
        joint_data = {i: {'times': [], 'torques': []} for i in range(1, 7)}
        
        for row in data:
            joint_num = row['joint_number']
            if joint_num in joint_data:
                joint_data[joint_num]['times'].append(datetime.fromisoformat(row['timestamp']))
                joint_data[joint_num]['torques'].append(abs(row['torque']))
        
        # Plotar
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for joint_num in range(1, 7):
            if joint_data[joint_num]['times']:
                ax.plot(joint_data[joint_num]['times'], joint_data[joint_num]['torques'],
                       label=f'Junta {joint_num}', marker='o', markersize=2, linewidth=1.5)
        
        # Linha de threshold
        ax.axhline(y=config.THRESHOLDS['joint_torque_warning'], color='orange',
                  linestyle='--', label='Limite Alerta', linewidth=2)
        ax.axhline(y=config.THRESHOLDS['joint_torque_critical'], color='red',
                  linestyle='--', label='Limite Crítico', linewidth=2)
        
        ax.set_xlabel('Data/Hora', fontsize=12)
        ax.set_ylabel('Torque', fontsize=12)
        ax.set_title('Evolução do Torque/Carga das Juntas', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        fig.autofmt_xdate()
        
        plt.tight_layout()
        
        graph_path = os.path.join(self.reports_dir, f'torque_graph_{timestamp}.png')
        plt.savefig(graph_path, dpi=config.PLOT_DPI, bbox_inches='tight')
        plt.close()
        
        return graph_path
    
    def export_to_excel(self, hours: int = 24) -> str:
        """
        Exporta dados para Excel
        
        Args:
            hours: Janela de tempo para análise
            
        Returns:
            Caminho do arquivo Excel gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = os.path.join(self.reports_dir, f"dados_exportados_{timestamp}.xlsx")
        
        # Obter dados
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        joint_data = self.db.get_joint_data_range(start_time.isoformat(), end_time.isoformat())
        events = self.db.get_events(hours=hours)
        
        # Criar Excel com múltiplas abas
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Aba 1: Dados das Juntas
            if joint_data:
                df_joints = pd.DataFrame(joint_data)
                df_joints.to_excel(writer, sheet_name='Dados das Juntas', index=False)
            
            # Aba 2: Eventos
            if events:
                df_events = pd.DataFrame(events)
                df_events.to_excel(writer, sheet_name='Eventos', index=False)
            
            # Aba 3: Estatísticas
            stats = self.db.get_statistics(hours)
            if stats:
                df_stats = pd.DataFrame.from_dict(stats, orient='index')
                df_stats.to_excel(writer, sheet_name='Estatísticas')
        
        return excel_path
