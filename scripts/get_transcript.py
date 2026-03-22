#!/usr/bin/env python3
"""Fetch a YouTube video transcript using the Google Gemini API."""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path(
    os.environ.get("TRANSCRIPT_OUTPUT_DIR", "~/CascadeProjects/semantechs/transcripts")
).expanduser()


def _extract_video_id(url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    match = re.search(r"(?:v=|youtu\.be/|/shorts/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else "unknown"


def get_transcript(youtube_url: str, model: str) -> str:
    """Send a YouTube URL to Gemini and return the transcript."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print(
            "Error: google-genai package not installed.\n"
            "Install it with: pip install google-genai",
            file=sys.stderr,
        )
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Error: GEMINI_API_KEY environment variable not set.\n"
            "Get a free key at https://ai.google.dev",
            file=sys.stderr,
        )
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_uri(
                file_uri=youtube_url,
                mime_type="video/*",
            ),
            "Provide a complete, verbatim transcript of this video. "
            "Output only the transcript text with no commentary, headers, or formatting.",
        ],
    )

    return response.text


def main():
    parser = argparse.ArgumentParser(description="Get YouTube video transcript via Gemini")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--model",
        default=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        help="Gemini model to use (default: gemini-2.5-flash or GEMINI_MODEL env var)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: auto-named in ~/CascadeProjects/semantechs/transcripts/)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of saving to file",
    )
    args = parser.parse_args()

    transcript = get_transcript(args.url, args.model)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    output = (
        f"---\n"
        f"source: {args.url}\n"
        f"model: {args.model}\n"
        f"date: {now}\n"
        f"---\n\n"
        f"{transcript}\n"
    )

    if args.stdout:
        print(output)
    else:
        if args.output:
            out_path = Path(args.output)
        else:
            video_id = _extract_video_id(args.url)
            date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
            filename = f"{date_str}_{video_id}.md"
            DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            out_path = DEFAULT_OUTPUT_DIR / filename

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"Transcript saved to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
