# ☕ Coffee Shop API

API para gerenciamento de pedidos de café desenvolvida com **FastAPI** e **PostgreSQL**. Esta API permite o registro de pedidos, listagem do menu, consulta de pedidos pendentes e análise de consumo de insumos para baristas.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso da API](#-uso-da-api)
- [Documentação](#-documentação)
- [Estrutura do Projeto](#️-estrutura-do-projeto)
- [Arquitetura](#-arquitetura)
- [Endpoints Detalhados](#-endpoints-detalhados)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Menu de Cafés](#-menu-de-cafés)
- [Análise de Consumo](#-análise-de-consumo)
- [Desenvolvimento](#-desenvolvimento)
- [Testes](#-testes)
- [Requisitos do Desafio](#-requisitos-do-desafio)
- [Contribuição](#-contribuição)

## ✨ Funcionalidades

### ✅ Requisitos Funcionais Implementados

- **POST /orders/** - Registrar pedidos de café com ingredientes e quantidades
- **GET /menu/** - Listar menu com cafés e respectivos preços
- **GET /orders/pending** - Listar pedidos pendentes com hora e ingredientes
- **GET /orders/consumption** - Análise de consumo para baristas (balanço de cafés, água, leite e café moído)

### 🎯 Funcionalidades Extras

- **GET /menu/all** - Endpoint administrativo com preços em centavos
- **GET /** - Endpoint raiz com informações da API
- **GET /health** - Health check para monitoramento
- **Documentação automática** - Swagger UI e ReDoc
- **Validação automática** - Pydantic para validação de dados
- **Relacionamentos otimizados** - Eager loading para performance

## 🛠️ Tecnologias

- **FastAPI** - Framework web moderno para APIs Python
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **Pydantic** - Validação de dados usando type hints
- **Uvicorn** - Servidor ASGI para produção
- **Python 3.8+** - Linguagem de programação

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório

```bash
git clone https://github.com/ZeFelipePF/test-blue.git
cd coffee-shop-api
```

### 2. Crie um ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
# Crie o banco PostgreSQL
createdb coffee_shop

# Ou usando psql:
psql -U postgres
CREATE DATABASE coffee_shop;
\q
```

### 5. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

**Conteúdo do arquivo .env:**
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/coffee_shop
```

### 6. Popule o menu inicial

```bash
python scripts/populate_menu.py
```

### 7. Execute os testes unitários

```bash
python -m pytest tests/unit/ -v
```

### 8. Execute a aplicação

```bash
# Desenvolvimento (com reload automático)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `DATABASE_URL` | URL de conexão com PostgreSQL | Obrigatório |

### Configurações da API

- **Título**: Coffee Shop API
- **Versão**: 1.0.0
- **CORS**: Habilitado para todas as origens
- **Documentação**: Swagger UI em `/docs` e ReDoc em `/redoc`

## 📖 Uso da API

### Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

**Resposta:**
```json
{
  "status": "healthy"
}
```

## 🏗️ Estrutura do Projeto

```
coffee-shop-api/
├── app/                          # Aplicação principal
│   ├── __init__.py
│   ├── main.py                   # FastAPI app e configuração
│   ├── config.py                 # Configurações globais
│   ├── database.py               # Configuração do banco de dados
│   ├── models/                   # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── coffee.py             # Modelo Coffee
│   │   └── order.py              # Modelos Order e OrderItem
│   ├── schemas/                  # Schemas Pydantic
│   │   ├── __init__.py
│   │   ├── coffee.py             # Schemas de validação Coffee
│   │   └── order.py              # Schemas de validação Order
│   ├── services/                 # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── coffee_service.py     # Operações com cafés
│   │   └── order_service.py      # Operações com pedidos
│   └── api/                      # Endpoints HTTP
│       ├── __init__.py
│       ├── coffee.py             # Endpoints do menu
│       └── order.py              # Endpoints de pedidos
├── scripts/                      # Scripts utilitários
│   ├── __init__.py
│   └── populate_menu.py          # População do menu inicial
├── requirements.txt              # Dependências Python
├── .env.example                  # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
```

## 🏛️ Arquitetura

### Padrão MVC Adaptado

O projeto segue o padrão **MVC (Model-View-Controller)** adaptado para APIs:

- **Models** (`app/models/`) - Definem a estrutura do banco de dados
- **Schemas** (`app/schemas/`) - Validam dados de entrada e saída
- **Services** (`app/services/`) - Contêm a lógica de negócio
- **API** (`app/api/`) - Definem os endpoints HTTP

### Fluxo de Dados

```
Cliente → API Endpoint → Service → Model → Database
                ↓
Cliente ← Schema ← Service ← Model ← Database
```

### Relacionamentos do Banco

```
coffees (1) ←→ (N) order_items (N) ←→ (1) orders
```

- Um café pode estar em vários itens de pedido
- Um pedido pode ter vários itens
- Cada item de pedido referencia um café específico

## 🔗 Endpoints Detalhados

### Menu

#### `GET /menu/`
Lista o menu com preços em reais para clientes.

**Headers:**
```
accept: application/json
```

**Resposta:**
```json
[
  {
    "id": 11,
    "name": "Expresso",
    "price": 2.0,
    "water_ml": 50,
    "milk_ml": 0,
    "coffee_grounds_g": 15
  }
]
```

#### `GET /menu/all`
Lista todos os cafés com preços em centavos para administradores.

**Headers:**
```
accept: application/json
```

**Resposta:**
```json
[
  {
    "id": 11,
    "name": "Expresso",
    "price": 200,
    "water_ml": 50,
    "milk_ml": 0,
    "coffee_grounds_g": 15
  }
]
```

### Pedidos

#### `POST /orders/`
Registra um novo pedido de café.

**Headers:**
```
Content-Type: application/json
accept: application/json
```

**Body:**
```json
{
  "items": [
    {
      "coffee_id": 11,
      "quantity": 2
    },
    {
      "coffee_id": 13,
      "quantity": 1
    }
  ]
}
```

**Resposta:**
```json
{
  "id": 1,
  "created_at": "2025-09-18T17:39:33.186615",
  "total_price": 8.5,
  "status": "pending",
  "items": [
    {
      "id": 1,
      "coffee_id": 11,
      "quantity": 2,
      "coffee_name": "Expresso",
      "item_price": 4.0
    },
    {
      "id": 2,
      "coffee_id": 13,
      "quantity": 1,
      "coffee_name": "Cappuccino",
      "item_price": 4.5
    }
  ]
}
```

#### `GET /orders/pending`
Lista todos os pedidos pendentes com informações detalhadas.

**Headers:**
```
accept: application/json
```

**Resposta:**
```json
[
  {
    "id": 1,
    "created_at": "2025-09-18T17:39:33.186615",
    "total_price": 8.5,
    "status": "pending",
    "items": [
      {
        "id": 1,
        "coffee_id": 11,
        "quantity": 2,
        "coffee_name": "Expresso",
        "item_price": 4.0
      }
    ]
  }
]
```

#### `GET /orders/consumption`
Análise de consumo de insumos para baristas.

**Query Parameters:**
- `days` (int, opcional): Número de dias para análise (padrão: 1)

**Headers:**
```
accept: application/json
```

**Resposta:**
```json
{
  "period_days": 7,
  "total_coffees": 45,
  "total_water_ml": 2250,
  "total_milk_ml": 1800,
  "total_coffee_grounds_g": 675,
  "daily_averages": {
    "coffees": 6.43,
    "water_ml": 321.43,
    "milk_ml": 257.14,
    "coffee_grounds_g": 96.43
  }
}
```

### Endpoints de Sistema

#### `GET /`
Endpoint raiz com informações da API.

**Resposta:**
```json
{
  "message": "Coffee Shop API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

#### `GET /health`
Health check para monitoramento.

**Resposta:**
```json
{
  "status": "healthy"
}
```

## 📝 Exemplos de Uso

### 1. Listar Menu

```bash
curl -X GET "http://localhost:8000/menu/" \
  -H "accept: application/json"
```

### 2. Criar Pedido

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "items": [
      {
        "coffee_id": 11,
        "quantity": 2
      },
      {
        "coffee_id": 13,
        "quantity": 1
      }
    ]
  }'
```

### 3. Consultar Pedidos Pendentes

```bash
curl -X GET "http://localhost:8000/orders/pending" \
  -H "accept: application/json"
```

### 4. Análise de Consumo (7 dias)

```bash
curl -X GET "http://localhost:8000/orders/consumption?days=7" \
  -H "accept: application/json"
```

### 5. Health Check

```bash
curl -X GET "http://localhost:8000/health" \
  -H "accept: application/json"
```

## ☕ Menu de Cafés

| Café | Preço | Água (ml) | Leite (ml) | Café moído (g) | ID |
|------|-------|-----------|------------|----------------|----|
| Expresso | R$ 2,00 | 50 | 0 | 15 | 11 |
| Expresso Duplo | R$ 3,00 | 100 | 0 | 30 | 12 |
| Cappuccino | R$ 4,50 | 30 | 120 | 15 | 13 |
| Flat White | R$ 5,50 | 30 | 150 | 15 | 14 |
| Americano | R$ 3,50 | 100 | 0 | 15 | 15 |

## 📊 Análise de Consumo

O endpoint `/orders/consumption` fornece análise detalhada para baristas:

### Funcionalidades

- **Período configurável**: Analisa os últimos X dias
- **Cálculo de médias**: Média diária de consumo
- **Projeção futura**: Baseada na média dos últimos dias
- **Métricas completas**: Cafés, água, leite e café moído

### Lógica de Cálculo

1. **Busca pedidos** dos últimos X dias
2. **Calcula totais** de ingredientes consumidos
3. **Divide pelo período** para obter médias diárias
4. **Retorna estatísticas** para planejamento

### Casos de Uso

- **Planejamento de estoque**: Quantos ingredientes comprar
- **Previsão de demanda**: Quantos cafés fazer por dia
- **Análise de tendências**: Padrões de consumo
- **Otimização de recursos**: Uso eficiente de ingredientes

## 🧪 Testes

O projeto inclui uma suíte completa de testes unitários e de integração para garantir a qualidade e confiabilidade da API.

### 📁 Estrutura dos Testes

```
tests/
├── conftest.py              # Configuração global e fixtures
├── unit/                    # Testes unitários
│   ├── test_coffee_service.py
│   └── test_order_service.py
```

### 🚀 Como Executar os Testes

1. **Instalar dependências (inclui dependências de teste):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar todos os testes:**
   ```bash
   pytest tests/ -v
   ```

3. **Executar testes específicos:**
   ```bash
   # Apenas testes unitários
   pytest tests/unit/ -v
   
   # Com cobertura de código
   pytest tests/ --cov=app --cov-report=term-missing
   ```

### 📊 Cobertura de Testes

- **Testes Unitários**: 100% dos serviços (coffee_service, order_service)
- **Casos de Sucesso**: Todos os cenários funcionais
- **Casos de Erro**: Validação de dados e tratamento de erros
- **Database de Teste**: SQLite em memória para isolamento

### 🎯 Cenários Testados

#### ✅ Casos de Sucesso
- Criação de pedidos válidos
- Busca de menu e pedidos pendentes
- Análise de consumo de insumos
- Endpoints principais funcionando

#### ❌ Casos de Erro
- IDs de café inválidos
- Dados de entrada inválidos
- Database vazio
- Parâmetros inválidos

#### 🔄 Casos de Consistência
- Consistência entre endpoints
- Validação de tipos de dados
- Estrutura de respostas
- Headers HTTP

### 📚 Documentação dos Testes

Para mais detalhes sobre a estrutura e execução dos testes, consulte os arquivos de teste em `tests/` que incluem comentários detalhados sobre cada cenário testado.

## 🛠️ Desenvolvimento

### Estrutura de Código

- **Type Hints**: Todos os parâmetros e retornos tipados
- **Docstrings**: Documentação completa em todos os endpoints
- **Error Handling**: Tratamento adequado de erros
- **Validation**: Validação automática com Pydantic
- **Performance**: Eager loading para evitar N+1 queries

### Padrões Utilizados

- **Dependency Injection**: Sessões de banco injetadas automaticamente
- **Repository Pattern**: Services encapsulam lógica de banco
- **Schema Validation**: Pydantic para validação de dados
- **Async/Await**: Suporte a operações assíncronas

### Comandos Úteis

```bash
# Executar com reload automático
uvicorn app.main:app --reload

# Executar em porta específica
uvicorn app.main:app --reload --port 8080

# Executar com logs detalhados
uvicorn app.main:app --reload --log-level debug

# Popular menu novamente
python scripts/populate_menu.py
```


## 📋 Requisitos do Desafio

### ✅ Requisitos Funcionais

- [x] **POST /orders** - Registrar pedidos com ingredientes e quantidades
- [x] **GET /menu** - Listar menu com cafés e preços
- [x] **GET /orders/pending** - Listar pedidos pendentes com hora e ingredientes
- [x] **GET /orders/consumption** - Análise de consumo para baristas

### ✅ Detalhes Técnicos

- [x] **Menu em banco de dados** - Tabela `coffees` com ingredientes
- [x] **Valor total no POST** - Resposta inclui preço total a ser pago
- [x] **Análise de consumo** - Média dos últimos 24h × dias informados
- [x] **Python** - Desenvolvido em Python com FastAPI

### ✅ Menu e Ingredientes

| Café | Preço | Água (ml) | Leite (ml) | Café moído (g) |
|------|-------|-----------|------------|----------------|
| Expresso | R$2,00 | 50 | 0 | 15 |
| Expresso Duplo | R$3,00 | 100 | 0 | 30 |
| Cappuccino | R$4,50 | 30 | 120 | 15 |
| Flat White | R$5,50 | 30 | 150 | 15 |
| Americano | R$3,50 | 100 | 0 | 15 |

### ✅ Requisitos de Entrega

- [x] **README detalhado** - Este documento com instruções completas
- [x] **Instruções de instalação** - Passo a passo detalhado
- [x] **Instruções de execução** - Como rodar a aplicação
- [x] **Exemplos de uso** - CURL examples e payloads
- [x] **Headers** - Documentação de headers necessários

### 🎯 Melhorias Implementadas

- **Documentação automática** - Swagger UI e ReDoc
- **Validação robusta** - Pydantic com type hints
- **Performance otimizada** - Eager loading e índices
- **Health check** - Endpoint para monitoramento
- **Estrutura escalável** - Padrão MVC bem definido
- **Error handling** - Tratamento adequado de erros
- **Relacionamentos** - Modelos bem estruturados
- **Scripts utilitários** - População automática do menu

## 🤝 Contribuição

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- **PEP 8**: Seguir padrões de código Python
- **Type Hints**: Sempre tipar parâmetros e retornos
- **Docstrings**: Documentar todas as funções públicas
- **Commits**: Mensagens claras e descritivas

### Issues

- Use o sistema de issues do GitHub
- Descreva o problema claramente
- Inclua passos para reproduzir
- Adicione logs e screenshots quando relevante

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

- **Email**: josefelipepintofaria@gmail.com
- **GitHub**: https://github.com/ZeFelipePF
- **LinkedIn**: https://www.linkedin.com/in/josefelipepintofaria

---
