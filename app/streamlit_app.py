import streamlit as st
import anthropic
from pathlib import Path

BASE = Path(__file__).parent.parent


def load_text(rel_path: str) -> str:
    return (BASE / rel_path).read_text(encoding="utf-8")


@st.cache_data
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


def main():
    st.set_page_config(page_title="GrappleCoach", page_icon="🥋", layout="centered")
    st.title("GrappleCoach")
    st.caption("Coach virtual para BJJ y Grappling — powered by Claude")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    client = anthropic.Anthropic()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribí tu pregunta o contame tu objetivo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""
            with client.messages.stream(
                model="claude-opus-4-7",
                max_tokens=2048,
                system=get_system_prompt(),
                messages=st.session_state.messages,
            ) as stream:
                for text in stream.text_stream:
                    full_reply += text
                    placeholder.markdown(full_reply + "▌")
            placeholder.markdown(full_reply)

        st.session_state.messages.append({"role": "assistant", "content": full_reply})

    if st.session_state.messages:
        if st.button("Nueva sesión", type="secondary"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
