import pandas as pd
import pickle
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

"""
Script para validação e análise do modelo de anomalias (Fase 5)
Compara dados normais com dados anormais e gera relatório de desempenho
"""

print("\n" + "="*60)
print("🔬 VALIDAÇÃO E ANÁLISE DO MODELO DE ANOMALIAS")
print("="*60)

# 1. Carregar modelo e scaler
try:
    with open('modelo_anomalia.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✓ Modelo e scaler carregados com sucesso")
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")
    exit(1)

# 2. Carregar dados de teste (normais e anormais)
try:
    df_normais = pd.read_csv('resultado1.csv')
    print(f"✓ Dados normais carregados: {len(df_normais)} registros")
except:
    print("❌ Arquivo 'resultado1.csv' não encontrado")
    exit(1)

try:
    df_anormais = pd.read_csv('resultados_carga_anomala.csv')
    print(f"✓ Dados anormais carregados: {len(df_anormais)} registros")
except:
    print("⚠️  Aviso: Arquivo 'resultados_carga_anomala.csv' não encontrado. Execute gerar_carga_anomala.py primeiro")
    df_anormais = None

# 3. Função para processar dados
def processar_dados(df):
    df = df[['elapsed', 'success', 'timeStamp']].copy()
    df = df.dropna()
    df['success'] = df['success'].astype(int)
    try:
        df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
    except:
        df['timeStamp'] = pd.to_datetime(df['timeStamp'])
    df['timeStamp'] = df['timeStamp'].astype('int64') // 10**9
    return df

# 4. Processar e testar dados normais
df_normais = processar_dados(df_normais)
X_normais_scaled = scaler.transform(df_normais)
preds_normais = model.predict(X_normais_scaled)

anomalias_nos_normais = (preds_normais == -1).sum()
percentual_falso_positivo = (anomalias_nos_normais / len(df_normais)) * 100

print(f"\n📊 ANÁLISE DE DADOS NORMAIS:")
print(f"  • Total de registros: {len(df_normais)}")
print(f"  • Anomalias detectadas: {anomalias_nos_normais}")
print(f"  • Taxa de falso positivo: {percentual_falso_positivo:.2f}%")

# 5. Se houver dados anormais
if df_anormais is not None:
    df_anormais = processar_dados(df_anormais)
    X_anormais_scaled = scaler.transform(df_anormais)
    preds_anormais = model.predict(X_anormais_scaled)
    
    anomalias_nos_anormais = (preds_anormais == -1).sum()
    taxa_deteccao = (anomalias_nos_anormais / len(df_anormais)) * 100
    
    print(f"\n🚨 ANÁLISE DE DADOS ANORMAIS:")
    print(f"  • Total de registros: {len(df_anormais)}")
    print(f"  • Anomalias detectadas: {anomalias_nos_anormais}")
    print(f"  • Taxa de detecção: {taxa_deteccao:.2f}%")

# 6. Estatísticas comparativas
print(f"\n📈 ESTATÍSTICAS COMPARATIVAS:")
print(f"  Dados Normais:")
print(f"    - Latência média: {df_normais['elapsed'].mean():.2f}ms")
print(f"    - Taxa de sucesso: {(df_normais['success'].mean()*100):.2f}%")

if df_anormais is not None:
    print(f"  Dados Anormais:")
    print(f"    - Latência média: {df_anormais['elapsed'].mean():.2f}ms (↑ {((df_anormais['elapsed'].mean() / df_normais['elapsed'].mean() - 1) * 100):.2f}%)")
    print(f"    - Taxa de sucesso: {(df_anormais['success'].mean()*100):.2f}% (↓ {((1 - df_anormais['success'].mean() / df_normais['success'].mean()) * 100):.2f}%)")

# 7. Resumo de desempenho
print(f"\n✅ RESUMO DE DESEMPENHO DO MODELO:")
print(f"  • Modelo: Isolation Forest")
print(f"  • Estimadores: {model.n_estimators}")
print(f"  • Taxa de contaminação esperada: {model.contamination*100:.1f}%")
print(f"  • Taxa de falso positivo nos dados normais: {percentual_falso_positivo:.2f}%")
if df_anormais is not None:
    print(f"  • Taxa de detecção nos dados anormais: {taxa_deteccao:.2f}%")
    print(f"  • Desempenho: {'✅ Excelente' if taxa_deteccao > 80 else '🟡 Bom' if taxa_deteccao > 60 else '❌ Fraco'}")

print("="*60 + "\n")
