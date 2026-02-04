import time
import logging
import pytest
from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check queue after copy job
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:LFPSWQAA-5475
    +timeout:420
    +asset:LFP
    +test_framework:TUF
    +external_files:combo_SWOP_embedded.jpg=d9904a956bcf378816ff4f2c5c7ef8c6b8e03a68f7bcdad1aa0a47f218508b88
    +name:test_ui_copy_multipage_and_check_queue
    +test:
        +title:test_ui_copy_multipage_and_check_queue
        +guid:14c74cd2-0fbd-4338-9024-6fa7361d4273
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy
    +delivery_team:LFP
    +feature_team:LFP_SOHO&SMB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_ui_copy_multipage_and_check_queue(spice, job, udw, printjob, net, configuration):
    # Wait for HomeScreen to appear and dismiss SystemError if exists
    spice.cleanSystemEventAndWaitHomeScreen()
    
    # Send job to print
    printjob.print_verify('d9904a956bcf378816ff4f2c5c7ef8c6b8e03a68f7bcdad1aa0a47f218508b88', timeout = 250)
    
    # Get last job
    last_job_id = job.get_last_job_id_cdm()
    
    # Go to Copy App
    spice.copy_ui().goto_copy_from_copyapp_at_home_screen()
    
    # Ensure media is unloaded
    unload_plot(udw)
    
    # Check number of copies default value
    assert spice.wait_for(CopyAppWorkflowObjectIds.spinBox_numberOfCopies)["value"] == 1
    
    # Change some settings
    spice.copy_ui().ui_copy_set_no_of_pages(5)
    spice.copy_ui().select_color_mode_landing("Grayscale")
    
    # Check Scanner waiting for plot to start
    spice.copy_ui().copy_button_present(spice)
    spice.copy_ui().press_copy_button(spice)
    time.sleep(3)

    # Check "Insert page in scanner" message
    check_insert_page_msg(spice,net)

    # Load plot
    load_plot(udw)
    time.sleep(5)
    
    # Start printing by pressing "Done" button
    spice.copy_ui().done_button_present(spice)
    spice.copy_ui().press_done_button(spice)
    
    # The eject screen is only present in Beam
    if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
        spice.wait_for(CopyAppWorkflowObjectIds.copy_release_pagePrompt_pagebtn).mouse_click() 
    
    # Get last job in the printing queue
    queue = job.get_job_queue()
    queue_job_id = queue[-1]["jobId"]

    # Wait until copy job is completed
    if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
        logging.info("The test is running on Beam: Waiting for copy completion window and click OK")
        spice.copy_ui().wait_for_copy_completion_window_and_click_ok(spice, net)
    else:
        logging.info("The test is running on Jupiter: Waiting for copy complete toast")
        spice.copy_ui().wait_and_validate_copy_complete_toast(spice, net)

    # Go to Job Queue App
    spice.goto_homescreen()
    spice.main_app.goto_job_queue_app()
    
    # Check copy job
    spice.job_ui.goto_job(queue_job_id)
    job.wait_for_job_completion_cdm(queue_job_id)
    time.sleep(2)
    assert spice.job_ui.recover_job_status() == "Completed"
    
    # Check that last job is present
    spice.job_ui.goto_job(last_job_id)
    assert spice.job_ui.recover_job_status() == "Completed"


def load_plot(udw):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    Control.validate_result(scan_action.load_media("MDF"))
    
def unload_plot(udw):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    Control.validate_result(scan_action.unload_media("MDF"))
    
def check_insert_page_msg(spice,net):
    # Check that "Insert page in scanner" message appears
    expected_msg = LocalizationHelper.get_string_translation(net, "cInsertPageInScanner")
    screen_text = spice.copy_ui().get_insert_page_msg(spice)
    # Check expected Msg
    assert screen_text == expected_msg
    

@pytest.fixture(autouse=True)
def setup_teardown_copy_multipage(spice, tclMaia, tcl):

    logging.info('-- SETUP (Copy Multipage Tests) --')

    # ---- Setup Maia Ready ----
    try:
        tclMaia.execute("setEmulatorReady",  recvTimeout=10)
    except ConnectionRefusedError:
        logging.info('The setEmulatorReady command not supported!')
    
    # ---- Setup For EngineSimulatorUw ----  
    try:
        tcl.execute("EngineSimulatorUw executeSimulatorAction PRINT setPrintSimulationConfiguration {{ printTimePerPageInMilliseconds: 10000 }}")
    except OSError:
        logging.info('The EngineSimulatorUw command not supported!')

    # Wait for HomeScreen to appear
    spice.cleanSystemEventAndWaitHomeScreen()
    spice.goto_homescreen()

    yield

    logging.info('-- TEARDOWN (Copy Multipage Tests) --')

    # Wait for HomeScreen to appear
    spice.goto_homescreen()
