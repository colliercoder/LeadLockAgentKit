#!/usr/bin/env python3
"""PreToolUse guard: keeps your API keys out of the chat, out of files, and out of git.

Claude Code runs this before every Bash, Read, Write and Edit call (see
.claude/settings.json). It reads the tool call as JSON on stdin and either
allows it (exit 0) or blocks it (exit 2, with the reason on stderr, which
Claude sees and acts on).

It blocks:
  1. Staging secret files: `git add .env` (or any gitignored secret file the kit
     names), and `git add -f` / `--force`, which bypasses .gitignore.
  2. Committing a live key: `git commit` when the staged diff contains one.
  3. Printing secrets into the transcript: cat/head/tail/less/grep/... on `.env`,
     the Read tool on `.env`, and echo/printf of a key variable.
  4. Pasting a live key into a command, or writing one into any file except `.env`.

Python 3 standard library only. Fails open (allows the call) if its own input
is unreadable, so a bug here never locks you out of Claude Code.
"""
import json
import re
import subprocess
import sys

# Real-looking secrets. Placeholders like sk_live_paste_your_key_here or
# pit-paste-your-token-here deliberately do not match.
SECRET_PATTERNS = [
    (re.compile(r"sk_live_[A-Za-z0-9]{20,}"), "a Leadlock API key (sk_live_...)"),
    (re.compile(r"pit-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"),
     "a GoHighLevel Private Integration Token (pit-...)"),
    (re.compile(r"\bkey_[A-Za-z0-9]{24,}"), "a Retell API key (key_...)"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "a JWT, such as an n8n API key (eyJ...)"),
]

# Files that hold real credentials. All are gitignored; these guards stop them
# being forced in or printed.
SECRET_FILES = re.compile(
    r"(^|[\s/'\"])(\.env(\.local)?|headers\.json|values\.json|my-a2p-answers\.md)(?=$|[\s'\";|&)])"
)
ENV_FILE = re.compile(r"(^|[\s/'\"=<])\.env(\.local)?(?=$|[\s'\";|&)])")
READERS = r"(cat|head|tail|less|more|bat|grep|egrep|rg|sed|awk|cut|sort|strings|xxd|od|nl|tac|open)"
KEY_VARS = r"\$\{?[A-Z_]*(API_KEY|AUTH_TOKEN|_AUTH|_PIT|SECRET|TOKEN)[A-Z_]*\}?"


def block(reason: str) -> None:
    sys.stderr.write(
        "Blocked by the kit's secret guard (.claude/hooks/guard_secrets.py): "
        + reason
        + "\n"
    )
    sys.exit(2)


def find_secret(text: str):
    for pattern, label in SECRET_PATTERNS:
        if pattern.search(text or ""):
            return label
    return None


def check_bash(cmd: str) -> None:
    # Split on shell separators so each sub-command is judged on its own.
    parts = [p.strip() for p in re.split(r"&&|\|\||;|\n", cmd) if p.strip()]
    for part in parts:
        if re.match(r"^git\s+add\b", part):
            if re.search(r"\s(-f|--force)\b", part):
                block("`git add --force` bypasses .gitignore, which is what keeps .env "
                      "and other credential files out of this public repo. Stage files "
                      "without --force.")
            if SECRET_FILES.search(part[len("git add"):]):
                block("that file holds real credentials and must never be committed. "
                      ".env is gitignored on purpose; commit .env.example instead.")
        if re.match(r"^git\s+commit\b", part):
            try:
                staged = subprocess.run(
                    ["git", "diff", "--cached", "-U0"],
                    capture_output=True, text=True, timeout=10,
                ).stdout
            except Exception:
                staged = ""
            added = "\n".join(l for l in staged.splitlines() if l.startswith("+"))
            label = find_secret(added)
            if label:
                block(f"the staged changes contain {label}. Remove it from the file "
                      "(keep real keys only in .env), re-stage, then commit.")
        # Printing .env (or another credential file) into the transcript.
        first = part.split("|")[0]
        if re.match(rf"^\s*(sudo\s+)?{READERS}\b", first) and ENV_FILE.search(first):
            block("printing .env would show your keys in the chat (and on screen). "
                  "Parse it in Python and print only masked values, e.g. "
                  "key[:6] + '...' + key[-4:], or just whether each variable is set.")
        if re.match(r"^\s*(echo|printf)\b", part) and re.search(KEY_VARS, part):
            block("echoing a key variable prints the secret. Print whether it is set, "
                  "or a masked form, instead.")
    label = find_secret(cmd)
    if label:
        block(f"the command contains {label} pasted in plain text. Read it from .env "
              "inside the script instead, so the value never appears in the chat.")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # fail open on unreadable input
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}

    if tool == "Bash":
        check_bash(inp.get("command", ""))
    elif tool == "Read":
        path = inp.get("file_path", "")
        if re.search(r"(^|/)\.env(\.local)?$", path):
            block("reading .env would show your keys in the chat. To check a setting, "
                  "parse .env in Python and report set / not set, or a masked value.")
    elif tool in ("Write", "Edit", "MultiEdit"):
        path = inp.get("file_path", "")
        if re.search(r"(^|/)\.env(\.local)?$", path):
            sys.exit(0)  # .env is where real keys belong
        texts = [inp.get("content", ""), inp.get("new_string", "")]
        texts += [e.get("new_string", "") for e in inp.get("edits", []) or []]
        label = find_secret("\n".join(t for t in texts if t))
        if label:
            block(f"this would write {label} into {path or 'a file'}. Real keys live only "
                  "in .env (gitignored). Use a placeholder or read the key from .env.")
    sys.exit(0)


if __name__ == "__main__":
    main()
