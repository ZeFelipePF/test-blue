#!/usr/bin/env python3
"""
Exemplo de como executar testes específicos
"""
import subprocess
import sys


def run_test_example():
    """Exemplo de execução de testes"""
    
    print("🧪 Exemplos de execução de testes")
    print("=" * 50)
    
    examples = [
        {
            "command": "pytest tests/unit/test_coffee_service.py::TestCoffeeService::test_get_all_coffees_success -v",
            "description": "Executar teste específico de serviço de café"
        },
        {
            "command": "pytest tests/integration/test_order_endpoints.py::TestOrderEndpoints::test_create_order_success -v",
            "description": "Executar teste específico de endpoint de pedido"
        },
        {
            "command": "pytest tests/unit/ -v --tb=short",
            "description": "Executar todos os testes unitários"
        },
        {
            "command": "pytest tests/integration/ -v --tb=short",
            "description": "Executar todos os testes de integração"
        },
        {
            "command": "pytest tests/ -v --cov=app --cov-report=term-missing",
            "description": "Executar todos os testes com cobertura"
        },
        {
            "command": "pytest tests/ -k 'test_create_order' -v",
            "description": "Executar apenas testes que contenham 'test_create_order'"
        },
        {
            "command": "pytest tests/ -k 'coffee' -v",
            "description": "Executar apenas testes relacionados a café"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   Comando: {example['command']}")
    
    print(f"\n{'='*50}")
    print("💡 Para executar os testes:")
    print("1. Ative o ambiente virtual: .\\venv\\Scripts\\Activate.ps1")
    print("2. Instale as dependências: pip install -r requirements.txt")
    print("3. Execute um dos comandos acima")
    print("4. Ou use o script: python run_tests.py")


if __name__ == "__main__":
    run_test_example()
