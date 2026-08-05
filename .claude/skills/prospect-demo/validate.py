#!/usr/bin/env python3
"""Validate a Leadlock voice agent before and after it goes live.

Two commands, no dependencies, no API key needed for either.

  # BEFORE you POST: does the prompt hold up for the model you are targeting?
  python3 validate.py prompt my-prompt.md --model grok-voice-think-fast-2.0

  # AFTER a test call: what went wrong, and which prompt line caused it?
  python3 validate.py call transcript.txt --prompt my-prompt.md

Exit 0 clean, 1 problems found, 2 bad input.

Why this exists: written guidance gets skipped under time pressure. Every rule
in the skill body was violated at least once while building the agent these
checks came from. The checks are the part that held.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

try:
    from voice_prompt_lint import (
        DEFAULT_PROFILE, FAIL, PROFILES, estimate_tokens, format_report, lint, summarize,
    )
    from voice_transcript_audit import (
        attach_causes, audit, format_report as format_audit, parse_transcript,
    )
except ImportError as e:  # noqa: BLE001
    print(f"validate.py: could not import the checkers next to this file: {e}",
          file=sys.stderr)
    sys.exit(2)


def profile_for_model(model: str | None) -> str:
    if model and "think-fast" in model:
        return "think-fast"
    if model:
        return "gpt-realtime"
    return DEFAULT_PROFILE


def cmd_prompt(args) -> int:
    f = Path(args.path)
    if not f.exists():
        print(f"validate.py: no such file: {f}", file=sys.stderr)
        return 2
    text = f.read_text()
    profile = args.profile or profile_for_model(args.model)
    findings = lint(text, greeting=args.greeting, profile=profile)
    fails, _ = summarize(findings)
    label = f"{f.name} ({profile}"
    label += f", {args.model})" if args.model else ")"
    print(format_report(findings, path=label, tokens=estimate_tokens(text)))
    if fails:
        print("\n  Do not POST this prompt until the FAILs are gone.")
    return 1 if fails else 0


def cmd_call(args) -> int:
    f = Path(args.path)
    if not f.exists():
        print(f"validate.py: no such file: {f}", file=sys.stderr)
        return 2
    text = f.read_text()
    prompt = None
    if args.prompt:
        pf = Path(args.prompt)
        if not pf.exists():
            print(f"validate.py: no such prompt file: {pf}", file=sys.stderr)
            return 2
        prompt = pf.read_text()

    if not parse_transcript(text):
        print("validate.py: no speaker-labelled turns found. Expected lines like\n"
              "  Agent: ...\n  Caller: ...", file=sys.stderr)
        return 2

    issues = attach_causes(audit(text, prompt=prompt), prompt)
    print(format_audit(issues, path=f.name, have_prompt=bool(prompt)))
    if issues and not prompt:
        print("\n  Re-run with --prompt to see which prompt line caused each one.")
    return 1 if issues else 0


def main() -> int:
    p = argparse.ArgumentParser(
        prog="validate.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("prompt", help="lint a system prompt before POSTing it")
    a.add_argument("path")
    a.add_argument("--model", help="the agent's xai_voice_model; picks the profile")
    a.add_argument("--profile", choices=sorted(PROFILES), help="override the profile")
    a.add_argument("--greeting", help="the configured greeting, checked for conflicts")
    a.set_defaults(func=cmd_prompt)

    b = sub.add_parser("call", help="audit a call transcript after a test call")
    b.add_argument("path")
    b.add_argument("--prompt", help="the system prompt, to name the causing lines")
    b.set_defaults(func=cmd_call)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
