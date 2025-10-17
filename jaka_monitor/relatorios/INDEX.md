# 📚 Índice Geral - Sistema JAKA Monitor

## Documentação Completa do Sistema

---

## 🚀 Início Rápido

### Para Começar Agora:
1. **`QUICKSTART.md`** - Guia de início rápido (5 minutos)
   - Instalação
   - Primeiro uso
   - Teste com simulador

---

## 📖 Documentação Principal

### **Visão Geral:**
- **`README.md`** - Visão geral completa do sistema
- **`SISTEMA_RESUMO.md`** - Resumo executivo
- **`ARCHITECTURE.md`** - Arquitetura do sistema

### **Instalação e Configuração:**
- **`QUICKSTART.md`** - Instalação rápida (Windows)
- **`install.bat`** - Script de instalação automática
- **`requirements.txt`** - Dependências Python
- **`config_example.py`** - Exemplo de configuração
- **`config.py`** - Configuração ativa (editar aqui)

---

## 📊 Extração e Análise de Dados

### **Guias de Análise:**
1. **`COMO_EXTRAIR_RESULTADOS.md`** ⭐ - **COMECE AQUI!**
   - 3 métodos simples
   - Guia visual rápido
   - Exemplos práticos

2. **`GUIA_EXTRACAO_DADOS.md`** - Guia completo detalhado
   - 5 métodos de extração
   - Estrutura do banco de dados
   - Exemplos para artigos científicos
   - Tutorial Pandas/Matplotlib

3. **`QUERIES_SQL_UTEIS.md`** - 25+ queries prontas
   - Queries básicas
   - Análise de juntas
   - Análise de eventos

### **Simulação e Artigos Científicos:**
4. **`RESUMO_EXECUTIVO_SIMULACAO.md`** � - **COMECE AQUI (SIMULAÇÃO)!**
   - Visão executiva completa
   - Métricas e resultados
   - Checklist de entrega
   - 5 minutos de leitura

5. **`QUICK_START_SIMULACAO.md`** ⚡ - Início rápido (3 comandos)
   - Uso simplificado
   - Checklist completo
   - Troubleshooting

6. **`GUIA_SIMULACAO_FALHAS.md`** 🔬 - Guia técnico completo
   - 9 cenários de falhas simuladas
   - Geração de dados realistas
   - Análise científica automatizada
   - Relatórios formatados para publicação
   - Gráficos de alta resolução (300 DPI)

7. **`FUNDAMENTOS_FISICOS.md`** 📐 - Base teórica
   - Equações físicas
   - Correlações esperadas
   - Referências científicas
   - Modelos de degradação

8. **`COMO_CITAR_ARTIGO.md`** 📝 - Templates de citação
   - BibTeX formatado
   - Exemplos de seções do artigo
   - Templates de tabelas/figuras
   - Abstract modelo

9. **`SIMULACAO_FALHAS_RESUMO.md`** 📋 - Resumo visual
   - Tabela de cenários
   - Guia de uso rápido
   - Queries para artigos

### **Scripts de Análise:**
- **`exemplo_analise.py`** ⭐ - Script pronto para executar
  - Gera 4 gráficos automaticamente
  - Exporta estatísticas em CSV
  - Análise de correlações
  - **Execute:** `python exemplo_analise.py`

- **`offline_analysis.py`** - Análise offline avançada
  - Classe `OfflineAnalyzer` reutilizável
  - Métodos para análises customizadas

### **Scripts de Simulação (Artigos Científicos):**
- **`test_fault_scenarios.py`** 🔬 - Simulador de falhas
  - 9 cenários de degradação
  - Dados realistas para pesquisa
  - **Execute:** `python test_fault_scenarios.py`

- **`analyze_fault_scenarios.py`** 📊 - Analisador científico
  - Relatórios formatados para artigos
  - Gráficos 300 DPI
  - Estatísticas em CSV
  - **Execute:** `python analyze_fault_scenarios.py`

---

## 🔧 Otimizações e Melhorias

### **Performance:**
- **`OTIMIZACAO_PERFORMANCE.md`** - Documentação técnica completa
  - Sistema de filas assíncronas
  - Multi-threading avançado
  - UI throttling
  - Comparações de performance

- **`OTIMIZACAO_RESUMO.md`** - Resumo rápido
  - Principais melhorias
  - Resultados obtidos

### **Interface:**
- **`CHANGELOG_ANOMALIAS.md`** - Mudanças no sistema de alertas
  - Remoção de popups
  - Novo painel de anomalias
  - Recursos visuais

---

## 🛠️ Suporte e Troubleshooting

