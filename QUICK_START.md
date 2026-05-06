# 🚀 GUIA DE INÍCIO RÁPIDO

## ⏱️ 1 Minuto para Começar

### Windows
```bash
quick_start.bat
```

### Linux/Mac
```bash
python run_all.py
```

---

## 📋 Passo a Passo (5 minutos)

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Treinar Modelo
```bash
python treinar_modelo_anomalia.py
```

**Resultado esperado:**
```
✅ Modelo de anomalia treinado e salvo com sucesso!
   - modelo_anomalia.pkl
   - scaler.pkl
```

### 3. Gerar Dados Anormais
```bash
python gerar_carga_anomala.py
```

**Resultado esperado:**
```
✅ Arquivo 'resultados_carga_anomala.csv' gerado com sucesso!
```

### 4. Validar Modelo
```bash
python validar_modelo.py
```

**Resultado esperado:**
```
✅ RESUMO DE DESEMPENHO DO MODELO:
  • Taxa de falso positivo: 6.00%
  • Taxa de detecção: 43.33%
```

### 5. Iniciar API
```bash
python app.py
```

**Resultado esperado:**
```
🚀 INICIANDO API DE DETECÇÃO DE ANOMALIAS
📍 Acesse em: http://localhost:5000
```

---

## 🌐 Acessar o Dashboard

Abra no navegador: **http://localhost:5000**

### Funcionalidades:
1. 📤 **Upload CSV** - Envie um arquivo de teste do JMeter
2. 📊 **Métricas** - Veja 6 KPIs em tempo real
3. 📈 **Gráficos** - Visualize latência e distribuição
4. 🚨 **Alertas** - Receba alertas de anomalias
5. 📋 **Tabela** - Detalhes dos 50 primeiros registros

---

## 📥 Testar com CSV de Exemplo

### Opção 1: Download no Dashboard
Clique em **"📥 Download CSV Exemplo"**

### Opção 2: Use Dados Existentes
- `resultado1.csv` - Dados normais (50 registros)
- `resultados_carga_anomala.csv` - Dados anormais (150 registros)

### Opção 3: Criar Novo CSV
Formato esperado:
```csv
elapsed,success,timeStamp
1174,1,1776299039968
1188,1,1776299041259
1116,1,1776299042434
```

---

## ✅ Verificar Status da API

### Health Check
```bash
curl http://localhost:5000/health
```

**Resposta esperada:**
```json
{
  "status": "online",
  "message": "API de detecção de anomalias funcionando!",
  "model_loaded": true,
  "scaler_loaded": true
}
```

### Estatísticas do Modelo
```bash
curl http://localhost:5000/model-stats
```

---

## 🛑 Parar a API

Pressione `Ctrl+C` no terminal

---

## 🐛 Problemas Comuns

### ❌ "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### ❌ "Porta 5000 já em uso"
Edite `app.py` (última linha):
```python
app.run(debug=True, port=5001)  # Mude para 5001
```

### ❌ "Arquivo CSV não encontrado"
Certifique-se que está no diretório correto:
```bash
cd c:\Users\isabela_reiter\Desktop\api-anomalia
```

---

## 📚 Arquivos Importantes

| Arquivo | Propósito |
|---------|-----------|
| `app.py` | API Flask (Fase 5) |
| `dashboard.html` | Interface Web |
| `treinar_modelo_anomalia.py` | Treinar modelo (Fase 3) |
| `gerar_carga_anomala.py` | Gerar dados anormais (Fase 4) |
| `validar_modelo.py` | Validar modelo (Fase 4-5) |
| `modelo_anomalia.pkl` | Modelo treinado |
| `scaler.pkl` | Normalizador |

---

## 🎯 Próximos Passos

### Teste Completo:
1. ✅ Treinar modelo
2. ✅ Gerar dados anormais  
3. ✅ Validar modelo
4. ✅ Iniciar API
5. ✅ Upload CSV no dashboard
6. ✅ Visualizar gráficos e alertas

### Customização:
- Ajuste `contamination` em `treinar_modelo_anomalia.py` para melhor taxa de detecção
- Modifique limites de alerta em `dashboard.html` (linha ~500)
- Altere porta em `app.py` se necessário

---

## 💡 Dicas

- 🔄 Para retreinar o modelo com novos dados, delete `modelo_anomalia.pkl` e `scaler.pkl`
- 📊 Abra DevTools (F12) para ver logs de requisição/resposta
- 🎨 Customize cores do dashboard editando CSS em `dashboard.html`
- 🚀 Para produção, use `gunicorn app:app --bind 0.0.0.0:5000`

---

**Pronto para usar! 🎉**
