import httpx
import pytest
from pytest_bdd import given, parsers, then, when

from tests.helpers.context import ApiContext


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def api_context() -> ApiContext:
    return ApiContext()


@given(parsers.parse('I am logged in as "{email}"'))
def api_login_as(email, login, api_context: ApiContext):
    api_context.auth = login(email)


@when(parsers.parse('I log in as "{email}"'))
def api_relogin(email, login, api_context: ApiContext):
    api_context.auth = login(email)


@given(parsers.parse('I create a board named "{name}" via API'))
@when(parsers.parse('I create a board named "{name}" via API'))
def api_create_board(name, base_url, api_context: ApiContext):
    response = httpx.post(
        f"{base_url}/boards",
        headers=auth_headers(api_context.auth["token"]),
        json={"name": name},
        timeout=10.0,
    )
    api_context.response = response
    if response.status_code == 201:
        api_context.board = response.json()


@when(parsers.parse('I create a board named "{name}"'))
def api_create_board_alias(name, base_url, api_context: ApiContext):
    api_create_board(name, base_url, api_context)


@when('I attempt to create a board without a name')
def api_create_board_missing_name(base_url, api_context: ApiContext):
    response = httpx.post(
        f"{base_url}/boards",
        headers=auth_headers(api_context.auth["token"]),
        json={},
        timeout=10.0,
    )
    api_context.response = response


@when(parsers.parse('I rename the board to "{name}" via API'))
def api_rename_board(name, base_url, api_context: ApiContext):
    board_id = api_context.board.get("id")
    response = httpx.patch(
        f"{base_url}/boards/{board_id}",
        headers=auth_headers(api_context.auth["token"]),
        json={"name": name},
        timeout=10.0,
    )
    api_context.response = response


@when('I list boards via API')
def api_list_boards(base_url, api_context: ApiContext):
    response = httpx.get(
        f"{base_url}/boards",
        headers=auth_headers(api_context.auth["token"]),
        timeout=10.0,
    )
    api_context.response = response
    if response.status_code == 200:
        api_context.boards = response.json()


@then(parsers.parse('the response status should be {status:d}'))
def api_assert_status(status, api_context: ApiContext):
    assert api_context.response is not None
    assert api_context.response.status_code == status


@then('the response status should be 400 or 422')
def api_assert_status_400_or_422(api_context: ApiContext):
    assert api_context.response is not None
    assert api_context.response.status_code in {400, 422}


@then('the board should not appear in the list')
def api_board_not_in_list(api_context: ApiContext):
    board_id = api_context.board.get("id")
    ids = {board.get("id") for board in api_context.boards}
    assert board_id not in ids


@then('all boards belong to my tenant')
def api_all_boards_tenant(api_context: ApiContext):
    tenant_id = api_context.auth.get("tenantId")
    for board in api_context.boards:
        assert board.get("tenantId") == tenant_id
        assert "id" in board
        assert "name" in board
        assert "ownerId" in board
        assert "archived" in board


@then(parsers.parse('an audit entry exists for action "{action}" on the board'))
def api_audit_entry_exists(action, base_url, api_context: ApiContext):
    response = httpx.get(
        f"{base_url}/audit",
        headers=auth_headers(api_context.auth["token"]),
        timeout=10.0,
    )
    assert response.status_code == 200
    entries = response.json()
    board_id = api_context.board.get("id")
    assert any(
        entry.get("entityType") == "board"
        and entry.get("entityId") == board_id
        and entry.get("action") == action
        for entry in entries
    )
