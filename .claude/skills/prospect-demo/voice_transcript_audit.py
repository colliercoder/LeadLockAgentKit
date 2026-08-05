"""Audit a real voice-agent call transcript, then point at the prompt line that caused it.

The lesson from the Drummond Law build (2026-08-03): every misbehaviour the
operator saw on a call was caused by a specific line already in the system
prompt, not by the model being unruly. The instinct to ADD a rule naming the
failure is backwards and grows the prompt past the point where a realtime model
follows any of it.

So this module does two things:

1. Detect known failure shapes in the agent's turns. Deterministic, no LLM.
2. Map each detected failure to the prompt pattern that usually causes it, and
   cite the offending prompt lines when a prompt is supplied.

Detectors are tuned against the actual failing transcripts from that build.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict, field

AGENT_LABELS = ("agent", "assistant", "ai", "bot", "marge", "maya", "ava")
CALLER_LABELS = ("caller", "user", "customer", "human", "client", "prospect")

LONG_TURN_WORDS = 40

# A spelled-out sequence ("G - A - U - E") or a run of spoken digits.
READBACK_RE = re.compile(
    r"(?:\b[A-Z]\b[\s\-,.]{1,3}){3,}"
    r"|(?:\b\d[\s\-,.]{0,3}){7,}"
    r"|\b\d{3}[\s\-.]\d{3}[\s\-.]\d{4}\b"
)

NARRATION_RES = [
    (re.compile(r"\bI(?:'|’)?ll\s+(?:spell|read)\b[^.?!]{0,30}\bback\b", re.I),
     "announces a read-back before doing it"),
    (re.compile(r"\bonce I have (?:that|this)\b", re.I),
     "announces the next step"),
    (re.compile(r"\b(?:then|next),?\s+I(?:'|’)?ll\b", re.I),
     "announces the next step"),
    (re.compile(r"\bI(?:'|’)?m going to ask\b", re.I),
     "previews an upcoming question"),
    (re.compile(r"\bI(?:'|’)?ll\s+(?:get|need|grab|take)\s+your\b", re.I),
     "announces the next field"),
]

FILLER_RES = [
    re.compile(r"\bso (?:we're|we are|were) on the same page\b", re.I),
    re.compile(r"\bjust to confirm\b", re.I),
    re.compile(r"\bso I know I(?:'|’)?ve got it right\b", re.I),
    re.compile(r"\bI(?:'|’)?ve got you down as\b", re.I),
    re.compile(r"\bthank you for providing that information\b", re.I),
    re.compile(r"\bI would be happy to\b", re.I),
]

REDUNDANT_CONFIRM_RE = re.compile(r"\bis that (?:correct|right)\b|\bdid I get that right\b", re.I)

# A call should not end on a bare acknowledgement. Observed 2026-08-04: the last
# field of an intake was an optional email, the caller said "she doesn't have
# one", and the agent said "No problem" and fired end_call in the same turn,
# skipping the entire closing including the callback number.
FAREWELL_RE = re.compile(
    r"\b(goodbye|good bye|bye|take care|have a (?:good|great|nice)|talk soon|"
    r"watch for it|reach(?:ing)? out|be in touch|call you|thanks for calling|"
    r"you did the right thing)\b",
    re.I,
)
ABRUPT_END_MAX_WORDS = 8
PHONE_RE = re.compile(r"\b\d{3}[\s\-.]\d{3}[\s\-.]\d{4}\b")

SELF_ANSWER_RE = re.compile(
    r"\?\s*(?:No|Yes|Nope|Yeah|Nah)\b[^?]{0,45}?\b(?:you|you're|youre|it's|its|that's)\b",
    re.I,
)

# failure code -> (what to look for in the prompt, what to do about it)
CAUSE_MAP = {
    "multi-question": (
        [r"group the questions", r"run together", r"batch", r"land like conversation",
         r"conversationally", r"work in\b"],
        "Cut any instruction that tells the agent to group or batch questions. "
        "Replace with: ASK ONE QUESTION, THEN STOP TALKING AND WAIT.",
    ),
    "narrating-next-step": (
        [r"\(\s*(?:spell|read)[^)]*back[^)]*\)", r"verify", r"read all ten digits",
         r"spell it back"],
        "Parenthetical field annotations like '(spell it back)' get SPOKEN. Remove them "
        "from the field list and state the behaviour once in an Instructions block. "
        "Add: the question is the last thing you say.",
    ),
    "redundant-confirmation": (
        [r"is that correct", r"confirm(?:ation)? (?:that|the)", r"verify"],
        "Add: read it back, then stop. Repeating it back already asks whether you got "
        "it right, so no 'is that correct?' on the end.",
    ),
    "repeat-question": (
        [r"ask (?:all|each|every)", r"work through", r"in order"],
        "Add the re-ask guard: keep track of what the caller has already told you and "
        "do not ask for the same thing twice.",
    ),
    "self-answered-question": (
        [r"work it out from", r"do not ask it", r"don't ask it", r"already know this",
         r"not questions", r"fill in silently"],
        "A derived field is also sitting in the question list. The model splits the "
        "difference and asks it AND answers it. Remove it from the numbered list entirely.",
    ),
    "long-turn": (
        [r"one to three sentences", r"keep (?:it|turns) (?:brief|short)", r"short sentence"],
        "Tighten to: keep turns to one short sentence. Two at the very most.",
    ),
    "robotic-repetition": (
        [r"sample phrases", r"vary"],
        "Add a Variety block: do not repeat the same sentence twice, and give 3-4 varied "
        "sample phrases for the moment that is repeating.",
    ),
    "corporate-filler": (
        [r"professional", r"courteous", r"assist"],
        "Replace adjective-style personality with audible behaviours and reaction "
        "triggers. Acknowledge what they SAID, not what you are doing with it.",
    ),
    "abrupt-ending": (
        [r"once you have what you need", r"when you have (?:it |what)", r"then end the call",
         r"if not, that'?s fine"],
        "Separate the closing SPEECH from the hangup. The trigger phrase makes the "
        "model jump straight to the tool once the last field is answered, and end_call "
        "terminates before the closing is spoken. Say the closing, wait for them to "
        "respond, and make the hangup a separate last act gated on what they must hear.",
    ),
    "closing-skipped": (
        [r"once you have what you need", r"then end the call", r"when you have everything"],
        "The closing never ran. Gate the hangup on the caller having heard the thing "
        "that matters (the callback number), not on the field list being complete.",
    ),
}


@dataclass
class Turn:
    speaker: str
    text: str
    index: int


@dataclass
class Issue:
    code: str
    detail: str
    turn_index: int
    quote: str
    fix: str = ""
    subject: str = ""
    prompt_lines: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


STOPWORDS = {
    "the", "a", "an", "of", "is", "are", "you", "your", "any", "and", "or", "do",
    "did", "have", "has", "in", "on", "at", "to", "for", "with", "that", "this",
    "what", "when", "where", "how", "was", "were", "been", "be", "it", "its",
}


def _keywords(text: str) -> set[str]:
    words = re.findall(r"[a-z]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def _numbered_line_for(prompt_lines: list[str], subject: str) -> list[dict]:
    """Numbered list entries that clearly cover the same field as `subject`."""
    want = _keywords(subject)
    if not want:
        return []
    out = []
    for n, line in enumerate(prompt_lines, 1):
        if not re.match(r"^\s*\d+[.)]\s", line):
            continue
        overlap = want & _keywords(line)
        if len(overlap) >= 2:
            out.append({"line": n, "text": line.strip()[:140]})
    return out


def _norm_speaker(raw: str) -> str:
    s = re.sub(r"[^a-z]", "", raw.lower())
    if any(s.startswith(a) for a in AGENT_LABELS):
        return "agent"
    if any(s.startswith(c) for c in CALLER_LABELS):
        return "caller"
    return "agent" if s else "unknown"


def parse_transcript(text: str) -> list[Turn]:
    """Accept 'Agent: ...', '**Agent:** ...', '> **Marge:** ...', or blank-line blocks."""
    turns: list[Turn] = []
    line_re = re.compile(r"^\s*>?\s*(?:\*\*)?([A-Za-z][A-Za-z .'_-]{0,24}?)(?:\*\*)?\s*:\s*(.*)$")
    current: Turn | None = None
    for raw in text.splitlines():
        if not raw.strip():
            continue
        m = line_re.match(raw)
        if m and not raw.strip().startswith(("http", "#")):
            speaker = _norm_speaker(m.group(1))
            body = m.group(2).strip()
            current = Turn(speaker, body, len(turns))
            turns.append(current)
        elif current is not None:
            current.text = (current.text + " " + raw.strip()).strip()
    return [t for t in turns if t.text]


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]


def _normalize_q(q: str) -> str:
    q = q.lower()
    q = re.sub(r"[^a-z ]", " ", q)
    q = re.sub(r"\b(and|so|okay|alright|now|well|just|please|may i|can i|could i|your|you)\b", " ", q)
    return re.sub(r"\s+", " ", q).strip()


def _closing_issues(agent_turns: list[Turn], prompt: str | None) -> list[Issue]:
    """Did the call actually close, or did the agent just stop?"""
    out: list[Issue] = []
    if not agent_turns:
        return out
    last = agent_turns[-1]
    words = len(last.text.split())
    # A transcript whose final agent turn is a QUESTION was cut off mid-flow, or is
    # an excerpt. Either way it is not a botched closing, which is what this checks.
    ended_on_question = last.text.rstrip().endswith("?")
    if (not ended_on_question and words <= ABRUPT_END_MAX_WORDS
            and not FAREWELL_RE.search(last.text)):
        out.append(Issue(
            "abrupt-ending",
            f"The call ends on a {words}-word acknowledgement with no farewell. "
            f"A closing that the caller never heard did not happen.",
            last.index, last.text[:150],
        ))

    # If the prompt's closing scripts a callback number, it must have been said.
    if prompt:
        closing = ""
        grab = False
        for line in prompt.splitlines():
            if re.match(r"^#+\s*clos", line, re.I):
                grab = True
                continue
            if grab and line.startswith("#"):
                break
            if grab:
                closing += " " + line
        spoken = " ".join(t.text for t in agent_turns)
        for num in set(PHONE_RE.findall(closing)):
            digits = re.sub(r"\D", "", num)
            spoken_digits = re.sub(r"\D", "", spoken)
            if digits and digits not in spoken_digits:
                out.append(Issue(
                    "closing-skipped",
                    f"The prompt's closing gives the caller {num}, and it was never "
                    f"said on this call. The close did not run.",
                    agent_turns[-1].index, agent_turns[-1].text[:150],
                ))
    return out


def audit(transcript: str, *, prompt: str | None = None) -> list[Issue]:
    turns = parse_transcript(transcript)
    agent_turns = [t for t in turns if t.speaker == "agent"]
    issues: list[Issue] = list(_closing_issues(agent_turns, prompt))

    seen_questions: dict[str, int] = {}
    sentence_counts: dict[str, int] = {}

    for t in agent_turns:
        text = t.text
        qmarks = text.count("?")

        if qmarks >= 2:
            issues.append(Issue(
                "multi-question",
                f"{qmarks} questions in one turn. The caller can only answer the last one.",
                t.index, text[:150],
            ))

        for rx, why in NARRATION_RES:
            m = rx.search(text)
            if m:
                issues.append(Issue(
                    "narrating-next-step", f"{why}: \"{m.group(0)}\"",
                    t.index, text[:150],
                ))
                break

        if REDUNDANT_CONFIRM_RE.search(text) and READBACK_RE.search(text):
            issues.append(Issue(
                "redundant-confirmation",
                "Adds 'is that correct?' after reading something back. The read-back "
                "already asks the question.",
                t.index, text[:150],
            ))

        m = SELF_ANSWER_RE.search(text)
        if m:
            # Keep the question that got self-answered so the cause pass can look
            # for that specific field sitting in a numbered list.
            asked = ""
            for s in _sentences(text):
                if s.endswith("?") and text.find(s) <= m.start():
                    asked = s
            iss = Issue(
                "self-answered-question",
                f"Asks a question and immediately answers it: \"{m.group(0).strip()}\"",
                t.index, text[:150],
            )
            iss.subject = asked or m.group(0)
            issues.append(iss)

        # A closing legitimately runs long: it carries the callback number and the
        # next step. It is NOT always the final turn, because a goodbye exchange
        # usually follows it, so exempt any closing-shaped turn in the last quarter
        # of the call rather than only the last one.
        words = len(text.split())
        tail_starts = len(agent_turns) - max(1, len(agent_turns) // 4)
        in_tail = agent_turns.index(t) >= tail_starts
        is_closing = in_tail and FAREWELL_RE.search(text)
        if words > LONG_TURN_WORDS and not is_closing:
            issues.append(Issue(
                "long-turn", f"{words} words in one turn (over {LONG_TURN_WORDS}).",
                t.index, text[:150],
            ))

        for rx in FILLER_RES:
            m = rx.search(text)
            if m:
                issues.append(Issue(
                    "corporate-filler",
                    f"Stiff filler phrase: \"{m.group(0)}\"",
                    t.index, text[:150],
                ))
                break

        for s in _sentences(text):
            if s.endswith("?"):
                key = _normalize_q(s)
                if len(key) > 12:
                    if key in seen_questions:
                        issues.append(Issue(
                            "repeat-question",
                            f"Already asked this in turn {seen_questions[key]}: \"{s}\"",
                            t.index, s[:150],
                        ))
                    else:
                        seen_questions[key] = t.index
            norm = _normalize_q(s)
            if len(norm) > 10:
                sentence_counts[norm] = sentence_counts.get(norm, 0) + 1

    for norm, n in sentence_counts.items():
        if n >= 3:
            issues.append(Issue(
                "robotic-repetition",
                f"The same sentence is used {n} times across the call.",
                -1, norm[:120],
            ))

    issues.sort(key=lambda i: (i.turn_index if i.turn_index >= 0 else 10**6, i.code))
    return issues


def attach_causes(issues: list[Issue], prompt: str | None) -> list[Issue]:
    """Fill in fix guidance, and cite the prompt lines that likely caused each issue."""
    lines = prompt.splitlines() if prompt else []
    for iss in issues:
        patterns, fix = CAUSE_MAP.get(iss.code, ([], ""))
        iss.fix = fix
        if not prompt:
            continue

        # A derived-field marker on its own is the CORRECT state, not a cause.
        # It only causes a self-answered question when the same field ALSO sits
        # in the numbered question list. Require both halves of the conflict.
        if iss.code == "self-answered-question":
            conflicting = _numbered_line_for(lines, iss.subject or iss.quote)
            if not conflicting:
                iss.fix = ("Already handled in this prompt: the field is declared derived "
                           "and is not in the question list. If the agent still voices it, "
                           "the derived note itself may be reading as a question.")
                continue
            marker_lines = []
            for n, line in enumerate(lines, 1):
                if any(re.search(p, line, re.I) for p in patterns):
                    marker_lines.append({"line": n, "text": line.strip()[:140]})
            iss.prompt_lines = (conflicting + marker_lines)[:3]
            continue

        hits = []
        for n, line in enumerate(lines, 1):
            for p in patterns:
                if re.search(p, line, re.I):
                    hits.append({"line": n, "text": line.strip()[:140]})
                    break
            if len(hits) >= 3:
                break
        iss.prompt_lines = hits
    return issues


def format_report(issues: list[Issue], *, path: str = "", have_prompt: bool = False) -> str:
    out = [f"bd-voice-transcript-audit {path}".strip()]
    if not issues:
        out.append("  OK - no known failure patterns in the agent's turns")
        return "\n".join(out)

    by_code: dict[str, list[Issue]] = {}
    for i in issues:
        by_code.setdefault(i.code, []).append(i)

    for code, group in sorted(by_code.items(), key=lambda kv: -len(kv[1])):
        out.append("")
        out.append(f"  {code}  ({len(group)}x)")
        for i in group[:4]:
            loc = f"turn {i.turn_index}" if i.turn_index >= 0 else "whole call"
            out.append(f"    - [{loc}] {i.detail}")
            out.append(f"      \"{i.quote}\"")
        if len(group) > 4:
            out.append(f"    ... and {len(group) - 4} more")
        if group[0].fix:
            out.append(f"    FIX: {group[0].fix}")
        cited = [pl for i in group for pl in i.prompt_lines]
        if cited:
            seen = set()
            out.append("    LIKELY CAUSE in the prompt:")
            for pl in cited:
                if pl["line"] in seen:
                    continue
                seen.add(pl["line"])
                out.append(f"      prompt:{pl['line']}  {pl['text']}")
        elif have_prompt:
            out.append("    No causing line found in the prompt. This one may need a NEW rule.")

    out.append("")
    out.append(f"  {len(issues)} issue(s) across {len(by_code)} pattern(s)")
    out.append("  Remove or fix the causing lines before adding anything new.")
    return "\n".join(out)
