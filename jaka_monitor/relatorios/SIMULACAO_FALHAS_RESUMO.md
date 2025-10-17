# 🔬 Simulação de Falhas para Artigos Científicos

## Início Rápido (3 passos)

### 1️⃣ Execute a Simulação
```bash
python test_fault_scenarios.py
```
Tempo estimado: ~37 minutos (9 cenários)

### 2️⃣ Analise os Resultados
```bash
python analyze_fault_scenarios.py
```

### 3️⃣ Use no seu Artigo
Resultados em: `analises/fault_scenarios/`
- 📊 Gráficos PNG (300 DPI)
- 📝 Relatório científico (TXT)
- 📈 Estatísticas (CSV)

---

## 🔬 9 Cenários de Falha Implementados

| # | Cenário | Grandezas Alteradas | Duração |
|---|---------|---------------------|---------|
| 1 | **Desgaste de Rolamento** | Temp (+15°C), Corrente (vibração), Torque | 180s |
| 2 | **Superaquecimento Motor** | Temp (+25°C), Corrente (↑40%), Torque | 150s |
| 3 | **Degradação Fonte** | Tensão (±4V), Corrente (ripple) | 200s |
| 4 | **Desgaste Mecânico** | Posição (folga 1.5°), Torque, Temp | 220s |
| 5 | **Problema Cabo** | Corrente (picos ×3), Valores intermitentes | 120s |
| 6 | **Falta Lubrificação** | Temp (+18°C), Torque (↑60%), Corrente | 250s |
| 7 | **Deriva Encoder** | Posição (erro acumulado), Corrente | 180s |
| 8 | **Sobrecarga** | Corrente (↑80%), Temp (+22°C), Torque | 140s |
| 9 | **Ressonância** | Corrente/Torque (oscilação), Temp | 160s |

---

## 📊 O que Você Recebe

### Relatório Científico (`relatorio_cientifico.txt`)

Para cada cenário:
- ✅ Descrição física do fenômeno
- ✅ Causas fundamentais
- ✅ Métricas quantitativas
- ✅ Indicadores de falha
- ✅ Interpretação científica
- ✅ Correlações esperadas

**Exemplo:**
```
CENÁRIO 1: Desgaste de Rolamento - Junta 3

📋 DESCRIÇÃO:
   Desgaste progressivo do rolamento causando aumento de temperatura,
   vibração e consumo de corrente devido ao atrito excessivo.

📊 MÉTRICAS OBSERVADAS:
   • Temperatura máxima: 52.34°C
   • Taxa de aquecimento: 0.0847°C/min
   • Variabilidade de corrente (CV): 0.1823
   • Aumento de torque: 0.421 Nm
   • Frequência dominante: 2.347 Hz

💡 INTERPRETAÇÃO CIENTÍFICA:
   O desgaste do rolamento manifesta-se através de três fenômenos:
   1. Aumento térmico: atrito metal-metal gera calor
   2. Vibração mecânica: irregularidades causam oscilações
   3. Sobrecarga elétrica: motor compensa perdas
```

### Gráficos (300 DPI)

**Temperatura:**
- Evolução temporal
- Distribuição por junta
- Limites de alerta/crítico

**Análise Elétrica:**
- Corrente vs. tempo
- Tensão vs. tempo
- Potência (V×I)

**Correlações:**
- Matriz de correlação
- Heatmap

### Estatísticas CSV

Tabela pronta para copiar ao artigo:

| Cenário | Junta | Temp_Max_C | Taxa_Aquec | Var_Corrente |
|---------|-------|------------|------------|--------------|
| Rolamento | 3 | 52.34 | 0.0847 | 0.182 |
| Motor | 2 | 68.91 | 0.2134 | 0.156 |

---

## ⚙️ Opções de Simulação

### Simulação Completa (recomendado)
```bash
python test_fault_scenarios.py
```

### Simulação Rápida
```bash
python test_fault_scenarios.py --interval 1.0 --normal-time 10
```

### Cenários Específicos
```bash
# Apenas desgaste e superaquecimento
python test_fault_scenarios.py --scenarios bearing,motor

# Apenas problemas elétricos
python test_fault_scenarios.py --scenarios power,cable
```

---

## 📖 Documentação Completa

Para detalhes técnicos, causas físicas e customizações:

➡️ **`GUIA_SIMULACAO_FALHAS.md`**

Contém:
- Explicação científica de cada cenário
- Como modificar intensidade/duração
- Como criar novos cenários
- Análises avançadas customizadas
- Referências técnicas
- Troubleshooting

---

## 🎓 Uso em Artigos

### Materiais e Métodos
```
Foram simulados 9 cenários de falhas comuns em robôs industriais,
incluindo desgaste de rolamento, superaquecimento do motor, degradação
da fonte de alimentação, entre outros. Cada cenário reproduz alterações
nas grandezas físicas (corrente, tensão, temperatura, torque e posição)
conforme documentado na literatura.
```

### Resultados
- Copie tabelas de `estatisticas_cenarios.csv`
- Insira gráficos PNG (300 DPI)
- Use valores numéricos do relatório

### Discussão
- Use interpretações científicas do `relatorio_cientifico.txt`
- Compare métricas com literatura
- Valide eficácia da detecção precoce

---

## 🆘 Troubleshooting

**Simulação não inicia:**
```bash
# Verifique config.py
MQTT_BROKER = "147.1.5.238"
MQTT_PORT = 1883
```

**Análise retorna vazio:**
```bash
# Verifique se há dados
sqlite3 data/jaka_monitor.db "SELECT COUNT(*) FROM robot_data"
```

**Gráficos não aparecem:**
```bash
# Instale dependências
pip install matplotlib seaborn pandas
```

---

## 📚 Arquivos Relacionados

- `test_fault_scenarios.py` - Simulador
- `analyze_fault_scenarios.py` - Analisador
- `GUIA_SIMULACAO_FALHAS.md` - Documentação completa
- `COMO_EXTRAIR_RESULTADOS.md` - Extração de dados
- `QUERIES_SQL_UTEIS.md` - Queries SQL

---

**Para dúvidas, consulte `GUIA_SIMULACAO_FALHAS.md`** 📖
