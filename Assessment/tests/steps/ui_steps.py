import re

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

from tests.e2e.pages.api_client import api_create_board, api_login
from tests.e2e.pages.app_page import AppPage
from tests.helpers.context import UiContext


@pytest.fixture()
def ui_context() -> UiContext:
    return UiContext()


@given('I open the app')
def ui_open_app(page, ui_context: UiContext):
    app = AppPage(page)
    app.goto()
    ui_context.app = app


@given(parsers.parse('I log in as "{email}" with password "{password}" and remember me {remember}'))
@when(parsers.parse('I log in as "{email}" with password "{password}" and remember me {remember}'))
def ui_login(email, password, remember, ui_context: UiContext):
    remember_flag = str(remember).lower() == "true"
    ui_context.app.login(email, password, remember=remember_flag)


@then('I should still be logged in after reload')
def ui_still_logged_in_after_reload(page):
    page.reload()
    expect(page.get_by_test_id("boards-new")).to_be_visible()


@then('the remember me cookie max age is about 604800 seconds')
def ui_cookie_max_age(ui_context: UiContext):
    cookie = ui_context.app.get_session_cookie()
    assert cookie, "Expected session cookie to be set"
    assert ui_context.app.is_cookie_approx_max_age(cookie, 604800)


@given(parsers.parse('I have a board named "{name}"'))
def ui_have_board(name, ui_context: UiContext):
    ui_context.board = ui_context.app.create_board(name)


@when(parsers.parse('I create a board named "{name}"'))
def ui_create_board(name, ui_context: UiContext):
    ui_context.board = ui_context.app.create_board(name)


@when(parsers.parse('I rename the board to "{name}"'))
def ui_rename_board(name, ui_context: UiContext):
    ui_context.app.rename_board(ui_context.board["id"], name)


@when('I archive the board')
def ui_archive_board(ui_context: UiContext):
    ui_context.app.archive_board(ui_context.board["id"])


@then('the board should not be listed')
def ui_board_not_listed(page, ui_context: UiContext):
    page.reload()
    expect(page.get_by_test_id(f"board-row-{ui_context.board['id']}")).to_have_count(0)


@when('I open the board')
def ui_open_board(ui_context: UiContext):
    ui_context.app.open_board(ui_context.board["id"])


@when(parsers.parse('I create a card titled "{title}" in column "{column}"'))
def ui_create_card(title, column, ui_context: UiContext):
    ui_context.card = ui_context.app.create_card(title, column=column)


@when(parsers.parse('I drag the card to column "{column}"'))
def ui_drag_card(column, ui_context: UiContext):
    column_test_id = f"column-{column.lower()}"
    ui_context.app.drag_card_to_column(ui_context.card["id"], column_test_id)


@then(parsers.parse('the card should be in column "{column}"'))
def ui_card_in_column(column, ui_context: UiContext):
    column_test_id = f"column-{column.lower()}"
    ui_context.app.card_in_column(ui_context.card["id"], column_test_id)


@then(parsers.parse('the card should remain in column "{column}" after refresh'))
def ui_card_persists_after_refresh(page, ui_context: UiContext, column):
    page.reload()
    expect(page.get_by_test_id("boards-new")).to_be_visible()
    ui_context.app.open_board(ui_context.board["id"])
    column_test_id = f"column-{column.lower()}"
    ui_context.app.card_in_column(ui_context.card["id"], column_test_id)


@given('a board exists for tenant A')
def ui_board_exists_for_tenant_a(ui_context: UiContext):
    token = api_login("adminA@example.com", "Password123!")
    ui_context.board = api_create_board(token, "Tenant A Shared Board")


@then('viewer board controls are disabled')
def ui_viewer_controls_disabled(page, ui_context: UiContext):
    expect(page.get_by_test_id("boards-new")).to_be_disabled()
    expect(page.get_by_test_id("boards-name-input")).to_be_disabled()
    expect(page.get_by_test_id("boards-save")).to_be_disabled()
    expect(page.get_by_test_id(f"board-row-{ui_context.board['id']}")).to_be_visible()
    expect(page.get_by_test_id(f"board-rename-{ui_context.board['id']}")).to_be_disabled()
    expect(page.get_by_test_id(f"board-archive-{ui_context.board['id']}")).to_be_disabled()


@when('I attempt to create a card with a title over 120 characters')
def ui_card_title_too_long(page, ui_context: UiContext):
    long_title = "a" * 121
    todo_column = page.get_by_test_id("column-todo")
    ui_context.card_count = todo_column.get_by_test_id(re.compile(r"^card-")).count()
    page.get_by_test_id("card-title-input").fill(long_title)
    page.get_by_test_id("card-save").click()


@then('a card title validation error is shown')
def ui_card_title_error(page):
    expect(page.get_by_test_id("card-error")).to_contain_text(
        "Card title must be 120 characters or less."
    )


@then('no new card is created in column "Todo"')
def ui_no_new_card(page, ui_context: UiContext):
    todo_column = page.get_by_test_id("column-todo")
    after_count = todo_column.get_by_test_id(re.compile(r"^card-")).count()
    assert after_count == ui_context.card_count
