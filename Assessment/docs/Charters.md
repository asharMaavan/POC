# Charters

## Charter 1 - Validate tenant isolation & RBAC across Boards & Cards
Timestamp: 2026-02-01 09:30-10:15
Heuristics: CRUD, SFDIPOT (Function, Data, Interfaces)

Mission
- Validate tenant isolation and role-based access across board and card actions.

Areas Covered
- Login via UI
- Board create/rename/archive with Viewer restrictions
- Card create/move restrictions by role
- Tenant A vs Tenant B visibility checks

Findings
- DEF-001: Archived board remains visible in list until refresh when Include Archived is unchecked.
- Viewer controls were disabled as expected; server returned 403 on create.

## Charter 2 - Cross-browser sanity: create/rename/archive board; drag-drop card
Timestamp: 2026-02-01 10:30-11:05
Heuristics: CRUD, SFDIPOT (Data, Time)

Mission
- Sanity check the main flow across browsers: create/rename/archive board and drag-drop a card.

Areas Covered
- Create board
- Rename and archive board
- Create card in Todo
- Drag to Doing/Done
- Refresh and re-open board

Findings
- DEF-002: Cards do not appear when opening the same board from a different browser/session (client-only storage).
- Drag/drop worked reliably within a session.
