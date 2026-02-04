import logging
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To check non concurrent copy job flow from copyapp
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-77856
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_non_concurrent_flow
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_non_concurrent_flow
        +guid:99f117b9-3343-4883-ab75-e18f543af526
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & EngineFirmwareFamily=DoX & DeviceFunction=Copy & ScannerInput=ManualFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_non_concurrent_flow(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    udw.mainApp.ScanMedia.unloadMedia("MDF")

    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.start_copy()
    copy_job_app.verify_copy_constrained_message(net)

    logging.info("Load MDF")
    udw.mainApp.ScanMedia.loadMedia("MDF")
    copy_job_app.start_copy()
    copy_job_app.wait_for_release_page_prompt_and_click_relasePage()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net,configuration)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To check non concurrent copy job flow triggered from widget
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-77856
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_from_widget_non_concurrent_flow
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_from_widget_non_concurrent_flow
        +guid:34ba913a-389d-40a0-851b-b278f09c13a0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & EngineFirmwareFamily=DoX & DeviceFunction=Copy & ScannerInput=ManualFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_from_widget_non_concurrent_flow(spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    udw.mainApp.ScanMedia.unloadMedia("MDF")
    copy_job_app = spice.copy_ui()
    copy_job_app.start_copy_widget()
    
    copy_job_app.verify_copy_constrained_message(net)
    logging.info("Load MDF")
    udw.mainApp.ScanMedia.loadMedia("MDF")
    spice.common_operations.compare_alert_toast_message(net, "cDocumentFeeder")

    copy_job_app.start_copy_widget()
    copy_job_app.wait_for_release_page_prompt_and_click_relasePage()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To check for header in cancel processing screen
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-116455
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_check_header_in_cancel_processing_screen
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_check_header_in_cancel_processing_screen
        +guid:ac3a5808-34dc-48ec-8bb3-c16100d3ba0d
        +dut:
            +type:Engine
            +configuration:DeviceClass=MFP & DeviceClass=LFP & EngineFirmwareFamily=DoX & DeviceFunction=Copy & ScannerInput=ManualFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_job_check_header_in_cancel_processing_screen(cdm, spice, udw, net, configuration, job):
    
    job_id = Copy(cdm, udw).do_copy_job(cancel = Cancel.after_start)
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration,message = "Canceling")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To Check Copy Header in Active Job Copy Completion Modal
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-120453
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_validate_header_in_active_job_completion_screen
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_validate_header_in_active_job_completion_screen
        +guid:ca9357f9-4384-4f76-9770-a9c414ea97b8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & EngineFirmwareFamily=DoX & DeviceFunction=Copy & ScannerInput=ManualFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_validate_header_in_active_job_completion_screen(setup_teardown_with_copy_job,spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    udw.mainApp.ScanMedia.loadMedia("MDF")

    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.start_copy()

    spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage(timeout = 50)
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration,message = "Complete")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])