# Requirement intake checklist

## Functional intent
- What problem is being solved?
- What user or system behavior should change?
- What should explicitly stay unchanged?

## Scope
- Which modules, packages, services, or screens are in scope?
- Which areas must not be touched?
- Is this a local fix or a cross-cutting change?

## Compatibility
- Can existing behavior break?
- Are schema, API, or file format changes allowed?
- Is backward compatibility mandatory?

## Quality
- What are the acceptance criteria?
- Are there latency, throughput, reliability, or security constraints?
- Are there rollout or migration constraints?

## Validation
- What test level is required?
- What examples, fixtures, or golden cases matter?
- Which previous issues or regressions should be rechecked?

## Documentation
- Which specs, ADRs, runbooks, or diagrams should be updated?
