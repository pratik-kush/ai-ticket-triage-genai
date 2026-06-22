from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=3, example="Login not working")
    description: str = Field(..., min_length=5, example="Production users are unable to login urgently")
    created_by: str = Field(..., min_length=2, example="Pratik")


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: str
    status: str
    created_by: str
    ai_explanation: str


class StatusUpdate(BaseModel):
    status: str = Field(..., example="Closed")


class PredictionRequest(BaseModel):
    description: str = Field(..., min_length=5, example="Payment deducted but invoice not generated")


class PredictionResponse(BaseModel):
    category: str
    priority: str
    ai_explanation: str
