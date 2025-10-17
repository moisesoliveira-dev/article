# ⚡ GUIA RÁPIDO - Executar Simulação pela Primeira Vez

## 🎯 Passos Corretos

### 1️⃣ Iniciar o Monitor (Terminal 1)
```bash
python main_gui.py
```
✅ Deixe rodando! Ele vai receber e armazenar os dados.

---

### 2️⃣ Executar Simulação (Terminal 2)
```bash
python test_fault_scenarios.py
```
⏱️ Aguarde ~37 minutos enquanto simula os 9 cenários.

**Você verá:**
```
======================================================================
SIMULADOR DE CENÁRIOS DE FALHAS - ROBÔ JAKA
======================================================================

Total de cenários: 9
Intervalo de publicação: 2.0s

1. Desgaste de Rolamento - Junta 3
   └─ Simulação de desgaste progressivo do rolamento...
   └─ Duração: 180s

...

Iniciando simulação...
```

---

### 3️⃣ Após Completar, Analisar (Terminal 2)
```bash
python analyze_fault_scenarios.py
```
📊 Gera relatórios em `analises/fault_scenarios/`

---

## 🚀 Versão Rápida (Para Testar)

Se quiser testar mais rápido (5 minutos):

```bash
# Terminal 1: Monitor
python main_gui.py

# Terminal 2: Simulação rápida
python test_fault_scenarios.py --interval 1.0 --normal-time 5
```

---

## ⚠️ Problemas Comuns

### "No such column: r.joint_1_pos"
**Causa:** Banco de dados vazio (nenhuma simulação executada ainda)  
**Solução:** Execute os passos 1 e 2 acima

### "Not connected to MQTT broker"
**Causa:** Configuração MQTT incorreta  
**Solução:** Verifique `config.py`:
```python
MQTT_BROKER = "147.1.5.238"
MQTT_PORT = 1883
MQTT_TOPIC = "jaka/jaka_monitor"
```

### "Database is locked"
**Causa:** `main_gui.py` está usando o banco  
**Solução:** Feche o monitor antes de analisar

---

## 📊 Como Saber se Funcionou?

### Durante a Simulação
No `main_gui.py` você verá:
- Dados atualizando na aba "Dashboard"
- Temperatura/corrente mudando
- Eventos sendo detectados

### Verificar Banco de Dados
```bash
python -c "import sqlite3; conn = sqlite3.connect('data/jaka_monitor.db'); print('Registros:', conn.execute('SELECT COUNT(*) FROM robot_data').fetchone()[0])"
```

Se retornar > 0, tem dados! ✅

---

## 🎯 Resumo Visual

```
┌─────────────────────┐
│  Terminal 1         │
│  python main_gui.py │  ← Deixar rodando
│  (Recebe dados)     │
└─────────────────────┘
         ↑
         │ MQTT
         │
┌─────────────────────────────────┐
│  Terminal 2                     │
│  python test_fault_scenarios.py │  ← Executar e aguardar
│  (Simula 37 min)                │
└─────────────────────────────────┘
         ↓
    (Aguardar completar)
         ↓
┌─────────────────────────────────┐
│  Terminal 2 (ou 1)              │
│  python analyze_fault_scen...   │  ← Após completar
│  (Gera relatórios)              │
└─────────────────────────────────┘
```

---

## 💡 Dica

**Enquanto a simulação roda, leia a documentação:**
- `GUIA_SIMULACAO_FALHAS.md`
- `FUNDAMENTOS_FISICOS.md`

---

**Pronto para começar? Execute o passo 1! 🚀**
