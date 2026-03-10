---
name: requirement-intake
description: Structured requirement clarification and intake checklist. Use this when the request is ambiguous, under-specified, or likely to affect compatibility, architecture, tests, or documentation.
license: Proprietary - project local use
---

Use this skill before implementation when any requirement is incomplete or could be interpreted in multiple ways.

## Objectives
- Minimize hidden assumptions.
- Ask fine-grained, high-signal questions.
- Capture acceptance criteria before implementation.

## Process
1. Summarize the requested change in one sentence.
2. Identify uncertainty in:
   - goal
   - scope
   - compatibility
   - data or schema impact
   - operational impact
   - test expectations
   - documentation impact
3. Ask only the minimum set of questions needed to unblock a safe design.
4. If proceeding with partial information, state explicit assumptions and label them as temporary.
5. Record clarified requirements in the nearest spec or work note if the repository has one.

## Question catalog
Refer to `checklists/question-checklist.md`.

## Output format
- Requested change
- Clarifying questions
- Current assumptions
- Acceptance criteria draft
