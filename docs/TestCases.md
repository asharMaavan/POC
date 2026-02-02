# Manual Test Cases

## Test Case Template
ID: TC-BOARD-001
Title: Create board with valid name
Preconditions: Logged in as Member, tenantId=A
Steps: Go to Boards → New → enter name "Q3 Plan" → Save
Expected: 201 created; board visible in list; audit entry created
Validation: UI toast, API 201, board in GET /boards with tenantId=A

| ID | Title | Preconditions | Steps | Expected |
| --- | --- | --- | --- | --- |
| TC-01 | Login with valid admin | API/UI running | 1. Open UI 2. Enter adminA@example.com / Password123! 3. Submit | Boards page visible; role/tenant shown |
| TC-02 | Remember-me persists after refresh | Logged out | 1. Login with Remember me checked 2. Refresh page | Still logged in; boards page visible |
| TC-03 | Viewer restrictions | Logged in as viewerA | 1. Go to Boards page 2. Observe controls | Create/rename/archive disabled and/or errors on write |
| TC-04 | Create board valid | Logged in as adminA | 1. Enter name <= 60 2. Create | Board appears in list |
| TC-05 | Board name validation | Logged in as adminA | 1. Enter 61-char name 2. Create | Error shown; board not created |
| TC-06 | Rename board | Existing board | 1. Click Rename 2. Enter new name <= 60 | Board name updated |
| TC-07 | Archive hides by default | Existing board; Include Archived unchecked | 1. Archive board | Board disappears from list |
| TC-08 | Include archived toggle | Archived board exists | 1. Check Include Archived | Archived board visible with indicator |
| TC-09 | Create card and move | Board open | 1. Create card in Todo 2. Drag to Doing | Card visible in Doing |
| TC-10 | Tenant isolation | Board in tenant A exists | 1. Login as adminB 2. List boards | Tenant A board not visible |
