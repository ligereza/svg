# What comes next

Do not connect large external datasets yet.

The immediate next implementation target is:

1. PostgreSQL migration tests
2. append-only event tests
3. observation deduplication tests
4. merge/split state reconstruction
5. snapshot reconstruction from event history
6. resolver benchmark harness
7. only then source adapters

This keeps the architecture testable before external data volume hides design errors.
