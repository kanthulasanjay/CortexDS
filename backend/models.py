from pydantic import BaseModel


class PredictionRequest(BaseModel):
    dataset_path: str
    target: str


class ChatRequest(BaseModel):
    question: str


class PredictionResponse(BaseModel):
    model: str
    accuracy: float
    message: str