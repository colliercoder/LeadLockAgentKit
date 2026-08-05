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
    "instructions": ("instruction", "rules", "communication", "guideline",
                     "guardrail", "hard limit"),
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
ABSOLUTE_SAFE_HEADERS = ("guardrail", "reminder", "never", "hard rule", "hard limit",
                         "boundaries", "limits")

# Prompting profiles.
#
# xAI's own migration guidance for grok-voice-think-fast (the model Leadlock runs)
# is explicit: "Simplify your system prompt... your prompt should be much shorter"
# and "Remove workaround prompting. Prompt hacks and edge-case fixes needed for GPT
# models are unnecessary." leadlock-app's migration doc calls this out as THE risk:
# "Our prompts are engineered against 1.0's quirks... it is prompt-quality, not code."
#
# So the structural scaffolding (six-section anatomy, explicit re-ask guard, split
# message handling, variety rule) is GPT-era patching. It is required under the
# `gpt-realtime` profile and dropped under `think-fast`.
SCAFFOLDING_CHECKS = {"missing-section", "no-reask-guard",
                      "no-split-message-handling", "no-variety-rule"}

PROFILES = {
    "think-fast": {"skip": SCAFFOLDING_CHECKS, "flag_scaffolding": True},
    "gpt-realtime": {"skip": set(), "flag_scaffolding": False},
}
DEFAULT_PROFILE = "think-fast"

# Instructions that exist only to patch older-model behaviour. On think-fast these
# consume the prompt without earning their place.
WORKAROUND_RES = [
    (re.compile(r"ask (?:exactly )?one question", re.I), "one-question-at-a-time rule"),
    (re.compile(r"then stop talking", re.I), "stop-talking rule"),
    (re.compile(r"last thing you say|ends on the question", re.I), "turn-ends-on-question rule"),
    (re.compile(r"do not repeat the same sentence", re.I), "variety rule"),
    (re.compile(r"\buh huh\b", re.I), "split-message handling"),
    (re.compile(r"rotate your acknowledge|do not lean on one phrase", re.I),
     "acknowledgement rotation"),
    (re.compile(r"spelled [A-Z](?:\s*-\s*[A-Z]){2,}", re.I), "read-back format template"),
    (re.compile(r"one line of the sheet is one turn", re.I), "one-field-per-turn rule"),
]

# Only IMPERATIVE absolutes matter. "Never end the call with fields blank" is the
# failure mode; "always on the caller's side" is a style descriptor and is fine.
IMPERATIVE_ABSOLUTE_RE = re.compile(
    r"^\s*(?:[-*+]\s*|\d+[.)]\s*)?(?:\*\*)?\s*(never|always)\b"
    r"|\byou\s+(?:must|should)\s+(?:never|always)\b",
    re.I,
)

SPEAKER_TURN_RE = re.compile(r"^\s*>?\s*\*\*[A-Z][A-Za-z ]{1,20}:\*\*", re.M)

