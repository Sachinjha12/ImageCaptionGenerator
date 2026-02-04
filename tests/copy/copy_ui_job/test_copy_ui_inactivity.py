import logging
import pytest
from time import sleep
import dunetuf.common.commonActions as CommonActions

from dunetuf.scan.ScanAction import ScanAction
from dunetuf.control.control import Control

INACTIVITY_TIMEOUT_100 = 30 # 100% of inactivity
INACTIVITY_TIMEOUT_095 = 25 # 95% of inactivity
INACTIVITY_TIMEOUT_010 = 10 # 10% of inactivity

def enter_copy_app_and_wait_nearest_to_inactivity_timeout(spice, inactivity_wait_expected=INACTIVITY_TIMEOUT_095):
    '''Method to enter the copy app and wait for the nearest to the inactivity timeout to check if the app is still active.
    current time is 
    Args:
        spice (tuf): library to interact with the device ui
        inactivity_wait_expected(int): time to wait for the app to be active before checking if it is still active.

    Returns:
        copy_app: qml pointer object to copy app
    '''
    # Enter app, wait 95% of timeout and check we are in app.
    spice.copy_ui().goto_copy()
    copy_app = spice.copy_app.get_copy_app()
    sleep(inactivity_wait_expected)
    spice.validate_app(copy_app, False)
    return copy_app

def start_copy_and_wait_nearest_to_inactivity_timeout(spice, cdm, copy_app):
    # Start Copy, insert media and wait 95% of timeout.
    spice.copy_app.start_copy()
    expected_copy_text_button = CommonActions.get_translated_text_in_device_language(cdm, spice.copy_app.locators.copy_string_id_button)
    spice.copy_app.wait_until_text_button(spice.copy_app.locators.copy_button, expected_copy_text_button)
    sleep(INACTIVITY_TIMEOUT_095)
    spice.validate_app(copy_app, False)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This tests checks that the system goes back to HS when the inactivity timeout is fired.
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-156155
    +timeout:180
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_ui_mdf_menucopy_inactivity
    +test:
        +title: test_copy_ui_mdf_menucopy_inactivity
        +guid: b0ff74f2-5dea-11ee-9a64-07207b1741ac
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menucopy_inactivity(spice, copy_configure_inactivity_30_seconds_scan_prepared):
    enter_copy_app_and_wait_nearest_to_inactivity_timeout(spice)

    # Wait until timeout hits and check we are in HS.
    sleep(INACTIVITY_TIMEOUT_010)
    assert spice.is_HomeScreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks that the inactivity timer is reset after a page is scanned and after that the cancel prompt appears.
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-156155
    +timeout:180
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_ui_mdf_menucopy_inactivity_reset_after_scan
    +test:
        +title: test_copy_ui_mdf_menucopy_inactivity_reset_after_scan
        +guid: 90f69518-5df0-11ee-9471-7b73650820e8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menucopy_inactivity_reset_after_scan(spice, cdm, copy_configure_inactivity_30_seconds_scan_prepared):
    copy_app = enter_copy_app_and_wait_nearest_to_inactivity_timeout(spice)
    start_copy_and_wait_nearest_to_inactivity_timeout(spice, cdm, copy_app)

    # After 10% more of the timout, check we are in HS
    sleep(INACTIVITY_TIMEOUT_010)
    assert spice.wait_for("#CancelJobWarningPrompt")
    cancelButton = spice.wait_for("#cancelJobWarningSecondaryButton")
    cancelButton.mouse_click()
    assert spice.is_HomeScreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks that the inactivity timer is reset after twp page are scanned and after that the cancel prompt appears, and go to home occurs as expected
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-156155
    +timeout:180
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_ui_mdf_menucopy_inactivity_reset_after_second_scan_waiting_return_to_home_automatically
    +test:
        +title: test_copy_ui_mdf_menucopy_inactivity_reset_after_second_scan_waiting_return_to_home_automatically
        +guid: 5777744e-00c2-11f0-84b4-977f8fbc5ca1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menucopy_inactivity_reset_after_second_scan_waiting_return_to_home_automatically(spice, cdm, udw, 
        copy_configure_inactivity_30_seconds_scan_prepared):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_app = enter_copy_app_and_wait_nearest_to_inactivity_timeout(spice)
    start_copy_and_wait_nearest_to_inactivity_timeout(spice, cdm, copy_app)

    # Start a second scan, insert media and wait 95% of timeout.
    Control.validate_result(scan_action.load_media("MDF"))
    expected_copy_text_button = CommonActions.get_translated_text_in_device_language(cdm, spice.copy_app.locators.copy_string_id_button)
    spice.copy_app.wait_until_text_button(spice.copy_app.locators.copy_button, expected_copy_text_button)
    sleep(INACTIVITY_TIMEOUT_095)
    spice.validate_app(copy_app, False)

    # After 10% more of the timout, check we are in HS
    sleep(INACTIVITY_TIMEOUT_010)
    assert spice.wait_for("#CancelJobWarningPrompt")
    sleep(INACTIVITY_TIMEOUT_100)
    assert spice.is_HomeScreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: check that inactivityTimer quits copy app when the scanner cover is open.
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-156155
    +timeout:180
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_ui_mdf_menucopy_inactivity_with_cover_open
    +test:
        +title: test_copy_ui_mdf_menucopy_inactivity_with_cover_open
        +guid: 7402145e-8eca-11ee-9486-5b830e89776b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing & InactivityTimeout=2Minutes
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menucopy_inactivity_with_cover_open(spice, udw, copy_configure_inactivity_30_seconds_scan_prepared):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Open Cover.
    scan_action.set_scan_state(3)

    # Dismiss prompt.
    hideButton = spice.wait_for("#closeButton")
    hideButton.mouse_click()

    enter_copy_app_and_wait_nearest_to_inactivity_timeout(spice)

    # After 10% more of the timout, check we are in HS.
    sleep(INACTIVITY_TIMEOUT_010)

    # Dismiss prompt, it should have been shown again.
    hideButton = spice.wait_for("#closeButton")
    hideButton.mouse_click()

    # We are in HS without needed user interaction.
    assert spice.is_HomeScreen()
