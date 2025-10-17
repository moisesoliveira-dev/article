# 📊 Queries SQL Úteis - Sistema JAKA Monitor

## Consultas Práticas para Análise de Dados

---

## 🎯 Queries Básicas

### 1. **Ver últimos registros**
```sql
SELECT * FROM robot_data
ORDER BY timestamp DESC
LIMIT 10;
```

### 2. **Contar total de registros**
```sql
SELECT 
    'robot_data' as tabela,
    COUNT(*) as total
FROM robot_data
UNION ALL
SELECT 
    'joint_data',
    COUNT(*)
FROM joint_data
UNION ALL
SELECT 
    'events',
    COUNT(*)
FROM events;
```

### 3. **Período de coleta**
```sql
SELECT 
    MIN(timestamp) as inicio,
    MAX(timestamp) as fim,
    ROUND((JULIANDAY(MAX(timestamp)) - JULIANDAY(MIN(timestamp))) * 24, 2) as horas_coleta
FROM robot_data;
```

---

## 📈 Análise das Juntas

### 4. **Estatísticas de temperatura por junta**
```sql
SELECT 
    joint_number as Junta,
    COUNT(*) as Amostras,
    ROUND(AVG(temperature), 2) as Temp_Media,
    ROUND(MIN(temperature), 2) as Temp_Min,
    ROUND(MAX(temperature), 2) as Temp_Max,
    ROUND(MAX(temperature) - MIN(temperature), 2) as Variacao
FROM joint_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY joint_number
ORDER BY joint_number;
```

### 5. **Juntas com temperatura acima do limite**
```sql
SELECT 
    joint_number,
    timestamp,
    temperature,
    current,
    torque
FROM joint_data
WHERE temperature > 40.0  -- Limite de alerta
    AND timestamp >= datetime('now', '-24 hours')
ORDER BY temperature DESC;
```

### 6. **Média horária de temperatura (Junta 3)**
```sql
SELECT 
    strftime('%Y-%m-%d %H:00', timestamp) as hora,
    ROUND(AVG(temperature), 2) as temp_media,
    ROUND(AVG(current), 3) as corrente_media,
    COUNT(*) as amostras
FROM joint_data
WHERE joint_number = 3
    AND timestamp >= datetime('now', '-24 hours')
GROUP BY hora
ORDER BY hora;
```

### 7. **Comparação entre juntas**
```sql
SELECT 
    j1.timestamp,
    j1.temperature as Junta1_Temp,
    j2.temperature as Junta2_Temp,
    j3.temperature as Junta3_Temp,
    j4.temperature as Junta4_Temp,
    j5.temperature as Junta5_Temp,
    j6.temperature as Junta6_Temp
FROM joint_data j1
LEFT JOIN joint_data j2 ON j1.timestamp = j2.timestamp AND j2.joint_number = 2
LEFT JOIN joint_data j3 ON j1.timestamp = j3.timestamp AND j3.joint_number = 3
LEFT JOIN joint_data j4 ON j1.timestamp = j4.timestamp AND j4.joint_number = 4
LEFT JOIN joint_data j5 ON j1.timestamp = j5.timestamp AND j5.joint_number = 5
LEFT JOIN joint_data j6 ON j1.timestamp = j6.timestamp AND j6.joint_number = 6
WHERE j1.joint_number = 1
    AND j1.timestamp >= datetime('now', '-6 hours')
ORDER BY j1.timestamp;
```

### 8. **Picos de corrente**
```sql
SELECT 
    joint_number,
    timestamp,
    current,
    temperature,
    torque
FROM joint_data
WHERE ABS(current) >= 2.0  -- Limite de alerta
ORDER BY ABS(current) DESC
LIMIT 20;
```

---

## ⚠️ Análise de Eventos/Anomalias

### 9. **Resumo de eventos por severidade**
```sql
SELECT 
    severity,
    COUNT(*) as quantidade,
    ROUND(AVG(duration), 2) as duracao_media_seg,
    MIN(timestamp) as primeiro_evento,
    MAX(timestamp) as ultimo_evento
FROM events
GROUP BY severity
ORDER BY 
    CASE severity
        WHEN 'emergency' THEN 1
        WHEN 'critical' THEN 2
        WHEN 'warning' THEN 3
        ELSE 4
    END;
```

### 10. **Eventos críticos detalhados**
```sql
SELECT 
    timestamp,
    event_type,
    severity,
    joint_number,
    description,
    value,
    threshold,
    ROUND(duration, 2) as duracao_seg
FROM events
WHERE severity IN ('critical', 'emergency')
ORDER BY timestamp DESC;
```

### 11. **Tipos de eventos mais frequentes**
```sql
SELECT 
    event_type,
    COUNT(*) as ocorrencias,
    ROUND(AVG(duration), 2) as duracao_media,
    ROUND(SUM(duration), 2) as duracao_total
FROM events
GROUP BY event_type
ORDER BY ocorrencias DESC;
```