- **`TROUBLESHOOTING.md`** - Solução de problemas comuns
  - Erros de conexão MQTT
  - Problemas de instalação
  - Erros de banco de dados
  - Problemas de interface

---

## 📂 Estrutura do Projeto

```
jaka_monitor/
│
├── 📖 DOCUMENTAÇÃO
│   ├── README.md                       ← Visão geral
│   ├── INDEX.md                        ← Este arquivo (índice)
│   ├── QUICKSTART.md                   ← Início rápido
│   ├── SISTEMA_RESUMO.md               ← Resumo executivo
│   ├── ARCHITECTURE.md                 ← Arquitetura técnica
│   ├── TROUBLESHOOTING.md              ← Problemas comuns
│   │
│   ├── 📊 ANÁLISE DE DADOS
│   ├── COMO_EXTRAIR_RESULTADOS.md      ⭐ COMECE AQUI
│   ├── GUIA_EXTRACAO_DADOS.md          ← Guia completo
│   ├── QUERIES_SQL_UTEIS.md            ← Queries prontas
│   ├── GUIA_SIMULACAO_FALHAS.md        🔬 Simulação de falhas
│   │
│   ├── 🚀 OTIMIZAÇÕES
│   ├── OTIMIZACAO_PERFORMANCE.md       ← Detalhes técnicos
│   ├── OTIMIZACAO_RESUMO.md            ← Resumo rápido
│   └── CHANGELOG_ANOMALIAS.md          ← Mudanças na UI
│
├── 🐍 CÓDIGO PYTHON
│   ├── main_gui.py                     ← Interface principal
│   ├── exemplo_analise.py              ⭐ Script de análise
│   ├── offline_analysis.py             ← Análise offline
│   ├── test_fault_scenarios.py         🔬 Simulador de falhas
│   ├── analyze_fault_scenarios.py      📊 Análise científica
│   ├── test_simulator.py               ← Simulador MQTT
│   ├── test_system.py                  ← Testes do sistema
│   ├── config.py                       ← Configurações
│   └── config_example.py               ← Exemplo de config
│
├── 📦 MÓDULOS
│   └── modules/
│       ├── __init__.py
│       ├── mqtt_client.py              ← Cliente MQTT
│       ├── database.py                 ← Banco de dados
│       ├── analyzer.py                 ← Detecção de anomalias
│       └── report_generator.py         ← Relatórios PDF/Excel
│
├── 💾 DADOS E RESULTADOS
│   ├── data/
│   │   └── jaka_monitor.db             ← Banco de dados SQLite
│   ├── reports/
│   │   ├── relatorio_*.pdf             ← Relatórios PDF
│   │   ├── dados_*.xlsx                ← Exportações Excel
│   │   └── *_graph_*.png               ← Gráficos temporários
│   ├── analises/
│   │   ├── (exemplo_analise.py)        ← Resultados de análises
│   │   └── fault_scenarios/            🔬 Simulações científicas
│   │       ├── relatorio_cientifico.txt
│   │       ├── estatisticas_cenarios.csv
│   │       └── *.png (gráficos 300 DPI)
│   └── logs/
│       └── system_*.log                ← Logs do sistema
│
└── ⚙️ INSTALAÇÃO
    ├── requirements.txt                ← Dependências
    ├── install.bat                     ← Instalador Windows
    └── venv/                           ← Ambiente virtual
```

---

## 🎯 Fluxo de Trabalho Recomendado

### **1. Instalação Inicial** (5 min)
```
QUICKSTART.md → install.bat → config.py
```

### **2. Primeiro Teste** (2 min)
```
python main_gui.py → Testar interface
python test_simulator.py → Dados simulados
```

### **3. Coleta de Dados** (24h+ recomendado)
```
python main_gui.py → Deixar rodando
```

### **4. Análise de Resultados** (10 min)
```
COMO_EXTRAIR_RESULTADOS.md → exemplo_analise.py
```

### **5. Análises Avançadas** (conforme necessário)
```
GUIA_EXTRACAO_DADOS.md → Python/SQL personalizado
```

---

## 📋 Casos de Uso por Documento

### **Quero instalar rapidamente:**
→ `QUICKSTART.md`

### **Quero entender o sistema:**
→ `README.md` + `SISTEMA_RESUMO.md`

### **Quero extrair dados para artigo:**
→ `COMO_EXTRAIR_RESULTADOS.md` ⭐

### **Quero análises personalizadas:**
→ `GUIA_EXTRACAO_DADOS.md` + `QUERIES_SQL_UTEIS.md`

### **Quero scripts prontos:**
→ `exemplo_analise.py`

