# 📐 Fundamentos Físicos das Grandezas Monitoradas

## Relações Físico-Matemáticas entre os Parâmetros

Este documento explica as bases científicas das correlações entre grandezas monitoradas, fundamentando a detecção de falhas.

---

## 1. 🌡️ Temperatura

### Equação Fundamental
```
Q = m × c × ΔT
```
Onde:
- Q = Calor gerado/dissipado (J)
- m = Massa do componente (kg)
- c = Calor específico (J/kg·K)
- ΔT = Variação de temperatura (K)

### Fontes de Calor

#### 1.1 Perdas Elétricas (Efeito Joule)
```
P_elétrica = R × I²
```
- R = Resistência do enrolamento (Ω)
- I = Corrente (A)
- **Conclusão**: Temperatura ∝ I²

#### 1.2 Perdas Mecânicas (Atrito)
```
P_atrito = μ × N × v
```
- μ = Coeficiente de atrito
- N = Força normal (N)
- v = Velocidade relativa (m/s)

**No rolamento:**
```
P_rolamento = K × (C/P)³
```
- K = Constante do rolamento
- C = Capacidade de carga
- P = Carga aplicada
- **Conclusão**: Desgaste ↑ → μ ↑ → Temperatura ↑

---

## 2. ⚡ Corrente Elétrica

### Motor DC/BLDC
```
I = (V - Kb×ω) / R + I_carga
```
Onde:
- V = Tensão aplicada (V)
- Kb = Constante de força contra-eletromotriz (V·s/rad)
- ω = Velocidade angular (rad/s)
- R = Resistência do enrolamento (Ω)
- I_carga = Corrente de carga

### Relação com Torque
```
T = Kt × I
```
- T = Torque (N·m)
- Kt = Constante de torque (N·m/A)
- **Conclusão**: Torque ↑ → Corrente ↑

### Variabilidade (Vibração)
```
I(t) = I_média + ΣAn × sin(2πfn×t + φn)
```
- An = Amplitude da n-ésima harmônica
- fn = Frequência (Hz)
- **Conclusão**: Defeitos mecânicos → oscilações na corrente

---

## 3. 🔌 Tensão

### Lei de Ohm Generalizada
```
V = R×I + L×(dI/dt)
```
- L = Indutância (H)
- dI/dt = Taxa de variação da corrente

### Quedas de Tensão
```
ΔV = I × (R_cabo + R_contato)
```
- R_cabo = Resistência do cabeamento
- R_contato = Resistência de contato
- **Conclusão**: Conexão ruim → quedas de tensão

### Capacitor Degradado
```
V_ripple = I / (2πf×C)
```
- C = Capacitância (F)
- f = Frequência (Hz)
- **Conclusão**: Capacitor degradado (C↓) → ripple↑

---

## 4. 🔩 Torque

### Torque Motor
```
T_motor = Kt × I - B×ω - T_atrito
```
- B = Coeficiente de amortecimento viscoso (N·m·s/rad)
- T_atrito = Torque de atrito seco (N·m)

### Torque de Atrito (Rolamento)
```
T_atrito = μ × dm/2 × F
```
- dm = Diâmetro médio do rolamento (m)
- F = Carga no rolamento (N)
- **Conclusão**: Desgaste → μ↑ → T_atrito↑

### Torque no Redutor
```
T_saída = η × N × T_entrada
```
- η = Eficiência (0-1)
- N = Razão de redução
- **Conclusão**: Desgaste → η↓ → T_entrada↑

---

## 5. 📍 Posição Angular

### Erro de Posicionamento
```
θ_erro = θ_comandada - θ_real
```

### Backlash (Folga)
```
B = θ_max - θ_min (para mesma posição comandada)
```
- **Conclusão**: Desgaste → folgas → B↑

### Deriva do Encoder
```
θ_deriva(t) = θ0 + ε×t
```
- ε = Taxa de deriva (°/s)
- **Conclusão**: Encoder danificado → deriva crescente

---

## 6. 🔀 Potência

### Potência Elétrica
```
P_elétrica = V × I × cos(φ)
```
- φ = Ângulo de fase

### Potência Mecânica
```
P_mecânica = T × ω
```
- ω = Velocidade angular (rad/s)

### Eficiência
```
η = P_mecânica / P_elétrica
```
- **Conclusão**: Degradação → η↓

