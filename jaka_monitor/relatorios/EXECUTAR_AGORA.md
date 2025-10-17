# 🚀 EXECUTAR SIMULAÇÃO AGORA - PASSO A PASSO

## ⚠️ SITUAÇÃO ATUAL:
- ❌ Você tem apenas dados REAIS do robô (temp ~24°C)
- ❌ NÃO tem dados SIMULADOS de falhas (temp deveria ser 52°C, 69°C, etc.)
- ❌ O arquivo `test_fault_scenarios.py` NUNCA foi executado

## ✅ O QUE FAZER AGORA:

### 📋 OPÇÃO 1: Simulação Rápida (5 minutos) - RECOMENDADO PARA TESTE

#### Passo 1: Limpar banco atual
```powershell
# Fazer backup (opcional)
Copy-Item data\jaka_monitor.db data\jaka_monitor_backup.db

# Limpar banco
Remove-Item data\jaka_monitor.db
```

#### Passo 2: Abrir 2 Terminais PowerShell

**TERMINAL 1** - Coletor de dados:
```powershell
cd C:\temp\ws-python\article\jaka_monitor
.\venv\Scripts\Activate.ps1
python main_gui.py
```
> ⏳ **AGUARDE** aparecer: "✅ Conectado ao broker MQTT"

**TERMINAL 2** - Simulador de falhas:
```powershell
cd C:\temp\ws-python\article\jaka_monitor
.\venv\Scripts\Activate.ps1
python test_fault_scenarios.py --interval 1.0 --normal-time 5
```

#### Passo 3: Observar execução
- Você verá 9 barras de progresso
- Cada cenário leva ~1 minuto
- Total: ~5 minutos

#### Passo 4: Após término, analisar
```powershell
.\venv\Scripts\Activate.ps1
python analyze_fault_scenarios.py --all
```

---

### 📋 OPÇÃO 2: Simulação Completa (37 minutos) - PARA ARTIGO CIENTÍFICO

#### Passo 1: Limpar banco atual
```powershell
# Fazer backup (opcional)
Copy-Item data\jaka_monitor.db data\jaka_monitor_backup.db

# Limpar banco
Remove-Item data\jaka_monitor.db
```

#### Passo 2: Abrir 2 Terminais PowerShell

**TERMINAL 1** - Coletor de dados:
```powershell
cd C:\temp\ws-python\article\jaka_monitor
.\venv\Scripts\Activate.ps1
python main_gui.py
```
> ⏳ **AGUARDE** aparecer: "✅ Conectado ao broker MQTT"

**TERMINAL 2** - Simulador de falhas (SEM parâmetros = simulação completa):
```powershell
cd C:\temp\ws-python\article\jaka_monitor
.\venv\Scripts\Activate.ps1
python test_fault_scenarios.py
```

#### Passo 3: Observar execução
- Você verá 9 barras de progresso
- Cada cenário: normal 30s → falha 150-250s → normal 30s
- Total: ~37 minutos

#### Passo 4: Após término, analisar
```powershell
.\venv\Scripts\Activate.ps1
python analyze_fault_scenarios.py --all
```

---

## 🎯 RESULTADOS ESPERADOS APÓS SIMULAÇÃO:

### ✅ Verificação Rápida:
```powershell
# Verificar temperatura máxima
python -c "import sqlite3; conn = sqlite3.connect('data/jaka_monitor.db'); cursor = conn.cursor(); cursor.execute('SELECT MAX(temperature) FROM joint_data'); print(f'Temp máxima: {cursor.fetchone()[0]:.1f}°C (esperado: ~69°C)')"

# Verificar quantidade de dados
python -c "import sqlite3; conn = sqlite3.connect('data/jaka_monitor.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM robot_data'); print(f'Registros: {cursor.fetchone()[0]} (esperado: >1000 para simulação completa)')"
```

### ✅ Valores Esperados na Análise:

| Cenário | Temp. Máx. | Taxa Aquec. | Var. Corrente |
|---------|-----------|-------------|---------------|
| Desgaste Rolamento | ~52°C | ~0.08°C/min | ~0.18 |
| Superaquecimento | ~69°C | ~0.21°C/min | ~0.16 |
| Fonte Alimentação | ~41°C | ~0.03°C/min | ~0.24 |
| Desgaste Mecânico | ~49°C | ~0.06°C/min | ~0.13 |
| Falta Lubrificação | ~54°C | ~0.11°C/min | ~0.17 |

---

## ❌ ERRO COMUM:

### Problema: "Nenhum dado no período"
**Solução:** Use `--all` para analisar todos os dados:
```powershell
python analyze_fault_scenarios.py --all
```

### Problema: Temperaturas muito baixas (~24°C)
**Causa:** Simulação não foi executada, são dados reais
**Solução:** Execute `test_fault_scenarios.py` conforme passos acima

---

## 📊 VERIFICAÇÃO FINAL:

Após a análise, abra os arquivos:

1. **Relatório Científico:**
   ```powershell
   notepad analises\fault_scenarios\relatorio_cientifico.txt
   ```
   Procure por temperaturas como 52°C, 69°C, etc.

2. **Estatísticas CSV:**
   ```powershell
   notepad analises\fault_scenarios\estatisticas_cenarios.csv
   ```
   Confira se os valores batem com a tabela esperada acima

3. **Gráficos PNG:**
   ```powershell
   explorer analises\fault_scenarios
   ```
   Os gráficos devem mostrar picos de temperatura

---

## 🆘 PRECISA DE AJUDA?

Se após executar tudo ainda aparecer temperaturas ~24°C:

1. Verifique se o MQTT está funcionando:
   - Terminal 1 deve mostrar mensagens chegando
   - Terminal 2 deve mostrar barras de progresso

2. Verifique se está usando o ambiente virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Verifique se há erros no Terminal 2 durante a simulação

---

## ⏱️ EXECUTE AGORA!

**Recomendação:** Comece com **OPÇÃO 1 (5 minutos)** para testar rapidamente.

Se os resultados estiverem corretos (temp ~69°C), então execute **OPÇÃO 2 (37 minutos)** para o artigo final.

**Comando para começar AGORA:**
```powershell
# Limpar banco
Remove-Item data\jaka_monitor.db -ErrorAction SilentlyContinue

# Terminal 1
.\venv\Scripts\Activate.ps1
python main_gui.py
```
