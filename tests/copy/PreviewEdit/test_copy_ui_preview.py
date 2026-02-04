from dunetuf.copy.copy import *
from dunetuf.copy.copy import Copy
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.control.control import Control
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
import logging
import pytest

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify prompt message and image after clicking on add button in preview 
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-176891
    +timeout:540
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_mdf_landingpagecopy_add_page_prompt
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_mdf_landingpagecopy_add_page_prompt
        +guid:a9550a4c-4540-476b-8d9b-03a66190a866
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_landingpagecopy_add_page_prompt(spice, udw, cdm, net, job, setup_teardown_homescreen):
    job.bookmark_jobs()
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_instance = Copy(cdm, udw)
    copy_app = spice.copy_ui()

    ##Ensure that there is unload media.
    Control.validate_result(scan_action.unload_media("MDF"))

    ##Go to Copy App.
    copy_app.goto_copy_from_copyapp_at_home_screen()
    spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.view_copyScreen)

    # Check ButtonStart.
    spice.copy_ui().wait_for_copy_landing_view()
    copy_app.wait_main_button_to_start_copy(cdm, is_constrained=True)

    ##Start copy, when we press on button Start, if there is not load media appears the modal Insert Page in the Scanner.
    spice.copy_app.start_copy()

    ##Verify constrained mensage
    copy_app.verify_copy_constrained_message(net)

    ## Load a page in the Scanner,
    Control.validate_result(scan_action.load_media("MDF"))

    copy_app.wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)
    addbutton = spice.wait_for(CopyAppWorkflowObjectIds.button_add_page, timeout=50)
    addbutton.mouse_click()
    spice.wait_for(CopyAppWorkflowObjectIds.preview_add_page_prompt)
    spice.wait_for(CopyAppWorkflowObjectIds.add_page_header, timeout=100)
    header_text = spice.wait_for(CopyAppWorkflowObjectIds.add_page_header +" SpiceText", timeout=30)["text"]
    logging.info(header_text)
    expected_string = spice.common_operations.get_expected_translation_str_by_str_id(net,'cInsertPageInScanner')
    assert header_text== expected_string, "String mismatch"

    #Dismiss the modal Insert Page in the Scanner.
    closeModal =spice.wait_for(CopyAppWorkflowObjectIds.button_ok_button_add_page)
    closeModal.mouse_click()

    ## Load a page in the Scanner.
    Control.validate_result(scan_action.load_media("MDF"))
    copy_app.wait_for_acquisition_finished(copy_instance)
    
    #Finish Copy
    copy_app.start_copy_after_preview()
    job.wait_for_no_active_jobs()
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=350)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter in edit view and cancel job 
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-201653
    +timeout: 360
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_open_edit_then_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_open_edit_then_cancel_job
        +guid: 487fe6a8-7c72-480c-8b1f-89896cb2f234
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & Copy=ImagePreview
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""    

def test_copy_ui_open_edit_then_cancel_job(udw,spice,job):
    try:
        udw.mainApp.ScanMedia.unloadMedia("MDF")

        home = spice.main_app.get_home()
        spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
        spice.validate_app(home, False)

        # Open CopyApp
        udw.mainApp.ScanMedia.loadMedia("MDF")
        spice.main_app.goto_copy_app()
        # CopyApp
        copy_app = spice.copy_app.get_copy_app()
        spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
        spice.validate_app(copy_app, False)

        #Start copy, when we press on button Start, if there is not load media appears the modal Insert Page in the Scanner.
        spice.copy_app.start_copy()

        spice.scan_settings.wait_for_preview_n(1)

        spice.scan_settings.click_on_edit_button()
        job.cancel_active_jobs()
        assert spice.wait_for(CopyAppWorkflowObjectIds.pre_preview_layout)
        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

    finally:
        spice.goto_homescreen()
        home = spice.main_app.get_home()
        spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
        spice.validate_app(home, False)