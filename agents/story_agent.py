from __future__ import annotations

import os
from typing import Optional

import google.generativeai as genai


DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


def _configure() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)


def build_prompt(name: str, age: int, tone: str, length: str, research_context: dict) -> str:
    length_instructions = {
        "short": "200-300 words",
        "medium": "400-600 words",
        "long": "700-1000 words",
    }.get(length, "200-300 words")

    facts = []
    for key in ["description", "birth_date", "death_date", "extract", "url"]:
        value = research_context.get(key)
        if value:
            facts.append(f"- {key}: {value}")
    facts_block = "\n".join(facts) if facts else "- No facts available."

    return (
        "You are a children’s storyteller. Write an inspirational, fact-grounded story for a child.\n"
        f"Target age: {age}. Tone: {tone}. Length: {length_instructions}.\n"
        "Keep the language simple and warm, avoid complex dates and heavy details.\n"
        "Include a gentle moral at the end, and ensure accuracy based on the facts provided.\n"
        f"Famous person: {name}.\n"
        "Facts (source material):\n"
        f"{facts_block}\n"
        "Story:"
    )


def generate_story(name: str, age: int, tone: str, length: str, research_context: dict, model: Optional[str] = None) -> str:
    _configure()
    prompt = build_prompt(name, age, tone, length, research_context)
    model_name = model or DEFAULT_MODEL

    # Using the text-only generate_content for simplicity
    gmodel = genai.GenerativeModel(model_name)
    response = gmodel.generate_content(prompt)
    if getattr(response, "prompt_feedback", None) and getattr(response.prompt_feedback, "block_reason", None):
        reason = response.prompt_feedback.block_reason
        raise RuntimeError(f"Model blocked the request: {reason}")
    text = getattr(response, "text", None)
    if not text:
        # Try to assemble from candidates if not directly available
        try:
            text = "\n\n".join([c.content.parts[0].text for c in response.candidates if c.content.parts])
        except Exception:
            text = ""
    return text.strip()

