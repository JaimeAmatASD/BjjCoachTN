# Integración con Make.com

> Este módulo permite que GrappleCoach **persista los entrenamientos del atleta** en una hoja de cálculo (o cualquier otro destino que soporte Make.com) mediante un webhook.

---

## ¿Por qué Make.com?

Make.com (ex-Integromat) actúa como **integration layer**:

- 🔌 Recibe el POST del LLM y lo enruta a donde quieras (Sheets, Notion, Airtable, DB).
- 💸 Tiene plan gratuito generoso (1000 operaciones/mes).
- 🛠️ No-code — un atleta puede modificar el destino sin tocar código.
- 🔐 Mantiene las credenciales de la DB fuera del LLM.

Alternativas equivalentes: **Zapier**, **n8n** (self-hosted), **Pipedream**.

---

## Setup paso a paso

### 1. Crear el escenario en Make.com

1. Entrá a [make.com](https://make.com) y registrate (gratis).
2. *Create a new scenario*.
3. Buscá el módulo **"Custom webhook"** y agregalo como primer paso.
4. *Add* → *Custom webhook* → dale un nombre (`grapplecoach-webhook`).
5. **Copiá la URL** que te genera. Tendrá la forma:

   ```
   https://hook.eu2.make.com/abc123def456ghi789...
   ```

### 2. Agregar el destino

Después del webhook, conectá el módulo del destino que prefieras:

#### Opción A: Google Sheets

1. *Add module* → **Google Sheets** → *Add a row*.
2. Conectá tu cuenta de Google.
3. Elegí el spreadsheet y la hoja donde guardar los registros.
4. Mapeá los campos del webhook a las columnas:

   | Columna del Sheet | Campo del webhook |
   |-------------------|-------------------|
   | A: Fecha | `{{1.fecha}}` |
   | B: Usuario | `{{1.usuario}}` |
   | C: Ejercicio | `{{1.ejercicio}}` |
   | D: Series | `{{1.series}}` |
   | E: Reps | `{{1.repeticiones}}` |
   | F: Carga (kg) | `{{1.carga_kg}}` |
   | G: Duración (min) | `{{1.duracion_min}}` |
   | H: Observaciones | `{{1.observaciones}}` |

#### Opción B: Notion

1. *Add module* → **Notion** → *Create a database item*.
2. Conectá tu workspace.
3. Mapeá los campos a las propiedades de la base.

#### Opción C: Airtable / Supabase / Postgres

Análogo. Make.com tiene módulos para todos.

### 3. Manejar el modo "consulta"

Para que el atleta pueda consultar su historial, agregá un router después del webhook:

```
Webhook
   ├─► [Filter: modo = "registro"] ──► Google Sheets: Add row
   └─► [Filter: modo = "consulta"]──► Google Sheets: Search rows
                                          │
                                          └─► Webhook response
```

### 4. Activar el escenario

- Dale al toggle de *"On"* arriba a la derecha.
- Make.com te dirá *"Listening for new webhook"*.

### 5. Configurar la Action en tu LLM

#### En ChatGPT Custom GPT

1. En *Configure* → *Actions* → *Create new action*.
2. *Import from URL* o pegá manualmente el contenido de [`openapi_schema.json`](./openapi_schema.json).
3. Reemplazá la URL del servidor (`servers[0].url`) por **tu URL de Make.com**.
4. *Test* — mandá un POST de prueba.

#### Vía API directa

Pegá la URL en tu variable de entorno `MAKE_WEBHOOK_URL` y usala en el handler del tool call (ver [`docs/deployment.md`](../../docs/deployment.md)).

---

## Estructura del payload

### Registro

```json
{
  "modo": "registro",
  "usuario": "Ana BJJ",
  "fecha": "2026-04-25",
  "ejercicio": "Sentadilla trasera",
  "series": 5,
  "repeticiones": 5,
  "carga_kg": 100,
  "duracion_min": 45,
  "observaciones": "Última serie con buena ejecución"
}
```

### Consulta

```json
{
  "modo": "consulta",
  "usuario": "Ana BJJ",
  "ejercicio": "Sentadilla trasera",
  "rango_dias": 30
}
```

### Respuesta esperada del webhook (consulta)

```json
{
  "ok": true,
  "registros": [
    {
      "fecha": "2026-04-20",
      "ejercicio": "Sentadilla trasera",
      "series": 5,
      "repeticiones": 5,
      "carga_kg": 95
    },
    {
      "fecha": "2026-04-13",
      "ejercicio": "Sentadilla trasera",
      "series": 5,
      "repeticiones": 5,
      "carga_kg": 92.5
    }
  ]
}
```

---

## Troubleshooting

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Webhook no recibe nada | URL incorrecta en la Action | Verificá que coincida exactamente con la de Make.com |
| Make.com responde 200 pero no escribe en el Sheet | Permisos del módulo de Sheets | Reconectá la cuenta de Google |
| El asistente no llama al webhook | Faltan campos obligatorios | Revisá `prompts/actions_prompt.md` — los campos requeridos |
| Error CORS al testear desde el browser | Make.com no responde con CORS headers | Hacé el test desde el LLM, no desde una página web local |

---

## Privacidad y seguridad

- 🔒 **No pongas datos médicos** en este sistema (lesiones graves, condiciones específicas). Los webhooks de Make.com no son una HIPAA-compliant DB.
- 🔑 **No expongas la URL del webhook** públicamente — cualquiera con la URL puede escribir.
- 📊 **Si tenés muchos atletas**, considerá agregar autenticación (header con token compartido).
