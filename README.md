# 🏢 API de Consulta CNPJ

Uma API FastAPI simples e eficiente para consultar a razão social de empresas brasileiras através do CNPJ.

## 🚀 Características

- ✅ Consulta rápida de razão social por CNPJ
- ✅ API RESTful com FastAPI
- ✅ Documentação automática (Swagger UI)
- ✅ Validação automática de CNPJ
- ✅ Pronto para deploy em cloud

## 📋 Pré-requisitos

- Python 3.11+
- pip

## 🛠️ Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd CnpjApp
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## 📖 Documentação da API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔍 Endpoints

### GET `/`
Retorna informações básicas da API.

### GET `/razao-social`

Consulta a razão social de uma empresa pelo CNPJ.

**Parâmetros:**
- `cnpj` (string): Número do CNPJ (com ou sem formatação)

**Exemplo de uso:**
```http
GET /razao-social?cnpj=11222333000181
```

**Resposta:**
```json
{
  "razao_social": "Nome da Empresa LTDA"
}
```

**Códigos de erro:**
- `400`: CNPJ inválido (deve ter 14 dígitos)
- `404`: Empresa não encontrada
- `500`: Erro interno do servidor

## 🚀 Deploy

Esta aplicação está configurada para deploy nas seguintes plataformas:

### Heroku
```bash
git push heroku main
```

### Railway
```bash
railway login
railway link
railway up
```

### Render
1. Conecte seu repositório GitHub ao Render
2. Configure o serviço como Web Service
3. Use o comando de build: `pip install -r requirements.txt`
4. Use o comando de start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🔧 Configuração

A aplicação usa as seguintes variáveis de ambiente:

- `PORT`: Porta para execução (padrão: 8000)

## 📦 Dependências

- `fastapi`: Framework web moderno para Python
- `uvicorn`: Servidor ASGI
- `requests`: Biblioteca para requisições HTTP
- `gunicorn`: Servidor WSGI para produção

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT.
