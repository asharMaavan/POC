import os
import httpx

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


def api_login(email: str, password: str) -> str:
    response = httpx.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password, "rememberMe": False},
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()["token"]


def api_create_board(token: str, name: str) -> dict:
    response = httpx.post(
        f"{API_BASE_URL}/boards",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name},
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


def api_list_boards(token: str, include_archived: bool = True) -> list:
    response = httpx.get(
        f"{API_BASE_URL}/boards",
        headers={"Authorization": f"Bearer {token}"},
        params={"includeArchived": str(include_archived).lower()},
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()
