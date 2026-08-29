# Contributing to HuluSafe

## Branches

`main` is for reviewed releases. All work goes through `develop`.

```text
GitHub Issue → feature branch → tests → pull request → review → merge to develop → release to main
```

## Pull request checklist

- Follows the architecture in `docs/architecture/`
- Uses the shared danger-event JSON in `docs/api/rest-api.md`
- Does not invent missing impact values
- Avoids unrelated edits in another student's files
- Includes tests where practical
- Shows publication time and event time (`Unknown` if missing)

## File ownership

- Student 1: `frontend/` dashboard, location, settings, auth UI, shared foundation
- Student 2: map, search, danger details, notifications, alert history
- Student 3: `backend/` database, news, APIs, time and proximity
- Student 4: `ai/`
- Student 5: scoring, clustering, regional tracking (`backend/app/services/intelligence.py` and related)

Shared contracts change only after a team discussion.
