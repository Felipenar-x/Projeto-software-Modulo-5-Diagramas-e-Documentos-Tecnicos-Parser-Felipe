# DoculA Parser API

Microsserviço responsável por analisar código-fonte e extrair informações estruturadas para geração de diagramas UML e documentação de API.

Este serviço faz parte do **Módulo 5 — Diagramas e Documentos Técnicos** da plataforma **DoculA**.

O Parser API recebe código-fonte, identifica classes, atributos, métodos, relacionamentos UML e endpoints REST, retornando esses dados em formato JSON para serem utilizados pelo **Gateway API** e pela **Diagram API**.

---

## Objetivo

O objetivo deste microsserviço é realizar a análise inicial do código-fonte enviado pelo Gateway API.

A partir do código recebido, o Parser API consegue extrair:

- Classes;
- Atributos;
- Métodos;
- Relacionamentos UML;
- Herança com `extends`;
- Implementação de interfaces com `implements`;
- Associações entre classes por atributos;
- Endpoints REST;
- Métodos HTTP como `GET`, `POST`, `PUT`, `DELETE` e `PATCH`.

Essas informações são utilizadas pelos demais serviços para geração automática de diagramas UML, documentação de API e artefatos técnicos do projeto.

---

## Arquitetura

```txt
Frontend
   ↓
Gateway API
   ↓
Parser API
   ↓
Diagram API
```

Fluxo completo dentro do Módulo 5:

```txt
Usuário / Módulo 1 / Módulo 2
   ↓
Frontend
   ↓
Gateway API
   ↓
Parser API
   ↓
Diagram API
   ↓
Gateway API
   ↓
Frontend
```

---

## Responsabilidades do Parser API

* Receber código-fonte enviado pelo Gateway API;
* Analisar a estrutura do código;
* Identificar classes;
* Identificar atributos;
* Identificar métodos;
* Identificar relacionamentos UML;
* Identificar herança e interfaces;
* Identificar associações entre classes;
* Extrair endpoints REST;
* Identificar métodos HTTP;
* Retornar JSON estruturado;
* Servir como base para geração automática de diagramas UML e documentação de API.

---

## Deploy em Produção

### Parser API

```txt
https://diagramas-parser-e6dzc7f5ateae3ce.canadacentral-01.azurewebsites.net
```

### Swagger/OpenAPI do Parser

```txt
https://diagramas-parser-e6dzc7f5ateae3ce.canadacentral-01.azurewebsites.net/docs
```

### Gateway API

```txt
https://docula-gateway-api-dzgfg8ghghadeedd.eastus-01.azurewebsites.net/
```

### Swagger/OpenAPI do Gateway

```txt
https://docula-gateway-api-dzgfg8ghghadeedd.eastus-01.azurewebsites.net/docs
```

### Diagram API

```txt
https://diagramas-diagram-eugce0h0bygfdqhf.canadacentral-01.azurewebsites.net
```

### Swagger/OpenAPI do Diagram API

```txt
https://diagramas-diagram-eugce0h0bygfdqhf.canadacentral-01.azurewebsites.net/docs
```

---

## Requisitos

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic

---

## Instalação

```powershell
pip install -r requirements.txt
```

---

## Como executar localmente

Execute o serviço com:

