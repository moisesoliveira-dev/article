# 🔄 Mudanças no Sistema de Alertas de Anomalias

## Data: 16/10/2025

### ✅ O que foi modificado

#### **Antes:**
- Anomalias críticas e de emergência apareciam em **popups modais** (QMessageBox)
- Interrompia o uso do sistema
- Usuário precisava fechar cada alerta manualmente

#### **Agora:**
- Todas as anomalias são exibidas em um **painel dedicado** no Dashboard
- Sistema continua operando sem interrupções
- Visual mais profissional e menos intrusivo

---

## 🎨 Nova Interface do Dashboard

O Dashboard agora está dividido em **duas seções lado a lado**:

### 📊 Esquerda: Log de Eventos (Tempo Real)
- Mostra todos os eventos do sistema
- Mantém histórico cronológico
- Cores indicam severidade

### ⚠️ Direita: Painel de Anomalias Detectadas
- **Fundo amarelo** para destacar alertas ativos
- **Cores e ícones** por severidade:
  - 🔴 **EMERGÊNCIA** (vermelho escuro)
  - 🟠 **CRÍTICO** (laranja avermelhado)
  - 🟡 **ALERTA** (laranja)
  - ℹ️ **INFO** (azul)

- **Efeito visual**: Anomalias críticas fazem o painel piscar em vermelho
- **Botão "Limpar Anomalias"**: Remove alertas já visualizados

---

## 📋 Formato das Anomalias

Cada anomalia exibida mostra:

```
[HH:MM:SS] 🟠 CRÍTICO [Junta 3]
   Temperatura da junta acima do limite crítico
   Valor: 52.3°C | Limite: 50.0°C
```

---

## 🎯 Benefícios

### ✅ Para Monitoramento
- **Não-bloqueante**: Sistema continua operando
- **Visão consolidada**: Todas as anomalias em um só lugar
- **Histórico visual**: Fácil rastrear padrões

### ✅ Para Análise
- **Exportável**: Dados continuam sendo salvos no banco
- **Rastreável**: Timestamp de cada anomalia
- **Contexto completo**: Valor atual vs limite

### ✅ Para Usabilidade
- **Menos cliques**: Sem necessidade de fechar popups
- **Melhor UX**: Interface mais moderna
- **Controle**: Usuário decide quando limpar alertas

---

## 🔧 Detalhes Técnicos

### Arquivos Modificados
- `main_gui.py`:
  - Adicionado painel de anomalias no `create_dashboard_tab()`
  - Removido `QMessageBox` do método `handle_anomaly()`
  - Novos métodos:
    - `show_anomaly_in_panel(anomaly)`: Exibe anomalia no painel
    - `flash_anomaly_panel()`: Efeito visual para alertas críticos
    - `clear_anomalies()`: Limpa painel de anomalias

### Componentes
- **QSplitter**: Divide dashboard em log + anomalias (50/50)
- **QTextEdit estilizado**: Fundo amarelo com borda laranja
- **HTML formatado**: Cores e layout estruturado

---

## 🚀 Como Usar

1. **Iniciar monitoramento** normalmente
2. Anomalias aparecem automaticamente no **painel direito**
3. Observar alertas sem interromper o fluxo de trabalho
4. Clicar em **"Limpar Anomalias"** quando revisar

---

## 📝 Notas

- **Logs continuam inalterados**: Todas as anomalias ainda vão para o log de eventos (esquerda)
- **Banco de dados**: Anomalias continuam sendo salvas para relatórios
- **Popups de relatórios**: Mantidos (sucesso/erro ao gerar PDF/Excel)

---

## 🐛 Bug Corrigido Simultaneamente

- **Erro de Unicode**: Símbolos `✓` e `✗` substituídos por `[OK]` e `[ERRO]`
  - Corrige erro de logging no Windows (codec cp1252)
  - Arquivo: `modules/mqtt_client.py`

---

**Desenvolvido para melhorar a experiência de monitoramento contínuo do robô JAKA!** 🤖
