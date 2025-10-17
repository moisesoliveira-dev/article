# Guia de Simulação de Falhas para Artigo Científico

## 📋 Visão Geral

Este guia explica como usar os scripts de simulação de falhas para gerar dados realistas e relatórios científicos sobre diferentes tipos de degradação em robôs industriais.

## 🎯 Scripts Disponíveis

### 1. `test_fault_scenarios.py` - Simulador de Falhas
Gera dados simulados de 9 tipos diferentes de falhas.

### 2. `analyze_fault_scenarios.py` - Analisador Científico
Analisa os dados gerados e cria relatórios formatados para artigos.

---

## 🔬 Cenários de Falha Implementados

### 1. Desgaste de Rolamento (Bearing Wear)

**Grandezas Alteradas:**
- ✅ **Temperatura**: Aumenta gradualmente (+15°C ao longo do tempo)
- ✅ **Corrente**: Variação aumentada (vibração/ruído)
- ✅ **Torque**: Leve aumento por atrito
- ✅ **Posição**: Pequenos desvios (folga)

**Causa Física:**
- Desgaste do material do rolamento
- Perda de esfericidade das esferas
- Aumento de folgas internas

**Duração:** 180-300 segundos

---

### 2. Superaquecimento do Motor

**Grandezas Alteradas:**
- ✅ **Temperatura**: Aumento rápido e exponencial (+25°C)
- ✅ **Corrente**: Aumenta significativamente (motor forçado)
- ✅ **Torque**: Variações irregulares
- ✅ **Temp. Ambiente**: Também aumenta

**Causa Física:**
- Obstrução de ventilação
- Sobrecarga contínua
- Falha no sistema de resfriamento

**Duração:** 150-240 segundos

---

### 3. Degradação da Fonte de Alimentação

**Grandezas Alteradas:**
- ✅ **Tensão**: Instável (quedas e picos até -4V)
- ✅ **Corrente**: Ripple aumentado
- ✅ **Temperatura**: Leve aumento
- ⚠️ **Afeta todas as juntas**

**Causa Física:**
- Capacitores degradados (ESR aumentado)
- Reguladores com deriva térmica
- Conexões oxidadas

**Duração:** 200-360 segundos

---

### 4. Desgaste Mecânico da Transmissão

**Grandezas Alteradas:**
- ✅ **Posição**: Folgas (backlash até 1.5°)
- ✅ **Torque**: Picos e vales irregulares
- ✅ **Corrente**: Levemente aumentada
- ✅ **Temperatura**: Aumento por atrito (+5°C)

**Causa Física:**
- Desgaste de engrenagens
- Folgas no redutor
- Desgaste de dentes

**Duração:** 220-400 segundos

---

### 5. Problema em Conexão de Cabo

**Grandezas Alteradas:**
- ✅ **Corrente**: Picos momentâneos (×1.5 a ×3.0)
- ✅ **Temperatura**: Leituras incorretas intermitentes
- ✅ **Tensão**: Valores anormais esporádicos
- ⚡ **Intermitente** (10-30% das leituras)

**Causa Física:**
- Cabo desgastado
- Conector com mau contato
- Oxidação nos terminais

**Duração:** 120-180 segundos

---

### 6. Deficiência de Lubrificação

**Grandezas Alteradas:**
- ✅ **Temperatura**: Aumento progressivo não-linear (+18°C)
- ✅ **Torque**: Aumento significativo (atrito)
- ✅ **Corrente**: Aumenta (compensação)
- ✅ **Vibração**: Ruído na corrente

**Causa Física:**
- Falta de lubrificante
- Degradação do lubrificante
- Perda de propriedades do óleo

**Duração:** 250-450 segundos

---

### 7. Deriva do Encoder

**Grandezas Alteradas:**
- ✅ **Posição**: Erro crescente acumulado
- ✅ **Corrente**: Aumenta (correção constante)
- ✅ **Temperatura**: Leve aumento
- 📐 **Diferença** entre posição comandada e real

**Causa Física:**
- Encoder desalinhado
- Encoder danificado
- Perda de calibração

**Duração:** 180-300 segundos

---

### 8. Sobrecarga Contínua

**Grandezas Alteradas:**
- ✅ **Corrente**: Muito elevada em várias juntas
- ✅ **Temperatura**: Alta em múltiplas juntas (+22°C)
- ✅ **Torque**: No limite ou acima
- ⚠️ **Afeta juntas 1, 2 e 3** (base)

