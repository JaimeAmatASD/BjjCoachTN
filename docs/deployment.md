# Guía de Despliegue

GrappleCoach se puede desplegar de tres formas según tus necesidades. Esta guía cubre las tres con paso a paso.

---

## Opción A — ChatGPT Custom GPT

**Tiempo estimado:** 5-10 minutos · **Requisitos:** ChatGPT Plus

### Pasos

1. **Crear el GPT**
   - Andá a [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor).
   - Click en *"Create a GPT"*.
   - Cambiá a la pestaña **Configure** (saltá el flujo conversacional).

2. **Llenar los campos básicos**
   - **Name:** `GrappleCoach` (o el que prefieras).
   - **Description:** `Coach virtual especializado en BJJ, grappling y lucha grecorromana. Genera planes personalizados de entrenamiento, nutrición y periodización.`
   - **Profile picture:** Subí un avatar relacionado al deporte.

3. **Cargar las instrucciones**
   - Pegá el contenido completo de [`prompts/system_prompt.md`](../prompts/system_prompt.md) en el campo **Instructions**.
   - Si querés que también registre entrenamientos, agregá al final el contenido de [`prompts/actions_prompt.md`](../prompts/actions_prompt.md).

4. **Conversation starters**
   - Copiá los starters de [`prompts/conversation_starters.md`](../prompts/conversation_starters.md).

5. **Knowledge**
   - Subí los archivos de la carpeta `knowledge/` (pueden ser todos juntos):
     - `nutrition_models.md`
     - `food_tables.md`
     - `training_fundamentals.md`
     - `exercises_library.md`
     - `trusted_sources.md`

6. **Capabilities** — activá:
   - ✅ Web Browsing
   - ✅ Code Interpreter & Data Analysis
   - ✅ Canvas (si está disponible)
   - ❌ Image Generation (no es necesario)

7. **Actions (opcional)** — para integración con Make.com:
   - Click en *"Create new action"*.
   - Importá el contenido de [`integrations/make_webhook/openapi_schema.json`](../integrations/make_webhook/openapi_schema.json).
   - Configurá tu URL de webhook real.

8. **Publicar**
   - Click en *"Save"* → elegí visibilidad (privado, link, público).

---

## Opción B — Claude Project

**Tiempo estimado:** 5 minutos · **Requisitos:** Claude Pro o equivalente

### Pasos

1. **Crear el Project**
   - En [claude.ai](https://claude.ai), click en *"Projects"* en el sidebar.
   - Click en *"Create project"*.
   - Nombre: `GrappleCoach`.

2. **Cargar las instrucciones**
   - En la sección **Set project instructions**, pegá [`prompts/system_prompt.md`](../prompts/system_prompt.md).

3. **Cargar el conocimiento**
   - Click en *"Add content"* → subí los archivos de `knowledge/`.

4. **Listo** — empezá a chatear.

> ⚠️ **Sobre el webhook:** Claude.ai (la interfaz web) no soporta tools/actions arbitrarias en Projects todavía. Si querés la integración con Make.com, usá la opción C (API directa con tool use).

---

## Opción C — Vía API directa

Para integrar GrappleCoach en una app propia (web, mobile, bot de Telegram, etc.).

### Con Claude (Anthropic API)

```python
import anthropic

client = anthropic.Anthropic(api_key="tu-api-key")

# Cargar el system prompt
with open("prompts/system_prompt.md") as f:
    system_prompt = f.read()

# Cargar la knowledge base como context
knowledge_files = [
    "knowledge/nutrition/nutrition_models.md",
    "knowledge/nutrition/food_tables.md",
    "knowledge/training/training_fundamentals.md",
    "knowledge/training/exercises_library.md",
    "knowledge/resources/trusted_sources.md",
]
knowledge = "\n\n---\n\n".join(open(f).read() for f in knowledge_files)

# Definir el tool del webhook
tools = [{
    "name": "registrar_entrenamiento",
    "description": "Registra un entrenamiento en el sistema de seguimiento.",
    "input_schema": {
        "type": "object",
        "properties": {
            "usuario": {"type": "string"},
            "fecha": {"type": "string"},
            "ejercicio": {"type": "string"},
            "series": {"type": "integer"},
            "repeticiones": {"type": "integer"},
            "carga_kg": {"type": "number"},
            "duracion_min": {"type": "number"},
            "observaciones": {"type": "string"},
        },
        "required": ["usuario", "fecha", "ejercicio", "series", "repeticiones", "carga_kg"],
    },
}]

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    system=f"{system_prompt}\n\n# CONOCIMIENTO\n\n{knowledge}",
    tools=tools,
    messages=[
        {"role": "user", "content": "Hola, soy Ana. Tengo torneo en 6 semanas."}
    ],
)
```

### Con OpenAI (Chat Completions con function calling)

```python
from openai import OpenAI

client = OpenAI(api_key="tu-api-key")

with open("prompts/system_prompt.md") as f:
    system_prompt = f.read()

# (cargar knowledge igual que arriba)

functions = [{
    "name": "registrar_entrenamiento",
    "description": "Registra un entrenamiento en el sistema de seguimiento.",
    "parameters": {
        "type": "object",
        "properties": {
            "usuario": {"type": "string"},
            "fecha": {"type": "string"},
            "ejercicio": {"type": "string"},
            "series": {"type": "integer"},
            "repeticiones": {"type": "integer"},
            "carga_kg": {"type": "number"},
        },
        "required": ["usuario", "fecha", "ejercicio", "series", "repeticiones", "carga_kg"],
    },
}]

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": f"{system_prompt}\n\n# CONOCIMIENTO\n\n{knowledge}"},
        {"role": "user", "content": "Hola, soy Ana. Tengo torneo en 6 semanas."},
    ],
    tools=[{"type": "function", "function": f} for f in functions],
)
```

### Manejo del tool call → webhook

Cuando el modelo decide llamar al tool, hacé el POST a Make.com:

```python
import requests

def handle_tool_call(tool_call):
    if tool_call.name == "registrar_entrenamiento":
        webhook_url = "https://hook.eu2.make.com/TU-WEBHOOK-ID"
        payload = {"modo": "registro", **tool_call.input}
        response = requests.post(webhook_url, json=payload)
        return response.json()
```

---

## Variables de entorno recomendadas

Para cualquier despliegue programático, mantené las credenciales fuera del código:

```bash
# .env (no commitear)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
MAKE_WEBHOOK_URL=https://hook.eu2.make.com/...
```
