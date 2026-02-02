from pathlib import Path

import pytest

ARTIFACTS_DIR = Path("reports") / "playwright"


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def capture_playwright_artifacts(page, request):
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    failed = getattr(request.node, "rep_call", None)
    if failed and failed.failed:
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace("::", "_")
        page.screenshot(path=str(ARTIFACTS_DIR / f"{safe_name}.png"), full_page=True)
        page.context.tracing.stop(path=str(ARTIFACTS_DIR / f"{safe_name}.zip"))
    else:
        page.context.tracing.stop()
