import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

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
# Ajuste os nomes se no seu CSV estiver diferente
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

# 6. Salvar modelo e scaler
with open('modelo_anomalia.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("Modelo de anomalia treinado e salvo com sucesso!")