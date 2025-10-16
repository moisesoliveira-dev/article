# Documentação - Dados de Monitoramento Robô JAKA

Este documento explica o significado dos campos do JSON retornado pela API TCP/IP do robô JAKA.

## Dados do Sistema

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `len` | Integer | Tamanho do pacote de dados em bytes (8979) |
| `drag_status` | Boolean | Status do modo de arrasto manual (false = desabilitado) |
| `errcode` | String | Código de erro hexadecimal ("0x0" = sem erros) |
| `errmsg` | String | Mensagem de erro descritiva (vazio = sem erros) |

## Dados de Monitoramento (`monitor_data`)

Array contendo informações gerais do sistema:

- **Índice [0-1]**: Timestamps/contadores de sistema (12338, 12593)
- **Índice [2]**: Temperatura interna do robô (49.0°C)
- **Índice [3]**: Temperatura ambiente (26.0°C)
- **Índice [4]**: Fator de escala de velocidade (1.072 = 107.2%)

### Dados das Juntas (índice [5])

Array com informações de cada uma das 6 juntas. Cada junta possui um sub-array com:

| Posição | Descrição | Unidade |
|---------|-----------|---------|
| 0 | Corrente da junta | Amperes (A) |
| 1 | Temperatura da junta | Celsius (°C) |
| 2 | Voltagem | Volts (V) |
| 3 | Status de erro | - |
| 4 | Velocidade | rad/s ou °/s |
| 5 | Posição do encoder | Pulsos |
| 6 | Posição absoluta | Pulsos |
| 7 | Carga/Torque | - |
| 8 | Contador auxiliar | - |
| 9-10 | Valores calculados | Posições/velocidades derivadas |

**Exemplo da Junta 1:**
```
[0.0665, 23.0, 50.0, 0.0, 0.1, 6007.2, 2888860.0, 2.6, 110602.0, 0.333, -0.067]
```

## Posicionamento

### Posições das Juntas

| Campo | Tipo | Descrição | Unidade |
|-------|------|-----------|---------|
| `joint_actual_position` | Array[6] | Posição real das juntas | Graus (°) |
| `joint_position` | Array[6] | Posição comandada das juntas | Graus (°) |

**Exemplo:**
```json
[-90.93589, 78.62194, 11.78346, -7.19999, -1.56947, 286.68364]
```

### Posições Cartesianas (TCP)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `actual_position` | Array[6] | Posição real do TCP [X, Y, Z, Rx, Ry, Rz] |
| `position` | Array[6] | Posição comandada do TCP [X, Y, Z, Rx, Ry, Rz] |

- **X, Y, Z**: Coordenadas em milímetros (mm)
- **Rx, Ry, Rz**: Orientação em graus (°)

**Exemplo:**
```json
[2.87773, 577.10489, 229.42427, -91.16764, -9.48043, 179.45318]
```

## Velocidades

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `instVel` | Array[6] | Velocidade instantânea das juntas |
| `curr_tcp_trans_vel` | Float | Velocidade translacional atual do TCP |

## I/O Digital e Analógico

### I/O Padrão do Controlador

| Campo | Tamanho | Descrição |
|-------|---------|-----------|
| `din` | Array[200] | Entradas digitais (0 = LOW, 1 = HIGH) |
| `dout` | Array[200] | Saídas digitais (0 = LOW, 1 = HIGH) |
| `ain` | Array[128] | Entradas analógicas (valores em volts ou mA) |
| `aout` | Array[128] | Saídas analógicas (valores em volts ou mA) |

### I/O da Ferramenta (Tool I/O)

| Campo | Tamanho | Descrição |
|-------|---------|-----------|
| `tio_din` | Array[8] | Entradas digitais da ferramenta |
| `tio_dout` | Array[8] | Saídas digitais da ferramenta |
| `tio_ain` | Array[2] | Entradas analógicas da ferramenta |
| `tio_key` | Array[3] | Sinais de teclas/botões da ferramenta |

**Observação:** No exemplo, `tio_ain` = [466.0, 469.0] indica leituras ativas.

### Relés

| Campo | Tamanho | Descrição |
|-------|---------|-----------|
| `relay_io` | Array[2] | Estado dos relés (0 = aberto, 1 = fechado) |

## Comunicação Industrial

### Modbus Slave

| Campo | Tamanho | Descrição |
|-------|---------|-----------|
| `mb_slave_din` | Array[128] | Entradas digitais via Modbus |
| `mb_slave_dout` | Array[128] | Saídas digitais via Modbus |
| `mb_slave_ain` | Array[64] | Entradas analógicas via Modbus |
| `mb_slave_aout` | Array[64] | Saídas analógicas via Modbus |

### PROFINET Device

