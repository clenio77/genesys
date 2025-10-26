"""
API REST para Automação de Prazos
"""

import sys
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.config.database import get_db
from shared.database.models import Prazo, Notificacao
from shared.utils.logger import setup_logger

logger = setup_logger("automacao_api", "automacao_api.log")

app = FastAPI(title="Automação de Prazos Processuais API", version="1.0.0")


# Pydantic Models
class PrazoCreate(BaseModel):
    tipo: str
    processo: Optional[str]
    tribunal: Optional[str]
    data_vencimento: date
    metadata: Optional[dict] = None


class PrazoResponse(BaseModel):
    id: int
    tipo: str
    processo: Optional[str]
    tribunal: Optional[str]
    data_vencimento: date
    status: str
    dias_restantes: int
    
    class Config:
        from_attributes = True


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "Automação de Prazos Processuais",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


@app.post("/prazos/", response_model=PrazoResponse)
async def criar_prazo(prazo: PrazoCreate, user_id: int, db: Session = Depends(get_db)):
    """Criar um novo prazo processual"""
    
    # Calcular dias restantes
    dias_restantes = (prazo.data_vencimento - date.today()).days
    
    if dias_restantes < 0:
        raise HTTPException(status_code=400, detail="Data de vencimento inválida")
    
    # Criar prazo
    novo_prazo = Prazo(
        user_id=user_id,
        tipo=prazo.tipo,
        processo=prazo.processo,
        tribunal=prazo.tribunal,
        data_vencimento=prazo.data_vencimento,
        status="pendente",
        metadata=prazo.metadata
    )
    
    db.add(novo_prazo)
    db.commit()
    db.refresh(novo_prazo)
    
    logger.info(f"Prazo criado: {novo_prazo.id}")
    
    return PrazoResponse(
        id=novo_prazo.id,
        tipo=novo_prazo.tipo,
        processo=novo_prazo.processo,
        tribunal=novo_prazo.tribunal,
        data_vencimento=novo_prazo.data_vencimento,
        status=novo_prazo.status,
        dias_restantes=dias_restantes
    )


@app.get("/prazos/", response_model=List[PrazoResponse])
async def listar_prazos(
    user_id: int = Query(...),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Listar prazos do usuário"""
    
    query = db.query(Prazo).filter(Prazo.user_id == user_id)
    
    if status:
        query = query.filter(Prazo.status == status)
    
    prazos = query.all()
    
    # Adicionar dias restantes
    hoje = date.today()
    resultado = []
    for prazo in prazos:
        dias_restantes = (prazo.data_vencimento - hoje).days
        
        resultado.append(PrazoResponse(
            id=prazo.id,
            tipo=prazo.tipo,
            processo=prazo.processo,
            tribunal=prazo.tribunal,
            data_vencimento=prazo.data_vencimento,
            status=prazo.status,
            dias_restantes=dias_restantes
        ))
    
    return resultado


@app.get("/prazos/{prazo_id}", response_model=PrazoResponse)
async def obter_prazo(prazo_id: int, db: Session = Depends(get_db)):
    """Obter detalhes de um prazo específico"""
    
    prazo = db.query(Prazo).filter(Prazo.id == prazo_id).first()
    
    if not prazo:
        raise HTTPException(status_code=404, detail="Prazo não encontrado")
    
    dias_restantes = (prazo.data_vencimento - date.today()).days
    
    return PrazoResponse(
        id=prazo.id,
        tipo=prazo.tipo,
        processo=prazo.processo,
        tribunal=prazo.tribunal,
        data_vencimento=prazo.data_vencimento,
        status=prazo.status,
        dias_restantes=dias_restantes
    )


@app.patch("/prazos/{prazo_id}/concluir")
async def concluir_prazo(prazo_id: int, db: Session = Depends(get_db)):
    """Marcar um prazo como concluído"""
    
    prazo = db.query(Prazo).filter(Prazo.id == prazo_id).first()
    
    if not prazo:
        raise HTTPException(status_code=404, detail="Prazo não encontrado")
    
    prazo.status = "concluido"
    prazo.updated_at = datetime.now()
    
    db.commit()
    db.refresh(prazo)
    
    logger.info(f"Prazo {prazo_id} marcado como concluído")
    
    return {"message": "Prazo marcado como concluído", "prazo_id": prazo_id}


@app.get("/estatisticas/")
async def obter_estatisticas(user_id: int, db: Session = Depends(get_db)):
    """Obter estatísticas de prazos do usuário"""
    
    hoje = date.today()
    
    # Total de prazos
    total_prazos = db.query(Prazo).filter(Prazo.user_id == user_id).count()
    
    # Prazos pendentes
    prazos_pendentes = db.query(Prazo).filter(
        Prazo.user_id == user_id,
        Prazo.status == "pendente"
    ).count()
    
    # Prazos vencendo nos próximos 7 dias
    prazos_7_dias = db.query(Prazo).filter(
        Prazo.user_id == user_id,
        Prazo.data_vencimento >= hoje,
        Prazo.data_vencimento <= date.today() + timedelta(days=7),
        Prazo.status == "pendente"
    ).count()
    
    # Prazos vencidos
    prazos_vencidos = db.query(Prazo).filter(
        Prazo.user_id == user_id,
        Prazo.data_vencimento < hoje,
        Prazo.status == "pendente"
    ).count()
    
    return {
        "total_prazos": total_prazos,
        "prazos_pendentes": prazos_pendentes,
        "prazos_7_dias": prazos_7_dias,
        "prazos_vencidos": prazos_vencidos,
        "taxa_conclusao": round((1 - prazos_pendentes/total_prazos) * 100, 2) if total_prazos > 0 else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

