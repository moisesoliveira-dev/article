# ⚡ INÍCIO RÁPIDO - Simulação de Falhas

## 🎯 O que Foi Criado

Dois scripts Python que simulam 9 tipos de falhas em robôs industriais e geram relatórios científicos prontos para artigos.

---

## 🚀 Uso em 3 Comandos

```bash
# 1. Simular falhas (~37 min)
python test_fault_scenarios.py

# 2. Analisar resultados
python analyze_fault_scenarios.py

# 3. Pegar resultados
cd analises/fault_scenarios
```

---

## 📦 O que Você Recebe

### 📊 Gráficos (300 DPI)
- `temp_analysis_*.png` - Evolução de temperatura
- `electrical_analysis_*.png` - Corrente/tensão/potência
- `correlation_*.png` - Matriz de correlação

### 📝 Relatório Científico
- `relatorio_cientifico.txt`
  - Descrição de cada falha
  - Causas físicas
  - Métricas numéricas
  - Interpretação científica
  - **Pronto para copiar ao artigo!**

### 📈 Estatísticas
- `estatisticas_cenarios.csv`
  - Tabela formatada
  - **Copiar direto para Excel/LaTeX**

---

## 🔬 9 Cenários Simulados

| Cenário | O que Altera | Causa |
|---------|--------------|-------|
| 1. Desgaste Rolamento | Temp +15°C, vibração | Fadiga do material |
| 2. Superaquecimento | Temp +25°C, corrente +40% | Ventilação obstruída |
| 3. Fonte Degradada | Tensão ±4V instável | Capacitor velho |
| 4. Desgaste Mecânico | Folga 1.5°, torque | Engrenagens gastas |
| 5. Cabo Ruim | Picos de corrente ×3 | Mau contato |
| 6. Sem Lubrificação | Temp +18°C, torque +60% | Óleo degradado |
| 7. Encoder Deriva | Erro posição crescente | Desalinhamento |
| 8. Sobrecarga | Corrente +80%, temp +22°C | Carga excessiva |
| 9. Ressonância | Oscilação 2-5 Hz | Freq. natural |

---

## 💡 Exemplo de Resultado

```
CENÁRIO 1: Desgaste de Rolamento - Junta 3
──────────────────────────────────────────

📊 MÉTRICAS OBSERVADAS:
   • Temperatura máxima: 52.34°C
   • Taxa de aquecimento: 0.0847°C/min
   • Variabilidade de corrente: 0.1823
   • Aumento de torque: 0.421 Nm
   • Frequência dominante: 2.347 Hz

💡 INTERPRETAÇÃO CIENTÍFICA:
   O desgaste do rolamento manifesta-se através de:
   1. Aumento térmico: atrito metal-metal gera calor
   2. Vibração mecânica: irregularidades causam oscilações
   3. Sobrecarga elétrica: motor compensa perdas mecânicas
```

---

## 📖 Documentação Completa

- **`GUIA_SIMULACAO_FALHAS.md`** - Guia completo (leia isso!)
  - Detalhes de cada cenário
  - Como customizar
  - Como criar novos cenários
  - Troubleshooting

- **`FUNDAMENTOS_FISICOS.md`** - Base teórica
  - Equações físicas
  - Correlações esperadas
  - Referências científicas

- **`SIMULACAO_FALHAS_RESUMO.md`** - Resumo visual

---

## ⚙️ Opções Úteis

### Simulação Mais Rápida
```bash
python test_fault_scenarios.py --interval 1.0 --normal-time 10
```

### Apenas Alguns Cenários
```bash
python test_fault_scenarios.py --scenarios bearing,motor,power
```

### Análise de Período Específico
```bash
python analyze_fault_scenarios.py --hours 2
```

---

## 🎓 Usar no Artigo

### 1. Materiais e Métodos
Copie a descrição dos cenários do `relatorio_cientifico.txt`

### 2. Resultados
- Insira gráficos PNG (300 DPI)
- Copie tabela de `estatisticas_cenarios.csv`

### 3. Discussão
Use as "Interpretações Científicas" do relatório

### 4. Referências
Veja `FUNDAMENTOS_FISICOS.md` para citações

---

## ✅ Checklist

- [ ] Executar `test_fault_scenarios.py`
- [ ] Manter `main_gui.py` rodando durante simulação
- [ ] Executar `analyze_fault_scenarios.py`
- [ ] Copiar arquivos de `analises/fault_scenarios/`
- [ ] Inserir gráficos no artigo
- [ ] Copiar estatísticas para tabelas
- [ ] Adicionar interpretações científicas

---

## 🆘 Problemas?

**Simulação não conecta:**
```python
# Verificar config.py
MQTT_BROKER = "147.1.5.238"
MQTT_PORT = 1883
```

**Análise retorna vazio:**
```bash
# Verificar dados no banco
sqlite3 data/jaka_monitor.db "SELECT COUNT(*) FROM robot_data"
```

**Mais ajuda:**
- `GUIA_SIMULACAO_FALHAS.md`
- `TROUBLESHOOTING.md`

---

## 📁 Arquivos Criados

```
jaka_monitor/
├── test_fault_scenarios.py           🔬 Simulador
├── analyze_fault_scenarios.py        📊 Analisador
├── GUIA_SIMULACAO_FALHAS.md          📖 Guia completo
├── FUNDAMENTOS_FISICOS.md            🔬 Base teórica
├── SIMULACAO_FALHAS_RESUMO.md        📋 Resumo
└── analises/fault_scenarios/         💾 Resultados
    ├── relatorio_cientifico.txt
    ├── estatisticas_cenarios.csv
    └── *.png (gráficos 300 DPI)
```

---

## 🎯 Pronto!

Tudo o que você precisa para simular falhas e gerar dados para seu artigo científico.

**Comece agora:**
```bash
python test_fault_scenarios.py
```

**Enquanto roda, leia:**
- `GUIA_SIMULACAO_FALHAS.md` (detalhes técnicos)
- `FUNDAMENTOS_FISICOS.md` (base teórica)

---

**Boa sorte com seu artigo! 🎓📊**
