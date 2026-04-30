from flask import Flask, request, jsonify
import pandas as pd
import pickle
import io

app = Flask(__name__)

# Carregar modelo e scaler ao iniciar
with open('modelo_anomalia.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


# 🔎 GET - Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "online",
        "message": "API de detecção de anomalias funcionando!"
    })


# 📊 POST - Inferência com CSV
@app.route('/predict', methods=['POST'])
def predict():

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
        df = df[required_cols]
        df = df.dropna()

        df['success'] = df['success'].astype(int)

        df['timeStamp'] = pd.to_datetime(df['timeStamp'])
        df['timeStamp'] = df['timeStamp'].astype('int64') // 10**9

        # Normalização
        X_scaled = scaler.transform(df)

        # Predição
        preds = model.predict(X_scaled)

        df['anomalia'] = preds

        # Converter saída para JSON
        resultado = df.to_dict(orient='records')

        # Resumo
        total = len(df)
        anomalias = int((preds == -1).sum())

        return jsonify({
            "total_registros": total,
            "anomalias_detectadas": anomalias,
            "dados": resultado
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rodar API
if __name__ == '__main__':
    app.run(debug=True)