
import logging
import uuid
import pytest
import traceback
from dunetuf.ssh import SSH
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from tests.ui.lib.actions.commonsActions import *
from time import sleep
from tests.copy.quicksets.copy_combination import *
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
import time
from dunetuf.copy.copy import *
from dunetuf.power.power import Power
from dunetuf.control.device_status import DuneDeviceStatus
from dunetuf.print.print_common_types import MediaInputIds, Edge, MediaSize, MediaType, Doors, MediaOrientation, TrayLevel


N_COPIES = 5
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Cancel Copy Job Warning Prompt when user press home Button in CopyApp
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-102306
    +timeout:150
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_validate_cancel_job_warning_prompt_on_home_event
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_validate_cancel_job_warning_prompt_on_home_event
        +guid:79dec1bc-cfef-4405-a91d-660dd4c03462
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_job_validate_cancel_job_warning_prompt_on_home_event(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("unload ADF")
    scan_emulation.media.unload_media(media_id='ADF')
    scan_emulation.media.load_media('Flatbed',1)
    try : 
        logging.info("Go to Copy > Previewpanel > click on preview > click on home > click on Cancel Job")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(15)
        homeButton = spice.wait_for(CopyAppWorkflowObjectIds.button_home)
        homeButton.mouse_click(2, 2)
        time.sleep(5)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
        yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
        yes_Cancel_Button.mouse_click()

        assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)
    finally : 
        scan_emulation.media.load_media(media_id='ADF')
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test Cancel Copy Job Warning Prompt when Inactivity Timeout fired and User Cancel Job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-102308
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout_event_then_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout_event_then_cancel_job
        +guid:6397f442-08e9-4789-aaa8-4fde136e075e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & InactivityTimeout=5Minutes
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout_event_then_cancel_job(scan_emulation, job, udw, spice, cdm):

    # check jobId
    job.bookmark_jobs()
    logging.info("unload ADF")

    scan_emulation.media.unload_media(media_id='ADF')
    udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(30)

    logging.info("Go to Copy > Previewpanel > click on preview > wait for Inactivity Timeout > click on Cancel Job")
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(25)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt, 20)
        cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_secondary_button, 10)
        cancel_Button.mouse_click()
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp, 15)

        # Verify no active job is present
        job.wait_for_no_active_jobs()

    finally:

        scan_emulation.media.load_media(media_id='ADF')
        udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(0)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test Cancel Copy Job Warning Prompt when Inactivity Timeout fired and User don't cancel job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-102308
    +timeout:240
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout_then_do_not_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout_then_do_not_cancel
        +guid:33c398bf-a5df-488b-9811-d7f87a8b9ace
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & InactivityTimeout=5Minutes
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout_then_do_not_cancel(job, udw, spice, cdm):

    # check jobId
    job.bookmark_jobs()
    logging.info("unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    # Inactivity Timeout set to 30 seconds
    udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(30)
    logging.info("Go to Copy > Previewpanel > click on preview > wait for Inactivity Timeout > click on No")
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(30)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt, 15)
        continue_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
        continue_Button.mouse_click()
        copy_job_app.verify_preview()
        time.sleep(25)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt, 15)
        cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_secondary_button)
        cancel_Button.mouse_click()
        
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp, 15)

        # Verify no active job is present
        job.wait_for_no_active_jobs()

    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(0)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test Cancel Copy Job Warning Prompt when user press Back Button in CopyApp
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-102306
    +timeout:150
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_validate_cancel_job_warning_prompt_on_back_event
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_validate_cancel_job_warning_prompt_on_back_event
        +guid:9fd30d5f-2c32-4370-9e99-1cc0ac082ce6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_validate_cancel_job_warning_prompt_on_back_event(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("unload ADF")
    scan_emulation.media.unload_media(media_id='ADF')
    on_homescreen = False
    
    logging.info("Go to Copy > Previewpanel > click on preview > click on cancel > click on preview > click on back")
    try :
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(5)

        copy_job_app.goto_main_panel()
        copy_job_app.wait_for_copy_status_toast_is_not_visible()

        spice.goto_homescreen()

        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
        yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
        yes_Cancel_Button.mouse_click()
        on_homescreen = True

    finally:
        scan_emulation.media.load_media(media_id='ADF')
        if not on_homescreen:
            spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test Cancel Copy Job Warning Prompt when Inactivity Timeout fired Two Times
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-102308
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout
        +guid:c804f843-da50-4469-8ba7-6fafdf8a9ca9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & InactivityTimeout=5Minutes
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_cancel_job_warning_prompt_on_inactivity_timeout(job, udw, spice, cdm):

    # check jobId
    job.clear_joblog
    job.bookmark_jobs()
    logging.info("unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    # Inactivity Timeout set to 30 seconds
    udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(30)
    logging.info("Go to Copy > Previewpanel > click on preview > wait for Inactivity Timeout No Interaction quit CopyApp")
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(25)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt, 50)
        time.sleep(25)
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp, 50)
        # Verify no active job is present
        job.wait_for_no_active_jobs()

    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(0)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify back to homescreen from Copy App screen with Standard Quality and color setting is successful
    +test_tier: 3
    +is_manual: False
    +reqid:DUNE-52016
    +timeout:250
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_standard_color_cancel
    +test:
        +title:test_copy_ui_job_standard_color_cancel
        +guid:4ce83870-8336-4a70-bf49-7c9f4fbd0948
        +dut:
            +type:Simulator, Engine, Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_standard_color_cancel(job, spice, udw, cdm):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    if cdm.device_feature_cdm.is_color_supported():
        copy_job_app.select_color_mode("Color")
    logging.info("Set Copy Quality to Standard")
    copy_job_app.select_quality_option("Standard")
    sleep(2)
    copy_job_app.back_to_landing_view()
    copy_job_app.wait_for_copy_landing_view()
    spice.goto_homescreen()
    assert spice.wait_for("#HomeScreenView")

    sleep(3)
    # Verify no active job is present
    job.wait_for_no_active_jobs()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job from Widget and after scanning cancel the job
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-88776
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_widget_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_widget_cancel_job
        +guid:5265bb78-9a60-48db-935b-186a5358ef98
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & Copy=IDCopy  & UIComponent=CopyWidget
   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_cancel_job(spice, udw, job, net, configuration):
    #Load the Document in MDF
    logging.info("load the MDF media")
    udw.mainApp.ScanMedia.loadMedia("MDF")

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Start Copy
    spice.copy_ui().start_copy_widget()

    spice.copy_ui().cancel_copy_from_preview_panel_launch_from_widget()
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')

    # Check after cancelling job user is on HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False) 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify cancelling copy job happens successfully
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_2copies_adf_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2copies_adf_cancel_job
        +guid:1624fdb4-4ad4-48e2-b8fb-9eaaa3ce7019
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Widget=Settings
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2copies_adf_cancel_job(setup_teardown_with_copy_job, spice, udw, job):
    copy_job_app = spice.copy_ui()
    logging.info("Load 100 pages in ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    udw.mainApp.ScanDeviceService.setNumScanPages(100)

    logging.info("Set numbers of copies as 2")
    copy_job_app.change_num_copies(num_copies=2)
    logging.info("Click Copy widget start button on Home screen")
    copy_job_app.start_copy_widget()

    logging.info("While job is in progress, navigate to Jobs, cancel the job")
    spice.main_app.goto_job_queue_app()
    job_queue = job.get_job_queue()
    job_id = job_queue[-1]["jobId"]

    spice.job_ui.goto_created_job(job_id)
    spice.job_ui.cancel_selected_job()
    
    logging.info("Check the copy job cancelled successfully")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])

    logging.info("Change numbers of copies back to 1")
    copy_job_app.change_num_copies(num_copies=1)
    udw.mainApp.ScanDeviceService.setNumScanPages(1)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform flatbed duplex job in UI, when cancel on prompt is clicked
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-34775
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_flatbed_duplex_job_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_flatbed_duplex_job_cancel
        +guid:52fdbcb3-d77f-4879-a084-44bada09842e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & ScannerType=MDuplex
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_flatbed_duplex_job_cancel(job, udw, spice,scan_emulation, configuration):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        scan_emulation.media.unload_media('ADF')
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_2_sided")

        job_ids = job.get_recent_job_ids()
        copy_job_id = job_ids[len(job_ids) - 1]
        assert copy_job_id != last_job_id, "Copy job is missing"

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "CANCELED")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:cancel copy after send a copy job and review it on jobs panel
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5488
    +timeout:300
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_then_cancel_job_and_review
    +test:
        +title:test_copy_ui_job_then_cancel_job_and_review
        +guid:958121b8-648b-4bf4-a881-5ad8a99d89f8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & DeviceClass=LFP & ScanEngine=LightWing
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_then_cancel_job_and_review(spice, job, udw, net, configuration):
    udw.mainApp.ScanMedia.loadMedia("MDF")
    logging.info("Go to Copy > click on start > wait for preview > click on canceljob")

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # CopyApp
    copy_job_app = spice.copy_ui()
    spice.main_app.goto_copy_app()

    # Start Copy 
    copy_job_app.start_copy()
    spice.scan_settings.wait_for_preview_n(1)

    # Go to HomeScreen for cancelling
    spice.goto_homescreen()
    spice.scan_settings.cancel_current_job_modal_alert(cancel_job=True)
    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)

    # Get last job in queue by CDM
    job.wait_for_no_active_jobs()
    queue_job = job.get_last_job_id_cdm() 

    # Go to Jobs queue
    spice.main_app.goto_job_queue_app()
    logging.info("Check the copy job cancelled successfully")
    job_cdm = job.get_job_from_history_by_id(queue_job)

    # Check the last job is cancelled
    assert job_cdm["completionState"] == "cancelled"

    # Get last job in queue
    job.wait_for_no_active_jobs()
    last_job_id = job.get_last_job_id_cdm()

    # Click in the last job completed
    spice.job_ui.goto_job(last_job_id)

    # Check that job is canceled 
    assert spice.job_ui.recover_job_status() == "Canceled"

    #Go to HomeScreen
    spice.goto_homescreen()   
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test Copy Cancel job for Long press
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_cancel_job_for_long_press
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_validate_cancel_job_for_long_press
        +guid:6a8e75b7-597c-4903-a00e-69a40108bda7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_cancel_job_for_long_press(job, spice):

    # check jobId
    job.bookmark_jobs()

    try:
        spice.copy_ui().goto_copy()
        spice.goto_homescreen()

        assert spice.wait_for("#HomeScreenView")

        sleep(3)
        # Verify no active job is present
        job.wait_for_no_active_jobs()
        
    
    finally:
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test validate copy cancel job when user select a different quickset
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_copy_cancel_job_for_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_validate_copy_cancel_job_for_quickset
        +guid:65c703ce-e248-4864-9c47-1e041555cdea
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_ui_validate_copy_cancel_job_for_quickset(cdm, job, spice, net):

    # check jobId
    job.bookmark_jobs()
    try:
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy2", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)

        sleep(1)
        # Verify no active job is present
        job.wait_for_no_active_jobs()              
        
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:User will not respond to the cancel job warning prompt while set inactivity timeout and verify rerouted to homescreen
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_cancel_job_warning_prompt_rerouted_to_home_screen_on_set_inactivity_timeout
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_cancel_job_warning_prompt_rerouted_to_home_screen_on_set_inactivity_timeout
        +guid:f20ebb30-e7e5-4718-a244-254a4ede3cc8
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & InactivityTimeout=30Seconds
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_cancel_job_warning_prompt_rerouted_to_home_screen_on_set_inactivity_timeout(udw, spice,job):
    # check jobId
    job.clear_joblog
    job.bookmark_jobs()
    logging.info("unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    try:
        spice.homeMenuUI().set_inactivitytimeout_thirtyseconds(spice)
        spice.goto_homescreen()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(30)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt, 30)
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp, 30)
        # Verify no active job is present
        job.wait_for_no_active_jobs()

    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(0)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copy cancel job warning prompt when user press Back Button in CopyApp
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_copyapp_landingpage_on_back_button_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_copyapp_landingpage_on_back_button_cancel_job
        +guid:861189ec-ea2d-49cb-868a-c76c668daee0
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_copyapp_landingpage_on_back_button_cancel_job(spice, udw, job):
    # check jobId
    job.clear_joblog
    job.bookmark_jobs()
    logging.info("unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(5)

        copy_job_app.goto_main_panel()
        copy_job_app.wait_for_copy_status_toast_is_not_visible()

        back_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_landing_view_back_button)
        back_button.mouse_click()
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt, 15)
        no_cancel_job=spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_secondary_button)
        no_cancel_job.mouse_click()
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_copyScreen, 10)
        back_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_landing_view_back_button)
        back_button.mouse_click()
        yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
        yes_Cancel_Button.mouse_click()

    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify cancel job warning prompt after reboot device
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_cancel_job_warning_prompt_after_reboot
    +test:
        +title:test_copy_ui_verify_cancel_job_warning_prompt_after_reboot
        +guid:295ce6a0-92c3-411a-a4a5-916c84d59dcd
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_cancel_job_warning_prompt_after_reboot(spice,job, udw, net):
    # check jobId
    job.clear_joblog
    job.bookmark_jobs()
    logging.info("unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(5)
        spice.goto_homescreen()
        time.sleep(5)
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
        #reboot
        Power(udw).power_cycle()
        sleep(60)
        # wait for system to reboot
        device_status = DuneDeviceStatus(net.ip_address,"")
        result = device_status.device_ready(300)
        assert all(result.values())
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        time.sleep(5)
        spice.goto_homescreen()
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
        yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
        yes_Cancel_Button.mouse_click()

    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copy button should not greyedout after cancel the copy job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_copyjob_cancel_verify_copy_button_should_not_greyedout
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_copyjob_cancel_verify_copy_button_should_not_greyedout
        +guid:1fc427a0-df3e-402c-b3b0-3725dd6472ca
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_copyjob_cancel_verify_copy_button_should_not_greyedout(spice, cdm, net,job, udw):
    job.bookmark_jobs()
    logging.info("Load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")

    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        logging.info("Start a copy job")
        copy_job_app.start_copy()
        logging.info("Click Cancel button")
        current_option = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_button)
        current_option.mouse_click()  
        time.sleep(5)
        logging.info("Check the copy job cancelled successfully")
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
        assert spice.wait_for(CopyAppWorkflowObjectIds.copy_button) ["visible"] is True, 'Copy button is not visible'
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copy job cancel while paper mismatch
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-161363
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_cancel_job_while_paper_mismatch
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_cancel_job_while_paper_mismatch
        +guid:0d4a9f0a-77b0-490e-a284-284d322bd6e6
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & MediaInputInstalled=Tray3 & ADFMediaSize=Statement
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_cancel_job_while_paper_mismatch(spice, print_emulation, print_mapper, tray, media,cdm, udw, job, net):
    try:
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        copy_job_app = spice.copy_ui()
        job_ids.clear()
        job.clear_joblog()
        job.bookmark_jobs()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        #Load Tray with Letter
        tray_list = print_emulation.tray.get_installed_trays()
        convert_tray_list = copy_job_app.convert_media_source_ids(tray_list)
        error_list = []
        print_emulation.tray.reset_trays()
        for tray_id in convert_tray_list:
            try:
                logging.info(f"Source tray is: {tray_id}")
                print_emulation.tray.setup_tray(tray_id, MediaSize.Letter.name, MediaType.Plain.name, orientation=MediaOrientation.Default.name, level=TrayLevel.Full.name)
            except Exception as e:
                error_list.append('================================================')
                logging.error(f'Error on {tray_id}: {e}')
                error_list.append(f'Error on {tray_id}:\n{traceback.format_exc()}')
                
        if len(error_list) > 0:
            error_list.insert(0,"ERROR SUMMARY: " )
            errors = '\n'.join(error_list)
            logging.error(f'Errors of this test: {errors}')
            raise Exception(errors)        

        logging.info("Go to copy screen")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_original_size('Statement (8.5x5.5 in.)')
        sleep(2)
        copy_job_app.select_media_size_option("Statement (8.5x5.5 in.)")
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()
        copy_job_app.wait_for_copy_landing_view()
        copy_job_app.start_copy()
        # Check Size/Type prompt on UI
        time.sleep(15)
        assert(media.check_if_alert_present("mediaMismatchSizeFlow"))
        job.cancel_active_jobs()
        job.wait_for_no_active_jobs()
        job_id = job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        logging.info("jobId is "+ job_id_cdm)
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()
        # goto job details from job queue
        spice.job_ui.goto_job(job_id_cdm)
        time.sleep(5)
        # Check the job details
        assert spice.job_ui.recover_job_status() == "Canceled"
        # JobType
        assert spice.job_ui.recover_job_type() == "Copy"
    
    finally:
        spice.goto_homescreen()
        print_emulation.tray.reset_trays() 
        job.clear_joblog()
