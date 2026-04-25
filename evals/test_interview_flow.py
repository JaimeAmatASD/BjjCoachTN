"""
Evals that verify GrappleCoach follows the 6-question interview protocol
before generating any training plan.

Run with:  pytest evals/test_interview_flow.py -v
Requires:  ANTHROPIC_API_KEY env var
"""

import pytest
import anthropic
from pathlib import Path

BASE = Path(__file__).parent.parent


def load_text(rel_path: str) -> str:
    return (BASE / rel_path).read_text(encoding="utf-8")


def get_system_prompt() -> str:
    system = load_text("prompts/system_prompt.md")
    knowledge_files = [
        "knowledge/training/training_fundamentals.md",
        "knowledge/training/exercises_library.md",
        "knowledge/nutrition/nutrition_models.md",
        "knowledge/nutrition/food_tables.md",
        "knowledge/resources/trusted_sources.md",
    ]
    knowledge = "\n\n---\n\n".join(load_text(f) for f in knowledge_files)
    return f"{system}\n\n# BASE DE CONOCIMIENTO\n\n{knowledge}"


@pytest.fixture(scope="module")
def client():
    return anthropic.Anthropic()


@pytest.fixture(scope="module")
def system_prompt():
    return get_system_prompt()


def chat(client: anthropic.Anthropic, system: str, messages: list) -> str:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=system,
        messages=messages,
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_opening_asks_one_question_at_a_time(client, system_prompt):
    """Opening response must ask exactly one question, not a barrage."""
    messages = [{"role": "user", "content": "Hola, quiero prepararme para un torneo"}]
    reply = chat(client, system_prompt, messages)

    question_marks = reply.count("?")
    assert question_marks >= 1, "Debe hacer al menos una pregunta al abrir"
    assert question_marks <= 3, (
        f"Preguntó demasiadas cosas a la vez ({question_marks} '?'). "
        f"Respuesta: {reply[:300]}"
    )


def test_first_question_is_about_personal_data(client, system_prompt):
    """First question should ask for age, weight, or experience level."""
    messages = [{"role": "user", "content": "Quiero mejorar mi condición para grappling"}]
    reply = chat(client, system_prompt, messages)

    personal_keywords = ["edad", "peso", "nivel", "experiencia", "años", "kg"]
    has_personal = any(kw in reply.lower() for kw in personal_keywords)
    assert has_personal, (
        "La primera pregunta debería ser sobre datos personales. "
        f"Respuesta: {reply[:300]}"
    )


def test_no_plan_without_interview(client, system_prompt):
    """Sending just a goal should NOT produce a full training plan."""
    messages = [{"role": "user", "content": "Dame un plan de entrenamiento para BJJ"}]
    reply = chat(client, system_prompt, messages)

    plan_triggers = ["semana 1", "lunes:", "plan global", "macros:", "periodización:"]
    has_plan = any(trigger.lower() in reply.lower() for trigger in plan_triggers)
    assert not has_plan, (
        "Generó un plan sin completar la entrevista. "
        f"Respuesta: {reply[:300]}"
    )


def test_second_question_asked_one_at_a_time(client, system_prompt):
    """After Q1 is answered, should ask Q2 alone — not Q3, Q4 together."""
    messages = [
        {"role": "user", "content": "Hola, quiero prepararme para competir en BJJ"},
        {
            "role": "assistant",
            "content": "¿Cuántos años tenés, cuál es tu peso actual y cómo describirías tu nivel de experiencia?",
        },
        {"role": "user", "content": "28 años, 80 kg, nivel intermedio, llevo 3 años"},
    ]
    reply = chat(client, system_prompt, messages)

    question_marks = reply.count("?")
    assert question_marks <= 2, (
        f"Preguntó varias cosas a la vez en Q2 ({question_marks} '?'). "
        f"Respuesta: {reply[:300]}"
    )


def test_no_plan_after_three_questions_answered(client, system_prompt):
    """Even with 3 questions answered, no plan should be generated yet."""
    messages = [
        {"role": "user", "content": "Hola, quiero prepararme para competir"},
        {"role": "assistant", "content": "¿Cuántos años tenés, peso y nivel?"},
        {"role": "user", "content": "28 años, 80 kg, intermedio"},
        {"role": "assistant", "content": "¿Cuáles son tus objetivos principales?"},
        {"role": "user", "content": "Mejorar fuerza y explosividad"},
        {"role": "assistant", "content": "¿Tenés fecha de torneo y es Gi o No-Gi?"},
        {"role": "user", "content": "Torneo en 8 semanas, No-Gi"},
    ]
    reply = chat(client, system_prompt, messages)

    plan_triggers = ["semana 1", "lunes:", "plan global", "día 1:", "fase 1:"]
    has_plan = any(trigger.lower() in reply.lower() for trigger in plan_triggers)
    assert not has_plan, (
        "Generó un plan después de solo 3 preguntas. "
        f"Respuesta: {reply[:300]}"
    )


def test_generates_plan_after_full_interview(client, system_prompt):
    """After all 6 questions are answered, a real plan should appear."""
    messages = [
        {"role": "user", "content": "Hola, quiero prepararme para un torneo"},
        {"role": "assistant", "content": "¿Cuántos años tenés, peso y nivel?"},
        {"role": "user", "content": "28 años, 80 kg, intermedio, 3 años en BJJ"},
        {"role": "assistant", "content": "¿Cuáles son tus objetivos principales?"},
        {"role": "user", "content": "Fuerza y explosividad, algo de cardio"},
        {"role": "assistant", "content": "¿Fecha del torneo y Gi o No-Gi?"},
        {"role": "user", "content": "Torneo en 8 semanas, No-Gi"},
        {"role": "assistant", "content": "¿Qué estilo de grappling practicás?"},
        {"role": "user", "content": "BJJ principalmente, algo de lucha"},
        {"role": "assistant", "content": "¿Cuántas sesiones semanales y cuánto duran?"},
        {"role": "user", "content": "4 sesiones por semana, 90 minutos cada una"},
        {
            "role": "assistant",
            "content": "¿Algo más que quieras contarme? ¿Experiencia anterior, feedback de tu profe?",
        },
        {
            "role": "user",
            "content": (
                "Mi profe dice que me falta explosión en entradas a piernas. "
                "Perdí por cansancio en semifinals hace 3 meses."
            ),
        },
    ]
    reply = chat(client, system_prompt, messages)

    plan_keywords = ["semana", "plan", "ejercicio", "sesión", "nutrición", "entrenamiento"]
    has_plan = any(kw.lower() in reply.lower() for kw in plan_keywords)
    assert has_plan, (
        "No generó ningún plan después de completar las 6 preguntas. "
        f"Respuesta: {reply[:300]}"
    )
