"""Deterministic linter for Leadlock voice-agent system prompts.

Encodes the realtime speech-to-speech prompting rules that Big Dawg keeps
re-learning the hard way. Every check traces to a source:

- OpenAI realtime prompting guide (bullets over paragraphs, Variety section,
  short varied sample phrases rather than multi-turn transcripts)
- Alejo / Amplify Voice AI (under 2000 tokens, re-ask guard, split-message
  handling, avoid blanket always/never)
- Tommy Chryst / Rose AI (six-section anatomy, em dashes break voice agents,
  unfilled variables get spoken literally)
- e-2822 (speech markup is inert on our realtime stack and risks literal readout)

No LLM. Pure string analysis, so the same prompt always lints the same way.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict

FAIL = "FAIL"
WARN = "WARN"

# ~4 chars per token is the heuristic used across this repo's prompt work.
CHARS_PER_TOKEN = 4
TOKEN_BUDGET = 2000

EM_DASH = "—"

# Inert on realtime speech-to-speech and liable to be read aloud verbatim.
SPEECH_MARKUP = [
    "<break", "<emotion", "<whisper", "<soft",
    "[pause]", "[breath]", "[laughter]", "[laugh]", "[sigh]", "[giggle]",
]

# header keyword -> human name. A prompt must cover all of these.
REQUIRED_SECTIONS = {
    "role": ("role", "identity", "objective"),
    "personality": ("personality", "voice", "how you talk", "how you sound"),
    "context": ("context", "facts", "business"),
    "instructions": ("instruction", "rules", "communication", "guideline"),
    "stages": ("stage", "flow", "script", "sheet", "call flow"),
}
RECOMMENDED_SECTIONS = {
    "examples": ("example", "sample phrase"),
}

REASK_PATTERNS = [
    r"same thing twice", r"same data twice", r"same question twice",
    r"already told you", r"already answered", r"do not ask again",
    r"don't ask again", r"never ask for the same",
]
SPLIT_MESSAGE_PATTERNS = [
    r"unfinished", r"split into two", r"broken up", r"two messages",
    r"uh huh", r"mid-sentence",
]
VARIETY_PATTERNS = [
    r"do not repeat the same", r"don't repeat the same", r"vary your",
    r"vary these", r"vary the wording", r"same acknowledgement twice",
]

# Sections where absolutes are legitimate and expected.
ABSOLUTE_SAFE_HEADERS = ("guardrail", "reminder", "never", "hard rule", "boundaries")

# Only IMPERATIVE absolutes matter. "Never end the call with fields blank" is the
# failure mode; "always on the caller's side" is a style descriptor and is fine.
IMPERATIVE_ABSOLUTE_RE = re.compile(
    r"^\s*(?:[-*+]\s*|\d+[.)]\s*)?(?:\*\*)?\s*(never|always)\b"
    r"|\byou\s+(?:must|should)\s+(?:never|always)\b",
    re.I,
)

SPEAKER_TURN_RE = re.compile(r"^\s*>?\s*\*\*[A-Z][A-Za-z ]{1,20}:\*\*", re.M)
VARIABLE_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")
HEADER_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$", re.M)


@dataclass
class Finding:
    level: str
    code: str
    message: str
    line: int | None = None

    def as_dict(self) -> dict:
        return asdict(self)


def _lines(text: str) -> list[str]:
    return text.splitlines()


def _headers(text: str) -> list[tuple[int, str]]:
    """Return (line_number, header_text_lower) for every markdown header."""
    out = []
    for m in HEADER_RE.finditer(text):
        line = text[: m.start()].count("\n") + 1
        out.append((line, m.group(2).strip().lower()))
    return out


def _section_at(headers: list[tuple[int, str]], line: int) -> str:
    """The nearest header at or above `line`."""
    current = ""
    for hline, htext in headers:
        if hline <= line:
            current = htext
        else:
            break
    return current


def estimate_tokens(text: str) -> int:
    return len(text) // CHARS_PER_TOKEN


def lint(
    text: str,
    *,
    variable_defaults: dict | None = None,
    greeting: str | None = None,
) -> list[Finding]:
    """Return findings, most severe first. Empty list means clean."""
    findings: list[Finding] = []
    lines = _lines(text)
    headers = _headers(text)
    low = text.lower()

    # 1. Token budget.
    tokens = estimate_tokens(text)
    if tokens > TOKEN_BUDGET:
        findings.append(Finding(
            FAIL, "token-budget",
            f"{tokens} estimated tokens exceeds the {TOKEN_BUDGET} ceiling "
            f"({len(text)} chars). Realtime models lose instruction-following "
            f"on bloated prompts. Group fields into stages and cut prose.",
        ))

    # 2. Em dashes break voice agents.
    for i, line in enumerate(lines, 1):
        if EM_DASH in line:
            findings.append(Finding(
                FAIL, "em-dash",
                "Em dash (U+2014) makes voice agents sound wrong when spoken. "
                "Use a hyphen, a colon, or split the sentence.",
                line=i,
            ))

    # 3. Speech markup that this stack does not interpret.
    for i, line in enumerate(lines, 1):
        ll = line.lower()
        for tag in SPEECH_MARKUP:
            if tag in ll:
                findings.append(Finding(
                    FAIL, "speech-markup",
                    f"'{tag}' is inert on realtime speech-to-speech and risks "
                    f"being read aloud literally (see e-2822). Control pacing "
                    f"with vad_silence_duration_ms and xai_speaking_speed instead.",
                    line=i,
                ))
                break

    # 4. Required sections.
    header_blob = " | ".join(h for _, h in headers)
    for name, keywords in REQUIRED_SECTIONS.items():
        if not any(k in header_blob for k in keywords):
            findings.append(Finding(
                FAIL, "missing-section",
                f"No '{name}' section. The six-section anatomy is Role and "
                f"Objective / Personality / Context / Instructions / Stages / "
                f"Example interactions.",
            ))
    for name, keywords in RECOMMENDED_SECTIONS.items():
        if not any(k in header_blob for k in keywords):
            findings.append(Finding(
                WARN, "missing-section",
                f"No '{name}' section. Short varied sample phrases teach style "
                f"better than adjectives.",
            ))

    # 5. Unfilled dynamic variables get spoken out loud.
    defaults = {k.lower() for k in (variable_defaults or {}) if variable_defaults[k]}
    seen_vars: set[str] = set()
    for m in VARIABLE_RE.finditer(text):
        var = m.group(1)
        if var.lower() in defaults or var in seen_vars:
            continue
        seen_vars.add(var)
        findings.append(Finding(
            FAIL, "unfilled-variable",
            f"{{{{{var}}}}} has no default_value. Unfilled variables are read "
            f"aloud literally (\"Is this tier patient_ame?\").",
            line=text[: m.start()].count("\n") + 1,
        ))

    # 6. Re-ask guard.
    if not any(re.search(p, low) for p in REASK_PATTERNS):
        findings.append(Finding(
            FAIL, "no-reask-guard",
            "No re-ask guard. Add: 'keep track of what the caller has already "
            "told you and do not ask for the same thing twice.' Agents re-ask "
            "constantly without it.",
        ))

    # 7. Split-message / voice-lag handling.
    if not any(re.search(p, low) for p in SPLIT_MESSAGE_PATTERNS):
        findings.append(Finding(
            WARN, "no-split-message-handling",
            "No split-message handling. Voice lag delivers one sentence as two "
            "messages. Tell the agent to answer an obviously unfinished message "
            "with 'uh huh' so the caller keeps going.",
        ))

    # 8. Variety.
    if not any(re.search(p, low) for p in VARIETY_PATTERNS):
        findings.append(Finding(
            WARN, "no-variety-rule",
            "No variety instruction. Sample phrases make agents repetitive "
            "without one. Add: 'do not repeat the same sentence twice.'",
        ))

    # 9. Blanket absolutes outside a guardrails/reminders section.
    for i, line in enumerate(lines, 1):
        if not IMPERATIVE_ABSOLUTE_RE.search(line):
            continue
        section = _section_at(headers, i)
        if any(s in section for s in ABSOLUTE_SAFE_HEADERS):
            continue
        if line.lstrip().startswith(">"):      # example dialogue, not an instruction
            continue
        findings.append(Finding(
            WARN, "blanket-absolute",
            "Blanket 'always'/'never' outside a guardrails section. Realtime "
            "models take absolutes literally and produce bad edge behaviour. "
            "Write the intent plus its exception.",
            line=i,
        ))

    # 10. Multi-turn transcripts eat the attention budget.
    turns = len(SPEAKER_TURN_RE.findall(text))
    if turns > 6:
        findings.append(Finding(
            WARN, "transcript-block",
            f"{turns} speaker-labelled turns. Realtime models follow short "
            f"varied sample phrases better than multi-turn transcripts, which "
            f"get imitated literally.",
        ))

    # 11. Greeting must appear in the prompt so stage 1 matches what is spoken.
    if greeting:
        head = greeting.strip().rstrip("?.!")[:40]
        if head and head.lower() not in low:
            findings.append(Finding(
                WARN, "greeting-mismatch",
                "The configured greeting does not appear in the prompt. Stage 1 "
                "should match the spoken greeting verbatim.",
            ))

    # 12. A field described as derived must not also sit in a question list.
    derived_markers = ("not questions", "fill in silently", "do not ask it",
                       "work it out from", "already know this")
    if any(m in low for m in derived_markers):
        for i, line in enumerate(lines, 1):
            if re.match(r"^\s*\d+\.\s", line) and re.search(
                r"\bover (the age of )?(fifty|50)\b", line, re.I
            ):
                findings.append(Finding(
                    WARN, "derived-field-conflict",
                    "A field marked as derived also appears in the numbered "
                    "question list. Realtime models split the difference and "
                    "ask it AND answer it. Keep derived fields out of the list.",
                    line=i,
                ))

    order = {FAIL: 0, WARN: 1}
    findings.sort(key=lambda f: (order[f.level], f.line or 0))
    return findings


def summarize(findings: list[Finding]) -> tuple[int, int]:
    fails = sum(1 for f in findings if f.level == FAIL)
    warns = sum(1 for f in findings if f.level == WARN)
    return fails, warns


def format_report(findings: list[Finding], *, path: str = "", tokens: int | None = None) -> str:
    fails, warns = summarize(findings)
    out = []
    header = f"bd-voice-prompt-lint {path}".strip()
    if tokens is not None:
        header += f"  ({tokens} est. tokens / {TOKEN_BUDGET} budget)"
    out.append(header)
    if not findings:
        out.append("  OK - no findings")
        return "\n".join(out)
    for f in findings:
        loc = f":{f.line}" if f.line else ""
        out.append(f"  {f.level}  [{f.code}]{loc}  {f.message}")
    out.append(f"  {fails} FAIL, {warns} WARN")
    return "\n".join(out)
