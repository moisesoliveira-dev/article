# 📊 Guia Completo - Extração e Análise de Resultados

## Sistema JAKA Monitor - Análise de Dados para Artigos Científicos

---

## 🎯 Visão Geral

Este guia mostra **passo a passo** como extrair e analisar os dados coletados pelo sistema de monitoramento JAKA.

### **O que você pode fazer:**
1. ✅ Gerar relatórios em **PDF** com gráficos e estatísticas
2. ✅ Exportar dados em **Excel** para análises personalizadas
3. ✅ Acessar banco de dados **SQLite** diretamente
4. ✅ Análise offline com **Python/Pandas**
5. ✅ Criar gráficos customizados para publicações

---

## 📁 Onde os Dados Estão Armazenados

```
jaka_monitor/
├── data/
│   └── jaka_monitor.db          ← Banco de dados principal (SQLite)
├── reports/
│   ├── relatorio_completo_*.pdf ← Relatórios PDF gerados
│   ├── dados_exportados_*.xlsx  ← Exportações Excel
│   └── *_graph_*.png            ← Gráficos temporários
└── logs/
    └── system_*.log             ← Logs do sistema
```

---

## 📊 Método 1: Interface Gráfica (Mais Fácil)

### **Passo 1: Gerar Relatório PDF Completo**

1. **Abra a interface**:
   ```powershell
   python main_gui.py
   ```

2. **Vá para aba "Relatórios"**

3. **Clique em "Gerar Relatório PDF Completo"**

4. **O que contém:**
   - 📈 Gráfico de temperatura das juntas ao longo do tempo
   - 📈 Gráfico de corrente das juntas
   - 📈 Gráfico de torque/carga
   - 📊 Estatísticas detalhadas por junta
   - ⚠️ Lista de todas as anomalias detectadas
   - 📝 Resumo executivo do período

5. **Localização**: `reports/relatorio_completo_YYYYMMDD_HHMMSS.pdf`

### **Passo 2: Exportar para Excel**

1. **Na aba "Relatórios"**, clique em **"Exportar Dados para Excel"**

2. **O que contém (múltiplas abas):**
   - **Dados do Robô**: Todos os registros gerais
   - **Dados das Juntas**: Temperatura, corrente, torque, etc.
   - **Eventos**: Anomalias detectadas
   - **Posições TCP**: Posições do Tool Center Point
   - **Estatísticas**: Médias, desvios, mín/máx

3. **Localização**: `reports/dados_exportados_YYYYMMDD_HHMMSS.xlsx`

4. **Como usar:**
   - Abra no Excel, LibreOffice ou Google Sheets
   - Cada aba tem dados formatados e prontos
   - Use para criar suas próprias análises

---

## 🗄️ Método 2: Acessar Banco de Dados Diretamente

### **Estrutura do Banco (SQLite)**

O arquivo `data/jaka_monitor.db` contém 5 tabelas principais:

#### **Tabela 1: `robot_data`**
Dados gerais do robô em cada momento

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único do registro |
| `timestamp` | DATETIME | Data/hora da coleta |
| `robot_id` | INTEGER | ID do robô JAKA |
| `robot_name` | TEXT | Nome do robô |
| `task_state` | INTEGER | Estado da tarefa (0-5) |
| `enabled` | BOOLEAN | Robô habilitado? |
| `powered_on` | INTEGER | Robô ligado? |
| `emergency_stop` | INTEGER | Parada de emergência? |
| `robot_temp` | REAL | Temperatura do robô (°C) |
| `ambient_temp` | REAL | Temperatura ambiente |
| `tcp_velocity` | REAL | Velocidade TCP |
| `json_data` | TEXT | Dados brutos completos (JSON) |

#### **Tabela 2: `joint_data`**
Dados individuais de cada junta

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único |
| `robot_data_id` | INTEGER | FK para robot_data |
| `timestamp` | DATETIME | Data/hora |
| `joint_number` | INTEGER | Número da junta (1-6) |
| `position` | REAL | Posição (graus) |
| `actual_position` | REAL | Posição real |
| `velocity` | REAL | Velocidade (rad/s) |
| `current` | REAL | Corrente (A) |
| `temperature` | REAL | Temperatura (°C) |
| `voltage` | REAL | Voltagem (V) |
| `torque` | REAL | Torque |
| `error_status` | REAL | Status de erro |

