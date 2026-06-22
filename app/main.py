from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from app.ai_engine import analyze_ticket
from app.database import delete_ticket, find_ticket_by_id, get_next_id, initialize_database, read_tickets, save_ticket, update_ticket_status
from app.models import PredictionRequest, PredictionResponse, StatusUpdate, TicketCreate, TicketResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="AI-Powered Smart Ticket Triage System",
    description="FastAPI + PyTorch Basics + LLM/GenAI Concept project for automatic support ticket classification and prioritization.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {"message": "AI-Powered Smart Ticket Triage System is running", "swagger_url": "/docs"}


@app.post("/predict", response_model=PredictionResponse)
def predict_ticket(request: PredictionRequest):
    return analyze_ticket(request.description)


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    prediction = analyze_ticket(ticket.description)
    new_ticket = {
        "id": get_next_id(),
        "title": ticket.title,
        "description": ticket.description,
        "category": prediction["category"],
        "priority": prediction["priority"],
        "status": "Open",
        "created_by": ticket.created_by,
        "ai_explanation": prediction["ai_explanation"],
    }
    return save_ticket(new_ticket)


@app.get("/tickets", response_model=List[TicketResponse])
def get_all_tickets():
    return read_tickets()


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    ticket = find_ticket_by_id(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.put("/tickets/{ticket_id}/status", response_model=TicketResponse)
def update_status(ticket_id: int, request: StatusUpdate):
    ticket = update_ticket_status(ticket_id, request.status)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.delete("/tickets/{ticket_id}")
def remove_ticket(ticket_id: int):
    deleted = delete_ticket(ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}
