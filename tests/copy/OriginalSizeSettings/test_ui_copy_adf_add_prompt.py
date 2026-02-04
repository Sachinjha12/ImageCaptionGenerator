import pytest
import logging
import time

from dunetuf.job.job import Job
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
   
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify appear/disappear "ADF" prompt after timeout in hpMfp
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-154928
    +test_classification:System
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_verify_adf_add_prompt_disappears
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_adf_add_prompt_disappears
        +guid:9469c119-28c4-4b53-907f-3a1179083a57
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & ADFMediaSize=MixedA4A3

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""        

def test_copy_ui_verify_adf_add_prompt_disappears(udw,spice,job,net, scan_emulation):
    try:
        job.bookmark_jobs()
        options = {
            'size': 'MIXED_LETTER_LEGAL'
            }
        loadmedia='ADF_PROMPT'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        spice.copy_ui().copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        
        # Verify Prompt
        time.sleep(5)
        assert spice.query_item(CopyAppWorkflowObjectIds.copy_adf_load_paper_alert)["text"] == "Document Feeder Empty", "No Prompt"

        # LoadMedia
        # udw.mainApp.ScanMedia.loadMedia("ADF")
        scan_emulation.media.load_media("ADF")

        # Wait
        print("Wait Timeout(240s)")
        time.sleep(240)
        
        # Verify job is cancelled
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not canceled'
        assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is not success'

    finally:
        # Go to home screen
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify appear "ADF" prompt and click start button for job start
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-154928
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_click_start_button_with_adf_add_prompt
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_click_start_button_with_adf_add_prompt
        +guid:bc9cb31f-7f45-4048-af37-deb216a60682
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & ADFMediaSize=MixedA4A3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_click_start_button_with_adf_add_prompt(udw,spice,job,net):
    try:
        job.bookmark_jobs()
        options = {
            'size': 'MIXED_LETTER_LEGAL'
            }
        loadmedia='ADF_PROMPT'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        spice.copy_ui().copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        
        # Verify Prompt
        time.sleep(5)
        assert spice.query_item(CopyAppWorkflowObjectIds.copy_adf_load_paper_alert)["text"] == "Document Feeder Empty", "No Prompt"

        # LoadMedia
        udw.mainApp.ScanMedia.loadMedia("ADF")

        # Start
        spice.wait_for(CopyAppWorkflowObjectIds.adf_add_prompt_start_button).mouse_click()
        
        # Verify job is cancelled
        time.sleep(10)
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
        assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    finally:
        # Go to home screen
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify appear "ADF" prompt and click cancel button for job cancel
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-154928
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_click_cancel_button_with_adf_add_prompt
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_click_cancel_button_with_adf_add_prompt
        +guid:2a2a7a1b-a2cd-4e9e-9d1c-035ec3307289
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & ADFMediaSize=MixedA4A3

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_click_cancel_button_with_adf_add_prompt(udw,spice,job,net):
    try:
        job.bookmark_jobs()
        options = {
            'size': 'MIXED_LETTER_LEGAL'
            }
        loadmedia='ADF_PROMPT'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        spice.copy_ui().copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        
        # Verify Prompt
        time.sleep(5)
        assert spice.query_item(CopyAppWorkflowObjectIds.copy_adf_load_paper_alert)["text"] == "Document Feeder Empty", "No Prompt"

        # LoadMedia
        udw.mainApp.ScanMedia.loadMedia("ADF")

        # cancel
        spice.wait_for(CopyAppWorkflowObjectIds.adf_add_prompt_cancel_button).mouse_click()
        
        # Verify job is cancelled
        time.sleep(10)
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not canceled'
        assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is not success'

    finally:
        # Go to home screen
        spice.goto_homescreen()
        spice.wait_ready()
