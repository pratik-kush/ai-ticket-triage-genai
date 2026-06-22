# AI-Powered Smart Ticket Triage System

A small real-world project built using the JD technologies: **Python, FastAPI, PyTorch Basics, LLM/GenAI Concepts, Docker, and GitHub Actions CI/CD**.

This project does not use Java or Spring Boot.

## Problem Statement
Support teams receive many customer tickets every day. Manual ticket classification and priority tagging can delay issue resolution. This project provides an AI-powered REST API that accepts a ticket description, predicts the ticket category, predicts ticket priority, and generates an AI-style explanation.

## Tech Stack
- Python
- FastAPI
- PyTorch Basics
- LLM / GenAI Concepts
- Docker
- GitHub Actions CI/CD
- JSON file storage for lightweight persistence

## Features
- Create a support ticket
- Predict ticket category
- Predict ticket priority
- Generate AI-style explanation
- View all tickets
- View ticket by ID
- Update ticket status
- Delete ticket
- Swagger UI documentation
- Docker support
- CI workflow using GitHub Actions

## Local Setup

```bash
cd ai_ticket_triage_genai_fastapi_final
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

For Mac/Linux:

```bash
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI: `http://localhost:8000/docs`

## Docker Setup

```bash
docker build -t ai-ticket-triage .
docker run -p 8000:8000 ai-ticket-triage
```

## Sample Request for POST /tickets

```json
{
  "title": "Login not working",
  "description": "Production users are unable to login and the issue is urgent",
  "created_by": "Pratik"
}
```

## Resume Line
AI-Powered Smart Ticket Triage System | Python, FastAPI, PyTorch Basics, LLM/GenAI Concepts, Docker, GitHub Actions
