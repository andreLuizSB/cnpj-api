import os
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="API Consulta CNPJ", description="API para consultar razão social por CNPJ")

@app.get("/")
def read_root():
    return {"message": "API de Consulta CNPJ está funcionando!", "docs": "/docs"}

@app.get("/razao-social")
def get_razao_social(cnpj: str):
    """
    Consulta a razão social de uma empresa pelo CNPJ
    
    - **cnpj**: Número do CNPJ (com ou sem formatação)
    """
    # Remove pontuação do CNPJ
    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if len(cnpj_limpo) != 14:
        raise HTTPException(status_code=400, detail="CNPJ deve ter 14 dígitos")
    
    url = f"https://open.cnpja.com/office/{cnpj_limpo}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")
        
        data = response.json()
        
        # Na API CNPJJá, a razão social está em company.name
        razao_social = data.get("company", {}).get("name")
        
        if not razao_social:
            raise HTTPException(status_code=404, detail="Razão social não encontrada")
        
        return {"razao_social": razao_social}
    
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Erro ao consultar API externa")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)