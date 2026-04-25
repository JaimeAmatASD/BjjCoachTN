# Changelog

Todos los cambios relevantes de este proyecto se documentan acá. El formato sigue [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) y el versionado sigue [Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026-04-25

### Cambiado
- 🔁 **Reestructuración completa del proyecto** para portfolio público en GitHub.
- 🌐 **Hecho model-agnostic** — ahora se puede desplegar en ChatGPT Custom GPT, Claude Projects, o vía API directa.
- 📁 Renombrado de archivos a inglés y organización por carpetas (`prompts/`, `knowledge/`, `integrations/`, `docs/`).
- ✏️ Limpieza de typos del system prompt original (acondicionaor → acondicionador, ves → vez, etc.).
- 📝 Eliminación de referencias a sitios placeholder (`www.linksuplentos.com`, `www.tussuplementos.com`).

### Agregado
- 🏗️ Diagrama de arquitectura del sistema en el README.
- 📚 Documentación técnica en `docs/` (architecture, deployment, customization).
- 💡 Ejemplos de conversación en `examples/conversation_examples.md`.
- 🔌 Schema OpenAPI documentado para la integración con Make.com.
- 🆔 Badges de estado, licencia y compatibilidad en el README.
- 📜 Licencia MIT.

### Quitado
- 🚫 Archivos PDF protegidos por copyright (libros de Saulo Ribeiro, Renzo Gracie, etc.) que estaban cargados en la versión privada del Custom GPT.

---

## [1.3.0] — Anterior (versión privada como Custom GPT)

### Agregado
- Ampliación de `links.md` con fuentes adicionales sobre nutrición y BJJ.
- Mejora de la guía de uso con ejemplos prácticos.

---

## [1.2.0] — Anterior (versión privada como Custom GPT)

### Agregado
- Opción de exportar tablas personalizadas.
- Recomendaciones de progresión basadas en %RM.
- Tests de progreso en fuerza máxima, resistencia y movilidad.

---

## [1.1.0] — Anterior (versión privada como Custom GPT)

### Agregado
- Columna de micronutrientes en tablas de nutrición.
- Tabla detallada de suplementos con dosis y horarios.
- Directrices para personalizar rutinas por nivel.
- Sección de movilidad y recuperación.

---

## [1.0.0] — Lanzamiento inicial

### Agregado
- Primera versión del Custom GPT con generación de planes de entrenamiento y nutrición.
- Exportación de planes en formato Excel.
- Knowledge base inicial con `Modelos.md`, `Tablas_de_comidas.md`, `Fundamentos_Entrenamiento_Fisico.md`, `Ejercicios_Lista.md`.
- Integración con webhook de Make.com para registrar progreso.

---

## Próximas versiones

### [2.1.0] — Planeada
- 🌍 Versión en inglés del system prompt.
- 🧪 Suite de evals para medir consistencia de los planes generados.
- 🥊 Adaptación a MMA y boxeo en `docs/customization.md`.

### [3.0.0] — Roadmap a largo plazo
- 🖥️ Dashboard web con Streamlit o Next.js sobre la API de Claude.
- 🎙️ Modo "voice coach" con TTS para entrenamientos en vivo.
