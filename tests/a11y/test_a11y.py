# import pytest
# from axe_playwright_python.sync_playwright import Axe

# pytestmark = pytest.mark.a11y


# @pytest.mark.parametrize("path", ["/", "/auth/login"])
# def test_no_critical_a11y_violations(page, path):
#     page.goto(path)
#     page.wait_for_load_state("networkidle")
#     violations = Axe().run(page).response["violations"]
#     serious = [v for v in violations if v["impact"] in ("critical", "serious")]
#     assert not serious, [(v["id"], v["impact"], len(v["nodes"])) for v in serious]