import logging
import pytest

from tests.ui.lib.actions.commonsActions import *

from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.control.control import Control
from dunetuf.copy.copy import Copy

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test will force the clipping message trying to print more than the maximum (9501mm)
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-82741
    +timeout:240
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_ui_clipping
    +test:
        +title: test_copy_ui_clipping
        +guid: 7b70ee8a-a7b8-11ed-adca-6fa9a08a551b
        +dut:
            +type:Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.skip(reason="This test fails in S3/PI for unknown reasons in wait_main_button_to_finish_copy step. Skipping while this can be investigated.")
def test_copy_ui_clipping(spice, cdm, udw, tcl, job, setup_teardown_homescreen):
    # Get Job ID
    GENERAL_PREVIEW_TIMEOUT=30
    last_job_id = job.get_last_job_id()

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw)
    copy_instance = Copy(cdm, udw)

    # max size length supported 8 A0= 9504 we want get over it so we set 10000mm height
    simulation = scan_action.set_scan_random_acquisition_mode(10000, 297)
    Control.validate_simulation(simulation)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))
    spice.main_app.goto_copy_app()
    spice.copy_ui().wait_for_copy_landing_view()
    spice.copy_ui().wait_main_button_to_start_copy(cdm)

    # Start Copy
    logging.info( "Starting copy" )
    spice.copy_app.start_copy()

    #check for sample message
    spice.scan_settings.verify_clip_in_scanner_screen(timeout=180.0)

    #acknowledge event
    spice.scan_settings.click_ok_on_alert_dialog()

    # Dismiss clip alert
    scan_action.set_scan_state(1)

    # Wait until the copy button is enabled. Timeout of 30 is required since the preview loading time is high
    copy_instance.wait_for_corresponding_scanner_status_with_cdm("Idle", timeout=GENERAL_PREVIEW_TIMEOUT)
    spice.scan_settings.wait_for_preview_n(1, timeout=GENERAL_PREVIEW_TIMEOUT)
    spice.copy_ui().wait_main_button_to_finish_copy(cdm, max_timeout=GENERAL_PREVIEW_TIMEOUT)

    # Finish Copy
    spice.copy_app.finish_copy()

    # Wait for the new job completion and Get Job ID, do extended wait for final processing
    job_id = job.print_completed_job(last_job_id,180)

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    scan_action.reset_simulation_mode()
