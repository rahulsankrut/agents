## Kids' Inspirational Story Generator

Create child-friendly inspirational stories about famous personalities. The app:
- Asks for the name of a famous person
- Uses a research sub-agent (Wikipedia API) to gather factual context
- Uses Gemini to generate a simple, inspirational story tailored for kids

### Quick start

1) Python 3.9+

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Set your Gemini API key:

```bash
export GEMINI_API_KEY="YOUR_KEY_HERE"
```

Optionally set a specific Gemini model (default: `gemini-1.5-flash`):

```bash
export GEMINI_MODEL="gemini-1.5-pro"
```

4) Run:

```bash
python main.py --name "Marie Curie"
```

Or interactively:

```bash
python main.py
```

### CLI options

```bash
python main.py \
  --name "Nelson Mandela" \
  --age 8 \
  --tone uplifting \
  --length short \
  --output story_mandela.md
```

- `--name` (required if not provided interactively): famous personality
- `--age` (default 8): target child age
- `--tone` (default "uplifting"): tone hint
- `--length` (default "short"): one of `short`, `medium`, `long`
- `--output` (optional): path to save a markdown story

### How it works
- `agents/research_agent.py`: fetches a concise, fact-based profile from Wikipedia REST API
- `agents/story_agent.py`: sends a structured prompt to a Gemini model to create a child-friendly story

### Notes
- Research uses open Wikimedia endpoints—no key required
- Gemini generation requires `GEMINI_API_KEY`
- Stories are guided to be simple, positive, and age-appropriate

