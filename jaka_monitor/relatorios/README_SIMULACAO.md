# 🔬 Simulação de Falhas - README

## Scripts de Simulação para Artigos Científicos

Este módulo contém scripts para simular 9 tipos de falhas em robôs industriais e gerar relatórios científicos automatizados.

---

## 📁 Arquivos Principais

### Scripts Python
- **`test_fault_scenarios.py`** - Simulador de falhas (execute primeiro)
- **`analyze_fault_scenarios.py`** - Analisador científico (execute depois)

### Documentação
- **`RESUMO_EXECUTIVO_SIMULACAO.md`** - **COMECE AQUI!** ⭐
- **`QUICK_START_SIMULACAO.md`** - 3 comandos para iniciar
- **`GUIA_SIMULACAO_FALHAS.md`** - Guia técnico completo
- **`FUNDAMENTOS_FISICOS.md`** - Base teórica e equações
- **`COMO_CITAR_ARTIGO.md`** - Templates BibTeX/LaTeX

---

## 🚀 Início Rápido

```bash
# 1. Simular falhas (37 minutos)
python test_fault_scenarios.py

# 2. Analisar resultados (2 minutos)
python analyze_fault_scenarios.py

# 3. Ver resultados
cd analises/fault_scenarios
```

---

## 🔬 9 Cenários Simulados

| # | Cenário | Grandezas | Duração |
|---|---------|-----------|---------|
| 1 | Desgaste de Rolamento | Temp, Corrente, Torque | 180s |
| 2 | Superaquecimento Motor | Temp, Corrente | 150s |
| 3 | Degradação Fonte | Tensão, Corrente | 200s |
| 4 | Desgaste Mecânico | Posição, Torque | 220s |
| 5 | Problema Cabo | Corrente (picos) | 120s |
| 6 | Falta Lubrificação | Temp, Torque | 250s |
| 7 | Deriva Encoder | Posição | 180s |
| 8 | Sobrecarga | Corrente, Temp | 140s |
| 9 | Ressonância | Oscilações | 160s |

---

## 📊 Resultados Gerados

### analises/fault_scenarios/
- **relatorio_cientifico.txt** - Relatório formatado para artigos
- **estatisticas_cenarios.csv** - Tabela de métricas
- **temp_analysis_*.png** - Gráficos temperatura (300 DPI)
- **electrical_analysis_*.png** - Gráficos elétricos (300 DPI)
- **correlation_*.png** - Matrizes de correlação (300 DPI)

---

## 📖 Documentação

### Para Começar (5 minutos)
➡️ `RESUMO_EXECUTIVO_SIMULACAO.md`

### Para Uso Completo (30 minutos)
➡️ `GUIA_SIMULACAO_FALHAS.md`

### Para Fundamentação Teórica (1 hora)
➡️ `FUNDAMENTOS_FISICOS.md`

### Para Citar em Artigos
➡️ `COMO_CITAR_ARTIGO.md`

---

## 🎓 Uso em Artigos

### Materiais e Métodos
```
Foram simulados 9 cenários de falhas comuns em robôs industriais...
```
📄 Templates em: `COMO_CITAR_ARTIGO.md`

### Resultados
- Inserir tabela de `estatisticas_cenarios.csv`
- Incluir gráficos PNG (300 DPI)

### Discussão
- Usar interpretações de `relatorio_cientifico.txt`

---

## ⚙️ Opções de Simulação

### Completa (recomendado)
```bash
python test_fault_scenarios.py
```

### Rápida
```bash
python test_fault_scenarios.py --interval 1.0 --normal-time 10
```

### Específica
```bash
python test_fault_scenarios.py --scenarios bearing,motor
```

---

## 🆘 Problemas?

1. **Simulação não conecta:**
   - Verificar `config.py` (MQTT_BROKER, MQTT_PORT)

2. **Análise retorna vazio:**
   - Verificar dados no banco: `sqlite3 data/jaka_monitor.db "SELECT COUNT(*) FROM robot_data"`

3. **Mais ajuda:**
   - `GUIA_SIMULACAO_FALHAS.md`
   - `TROUBLESHOOTING.md`

---

## 📚 Arquivos Relacionados

- **Análise rápida:** `exemplo_analise.py`
- **Extração de dados:** `COMO_EXTRAIR_RESULTADOS.md`
- **Queries SQL:** `QUERIES_SQL_UTEIS.md`
- **Índice geral:** `INDEX.md`

---

**Para documentação completa, veja `INDEX.md`** 📖