### **Sistema está travando:**
→ `OTIMIZACAO_PERFORMANCE.md` (já implementado!)

### **Tenho um erro:**
→ `TROUBLESHOOTING.md`

### **Quero entender a arquitetura:**
→ `ARCHITECTURE.md`

---

## 🎓 Para Artigos Científicos

### **Documentos Essenciais:**
1. ⭐ `COMO_EXTRAIR_RESULTADOS.md` - Métodos de extração
2. ⭐ `exemplo_analise.py` - Gerar gráficos/estatísticas
3. `GUIA_EXTRACAO_DADOS.md` - Análises detalhadas
4. `QUERIES_SQL_UTEIS.md` - Consultas SQL prontas

### **Checklist de Coleta:**
- [ ] Leia: `QUICKSTART.md`
- [ ] Configure: `config.py` (thresholds, MQTT)
- [ ] Colete: Mínimo 24h de dados
- [ ] Execute: `python exemplo_analise.py`
- [ ] Gere: Relatório PDF na interface
- [ ] Exporte: Excel para análises adicionais
- [ ] Salve: Backup de `data/jaka_monitor.db`
- [ ] Documente: Período, configurações usadas

---

## 💡 Dicas Importantes

### **Para Iniciantes:**
1. Comece por `QUICKSTART.md`
2. Use a interface gráfica primeiro
3. Teste com `test_simulator.py`
4. Depois explore análises customizadas

### **Para Análise de Dados:**
1. **Mais Fácil:** Interface → Aba Relatórios → PDF/Excel
2. **Rápido:** `python exemplo_analise.py`
3. **Flexível:** `GUIA_EXTRACAO_DADOS.md` + Python/SQL

### **Para Troubleshooting:**
1. Verifique `logs/system_*.log`
2. Consulte `TROUBLESHOOTING.md`
3. Revise `config.py`

---

## 🔄 Atualizações Recentes

### **Versão 1.0.0 (Outubro 2025)**

#### **Performance:**
- ✅ Sistema de filas assíncronas
- ✅ Multi-threading otimizado
- ✅ UI throttling (sem travamentos)
- ✅ Thread separada para banco de dados

#### **Interface:**
- ✅ Painel de anomalias no dashboard
- ✅ Remoção de popups bloqueantes
- ✅ Efeitos visuais para alertas críticos

#### **Documentação:**
- ✅ Guias de extração de dados
- ✅ 25+ queries SQL prontas
- ✅ Script de análise completo
- ✅ Exemplos para artigos científicos

---

## 📞 Suporte

### **Recursos Disponíveis:**
- 📖 Documentação completa (este índice)
- 💻 Scripts de exemplo prontos
- 🔍 Troubleshooting guide
- 📊 Queries SQL úteis

### **Em Caso de Problemas:**
1. Consulte `TROUBLESHOOTING.md`
2. Verifique logs em `logs/`
3. Revise configurações em `config.py`

---

## ✅ Status do Projeto

- **Versão:** 1.0.0
- **Status:** ✅ Produção
- **Última Atualização:** Outubro 2025
- **Python:** 3.8+
- **Plataforma:** Windows (testado)

---

**🎯 Recomendação: Comece por `COMO_EXTRAIR_RESULTADOS.md` para análise de dados!**

Bem-vindo ao Sistema de Monitoramento e Análise para Robôs JAKA!

Este índice organiza toda a documentação disponível para facilitar o uso do sistema.

---

## 🚀 COMEÇANDO

### Para Iniciantes
1. **[QUICKSTART.md](QUICKSTART.md)** - Guia de início rápido (5 minutos)
   - Instalação em 4 passos
   - Primeiro uso
   - Teste sem robô real
   - Checklist de verificação

2. **[install.bat](install.bat)** - Script de instalação automática
   - Duplo clique e pronto!
   - Cria ambiente virtual
   - Instala todas as dependências

### Para Usuários Avançados
3. **[README.md](README.md)** - Documentação completa (300+ linhas)
   - Características detalhadas
   - Instalação manual
   - Configuração avançada
   - Estrutura do projeto
   - Referências técnicas

---

## ⚙️ CONFIGURAÇÃO

4. **[config.py](config.py)** - Arquivo de configuração principal
   - Conexão MQTT (broker, porta, credenciais)
   - Thresholds de detecção de anomalias
   - Níveis de criticidade temporal
   - Parâmetros de análise

5. **[config_example.py](config_example.py)** - Exemplo comentado
   - Todas as opções explicadas
   - Valores sugeridos
   - Notas de uso

---

## 📖 ENTENDENDO O SISTEMA

