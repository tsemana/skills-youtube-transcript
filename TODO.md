# YouTube Transcript Skill — Remaining Tasks

## Context

This skill fetches YouTube video transcripts using Google Gemini API. The full pipeline is built and end-to-end tested:

- **Script**: `scripts/get_transcript.py` — takes a YouTube URL, sends to Gemini, outputs transcript with YAML frontmatter
- **Secrets**: Varlock + 1Password service account (scoped to AI vault only) + macOS Keychain (no auth prompts)
- **Config**: `.env.schema` defines `OP_SERVICE_ACCOUNT_TOKEN`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `TRANSCRIPT_OUTPUT_DIR`
- **Output**: Defaults to `~/CascadeProjects/semantechs/transcripts/YYYYMMDD_VIDEOID.md`, overridable with `-o` or `--stdout`
- **Python**: Uses `.venv` in skill directory with Python 3.13 (`/usr/local/bin/python3`); pyenv default is 3.7 which is too old

### Secret chain
macOS Keychain (`op-agent-skills-token`) → 1Password service account (AI vault, read-only) → `GEMINI_API_KEY` → Gemini API

### 1Password details
Sensitive identifiers stored in Claude memory (`project_1password_details.md`), not in this file.
- Service account token stored in: Private vault as `agent-skills-service-account-token`
- Gemini key stored in: AI vault as `gemini-api-key-transcript` (password field)

---

## Completed

- [x] Update SKILL.md to reflect current state (Keychain secret chain, .venv, --stdout, auto-naming, no .env files)
- [x] Add `.gitignore` with `.venv/` entry
- [x] Run skill-reviewer agent — addressed findings (SKILL_DIR docs, working dir, Shorts trigger, progressive disclosure)
- [x] Save memories for future conversations (secret management, skill structure, 1Password details, no-plaintext feedback)
- [x] Move troubleshooting to `references/troubleshooting.md`
- [x] Remove sensitive 1Password identifiers from this file (moved to Claude memory)
