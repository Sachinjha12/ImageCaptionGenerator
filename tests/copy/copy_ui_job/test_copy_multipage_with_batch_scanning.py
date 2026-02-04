import logging
import pytest
from time import sleep
from typing import ClassVar

from dunetuf.copy.copy import Copy
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

TIMEOUT = 15.0
CHANGE_SETTINGS_JOB_CREATED={'colorMode': 'Grayscale'}
CHANGE_SETTINGS_SECOND_JOB={'originalPaperType': 'blueprint','resolution':'300Dpi', 'copies': 2}
CHANGE_SETTINGS_BETWEEN_PAGES={'contentType': 'Image'}

def load_page(cdm, scan_action, cp_app, copy_instance, check_button_enable=True):
    '''Load a page and wait for the copy button to be present

    Args:
        cdm : CDM library
        scan_action : Scan common Library action
        cp_app (_type_): Copy App Workflow Operation Library
        copy_instance (_type_): Copy Dunetuff Instance
    '''
    scan_action.load_media()
    # Copy button presence ensure that scanning is finished
    # and avoids race condition with states
    is_done_button_flow = False
    if check_button_enable:
        cp_app.wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance, timeout=TIMEOUT)
    else:
        cp_app.wait_for_acquisition_finished(copy_instance, timeout=TIMEOUT)
        is_done_button_flow = True

    cp_app.wait_main_button_to_finish_copy(cdm,is_done_button=is_done_button_flow)


def finish_job(spice, job, printjob, last_job_id):
    '''Finish current Job and check result

    Args:
        spice : UI library
        job: Job Engine library
        prinjob: Print Common Job Library
        last_job_id (num): previous job id to check new id of job
    '''
    # Finish Copy
    spice.copy_app.finish_copy()

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id)
    assert job_id != last_job_id, "The new job has not been generated"
    printjob.wait_for_job_completion(job_id)
    status_job = job.get_status_job(job_id)
    job.validate_completion_success_status_job(status_job)
    return job_id

