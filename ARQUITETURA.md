# 🏗️ ARQUITETURA DO SISTEMA

## Fluxo Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE DETECÇÃO                         │
└─────────────────────────────────────────────────────────────────┘

FASE 3: TREINAR MODELO
┌──────────────────────────────────────────────────────────────┐
│ resultado1.csv (50 registros)                                │
│     ↓                                                         │
│ treinar_modelo_anomalia.py                                   │
│   • Carrega CSV                                              │
│   • Pré-processa (elapsed, success, timeStamp)              │
│   • Normaliza com StandardScaler                            │
│   • Treina Isolation Forest (100 est, cont=0.05)           │
│   • Calcula métricas                                        │
│     ↓                                                         │
│ modelo_anomalia.pkl + scaler.pkl                           │
└──────────────────────────────────────────────────────────────┘

FASE 4A: GERAR DADOS ANORMAIS
┌──────────────────────────────────────────────────────────────┐
│ resultado1.csv (linha de base)                              │
│     ↓                                                         │
│ gerar_carga_anomala.py                                       │
│   • Replica 3x o volume (150 registros)                     │
│   • Introduce anomalias:                                     │
│     - Latência +50-150% (30%)                              │
│     - Taxa sucesso reduzida (20%)                          │
│     - Timeouts (10%)                                       │
│   • Mantém sequência de timestamps                          │
│     ↓                                                         │
│ resultados_carga_anomala.csv (150 registros anormais)     │
└──────────────────────────────────────────────────────────────┘

FASE 4B: VALIDAR MODELO
┌──────────────────────────────────────────────────────────────┐
│ validar_modelo.py                                            │
│   • Carrega modelo_anomalia.pkl + scaler.pkl               │
│   • Testa com resultado1.csv → Taxa falso positivo: 6%    │
│   • Testa com resultados_carga_anomala.csv → Det: 43%     │
│   • Exibe métricas comparativas                            │
│     ↓                                                         │
│ Relatório de desempenho                                     │
└──────────────────────────────────────────────────────────────┘

FASE 5: API + DASHBOARD
┌──────────────────────────────────────────────────────────────┐
│                         WEB BROWSER                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           dashboard.html (Frontend)                     │ │
│  │  ┌───────────────────────────────────────────────────┐  │ │
│  │  │ 1. Upload CSV                                     │  │ │
│  │  │ 2. Enviar para /predict (POST)                    │  │ │
│  │  │ 3. Receber JSON com predições                     │  │ │
│  │  │ 4. Renderizar gráficos e alertas                  │  │ │
│  │  └───────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                           ↕                                   │
│  HTTP Requests/Responses                                      │
│                           ↕                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              app.py (Backend Flask)                    │ │
│  │  ┌───────────────────────────────────────────────────┐  │ │
│  │  │ GET / → Serve dashboard.html                      │  │ │
│  │  │ GET /health → Status da API                       │  │ │
│  │  │ POST /predict → Classifica CSV                    │  │ │
│  │  │ GET /model-stats → Info do modelo                │  │ │
│  │  │ GET /download-sample → CSV exemplo                │  │ │
│  │  └───────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              ↕
               Load em memória at startup:
                              ↕
        modelo_anomalia.pkl + scaler.pkl
```

---

## 📊 Fluxo de Dados - POST /predict

```
Cliente (Browser)
    ↓
CSV Upload (FormData)
    ↓
Flask API (app.py)
    ├─ Validar colunas [elapsed, success, timeStamp]
    ├─ Pré-processar dados
    ├─ Converter tipos (int, datetime, float)
    ├─ Normalizar com scaler.pkl
    ├─ Predição com modelo_anomalia.pkl
    ├─ Calcular 6 métricas:
    │   ├─ Total registros
    │   ├─ Anomalias detectadas
    │   ├─ Percentual anomalias
    │   ├─ Taxa de sucesso
    │   ├─ Latência média/max/min
    │   └─ Status de alerta
    └─ Retornar JSON
        ↓
    Browser
    ├─ Renderizar gráfico latência (Chart.js)
    ├─ Renderizar gráfico distribuição (Chart.js)
    ├─ Popular tabela com 50 registros
    ├─ Mostrar alertas visuais
    └─ Atualizar KPIs
