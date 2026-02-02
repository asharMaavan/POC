from pytest_bdd import scenario


@scenario("../../features/boards.feature", "Audit log captures create and update events")
def test_audit_log():
    pass


@scenario("../../features/boards.feature", "Board name is required")
def test_board_name_required():
    pass


@scenario("../../features/rbac.feature", "Viewer cannot create a board via API")
def test_viewer_cannot_create_board_api():
    pass


@scenario("../../features/tenant_isolation.feature", "Tenant B cannot see boards created by tenant A")
def test_tenant_isolation():
    pass
