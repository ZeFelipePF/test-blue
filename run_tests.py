#!/usr/bin/env python3
"""
Script para executar testes da API Coffee Shop
"""
import subprocess
import sys
import os


def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Função principal"""
    print("🧪 Executando testes da API Coffee Shop")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app"):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Instalar dependências se necessário
    print("\n📦 Verificando dependências...")
    try:
        import pytest
        import httpx
    except ImportError:
        print("📦 Instalando dependências...")
        if not run_command("pip install -r requirements.txt", "Instalando dependências"):
            print("❌ Falha ao instalar dependências")
            sys.exit(1)
    
    # Executar testes unitários
    run_command("pytest tests/unit/ -v --tb=short", "Executando testes unitários")
    
    # Executar testes de integração
    run_command("pytest tests/integration/ -v --tb=short", "Executando testes de integração")
    
    # Executar todos os testes
    run_command("pytest tests/ -v --tb=short", "Executando todos os testes")
    
    # Executar testes com cobertura
    run_command("pytest tests/ --cov=app --cov-report=term-missing", "Executando testes com cobertura")
    
    print(f"\n{'='*60}")
    print("✅ Testes concluídos!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