---

## 📊 Tabela de Correlações Esperadas

| Grandeza 1 | Grandeza 2 | Correlação | Motivo Físico |
|------------|------------|------------|---------------|
| **Temperatura** | **Corrente** | +0.65 a +0.85 | Efeito Joule (P ∝ I²) |
| **Torque** | **Corrente** | +0.70 a +0.90 | T = Kt × I |
| **Temperatura** | **Torque** | +0.40 a +0.60 | Atrito gera calor |
| **Temperatura** | **Tensão** | -0.10 a +0.10 | Pouca relação direta |
| **Corrente** | **Tensão** | -0.30 a -0.50 | V↑ → I↓ (para P constante) |
| **Posição** | **Torque** | -0.20 a +0.20 | Varia com trajetória |

---

## 🔬 Fenômenos Específicos por Tipo de Falha

### 1. Desgaste de Rolamento

**Modelo de Vibração:**
```
a(t) = A × sin(2πf_BPFO×t)
```
Onde:
- f_BPFO = (n/2) × fr × (1 + d/D)
- n = Número de esferas
- fr = Frequência de rotação (Hz)
- d = Diâmetro da esfera (mm)
- D = Diâmetro primitivo (mm)

**Assinatura:**
- Frequência característica na FFT da corrente
- Temperatura crescente não-linear
- Variabilidade de corrente (CV) > 15%

### 2. Superaquecimento do Motor

**Lei de Arrhenius (Degradação do Isolamento):**
```
L = L0 × 2^(-ΔT/10)
```
- L = Vida útil restante
- L0 = Vida útil nominal (horas)
- ΔT = Aumento de temperatura acima do nominal (°C)
- **Conclusão**: +10°C → vida útil reduzida pela metade

**Dissipação de Calor:**
```
dT/dt = (P_gerada - P_dissipada) / (m×c)
```
- P_dissipada = h×A×(T - T_amb)
- h = Coeficiente de convecção (W/m²·K)
- A = Área de superfície (m²)
- **Conclusão**: Obstrução → h↓ → aquecimento↑

### 3. Degradação da Fonte

**Capacitor Eletrolítico:**
```
C(t) = C0 × e^(-t/τ)
ESR(t) = ESR0 × e^(t/τ')
```
- τ = Constante de tempo de degradação da capacitância
- τ' = Constante de tempo do aumento de ESR
- **Conclusão**: Tempo → C↓, ESR↑ → ripple↑

**Ripple de Tensão:**
```
V_ripple = ΔI × ESR + I/(2πf×C)
```
- ΔI = Variação de corrente
- ESR = Resistência série equivalente (Ω)

### 4. Falta de Lubrificação

**Equação de Stribeck:**
```
μ = μ_coulomb + (μ_static - μ_coulomb)×e^(-(v/v_s)^α) + μ_viscous×v
```
- μ_coulomb = Coeficiente de atrito seco
- μ_static = Coeficiente de atrito estático
- v_s = Velocidade de Stribeck
- α = Expoente (tipicamente 0.5-2)

**Sem lubrificação:**
- μ_coulomb ↑↑ (metal-metal)
- μ_viscous → 0
- **Resultado**: Torque ↑ 30-60%, Temperatura ↑ 15-25°C

### 5. Ressonância Mecânica

**Frequência Natural:**
```
fn = (1/2π) × √(k/m_eq)
```
- k = Rigidez do sistema (N/m)
- m_eq = Massa equivalente (kg)

**Amplificação:**
```
X = F0 / √[(k - mω²)² + (cω)²]
```
- F0 = Força de excitação (N)
- c = Coeficiente de amortecimento (N·s/m)
- ω = Frequência de excitação (rad/s)
- **Conclusão**: ω ≈ ωn → amplificação máxima

---

## 📈 Modelos de Degradação

### Modelo Exponencial (Rolamento)
```
P(t) = 1 - e^(-(t/η)^β)
```
- P(t) = Probabilidade de falha
- η = Vida característica (horas)
- β = Parâmetro de forma (Weibull)

### Modelo Linear (Desgaste)
```
W(t) = k × v × F × t
```
- W = Volume desgastado (mm³)
- k = Coeficiente de desgaste
- v = Velocidade (m/s)
- F = Força (N)
- t = Tempo (s)