# "bad phrasing" -> "good phrasing" pairs. Useful on cascaded pipelines, but on a
# realtime model the BAD string is just another quotable phrase sitting in
# context, and it gets imitated. Confirmed 2026-08-04: a prompt containing
#   "G - A - U - E - R - K - E. Is that correct?" -> "G - A - U - E - R - K - E."
# produced an agent that said "Is that right?" after every read-back.
BAD_GOOD_PAIR_RE = re.compile(r'"[^"\n]{6,}"\s*(?:->|→)\s*"', re.M)
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
    profile: str = DEFAULT_PROFILE,
) -> list[Finding]:
    """Return findings, most severe first. Empty list means clean.

    `profile` selects which checks apply. See PROFILES: `think-fast` (default,
    what Leadlock runs) drops the GPT-era structural scaffolding and instead
    flags it, per xAI's migration guidance. `gpt-realtime` keeps it.
    """
    cfg = PROFILES.get(profile, PROFILES[DEFAULT_PROFILE])
    skip = cfg["skip"]
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
                "Em dash (U+2014). House style bans it, and on a CASCADED "
                "pipeline it makes the TTS sound wrong (Chryst). NOTE: on true "
                "speech-to-speech there is no TTS reading the text, and em dashes "
                "in the agent's own transcript were confirmed inaudible on "
                "grok-voice-think-fast-2.0 (2026-08-04). Kept as a FAIL because it "
                "is free to fix, not because it is proven harmful on this stack.",
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

    # 4. Required sections. GPT-era scaffolding; skipped on think-fast.
    if "missing-section" not in skip:
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

    # 6. Re-ask guard. GPT-era scaffolding; skipped on think-fast.
    if "no-reask-guard" not in skip and not any(re.search(p, low) for p in REASK_PATTERNS):
        findings.append(Finding(
            FAIL, "no-reask-guard",
            "No re-ask guard. Add: 'keep track of what the caller has already "
            "told you and do not ask for the same thing twice.' Agents re-ask "
            "constantly without it.",
        ))

    # 7. Split-message / voice-lag handling. Skipped on think-fast.
    if ("no-split-message-handling" not in skip
            and not any(re.search(p, low) for p in SPLIT_MESSAGE_PATTERNS)):
        findings.append(Finding(
            WARN, "no-split-message-handling",
            "No split-message handling. Voice lag delivers one sentence as two "
            "messages. Tell the agent to answer an obviously unfinished message "
            "with 'uh huh' so the caller keeps going.",
        ))

    # 8. Variety. Skipped on think-fast.
    if "no-variety-rule" not in skip and not any(re.search(p, low) for p in VARIETY_PATTERNS):
        findings.append(Finding(
            WARN, "no-variety-rule",
            "No variety instruction. Sample phrases make agents repetitive "
            "without one. Add: 'do not repeat the same sentence twice.'",
        ))

    # 8b. Workaround prompting carried over from GPT-era models. xAI advises
    # stripping these on think-fast, where they cost prompt budget for nothing.
    if cfg["flag_scaffolding"]:
        found = []
        for rx, name in WORKAROUND_RES:
            m = rx.search(text)
            if m:
                found.append((name, text[: m.start()].count("\n") + 1))
        if len(found) >= 3:
            names = ", ".join(n for n, _ in found[:5])
            findings.append(Finding(
                WARN, "workaround-prompting",
                f"{len(found)} GPT-era workaround instructions ({names}). xAI's "
                f"think-fast guidance is to strip prompt hacks written for weaker "
                f"models: the reasoning handles turn-taking and tone natively, and "
                f"these crowd out the content only you can supply.",
                line=found[0][1],
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

    # 10b. Bad/good phrasing pairs prime the bad phrasing on realtime models.
    for m in BAD_GOOD_PAIR_RE.finditer(text):
        findings.append(Finding(
            WARN, "bad-good-pair",
            "A 'bad phrasing' -> 'good phrasing' pair. On realtime models the BAD "
            "string is quotable context and gets imitated. Show only the phrasing "
            "you want.",
            line=text[: m.start()].count("\n") + 1,
        ))
        break

    # 11. If the prompt scripts an opening, it must match the configured greeting.
    # A prompt that scripts no opening at all (fine on think-fast, where the
    # greeting field stands alone) has nothing to contradict, so there is no finding.
    if greeting:
        header_blob_all = " | ".join(h for _, h in headers)
        scripts_opening = any(k in header_blob_all for k in ("stage", "flow", "script")) \
            or "greeting" in low
        head = greeting.strip().rstrip("?.!")[:40]
        if scripts_opening and head and head.lower() not in low:
            findings.append(Finding(
                WARN, "greeting-mismatch",
                "This prompt scripts an opening, but the configured greeting does "
                "not appear in it. The two will contradict each other.",
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
