import os
import logging
from fastapi import FastAPI, HTTPException
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Consulta CNPJ", 
    description="API para consultar razão social por CNPJ",
    version="1.0.0"
)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "API de Consulta CNPJ está funcionando!", "docs": "/docs"}

@app.get("/health")
def health_check():
    """Health check endpoint for Azure monitoring"""
    return {"status": "healthy", "service": "cnpj-api"}

@app.get("/razao-social")
def get_razao_social(cnpj: str):
    """
    Consulta a razão social de uma empresa pelo CNPJ
    
    - **cnpj**: Número do CNPJ (com ou sem formatação)
    """
    logger.info(f"Consulta CNPJ recebida: {cnpj}")
    
    # Remove pontuação do CNPJ
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if len(cnpj_limpo) != 14:
        logger.warning(f"CNPJ inválido: {cnpj}")
        raise HTTPException(status_code=400, detail="CNPJ deve ter 14 dígitos")
    
    url = f"https://open.cnpja.com/office/{cnpj_limpo}"
    
    try:
        logger.info(f"Consultando API externa: {url}")
        response = requests.get(url, timeout=30, headers={'User-Agent': 'CNPJ-API/1.0'})
        
        if response.status_code != 200:
            logger.error(f"API externa retornou status {response.status_code}")
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        data = response.json()
        
        # Na API CNPJJá, a razão social está em company.name
        razao_social = data.get("company", {}).get("name")
        
        if not razao_social:
            logger.error("Razão social não encontrada na resposta da API")
            raise HTTPException(status_code=404, detail="Razão social não encontrada")
        
        logger.info(f"Razão social encontrada: {razao_social}")
        return {"razao_social": razao_social}
    
    except requests.RequestException as e:
        logger.error(f"Erro ao consultar API externa: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao consultar API externa")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Iniciando aplicação na porta {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)