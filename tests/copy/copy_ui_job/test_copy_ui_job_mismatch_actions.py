import pytest
import time

from dunetuf.copy.copy import Copy
from dunetuf.ui.uioperations.WorkflowOperations.JobAppWorkflowObjectIds import JobAppWorkflowObjectIds

def run_copy_and_wait_finished(cdm, udw, spice, check_button_enable=True):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().wait_for_copy_landing_view()
    spice.copy_app.start_copy()

    if check_button_enable:
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    else:
        spice.copy_ui().wait_for_acquisition_finished(Copy(cdm, udw))

def run_and_finish_copy_job(cdm, udw, spice):
    run_copy_and_wait_finished(cdm, udw, spice)
    spice.copy_app.finish_copy()

def validate_job_completion_status(job, cdm, status="success"):
    # Check Completion status
    job.wait_for_no_active_jobs(time_out=30)
    job.check_job_log_by_status_and_type_cdm([{"type": "copy", "status": status}], time_out=30)
    job.verify_jobdetails_stats_data(cdm, job, "copy", 1, 1)

def select_media_input_in_ok_state_and_reset_size(spice, tray):
    # Select roll card and continue
    spice.mediaapp.select_roll_card_in_load_media_from_mismatch_out_of_media_alert()

    # Set media input rolls in ok state
    time.sleep(2) # If set roll state faster than expected, media handling cause a crash. Need a little delay.
    tray.reset_and_load_trays()

