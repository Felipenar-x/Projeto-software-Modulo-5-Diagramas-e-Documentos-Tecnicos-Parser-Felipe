import re
from typing import List, Dict


def parse_api_endpoints(source_code: str) -> List[Dict]:
    endpoints = []

    endpoints.extend(parse_fastapi_endpoints(source_code))
    endpoints.extend(parse_spring_endpoints(source_code))

    return endpoints


def parse_fastapi_endpoints(source_code: str) -> List[Dict]:
    pattern = r'@\w+\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']\)'
    matches = re.findall(pattern, source_code, re.IGNORECASE)

    endpoints = []

    for method, path in matches:
        endpoints.append({
            "method": method.upper(),
            "path": path,
            "framework": "FastAPI",
            "description": f"Endpoint {method.upper()} detectado automaticamente em {path}"
        })

    return endpoints


def parse_spring_endpoints(source_code: str) -> List[Dict]:
    endpoints = []

    spring_mapping = {
        "GetMapping": "GET",
        "PostMapping": "POST",
        "PutMapping": "PUT",
        "DeleteMapping": "DELETE",
        "PatchMapping": "PATCH"
    }

    for annotation, method in spring_mapping.items():
        pattern = rf'@{annotation}\(["\']([^"\']+)["\']\)'
        matches = re.findall(pattern, source_code)

        for path in matches:
            endpoints.append({
                "method": method,
                "path": path,
                "framework": "Spring Boot",
                "description": f"Endpoint {method} detectado automaticamente em {path}"
            })

    return endpoints