from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import pickle
import io
import os
import json
import numpy as np

app = Flask(__name__)

# Enable CORS
CORS(app)

# Converter numpy types para tipos JSON serializáveis
def convert_to_native_types(obj):
    """Converte numpy/pandas types para tipos Python nativos"""
    if isinstance(obj, dict):
        return {k: convert_to_native_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native_types(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    return obj

# Carregar modelo e scaler ao iniciar
try:
    with open('modelo_anomalia.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")
    model = None

try:
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✅ Scaler carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar scaler: {e}")
    scaler = None


# 🏠 GET - Home (Servir dashboard)
@app.route('/', methods=['GET'])
def home():
    try:
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except:
        return jsonify({"error": "Dashboard não encontrado"}), 404


# 🔎 GET - Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "message": "API de detecção de anomalias funcionando!",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    })


# 📊 POST - Inferência com CSV
@app.route('/predict', methods=['POST'])
def predict():
    
    if model is None or scaler is None:
        return jsonify({"error": "Modelo ou scaler não carregados"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    try:
        # Ler CSV recebido
        stream = io.StringIO(file.stream.read().decode("UTF8"))
        df = pd.read_csv(stream)

        # Validar colunas
        required_cols = ['elapsed', 'success', 'timeStamp']
        if not all(col in df.columns for col in required_cols):
            return jsonify({
                "error": f"CSV precisa ter colunas: {required_cols}"
            }), 400

        # Pré-processamento
        df = df[required_cols].copy()
        df = df.dropna()

        df['success'] = df['success'].astype(int)
        
        # Converter timestamp - tenta diferentes formatos
        try:
            df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
        except:
            try:
                df['timeStamp'] = pd.to_datetime(df['timeStamp'])
            except:
                df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')
        
        df['timeStamp'] = df['timeStamp'].astype('int64') // 10**9

        # Normalização
        X_scaled = scaler.transform(df)

        # Predição
        preds = model.predict(X_scaled)

        df['anomalia'] = preds

        # Adicionar scores de anomalia
        df['anomaly_score'] = model.score_samples(X_scaled)

        # Converter saída para JSON (com apenas os primeiros 1000 registros para performance)
        df_saida = df.head(1000).copy()
        df_saida['anomalia'] = df_saida['anomalia'].astype(int)
        df_saida['elapsed'] = df_saida['elapsed'].astype(int)
        df_saida['success'] = df_saida['success'].astype(int)
        df_saida['timeStamp'] = df_saida['timeStamp'].astype(int)
        resultado = df_saida.to_dict(orient='records')
        resultado = convert_to_native_types(resultado)

        # Resumo
        total = len(df)
        anomalias = int((preds == -1).sum())
        anomalia_percentage = (anomalias / total * 100) if total > 0 else 0

        # Estatísticas
        latencia_media = df['elapsed'].mean()
        latencia_max = df['elapsed'].max()
        latencia_min = df['elapsed'].min()
        taxa_sucesso = (df['success'].sum() / total * 100) if total > 0 else 0

        return jsonify({
            "total_registros": int(total),
            "anomalias_detectadas": int(anomalias),
            "percentual_anomalias": float(round(anomalia_percentage, 2)),
            "taxa_sucesso": float(round(taxa_sucesso, 2)),
            "latencia_media_ms": float(round(latencia_media, 2)),
            "latencia_max_ms": float(round(latencia_max, 2)),
            "latencia_min_ms": float(round(latencia_min, 2)),
            "status_alerta": "CRITICO" if anomalia_percentage > 10 else "AVISO" if anomalia_percentage > 5 else "NORMAL",
            "dados": resultado
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📥 GET - Download dados de exemplo
@app.route('/download-sample', methods=['GET'])
def download_sample():
    csv_data = """elapsed,success,timeStamp
1174,1,1776299039968
1188,1,1776299041259
1116,1,1776299042434
1435,1,1776299043644
1227,1,1776299044782
1164,1,1776299046038
1242,1,1776299047252
1199,1,1776299048436
1305,1,1776299049662
1116,1,1776299050857"""
    
    return csv_data, 200, {
        'Content-Disposition': 'attachment; filename="sample_jmeter.csv"',
        'Content-Type': 'text/csv'
    }


# 📈 GET - Estatísticas do modelo
@app.route('/model-stats', methods=['GET'])
def model_stats():
    if model is None:
        return jsonify({"error": "Modelo não carregado"}), 500
    
    return jsonify({
        "model_type": "Isolation Forest",
        "n_estimators": model.n_estimators,
        "contamination": model.contamination,
        "random_state": model.random_state,
        "scaler_type": "StandardScaler"
    }), 200


# Rodar API
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 INICIANDO API DE DETECÇÃO DE ANOMALIAS")
    print("="*60)
    print("📍 Acesse em: http://localhost:5000")
    print("🔎 Health check: http://localhost:5000/health")
    print("📊 Dashboard: http://localhost:5000/")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
