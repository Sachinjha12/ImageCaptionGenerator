import pytest
import os
from dunetuf.ews.helper import EwsHelper

@pytest.fixture
def helper(ews):
    yield EwsHelper(ews)


# Hook to make test results available in fixtures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Passes test outcome to fixtures
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def cleanup(request, ews):
    """
    Capture the log if the test is a failure
    """
    yield
    if request.node.rep_call.failed:
        logpath = request.config.option.capture_logs_to
        logpath = logpath if logpath else os.path.join("/code/output/")
        current_test = os.environ.get("PYTEST_CURRENT_TEST").split("::")[1]
        ews.helper.get_browser_console_log(logpath, current_test)
        ews.helper.get_browser_performance_log(logpath, current_test)
