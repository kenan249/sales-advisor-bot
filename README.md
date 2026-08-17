# Código Café — Backend Starter

Base inicial del backend con FastAPI + SQLAlchemy + MySQL + Redis y arquitectura hexagonal.

## Capas

- domain: reglas y modelos del negocio
- application: casos de uso, puertos y servicios
- adapters/inbound: entradas HTTP/WhatsApp
- adapters/outbound: OpenAI, WhatsApp, repositorios
- infrastructure/shared: configuración y composición de dependencias

## Ejecutar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up --build
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

## Flujo inicial

WhatsApp -> Webhook -> MessageHandler -> AIIntentInterpreter -> IntentRouter -> UseCase -> ResponseGenerator -> WhatsAppSender

Los adapters de OpenAI y WhatsApp son FAKES inicialmente para poder probar la arquitectura sin credenciales externas.

Para usar OpenAI, añade estas variables a `.env`. Al definir `OPENAI_API_KEY`, el
contenedor selecciona automáticamente el adaptador real; sin ella utiliza el fake.

```env
OPENAI_API_KEY=tu_clave
OPENAI_MODEL=gpt-4.1-mini
```
