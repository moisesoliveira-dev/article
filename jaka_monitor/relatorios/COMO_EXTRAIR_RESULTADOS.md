# 🚀 Guia Rápido - Extração de Resultados

## 3 Métodos Simples para Analisar seus Dados

---

## 🎯 Método 1: Interface Gráfica (MAIS FÁCIL) ⭐

### **Passo a Passo:**

1. **Abra o sistema:**
   ```powershell
   python main_gui.py
   ```

2. **Vá para a aba "Relatórios"**

3. **Clique nos botões:**

   **📄 Gerar Relatório PDF Completo**
   - Contém: Gráficos + Estatísticas + Anomalias
   - Localização: `reports/relatorio_completo_*.pdf`
   - ✅ Pronto para usar em artigos!

   **📊 Exportar Dados para Excel**
   - Contém: 5 abas com dados organizados
   - Localização: `reports/dados_exportados_*.xlsx`
   - ✅ Abra no Excel e analise!

---

## 🐍 Método 2: Script Pronto (RÁPIDO)

### **Execute o script de exemplo:**

```powershell
python exemplo_analise.py
```

### **O que ele faz automaticamente:**
- ✅ Mostra estatísticas das juntas
- ✅ Lista todas as anomalias
- ✅ Gera 4 gráficos em alta resolução (300 DPI)
- ✅ Exporta dados em CSV
- ✅ Calcula correlações

### **Resultados em:** `analises/`

```
analises/
├── estatisticas_juntas.csv          ← Média, max, min por junta
├── resumo_eventos.csv               ← Todas as anomalias
├── grafico_temperatura.png          ← Evolução temporal
├── grafico_corrente.png             ← Evolução de corrente
├── boxplot_temperatura.png          ← Distribuição
├── heatmap_correlacao.png           ← Matriz de correlação
└── [tabela]_completo.csv            ← Dados brutos
```

---

## 💻 Método 3: Python Personalizado (FLEXÍVEL)

### **Template básico:**

```python
import sqlite3
import pandas as pd

# Conectar ao banco
conn = sqlite3.connect('data/jaka_monitor.db')

# Sua query SQL
df = pd.read_sql_query("""
    SELECT 
        joint_number,
        AVG(temperature) as temp_media,
        MAX(temperature) as temp_max
    FROM joint_data
    WHERE timestamp >= datetime('now', '-24 hours')
    GROUP BY joint_number
""", conn)

# Ver resultados
print(df)

# Exportar
df.to_csv('minha_analise.csv', index=False)

conn.close()
```

---

## 📊 O Que Cada Método Oferece

| Recurso | Interface GUI | Script Pronto | Python Custom |
|---------|--------------|---------------|---------------|
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Velocidade** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡ | ⚡⚡⚡ |
| **Flexibilidade** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Gráficos** | ✅ Sim | ✅ 4 gráficos | ✅ Ilimitado |
| **Personalização** | ❌ Não | ⚠️ Limitada | ✅ Total |
| **Para Artigos** | ✅ Sim | ✅ Sim | ✅ Sim |

---

## 📁 Estrutura de Dados

### **Banco de Dados:** `data/jaka_monitor.db`

**Principais Tabelas:**

1. **`robot_data`** - Dados gerais do robô
   - ID, nome, temperatura, estado, etc.

2. **`joint_data`** - Dados de cada junta (1-6)
   - Temperatura, corrente, torque, posição, velocidade

3. **`events`** - Anomalias detectadas
   - Tipo, severidade, descrição, valor, threshold

4. **`tcp_positions`** - Posições TCP (x, y, z, rx, ry, rz)

5. **`statistics`** - Estatísticas agregadas

---

## 🔍 Queries SQL Úteis

### **Temperatura média das juntas:**
```sql
SELECT 
    joint_number,
    AVG(temperature) as temp_media,
    MAX(temperature) as temp_max
FROM joint_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY joint_number;
```

### **Anomalias críticas:**
```sql
SELECT * FROM events
WHERE severity IN ('critical', 'emergency')
ORDER BY timestamp DESC;
```

