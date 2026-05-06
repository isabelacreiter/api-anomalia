import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carregar CSV
try:
    df = pd.read_csv('resultado1.csv')
except FileNotFoundError:
    print("Erro: Arquivo 'resultado1.csv' não encontrado. Verifique se o arquivo existe no diretório.")
    exit(1)

# Verificar se as colunas necessárias existem
required_columns = ['elapsed', 'success', 'timeStamp']
if not all(col in df.columns for col in required_columns):
    print(f"Erro: O CSV deve conter as colunas: {required_columns}")
    exit(1)

# 2. Selecionar colunas importantes
df_original = df.copy()
df = df[['elapsed', 'success', 'timeStamp']]

# 3. Limpeza de dados
df = df.dropna()

# Converter success para numérico (True/False → 1/0)
df['success'] = df['success'].astype(int)

# Converter timestamp para número (epoch) - assumindo milliseconds do JMeter
df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
df['timeStamp'] = df['timeStamp'].astype('int64') // 10**9

# 4. Normalização (importante para ML)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# 5. Treinar modelo de anomalia
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,  # 5% esperado de anomalias
    random_state=42
)

model.fit(X_scaled)
predictions = model.predict(X_scaled)

# 6. Análise de Resultados
print("\n" + "="*60)
print("📊 RELATÓRIO DE TREINAMENTO DO MODELO DE ANOMALIAS")
print("="*60)

# Estatísticas básicas
total_samples = len(df)
anomalies = (predictions == -1).sum()
normal = (predictions == 1).sum()
anomaly_percentage = (anomalies / total_samples) * 100

print(f"\n✓ Total de amostras: {total_samples}")
print(f"✓ Amostras normais: {normal} ({(normal/total_samples)*100:.2f}%)")
print(f"✓ Anomalias detectadas: {anomalies} ({anomaly_percentage:.2f}%)")

# Estatísticas dos dados
print(f"\n📈 Estatísticas dos dados de entrada:")
print(f"  • Latência (elapsed) - Min: {df['elapsed'].min()}, Max: {df['elapsed'].max()}, Média: {df['elapsed'].mean():.2f}")
print(f"  • Taxa de sucesso - {(df['success'].mean()*100):.2f}%")

# 7. Salvar modelo e scaler
with open('modelo_anomalia.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print(f"\n✅ Modelo de anomalia treinado e salvo com sucesso!")
print(f"   - modelo_anomalia.pkl")
print(f"   - scaler.pkl")
print("="*60 + "\n")