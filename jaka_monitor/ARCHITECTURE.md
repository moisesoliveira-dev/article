# 🏗️ Arquitetura do Sistema JAKA Monitor

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SISTEMA JAKA MONITOR v1.0.0                     │
│                  Sistema de Monitoramento em Tempo Real             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         CAMADA DE INTERFACE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    main_gui.py (PyQt5)                     │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │    │
│  │  │Dashboard │ │  Juntas  │ │ Eventos  │ │Relatórios│     │    │
│  │  │   Tab    │ │   Tab    │ │   Tab    │ │   Tab    │     │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │    │
│  │                                                            │    │
│  │  • Health Score (0-100%)                                  │    │
│  │  • Status em Tempo Real                                   │    │
│  │  • Alertas Visuais                                        │    │
│  │  • Log de Eventos                                         │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE NEGÓCIO                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  mqtt_client.py  │  │   analyzer.py    │  │report_generator │  │
│  ├──────────────────┤  ├──────────────────┤  ├─────────────────┤  │
│  │• Conexão MQTT    │  │• Detecção de     │  │• PDF com        │  │
│  │• Autenticação    │  │  Anomalias       │  │  ReportLab      │  │
│  │• Callbacks       │  │• 7 Tipos:        │  │• Excel com      │  │
│  │• Reconexão Auto  │  │  - Temperatura   │  │  pandas         │  │
│  │• QoS Config      │  │  - Corrente      │  │• Gráficos alta  │  │
│  │                  │  │  - Voltagem      │  │  resolução      │  │
│  │Broker:           │  │  - Torque        │  │• Tabelas        │  │
│  │147.1.5.238:1883  │  │  - Posição       │  │  formatadas     │  │
│  │                  │  │  - Estados       │  │                 │  │
│  │Topic:            │  │  - Tendências    │  │Outputs:         │  │
│  │jaka/monitor      │  │                  │  │• PDF Completo   │  │
│  │                  │  │• Criticidade     │  │• Excel Multi-aba│  │
│  │                  │  │  Temporal        │  │• Gráficos PNG   │  │
│  │                  │  │• Health Score    │  │                 │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
│           │                      │                      │           │
└───────────┼──────────────────────┼──────────────────────┼───────────┘
            │                      │                      │
            ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CAMADA DE PERSISTÊNCIA                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    database.py (SQLite)                    │    │
│  ├────────────────────────────────────────────────────────────┤    │
│  │                                                            │    │
│  │  Tabela: robot_data                                       │    │
│  │  ├─ id, timestamp, robot_id, robot_name                   │    │
│  │  ├─ task_state, enabled, powered_on                       │    │
│  │  ├─ robot_temp, ambient_temp                              │    │
│  │  └─ json_data (completo)                                  │    │
│  │                                                            │    │
│  │  Tabela: joint_data                                       │    │
│  │  ├─ id, robot_data_id, joint_number                       │    │
│  │  ├─ position, velocity, current                           │    │
│  │  ├─ temperature, voltage, torque                          │    │
│  │  └─ error_status                                          │    │
│  │                                                            │    │
│  │  Tabela: tcp_positions                                    │    │
│  │  ├─ x, y, z (mm)                                          │    │
│  │  └─ rx, ry, rz (graus)                                    │    │
│  │                                                            │    │
│  │  Tabela: events                                           │    │
│  │  ├─ timestamp, event_type, severity                       │    │
│  │  ├─ description, value, threshold                         │    │
│  │  └─ duration, resolved                                    │    │
│  │                                                            │    │
│  │  Tabela: statistics                                       │    │
│  │  ├─ period_start, period_end                              │    │
│  │  ├─ avg/max: temperature, current, velocity               │    │
│  │  └─ avg/max: torque                                       │    │
│  │                                                            │    │
│  │  Índices Otimizados:                                      │    │
│  │  • idx_robot_data_timestamp                               │    │
│  │  • idx_joint_data_timestamp                               │    │
│  │  • idx_events_timestamp                                   │    │
│  │  • idx_events_resolved                                    │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  Localização: data/jaka_monitor.db                                  │
└─────────────────────────────────────────────────────────────────────┘
                                  ▲
                                  │
┌─────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE ENTRADA                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐          ┌──────────────────┐                │
│  │   Robô JAKA      │          │  test_simulator  │                │
│  │   (Hardware)     │          │    (Software)    │                │
│  ├──────────────────┤          ├──────────────────┤                │
│  │• Publica via     │          │• Simula dados    │                │
│  │  MQTT em tempo   │    OU    │• Gera anomalias  │                │
│  │  real            │          │• Útil para testes│                │
│  │                  │          │                  │                │
│  │Formato: JSON     │          │Formato: JSON     │                │
│  │~9KB por mensagem │          │~9KB por mensagem │                │
│  └──────────────────┘          └──────────────────┘                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Dados

