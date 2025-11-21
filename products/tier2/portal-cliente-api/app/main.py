from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from . import models, database

# --- Schemas ---
class TimelineEventSchema(BaseModel):
    date: datetime
    title: str
    description: str
    icon_type: str
    status: str

class ProcessSchema(BaseModel):
    id: int
    cnj: str
    title: str
    status: str
    last_update: datetime
    next_step: str
    lawyer_name: str
    timeline: List[TimelineEventSchema] = []

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    cpf: str

# --- App ---
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Portal do Cliente API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Seed Data (Run once) ---
def seed_data(db: Session):
    if db.query(models.User).first():
        return

    # Create User
    user = models.User(cpf="123.456.789-00", name="Cliente Exemplo", hashed_password="dummy")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create Process 1
    p1 = models.Process(
        cnj="5001234-12.2024.8.13.0024",
        title="Ação de Indenização - Danos Morais",
        status="Em Andamento",
        next_step="Aguardando decisão do Juiz",
        lawyer_name="Dr. Carlos Silva",
        client_id=user.id,
        last_update=datetime(2025, 11, 20)
    )
    db.add(p1)
    db.commit()

    # Timeline for P1
    db.add_all([
        models.TimelineEvent(process_id=p1.id, title="Conclusos para Despacho", description="O processo está na mesa do Juiz para análise.", icon_type="gavel", status="current", date=datetime(2025, 11, 20)),
        models.TimelineEvent(process_id=p1.id, title="Petição Juntada", description="Seu advogado enviou novos documentos.", icon_type="file", status="completed", date=datetime(2025, 11, 15)),
        models.TimelineEvent(process_id=p1.id, title="Citação Realizada", description="A outra parte foi avisada.", icon_type="check", status="completed", date=datetime(2025, 11, 1)),
    ])
    db.commit()

    # Create Process 2
    p2 = models.Process(
        cnj="0023456-88.2023.5.03.0011",
        title="Reclamação Trabalhista",
        status="Audiência Marcada",
        next_step="Audiência em 10/12/2025",
        lawyer_name="Dra. Ana Souza",
        client_id=user.id,
        last_update=datetime(2025, 11, 18)
    )
    db.add(p2)
    db.commit()

    # Timeline for P2
    db.add_all([
        models.TimelineEvent(process_id=p2.id, title="Audiência Agendada", description="Sua audiência foi marcada para 10/12/2025.", icon_type="clock", status="current", date=datetime(2025, 11, 18)),
        models.TimelineEvent(process_id=p2.id, title="Defesa Apresentada", description="A empresa apresentou defesa.", icon_type="file", status="completed", date=datetime(2025, 11, 10)),
    ])
    db.commit()

# --- Endpoints ---

@app.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    seed_data(db)
    db.close()

@app.post("/api/auth/login")
def login(request: LoginRequest, db: Session = Depends(database.get_db)):
    # Simple login for demo: checks if CPF exists
    # In production, use JWT and password hashing
    user = db.query(models.User).filter(models.User.cpf == request.cpf).first()
    if not user:
        # Auto-create user for demo purposes if not exists (optional, but good for testing)
        # For now, let's enforce using the seeded CPF or return error
        if request.cpf == "123.456.789-00":
             return {"token": "demo-token", "user": {"name": "Cliente Exemplo", "id": 1}}
        
        raise HTTPException(status_code=401, detail="CPF não encontrado")
    
    return {"token": "demo-token", "user": {"name": user.name, "id": user.id}}

@app.get("/api/processos", response_model=List[ProcessSchema])
def get_processos(db: Session = Depends(database.get_db)):
    # In a real app, filter by logged user ID from token
    # For demo, return all processes for the seeded user
    return db.query(models.Process).all()

@app.get("/api/processos/{process_id}", response_model=ProcessSchema)
def get_processo(process_id: int, db: Session = Depends(database.get_db)):
    process = db.query(models.Process).filter(models.Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    return process

# --- Webhook e Notificações ---
class NewMovimentacaoRequest(BaseModel):
    process_cnj: str
    title: str
    description: str
    icon_type: str = "file"

@app.post("/api/webhook/movimentacao")
async def webhook_movimentacao(
    request: NewMovimentacaoRequest,
    db: Session = Depends(database.get_db)
):
    """
    Webhook que recebe novas movimentações processuais.
    Em produção, seria chamado pelo PJe/e-SAJ quando há atualizações.
    """
    from .notification_service import NotificationService
    
    # Encontrar processo
    process = db.query(models.Process).filter(
        models.Process.cnj == request.process_cnj
    ).first()
    
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    
    # Marcar todas as movimentações anteriores como completed
    db.query(models.TimelineEvent).filter(
        models.TimelineEvent.process_id == process.id,
        models.TimelineEvent.status == "current"
    ).update({"status": "completed"})
    
    # Adicionar nova movimentação
    new_event = models.TimelineEvent(
        process_id=process.id,
        title=request.title,
        description=request.description,
        icon_type=request.icon_type,
        status="current",
        date=datetime.utcnow()
    )
    db.add(new_event)
    
    # Atualizar processo
    process.last_update = datetime.utcnow()
    process.next_step = request.description
    
    db.commit()
    
    # Enviar notificação WhatsApp (simulado)
    notifier = NotificationService()
    client = process.client
    
    # Em produção, o cliente teria um campo 'phone'
    # Por ora, simulamos
    notifier.send_process_update(
        phone="+55 11 98765-4321",  # Todo: pegar do banco
        client_name=client.name,
        process_title=process.title,
        process_cnj=process.cnj,
        event_title=request.title,
        event_description=request.description
    )
    
    return {
        "status": "success",
        "message": "Movimentação registrada e notificação enviada",
        "process_id": process.id,
        "event_id": new_event.id
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Portal do Cliente API", "version": "1.0.0"}
