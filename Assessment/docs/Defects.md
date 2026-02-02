# Defects

## Defect Template
- Title:
- Env/Build:
- Severity/Priority:
- Preconditions:
- Steps to Reproduce:
- Expected Result:
- Actual Result:
- Evidence (screenshot/log/har):
- Notes / Suspected Cause:

---

## DEF-001
- Title: Archived board remains visible in list until refresh when Include Archived is unchecked
- Env/Build: Local UI http://localhost:5173, API http://localhost:8000
- Severity/Priority: Medium / P2
- Preconditions: Logged in as Admin; Include Archived unchecked
- Steps to Reproduce:
  1. Create a new board
  2. Click Archive on the board
- Expected Result: Archived board is hidden immediately because Include Archived is unchecked
- Actual Result: Board remains visible (marked archived) until a manual refresh or list reload
- Evidence (screenshot/log/har): Observed during Charter 1
- Notes / Suspected Cause: Aligns with requirement "Archived boards hidden by default unless includeArchived=true"

---

## DEF-002
- Title: Cards do not appear when opening the same board from a different browser/session
- Env/Build: Local UI http://localhost:5173, API http://localhost:8000
- Severity/Priority: Medium / P2
- Preconditions: Board and cards created in Browser A
- Steps to Reproduce:
  1. In Browser A, create a board and add a card
  2. Open a new browser or incognito session
  3. Login with same user and open the same board
- Expected Result: Cards appear for the board (server-side persistence)
- Actual Result: No cards are shown; cards are stored only in Browser A localStorage
- Evidence (screenshot/log/har): Observed during Charter 2
- Notes / Suspected Cause: UI stores cards locally; API has no GET /cards endpoint

---

## DEF-003
- Title: POST /boards without name returns 422 instead of 400
- Env/Build: API http://localhost:8000
- Severity/Priority: Low / P3
- Preconditions: Valid admin token
- Steps to Reproduce:
  1. Send POST /api/v1/boards with empty JSON body
- Expected Result: 400 Bad Request (per spec)
- Actual Result: 422 Unprocessable Entity
- Evidence (screenshot/log/har): API regression test observation
- Notes / Suspected Cause: Acceptable if spec updated; otherwise enforce 400 in handler