#### **Tabela 3: `events`**
Anomalias e eventos detectados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único |
| `timestamp` | DATETIME | Quando ocorreu |
| `event_type` | TEXT | Tipo de evento |
| `severity` | TEXT | info/warning/critical/emergency |
| `joint_number` | INTEGER | Junta afetada (ou NULL) |
| `description` | TEXT | Descrição textual |
| `value` | REAL | Valor que causou o alerta |
| `threshold` | REAL | Limite que foi ultrapassado |
| `duration` | REAL | Duração em segundos |
| `resolved` | BOOLEAN | Evento resolvido? |

#### **Tabela 4: `tcp_positions`**
Posições do Tool Center Point

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `robot_data_id` | INTEGER | FK para robot_data |
| `x`, `y`, `z` | REAL | Posição cartesiana (mm) |
| `rx`, `ry`, `rz` | REAL | Orientação (graus) |

#### **Tabela 5: `statistics`**
Estatísticas agregadas por período

---

### **Exemplos de Consultas SQL**

#### **1. Dados das últimas 24 horas**
```sql
SELECT * FROM robot_data
WHERE timestamp >= datetime('now', '-24 hours')
ORDER BY timestamp DESC;
```

#### **2. Temperatura média por junta**
```sql
SELECT 
    joint_number,
    AVG(temperature) as temp_media,
    MAX(temperature) as temp_maxima,
    MIN(temperature) as temp_minima,
    STDDEV(temperature) as desvio_padrao
FROM joint_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY joint_number
ORDER BY joint_number;
```

#### **3. Eventos críticos**
```sql
SELECT 
    timestamp,
    event_type,
    severity,
    joint_number,
    description,
    value,
    threshold
FROM events
WHERE severity IN ('critical', 'emergency')
ORDER BY timestamp DESC;
```

#### **4. Evolução de temperatura da Junta 3**
```sql
SELECT 
    timestamp,
    temperature,
    current,
    torque
FROM joint_data
WHERE joint_number = 3
    AND timestamp >= datetime('now', '-6 hours')
ORDER BY timestamp;
```

#### **5. Contagem de eventos por tipo**
```sql
SELECT 
    event_type,
    severity,
    COUNT(*) as quantidade,
    AVG(duration) as duracao_media
FROM events
GROUP BY event_type, severity
ORDER BY quantidade DESC;
```

---

## 🐍 Método 3: Análise Offline com Python

### **Script: `offline_analysis.py`**

Já existe um script pronto para análises offline!

#### **Uso Básico**

```powershell
python offline_analysis.py
```

#### **Como Usar o Script**

```python
from offline_analysis import OfflineAnalyzer

# Criar analisador
analyzer = OfflineAnalyzer()

# 1. Ver resumo dos dados
analyzer.get_data_summary()

# 2. Analisar tendências das juntas
analyzer.analyze_joint_trends(joint_number=3, hours=24)  # Junta 3, últimas 24h
analyzer.analyze_joint_trends(hours=48)  # Todas as juntas, últimas 48h

# 3. Analisar eventos
analyzer.analyze_events(hours=24)

# 4. Análise de desempenho do robô
analyzer.analyze_robot_performance(hours=24)

# 5. Exportar dados customizados
analyzer.export_custom_data(
    start_time="2025-10-15 00:00:00",
    end_time="2025-10-17 23:59:59",
    output_file="minha_analise.xlsx"
)
```

---

## 📈 Método 4: Análise com Pandas (Personalizada)

### **Exemplo Completo: Análise Customizada**

