from pydantic import BaseModel
from typing import List


class ParseRequest(BaseModel):
    source_code: str


class ParsedClass(BaseModel):
    name: str
    attributes: List[str]
    methods: List[str]


class ParsedRelationship(BaseModel):
    from_class: str
    to_class: str
    type: str


class ParseResponse(BaseModel):
    classes: List[ParsedClass]
    relationships: List[ParsedRelationship]


class ApiDocumentationRequest(BaseModel):
    source_code: str


class ApiEndpoint(BaseModel):
    method: str
    path: str
    framework: str
    description: str


class ApiDocumentationResponse(BaseModel):
    endpoints: List[ApiEndpoint]