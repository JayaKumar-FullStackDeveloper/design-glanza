# Conversational UX

## Responsibility
The interaction contract for a **conversational** interaction model —
`methodology/ideate.md` item 2 already names this as one of the interaction
models compared against Empathize's Frequency/Environment/Decision-making
dimensions, but names it only, with nothing yet specifying its actual shape.
This file gives it the same concrete, checkable rules every other named
interaction model in `ux-engine/*` already has, for the case where Ideate
selects it: a chat-style or turn-based assistant flow (a support bot, a
guided data-entry conversation, a natural-language query surface), not the
literal chrome of a messaging app.

## When conversational is the right model
Per `ideate.md`'s own selection criteria, applied to this model specifically:
favors a task that is rarely performed (doesn't rely on the user remembering
a UI's layout from last time), genuinely open-ended or variable in shape (the
next question depends on the last answer in a way a fixed form can't express
cleanly), or where natural language is itself the fastest input method for
this actor (describing a problem is faster than navigating to the right
form field for it). **Not** a good fit for a frequent, structured, or
high-volume task — a conversational flow imposed on a task better served by
a form or table is slower and less scannable than the model it replaced,
which is itself a defect (`user-flow-engine.md` criterion 2, Fast
decision-making).

## Turn structure
Every conversational exchange is one instance of `user-flow-engine.md`'s own
six-part notation, not a separate notation:
```
ENTRY → ACTION (user's message/input) → DECISION (intent parsed, or
ambiguous) → SYSTEM RESPONSE (reply, or clarifying question) → NEXT ACTION →
COMPLETION
```
A conversational flow is still traceable to a `FLOW-NNN`, still has a named
Completion state, and still needs every Decision branch's outcome named — the
model changes the *medium* of Action/System response, not the requirement
that the flow be fully specified.

## The error-reprompt ladder
An unparseable or ambiguous user input is a Decision branch
(`user-flow-engine.md`'s Decision part) that must resolve to a named outcome,
never a silent repeat of the same question. Three escalating tries, in
order, before handing off:
1. **First miss** — ask a narrower, more specific version of the same
   question (per `ux-writing.md`'s clarity rules), not a repeat of the
   original open-ended prompt.
2. **Second miss** — offer a small set of concrete choices (buttons/chips) in
   place of free text, narrowing the input space rather than asking the user
   to try free text a third time.
3. **Third miss** — escalate: hand off to a human, a traditional form
   equivalent of the same task, or a documented fallback — per
   `user-flow-engine.md`'s Recovery paths' **escalate** resolution. A
   conversational flow with no such fallback after repeated failure is a
   dead end (Blocker-severity, same as any other flow with no path forward).

## Voice and tone rules
Cites, rather than restates, `ux-writing.md`'s existing voice/tone/clarity
rules — a conversational surface follows the same product voice as every
other piece of interface copy, not a separate "chattier" register invented
for the chat medium. Two additions specific to the turn-based medium:
- **State what it understood, before acting on anything consequential** — a
  conversational input that triggers a non-trivial or irreversible action
  (per `interaction-design.md`'s reversibility×risk matrix) restates its
  parsed interpretation as part of the System response, so the user can
  correct a misunderstanding before the action fires, not after.
- **Never fabricate certainty** — a response built from an inference the
  system isn't actually sure of is phrased as a question or a qualified
  suggestion, not a flat statement — the same Known/Assumed/Inferred
  distinction `design-research/research-methodology.md` already applies to
  research findings applies here to what the system tells the user it
  understood.

## Progress and state visibility
A multi-turn conversational flow that's building up structured state (a
guided setup, a multi-field intake conducted as a conversation) still needs
`user-flow-engine.md` criterion 8's operational clarity — surface what's been
captured so far and what's still needed, the same content a form's own
in-progress state would show, rather than relying on the user to remember
the conversation's history themselves.

## Explicitly not here
- The general interaction-model selection process and its comparison
  criteria → `methodology/ideate.md` item 2.
- The canonical flow notation and recovery-path mechanics this model reuses
  → `ux-engine/user-flow-engine.md`.
- General copy voice/tone/clarity rules → `ux-engine/ux-writing.md`.
- Action-feedback timing, reversibility×risk matrix → `ux-engine/
  interaction-design.md`.
