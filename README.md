# ChatBot API con FastAPI y LangChain

API simple de chat que utiliza FastAPI y LangChain para interactuar con el modelo GPT de OpenAI. Este proyecto implementa un chatbot con memoria de conversación que puede mantener contexto entre mensajes.

## Características

- FastAPI como framework web
- Integración con OpenAI a través de LangChain
- Historial de conversación en memoria
- Dockerizado para fácil despliegue
- Endpoints de health check y documentación automática

## Requisitos Previos

- Python 3.11+
- Docker y Docker Compose
- Clave API de OpenAI

## Configuración

1. Clona el repositorio:
2. Crea un archivo `.env` en la raíz del proyecto:
3. Agrega tu clave API de OpenAI en el archivo `.env`: OPENAI_API_KEY=your_openai_api_key
4. Instala las dependencias: pip install -r requirements.txt
5. Inicia el servidor: uvicorn main:app --reload
6. a. Construye y ejecuta con docker-compose: docker-compose up --build
   b. Alternativamente, construye y ejecuta con docker:

        ```
        docker build -t chatbot-api .
        docker run -d -p 8000:8000 chatbot-api
        ``` 


## Uso de la API

### Endpoints Disponibles

- `GET /`: Página de bienvenida con información de la API
- `GET /health`: Verificación del estado de la API
- `POST /chat`: Endpoint principal para interactuar con el chatbot

### Instrucciones de uso

1. Verificar el estado de la API:

```
curl -X GET http://localhost:8000/health
```

2. Interactuar con el chatbot:

```
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "Hola, ¿cómo estás?"}'
```

### Ejemplos de uso

{"message":"Bienvenido a la API del Chatbot","endpoints":{"chat":"/chat - POST para enviar mensajes","health":"/health - GET para verificar el estado"}}%       

% curl http://localhost:8000/health
 
{"status":"healthy"}% 

% curl -X POST http://localhost:8000/chat \ 
  -H "Content-Type: application/json" \
  -d '{"user_message": "Cual es la capital de Francia?"}'

{"assistant_message":"La capital de Francia es París."}%                       

% curl -X POST http://localhost:8000/chat \ 
  -H "Content-Type: application/json" \
  -d '{"user_message": "Y la de Argentina?"}'

{"assistant_message":"La capital de Argentina es Buenos Aires."}              

% curl -X POST http://localhost:8000/chat \ 
  -H "Content-Type: application/json" \
  -d '{"user_message": "De que estamos hablando?"}'

{"assistant_message":"Estamos hablando de las capitales de diferentes países, en este caso de Francia y Argentina."}%  