def check_job_stats(cdm, scanned_pages=1, requested_copies=1):
    # Read Data from stats Job 
    # Check if the history stats returns success
    # ! IF TEST FAILS HERE, PROBABLY IS CAUSED BECAUSE CLONE TICKET IS CLONING PREVIOUS USED TICKET, INSTEAD OF CLONE DEFAULT AND INJECT LAST USED VALUES
    # ! THIS IS NOT SUPPORTED CURRENTLY; BECAUSE CLONE TICKET WITH PAGE GENERATED WILL BE CONSIDERED AS A REPRINT OF COPY JOB BY JOB FRAMEWORK INFRASTRUCTURE
    response = cdm.get_raw(cdm.JOB_HISTORY_STATS_ENDPOINT)
    assert response.status_code==200, 'Unexpected response'
    job_scan_info_stats = response.json()["historyStats"][-1]
    expected_impression_count = scanned_pages * requested_copies

    logging.info(job_scan_info_stats)
    assert job_scan_info_stats['printInfo']['impressionCount']                             == expected_impression_count,   "Number of printed pages mismatch"
    assert job_scan_info_stats['printInfo']['printSettings']['requestedImpressionCount']   == expected_impression_count,   "Incorrect requestedImpressionCount"
    assert job_scan_info_stats['printInfo']['copiesCount']                                 == requested_copies,            "Number of copies count mismatch"
    assert job_scan_info_stats['printInfo']['printSettings']['requestedCopiesCount']       == requested_copies,            "Incorrect requestedCopiesCount"
    assert job_scan_info_stats['scanInfo']['scannedPageCount']                             == scanned_pages,               "Incorrect scanned page count"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test to check batch scanning in copy with changing some settings between, before and after a job, running two jobs at least and check the job stats
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:LFPSWQAA-4942
    +timeout:300
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_multipage_with_batch_scanning 
    +test:
        +title:test_copy_multipage_with_batch_scanning
        +guid: 0aa51834-c6f4-11ec-9488-87df685cb8c0
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_multipage_with_batch_scanning(setup_teardown_print_device, copy_page_sensor_setup, spice, cdm, udw, job, printjob, net, locale: str = "en"):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw).set_cdm(cdm)
    copy_instance = Copy(cdm, udw)
    last_job_id = job.get_last_job_id()
    cp_app = spice.copy_ui()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

    # Go to Copy App.
    cp_app.goto_copy()

    # Check buttons and Unload current media.
    cp_app.startscan_button_present(spice, TIMEOUT)
    cp_app.eject_button_present(spice, TIMEOUT)
    cp_app.press_eject_button(spice)
    cp_app.copy_button_present(spice, TIMEOUT)

    # Check number of copies default value
    assert spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies)["value"] == 1

    # Change some settings
    cp_app.goto_select_setting_with_payload_and_back_landing_view(udw, net, CHANGE_SETTINGS_JOB_CREATED)

    # Wait for and check "Insert page in scanner" msg
    cp_app.press_copy_button(spice)
    
    # Check that "Insert page in scanner" message appears
    expected_msg = LocalizationHelper.get_string_translation(net, "cInsertPageInScanner", locale)
    screen_text = cp_app.get_insert_page_msg(spice)
    # Check expected Msg
    assert screen_text == expected_msg

    # Scan First Page
    load_page(cdm, scan_action, cp_app, copy_instance)

    # Wait until the toast is no longer visible, change certain settings and eject the media
    cp_app.eject_button_present(spice, TIMEOUT)
    cp_app.press_eject_button(spice)
    # Wait until there is no toast visible, change certain settings while a toast is visible of a combo box could cause an issue
    cp_app.wait_for_copy_status_toast_is_not_visible()
    cp_app.goto_select_setting_with_payload_and_back_landing_view(udw, net, CHANGE_SETTINGS_BETWEEN_PAGES)

    # Scan Second Page and Finish
    load_page(cdm, scan_action, cp_app, copy_instance)
    last_job_id = finish_job(spice, job, printjob, last_job_id)
    check_job_stats(cdm, scanned_pages=2, requested_copies=1)

    # SECOND JOB IN SAME SESSION
    # Wait until there is no toast visible, change certain settings while a toast is visible of a combo box could cause an issue
    cp_app.wait_for_copy_status_toast_is_not_visible()
    cp_app.goto_select_setting_with_payload_and_back_landing_view(udw, net, CHANGE_SETTINGS_SECOND_JOB)
    
    # Run second job
    load_page(cdm, scan_action, cp_app, copy_instance)
    finish_job(spice, job, printjob, last_job_id)
    check_job_stats(cdm, scanned_pages=1, requested_copies=2)
    
    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test to check batch scanning in copy with changing some settings between, before and after a job, running two jobs at least in direct copy and check the job stats
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-237980
    +timeout:300
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_multipage_with_batch_scanning_direct_copy 
    +test:
        +title:test_copy_multipage_with_batch_scanning_direct_copy
        +guid: 37920540-ff64-11ef-8c15-4fc71ff68fd8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_multipage_with_batch_scanning_direct_copy(setup_teardown_print_device, copy_page_sensor_setup_force_direct_copy_mode, spice, cdm, udw, job, printjob, net, locale: str = "en"):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw).set_cdm(cdm)
    copy_instance = Copy(cdm, udw)
    last_job_id = job.get_last_job_id()
    cp_app = spice.copy_ui()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

    # Go to Copy App.
    cp_app.goto_copy()

    # Check buttons and Unload current media.
    cp_app.startscan_button_present(spice, TIMEOUT)
    cp_app.eject_button_present(spice, TIMEOUT)
    cp_app.press_eject_button(spice)
    cp_app.copy_button_present(spice, TIMEOUT)

    # Check number of copies default value
    assert spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies)["value"] == 1

    # Change some settings
    cp_app.goto_select_setting_with_payload_and_back_landing_view(udw, net, CHANGE_SETTINGS_JOB_CREATED)

    # Wait for and check "Insert page in scanner" msg
    cp_app.press_copy_button(spice)
    
    # Check that "Insert page in scanner" message appears
    expected_msg = LocalizationHelper.get_string_translation(net, "cInsertPageInScanner", locale)
    screen_text = cp_app.get_insert_page_msg(spice)
    # Check expected Msg
    assert screen_text == expected_msg

    # Scan First Page
    load_page(cdm, scan_action, cp_app, copy_instance, check_button_enable=False)

    # Wait until the toast is no longer visible, change certain settings and eject the media
    cp_app.eject_button_present(spice, TIMEOUT)
    cp_app.press_eject_button(spice)
    # Wait until there is no toast visible, change certain settings while a toast is visible of a combo box could cause an issue
    cp_app.wait_for_copy_status_toast_is_not_visible()
    cp_app.goto_select_setting_with_payload_and_back_landing_view(udw, net, CHANGE_SETTINGS_BETWEEN_PAGES)

    # Scan Second Page and Finish
    load_page(cdm, scan_action, cp_app, copy_instance, check_button_enable=False)
    last_job_id = finish_job(spice, job, printjob, last_job_id)
    check_job_stats(cdm, scanned_pages=2, requested_copies=1)

    # SECOND JOB IN SAME SESSION
    # Wait until there is no toast visible, change certain settings while a toast is visible of a combo box could cause an issue
    cp_app.wait_for_copy_status_toast_is_not_visible()
    cp_app.goto_select_setting_with_payload_and_back_landing_view(udw, net, CHANGE_SETTINGS_SECOND_JOB)
    
    # Run second job
    load_page(cdm, scan_action, cp_app, copy_instance, check_button_enable=False)
    finish_job(spice, job, printjob, last_job_id)
    check_job_stats(cdm, scanned_pages=1, requested_copies=2)
    
    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)