```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar ao banco
conn = sqlite3.connect('data/jaka_monitor.db')

# 1. Carregar dados das juntas
df_joints = pd.read_sql_query("""
    SELECT 
        timestamp,
        joint_number,
        temperature,
        current,
        torque,
        velocity
    FROM joint_data
    WHERE timestamp >= datetime('now', '-24 hours')
    ORDER BY timestamp
""", conn)

# Converter timestamp para datetime
df_joints['timestamp'] = pd.to_datetime(df_joints['timestamp'])

# 2. Estatísticas descritivas
print("📊 ESTATÍSTICAS DAS JUNTAS:")
print(df_joints.groupby('joint_number').describe())

# 3. Criar gráfico de temperatura
plt.figure(figsize=(14, 6))
for joint in range(1, 7):
    data = df_joints[df_joints['joint_number'] == joint]
    plt.plot(data['timestamp'], data['temperature'], 
             label=f'Junta {joint}', marker='o', markersize=3)

plt.axhline(y=40, color='orange', linestyle='--', label='Limite Alerta')
plt.axhline(y=50, color='red', linestyle='--', label='Limite Crítico')
plt.xlabel('Tempo')
plt.ylabel('Temperatura (°C)')
plt.title('Evolução da Temperatura das Juntas')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('temperatura_juntas.png', dpi=300)
plt.show()

# 4. Análise de correlações
correlacao = df_joints[['temperature', 'current', 'torque', 'velocity']].corr()
print("\n🔗 MATRIZ DE CORRELAÇÃO:")
print(correlacao)

# 5. Detectar outliers
Q1 = df_joints['temperature'].quantile(0.25)
Q3 = df_joints['temperature'].quantile(0.75)
IQR = Q3 - Q1
outliers = df_joints[(df_joints['temperature'] < Q1 - 1.5*IQR) | 
                     (df_joints['temperature'] > Q3 + 1.5*IQR)]
print(f"\n⚠️ {len(outliers)} outliers detectados")

# 6. Exportar para análise em outro software
df_joints.to_csv('dados_juntas_analise.csv', index=False)
print("\n✅ Dados exportados para: dados_juntas_analise.csv")

conn.close()
```

---

## 📊 Método 5: Ferramentas de Terceiros

### **Opção A: DB Browser for SQLite (GUI)**

1. **Download**: https://sqlitebrowser.org/
2. **Instalar** e abrir
3. **Abrir banco**: `data/jaka_monitor.db`
4. **Explorar** tabelas visualmente
5. **Executar** queries SQL
6. **Exportar** resultados (CSV, JSON, SQL)

### **Opção B: DBeaver (Profissional)**

1. **Download**: https://dbeaver.io/
2. **Conectar** ao SQLite
3. **ER Diagram** automático
4. **Queries avançadas**
5. **Visualizações** de dados

### **Opção C: Jupyter Notebook**

```python
# Instalar Jupyter
pip install jupyter pandas matplotlib seaborn

# Criar notebook
jupyter notebook
```

**Exemplo de célula:**
```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('data/jaka_monitor.db')

# Query interativa
df = pd.read_sql_query("""
    SELECT * FROM joint_data 
    WHERE joint_number = 1 
    LIMIT 100
""", conn)

df.head()
df.plot()
```

---

## 📝 Exemplos para Artigos Científicos

### **Exemplo 1: Tabela de Estatísticas**

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('data/jaka_monitor.db')

# Dados para tabela do artigo
stats = pd.read_sql_query("""
    SELECT 
        joint_number as 'Junta',
        ROUND(AVG(temperature), 2) as 'Temp. Média (°C)',
        ROUND(MAX(temperature), 2) as 'Temp. Máxima (°C)',
        ROUND(AVG(current), 3) as 'Corrente Média (A)',
        ROUND(MAX(current), 3) as 'Corrente Máxima (A)',
        ROUND(AVG(torque), 2) as 'Torque Médio',
        COUNT(*) as 'Amostras'
    FROM joint_data
    WHERE timestamp >= datetime('now', '-24 hours')
    GROUP BY joint_number
    ORDER BY joint_number
""", conn)

