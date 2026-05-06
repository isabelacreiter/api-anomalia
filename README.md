# 🚨 Sistema Completo de Detecção de Anomalias em Testes de Carga

## 📋 Visão Geral

Este projeto implementa um **pipeline completo** de detecção de anomalias em dados de teste de carga (JMeter) utilizando Machine Learning.

### Arquitetura do Projeto

```
Fase 3: Treinar Modelo
  ↓
resultado1.csv → treinar_modelo_anomalia.py → modelo_anomalia.pkl + scaler.pkl

Fase 4: Gerar Dados Anormais
  ↓
resultado1.csv → gerar_carga_anomala.py → resultados_carga_anomala.csv

Fase 4: Validar Modelo
  ↓
resultado1.csv + resultados_carga_anomala.csv → validar_modelo.py → Relatório

Fase 5: API + Dashboard
  ↓
CSV (upload) → app.py (API Flask) ↔ dashboard.html (Frontend)
                    ↓
             modelo_anomalia.pkl (predição)
                    ↓
             Análise + Gráficos + Alertas
```

---

## 🚀 Como Executar

### Pré-requisitos

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Etapa 1: Treinar o Modelo (Fase 3)

```bash
python treinar_modelo_anomalia.py
```

**Saída esperada:**
- `modelo_anomalia.pkl` (modelo treinado)
- `scaler.pkl` (normalizador)
- Relatório de treinamento

### Etapa 2: Gerar Dados Anormais (Fase 4)

```bash
python gerar_carga_anomala.py
```

**Saída esperada:**
- `resultados_carga_anomala.csv` (dados com anomalias simuladas)
- Comparação com dados normais

### Etapa 3: Validar o Modelo (Fase 4+5)

```bash
python validar_modelo.py
```

**Saída esperada:**
- Taxa de falso positivo
- Taxa de detecção
- Métricas de desempenho

### Etapa 4: Executar a API + Dashboard (Fase 5)

```bash
python app.py
```

**Acesse:**
- 🏠 Dashboard: http://localhost:5000
- 🔎 Health Check: http://localhost:5000/health
- 📊 API Predict: POST http://localhost:5000/predict

---

## 📊 Funcionalidades do Dashboard

### Upload e Análise
- ✅ Upload de arquivos CSV do JMeter
- 🤖 Processamento automático e classificação
- 📈 Análise em tempo real

### Métricas Exibidas
- **Total de Registros**: quantidade total analisada
- **Registros Normais**: quantidade classificada como normal
- **Anomalias**: quantidade de anomalias detectadas
- **Taxa de Anomalia**: percentual de anomalias
- **Latência Média**: latência média em ms
- **Taxa de Sucesso**: percentual de requisições bem-sucedidas

### Visualizações
- 📉 **Gráfico de Latência**: evolução temporal da latência
- 🍩 **Gráfico de Distribuição**: proporção normal vs anomalia
- 📋 **Tabela de Detalhes**: listagem de 50 primeiros registros

### Sistema de Alertas
- 🟢 **NORMAL**: < 5% de anomalias
- 🟡 **AVISO**: 5-10% de anomalias
- 🔴 **CRÍTICO**: > 10% de anomalias

---

## 📁 Estrutura de Arquivos

```
api-anomalia/
├── app.py                          # API Flask (Fase 5)
├── treinar_modelo_anomalia.py     # Treinar modelo (Fase 3)
├── gerar_carga_anomala.py         # Gerar dados anormais (Fase 4)
├── validar_modelo.py              # Validar modelo (Fase 4-5)
├── detectar_anomalias.py          # Script legacy de detecção
├── organizar_projeto.py           # Organizar estrutura
├── dashboard.html                 # Frontend (Fase 5)
├── modelo_anomalia.pkl            # Modelo treinado
├── scaler.pkl                     # Normalizador
├── requirements.txt               # Dependências Python
├── Procfile                       # Deploy no Heroku
├── resultado1.csv                 # Dados normais (Fase 3)
├── resultados_carga_anomala.csv  # Dados anormais (Fase 4)
├── resultado_com_anomalias.csv   # Resultado com predições
├── somente_anomalias.csv         # Apenas anomalias
└── README.md                      # Este arquivo
```

---

## 🔧 Configuração do Modelo

### Isolation Forest

```python
IsolationForest(
    n_estimators=100,           # 100 árvores
    contamination=0.05,         # Espera 5% de anomalias
    random_state=42             # Para reprodutibilidade
)
```

### Normalização

```python
StandardScaler()  # Normaliza para média=0, desvio=1
```

---

## 📝 Formato do CSV de Entrada

Esperado 3 colunas obrigatórias:

```csv
elapsed,success,timeStamp
1174,1,1776299039968
1188,1,1776299041259
1116,1,1776299042434
```

- **elapsed**: latência em milissegundos
- **success**: 1 (sucesso) ou 0 (falha)
- **timeStamp**: timestamp em milissegundos (época)

---

## 🎯 Critérios de Avaliação

### ✅ Funcionalidade (40%)
- [x] Treinar modelo com dados normais
- [x] Gerar dados anormais simulados
- [x] API funciona e classifica corretamente
- [x] Dashboard exibe alertas visuais

### ✅ Qualidade Técnica (30%)
- [x] Código bem organizado e comentado
- [x] Modelo Isolation Forest justificado
- [x] Normalização correta dos dados
- [x] Tratamento de erros implementado

### ✅ Front End (20%)
- [x] Interface intuitiva e responsiva
- [x] Gráficos interativos (Chart.js)
- [x] Alertas visuais claros
- [x] Upload com feedback visual

### ✅ Apresentação (10%)
- [x] Código documentado
- [x] README completo
- [x] Fácil de executar
- [x] Resultados claros

---

## 🧪 Teste Rápido

```bash
# 1. Treinar modelo
python treinar_modelo_anomalia.py

# 2. Gerar dados anormais
python gerar_carga_anomala.py

# 3. Validar
python validar_modelo.py

# 4. Iniciar API
python app.py

# 5. Abrir no navegador
# http://localhost:5000
```

---

## 🐳 Deploy com Gunicorn (Produção)

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

---

## 📚 Referências

- **Isolation Forest**: https://scikit-learn.org/stable/modules/ensemble.html#isolation-forest
- **Flask**: https://flask.palletsprojects.com/
- **Pandas**: https://pandas.pydata.org/
- **Chart.js**: https://www.chartjs.org/

---

## 📞 Suporte

Para erros ou dúvidas:
1. Verifique se `resultado1.csv` existe
2. Certifique-se de ter instalado as dependências
3. Execute `python treinar_modelo_anomalia.py` antes de rodar a API
4. Verifique a porta 5000 (use porta diferente se necessário em `app.py`)

---

**Desenvolvido com ❤️ para detecção inteligente de anomalias**
