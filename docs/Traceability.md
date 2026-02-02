# Traceability Matrix

Legend for Status:
- Implemented: test exists but not executed
- Covered: manual or automated executed
- Gap: not covered

Example:
- AC-3 (RBAC): TC-RBAC-002, TC-RBAC-004 → E2E: tests/e2e/test_ui_smoke.py::test_viewer_controls_ui → Status: PASS

| AC ID | Acceptance Criteria | Manual TCs | Automated Tests | Status |
| --- | --- | --- | --- | --- |
| AC-01 | Login returns token/tenantId/role; rememberMe sets cookie | TC-01, TC-02 | tests/e2e/test_ui_smoke.py::test_remember_me | Implemented |
| AC-02 | Boards list scoped to tenant; includeArchived filters | TC-08, TC-10 | tests/api/test_api_regression.py::test_tenant_isolation | Implemented |
| AC-03 | Admin/Member can create board with name <= 60 | TC-04 | tests/e2e/test_ui_smoke.py::test_board_lifecycle_ui | Implemented |
| AC-04 | Rename/archive board by owner/Admin; archived hidden by default | TC-06, TC-07 | tests/e2e/test_ui_smoke.py::test_board_lifecycle_ui | Implemented |
| AC-05 | Viewer is read-only (write endpoints return 403) | TC-03 | tests/api/test_api_regression.py::test_viewer_cannot_create_board_api; tests/e2e/test_ui_smoke.py::test_viewer_controls_ui | Implemented |
| AC-06 | Card create and move columns | TC-09 | tests/e2e/test_ui_smoke.py::test_card_move_ui | Implemented |
| AC-07 | Validation: board name required and <= 60 | TC-05 | tests/api/test_api_regression.py::test_board_name_required; tests/e2e/test_ui_smoke.py::test_board_lifecycle_ui | Implemented |
| AC-08 | Validation: card title required and <= 120 | TC-09 | tests/e2e/test_ui_smoke.py::test_card_title_validation_ui | Implemented |
| AC-09 | Multi-tenant isolation on every endpoint | TC-10 | tests/api/test_api_regression.py::test_tenant_isolation | Implemented |
| AC-10 | Audit log available for create/update actions | - | tests/api/test_api_regression.py::test_audit_log | Implemented |