**Causa Física:**
- Carga acima da especificação
- Operação fora dos limites nominais

**Duração:** 140-200 segundos

---

### 9. Ressonância Mecânica

**Grandezas Alteradas:**
- ✅ **Corrente**: Oscilação senoidal crescente
- ✅ **Torque**: Oscilação senoidal crescente
- ✅ **Temperatura**: Oscila e aumenta
- 🌊 **Padrão periódico** (2-5 Hz)

**Causa Física:**
- Frequência de operação = frequência natural
- Modos de vibração excitados
- Amortecimento insuficiente

**Duração:** 160-250 segundos

---

## 🚀 Como Usar

### Passo 1: Executar Simulação

```bash
# Executar TODOS os cenários
python test_fault_scenarios.py

# Executar com intervalo personalizado (mais rápido)
python test_fault_scenarios.py --interval 1.0

# Executar cenários específicos
python test_fault_scenarios.py --scenarios bearing,motor

# Reduzir tempo de operação normal entre cenários
python test_fault_scenarios.py --normal-time 10
```

**Opções disponíveis:**
- `--interval`: Tempo entre publicações MQTT (segundos)
- `--normal-time`: Tempo de operação normal entre cenários (segundos)
- `--scenarios`: Cenários a executar (all, bearing, motor, power, mechanical, cable, lubrication, encoder, overload, vibration)

**Exemplo para artigo (recomendado):**
```bash
python test_fault_scenarios.py --interval 2.0 --normal-time 30
```

**Tempo total estimado:**
- 9 cenários × (duração média 220s + 30s normal) = ~37 minutos

---

### Passo 2: Deixar o Monitor Rodando

Em outro terminal/janela, mantenha o sistema de monitoramento ativo:

```bash
python main_gui.py
```

Ou, se preferir sem interface:

```bash
python -c "from modules.mqtt_client import MQTTClient; import time; client = MQTTClient(); client.connect(); time.sleep(3600)"
```

---

### Passo 3: Analisar Resultados

Após a simulação completar:

```bash
# Análise completa (últimas 24 horas)
python analyze_fault_scenarios.py

# Análise de janela específica
python analyze_fault_scenarios.py --hours 2

# Banco de dados customizado
python analyze_fault_scenarios.py --db caminho/para/banco.db
```

---

## 📊 Resultados Gerados

A análise cria a pasta `analises/fault_scenarios/` com:

### 1. Gráficos (PNG - 300 DPI)

**Análise de Temperatura:**
- `temp_analysis_Desgaste_Rolamento.png`
- `temp_analysis_Superaquecimento_Motor.png`
- `temp_analysis_Visao_Geral.png`

**Análise Elétrica:**
- `electrical_analysis_J2_Superaquecimento_Motor.png`
- `electrical_analysis_J3_Desgaste_Rolamento.png`

**Correlações:**
- `correlation_Fonte_Alimentacao.png`

### 2. Relatório Científico

**Arquivo:** `relatorio_cientifico.txt`

**Conteúdo:**
- ✅ Descrição de cada cenário
- ✅ Causa física detalhada
- ✅ Métricas observadas com valores numéricos
- ✅ Indicadores de falha detectados
- ✅ Interpretação científica
- ✅ Conclusões e recomendações

**Exemplo de seção:**
```
CENÁRIO 1: Desgaste de Rolamento - Junta 3
─────────────────────────────────────────────

📋 DESCRIÇÃO:
   Desgaste progressivo do rolamento causando aumento de temperatura,
   vibração e consumo de corrente devido ao atrito excessivo.

🔬 CAUSA FÍSICA:
   - Fadiga do material do rolamento
   - Perda de esfericidade das esferas/roletes
   - Aumento de folgas internas
   - Perda de lubrificação

📊 MÉTRICAS OBSERVADAS:
   • Temperatura máxima: 52.34°C
   • Taxa de aquecimento: 0.0847°C/min
   • Variabilidade de corrente (CV): 0.1823
   • Aumento de torque: 0.421 Nm
   • Frequência dominante: 2.347 Hz

⚠️  INDICADORES DE FALHA:
   🟡 Aumento moderado de temperatura
   🔴 Alta variabilidade de corrente (vibração)
   🟡 Aumento de torque por atrito

💡 INTERPRETAÇÃO CIENTÍFICA:
   O desgaste do rolamento manifesta-se através de três fenômenos principais:
   1. Aumento térmico: O atrito metal-metal gera calor dissipado
   2. Vibração mecânica: Irregularidades na superfície causam oscilações
   3. Sobrecarga elétrica: Motor compensa perdas mecânicas
```

