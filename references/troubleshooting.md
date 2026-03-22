# Troubleshooting

- **"google-genai not installed"**: Run `.venv/bin/pip install google-genai` from the skill directory.
- **"GEMINI_API_KEY not set"**: Ensure the 1Password app is running. Run `varlock load` to verify secret resolution.
- **Varlock validation fails**: Run `varlock load` to see which variables failed. The macOS Keychain item `op-agent-skills-token` must exist and the 1Password AI vault item must be accessible.
- **Video processing fails**: The video may be private, age-restricted, or too long. Try a different video to confirm the setup works.
- **Model not found**: Check available models at https://ai.google.dev/gemini-api/docs/models — update the `--model` flag or `GEMINI_MODEL` in `.env.schema` accordingly.
