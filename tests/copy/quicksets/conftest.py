import os
import pytest
from dunetuf.send.email.email import *
from dunetuf.send.folder.folder import Folder
from dunetuf.send.common import common
import time
from dunetuf.ews.helper import EwsHelper


@pytest.fixture
def default_email_server(request, cdm, udw):
    email = Email(cdm, udw)
    email.start_email_server()
    email.create_email_profile("profile1", True)
    
    yield "profile1"

    email.delete_all_email_profiles()
    email.stop_email_server(request)

@pytest.fixture
def custom_email_server(request, cdm, udw):
    email = Email(cdm, udw)
    email.start_email_server()
    email.create_email_profile("profile1")
    
    yield "profile1"

    email.delete_all_email_profiles()
    email.stop_email_server(request)

@pytest.fixture
def setup_teardown_folder_server(cdm, udw, request):
    folder = Folder(cdm, udw)
    folder.set_up_folder_server(specific_password=True)
    folder_path, user_name, password = folder.get_server_details()
    
    yield folder_path, user_name, password

    folder.tear_down_folder_server(request)

@pytest.fixture
def setup_teardown_folder_server_credentials(cdm, udw, request):
    folder = Folder(cdm, udw)
    folder.set_up_folder_server(specific_password=True, credentials={"user":"dsuser01", "password":"Pass1701"})
    folder_path, user_name, password = folder.get_server_details()
    
    yield folder_path, user_name, password

    folder.tear_down_folder_server(request)

@pytest.fixture
def setup_teardown_usb_device(usbdevice, ssh):
    logging.info("remove all the mock devices")
    usbdevice.remove_all_mock_devices(ssh)

    if not usbdevice.check_device("usbdisk1"):
        logging.info('Adding USB mock device')
        usbdevice.add_mock_device('usbdisk1', 'UsbDisk1', 'frontUsb')

    yield
 
    logging.info("remove all the mock devices")
    usbdevice.remove_all_mock_devices(ssh)

@pytest.fixture
def setup_teardown_flatbed(cdm, udw):
    x = common.Common(cdm, udw)
    scan_resource = x.scan_resource()

    if scan_resource == "ADF":
        logging.info('Load document on Flatbed')
        udw.mainApp.ScanMedia.unloadMedia("ADF")

    yield
    
    if scan_resource == "MDF":
        udw.mainApp.ScanMedia.loadMedia("MDF")
    else:
        udw.mainApp.ScanMedia.loadMedia("ADF")

@pytest.fixture
def setup_teardown_quickset(spice, ews, job, cdm):
    """Default setup/teardown fixture for send to email quickset tests."""

    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    logging.info("bookmark jobs")
    job.bookmark_jobs()

    yield

    ews.quicksets_app.csc.delete_all_shortcuts()
    time.sleep(2)
    ews.close_browser()
    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    job.clear_joblog()
    spice.goto_homescreen()


@pytest.fixture(autouse=True)
def teardown_signout(spice):
    """
    check if the user is signed in, if so sign out
    """
    yield
    spice.goto_homescreen()
    spice.wait_ready()
    if spice.signIn.is_signed_in():
        spice.signIn.goto_universal_sign_in("Sign Out")

@pytest.fixture
def setup_teardown_no_delete_quickset(spice, ews, job):
    """Default setup/teardown fixture for send to email quickset tests."""

    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    logging.info("bookmark jobs")
    job.bookmark_jobs()

    yield

    ews.close_browser()
    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    job.clear_joblog()
    spice.goto_homescreen()

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
    # if request.node.rep_call.failed and (ews.driver is not None):
    if ews.driver is not None:
        if request.node.rep_call.failed:
            logpath = request.config.option.capture_logs_to
            logpath = logpath if logpath else os.path.join('/code/output/')
            current_test = os.environ.get('PYTEST_CURRENT_TEST').split('::')[1]
            ews.helper.get_browser_console_log(logpath, current_test)
            ews.helper.get_browser_performance_log(logpath, current_test)
