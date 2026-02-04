import time
import pytest
from random import randint
from dunetuf.copy.copy import *
import CopyReprintHelper
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

# COMMON TEST FUNCTION

@pytest.fixture(autouse=True)
def setup_teardown(cdm):
    # If the hideDeletedJobs is set to true, we need to set it to false to be able to see the job in the history using UI
    job_configuration = cdm.get(cdm.JOB_CONFIGURATION_ENDPOINT)
    if ("hideDeletedJobs" in job_configuration):
        oldHideDeletedJobs = job_configuration["hideDeletedJobs"]
        cdm.patch(cdm.JOB_CONFIGURATION_ENDPOINT, {"version": job_configuration["version"], "hideDeletedJobs": "false"})
        assert(cdm.get(cdm.JOB_CONFIGURATION_ENDPOINT)["hideDeletedJobs"] == "false")
    
    yield

    # Restore the hideDeletedJobs with the old value
    if (oldHideDeletedJobs):
        cdm.patch(cdm.JOB_CONFIGURATION_ENDPOINT, {"version": job_configuration["version"], "hideDeletedJobs": "true"})
        assert(cdm.get(cdm.JOB_CONFIGURATION_ENDPOINT)["hideDeletedJobs"] == "true")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test to verify the cancelled jo is not reprintable 
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-118383
    +timeout:500
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_validate_cancelled_jobs_are_not_reprintable
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Reprint
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_cancelled_jobs_are_not_reprintable
        +guid:40021dcb-979d-4854-9d3f-7f05bcb049b8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_cancelled_jobs_are_not_reprintable( spice, cdm, udw, net, job, copy,configuration):
    try:
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job, net,configuration)
        job.cancel_job(job_id)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration,message = "Cancel")
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()
        time.sleep(3)
        assert CopyReprintHelper.check_for_reprint_button_for_given_job(spice, job, cdm,job_id) == False
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test to verify that (1) number of copies can be set between 1 to 99 (2) verify entering and exiting reprint screen will not add a new job
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-118383
    +timeout:500
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_validate_no_copies_variable_btwn_min_max_from_reprint_window
    +test:
        +title:test_copy_ui_validate_no_copies_variable_btwn_min_max_from_reprint_window
        +guid:1ddb3643-6e15-44af-9604-c93d640a614c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_no_copies_variable_btwn_min_max_from_reprint_window(spice, cdm, udw, net, job, copy,configuration):
    try:
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job, net,configuration)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()
        time.sleep(3)
        assert CopyReprintHelper.check_for_reprint_button_for_given_job(spice, job, cdm, job_id)
        CopyReprintHelper.enter_reprint_screen(spice)
        reprint_spin = spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_job_reprint_screen_spin_box)
        reprint_spin["value"] = randint(CopyReprintHelper.min_no_copies, CopyReprintHelper.max_no_copies)
        reprint_spin["value"] = randint(CopyReprintHelper.min_no_copies, CopyReprintHelper.max_no_copies)

        reprint_spin["value"] = CopyReprintHelper.max_no_copies
        spin_box_up_btn_enabled = spice.query_item(CopyAppWorkflowObjectIds.jobs_app_job_reprint_screen_spin_box+ " #upBtn")["enabled"]
        assert spin_box_up_btn_enabled == False
        reprint_spin["value"] = CopyReprintHelper.min_no_copies
        spin_box_down_btn_enabled = spice.query_item(CopyAppWorkflowObjectIds.jobs_app_job_reprint_screen_spin_box+ " #downBtn")["enabled"]
        assert spin_box_down_btn_enabled == False
        #go back and check no new job is started
        CopyReprintHelper.go_back_to_jobque_detail_panel(spice)
        time.sleep(2)
        queue = job.get_job_queue()
        assert len(queue) == 0
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: After deleting the content of copy job reprint should not be possible
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-118383
    +timeout:500
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_validate_contetnt_deleted_jobs_are_not_reprintable
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Reprint
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_contetnt_deleted_jobs_are_not_reprintable
        +guid:2f1016f0-54b5-42a3-bae4-22358acb34c8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_contetnt_deleted_jobs_are_not_reprintable( spice, cdm, udw, net, job, copy,configuration):
    try:
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job, net,configuration)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()
        time.sleep(3)
        assert CopyReprintHelper.check_for_reprint_button_for_given_job(spice, job, cdm,job_id)
        CopyReprintHelper.delete_content_of_given_job(spice, job, cdm,job_id) 
        assert CopyReprintHelper.check_for_reprint_button_for_given_job(spice, job, cdm,job_id) == False
    finally:
        spice.goto_homescreen()