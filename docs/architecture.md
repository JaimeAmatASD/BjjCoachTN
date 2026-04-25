# Arquitectura

GrappleCoach está pensado como un **sistema modular** que separa el comportamiento del asistente, su base de conocimiento y sus integraciones con sistemas externos. Esto permite cambiar cualquiera de las tres capas sin tocar las otras.

---

## Vista de alto nivel

```
┌──────────────────────────────────────────────────────────────────┐
│                          USUARIO FINAL                            │
│                  (atleta de BJJ / Grappling)                      │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                              │  Chat en lenguaje natural
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CAPA DE INTERFAZ                               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐│
│  │ ChatGPT         │  │ Claude Project   │  │ API directa       ││
│  │ Custom GPT      │  │                  │  │ (Anthropic/OpenAI)││
│  └─────────────────┘  └──────────────────┘  └──────────────────┘│
└─────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                       CAPA LLM (motor)                            │
│              GPT-4 / Claude / Gemini / etc.                       │
│                                                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  System Prompt                                           │   │
│   │  - Identidad y propósito                                 │   │
│   │  - Flujo de entrevista (6 preguntas)                     │   │
│   │  - Reglas de comportamiento                              │   │
│   │  - Estilo y tono                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│  KNOWLEDGE BASE   │ │  TOOLS       │ │  PROGRESS STORE          │
│                   │ │  (Actions)   │ │                          │
│ - Modelos nutric. │ │              │ │  Make.com webhook        │
│ - Tabla de macros │ │  POST a      │ │       │                  │
│ - Periodización   │ │  webhook ──► │ │       ▼                  │
│ - 100 ejercicios  │ │              │ │  Google Sheets / Notion  │
│ - Fuentes ext.    │ │              │ │  / Airtable / DB         │
└──────────────────┘ └──────────────┘ └──────────────────────────┘
```

---

## Componentes en detalle

### 1. Capa de interfaz

El sistema es **agnóstico al cliente**. Las tres opciones soportadas:

| Plataforma | Pros | Contras |
|------------|------|---------|
| ChatGPT Custom GPT | Setup en 5 min, distribución vía link, store público | Vendor lock-in con OpenAI, sin control fino del modelo |
| Claude Project | Mejor comprensión de instrucciones largas, knowledge nativa | Sin equivalente directo a "Actions" — requiere API para webhooks |
| API directa | Control total, integrable en cualquier app | Hay que construir la UI |

### 2. System Prompt

Vive en [`prompts/system_prompt.md`](../prompts/system_prompt.md). Es el **único punto de control** del comportamiento del asistente. Está estructurado en 9 secciones:

1. Identidad y propósito
2. Flujo de entrevista inicial
3. Estilo de comunicación
4. Funciones principales
5. Reglas de comportamiento
6. Personalización a pedido
7. Recursos disponibles
8. Ejemplos de preguntas
9. Restricciones (qué nunca hace)

### 3. Knowledge Base

La base de conocimiento se carga como **archivos adjuntos** a la conversación (sea en ChatGPT, Claude o vía API con context window). Son cinco archivos:

- `nutrition_models.md` — 7 modelos nutricionales con principios, estructura y pros/contras.
- `food_tables.md` — Tabla de macros para ~45 alimentos comunes.
- `training_fundamentals.md` — Principios de periodización (off-season / pretemporada / in-season) basados en literatura clásica de S&C.
- `exercises_library.md` — 100 ejercicios en 10 categorías (técnicos, drills, fuerza, potencia, cardio, core, cuello, agarre, movilidad).
- `trusted_sources.md` — Lista de fuentes externas confiables que el asistente puede citar.

### 4. Tools (Actions / Function Calling)

El asistente puede llamar a un **webhook HTTP** para persistir datos del atleta. El schema está en [`integrations/make_webhook/openapi_schema.json`](../integrations/make_webhook/openapi_schema.json).

Dos modos de operación:

```
modo: "registro"  → POST con datos de un entrenamiento
modo: "consulta"  → POST con filtros para recuperar historial
```

La lógica del lado del LLM (qué preguntar antes de llamar al webhook, cómo manejar errores) está en [`prompts/actions_prompt.md`](../prompts/actions_prompt.md).

### 5. Progress Store

Make.com actúa como **integration layer**. Recibe el webhook y reenvía a:

- **Google Sheets** (default — un row por sesión)
- **Notion** (opcional — una página por atleta)
- **Airtable / Supabase / Postgres** (opcional)

El asistente nunca habla directamente con la base de datos — siempre vía Make.com. Esto desacopla el sistema y permite cambiar el almacenamiento sin tocar el LLM.

---

## Flujos principales

### Flujo A — Generación de un plan nuevo

```
Atleta abre el chat
   ↓
Asistente saluda y pregunta el nombre/perfil
   ↓
[Loop: 6 preguntas, una por turno]
   ↓
Asistente sintetiza la información
   ↓
Asistente consulta knowledge/training/training_fundamentals.md
Asistente consulta knowledge/training/exercises_library.md
Asistente consulta knowledge/nutrition/nutrition_models.md
   ↓
Asistente devuelve:
   - Programa global con fases
   - Plan semanal detallado
   - Plan nutricional
   - Suplementación
   ↓
Atleta da feedback / pide ajustes
   ↓
Asistente ajusta y confirma
```

### Flujo B — Registro de una sesión

```
Atleta: "Registrá mi sentadilla 5×5 a 100 kg"
   ↓
Asistente verifica que tiene el nombre del atleta
   ↓
Asistente verifica los campos obligatorios:
   fecha, ejercicio, series, repeticiones, carga_kg
   ↓
[Si falta algo, pregunta]
   ↓
Asistente hace POST al webhook
   ↓
Make.com escribe en Google Sheets
   ↓
Asistente confirma con visual ✅
```

### Flujo C — Consulta de historial

```
Atleta: "Mostrame mis dominadas del último mes"
   ↓
Asistente hace POST con modo: "consulta"
   ↓
Make.com devuelve los registros filtrados
   ↓
Asistente formatea como tabla o gráfico ASCII
   ↓
Asistente comenta tendencias relevantes
```

---

## Decisiones de diseño

### ¿Por qué entrevista guiada en lugar de un formulario?

Un formulario funcionaría — pero un atleta que abre un chat no quiere llenar campos, quiere hablar. La entrevista en turnos cortos:

- Reduce fricción inicial.
- Permite que el atleta agregue contexto que un formulario no captaría.
- Da tiempo al modelo a procesar cada respuesta antes de la siguiente pregunta.

### ¿Por qué excluir la dieta cetogénica?

La cetogénica estricta es subóptima para deportes glucolíticos como el grappling, donde la potencia y la resistencia anaeróbica dependen del glucógeno muscular. Hay literatura de NSCA y ACSM que respalda esta exclusión.

### ¿Por qué webhook a Make.com en lugar de DB propia?

- ⏱️ **Velocidad de iteración** — Make.com permite cambiar el destino (Sheets → Notion → DB) sin tocar el código del asistente.
- 💰 **Costo** — Plan gratuito de Make.com cubre casos de uso personales.
- 🔐 **Separación de responsabilidades** — El LLM no necesita credenciales de DB.

### ¿Por qué knowledge en archivos `.md` y no embeddings/RAG?

El volumen de conocimiento es chico (<50k tokens total). Cabe en la ventana de contexto de cualquier LLM moderno. Embeddings + RAG agregan complejidad sin ganancia clara para este caso de uso.

> Cuando la base crezca a >100k tokens (libros enteros, transcripciones de muchas clases), tiene sentido migrar a RAG con vector store.
