# 🎯 RESUMO VISUAL - Extração de Dados

## Guia de 1 Minuto para Analisar Resultados

---

## 🚀 3 Opções Simples

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1️⃣  INTERFACE GRÁFICA (Clique e Pronto)                  │
│                                                             │
│     python main_gui.py                                      │
│     ↓                                                       │
│     Aba "Relatórios"                                        │
│     ↓                                                       │
│     • Gerar PDF Completo  ← Gráficos + Estatísticas       │
│     • Exportar Excel      ← 5 abas de dados               │
│                                                             │
│     ✅ Mais Fácil | ⚡ Mais Rápido | 📊 Pronto p/ Artigos  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  2️⃣  SCRIPT AUTOMÁTICO (Análise Completa)                 │
│                                                             │
│     python exemplo_analise.py                               │
│     ↓                                                       │
│     Gera automaticamente:                                   │
│     ✓ 4 gráficos (300 DPI)                                 │
│     ✓ Estatísticas (CSV)                                   │
│     ✓ Correlações                                          │
│     ✓ Resumo de anomalias                                  │
│                                                             │
│     📁 Resultados em: analises/                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  3️⃣  PYTHON PERSONALIZADO (Máxima Flexibilidade)          │
│                                                             │
│     import pandas as pd                                     │
│     import sqlite3                                          │
│                                                             │
│     conn = sqlite3.connect('data/jaka_monitor.db')         │
│     df = pd.read_sql_query("SELECT ...", conn)            │
│     df.plot()                                              │
│                                                             │
│     💡 Use queries de: QUERIES_SQL_UTEIS.md               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 O Que Cada Método Gera

### **Opção 1: Interface GUI**
```
📄 relatorio_completo_20251017_143022.pdf
   • Resumo executivo
   • 3 gráficos temporais
   • Estatísticas das juntas
   • Lista de anomalias

📊 dados_exportados_20251017_143025.xlsx
   [Aba 1] Dados do Robô
   [Aba 2] Dados das Juntas (temperatura, corrente, etc.)
   [Aba 3] Eventos/Anomalias
   [Aba 4] Posições TCP
   [Aba 5] Estatísticas
```

### **Opção 2: Script Automático**
```
analises/
├── 📊 estatisticas_juntas.csv
├── ⚠️ resumo_eventos.csv
├── 📈 grafico_temperatura.png (300 DPI)
├── 📈 grafico_corrente.png (300 DPI)
├── 📊 boxplot_temperatura.png (300 DPI)
├── 🔥 heatmap_correlacao.png (300 DPI)
└── 💾 [tabela]_completo.csv (dados brutos)
```

### **Opção 3: Personalizado**
```
🎨 Seus próprios gráficos
📊 Suas próprias análises
📝 Formatação customizada
```

---

## 🗄️ Estrutura do Banco de Dados

```
data/jaka_monitor.db (SQLite)
│
├── 🤖 robot_data
│   ├── timestamp
│   ├── robot_id, robot_name
│   ├── task_state, task_mode
│   ├── robot_temp, ambient_temp
│   └── json_data (dados brutos)
│
├── 🔧 joint_data (6 juntas)
│   ├── timestamp
│   ├── joint_number (1-6)
│   ├── temperature
│   ├── current
│   ├── torque
│   ├── position
│   └── velocity
│
├── ⚠️ events
│   ├── timestamp
│   ├── event_type
│   ├── severity (info/warning/critical/emergency)
│   ├── joint_number
│   ├── description
│   ├── value
│   └── threshold
│
├── 📍 tcp_positions
│   ├── x, y, z (mm)
│   └── rx, ry, rz (graus)
│
└── 📊 statistics
    └── (agregados por período)
```

---

## 🔍 Queries Mais Usadas

### **1. Estatísticas das Juntas**
```sql
SELECT 
    joint_number,
    AVG(temperature) as temp_media,
    MAX(temperature) as temp_max,
    AVG(current) as corrente_media
FROM joint_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY joint_number;
```

### **2. Anomalias Críticas**
```sql
SELECT * FROM events
WHERE severity IN ('critical', 'emergency')
ORDER BY timestamp DESC;
```

### **3. Evolução Temporal**
```sql
SELECT timestamp, temperature, current
FROM joint_data
WHERE joint_number = 3
    AND timestamp >= datetime('now', '-6 hours')
ORDER BY timestamp;
```