### **Evolução temporal (Junta 3):**
```sql
SELECT timestamp, temperature, current, torque
FROM joint_data
WHERE joint_number = 3
    AND timestamp >= datetime('now', '-6 hours')
ORDER BY timestamp;
```

---

## 📈 Gráficos Prontos no Script

### 1. **Evolução de Temperatura**
- Linha do tempo para todas as 6 juntas
- Limites de alerta e crítico marcados
- 300 DPI (publicável)

### 2. **Evolução de Corrente**
- Consumo de corrente ao longo do tempo
- Comparação entre juntas
- Limites destacados

### 3. **Boxplot de Temperatura**
- Distribuição estatística
- Identifica outliers
- Comparação entre juntas

### 4. **Heatmap de Correlação**
- Correlações entre variáveis
- Temperatura vs Corrente vs Torque
- Para todas as juntas

---

## 🎓 Para Artigos Científicos

### **Checklist:**

- [ ] Coletou dados por **24+ horas**
- [ ] Gerou **relatório PDF completo**
- [ ] Exportou dados para **Excel**
- [ ] Executou **script de análise**
- [ ] Criou **gráficos em alta resolução** (300 DPI)
- [ ] Documentou **período e configurações**
- [ ] Salvou **backup dos dados brutos**

### **Formato dos Dados:**

**CSV** → Excel, Google Sheets, SPSS  
**PNG (300 DPI)** → Artigos, apresentações  
**PDF (relatório)** → Documentação completa  
**SQLite** → Análises avançadas

---

## 💡 Exemplos Práticos

### **Exemplo 1: Tabela para Artigo**

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect('data/jaka_monitor.db')
df = pd.read_sql_query("""
    SELECT 
        joint_number as 'Junta',
        ROUND(AVG(temperature), 2) as 'Temperatura Média (°C)',
        ROUND(MAX(temperature), 2) as 'Temperatura Máxima (°C)'
    FROM joint_data
    GROUP BY joint_number
""", conn)

print(df.to_latex(index=False))  # Formato LaTeX
print(df.to_markdown(index=False))  # Formato Markdown
```

### **Exemplo 2: Gráfico Customizado**

```python
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

conn = sqlite3.connect('data/jaka_monitor.db')
df = pd.read_sql_query("""
    SELECT timestamp, temperature 
    FROM joint_data 
    WHERE joint_number = 1
""", conn)

plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['temperature'])
plt.xlabel('Tempo')
plt.ylabel('Temperatura (°C)')
plt.title('Evolução Térmica - Junta 1')
plt.savefig('figura_artigo.png', dpi=300)
```

---

## 🆘 Problemas Comuns

### **"Banco de dados vazio"**
```python
import sqlite3
conn = sqlite3.connect('data/jaka_monitor.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM robot_data")
print(f"Registros: {cursor.fetchone()[0]}")
```
Se retornar 0 → Execute o sistema de monitoramento primeiro!

### **"Script não funciona"**
```powershell
pip install pandas matplotlib seaborn openpyxl
```

### **"Erro ao abrir Excel"**
Use LibreOffice Calc ou Google Sheets como alternativa

---

## 📚 Documentação Completa

- **`GUIA_EXTRACAO_DADOS.md`** - Guia detalhado completo
- **`exemplo_analise.py`** - Script pronto para usar
- **`offline_analysis.py`** - Analisador offline avançado

---

## 🚀 Começar Agora

### **Opção A: Mais Fácil**
```powershell
python main_gui.py
# Aba Relatórios → Gerar PDF
```

### **Opção B: Análise Rápida**
```powershell
python exemplo_analise.py
# Resultados em: analises/
```

### **Opção C: Personalizado**
```powershell
# Crie seu próprio script baseado nos exemplos
```

---

**✨ Agora você tem tudo para extrair insights dos seus dados!**

Escolha o método que melhor se adapta às suas necessidades e comece a analisar! 🎉