```

---

## 🔧 Componentes Técnicos

### 1. Preprocessing (treinar_modelo_anomalia.py)

```python
# Input: DataFrame bruto
df = pd.read_csv('resultado1.csv')

# Step 1: Select colunas
df = df[['elapsed', 'success', 'timeStamp']]

# Step 2: Drop NaN
df = df.dropna()

# Step 3: Type conversion
df['success'] = df['success'].astype(int)
df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
df['timeStamp'] = df['timeStamp'].astype('int64') // 10**9

# Output: Prepared DataFrame
```

### 2. Modelo ML (Isolation Forest)

```python
# Normalização
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# Treinamento
model = IsolationForest(
    n_estimators=100,      # 100 árvores de isolamento
    contamination=0.05,    # Espera 5% de anomalias
    random_state=42        # Reprodutibilidade
)
model.fit(X_scaled)

# Predição
predictions = model.predict(X_scaled)  # Returns: 1 (normal) ou -1 (anomalia)
```

### 3. API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Serve dashboard.html |
| `/health` | GET | Status + modelo/scaler loaded |
| `/predict` | POST | Classifica CSV enviado |
| `/download-sample` | GET | Retorna CSV exemplo |
| `/model-stats` | GET | Info do modelo (estimadores, contamination) |

### 4. Frontend - Gráficos (Chart.js)

```javascript
// Gráfico 1: Latência (Line Chart)
data: latencies.slice(0, 50)
labels: ['#1', '#2', ..., '#50']

// Gráfico 2: Distribuição (Doughnut Chart)
data: [normalCount, anomalyCount]
labels: ['Normal', 'Anomalia']
colors: ['#30cfd0', '#f5576c']
```

---

## 📈 Decisões de Design

### Por que Isolation Forest?
- ✅ Otimizado para detecção de outliers
- ✅ Escalável e rápido
- ✅ Funciona bem com poucos dados
- ✅ Não requer labels (unsupervised)

### Por que StandardScaler?
- ✅ Normaliza features para mesma escala
- ✅ Essencial para modelos de distância
- ✅ Melhora convergência do modelo

### Por que Chart.js?
- ✅ Leve e sem dependências pesadas
- ✅ Gráficos responsivos
- ✅ API simples e intuitiva

### Por que Flask-CORS?
- ✅ Permite requisições cross-origin
- ✅ Compatível com deployment futuro
- ✅ Essencial para qualquer integração

---

## 🔄 Ciclo de Vida do Modelo

```
1. TREINAMENTO (primeira vez)
   treinar_modelo_anomalia.py
   ↓
   modelo_anomalia.pkl + scaler.pkl (salvos em disco)

2. INFERÊNCIA (toda vez que API inicia)
   app.py startup
   ↓
   Carrega modelo_anomalia.pkl + scaler.pkl em memória
   ↓
   Pronto para fazer predições

3. PREDIÇÃO (usuário upload CSV)
   POST /predict
   ↓
   Aplica scaler ao novo CSV
   ↓
   Modelo.predict() retorna 1 ou -1
   ↓
   Calcula métricas e retorna JSON

4. RETREINAMENTO (opcional)
   Delete modelo_anomalia.pkl + scaler.pkl
   ↓
   Rode treinar_modelo_anomalia.py novamente
```

---

## 🚀 Performance

- **Tempo treinamento**: ~100ms (50 registros)
- **Tempo predição**: ~10ms por 50 registros
- **Memória**: ~5MB (modelo + scaler)
- **Suporta**: Até 1000 registros por requisição

---

## 🔐 Segurança

- ✅ Input validation (colunas obrigatórias)
- ✅ Tratamento de exceções
- ✅ CORS habilitado para integração futura
- ⚠️ Sem autenticação (adicione JWT em produção)
- ⚠️ Limite de taxa (adicione rate limiting em produção)

---

## 📋 Checklist de Funcionalidades

- [x] Treinar modelo Isolation Forest
- [x] Salvar/carregar modelo serializado
- [x] Gerar dados anormais simulados
- [x] Validar modelo com métricas
- [x] API REST Flask funcional
- [x] Dashboard HTML/CSS/JavaScript
- [x] Upload de CSV com validação
- [x] Gráficos interativos (Chart.js)
- [x] Sistema de alertas visuais
- [x] Responsivo para mobile
- [x] CORS habilitado
- [x] Documentação completa

---

**Arquitetura finalizada e testada! ✅**