### Modelo de Paris (Fadiga)
```
da/dN = C × ΔK^m
```
- a = Comprimento da trinca (m)
- N = Número de ciclos
- ΔK = Fator de intensidade de tensão (MPa·√m)
- C, m = Constantes do material

---

## 🎯 Valores de Referência

### Faixas Normais (Robô JAKA)

| Parâmetro | Nominal | Alerta | Crítico |
|-----------|---------|--------|---------|
| Temperatura junta (°C) | 25-40 | 45-60 | >65 |
| Temperatura robô (°C) | 30-45 | 50-65 | >70 |
| Corrente (A) | 0.8-1.5 | 2.0-2.5 | >3.0 |
| Tensão (V) | 47-49 | 46-47 | <46 |
| Torque (Nm) | 1.0-2.5 | 3.0-4.0 | >4.5 |
| Erro posição (°) | <0.05 | 0.1-0.5 | >1.0 |

### Taxas de Variação

| Fenômeno | Taxa Esperada |
|----------|---------------|
| Aquecimento normal | 0.01-0.05°C/min |
| Desgaste rolamento | 0.05-0.15°C/min |
| Superaquecimento | 0.20-0.40°C/min |
| Falta lubrificação | 0.03-0.08°C/min |
| Sobrecarga | 0.15-0.30°C/min |

---

## 📚 Referências Científicas Recomendadas

### Livros
1. **Harris, T. A., & Kotzalas, M. N.** (2006). *Rolling Bearing Analysis* (5th ed.). CRC Press.
   - Capítulos sobre falhas em rolamentos

2. **Boldea, I., & Nasar, S. A.** (2010). *Electric Drives* (3rd ed.). CRC Press.
   - Modelos elétricos e térmicos de motores

3. **Moubray, J.** (1997). *Reliability-Centered Maintenance* (2nd ed.). Industrial Press.
   - Modos de falha e análise

### Papers
1. Lei, Y., et al. (2013). "Condition monitoring and fault diagnosis of planetary gearboxes: A review." *Measurement*, 48, 292-305.

2. Randall, R. B., & Antoni, J. (2011). "Rolling element bearing diagnostics—A tutorial." *Mechanical Systems and Signal Processing*, 25(2), 485-520.

3. Toma, R. N., et al. (2022). "Bearing fault diagnosis using machine learning and artificial intelligence algorithms." *Sensors*, 22(16), 6102.

### Normas Técnicas
- **ISO 10816**: Vibração mecânica - Avaliação de vibração de máquinas
- **ISO 13381**: Monitoramento de condição e diagnóstico de máquinas
- **IEC 60034-1**: Máquinas elétricas rotativas - Características nominais e de desempenho

---

## 💡 Aplicações Práticas

### Para Detecção Precoce

**Índices Compostos:**
```
Health_Index = w1×(T/T_max) + w2×(I/I_max) + w3×(σI/I)
```
Onde:
- w1, w2, w3 = Pesos (soma = 1)
- T_max, I_max = Valores máximos permitidos
- σI = Desvio padrão da corrente

**Limiar Adaptativo:**
```
Limiar(t) = μ(t) + k×σ(t)
```
- μ(t) = Média móvel
- σ(t) = Desvio padrão móvel
- k = Fator (tipicamente 2-3)

### Para Prognóstico

**RUL (Remaining Useful Life):**
```
RUL = (Valor_falha - Valor_atual) / Taxa_degradação
```

**Exemplo (Temperatura):**
```python
T_atual = 52°C
T_falha = 70°C
taxa = 0.08°C/min

RUL = (70 - 52) / 0.08 = 225 minutos ≈ 3.75 horas
```

---

## 🔗 Conexão com os Cenários Simulados

Cada cenário implementado em `test_fault_scenarios.py` baseia-se nestas equações:

1. **BearingWearScenario**: Implementa modelo de atrito + Joule
2. **MotorOverheatingScenario**: Usa lei de dissipação térmica
3. **PowerSupplyDegradationScenario**: Modela ripple de capacitor
4. **MechanicalWearScenario**: Aplica modelo de folga crescente
5. **LubricationDeficiencyScenario**: Equação de Stribeck
6. **VibrationResonanceScenario**: Frequências harmônicas

---

**Use este documento como fundamentação teórica em seu artigo científico!** 📖
