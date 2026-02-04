import logging
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy
import json
import pprint
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for blank page suppression of Copy default option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-24421
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_default_option_blank_page_suppression
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_default_option_blank_page_suppression
        +guid:6eb68441-ff2e-4cc5-9368-17b819c58e8d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & DigitalStorageType=HardDisk & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_default_option_blank_page_suppression(spice, job, udw, net, cdm,scan_emulation): 
    scan_emulation.media.load_media('ADF', 1)
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        
        logging.info("Verify the value displayed for blank page suppression")
        spice.copy_ui().verify_copy_settings_selected_option(net, "blank_page_suppression", "off")
        
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for blank page suppression of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-24421
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_option_blank_page_suppression
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_blank_page_suppression
        +guid:dc1d09f7-b5e0-4ba0-9682-43b6079346f8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & DigitalStorageType=HardDisk & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_blank_page_suppression(spice, job, udw, net, cdm, scan_emulation):
    scan_emulation.media.load_media('ADF', 1)
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_blank_page_suppression(option="on")
        spice.copy_ui().back_to_landing_view()
        
        # Verify ticket values
        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(blank_page_suppression= "true")
        time.sleep(5)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test for changing the blank page suppression default option of Copy option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-24421
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_change_default_option_blank_page_suppression
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_change_default_option_blank_page_suppression
        +guid:5f6e7b07-bbdd-4036-b3b2-a864b78db5ee
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & DigitalStorageType=HardDisk & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_change_default_option_blank_page_suppression(spice, job, udw, net, cdm):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    original_ticket_default_body = Copy.get_copy_default_ticket(cdm)
    
    try:
        # set copy options
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_blank_page_suppression(option="on")
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()

        # Verify ticket values
        ticket_default_body = Copy.get_copy_default_ticket(cdm)
        assert "true" == ticket_default_body["pipelineOptions"]["imageModifications"]["blankPageSuppressionEnabled"]
        
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        spice.signIn.goto_universal_sign_in("Sign Out")
        Copy.reset_copy_default_ticket(cdm, original_ticket_default_body)
