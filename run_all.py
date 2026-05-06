#!/usr/bin/env python3
"""
Script wrapper para executar todo o pipeline de detecção de anomalias
Executa as 5 fases na sequência correta
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Executa um script Python e exibe status"""
    print("\n" + "="*70)
    print(f"📍 {description}")
    print(f"   Executando: {script_name}")
    print("="*70)
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        print(f"✅ {description} - CONCLUÍDO\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO ao executar {script_name}")
        print(f"   Código de erro: {e.returncode}\n")
        return False
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {script_name}\n")
        return False

def main():
    print("\n" + "="*70)
    print("🚀 PIPELINE COMPLETO DE DETECÇÃO DE ANOMALIAS")
    print("="*70)
    print("\nEste script executará todos os estágios automaticamente:")
    print("  Fase 3: Treinar modelo com dados normais")
    print("  Fase 4: Gerar dados anormais")
    print("  Fase 4+5: Validar modelo")
    print("  Fase 5: Iniciar API (será necessário parar manualmente)")
    print("\n")
    
    input("Pressione ENTER para começar...")
    
    # Verificar arquivo de dados
    if not os.path.exists('resultado1.csv'):
        print("❌ ERRO: Arquivo 'resultado1.csv' não encontrado!")
        print("   Certifique-se de que o arquivo está no diretório atual.")
        sys.exit(1)
    
    # Fase 3: Treinar modelo
    if not run_script('treinar_modelo_anomalia.py', 'FASE 3: Treinar Modelo'):
        print("⚠️  Continuando mesmo com o erro...\n")
    
    # Verificar se modelo foi criado
    if not os.path.exists('modelo_anomalia.pkl'):
        print("❌ ERRO CRÍTICO: Modelo não foi criado!")
        print("   Verifique o arquivo treinar_modelo_anomalia.py")
        sys.exit(1)
    
    # Fase 4a: Gerar dados anormais
    if not run_script('gerar_carga_anomala.py', 'FASE 4A: Gerar Dados Anormais'):
        print("⚠️  Pulando validação do modelo...\n")
    
    # Fase 4b: Validar modelo (apenas se dados anormais foram gerados)
    if os.path.exists('resultados_carga_anomala.csv'):
        run_script('validar_modelo.py', 'FASE 4B: Validar Modelo')
    else:
        print("⚠️  Dados anormais não encontrados, pulando validação\n")
    
    # Fase 5: Iniciar API
    print("\n" + "="*70)
    print("📍 FASE 5: Iniciar API e Dashboard")
    print("="*70)
    print("\nA API será iniciada agora. Acesse:")
    print("  🏠 Dashboard: http://localhost:5000")
    print("  🔎 Health: http://localhost:5000/health")
    print("\nPressione Ctrl+C para parar o servidor")
    print("="*70 + "\n")
    
    input("Pressione ENTER para iniciar o servidor Flask...")
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n✅ Servidor interrompido pelo usuário")
    except FileNotFoundError:
        print("❌ Arquivo app.py não encontrado")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Pipeline interrompido")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