### 3. Estatísticas (CSV)

**Arquivo:** `estatisticas_cenarios.csv`

**Colunas:**
- Cenário
- Junta
- Temp_Max_C
- Taxa_Aquecimento_C_min
- Var_Corrente_CV
- Aumento_Torque_Nm
- Freq_Vibracao_Hz
- Elevacao_Temp_C
- Tempo_Critico_s
- Aumento_Corrente_pct
- Indice_Estresse_Termico

**Uso:** Copiar/colar direto para tabelas do artigo!

---

## 📖 Usando no Artigo Científico

### Seção "Materiais e Métodos"

```latex
Para validar o sistema de monitoramento preditivo, foram simulados
9 cenários distintos de falhas comuns em robôs industriais. Cada cenário
reproduz alterações nas grandezas físicas (corrente, tensão, temperatura,
torque e posição) conforme documentado na literatura [REF].

Os cenários incluem:
1. Desgaste de rolamento com aumento de vibração e temperatura
2. Superaquecimento do motor por obstrução de ventilação
3. Degradação da fonte de alimentação
... (listar todos)

A simulação foi executada em ambiente controlado, publicando dados via
protocolo MQTT a cada 2 segundos, com períodos de operação normal de 30s
entre cada cenário de falha.
```

### Seção "Resultados"

**Tabela 1: Métricas de Detecção de Falhas**

Copie os dados de `estatisticas_cenarios.csv`:

| Cenário | Junta | Temp Max (°C) | Taxa Aquec. (°C/min) | Var. Corrente |
|---------|-------|---------------|----------------------|---------------|
| Desg. Rolamento | 3 | 52.34 | 0.0847 | 0.182 |
| Superaq. Motor | 2 | 68.91 | 0.2134 | 0.156 |
| ... | ... | ... | ... | ... |

**Figura 1: Evolução Temporal da Temperatura**

Inserir: `temp_analysis_Visao_Geral.png`

**Figura 2: Análise Elétrica - Desgaste de Rolamento**

Inserir: `electrical_analysis_J3_Desgaste_Rolamento.png`

### Seção "Discussão"

Use as interpretações científicas do `relatorio_cientifico.txt`:

```
A análise do cenário de desgaste de rolamento demonstrou que a 
variabilidade da corrente (CV = 0.182) é um indicador precoce eficaz,
precedendo o aumento de temperatura em média 47 segundos. Este resultado
corrobora com [REF] que identificou a vibração mecânica como primeiro
sintoma de degradação do rolamento.

O padrão de aquecimento não-linear observado no superaquecimento do motor
(índice de estresse térmico = 0.4873) sugere um processo de thermal runaway,
consistente com o modelo teórico de [REF]...
```

---

## 🔍 Análise Avançada

### Extrair Dados para Análise Customizada

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/jaka_monitor.db')

# Dados de um cenário específico
query = """
SELECT r.timestamp, j.joint_number, j.temperature, j.current, j.torque
FROM robot_data r
JOIN joint_data j ON r.id = j.robot_data_id
WHERE r.timestamp BETWEEN '2025-10-17 10:00:00' AND '2025-10-17 10:30:00'
  AND j.joint_number = 3
ORDER BY r.timestamp
"""

df = pd.read_sql_query(query, conn)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sua análise aqui
import matplotlib.pyplot as plt
plt.plot(df['timestamp'], df['temperature'])
plt.show()
```

### Calcular Métricas Adicionais

```python
from analyze_fault_scenarios import FaultScenarioAnalyzer

analyzer = FaultScenarioAnalyzer()
analyzer.connect()

# Obter dados
df = analyzer.get_time_series_data(
    start_time='2025-10-17 10:00:00',
    end_time='2025-10-17 11:00:00'
)

# Análise customizada
joint_3 = df[df['joint_number'] == 3]

# FFT para análise de frequência
import numpy as np
fft = np.fft.fft(joint_3['current'].values)
freq = np.fft.fftfreq(len(joint_3), d=2.0)  # 2s de intervalo

