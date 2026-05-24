from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    ParseRequest,
    ParseResponse,
    ApiDocumentationRequest,
    ApiDocumentationResponse
)

from app.services.java_parser import parse_java_code
from app.services.api_parser import parse_api_endpoints


app = FastAPI(
    title="DoculA Parser API",
    description="Microsserviço responsável por analisar código-fonte e extrair informações para geração de diagramas UML e documentação de API.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "docula-parser-api",
        "version": "0.4.0"
    }


@app.post("/parse/class", response_model=ParseResponse)
def parse_class(request: ParseRequest):
    parsed_result = parse_java_code(request.source_code)

    return parsed_result

@app.post("/parse/api", response_model=ApiDocumentationResponse)
def parse_api_documentation(request: ApiDocumentationRequest):
    endpoints = parse_api_endpoints(request.source_code)

    return {
        "endpoints": endpoints
    }