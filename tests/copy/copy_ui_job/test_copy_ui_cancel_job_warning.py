import uuid
import logging
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Cancel Copy Job Warning Prompt when user press home Button in CopyApp and Cancel Job 
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-102306
    +timeout:120
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_warning_prompt_on_home_event_then_cancel_job_in_preview_state
    +test:
        +title:test_copy_ui_validate_cancel_job_warning_prompt_on_home_event_then_cancel_job_in_preview_state
        +guid:1693ff2c-4110-430b-9844-5f8a2e0384dc
        +dut:
            +type:Simulator
            +configuration: DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy= ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_cancel_job_warning_prompt_on_home_event_then_cancel_job_in_preview_state(spice, job, udw, setup_teardown_print_device):

    logging.info("load MDF")
    udw.mainApp.ScanMedia.loadMedia("MDF")

    home = spice.main_app.get_home()
    spice.main_app.wait_locator_visible(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    spice.main_app.goto_copy_app()

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait a few to avoid cancel when job is not started properly
    job.wait_for_active_jobs()
    
    spice.scan_settings.goto_homescreen_with_ongoing_scan_job()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test Cancel Copy Job Warning Prompt when user press home Button in CopyApp and then don't cancel
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-102306
    +timeout:180
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_warning_prompt_on_home_event_then_do_not_cancel_in_preview_state
    +test:
        +title:test_copy_ui_validate_cancel_job_warning_prompt_on_home_event_then_do_not_cancel_in_preview_state
        +guid:41e09bc6-0642-4f4e-9688-a13a0dcb5f9f
        +dut:
            +type:Simulator
            +configuration: DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy= ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_cancel_job_warning_prompt_on_home_event_then_do_not_cancel_in_preview_state(spice, udw, job, setup_teardown_print_device):
    logging.info("load MDF")
    udw.mainApp.ScanMedia.loadMedia("MDF")

    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    spice.main_app.goto_copy_app()

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait a few to avoid cancel when job is not started properly
    job.wait_for_active_jobs()
    
    spice.copy_app.goto_home()
    spice.scan_settings.cancel_current_job_modal_alert(cancel_job=False)

    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    spice.copy_app.goto_home()
    spice.scan_settings.cancel_current_job_modal_alert(cancel_job=True)

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Cancel Copy Job from not home action button then copy app should still there without crashes
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-175557
    +timeout:180
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_externally_and_copy_app_return_to_idle_state
    +test:
        +title:test_copy_ui_validate_cancel_job_externally_and_copy_app_return_to_idle_state
        +guid:671f3498-bf8e-11ee-9c7c-bf36ae843ba4
        +dut:
            +type:Simulator
            +configuration: DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_cancel_job_externally_and_copy_app_return_to_idle_state(spice, job, udw, setup_teardown_print_device):
    logging.info("load MDF")
    udw.mainApp.ScanMedia.loadMedia("MDF")

    # Check that init in home and go to copy app
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_visible(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    spice.main_app.goto_copy_app()

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for new jobs to avoid cancel when job is not started properly
    job.wait_for_active_jobs()
    job_ids = job.get_active_jobs()
    assert len(job_ids) > 0, "No job ids found"
    new_job_id = job_ids[-1].get('jobId')
    
    # Check if the new job has been generated
    job.cancel_active_jobs()

    # Wait for the new job completion and Get Job ID
    job.wait_canceled_job(new_job_id)

    # Validate current state of app
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)
    
    # Check start button is present
    spice.copy_ui().startscan_button_present(spice)

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