''' 
Media Size Mismatches with Indirect Copy Flow
'''
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media input size mismatch and cancel action
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_indirect_copy_media_size_mismatch_and_cancel
    +test:
        +title: test_copy_ui_job_indirect_copy_media_size_mismatch_and_cancel
        +guid: b1bbb64a-9ab5-11ef-a660-9b588da85208
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_indirect_copy_media_size_mismatch_and_cancel(
        job, cdm, udw, spice, net, copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_and_finish_copy_job(cdm, udw, spice)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click cancel button
    spice.job_ui.mismatch_alert_cancel_job()

    # Check Completion status
    validate_job_completion_status(job, cdm, "cancelled")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch and load media
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_indirect_copy_media_size_mismatch_and_load_media
    +test:
        +title: test_copy_ui_job_indirect_copy_media_size_mismatch_and_load_media
        +guid: 968b2af4-9ac4-11ef-9420-0bfdf239177b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_indirect_copy_media_size_mismatch_and_load_media(
        job, cdm, udw, spice, net, tray, copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_and_finish_copy_job(cdm, udw, spice)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_load_media_job()

    # Select roll and reset state of inputs
    select_media_input_in_ok_state_and_reset_size(spice, tray)

    # Check Completion status
    validate_job_completion_status(job, cdm)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media out of paper mismatch and load media without press any button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_indirect_copy_media_size_mismatch_and_resolve_media_without_dismiss_alert
    +test:
        +title: test_copy_ui_job_indirect_copy_media_size_mismatch_and_resolve_media_without_dismiss_alert
        +guid: d6bdefd0-9c45-11ef-bee5-fb6930705bba
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_indirect_copy_media_size_mismatch_and_resolve_media_without_dismiss_alert(
        job, cdm, udw, spice, tray, net, copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_and_finish_copy_job(cdm, udw, spice)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Load any media roll
    time.sleep(1) # If set roll state faster than expected, auto-resume not works as expected because load is received between set to pause is processed.
    tray.reset_trays()

    # Check Completion status
    validate_job_completion_status(job, cdm)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch, press hold and then cancel job
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_indirect_copy_media_size_mismatch_and_hold_then_cancel_job
    +test:
        +title: test_copy_ui_job_indirect_copy_media_size_mismatch_and_hold_then_cancel_job
        +guid: 52200884-9ac5-11ef-9175-6b5127e44554
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_indirect_copy_media_size_mismatch_and_hold_then_cancel_job(
        job, cdm, udw, spice, net, copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_and_finish_copy_job(cdm, udw, spice)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_hold_job()

    # Cancel jobs
    job.cancel_active_jobs()

    # Check Completion status
    validate_job_completion_status(job, cdm, "cancelled")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch, press print anyway
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_indirect_copy_media_size_mismatch_and_print_anyway
    +test:
        +title: test_copy_ui_job_indirect_copy_media_size_mismatch_and_print_anyway
        +guid: 893e2550-9ad2-11ef-8eca-4f948f997e84
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_indirect_copy_media_size_mismatch_and_print_anyway(
        job, cdm, udw, spice, net, copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_and_finish_copy_job(cdm, udw, spice)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_printanyway_job()

    # Check Completion status
    validate_job_completion_status(job, cdm)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch, press hold, load media and expect job completed success
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:200
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_indirect_copy_size_mismatch_and_hold_then_load_media_and_job_is_completed_success
    +test:
        +title: test_copy_ui_job_indirect_copy_size_mismatch_and_hold_then_load_media_and_job_is_completed_success
        +guid: 4d45d7fa-9ac8-11ef-ba18-6747ad38f844
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_indirect_copy_size_mismatch_and_hold_then_load_media_and_job_is_completed_success(
        job, tray, cdm, udw, spice, net, copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_and_finish_copy_job(cdm, udw, spice)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_hold_job()

    # Back to the home screen after finish the job
    spice.goto_homescreen()
    
    # Wait for job to enter into paused state
    job_id = job.get_job_queue()[-1]["jobId"]
    job.check_job_state(job_id, state='paused', timeout=60)

    # Set media input rolls in ok state
    tray.reset_trays()

    # Check Completion status
    validate_job_completion_status(job, cdm)

''' 
Media Size Mismatches with Direct Copy Flow
'''
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media input size mismatch and cancel action
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_direct_copy_media_size_mismatch_and_cancel
    +test:
        +title: test_copy_ui_job_direct_copy_media_size_mismatch_and_cancel
        +guid: 78a07e08-9aca-11ef-8d89-b70f4ff00385
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_direct_copy_media_size_mismatch_and_cancel(
        job, cdm, udw, spice, net, copy_page_sensor_setup_direct_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Start a copy job in UI
    run_copy_and_wait_finished(cdm, udw, spice, check_button_enable=False)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click cancel button
    spice.job_ui.mismatch_alert_cancel_job()

    # Check Completion status
    validate_job_completion_status(job, cdm, "cancelled")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media out of paper mismatch and load media without press any button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_direct_copy_media_size_mismatch_and_resolve_media_without_dismiss_alert
    +test:
        +title: test_copy_ui_job_direct_copy_media_size_mismatch_and_resolve_media_without_dismiss_alert
        +guid: c27eaca6-9c47-11ef-85e3-470cd28fb52e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_direct_copy_media_size_mismatch_and_resolve_media_without_dismiss_alert(
        job, cdm, udw, spice, tray, net, copy_page_sensor_setup_direct_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Do a copy job in UI
    run_copy_and_wait_finished(cdm, udw, spice, check_button_enable=False)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Load any media roll
    time.sleep(1) # If set roll state faster than expected, auto-resume not works as expected because load is received between set to pause is processed.
    tray.reset_and_load_trays()

    # Finish Copy
    spice.copy_app.finish_copy()

    # Check Completion status
    validate_job_completion_status(job, cdm)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch, press hold and then cancel job
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_direct_copy_media_size_mismatch_and_hold_then_cancel_job
    +test:
        +title: test_copy_ui_job_indirect_copy_media_size_mismatch_and_hold_then_cancel_job
        +guid: 233659aa-9ad0-11ef-a6f6-3ff871be6d3c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_direct_copy_media_size_mismatch_and_hold_then_cancel_job(
        job, cdm, udw, spice, net, copy_page_sensor_setup_direct_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Start a copy job in UI
    run_copy_and_wait_finished(cdm, udw, spice, check_button_enable=False)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_hold_job()

    # Cancel jobs
    job.cancel_active_jobs()

    # Check Completion status
    validate_job_completion_status(job, cdm, "cancelled")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch, press print anyway
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_direct_copy_media_size_mismatch_and_print_anyway
    +test:
        +title: test_copy_ui_job_direct_copy_media_size_mismatch_and_print_anyway
        +guid: dfeb49de-9ad0-11ef-b638-2fcec1e25ad4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_direct_copy_media_size_mismatch_and_print_anyway(
        job, cdm, udw, spice, net, copy_page_sensor_setup_direct_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Start a copy job in UI
    run_copy_and_wait_finished(cdm, udw, spice, check_button_enable=False)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_printanyway_job()

    # Finish Copy
    spice.copy_app.finish_copy()

    # Check Completion status
    validate_job_completion_status(job, cdm)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy interaction with media size mismatch, press hold, load media and expect job completed success
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-208159
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_ui_job_direct_copy_size_mismatch_and_hold_then_load_media_after_press_done_and_job_is_completed_success
    +test:
        +title: test_copy_ui_job_direct_copy_size_mismatch_and_hold_then_load_media_after_press_done_and_job_is_completed_success
        +guid: 7e19daa8-9ad1-11ef-9620-db93c0f736cc
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_direct_copy_size_mismatch_and_hold_then_load_media_after_press_done_and_job_is_completed_success(
        job, tray, cdm, udw, spice, net, copy_page_sensor_setup_direct_mode_and_reduce_size_media_inputs, locale:str="en"):
    # Start a copy job in UI
    run_copy_and_wait_finished(cdm, udw, spice, check_button_enable=False)

    # Check on hold alert
    spice.job_ui.verify_mismatch_alert(net, locale, JobAppWorkflowObjectIds.size_mismatch_title, "cPaperSizeMismatchTitle")

    # Click load media button
    spice.job_ui.mismatch_alert_hold_job()

    # Finish Copy
    spice.copy_app.finish_copy()

    # Set media input rolls in ok state to force auto resume
    time.sleep(5) # If set roll state faster than expected, auto-resume not works as expected because load is received between set to pause is processed.
    tray.reset_trays()

    # Check Completion status
    validate_job_completion_status(job, cdm)

''' 
Media Category Mismatches with Indirect Copy Flow
'''
''' 
Media Category Mismatches with Direct Copy Flow
'''
# TODO - To be implemented with Paper Category Epic