print(stats.to_latex(index=False))  # Formato LaTeX para artigos
print(stats.to_markdown(index=False))  # Formato Markdown
```

### **Exemplo 2: Gráfico Publicável**

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar para publicação
plt.style.use('seaborn-v0_8-paper')
sns.set_context("paper", font_scale=1.5)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

# ... seu código de plot ...

plt.xlabel('Tempo (horas)', fontsize=14)
plt.ylabel('Temperatura (°C)', fontsize=14)
plt.title('Monitoramento Térmico do Robô JAKA', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='best', frameon=True, shadow=True)
plt.tight_layout()

# Salvar em alta resolução
plt.savefig('figura_artigo.png', dpi=300, bbox_inches='tight')
plt.savefig('figura_artigo.pdf', bbox_inches='tight')  # Formato vetorial
```

### **Exemplo 3: Análise de Anomalias**

```python
# Quantidade de anomalias por severidade
anomalias = pd.read_sql_query("""
    SELECT 
        severity,
        COUNT(*) as quantidade,
        AVG(duration) as duracao_media,
        event_type
    FROM events
    GROUP BY severity, event_type
""", conn)

# Gráfico de barras
anomalias.pivot(index='event_type', columns='severity', values='quantidade').plot(
    kind='bar', 
    figsize=(12, 6),
    color=['blue', 'orange', 'red']
)
plt.ylabel('Quantidade de Eventos')
plt.xlabel('Tipo de Evento')
plt.title('Distribuição de Anomalias por Severidade')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('anomalias_artigo.png', dpi=300)
```

---

## 🎯 Checklist de Análise para Artigos

### **Antes de Publicar:**

- [ ] Dados coletados por **período significativo** (mín. 24h)
- [ ] **Estatísticas descritivas** calculadas (média, DP, mín/máx)
- [ ] **Gráficos** salvos em alta resolução (300 DPI)
- [ ] **Anomalias** identificadas e classificadas
- [ ] **Correlações** entre variáveis analisadas
- [ ] **Tabelas** formatadas (LaTeX/Markdown)
- [ ] **Metadados** documentados (data, configuração, etc.)
- [ ] **Backup** dos dados brutos

---

## 💡 Dicas Importantes

### **1. Período de Coleta**
- **Mínimo**: 24 horas para dados confiáveis
- **Recomendado**: 7 dias para padrões completos
- **Ideal**: 30 dias para análise estatística robusta

### **2. Qualidade dos Dados**
```python
# Verificar qualidade
df.isnull().sum()  # Valores faltantes
df.describe()      # Estatísticas
df.info()          # Tipos de dados
```

### **3. Reprodutibilidade**
- Documente **todas as configurações** (thresholds, etc.)
- Salve **scripts de análise**
- Mantenha **backup dos dados brutos**
- Anote **data/hora** de início e fim da coleta

### **4. Visualizações**
- Use **cores consistentes**
- Adicione **legendas claras**
- Inclua **unidades de medida**
- Salve em **formato vetorial** (PDF) quando possível

---

## 🆘 Troubleshooting

### **Problema: Banco vazio**
```python
import sqlite3
conn = sqlite3.connect('data/jaka_monitor.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM robot_data")
print(f"Registros: {cursor.fetchone()[0]}")
```

### **Problema: Dados incompletos**
```python
# Ver última coleta
cursor.execute("SELECT MAX(timestamp) FROM robot_data")
print(f"Última coleta: {cursor.fetchone()[0]}")
```

### **Problema: Excel não abre**
- Instale: `pip install openpyxl xlsxwriter`
- Ou use LibreOffice Calc

---

## 📚 Recursos Adicionais

### **Documentação**
- SQLite: https://www.sqlite.org/docs.html
- Pandas: https://pandas.pydata.org/docs/
- Matplotlib: https://matplotlib.org/
- Seaborn: https://seaborn.pydata.org/

### **Tutoriais**
- SQL para análise: https://mode.com/sql-tutorial/
- Pandas Cheat Sheet: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf

---

## ✅ Próximos Passos

1. **Colete dados** por período adequado
2. **Explore** com interface gráfica primeiro
3. **Exporte** para Excel/PDF
4. **Análise detalhada** com Python/Pandas
5. **Crie visualizações** para publicação
6. **Documente** sua metodologia

---

**Agora você tem todas as ferramentas para extrair insights valiosos dos seus dados! 📊🚀**

Qualquer dúvida, consulte os scripts de exemplo ou os métodos já implementados no sistema.