6. **[SISTEMA_RESUMO.md](SISTEMA_RESUMO.md)** - Visão geral completa
   - ✅ O que foi implementado
   - 📂 Estrutura de arquivos
   - 🎯 Funcionalidades
   - 📊 Dados analisados
   - 🎓 Uso para artigos científicos

7. **[jaka_robot_data.md](../jaka_robot_data.md)** - Especificação dos dados
   - Formato JSON completo
   - Descrição de cada campo
   - Tabelas de referência
   - Exemplos de valores

---

## 🔧 USANDO O SISTEMA

### Aplicação Principal
8. **[main_gui.py](main_gui.py)** - Interface gráfica
   ```powershell
   python main_gui.py
   ```
   - Dashboard em tempo real
   - Monitoramento de 6 juntas
   - Geração de relatórios
   - Exportação de dados

### Ferramentas Auxiliares
9. **[test_simulator.py](test_simulator.py)** - Simulador de dados
   ```powershell
   python test_simulator.py
   ```
   - Testa sistema sem robô real
   - Simula anomalias
   - Útil para desenvolvimento

10. **[offline_analysis.py](offline_analysis.py)** - Análise offline
    ```powershell
    python offline_analysis.py
    ```
    - Analisa dados já coletados
    - Detecta padrões de desgaste
    - Exporta para artigos

11. **[test_system.py](test_system.py)** - Testes automatizados
    ```powershell
    python test_system.py
    ```
    - Verifica todos os módulos
    - Valida instalação
    - Testa funcionalidades

---

## 🆘 SOLUÇÃO DE PROBLEMAS

12. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Guia completo
    - Erros de instalação
    - Problemas de conexão MQTT
    - Erros na interface gráfica
    - Problemas com banco de dados
    - Erros na geração de relatórios
    - Performance e otimização
    - Ferramentas de diagnóstico

---

## 📦 MÓDULOS DO SISTEMA

Localização: `modules/`

13. **[mqtt_client.py](modules/mqtt_client.py)** - Cliente MQTT
    - Conexão com broker
    - Autenticação
    - Callbacks de mensagens

14. **[database.py](modules/database.py)** - Gerenciamento de banco
    - 5 tabelas relacionadas
    - Inserção e consulta
    - Estatísticas

15. **[analyzer.py](modules/analyzer.py)** - Análise de anomalias
    - 7 tipos de detecção
    - Criticidade temporal
    - Health score

16. **[report_generator.py](modules/report_generator.py)** - Relatórios
    - Geração de PDF
    - Exportação Excel
    - Gráficos alta resolução

---

## 📁 ESTRUTURA DE DIRETÓRIOS

```
jaka_monitor/
│
├── 📄 Documentação
│   ├── README.md                   ← Documentação completa
│   ├── QUICKSTART.md              ← Início rápido
│   ├── SISTEMA_RESUMO.md          ← Visão geral
│   ├── TROUBLESHOOTING.md         ← Solução de problemas
│   └── INDEX.md                   ← Este arquivo
│
├── ⚙️ Configuração
│   ├── config.py                  ← Configurações ativas
│   ├── config_example.py          ← Exemplo comentado
│   └── requirements.txt           ← Dependências Python
│
├── 🖥️ Aplicações
│   ├── main_gui.py                ← Interface principal
│   ├── test_simulator.py          ← Simulador de dados
│   ├── offline_analysis.py        ← Análise offline
│   └── test_system.py             ← Testes automatizados
│
├── 📦 Módulos (modules/)
│   ├── __init__.py
│   ├── mqtt_client.py             ← Cliente MQTT
│   ├── database.py                ← Banco de dados
│   ├── analyzer.py                ← Análise de anomalias
│   └── report_generator.py        ← Geração de relatórios
│
├── 💾 Dados (auto-criado)
│   └── data/
│       └── jaka_monitor.db        ← Banco SQLite
│
├── 📊 Relatórios (auto-criado)
│   └── reports/
│       ├── *.pdf                  ← Relatórios PDF
│       ├── *.xlsx                 ← Exportações Excel
│       └── *.png                  ← Gráficos
│
└── 📝 Logs (auto-criado)
    └── logs/
        └── system_*.log           ← Logs do sistema
```

---

## 🎯 FLUXO DE TRABALHO TÍPICO

### 1️⃣ Instalação (5 min)
```powershell
# Opção A: Automática
install.bat

# Opção B: Manual
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2️⃣ Configuração (2 min)
- Editar `config.py` (MQTT, thresholds)
- Verificar documentação: `config_example.py`

### 3️⃣ Teste (2 min)
```powershell
# Validar instalação
python test_system.py

