import os

import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


@pytest.fixture()
def login(base_url):
    def _login(email: str, password: str = "Password123!", remember_me: bool = False):
        import httpx

        response = httpx.post(
            f"{base_url}/auth/login",
            json={"email": email, "password": password, "rememberMe": remember_me},
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        token = data["token"]
        return {
            "token": token,
            "tenantId": data["tenantId"],
            "role": data["role"],
            "cookies": response.cookies,
        }

    return _login