| Campo | Tamanho | Descrição |
|-------|---------|-----------|
| `pn_dev_din` | Array[64] | Entradas digitais via PROFINET |
| `pn_dev_dout` | Array[64] | Saídas digitais via PROFINET |
| `pn_dev_ain` | Array[64] | Entradas analógicas via PROFINET |
| `pn_dev_aout` | Array[64] | Saídas analógicas via PROFINET |

### EtherNet/IP Adapter

| Campo | Tamanho | Descrição |
|-------|---------|-----------|
| `eip_adpt_din` | Array[64] | Entradas digitais via EtherNet/IP |
| `eip_adpt_dout` | Array[64] | Saídas digitais via EtherNet/IP |
| `eip_adpt_ain` | Array[48] | Entradas analógicas via EtherNet/IP |
| `eip_adpt_aout` | Array[48] | Saídas analógicas via EtherNet/IP |

## Estados do Sistema

### Estados de Operação

| Campo | Tipo | Descrição | Valores |
|-------|------|-----------|---------|
| `task_state` | Integer | Estado da tarefa | 0-5 (4 = IDLE/READY) |
| `task_mode` | Integer | Modo de operação | 1 = Manual, 2 = Auto |
| `interp_state` | Integer | Estado do interpolador | 0 = Parado |
| `motion_mode` | Integer | Modo de movimento | 1 = Junta, 2 = Linear |
| `enabled` | Boolean | Robô habilitado | true/false |
| `powered_on` | Integer | Sistema energizado | 0 = OFF, 1 = ON |
| `paused` | Boolean | Movimento pausado | true/false |
| `inpos` | Boolean | Em posição alvo | true/false |

### Estados de Segurança

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `emergency_stop` | Integer | Parada de emergência ativada (0 = não, 1 = sim) |
| `protective_stop` | Integer | Parada de proteção ativada (0 = não, 1 = sim) |
| `on_soft_limit` | Integer | Limite de software atingido (0 = não, 1 = sim) |
| `drag_near_limit` | Array[6] | Juntas próximas ao limite no modo arrasto |

### Referenciamento (Homing)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `homed` | Array[9] | Status de referenciamento (1 = referenciado, 0 = não) |

**Exemplo:** `[1,1,1,1,1,1,0,0,0]` - primeiras 6 juntas referenciadas

## Configuração e Controle

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `rapidrate` | Float | Percentual de velocidade rápida (1.0 = 100%) |
| `current_tool_id` | Integer | ID da ferramenta atual (1) |
| `current_user_id` | Integer | ID do sistema de coordenadas do usuário (0) |
| `point_key` | Integer | Chave do ponto atual |
| `motion_line` | Integer | Linha de movimento atual |
| `err_add_line` | Integer | Linha adicional de erro |

## Sensor de Torque (`torqsensor`)

Array contendo configuração e leituras do sensor de força/torque:

```json
[
  [0, ["192.168.2.100", 8080], [0.449, [0.0, 0.0, 20.0]]],
  [0, 0, [Fx, Fy, Fz, Mx, My, Mz], [...], [...]]
]
```

- **Primeiro array**: Configuração (status, IP:porta, calibração)
- **Segundo array**: Leituras de força e momento

## Extensões I/O (`extio`)

Configuração e status de módulos de I/O externos:

### Estrutura

```json
{
  "status": [...],
  "setup": [[1, "AS228P", ["192.168.1.5", 502, 1], [...], "ext_0f5118ef9a5cb05b"]],
  "num": 1,
  "pinmap": [[0, 0, 0, 0]],
  "mode": 0
}
```

- **`setup`**: Configuração dos módulos (tipo, IP, porta Modbus, etc.)
- **`status`**: Estados dos I/Os dos módulos
- **`num`**: Número de módulos conectados
- **`mode`**: Modo de operação

## Funções Digitais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `funcdi` | Array[15][2] | Mapeamento de funções digitais especiais |

**Exemplo:** `[[-1, -1], [-1, -1], ...]` - sem funções mapeadas (-1 = não usado)

## Sinais RS da Ferramenta

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `tio_rs_signals` | Array[8] | Sinais seriais da ferramenta [nome, estado, ...] |

## Estado da Rede

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `netState` | Integer | Estado da conexão de rede (1 = conectado) |

## Informações de Identificação

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ID` | Integer | Identificador do robô (4) |
| `NOME` | String | Nome do robô ("Touchup") |
| `LINHA` | String | Linha de produção ("Linha-1") |

---

## Exemplo de Uso

Este JSON é tipicamente retornado pela porta TCP/IP do robô JAKA e pode ser usado para:

- **Monitoramento em tempo real** do estado do robô
- **Diagnóstico** de problemas e erros
- **Controle supervisório** de células robotizadas
- **Integração** com sistemas SCADA/MES
- **Registro de dados** (data logging)

## Referências

- [Documentação Oficial JAKA - TCP/IP Communication](https://www.jaka.com/docs/en/guide/tcpip.html#communication-port-data-description)
