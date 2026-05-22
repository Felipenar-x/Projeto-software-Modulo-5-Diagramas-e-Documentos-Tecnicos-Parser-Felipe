import re
from typing import Dict, List, Tuple


def parse_java_code(source_code: str) -> Dict:
    parsed_classes = []
    relationships = []

    class_blocks = extract_class_blocks(source_code)
    class_names = [class_data["name"] for class_data, _ in class_blocks]

    for class_data, body in class_blocks:
        class_name = class_data["name"]

        attributes_with_types = extract_attributes_with_types(body)
        methods = extract_methods(body)

        attributes = [attribute["name"] for attribute in attributes_with_types]

        parsed_classes.append({
            "name": class_name,
            "attributes": attributes,
            "methods": methods
        })

        if class_data.get("extends"):
            relationships.append({
                "from_class": class_name,
                "to_class": class_data["extends"],
                "type": "inheritance"
            })

        for interface in class_data.get("implements", []):
            relationships.append({
                "from_class": class_name,
                "to_class": interface,
                "type": "implementation"
            })

        for attribute in attributes_with_types:
            attribute_type = clean_type(attribute["type"])

            if attribute_type in class_names and attribute_type != class_name:
                relationships.append({
                    "from_class": class_name,
                    "to_class": attribute_type,
                    "type": "association"
                })

    return {
        "classes": parsed_classes,
        "relationships": remove_duplicate_relationships(relationships)
    }


def extract_class_blocks(source_code: str) -> List[Tuple[Dict, str]]:
    class_pattern = re.compile(
        r'\b(?:public|private|protected)?\s*'
        r'(?:abstract\s+|final\s+)?'
        r'class\s+(\w+)'
        r'(?:\s+extends\s+(\w+))?'
        r'(?:\s+implements\s+([^{]+))?'
        r'\s*\{',
        re.MULTILINE
    )

    results = []

    for match in class_pattern.finditer(source_code):
        class_name = match.group(1)
        extends = match.group(2)

        implements_raw = match.group(3)
        implements = []

        if implements_raw:
            implements = [
                item.strip()
                for item in implements_raw.split(",")
                if item.strip()
            ]

        body_start = match.end() - 1
        body_end = find_matching_brace(source_code, body_start)

        if body_end == -1:
            body = source_code[body_start + 1:]
        else:
            body = source_code[body_start + 1:body_end]

        results.append((
            {
                "name": class_name,
                "extends": extends,
                "implements": implements
            },
            body
        ))

    return results


def find_matching_brace(source_code: str, opening_brace_index: int) -> int:
    count = 0

    for index in range(opening_brace_index, len(source_code)):
        char = source_code[index]

        if char == "{":
            count += 1
        elif char == "}":
            count -= 1

            if count == 0:
                return index

    return -1


def extract_attributes_with_types(class_body: str) -> List[Dict]:
    attribute_pattern = re.compile(
        r'\b(?:private|public|protected)\s+'
        r'(?:static\s+|final\s+)*'
        r'([\w<>\[\]]+)\s+'
        r'(\w+)\s*'
        r'(?:=[^;]*)?;',
        re.MULTILINE
    )

    attributes = []

    for match in attribute_pattern.finditer(class_body):
        attributes.append({
            "type": match.group(1),
            "name": match.group(2)
        })

    return attributes


def extract_methods(class_body: str) -> List[str]:
    method_pattern = re.compile(
        r'\b(?:private|public|protected)\s+'
        r'(?:static\s+|final\s+|abstract\s+)*'
        r'[\w<>\[\], ?]+\s+'
        r'(\w+)\s*'
        r'\([^)]*\)\s*'
        r'(?:\{|;)',
        re.MULTILINE
    )

    ignored = {"if", "for", "while", "switch", "catch"}

    methods = []

    for match in method_pattern.finditer(class_body):
        method_name = match.group(1)

        if method_name not in ignored:
            methods.append(method_name)

    return methods


def clean_type(type_name: str) -> str:
    cleaned = type_name.replace("[]", "")

    generic_match = re.match(r'(\w+)<(\w+)>', cleaned)
    if generic_match:
        return generic_match.group(2)

    return cleaned


def remove_duplicate_relationships(relationships: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []

    for relationship in relationships:
        key = (
            relationship["from_class"],
            relationship["to_class"],
            relationship["type"]
        )

        if key not in seen:
            seen.add(key)
            unique.append(relationship)

    return unique