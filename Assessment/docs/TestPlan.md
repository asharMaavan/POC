# Test Plan - Boards QA Assessment (Risk Based)

Date: 2026-02-01
Owner: QA

## Objectives
- Validate core user flows for the Boards app: login, boards, and cards.
- Verify RBAC and tenant isolation across API and UI.
- Confirm key validations and error handling.
- Establish a performance smoke baseline for GET /boards.

## In Scope
- API: /api/v1/auth/login, /boards (GET/POST/PATCH), /cards (POST/PATCH), /audit (GET).
- UI: login page, boards page, board page with drag/drop.
- RBAC: Admin, Member, Viewer behaviors.
- Multi-tenant isolation.
- Validation: board name <= 60, card title <= 120.
- Performance smoke test (JMeter scenario).

## Out of Scope
- Persistence across server restarts (in-memory data only).
- Delete endpoints (not implemented).
- Search, pagination, sorting beyond includeArchived.
- Security testing beyond basic auth/role checks (e.g., OWASP, rate limiting).
- Mobile native apps.

## Approach
Risk-based prioritization focuses on auth, isolation, RBAC, and CRUD paths.

Test types:
- Automated API regression (pytest + httpx).
- Automated UI E2E (pytest-playwright).
- Exploratory sessions (charters).
- Performance smoke (JMeter).

## Test Environment
- Local API: http://localhost:8000
- Local UI: http://localhost:5173
- Seed users:
  - Tenant A: adminA/memberA/viewerA@example.com
  - Tenant B: adminB/memberB/viewerB@example.com
  - Password: Password123!

## Entry Criteria
- API and UI can start locally.
- Seed users available.
- Test data isolated per run (unique names).

## Exit Criteria
- Automated suites executed without critical failures.
- Top risks reviewed and defects triaged.
- Performance smoke executed and reported.

## Key Risks and Mitigations
- Tenant data leakage (mitigate with API isolation tests).
- RBAC bypass (mitigate with UI and API negative tests).
- Validation regressions (mitigate with boundary tests).
- Drag/drop stability (mitigate with Playwright E2E).
- Performance regressions (mitigate with JMeter smoke).

## Deliverables
- Test cases, charters, defects, traceability, summary.
- Automated test suites in tests/api and tests/e2e.
- Performance smoke plan in perf/boards_smoke.jmx.
