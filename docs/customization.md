# Personalización

GrappleCoach está diseñado para BJJ y grappling, pero la arquitectura permite adaptarlo a otros deportes con relativa facilidad. Esta guía explica qué tocar y qué dejar quieto.

---

## Adaptar a otro deporte de combate

### A MMA

Cambios necesarios:

- **`prompts/system_prompt.md`**
  - Sección 1: cambiar identidad a *"coach de MMA"*.
  - Sección 2.4: agregar opciones de estilo (striker, grappler, MMA híbrido).
- **`knowledge/training/exercises_library.md`**
  - Agregar categoría de **striking** (saco, pads, footwork, defensa).
  - Mantener todas las categorías de fuerza, potencia, cardio.
- **`knowledge/training/training_fundamentals.md`**
  - Ajustar la periodización a calendarios típicos de MMA (camp de 8-12 semanas).

### A boxeo

Cambios más profundos:

- **`prompts/system_prompt.md`**
  - Sección 4.1: el énfasis pasa a **velocidad de manos**, footwork y resistencia anaeróbica de alta intensidad.
- **`knowledge/training/exercises_library.md`**
  - Reemplazar categorías de grappling (técnicos en pie/par terre, drills) por **shadow boxing**, **bag work**, **mitt work**, **sparring drills**.
  - Mantener fuerza, potencia, cardio, core, agarre (para clinch).
- **`knowledge/training/training_fundamentals.md`**
  - Reescribir basándose en literatura específica de boxeo (Ross Enamait, Charlie Francis aplicado a combate).

### A judo

Más fácil — la base de grappling sirve casi entera:

- **`prompts/system_prompt.md`**
  - Sección 1: cambiar identidad a *"coach de judo"*.
  - Sección 2.4: agregar referencias a kumi-kata y nage-waza.
- **`knowledge/training/exercises_library.md`**
  - Categoría 1 (técnicos en pie) cambia ligeramente — agregar *uchikomi*, *tsugi-ashi*, etc.
  - Categoría 2 (par terre) se renombra a **ne-waza**.
- **`knowledge/training/training_fundamentals.md`**
  - Mantener mayormente igual — los principios de Prilepin y la periodización por temporada aplican.

---

## Qué editar y qué no tocar

| Componente | Editable | Recomendación |
|------------|----------|---------------|
| Tono y estilo del coach | ✅ | Cambialo libremente en sección 3 del system prompt. |
| Lista de ejercicios | ✅ | Agregá, sacá o reescribí según el deporte. |
| Modelos nutricionales | ✅ | La cetogénica está intencionalmente fuera. Justificalo si la querés sumar. |
| Preguntas de la entrevista inicial | ✅ | Mantené el principio de *"una pregunta por turno"* — es lo que hace la experiencia única. |
| Periodización base | ⚠️ | Requiere conocer la temporada del deporte. No lo toques sin entender por qué. |
| Flujo de Actions/webhook | ⚠️ | El schema es agnóstico. Podés mantenerlo casi igual. |
| Reglas de seguridad (sección 9 del system prompt) | ❌ | No quites. Son las que evitan que el asistente dé consejo médico fuera de su rol. |

---

## Adaptar el idioma

El proyecto está en español rioplatense / neutro. Para portar a otro idioma:

1. Traducí `prompts/system_prompt.md`.
2. Traducí `prompts/conversation_starters.md`.
3. La knowledge base se puede traducir o dejar en español — el LLM la entiende igual.
4. Si querés que el asistente responda **siempre en un idioma específico**, agregá una línea explícita al system prompt:
   > *"Respondé siempre en inglés, sin importar el idioma en que te escriba el atleta."*

---

## Adaptar el tono

El system prompt actual está calibrado para un tono **profesional pero cercano**, evitando ser forzadamente cool. Si querés cambiarlo:

### Más formal

En sección 3, reemplazá:

```
- Tono profesional pero cercano
+ Tono profesional y respetuoso, tratando al atleta de "usted".
+ Sin emoticones ni lenguaje coloquial.
```

### Más motivacional

```
- Tono profesional pero cercano
+ Tono motivacional y enérgico, como un coach de deportes de élite.
+ Usá frases cortas y declarativas. Felicitá los avances.
```

### Más técnico/científico

```
- Tono profesional pero cercano
+ Tono académico. Citá literatura cuando sea relevante.
+ Explicá el "por qué" fisiológico detrás de cada recomendación.
```

---

## Agregar nuevas funciones

### Generación de meal plans con imágenes

Si tu plataforma soporta generación de imágenes (DALL-E, Imagen):

1. Agregá un tool `generar_imagen_receta` al system prompt.
2. Que el asistente lo invoque después de proponer una receta.
3. La imagen se genera y se muestra junto al texto.

### Generación de videos de ejecución

Más complejo. Requiere:

1. Una librería de videos pregrabados de cada ejercicio.
2. El asistente referencia el video por ID cuando lo menciona.
3. La interfaz muestra el video embebido.

### Conexión con wearables

Para pulling automático de datos:

1. Integración con APIs de Whoop, Garmin, Apple Health.
2. El asistente consulta métricas (HRV, sueño, recovery score) antes de recomendar la sesión del día.
3. Ajusta intensidad si la recovery está baja.

---

## Mantener actualizada la knowledge base

Cada 3-6 meses revisá:

- ¿Hay nueva literatura relevante? (Buscá en `knowledge/resources/trusted_sources.md`).
- ¿Cambió la disponibilidad de algún suplemento o se descubrió algún efecto adverso?
- ¿Hay nuevas modalidades competitivas? (ADCC tiene nuevas reglas, IBJJF cambia formato, etc.).

Documentá los cambios en `CHANGELOG.md`.
