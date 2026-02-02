import os
import re
import time
from dataclasses import dataclass
from typing import Dict

from playwright.sync_api import Page, expect

UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:5173")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
API_ORIGIN = API_BASE_URL.split("/api/v1")[0]


@dataclass
class LoginResult:
    token: str
    tenantId: str
    role: str


class AppPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        self.page.goto(UI_BASE_URL)

    def login(self, email: str, password: str, remember: bool = False) -> LoginResult:
        self.page.get_by_test_id("login-email").fill(email)
        self.page.get_by_test_id("login-password").fill(password)
        remember_box = self.page.get_by_test_id("login-remember")
        if remember:
            remember_box.check()
        else:
            remember_box.uncheck()

        with self.page.expect_response(
            lambda response: response.url.endswith("/api/v1/auth/login")
            and response.request.method == "POST"
        ) as response_info:
            self.page.get_by_test_id("login-submit").click()

        response = response_info.value
        assert response.ok, f"Login failed with status {response.status}"
        data: Dict[str, str] = response.json()
        expect(self.page.get_by_test_id("boards-new")).to_be_visible()
        return LoginResult(**data)

    def board_rows(self):
        return self.page.get_by_test_id(re.compile(r"^board-row-"))

    def create_board(self, name: str) -> Dict[str, str]:
        self.page.get_by_test_id("boards-name-input").fill(name)
        with self.page.expect_response(
            lambda response: response.url.endswith("/api/v1/boards")
            and response.request.method == "POST"
        ) as response_info:
            self.page.get_by_test_id("boards-save").click()

        response = response_info.value
        assert response.status == 201, f"Create board failed with status {response.status}"
        board = response.json()
        expect(self.page.get_by_test_id(f"board-row-{board['id']}")).to_be_visible()
        return board

    def rename_board(self, board_id: str, new_name: str) -> None:
        self.page.get_by_test_id(f"board-rename-{board_id}").click()
        self.page.get_by_test_id("boards-rename-input").fill(new_name)
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/v1/boards/{board_id}")
            and response.request.method == "PATCH"
        ) as response_info:
            self.page.get_by_test_id("boards-rename-save").click()
        response = response_info.value
        assert response.ok, f"Rename board failed with status {response.status}"

    def archive_board(self, board_id: str) -> None:
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/v1/boards/{board_id}")
            and response.request.method == "PATCH"
        ) as response_info:
            self.page.get_by_test_id(f"board-archive-{board_id}").click()
        response = response_info.value
        assert response.ok, f"Archive board failed with status {response.status}"

    def open_board(self, board_id: str) -> None:
        self.page.get_by_test_id(f"board-open-{board_id}").click()
        expect(self.page.get_by_test_id("column-todo")).to_be_visible()

    def create_card(self, title: str, description: str = "", column: str = "Todo") -> Dict[str, str]:
        self.page.get_by_test_id("card-title-input").fill(title)
        self.page.get_by_test_id("card-desc-input").fill(description)
        self.page.get_by_test_id("card-column-select").select_option(column)
        with self.page.expect_response(
            lambda response: response.url.endswith("/api/v1/cards")
            and response.request.method == "POST"
        ) as response_info:
            self.page.get_by_test_id("card-save").click()

        response = response_info.value
        assert response.status == 201, f"Create card failed with status {response.status}"
        card = response.json()
        expect(self.page.get_by_test_id(f"card-{card['id']}")).to_be_visible()
        return card

    def drag_card_to_column(self, card_id: str, column_test_id: str) -> None:
        card_locator = self.page.get_by_test_id(f"card-{card_id}")
        target = self.page.get_by_test_id(column_test_id)
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/v1/cards/{card_id}")
            and response.request.method == "PATCH"
        ) as response_info:
            card_locator.drag_to(target)
        response = response_info.value
        assert response.ok, f"Move card failed with status {response.status}"
        expect(target.get_by_test_id(f"card-{card_id}")).to_be_visible()

    def card_in_column(self, card_id: str, column_test_id: str) -> None:
        target = self.page.get_by_test_id(column_test_id)
        expect(target.get_by_test_id(f"card-{card_id}")).to_be_visible()

    def get_session_cookie(self) -> Dict[str, object]:
        cookies = self.page.context.cookies(API_ORIGIN)
        for cookie in cookies:
            if cookie.get("name") == "session":
                return cookie
        return {}

    @staticmethod
    def is_cookie_approx_max_age(cookie: Dict[str, object], seconds: int, tolerance: int = 300) -> bool:
        expires = cookie.get("expires", 0)
        if not isinstance(expires, (int, float)) or expires <= 0:
            return False
        delta = abs(expires - (time.time() + seconds))
        return delta <= tolerance