```powershell
python -m uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```txt
http://127.0.0.1:8000
```

Swagger/OpenAPI local:

```txt
http://127.0.0.1:8000/docs
```

Caso esteja executando junto com o Gateway API e o Diagram API, recomenda-se usar a porta `8001`:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

Arquitetura local recomendada:

```txt
Gateway API  → http://127.0.0.1:8000
Parser API   → http://127.0.0.1:8001
Diagram API  → http://127.0.0.1:8002
```

---

## Endpoints

### Health check

```http
GET /health
```

Exemplo de resposta:

```json
{
  "status": "ok",
  "service": "docula-parser-api"
}
```

---

## Analisar código-fonte para UML

```http
POST /parse/class
```

Este endpoint recebe código-fonte e retorna classes, atributos, métodos e relacionamentos UML.

### Exemplo de entrada

```json
{
  "source_code": "public class Usuario { private String nome; public void login() { } } public class Pedido extends Entidade { private Usuario usuario; public void finalizar() { } }"
}
```

### Exemplo de resposta

```json
{
  "classes": [
    {
      "name": "Usuario",
      "attributes": ["nome"],
      "methods": ["login"]
    },
    {
      "name": "Pedido",
      "attributes": ["usuario"],
      "methods": ["finalizar"]
    }
  ],
  "relationships": [
    {
      "from_class": "Pedido",
      "to_class": "Entidade",
      "type": "inheritance"
    },
    {
      "from_class": "Pedido",
      "to_class": "Usuario",
      "type": "association"
    }
  ]
}
```

---

## Tipos de relacionamentos UML detectados

O Parser API consegue identificar os seguintes tipos de relacionamento:

### Herança

Detectada quando uma classe usa `extends`.

Exemplo:

```java
public class Pedido extends Entidade {
}
```

Retorno:

```json
{
  "from_class": "Pedido",
  "to_class": "Entidade",
  "type": "inheritance"
}
```

Na Diagram API, esse relacionamento é renderizado como:

```txt
Pedido --|> Entidade
```

---

### Implementação de interface

Detectada quando uma classe usa `implements`.

Exemplo:

```java
public class UsuarioService implements IService {
}
```

Retorno:

```json
{
  "from_class": "UsuarioService",
  "to_class": "IService",
  "type": "implementation"
}
```

Na Diagram API, esse relacionamento é renderizado como:

```txt
UsuarioService ..|> IService
```

---

### Associação por atributo

Detectada quando uma classe possui um atributo cujo tipo é outra classe encontrada no código.

Exemplo:

```java
public class Pedido {
    private Usuario usuario;
}
```

Retorno:

```json
{
  "from_class": "Pedido",
  "to_class": "Usuario",
  "type": "association"
}
```

Na Diagram API, esse relacionamento é renderizado como:

```txt
Pedido --> Usuario
```

---

## Extrair documentação de API

```http
POST /parse/api
```

Este endpoint recebe código-fonte de APIs e extrai endpoints REST.

Atualmente possui suporte inicial para padrões como:

* FastAPI;
* Spring Boot;
* Rotas com métodos HTTP comuns.

### Exemplo de entrada FastAPI

```json
{
  "source_code": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/users')\ndef list_users(): pass\n@app.post('/users')\ndef create_user(): pass"
}
```

### Exemplo de resposta

```json
{
  "endpoints": [
    {
      "method": "GET",
      "path": "/users",
      "framework": "FastAPI",
      "description": "Endpoint GET detectado automaticamente em /users"
    },
    {
      "method": "POST",
      "path": "/users",
      "framework": "FastAPI",
      "description": "Endpoint POST detectado automaticamente em /users"
    }
  ]
}
```

### Exemplo de entrada Spring Boot

```json
{
  "source_code": "@RestController\n@RequestMapping('/users')\npublic class UserController {\n    @GetMapping\n    public List<User> listUsers() { return null; }\n\n    @PostMapping\n    public User createUser() { return null; }\n}"
}
```

### Exemplo de resposta

```json
{
  "endpoints": [
    {
      "method": "GET",
      "path": "/users",
      "framework": "Spring Boot",
      "description": "Endpoint GET detectado automaticamente em /users"
    },
    {
      "method": "POST",
      "path": "/users",
      "framework": "Spring Boot",
      "description": "Endpoint POST detectado automaticamente em /users"
    }
  ]
}
```

---

## Fluxo de funcionamento

```txt
1. O usuário envia código-fonte pelo Frontend ou seleciona arquivos vindos do Módulo 2.
2. O Frontend chama o Gateway API.
3. O Gateway envia o código para o Parser API.
4. O Parser API identifica classes, atributos, métodos e relacionamentos.
5. O Parser API retorna os dados estruturados para o Gateway.
6. O Gateway envia esses dados para a Diagram API.
7. A Diagram API gera o PlantUML.
8. O resultado retorna ao Gateway.
9. O Gateway retorna o resultado ao Frontend.
10. Opcionalmente, o diagrama gerado pode ser salvo no Módulo de Upload.
```

---

## Papel na integração com outros microsserviços

Este microsserviço não é consumido diretamente pelo usuário final.

Ele é chamado pelo **Gateway API**, que centraliza a comunicação entre os serviços do Módulo 5.

```txt
Gateway API → Parser API → Dados estruturados
```

Os dados retornados pelo Parser API são utilizados pela Diagram API para gerar diagramas UML.

---

## Integração com o Módulo 1

A integração com o **Módulo 1 — Gerenciamento de Projetos e Usuários** ocorre por meio do Gateway API.

O Módulo 1 envia para o Frontend:

```txt
project_id
company_id
token JWT
```

O Frontend repassa o token ao Gateway no header:

```http
Authorization: Bearer TOKEN
```

O Parser API não valida diretamente usuários ou permissões. Essa responsabilidade fica no Gateway API.

---

## Integração com o Módulo 2

A integração com o **Módulo 2 — Upload, Cadastro e Gerenciamento de Dados** também ocorre por meio do Gateway API.

O Gateway busca os artefatos do projeto no Módulo 2, baixa os arquivos selecionados e envia o conteúdo de código-fonte para o Parser API.

Fluxo:

```txt
Módulo 2 → artefatos do projeto
Gateway API → baixa código-fonte
Gateway API → envia código ao Parser API
Parser API → extrai estrutura técnica
```

O Parser API não acessa diretamente o banco do Módulo 2 nem o Azure Blob Storage.

---

## Exemplo de integração UML

Entrada enviada pelo Gateway:

```json
{
  "source_code": "public class Produto { private String nome; private double preco; public void atualizarPreco() { } }"
}
```

Resposta do Parser API:

```json
{
  "classes": [
    {
      "name": "Produto",
      "attributes": ["nome", "preco"],
      "methods": ["atualizarPreco"]
    }
  ],
  "relationships": []
}
```

Essa resposta pode ser enviada para a Diagram API para gerar um diagrama UML em PlantUML.

---

## Exemplo de integração com relacionamento

Entrada enviada pelo Gateway:

```json
{
  "source_code": "public class Usuario { private String nome; public void login() { } } public class Pedido extends Entidade { private Usuario usuario; public void finalizar() { } }"
}
```

Resposta do Parser API:

```json
{
  "classes": [
    {
      "name": "Usuario",
      "attributes": ["nome"],
      "methods": ["login"]
    },
    {
      "name": "Pedido",
      "attributes": ["usuario"],
      "methods": ["finalizar"]
    }
  ],
  "relationships": [
    {
      "from_class": "Pedido",
      "to_class": "Entidade",
      "type": "inheritance"
    },
    {
      "from_class": "Pedido",
      "to_class": "Usuario",
      "type": "association"
    }
  ]
}
```

---

## Tecnologias utilizadas

* Python
* FastAPI
* Uvicorn
* Pydantic
* Regex
* Azure App Service
* Swagger/OpenAPI

---

## Deploy

O serviço está preparado para deploy em **Azure App Service**.

Startup command utilizado:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Versionamento

O projeto utiliza versionamento semântico.

Versão atual:

```txt
v1.0.0
```

Histórico inicial:

```txt
v0.1.0 - Primeira versão funcional do Parser API com extração de classes, atributos e métodos
v0.1.1 - Preparação para deploy Azure
v0.2.0 - Adição da extração de endpoints REST para documentação de API
v0.3.0 - Adição de relacionamentos UML, herança, interfaces e associações entre classes
v1.0.0 - Versão final do Parser API para entrega do Módulo 5
```
