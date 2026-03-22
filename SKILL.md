---
name: YouTube Transcript
description: This skill should be used when the user asks to "get a YouTube transcript", "transcribe a YouTube video", "get the transcript of this video", "transcribe this" with a YouTube URL, provides a YouTube or YouTube Shorts URL and wants its content transcribed, or mentions "youtube transcript" or "video transcript". Extracts verbatim transcripts from YouTube videos (including Shorts) using Google Gemini.
version: 0.1.0
---

# YouTube Transcript

Extract verbatim transcripts from YouTube videos (including Shorts) using the Google Gemini API. The transcript is returned with YAML frontmatter containing the source URL, model used, and timestamp.

`SKILL_DIR` refers to this skill's directory. All `varlock` commands must be run from `SKILL_DIR` (it reads `.env.schema` from the current directory).

## Prerequisites

- **Python 3.13 virtual environment**: The skill uses its own `.venv` (pyenv default is 3.7, too old). Set up once:
  ```bash
  cd "${SKILL_DIR}"
  /usr/local/bin/python3 -m venv .venv
  .venv/bin/pip install google-genai
  ```
- **Varlock + 1Password + macOS Keychain**: Secrets are resolved at runtime with no auth prompts. The chain is:
  macOS Keychain (`op-agent-skills-token`) → 1Password service account (AI vault, read-only) → `GEMINI_API_KEY` → Gemini API.
  The `.env.schema` in this skill directory defines all required variables — no `.env` files are used.
- **API key**: Stored in 1Password vault "AI" as item `gemini-api-key-transcript` (password field). Obtain a key at https://ai.google.dev

## Usage

Run the script from the skill directory via `varlock run` to securely inject secrets:

```bash
cd "${SKILL_DIR}" && varlock run -- .venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL"
```

### Options

| Flag | Description |
|---|---|
| `--model MODEL` | Gemini model to use (default: `gemini-2.5-flash` or `GEMINI_MODEL` env var) |
| `-o FILE`, `--output FILE` | Save transcript to a specific file path |
| `--stdout` | Print transcript to stdout instead of saving to file |

### Default output behavior

When neither `--output` nor `--stdout` is specified, the transcript is auto-saved to:
```
~/CascadeProjects/semantechs/transcripts/YYYYMMDD_VIDEOID.md
```
The output directory is configurable via the `TRANSCRIPT_OUTPUT_DIR` env var in `.env.schema`.

### Examples

Auto-save transcript to default directory:
```bash
cd "${SKILL_DIR}" && varlock run -- .venv/bin/python3 scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Print transcript to stdout:
```bash
cd "${SKILL_DIR}" && varlock run -- .venv/bin/python3 scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --stdout
```

## Output Format

The script outputs the transcript with YAML frontmatter:

```markdown
---
source: https://www.youtube.com/watch?v=...
model: gemini-2.5-flash
date: 2026-03-22T12:00:00Z
---

[Verbatim transcript text here]
```

## Workflow

When a user provides a YouTube URL and asks for a transcript:

1. `cd "${SKILL_DIR}"` — all commands must run from the skill directory.
2. Run `varlock load --quiet` to validate that all required secrets can be resolved. If validation fails, ensure the 1Password app is running (Keychain access requires no auth prompt).
3. Verify the `.venv` exists and `google-genai` is installed. If not, set it up per the Prerequisites section.
4. Run the script via `varlock run` with the provided URL, using the `.venv` Python interpreter.
5. If the user specified an output file, use `-o`. If they want console output, use `--stdout`. Otherwise, let it auto-save to the default transcript directory.
6. If the API call fails, see `references/troubleshooting.md`.

**Important**: Never read or print secret values. Always use `varlock run` to inject secrets into the process environment. Secrets are resolved from 1Password via macOS Keychain at runtime — nothing sensitive is stored on disk.

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common errors and fixes.
