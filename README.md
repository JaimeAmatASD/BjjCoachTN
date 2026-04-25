# 🤼 GrappleCoach — Coach virtual para BJJ y Grappling

> Sistema de coaching impulsado por LLM para atletas de Brazilian Jiu-Jitsu, lucha grecorromana y grappling. Genera planes personalizados de entrenamiento, nutrición y periodización según el perfil, los objetivos y el calendario competitivo del atleta.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Made with](https://img.shields.io/badge/Made%20with-Prompt%20Engineering-blueviolet)]()
[![LLM Compatible](https://img.shields.io/badge/LLM-Claude%20%7C%20GPT--4%20%7C%20Gemini-1f6feb)]()
[![Status](https://img.shields.io/badge/Status-Live-brightgreen)]()

---

## 📖 Índice

- [¿Qué es esto?](#-qué-es-esto)
- [Demo y casos de uso](#-demo-y-casos-de-uso)
- [Arquitectura](#-arquitectura)
- [Estructura del repo](#-estructura-del-repo)
- [Despliegue rápido](#-despliegue-rápido)
- [Personalización](#-personalización)
- [Integración con Make.com](#-integración-con-makecom)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)

---

## 🥋 ¿Qué es esto?

**GrappleCoach** es un *system prompt* + *base de conocimiento* + *integración de webhook* que convierte cualquier LLM moderno (Claude, GPT-4, Gemini, etc.) en un asistente especializado en preparación física para deportes de combate de agarre.

A diferencia de un chatbot genérico de fitness, el sistema:

- 🎯 **Hace una entrevista guiada** al atleta antes de generar nada (edad, peso, nivel, fecha de torneo, estilo, frecuencia, objetivos).
- 🏋️ **Conoce los principios de periodización** para grappling (off-season, pretemporada, temporada) basados en literatura de fuerza y acondicionamiento.
- 🍎 **Selecciona modelos nutricionales** apropiados al objetivo (déficit calórico, IIFYM, ciclado de carbos, ayuno intermitente, mediterránea, etc.).
- 📊 **Registra el progreso** del atleta vía un webhook externo (Make.com) que persiste los datos en una hoja de cálculo.
- 📚 **Usa una biblioteca propia** de 100 ejercicios técnicos y de fuerza para grappling, organizados por categoría.

---

## 🎬 Demo y casos de uso

### Ejemplo de conversación

> **Atleta:** Quiero prepararme para un torneo en 8 semanas, peso 78 kg y necesito bajar a 74 kg.
>
> **GrappleCoach:** Antes de armarte un plan, ¿cuál es tu nivel de experiencia? *principiante / intermedio / avanzado*
>
> **Atleta:** Intermedio, llevo 3 años entrenando.
>
> **GrappleCoach:** Perfecto. ¿Es Gi o No-Gi? *(siguiente pregunta…)*

El asistente nunca lanza un plan antes de tener los 6 datos clave. Una vez que los tiene, devuelve:

- 📅 **Programa global** de las 8 semanas con fases.
- 🗓️ **Plan semanal detallado** con circuitos, kilos y progresiones.
- 🥗 **Plan nutricional** diario con recetas y macros.
- 💊 **Recomendaciones de suplementación** con dosis y horarios.
- 📈 **Tracking** automático del progreso si está conectado al webhook.

### Casos de uso reales

| Caso | Pregunta del atleta | Lo que hace GrappleCoach |
|------|---------------------|--------------------------|
| 🥇 Preparación competitiva | *"Tengo torneo en 6 semanas, ¿cómo estructuro?"* | Plan periodizado en 3 fases con tapering pre-pelea |
| ⚖️ Corte de peso | *"Necesito bajar 4 kg sin perder fuerza"* | Déficit progresivo con ciclado de carbos en días intensos |
| 🔄 Día de descanso activo | *"Circuito de 30 min para hoy"* | Rutina ligera de movilidad + core + cardio |
| 📊 Seguimiento | *"Registrá mi sentadilla 5×5 a 100 kg"* | Hace POST al webhook y confirma el registro |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         USUARIO                              │
│              (Atleta de BJJ / Grappling)                    │
└────────────────────────┬────────────────────────────────────┘
                         │ Conversación natural
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ DE CHAT                          │
│        (ChatGPT Custom GPT  /  Claude Project  /  API)      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ SYSTEM       │  │ KNOWLEDGE    │  │ ACTION / TOOL    │
│ PROMPT       │  │ BASE         │  │ (Webhook)        │
│              │  │              │  │                  │
│ - Reglas     │  │ - Modelos    │  │ POST a Make.com  │
│ - Tono       │  │   nutrición  │  │ → Google Sheets  │
│ - Flujo de   │  │ - 100 ejerc. │  │   (registro de   │
│   entrevista │  │ - Periodizac.│  │    sesiones)     │
│ - Objetivos  │  │ - Tablas     │  │                  │
│              │  │   nutric.    │  │                  │
└──────────────┘  └──────────────┘  └──────────────────┘
```

Tres componentes desacoplados:

1. **`prompts/`** — Define el comportamiento del asistente (qué pregunta, en qué orden, qué tono usa).
2. **`knowledge/`** — La base de conocimiento que el modelo consulta (modelos nutricionales, biblioteca de ejercicios, fundamentos de periodización).
3. **`integrations/`** — Conexiones a sistemas externos para persistencia (webhook Make.com → Google Sheets).

---

## 📁 Estructura del repo

```
BjjCoachTN/
├── README.md                      ← Estás acá
├── LICENSE
├── CHANGELOG.md
├── .gitignore
│
├── docs/                          ← Documentación técnica
│   ├── architecture.md            ← Arquitectura detallada
│   ├── deployment.md              ← Cómo desplegarlo en cada plataforma
│   └── customization.md           ← Cómo adaptarlo a otro deporte
│
├── prompts/                       ← El cerebro del asistente
│   ├── system_prompt.md           ← Instrucciones principales
│   ├── actions_prompt.md          ← Lógica de la integración con webhook
│   └── conversation_starters.md   ← Preguntas iniciales sugeridas
│
├── knowledge/                     ← Base de conocimiento
│   ├── nutrition/
│   │   ├── nutrition_models.md    ← 7 modelos nutricionales
│   │   └── food_tables.md         ← Tabla de macros por alimento
│   ├── training/
│   │   ├── training_fundamentals.md  ← Periodización para grappling
│   │   └── exercises_library.md      ← 100 ejercicios categorizados
│   └── resources/
│       └── trusted_sources.md     ← Fuentes externas confiables
│
├── integrations/
│   └── make_webhook/              ← Integración con Make.com
│       ├── README.md
│       └── openapi_schema.json    ← Schema para registrar la Action
│
└── examples/
    └── conversation_examples.md   ← Conversaciones de ejemplo
```

---

## 🚀 Despliegue rápido

### Opción A — ChatGPT Custom GPT

1. Entrá a [chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor) y creá un GPT nuevo.
2. En **Instructions**, pegá el contenido de [`prompts/system_prompt.md`](./prompts/system_prompt.md).
3. En **Conversation starters**, copiá los de [`prompts/conversation_starters.md`](./prompts/conversation_starters.md).
4. En **Knowledge**, subí los archivos de la carpeta `knowledge/`.
5. (Opcional) En **Actions**, importá [`integrations/make_webhook/openapi_schema.json`](./integrations/make_webhook/openapi_schema.json) y configurá tu webhook de Make.com.

### Opción B — Claude Project

1. En [claude.ai](https://claude.ai), creá un Project nuevo.
2. En **Project instructions**, pegá `prompts/system_prompt.md`.
3. En **Project knowledge**, subí los archivos de `knowledge/`.
4. Listo. (La integración por webhook requiere usar la API con tool use — ver `docs/deployment.md`).

### Opción C — Vía API directa

Ver [`docs/deployment.md`](./docs/deployment.md) para implementación con Claude Messages API o OpenAI Chat Completions con function calling.

---

## ⚙️ Personalización

¿Querés adaptarlo a otro deporte de combate (boxeo, MMA, judo)? Lo importante:

| Componente | Editable | Cómo |
|------------|----------|------|
| Tono del coach | ✅ | Sección 5 de `system_prompt.md` |
| Lista de ejercicios | ✅ | `knowledge/training/exercises_library.md` |
| Modelos nutricionales | ✅ | `knowledge/nutrition/nutrition_models.md` |
| Preguntas iniciales | ✅ | Sección 2 de `system_prompt.md` |
| Periodización base | ⚠️ | Requiere conocer la temporada del deporte |

Detalle completo en [`docs/customization.md`](./docs/customization.md).

---

## 🔌 Integración con Make.com

El asistente puede hacer POST a un webhook de Make.com para registrar entrenamientos en una hoja de cálculo. El flujo:

```
Atleta → "Registrá mi sesión de hoy"
   ↓
LLM detecta intención y llama al tool
   ↓
POST https://hook.eu2.make.com/<TU-WEBHOOK-ID>
   ↓
Make.com → Google Sheets / Notion / Airtable
   ↓
Confirmación al atleta
```

Schema y setup en [`integrations/make_webhook/README.md`](./integrations/make_webhook/README.md).

---

## 🗺️ Roadmap

- [x] Sistema de prompts en español
- [x] Base de conocimiento de nutrición y entrenamiento
- [x] Integración con Make.com vía webhook
- [x] 100 ejercicios categorizados
- [ ] Versión en inglés del system prompt
- [ ] Dashboard web (Streamlit / Next.js) sobre la API de Claude
- [ ] Dataset de evals para medir calidad de los planes generados
- [ ] Modo "voice coach" con TTS para entrenamientos en vivo
- [ ] Adaptación a MMA y boxeo

---

## 📝 Licencia

MIT — ver [`LICENSE`](./LICENSE).

El contenido sobre periodización está basado en literatura pública de fuerza y acondicionamiento. Los archivos PDF de obras protegidas (libros de Saulo Ribeiro, Renzo Gracie, etc.) **no se incluyen en este repo** por respeto al copyright; cargá los tuyos en la sección de Knowledge si los tenés legalmente.

---

## 🙋 Sobre el autor

Proyecto desarrollado en Mallorca, España. Si pasás por la zona, pasate por el dojo de **BJJ Santanyí** 🥋.

¿Sugerencias o querés contribuir? Abrí un issue o un PR. Toda mejora es bienvenida.