# Testar com simulador
python test_simulator.py  # Terminal 1
python main_gui.py        # Terminal 2
```

### 4️⃣ Uso Real (contínuo)
```powershell
python main_gui.py
# Clicar: "Iniciar Monitoramento"
# Deixar rodando...
```

### 5️⃣ Análise (após coleta)
```powershell
# Gerar relatórios pela interface
# OU análise offline customizada
python offline_analysis.py
```

---

## 📊 DADOS GERADOS

### Banco de Dados
- **Localização**: `data/jaka_monitor.db`
- **Formato**: SQLite
- **Tabelas**: 5 (robot_data, joint_data, tcp_positions, events, statistics)

### Relatórios PDF
- **Localização**: `reports/relatorio_completo_*.pdf`
- **Conteúdo**: Gráficos + estatísticas + eventos
- **Qualidade**: 150 DPI (publicação)

### Exportações Excel
- **Localização**: `reports/dados_exportados_*.xlsx`
- **Abas**: Dados Juntas, Eventos, Estatísticas
- **Formato**: Compatível com análise estatística

### Logs
- **Localização**: `logs/system_*.log`
- **Conteúdo**: Todas as operações do sistema
- **Útil**: Diagnóstico de problemas

---

## 🎓 PARA ARTIGOS CIENTÍFICOS

### Documentos Relevantes
1. **[SISTEMA_RESUMO.md](SISTEMA_RESUMO.md)** - Seção "Uso para Artigos Científicos"
2. **[offline_analysis.py](offline_analysis.py)** - Exportação formatada
3. **[README.md](README.md)** - Seção "Uso para Artigos Científicos"

### Dados Disponíveis
- ✅ Estatísticas descritivas (média, DP, min, max)
- ✅ Séries temporais completas
- ✅ Detecção de anomalias documentada
- ✅ Gráficos de alta resolução
- ✅ Rastreabilidade completa (timestamps)

### Exemplo de Metodologia
Ver `README.md` - Seção "Exemplo de Metodologia para Artigo"

---

## 🔗 LINKS RÁPIDOS

| Preciso... | Consultar... |
|------------|--------------|
| Instalar rapidamente | [QUICKSTART.md](QUICKSTART.md) |
| Entender o sistema | [SISTEMA_RESUMO.md](SISTEMA_RESUMO.md) |
| Configurar MQTT | [config.py](config.py) + [config_example.py](config_example.py) |
| Resolver um erro | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Usar para artigo | [SISTEMA_RESUMO.md](SISTEMA_RESUMO.md) + [offline_analysis.py](offline_analysis.py) |
| Entender os dados | [jaka_robot_data.md](../jaka_robot_data.md) |
| Referência completa | [README.md](README.md) |

---

## 💡 DICAS

### Primeira Vez
1. Leia [QUICKSTART.md](QUICKSTART.md)
2. Execute `install.bat`
3. Teste com simulador
4. Leia [README.md](README.md) para detalhes

### Problema?
1. Consulte [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Verifique logs em `logs/`
3. Execute `python test_system.py`

### Artigo Científico?
1. Colete dados por 24h+
2. Use `offline_analysis.py`
3. Gere relatórios PDF
4. Exporte Excel para análises adicionais

---

## 📞 SUPORTE

### Auto-Ajuda
1. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Primeiro recurso
2. **Logs**: `logs/system_*.log`
3. **Testes**: `python test_system.py`

### Recursos Externos
- [Documentação JAKA](https://www.jaka.com/)
- [MQTT Protocol](https://mqtt.org/)
- [PyQt5 Docs](https://www.riverbankcomputing.com/static/Docs/PyQt5/)

---

## ✅ CHECKLIST DE USO

### Antes de Começar
- [ ] Python 3.8+ instalado
- [ ] Documentação lida ([QUICKSTART.md](QUICKSTART.md))
- [ ] Dependências instaladas
- [ ] Config.py configurado

### Durante o Uso
- [ ] Ambiente virtual ativo
- [ ] Conexão MQTT verificada
- [ ] Logs sendo gerados
- [ ] Dados sendo salvos

### Após Coleta
- [ ] Relatórios gerados
- [ ] Backup do banco de dados
- [ ] Análise offline realizada
- [ ] Dados exportados para artigo

---

**Sistema JAKA Monitor v1.0.0**  
**Documentação Completa e Organizada**  
**Outubro 2025**

---

*Este índice cobre toda a documentação disponível. Para qualquer dúvida, consulte os arquivos referenciados ou [TROUBLESHOOTING.md](TROUBLESHOOTING.md).*
