from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

from agents.research_agent import ResearchAgent
from agents.story_agent import generate_story


app = typer.Typer(add_completion=False)


def _validate_length(value: str) -> str:
    allowed = {"short", "medium", "long"}
    if value not in allowed:
        raise typer.BadParameter(f"length must be one of {sorted(allowed)}")
    return value


@app.command()
def main(
    name: Optional[str] = typer.Option(None, "--name", help="Famous person's name"),
    age: int = typer.Option(8, "--age", min=3, max=14, help="Target child age"),
    tone: str = typer.Option("uplifting", "--tone", help="Tone of the story"),
    length: str = typer.Option("short", "--length", callback=_validate_length, help="Story length"),
    output: Optional[Path] = typer.Option(None, "--output", help="Write story to this file"),
    model: Optional[str] = typer.Option(None, "--model", help="Override Gemini model"),
):
    if not name:
        name = Prompt.ask("Which famous person should the story be about?")

    print(Panel.fit(f"Researching: [bold]{name}[/bold]", title="Research Agent"))
    researcher = ResearchAgent()
    profile = researcher.research(name)
    profile_dict = profile.to_brief_dict()

    print(Panel.fit(json.dumps(profile_dict, indent=2), title="Factual context"))

    print(Panel.fit("Generating story with Gemini...", title="Story Agent"))
    try:
        story = generate_story(profile.name, age, tone, length, profile_dict, model=model)
    except Exception as e:
        print(f"[red]Failed to generate story: {e}[/red]")
        raise typer.Exit(code=1)

    if output:
        output.write_text(story, encoding="utf-8")
        print(Panel.fit(f"Story saved to {output}", title="Done"))
    else:
        print(Panel.fit(story, title=f"Story about {profile.name}"))


if __name__ == "__main__":
    app()

