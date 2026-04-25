# Integración con Google Apps Script

> Webhook directo a Google Sheets sin intermediarios. El LLM hace POST al endpoint del script y éste escribe o consulta la hoja en tiempo real.

---

## ¿Por qué Apps Script en lugar de Make.com?

| | Make.com | Apps Script |
|---|---|---|
| Costo | Gratis hasta 1 000 ops/mes | Gratis (cuota diaria de Google) |
| Dependencias | Cuenta en Make.com | Solo cuenta de Google |
| Control del código | No-code, caja negra | JavaScript, 100% tuyo |
| Latencia | ~300-500 ms | ~150-250 ms |
| Lógica custom | Limitada por módulos | Sin límites |

---

## Setup paso a paso

### 1. Crear el spreadsheet

1. Abrí [sheets.new](https://sheets.new) y creá una hoja nueva.
2. Copiá el **ID** de la URL (la parte entre `/d/` y `/edit`):
   ```
   https://docs.google.com/spreadsheets/d/ESTE-ES-EL-ID/edit
   ```

### 2. Crear el script

1. En el spreadsheet → **Extensiones → Apps Script**.
2. Borrá el contenido del editor y pegá el contenido de [`Code.gs`](./Code.gs).
3. En la primera variable, pegá tu ID:
   ```javascript
   var SPREADSHEET_ID = 'ESTE-ES-EL-ID';
   ```
4. **Guardá** (Ctrl+S).

### 3. Testear desde el editor

Antes de deployar, verificá que el script puede escribir en tu hoja:

1. En el dropdown de funciones, elegí **`testRegistro`** y hacé click en **▶ Ejecutar**.
2. En el panel **Registro de ejecución** deberías ver:
   ```json
   {"ok":true,"mensaje":"Sesión registrada correctamente."}
   ```
3. Abrí el spreadsheet — la hoja `Entrenamientos` se creó sola con cabeceras en negrita.
4. Repetí con **`testConsulta`** para verificar que la consulta devuelve los registros.

> Si Google pide permisos, autorizalos — el script necesita acceso a Sheets.

### 4. Deployar como web app

1. **Deploy → New deployment**.
2. Tipo: **Web app**.
3. Configuración:
   - *Execute as*: **Me**.
   - *Who has access*: **Anyone** (para que el LLM pueda hacer POST).
4. Hacé click en **Deploy** y autorizá los permisos.
5. **Copiá la URL** resultante:
   ```
   https://script.google.com/macros/s/TU-DEPLOYMENT-ID/exec
   ```

> Cada vez que modifiques `Code.gs` tenés que hacer un **New deployment** (o *Manage deployments → Edit*) para que los cambios se apliquen al endpoint.

### 5. Configurar la Action en tu LLM

#### En ChatGPT Custom GPT

1. *Configure → Actions → Create new action*.
2. Pegá el contenido de [`openapi_schema.json`](./openapi_schema.json).
3. Reemplazá `TU-DEPLOYMENT-ID` en `servers[0].url`.
4. *Test* — mandá un POST de prueba.

#### En Claude Project (vía API)

Agregá la URL como variable de entorno en tu app:

```bash
APPS_SCRIPT_URL=https://script.google.com/macros/s/TU-DEPLOYMENT-ID/exec
```

---

## Estructura de la hoja generada

Si la hoja `Entrenamientos` no existe, el script la crea automáticamente:

| Fecha | Usuario | Ejercicio | Series | Reps | Carga (kg) | Duración (min) | Observaciones | Timestamp |
|-------|---------|-----------|--------|------|------------|----------------|---------------|-----------|
| 2026-04-25 | Ana BJJ | Sentadilla | 5 | 5 | 100 | 45 | ... | 2026-04-25T... |

---

## Payloads de referencia

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

### Respuesta (consulta)

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
    }
  ]
}
```

---

## Troubleshooting

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error 403 | Acceso no configurado como *Anyone* | Re-deploy con *Who has access: Anyone* |
| No escribe en el Sheet | `SPREADSHEET_ID` vacío o incorrecto | Verificá el ID en `Code.gs` |
| Error de autorización | Permisos no otorgados | Volvé a deployar y autorizá cuando Google lo pida |
| El LLM no llama al tool | URL desactualizada | Actualizá `servers[0].url` en el schema con el ID real |
| Cambios en el script no tienen efecto | Deployment viejo | Hacé *New deployment* o editá el existente |

---

## Privacidad y seguridad

- La URL del script es pública — no registres datos médicos sensibles.
- Para agregar autenticación básica, validá un header `X-Token` en `doPost` y configurá el mismo token en la Action del LLM.
- Si tenés muchos atletas, el campo `usuario` actúa como identificador; no hace falta una hoja por atleta.
