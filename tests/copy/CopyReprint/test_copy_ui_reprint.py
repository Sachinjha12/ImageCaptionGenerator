import time
import pytest
from random import randint
from dunetuf.copy.copy import *
from tests.copy.CopyReprint import CopyReprintHelper
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

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
    +purpose: verify reprinting the copy job works fine
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-118383
    +timeout:900
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_successful_copy_jobs_are_reprintable
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title:test_copy_ui_validate_successful_copy_jobs_are_reprintable
        +guid:8fd26c03-47d6-4051-8a6a-79371c871fe8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob & Copy=BluePrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_successful_copy_jobs_are_reprintable(spice, cdm, udw, net, job, copy,configuration):
    try:
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job, net,configuration)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, timeout=120)
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()
        time.sleep(3)
        assert CopyReprintHelper.check_for_reprint_button_for_given_job(spice, job, cdm,job_id)
        CopyReprintHelper.enter_reprint_screen(spice)

        if configuration.productname in ["beam/beammfp_power","odyssey"]:
            max_no_copies = 99
        else:
            max_no_copies = 999    
        random_no_copies = randint(CopyReprintHelper.min_no_copies, max_no_copies)
        CopyReprintHelper.start_reprint_job_and_verify_it_is_printed(spice, job, cdm, udw, net, configuration,random_no_copies)
    finally:
        spice.goto_homescreen()

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
    +name:test_walkupapp_copy_ui_validate_cancelled_jobs_are_not_reprintable
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title:test_walkupapp_copy_ui_validate_cancelled_jobs_are_not_reprintable
        +guid:142cf357-3f28-466a-91e8-20355d72de71
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob & Copy=BluePrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_walkupapp_copy_ui_validate_cancelled_jobs_are_not_reprintable( spice, cdm, udw, net, job, copy,configuration):
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
    +name:test_walkupapp_copy_ui_validate_no_copies_variable_btwn_min_max_from_reprint_window
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title:test_walkupapp_copy_ui_validate_no_copies_variable_btwn_min_max_from_reprint_window
        +guid:d89a0bd7-bb5f-482b-87fb-827feda25f22
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob & Copy=BluePrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_walkupapp_copy_ui_validate_no_copies_variable_btwn_min_max_from_reprint_window(spice, cdm, udw, net, job, copy,configuration):
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
    +name:test_copy_ui_validate_contetnt_deleted_jobs_are_not_reprintable2
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title:test_copy_ui_validate_contetnt_deleted_jobs_are_not_reprintable2
        +guid:54e68d56-041b-4611-87cd-cce4dfe6ea9a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob & Copy=BluePrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_contetnt_deleted_jobs_are_not_reprintable2( spice, cdm, udw, net, job, copy,configuration):
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