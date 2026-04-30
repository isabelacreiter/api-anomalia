import os
import shutil

# Nome da pasta do projeto
PASTA = "api_anomalia"

# Criar pasta principal
os.makedirs(PASTA, exist_ok=True)

# Arquivos obrigatórios
arquivos = [
    "app.py",
    "modelo_anomalia.pkl",
    "scaler.pkl"
]

# Mover arquivos para a pasta
for arquivo in arquivos:
    if os.path.exists(arquivo):
        shutil.move(arquivo, os.path.join(PASTA, arquivo))
        print(f"Movido: {arquivo}")
    else:
        print(f"Aviso: {arquivo} não encontrado")

# Criar requirements.txt
requirements = """flask
pandas
scikit-learn
gunicorn
"""

with open(os.path.join(PASTA, "requirements.txt"), "w") as f:
    f.write(requirements)

print("requirements.txt criado")

# Criar Procfile
procfile = "web: gunicorn app:app"

with open(os.path.join(PASTA, "Procfile"), "w") as f:
    f.write(procfile)

print("Procfile criado")

print("\nProjeto organizado com sucesso!")