# 📚 ÍNDICE DE DOCUMENTAÇÃO - Sistema JAKA Monitor

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