### 12. **Eventos por junta**
```sql
SELECT 
    joint_number,
    COUNT(*) as total_eventos,
    SUM(CASE WHEN severity='warning' THEN 1 ELSE 0 END) as avisos,
    SUM(CASE WHEN severity='critical' THEN 1 ELSE 0 END) as criticos,
    SUM(CASE WHEN severity='emergency' THEN 1 ELSE 0 END) as emergencias
FROM events
WHERE joint_number IS NOT NULL
GROUP BY joint_number
ORDER BY total_eventos DESC;
```

### 13. **Timeline de eventos**
```sql
SELECT 
    DATE(timestamp) as data,
    COUNT(*) as total_eventos,
    SUM(CASE WHEN severity='critical' OR severity='emergency' THEN 1 ELSE 0 END) as eventos_graves
FROM events
GROUP BY DATE(timestamp)
ORDER BY data DESC;
```

---

## 🤖 Análise do Robô

### 14. **Estados do robô ao longo do tempo**
```sql
SELECT 
    task_state,
    COUNT(*) as quantidade,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM robot_data), 2) as percentual,
    CASE task_state
        WHEN 0 THEN 'Desconhecido'
        WHEN 1 THEN 'Iniciando'
        WHEN 2 THEN 'Executando'
        WHEN 3 THEN 'Pausado'
        WHEN 4 THEN 'IDLE'
        WHEN 5 THEN 'Erro'
        ELSE 'Outro'
    END as descricao
FROM robot_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY task_state
ORDER BY quantidade DESC;
```

### 15. **Temperatura do robô vs ambiente**
```sql
SELECT 
    strftime('%Y-%m-%d %H:00', timestamp) as hora,
    ROUND(AVG(robot_temp), 2) as temp_robo,
    ROUND(AVG(ambient_temp), 2) as temp_ambiente,
    ROUND(AVG(robot_temp) - AVG(ambient_temp), 2) as diferenca
FROM robot_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY hora
ORDER BY hora;
```

### 16. **Paradas de emergência**
```sql
SELECT 
    timestamp,
    emergency_stop,
    protective_stop,
    task_state,
    robot_temp
FROM robot_data
WHERE emergency_stop = 1 OR protective_stop = 1
ORDER BY timestamp DESC;
```

---

## 📍 Análise de Posições TCP

### 17. **Estatísticas de movimento TCP**
```sql
SELECT 
    COUNT(*) as total_posicoes,
    ROUND(AVG(x), 2) as x_medio,
    ROUND(AVG(y), 2) as y_medio,
    ROUND(AVG(z), 2) as z_medio,
    ROUND(MAX(x) - MIN(x), 2) as amplitude_x,
    ROUND(MAX(y) - MIN(y), 2) as amplitude_y,
    ROUND(MAX(z) - MIN(z), 2) as amplitude_z
FROM tcp_positions
WHERE timestamp >= datetime('now', '-24 hours');
```

### 18. **Trajetória TCP recente**
```sql
SELECT 
    timestamp,
    ROUND(x, 2) as x,
    ROUND(y, 2) as y,
    ROUND(z, 2) as z,
    ROUND(rx, 2) as rx,
    ROUND(ry, 2) as ry,
    ROUND(rz, 2) as rz
FROM tcp_positions
WHERE timestamp >= datetime('now', '-1 hours')
ORDER BY timestamp;
```

---

## 📊 Análises Avançadas

### 19. **Correlação entre temperatura e corrente (por junta)**
```sql
-- Esta query prepara dados para análise de correlação
SELECT 
    joint_number,
    temperature,
    current,
    torque
FROM joint_data
WHERE timestamp >= datetime('now', '-24 hours')
ORDER BY joint_number, timestamp;
```

### 20. **Detecção de outliers (temperatura)**
```sql
WITH stats AS (
    SELECT 
        joint_number,
        AVG(temperature) as media,
        AVG(temperature) + 2 * (
            AVG(temperature * temperature) - AVG(temperature) * AVG(temperature)
        ) as limite_superior
    FROM joint_data
    GROUP BY joint_number
)
SELECT 
    j.joint_number,
    j.timestamp,
    j.temperature,
    ROUND(s.media, 2) as media_junta,
    ROUND(s.limite_superior, 2) as limite
FROM joint_data j
JOIN stats s ON j.joint_number = s.joint_number
WHERE j.temperature > s.limite_superior
ORDER BY j.temperature DESC;
```

