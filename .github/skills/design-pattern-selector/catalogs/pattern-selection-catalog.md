# Pattern selection catalog

## Strategy
Use when behavior varies by policy and should remain swappable and testable.

## Adapter
Use when integrating with external or legacy interfaces while preserving an internal contract.

## Factory / Abstract Factory
Use when object construction logic should be centralized, varied, or hidden from consumers.

## State
Use when lifecycle transitions drive behavior and explicit state transitions improve correctness.

## Observer / Pub-Sub
Use when multiple consumers must react to events without tight coupling.

## Decorator
Use when cross-cutting behavior should wrap a stable core contract.

## Repository
Use when persistence details must be isolated from domain logic.

## Policy Object / Rule Object
Use when complex branching can be modeled as composable rules.

## Command
Use when operations need queuing, auditing, retries, undo, or deferred execution.

## Anti-pattern reminders
- Do not introduce a pattern only to mirror terminology.
- Avoid inheritance-heavy structures when composition is sufficient.
- Avoid adding factory layers when constructors are already simple and stable.
