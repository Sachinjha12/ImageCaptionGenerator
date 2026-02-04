import logging
import uuid
import pytest
from dunetuf.ssh import SSH
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from tests.ui.lib.actions.commonsActions import *
from time import sleep
from tests.copy.quicksets.copy_combination import *
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
import copy
from dunetuf.copy.copy import *
from tests.copy.quicksets.copy_combination import *


N_COPIES = 5
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test Validate  job is not started when user click on back button in landing view
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_noactive_copy_job_on_back_button
    +test:
        +title: test_copy_ui_validate_noactive_copy_job_on_back_button
        +guid:e0cc73a5-8005-4dc9-979f-a3a7cd004008
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_noactive_copy_job_on_back_button(setup_teardown_with_copy_job, job, spice):
    # check jobId
    job.bookmark_jobs()

    try:
        spice.copy_ui().goto_copy()
        sleep(5)
        spice.copy_ui().back_to_homescreen()

        assert spice.wait_for("#HomeScreenView")

        sleep(3)
        # Verify no active job is present
        job.wait_for_no_active_jobs()
        
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test  job should not be called after inactivity timeout
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-
    +timeout:200
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_validate_noactive_job_for_inactivity_timeout
    +test:
        +title:test_copy_ui_validate_noactive_job_for_inactivity_timeout
        +guid:765123cd-534e-4743-a079-9f5ebf6590c2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_noactive_job_for_inactivity_timeout(setup_teardown_with_copy_job, job, udw, spice, cdm):

    # check jobId
    job.bookmark_jobs()

   
    try:
        cdm.patch_raw(cdm.POWER_CONFIG, {"inactivityTimeout":"30"}, timeout = 10.0)
        spice.copy_ui().goto_copy()
        sleep(35)

        assert spice.wait_for("#HomeScreenView")

        # Verify no active job is present
        job.wait_for_no_active_jobs()

    finally:
        cdm.patch_raw(cdm.POWER_CONFIG, {"inactivityTimeout":"0"}, timeout = 10.0)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify user is able to enter options screen multiple times.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +external_files:
    +test_classification:System
    +name:test_copy_ui_open_options_screen_twice_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_open_options_screen_twice_copy_job
        +guid:c4e4cac3-9e6c-4191-98cd-ca4532985c5e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_open_options_screen_twice_copy_job(setup_teardown_with_copy_job, spice, cdm, udw, net, job, configuration):
    expected_number_of_copies = 5
    
    copy_job_app = spice.copy_ui()
    logging.info("Go to Copy")
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    logging.info("Go to Options, change any option (e.g.: set num of copies to 5)")
    copy_job_app.goto_copy_options_list()
    copy_job_app.change_num_copyApp_copies(5)
    logging.info("Go back to the previous screen")
    copy_job_app.back_to_landing_view()
    actual_number_of_copies = copy_job_app.get_number_of_copies()
    assert expected_number_of_copies == actual_number_of_copies, "Num Copies setting value mismatch"
    logging.info("Click on options button again, move back to landing view")
    copy_job_app.goto_copy_options_list()
    actual_number_of_copies = copy_job_app.get_number_of_copies()
    assert expected_number_of_copies == actual_number_of_copies, "Num Copies setting value mismatch"
    copy_job_app.back_to_landing_view()
    logging.info("Start a copy job")
    copy_job_app.start_copy()

    logging.info("Validate copy settings for current job")
    Copy(cdm, udw).validate_settings_used_in_copy(number_of_copies=5)
    
    logging.info("Check the copy job complete successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:click spinbox and then change quality
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-222097 
    +timeout:300
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_click_spinbox_quality
    +test:
        +title:test_copy_ui_click_spinbox_quality
        +guid:6c4a4a74-ba43-4b4d-b099-5eeaa2774a2d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""

def test_copy_ui_click_spinbox_quality(spice, job, udw, net, configuration):
    '''
    The test is only enabled for beam because currently we are using hardcoding coordinate for beam to perform click. The implementation for interactive summary to auto detect objectname and perform click 
    is not implemented. The click cordinates for other homepro product are diffrent because of different UI.
    '''

    if configuration.productname == "beam/beammfp" and spice.uitype == "Workflow" and spice.uisize == "S":
        copy_job_app = spice.copy_ui()
        spice.main_app.goto_copy_app()
        time.sleep(1)

        copy_spin_box = spice.wait_for(CopyAppWorkflowObjectIds.spinbox_copy)
        copy_spin_box.mouse_click(300,150)
        spinboxOkKey = spice.wait_for(CopyAppWorkflowObjectIds.spinbox_ok_key)
        spinboxOkKey.mouse_click()
        spice.basic_common_operations.scroll_to_position_vertical(0.4, scrollbar_objectname = CopyAppWorkflowObjectIds.vertical_layout_scrollbar) 
    
        qualitybox = spice.wait_for(CopyAppWorkflowObjectIds.row_combo_copySettings_quality)
        qualitybox.mouse_click()

        change_quality = spice.wait_for(CopyAppWorkflowObjectIds.select_best_quality)
        change_quality.mouse_click()
        spice.goto_homescreen()

 