### 21. **Análise de tendência (últimas 3 horas vs 3 horas anteriores)**
```sql
WITH ultimas AS (
    SELECT 
        joint_number,
        AVG(temperature) as temp_recente
    FROM joint_data
    WHERE timestamp >= datetime('now', '-3 hours')
    GROUP BY joint_number
),
anteriores AS (
    SELECT 
        joint_number,
        AVG(temperature) as temp_anterior
    FROM joint_data
    WHERE timestamp >= datetime('now', '-6 hours')
        AND timestamp < datetime('now', '-3 hours')
    GROUP BY joint_number
)
SELECT 
    u.joint_number,
    ROUND(a.temp_anterior, 2) as temp_anterior,
    ROUND(u.temp_recente, 2) as temp_recente,
    ROUND(u.temp_recente - a.temp_anterior, 2) as variacao,
    CASE 
        WHEN u.temp_recente > a.temp_anterior THEN 'AQUECENDO'
        WHEN u.temp_recente < a.temp_anterior THEN 'ESFRIANDO'
        ELSE 'ESTÁVEL'
    END as tendencia
FROM ultimas u
JOIN anteriores a ON u.joint_number = a.joint_number
ORDER BY u.joint_number;
```

### 22. **Duração média entre eventos por junta**
```sql
WITH eventos_ordenados AS (
    SELECT 
        joint_number,
        timestamp,
        LAG(timestamp) OVER (PARTITION BY joint_number ORDER BY timestamp) as timestamp_anterior
    FROM events
    WHERE joint_number IS NOT NULL
)
SELECT 
    joint_number,
    COUNT(*) as total_eventos,
    ROUND(AVG(JULIANDAY(timestamp) - JULIANDAY(timestamp_anterior)) * 24 * 60, 2) as minutos_entre_eventos
FROM eventos_ordenados
WHERE timestamp_anterior IS NOT NULL
GROUP BY joint_number
ORDER BY joint_number;
```

---

## 🔍 Queries para Artigos Científicos

### 23. **Tabela resumo para publicação**
```sql
SELECT 
    joint_number as 'Junta',
    COUNT(*) as 'N',
    ROUND(AVG(temperature), 2) as 'Temp. Média (°C)',
    ROUND(
        SQRT(SUM((temperature - (SELECT AVG(temperature) FROM joint_data j2 WHERE j2.joint_number = j1.joint_number)) * 
                 (temperature - (SELECT AVG(temperature) FROM joint_data j2 WHERE j2.joint_number = j1.joint_number))) / 
             (COUNT(*) - 1)
        ), 2
    ) as 'Desvio Padrão',
    ROUND(MIN(temperature), 2) as 'Temp. Mín (°C)',
    ROUND(MAX(temperature), 2) as 'Temp. Máx (°C)',
    ROUND(AVG(current), 3) as 'Corrente Média (A)',
    ROUND(AVG(torque), 2) as 'Torque Médio'
FROM joint_data j1
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY joint_number
ORDER BY joint_number;
```

### 24. **Dados para gráfico de série temporal**
```sql
SELECT 
    strftime('%Y-%m-%d %H:%M', timestamp) as tempo,
    joint_number,
    ROUND(AVG(temperature), 2) as temperatura
FROM joint_data
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY strftime('%Y-%m-%d %H:%M', timestamp), joint_number
ORDER BY timestamp, joint_number;
```

### 25. **Análise de confiabilidade (tempo sem eventos críticos)**
```sql
WITH periodos AS (
    SELECT 
        timestamp as evento_atual,
        LAG(timestamp) OVER (ORDER BY timestamp) as evento_anterior,
        JULIANDAY(timestamp) - JULIANDAY(LAG(timestamp) OVER (ORDER BY timestamp)) as dias_entre
    FROM events
    WHERE severity IN ('critical', 'emergency')
)
SELECT 
    COUNT(*) as total_periodos,
    ROUND(AVG(dias_entre * 24), 2) as mtbf_horas,
    ROUND(MIN(dias_entre * 24), 2) as min_horas,
    ROUND(MAX(dias_entre * 24), 2) as max_horas
FROM periodos
WHERE dias_entre IS NOT NULL;
```

---

## 💡 Dicas de Uso

### **Executar queries:**

**Opção 1: DB Browser for SQLite**
1. Baixe: https://sqlitebrowser.org/
2. Abra `data/jaka_monitor.db`
3. Vá em "Execute SQL"
4. Cole a query e execute

**Opção 2: Python**
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/jaka_monitor.db')
df = pd.read_sql_query("SUA_QUERY_AQUI", conn)
print(df)
conn.close()
```

**Opção 3: Linha de comando**
```powershell
sqlite3 data/jaka_monitor.db < query.sql
```

### **Modificar período:**
Troque `'-24 hours'` por:
- `'-1 hours'` - última hora
- `'-7 days'` - última semana
- `'2025-10-15'` - data específica

### **Exportar resultados:**
```sql
.mode csv
.output resultado.csv
SELECT * FROM sua_query;
.output stdout
```

---

**📚 Mais informações: Ver `GUIA_EXTRACAO_DADOS.md`**
