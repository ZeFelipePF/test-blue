from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_tables
from app.api import coffee_router, order_router

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(coffee_router)
app.include_router(order_router)

@app.on_event("startup")
async def startup_event():
    """Cria as tabelas do banco de dados na inicialização"""
    create_tables()

@app.get("/")
async def root():
    """
    Endpoint raiz da API.
    
    Retorna informações básicas sobre a API, incluindo versão e links para documentação.
    
    **Request URL:**
    ```
    GET http://localhost:8000/
    ```
    
    **Headers:**
    ```
    accept: application/json
    ```
    
    **CURL Example:**
    ```bash
    curl -X GET "http://localhost:8000/" \
      -H "accept: application/json"
    ```
    
    **Response Example:**
    ```json
    {
        "message": "Coffee Shop API",
        "version": "1.0.0",
        "docs": "/docs"
    }
    ```
    
    **Response Fields:**
    - `message`: Nome da API
    - `version`: Versão atual da API
    - `docs`: Link para a documentação interativa
    """
    return {
        "message": "Coffee Shop API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de health check.
    
    Verifica se a API está funcionando corretamente. Útil para monitoramento
    e verificação de status da aplicação.
    
    **Request URL:**
    ```
    GET http://localhost:8000/health
    ```
    
    **Headers:**
    ```
    accept: application/json
    ```
    
    **CURL Example:**
    ```bash
    curl -X GET "http://localhost:8000/health" \
      -H "accept: application/json"
    ```
    
    **Response Example:**
    ```json
    {
        "status": "healthy"
    }
    ```
    
    **Response Fields:**
    - `status`: Status da API ("healthy" quando funcionando corretamente)
    
    **Use Cases:**
    - Monitoramento de aplicação
    - Verificação de status em load balancers
    - Health checks em containers Docker
    - Verificação de conectividade
    """
    return {"status": "healthy"}
