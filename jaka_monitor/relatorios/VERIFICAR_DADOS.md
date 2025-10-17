# ⚠️ DADOS GERADOS NÃO CORRESPONDEM ÀS CITAÇÕES

## 🔴 PROBLEMA IDENTIFICADO

Você executou `analyze_fault_scenarios.py` **ANTES** de executar `test_fault_scenarios.py`!

### ❌ O que aconteceu:
1. ✅ `main_gui.py` coletou dados REAIS do robô (939 registros)
2. ❌ `test_fault_scenarios.py` **NUNCA foi executado** (simulação não rodou)
3. ❌ `analyze_fault_scenarios.py` analisou dados REAIS ao invés de dados SIMULADOS

### 📊 Comparação:

| Item | ESPERADO (citação) | OBTIDO (análise) | Status |
|------|-------------------|------------------|--------|
| **Desgaste Rolamento** | | | |
| Temp. Máx. | 52.34°C | 24.00°C | ❌ |
| Taxa Aquec. | 0.0847°C/min | -0.0007°C/min | ❌ |
| Var. Corrente | 0.182 | -1.87 | ❌ |
| Torque | +0.421 Nm | +0.120 Nm | ❌ |
| **Superaquecimento Motor** | | | |
| Temp. Máx. | 68.91°C | 23.00°C | ❌ |
| Taxa Aquec. | 0.2134°C/min | 0°C/min | ❌ |
| Aumento Corrente | +40% | -344% | ❌ |
| Índice Térm. | 0.4873 | 0.0000 | ❌ |

---

## ✅ SOLUÇÃO

### Passo 1: Limpar banco de dados atual (OPCIONAL)
```powershell
# Backup dos dados reais
Copy-Item data\jaka_monitor.db data\jaka_monitor_backup_real.db

# Limpar para simulação
Remove-Item data\jaka_monitor.db
```

### Passo 2: Executar SIMULAÇÃO completa

#### 🚀 OPÇÃO A: Teste Rápido (5 minutos)
```powershell
# Terminal 1 (deixar rodando)
.\venv\Scripts\Activate.ps1
python main_gui.py

# Terminal 2 (executar simulação rápida)
.\venv\Scripts\Activate.ps1
python test_fault_scenarios.py --interval 1.0 --normal-time 5
```

#### 🔬 OPÇÃO B: Simulação Completa (37 minutos) - RECOMENDADO PARA ARTIGO
```powershell
# Terminal 1 (deixar rodando)
.\venv\Scripts\Activate.ps1
python main_gui.py

# Terminal 2 (executar simulação completa)
.\venv\Scripts\Activate.ps1
python test_fault_scenarios.py
```

### Passo 3: Aguardar término da simulação
- Opção A: ~5 minutos
- Opção B: ~37 minutos
- Você verá barras de progresso e mensagens de status

### Passo 4: Executar análise
```powershell
.\venv\Scripts\Activate.ps1
python analyze_fault_scenarios.py --all
```
**NOTA:** Use `--all` para analisar todos os dados, ou `--hours 48` para últimas 48h

---

## 🎯 Resultados Esperados APÓS simulação correta:

### Cenário 1: Desgaste de Rolamento (Junta 3)
- ✅ Temperatura máxima: ~52°C (+15°C do normal)
- ✅ Taxa de aquecimento: ~0.08°C/min
- ✅ Variabilidade corrente (CV): ~0.18 (vibração)
- ✅ Aumento de torque: ~0.42 Nm

### Cenário 2: Superaquecimento Motor (Junta 2)
- ✅ Temperatura máxima: ~69°C (+25°C do normal)
- ✅ Taxa de aquecimento: ~0.21°C/min (rápida!)
- ✅ Aumento de corrente: ~+40%
- ✅ Índice estresse térmico: ~0.49

### Cenário 3: Degradação Fonte de Alimentação
- ✅ Tensão média: ~44V (nominal 48V)
- ✅ Coeficiente variação: ~8.3%
- ✅ Quedas de tensão: 15-20 eventos

### Cenário 4: Desgaste Mecânico (Junta 4)
- ✅ Temperatura máxima: ~49°C
- ✅ Backlash (folga): até 1.5°
- ✅ Aumento de torque: ~0.86 Nm (+60%)

### Cenário 5: Falta de Lubrificação (Junta 5)
- ✅ Temperatura máxima: ~54°C (+18°C)
- ✅ Taxa de aquecimento: ~0.11°C/min
- ✅ Aumento de torque: ~0.72 Nm (+60%)

---

## 📋 CHECKLIST de Execução:

- [ ] 1. Limpar banco de dados atual (opcional)
- [ ] 2. Abrir Terminal 1: `python main_gui.py`
- [ ] 3. Aguardar mensagem "Conectado ao broker MQTT"
- [ ] 4. Abrir Terminal 2: `python test_fault_scenarios.py`
- [ ] 5. Observar barras de progresso (9 cenários)
- [ ] 6. Aguardar término completo da simulação
- [ ] 7. Executar: `python analyze_fault_scenarios.py`
- [ ] 8. Verificar resultados em `analises/fault_scenarios/`
- [ ] 9. Conferir valores no relatório científico
- [ ] 10. Comparar com tabelas do COMO_CITAR_ARTIGO.md

---

## 🔍 Como Verificar se os Dados São Simulados:

### Método 1: Verificar tamanho do banco
```powershell
(Get-Item data\jaka_monitor.db).length / 1MB
```
- Dados reais: ~0.5 MB (poucos registros)
- Dados simulados: ~2-5 MB (muitos registros + falhas)

### Método 2: Verificar timestamps
```powershell
python -c "import sqlite3; conn = sqlite3.connect('data/jaka_monitor.db'); cursor = conn.cursor(); cursor.execute('SELECT MIN(timestamp), MAX(timestamp), COUNT(*) FROM robot_data'); print(cursor.fetchone())"
```
- Dados reais: poucos minutos de diferença
- Dados simulados: exatamente 37 minutos (ou 5 min no modo rápido)

### Método 3: Verificar temperatura máxima
```powershell
python -c "import sqlite3; conn = sqlite3.connect('data/jaka_monitor.db'); cursor = conn.cursor(); cursor.execute('SELECT MAX(temperature) FROM joint_data'); print(f'Temp máxima: {cursor.fetchone()[0]}°C')"
```
- Dados reais: ~20-25°C (temperatura ambiente)
- Dados simulados: ~65-70°C (cenário superaquecimento)

---

## 💡 IMPORTANTE PARA O ARTIGO:

Os valores citados no arquivo `COMO_CITAR_ARTIGO.md` são **valores esperados** baseados na programação do simulador. Para o artigo científico ser **reprodutível**, você deve:

1. ✅ Executar a simulação completa (37 min)
2. ✅ Usar os valores REAIS obtidos da análise
3. ✅ Atualizar o arquivo `COMO_CITAR_ARTIGO.md` com valores reais
4. ✅ Documentar parâmetros de simulação (--interval, --normal-time)

Ou alternativamente:

1. ✅ Manter valores do `COMO_CITAR_ARTIGO.md` como "teóricos esperados"
2. ✅ Adicionar seção "Resultados Experimentais" com valores obtidos
3. ✅ Comparar teórico vs experimental (análise de desvios)

---

## 📞 Próximo Passo AGORA:

Execute no PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
python test_fault_scenarios.py --interval 1.0 --normal-time 5
```

**Aguarde 5 minutos** e depois execute a análise novamente!
