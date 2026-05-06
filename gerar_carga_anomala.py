import pandas as pd
import numpy as np
from datetime import datetime

"""
Script para simular carga ANORMAL (Fase 4)
Gera um CSV com dados de teste que representam degradação de performance
"""

# 1. Carregar dados normais como base
try:
    df_normal = pd.read_csv('resultado1.csv')
except FileNotFoundError:
    print("Erro: Arquivo 'resultado1.csv' não encontrado.")
    exit(1)

print("\n" + "="*60)
print("🚨 GERANDO DADOS DE CARGA ANORMAL (SIMULAÇÃO)")
print("="*60)

# 2. Criar dados anormais
df_anomalo = df_normal.copy()

# Aumentar significativamente o número de registros (simula mais requisições)
df_anomalo = pd.concat([df_anomalo] * 3, ignore_index=True)

# 3. Introduzir anomalias
np.random.seed(42)

# Converter elapsed para float para permitir valores com ponto flutuante
df_anomalo['elapsed'] = df_anomalo['elapsed'].astype(float)

# Anomalia 1: Aumentar latência em 50-150% para 30% dos registros
anomaly_indices_1 = np.random.choice(len(df_anomalo), size=int(len(df_anomalo)*0.30), replace=False)
df_anomalo.loc[anomaly_indices_1, 'elapsed'] = (df_anomalo.loc[anomaly_indices_1, 'elapsed'] * 
                                                  np.random.uniform(1.5, 2.5, len(anomaly_indices_1)))

# Anomalia 2: Reduzir taxa de sucesso para 20% dos registros
anomaly_indices_2 = np.random.choice(len(df_anomalo), size=int(len(df_anomalo)*0.20), replace=False)
df_anomalo.loc[anomaly_indices_2, 'success'] = False

# Anomalia 3: Timeouts e desconexões (10% dos registros)
anomaly_indices_3 = np.random.choice(len(df_anomalo), size=int(len(df_anomalo)*0.10), replace=False)
df_anomalo.loc[anomaly_indices_3, 'elapsed'] = np.random.uniform(5000, 15000, len(anomaly_indices_3))
df_anomalo.loc[anomaly_indices_3, 'success'] = False

# Converter elapsed de volta para int para manter compatibilidade
df_anomalo['elapsed'] = df_anomalo['elapsed'].astype(int)

# Ajustar timestamp (manter sequência)
start_ts = int(df_anomalo['timeStamp'].iloc[0])
df_anomalo['timeStamp'] = start_ts + np.arange(len(df_anomalo))

# 4. Reordenar timestamp
df_anomalo = df_anomalo.sort_values('timeStamp').reset_index(drop=True)

# 5. Salvar apenas as colunas essenciais para o modelo
df_saida = df_anomalo[['elapsed', 'success', 'timeStamp']].copy()
df_saida.to_csv('resultados_carga_anomala.csv', index=False)

# 6. Estatísticas
print(f"\n✓ Registros gerados: {len(df_anomalo)}")
print(f"✓ Taxa de sucesso: {(df_anomalo['success'].sum() / len(df_anomalo) * 100):.2f}%")
print(f"✓ Taxa de falha: {((~df_anomalo['success']).sum() / len(df_anomalo) * 100):.2f}%")
print(f"✓ Latência média: {df_anomalo['elapsed'].mean():.2f}ms")
print(f"✓ Latência máxima: {df_anomalo['elapsed'].max():.2f}ms")

# Comparação com dados normais
print(f"\n📊 COMPARAÇÃO COM DADOS NORMAIS:")
print(f"  Dados normais:")
print(f"    - Taxa de sucesso: {(df_normal['success'].sum() / len(df_normal) * 100):.2f}%")
print(f"    - Latência média: {df_normal['elapsed'].mean():.2f}ms")
print(f"  Dados anormais:")
print(f"    - Taxa de sucesso: {(df_anomalo['success'].sum() / len(df_anomalo) * 100):.2f}% (↓ degradação)")
print(f"    - Latência média: {df_anomalo['elapsed'].mean():.2f}ms (↑ aumento)")

print(f"\n✅ Arquivo 'resultados_carga_anomala.csv' gerado com sucesso!")
print("="*60 + "\n")