# Encontrar pico
peak_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
peak_freq = abs(freq[peak_idx])
print(f"Frequência dominante: {peak_freq:.3f} Hz")
```

---

## ⚙️ Customização dos Cenários

### Modificar Duração

Edite `test_fault_scenarios.py`:

```python
# Linha ~680
simulator.add_scenario(BearingWearScenario(
    joint_number=3, 
    duration=300  # ← Altere aqui (segundos)
))
```

### Modificar Intensidade

Edite a classe do cenário desejado:

```python
# Exemplo: BearingWearScenario - Linha ~65
# Aumentar temperatura máxima de 15°C para 20°C
self.base_temp_increase = progress * 20.0  # ← Era 15.0
```

### Adicionar Novo Cenário

```python
class MinhaFalhaScenario(FaultScenario):
    def __init__(self, joint_number: int, duration: int = 240):
        super().__init__(
            name=f"Minha Falha - Junta {joint_number}",
            description="Descrição da falha",
            duration=duration
        )
        self.joint = joint_number
    
    def apply(self, base_data: dict) -> dict:
        super().apply(base_data)
        progress = self.get_progress()
        
        # Modificar grandezas aqui
        monitor_data = base_data.get("monitor_data", [])
        if len(monitor_data) > 5:
            joint_data = monitor_data[5][self.joint - 1]
            
            # Exemplo: aumentar corrente
            joint_data[0] *= (1 + progress * 0.5)
        
        return base_data
```

---

## 📚 Referências Técnicas

### Faixas Normais de Operação

| Grandeza | Valor Normal | Alerta | Crítico |
|----------|--------------|--------|---------|
| Temperatura (°C) | 25-40 | 45-60 | >65 |
| Corrente (A) | 0.8-1.5 | 2.0-2.5 | >3.0 |
| Tensão (V) | 47-49 | 46-47 | <46 |
| Torque (Nm) | 1.0-2.5 | 3.0-4.0 | >4.5 |

### Taxas de Degradação Típicas

- **Rolamento**: 0.05-0.15°C/min
- **Motor**: 0.20-0.40°C/min (superaquecimento)
- **Lubrificação**: 0.03-0.08°C/min (progressivo)

### Correlações Esperadas

- **Temperatura ↔ Corrente**: 0.65-0.85 (alta)
- **Torque ↔ Corrente**: 0.70-0.90 (muito alta)
- **Temperatura ↔ Tensão**: -0.15-0.15 (baixa)

---

## 🎓 Citação Recomendada

```bibtex
@software{jaka_fault_simulator,
  title={Sistema de Simulação e Análise de Falhas para Robôs Industriais},
  author={Sistema JAKA Monitor},
  year={2025},
  note={Implementa 9 cenários de falha com análise automatizada}
}
```

---

## ✅ Checklist para Artigo

- [ ] Executar simulação completa (`test_fault_scenarios.py`)
- [ ] Gerar análise (`analyze_fault_scenarios.py`)
- [ ] Copiar estatísticas de `estatisticas_cenarios.csv` para tabelas
- [ ] Inserir gráficos PNG (300 DPI) nas figuras
- [ ] Usar interpretações do `relatorio_cientifico.txt`
- [ ] Adicionar referências teóricas
- [ ] Descrever metodologia na seção "Materiais e Métodos"
- [ ] Discutir resultados comparando com literatura
- [ ] Validar unidades de medida nas tabelas

---

## 🆘 Solução de Problemas

### Erro: "Not connected to MQTT broker"

Verifique em `config.py`:
```python
MQTT_BROKER = "147.1.5.238"
MQTT_PORT = 1883
MQTT_TOPIC = "jaka/jaka_monitor"
```

### Erro: "Database is locked"

Feche `main_gui.py` antes de executar a análise.

### Gráficos não aparecem

Verifique se há dados no banco:
```bash
sqlite3 data/jaka_monitor.db "SELECT COUNT(*) FROM robot_data"
```

### Tempo de simulação muito longo

Reduza as durações:
```bash
python test_fault_scenarios.py --interval 1.0 --normal-time 10
```

---

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- `TROUBLESHOOTING.md`
- `GUIA_EXTRACAO_DADOS.md`
- `README.md`

---

**Boa sorte com seu artigo científico! 🎓📊**
