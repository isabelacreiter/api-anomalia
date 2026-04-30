import pandas as pd
import pickle

# 1. Carregar modelo e scaler
with open('modelo_anomalia.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# 2. Carregar dados de carga REAL
# 👉 ajuste o nome se necessário
df = pd.read_csv('resultado1.csv')

# 3. Verificar colunas (debug opcional)
print("Colunas do CSV:", df.columns)

# 4. Selecionar colunas necessárias
df = df[['elapsed', 'success', 'timeStamp']]

# 5. Limpeza
df = df.dropna()
df['success'] = df['success'].astype(int)

# 6. Converter timestamp para número
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['timeStamp'] = df['timeStamp'].astype('int64') // 10**9

# 7. Normalizar (usar o MESMO scaler da Fase 3)
X_scaled = scaler.transform(df)

# 8. Detectar anomalias
# 1 = normal | -1 = anomalia
df['anomalia'] = model.predict(X_scaled)

# 9. Separar dados
anomalias = df[df['anomalia'] == -1]
normais = df[df['anomalia'] == 1]

# 10. Salvar resultados
df.to_csv('resultado_com_anomalias.csv', index=False)
anomalias.to_csv('somente_anomalias.csv', index=False)

# 11. Resumo
print("\nResumo:")
print("Total de registros:", len(df))
print("Registros normais:", len(normais))
print("Anomalias detectadas:", len(anomalias))

# Percentual
percentual = (len(anomalias) / len(df)) * 100
print(f"Percentual de anomalias: {percentual:.2f}%")