```
┌─────────────┐
│ Robô JAKA   │
│ ou          │
│ Simulador   │
└──────┬──────┘
       │ JSON via MQTT (jaka/monitor)
       ▼
┌──────────────────────┐
│   mqtt_client.py     │
│  • Recebe mensagem   │
│  • Decodifica JSON   │
└──────┬───────────────┘
       │ Dict Python
       ├─────────────────────────┐
       │                         │
       ▼                         ▼
┌──────────────────┐    ┌─────────────────┐
│   analyzer.py    │    │  main_gui.py    │
│ • Analisa dados  │    │ • Atualiza UI   │
│ • Detecta        │    │ • Mostra dados  │
│   anomalias      │    │                 │
└──────┬───────────┘    └─────────────────┘
       │ Anomalias detectadas
       ├─────────────────────────┐
       │                         │
       ▼                         ▼
┌──────────────────┐    ┌─────────────────┐
│   database.py    │    │  main_gui.py    │
│ • Salva dados    │    │ • Exibe alertas │
│ • Salva eventos  │    │ • Log visual    │
└──────────────────┘    └─────────────────┘
       │
       │ (Após acúmulo de dados)
       ▼
┌──────────────────────┐
│ report_generator.py  │
│ • Consulta banco     │
│ • Gera gráficos      │
│ • Cria PDF/Excel     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│   reports/           │
│ • PDF                │
│ • Excel              │
│ • Gráficos PNG       │
└──────────────────────┘
```

---

## Thresholds e Criticidade

```
DETECÇÃO DE ANOMALIAS
═══════════════════════════════════════════════════════════

Parâmetro          │ Warning │ Critical │ Unidade
───────────────────┼─────────┼──────────┼─────────
Temp. Junta        │  40.0   │   50.0   │   °C
Temp. Robô         │  45.0   │   55.0   │   °C
Corrente           │   2.0   │    3.0   │    A
Torque             │   3.0   │    3.5   │   -
Desvio Posição     │   0.5   │    1.0   │   °
Voltagem           │ 48-52V  │     -    │   V

ESCALADA TEMPORAL
═══════════════════════════════════════════════════════════

Duração       │ Nível      │ Ação Sugerida
──────────────┼────────────┼──────────────────────────
0-30s         │ INFO       │ Monitorar
30-120s       │ WARNING    │ Atenção necessária
120-300s      │ CRITICAL   │ Investigar problema
>300s         │ EMERGENCY  │ Ação imediata

HEALTH SCORE
═══════════════════════════════════════════════════════════

Score    │ Status        │ Cor    │ Ação
─────────┼───────────────┼────────┼────────────────
80-100%  │ Excelente     │ Verde  │ Normal
50-79%   │ Aceitável     │ Laranja│ Monitorar
0-49%    │ Problemático  │ Vermelho│ Intervenção
```

---

## Tecnologias Utilizadas

```
FRONTEND
═══════════════════════════════════════════════════════════
PyQt5 5.15.9
├─ Interface gráfica rica
├─ 4 abas funcionais
├─ Atualização em tempo real
└─ Alertas visuais

BACKEND
═══════════════════════════════════════════════════════════
Python 3.8+
├─ paho-mqtt 1.6.1      → Comunicação MQTT
├─ pandas 2.0.3         → Análise de dados
├─ matplotlib 3.7.2     → Gráficos
├─ seaborn 0.12.2       → Estilização
├─ reportlab 4.0.4      → Geração PDF
├─ openpyxl 3.1.2       → Exportação Excel
└─ sqlite3 (built-in)   → Banco de dados

ANÁLISE
═══════════════════════════════════════════════════════════
• Detecção baseada em regras (não-IA)
• 7 tipos de análise
• Criticidade temporal
• Health score algorítmico
```

---

## Capacidades do Sistema

```
ENTRADA
═══════════════════════════════════════════════════════════
• MQTT com QoS configurável
• Autenticação usuário/senha
• Reconexão automática
• Taxa: ~1-10 mensagens/segundo

PROCESSAMENTO
═══════════════════════════════════════════════════════════
• Análise em tempo real
• Thread separado (não bloqueia UI)
• 7 tipos de detecção simultâneos
• Rastreamento de anomalias persistentes

ARMAZENAMENTO
═══════════════════════════════════════════════════════════
• SQLite otimizado com índices
• 5 tabelas relacionadas
• Capacidade: >1 milhão de registros
• Salvamento configurável (batch)

SAÍDA
═══════════════════════════════════════════════════════════
• Relatórios PDF profissionais
• Exportação Excel multi-aba
• Gráficos alta resolução (150 DPI)
• Logs detalhados
```

---

## Escalabilidade

```
CONFIGURAÇÕES DE PERFORMANCE
═══════════════════════════════════════════════════════════

SAVE_INTERVAL = 10
├─ Baixo (5): Mais dados, mais carga
├─ Médio (10): Balanceado ✓
└─ Alto (20+): Menos carga, menos resolução

ANALYSIS_WINDOW = 60
├─ Pequeno (30s): Análise rápida
├─ Médio (60s): Balanceado ✓
└─ Grande (120s+): Mais contexto, mais memória

HISTORY MAXLEN = 100
├─ Pequeno (50): Menos memória
├─ Médio (100): Balanceado ✓
└─ Grande (200+): Mais tendências, mais RAM
```

---

## Integração

```
API DE INTEGRAÇÃO
═══════════════════════════════════════════════════════════

DatabaseManager
├─ insert_robot_data(data: dict) → int
├─ insert_event(...) → int
├─ get_recent_data(minutes: int) → List[dict]
├─ get_statistics(hours: int) → Dict
└─ get_events(severity, hours) → List[dict]

AnomalyDetector
├─ analyze(data: dict) → List[anomaly]
├─ get_health_score(data: dict) → float
├─ calculate_criticality(...) → (severity, duration)
└─ clear_anomaly(key: str) → None

ReportGenerator
├─ generate_full_report(hours: int) → str (path)
├─ export_to_excel(hours: int) → str (path)
└─ (gráficos gerados automaticamente)
```

---

**Sistema Completo e Modular**  
**Pronto para Extensão e Customização**