**📚 Mais queries: QUERIES_SQL_UTEIS.md (25+ exemplos)**

---

## 📈 Gráficos Disponíveis

### **Gerados Automaticamente:**

```
┌─────────────────────────────────────┐
│   Evolução de Temperatura           │
│                                     │
│   Junta 1 ─────                    │
│   Junta 2 ─────                    │
│   Junta 3 ─────                    │
│   ...                               │
│   Limite Alerta  - - - - -         │
│   Limite Crítico ————————          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   Boxplot de Distribuição           │
│                                     │
│   J1  J2  J3  J4  J5  J6           │
│   ▪  ▪  ▪  ▪  ▪  ▪               │
│   │  │  │  │  │  │               │
│   ▪  ▪  ▪  ▪  ▪  ▪               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   Heatmap de Correlação              │
│                                     │
│        Temp  Curr  Torq             │
│   Temp  1.0  0.7   0.5              │
│   Curr  0.7  1.0   0.8              │
│   Torq  0.5  0.8   1.0              │
└─────────────────────────────────────┘
```

**Todos em 300 DPI → Prontos para publicação!**

---

## 🎓 Para Artigos Científicos

### **Fluxo Recomendado:**

```
1. Coletar Dados
   └─► python main_gui.py (deixar rodando 24h+)

2. Análise Rápida
   └─► python exemplo_analise.py

3. Exportar Relatórios
   └─► Interface → Aba Relatórios → PDF + Excel

4. Análises Customizadas
   └─► Python/SQL (GUIA_EXTRACAO_DADOS.md)

5. Backup
   └─► Copiar data/jaka_monitor.db
```

### **Checklist:**
- [ ] ✅ Dados coletados (24h+)
- [ ] ✅ Gráficos gerados (300 DPI)
- [ ] ✅ Estatísticas calculadas
- [ ] ✅ Anomalias documentadas
- [ ] ✅ Período registrado
- [ ] ✅ Configurações salvas
- [ ] ✅ Backup dos dados

---

## 📚 Documentação Completa

```
📖 Para ler AGORA:
   └─► COMO_EXTRAIR_RESULTADOS.md (este guia expandido)

🔍 Para detalhes:
   └─► GUIA_EXTRACAO_DADOS.md (tutorial completo)

💻 Para queries:
   └─► QUERIES_SQL_UTEIS.md (25+ exemplos)

🐍 Para código:
   └─► exemplo_analise.py (script funcional)

🗺️ Para navegar tudo:
   └─► INDEX.md (índice geral)
```

---

## 💡 Dicas Rápidas

### **Começando:**
```powershell
# 1. Instalar
pip install -r requirements.txt

# 2. Configurar
# Edite config.py (MQTT, thresholds)

# 3. Coletar
python main_gui.py

# 4. Analisar
python exemplo_analise.py
```

### **Problemas Comuns:**

**"Banco vazio"**
→ Execute o sistema de monitoramento primeiro!

**"Erro ao importar"**
→ `pip install pandas matplotlib seaborn`

**"Excel não abre"**
→ Use LibreOffice Calc ou Google Sheets

---

## 🚀 Começar AGORA

### **Opção Rápida (5 min):**
```powershell
python main_gui.py
# Aba Relatórios → Gerar PDF
```

### **Opção Análise (10 min):**
```powershell
python exemplo_analise.py
# Ver resultados em: analises/
```

### **Opção Completa:**
```powershell
# Leia: GUIA_EXTRACAO_DADOS.md
# Depois: crie suas análises personalizadas
```

---

## 📊 Exemplo de Resultado Final

### **Para um Artigo:**

```latex
\begin{table}[h]
\caption{Estatísticas das Juntas - 24h de Monitoramento}
\begin{tabular}{|c|c|c|c|}
\hline
Junta & Temp. Média (°C) & Temp. Máx (°C) & Corrente Média (A) \\
\hline
1 & 35.2 ± 2.1 & 42.3 & 1.23 ± 0.15 \\
2 & 36.8 ± 2.3 & 43.1 & 1.31 ± 0.18 \\
...
\hline
\end{tabular}
\end{table}
```

**Fonte dos dados:** `exemplo_analise.py` ou Interface → Excel

---

**✨ Agora você tem TUDO para extrair insights valiosos!**

**Escolha o método que prefere e comece a analisar! 🎉**

---

**📞 Precisa de mais detalhes?**
→ Veja `GUIA_EXTRACAO_DADOS.md`
