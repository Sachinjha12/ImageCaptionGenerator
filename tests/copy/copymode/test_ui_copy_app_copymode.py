import logging
import pytest
import uuid
import dunetuf.common.commonActions as CommonActions
import requests

from dunetuf.control.control import Control
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction, ScannerState
from dunetuf.cdm.CdmEndpoints import CdmEndpoints
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from tests.ui.lib.actions.commonsActions import *
from dunetuf.copy.copy import Copy
from requests.exceptions import HTTPError

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app and check copy mode button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_check_copymode
    +test:
        +title:test_copy_ui_enter_app_and_check_copymode
        +guid: 47ee558e-abc2-11ee-b0dc-3fec993a859e
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_copymode(setup_teardown_default_copy_mode, spice):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)
    # Visible, enabled
    spice.validate_button(copymode_button)

    # Back Home
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app through widget and check copy mode button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_copymode
    +test:
        +title:test_copy_widget_copymode
        +guid: 8cbc3af4-abc3-11ee-ba42-133bec214ba6
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_copymode(setup_teardown_default_copy_mode, spice, cdm, udw):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    copy_instance = Copy(cdm, udw)

    # Make sure media is  present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # CopyApp
    spice.copy_ui().start_copy_widget()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Wait for page to finish
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance, expanded = True)

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)
    # Not Visible and enabled
    spice.validate_button(copymode_button, False)

    # Goes back to HS after finishing job
    spice.copy_app.finish_copy( expanded = True )
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app through widget more options button and check copy mode button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_more_options_copymode
    +test:
        +title:test_copy_widget_more_options_copymode
        +guid: 4e7acbfc-abc8-11ee-8822-e39ace3e4710
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_more_options_copymode(setup_teardown_default_copy_mode, spice, udw):
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Make sure media is  present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # CopyApp
    spice.copy_ui().launch_copyapp_from_widget_more_options()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)

    # Visible, enabled
    spice.validate_button(copymode_button)

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    
    """
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app through one touch quickset more options button and check copy mode button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:200
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_onetouch_moreoptions_copymode
    +test:
        +title:test_copy_onetouch_moreoptions_copymode
        +guid: 26b98099-9a1d-4947-8058-41f142f89a44
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & DeviceFunction=Quickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_onetouch_moreoptions_copymode(setup_teardown_default_copy_mode, spice, cdm, net, udw):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    csc = CDMShortcuts(cdm, net)

    # Make sure media is  present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
    csc.shortcuts_init("MyCopy")
    shortcut_id = str(uuid.uuid4())
    csc.create_custom_shortcut("MyCopy1", shortcut_id, "scan", ["print"], "execute",
                                "true", False, csc.JobTicketType.COPY)

    # CopyApp
    menu_app = spice.homeMenuUI()
    menu_app.goto_menu_quickSets_and_check_loading_screen(spice, net, quickset_type="copy")
    menu_app.select_onetouch_quickset_from_menu_quickset(spice, "#MyCopy1")

    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)
    # Visible, enabled
    spice.validate_button(copymode_button, False)

    # Back Home
    csc.delete_shortcut(shortcut_id)

    spice.copy_app.finish_copy( expanded = True )
    menu_app.wait_for_menu_quickSets_screen(spice)
    spice.goto_homescreen_back_button()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app and do a direct copy with one page. Expect success job.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_direct_copy_single_page
    +test:
        +title:test_copy_ui_direct_copy_single_page
        +guid: e7518e54-0f1c-4dd1-8e53-e20053886016
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_direct_copy_single_page(setup_teardown_default_copy_mode, spice, cdm, job, net, udw):
    
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Set media not loaded from start
    Control.validate_result(scan_action.unload_media("MDF"))

    # Make sure copy mode is direct
    copy_instance = Copy(cdm, udw)
    copy_instance.set_copymode_direct()

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # wait for copy landing view
    spice.copy_ui().wait_for_copy_landing_view()

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)
    # Visible, enabled
    spice.validate_button(copymode_button)

    # Insert media
    spice.copy_ui().wait_main_button_to_start_copy(cdm, is_constrained = True)
    Control.validate_result(scan_action.load_media("MDF"))

    # Copy starts automatically, wait scanner is ready
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Validate Done button text.
    expected_done_text_button = CommonActions.get_translated_text_in_device_language(cdm, "cDoneButton")
    spice.copy_app.wait_until_text_button(spice.copy_app.locators.done_button, expected_done_text_button)
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.done_button)

    # Finish Copy (click on button done)
    spice.copy_app.finish_copy()

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id)

    # Check if the new job has been generated  
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app and do a direct copy with three pages. Expect success job.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_direct_copy_three_pages
    +test:
        +title:test_copy_ui_direct_copy_three_pages
        +guid: 3e7266a8-b6c1-11ee-8fb5-73b5761e9a7b
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_direct_copy_three_pages(setup_teardown_default_copy_mode, spice, cdm, job, tcl, udw):
    job_concurrency_path = job.job_concurrency_supported == "true"
    scan_action = ScanAction()
    scan_action.set_udw(udw).set_tcl(tcl)

    # Set media not loaded from start
    Control.validate_result(scan_action.unload_media("MDF"))

    # Simulation DIN A0
    scan_action.set_scan_random_acquisition_mode(841, 1189)

    # Make sure copy mode is direct
    copy_instance = Copy(cdm, udw)
    copy_instance.set_copymode_direct()

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # wait for copy landing view
    spice.copy_ui().wait_for_copy_landing_view()

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)
    # Visible, enabled
    spice.validate_button(copymode_button)

    # Wait that button is completely loaded before start range iteration
    spice.copy_ui().wait_main_button_to_start_copy(cdm, is_constrained = True)
    for page_number in range(3):

        # Insert media, ensuring that simulator is in correct state and transitions occurs as expected
        scan_action.check_scanner_state(ScannerState.READY)
        Control.validate_result(not scan_action.is_media_loaded("MDF"))
        Control.validate_result(scan_action.load_media("MDF"))

        # Copy starts automatically, wait scanner is ready
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

        # Wait for previews.
        if job_concurrency_path:
            spice.scan_settings.wait_for_preview_n(page_number + 1)

        # Validate Done button text.
        expected_done_text_button = CommonActions.get_translated_text_in_device_language(cdm, "cDoneButton")
        spice.copy_app.wait_until_text_button(spice.copy_app.locators.done_button, expected_done_text_button)
        # Increase the timeout to 15 s since the plot is an A0 and with 7 s sometimes it times out
        spice.copy_app.wait_locator_enabled(spice.copy_app.locators.done_button, 15)
    
    # Finish Copy (click on button done)
    spice.copy_app.finish_copy()

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id)

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

    # Restore default simulation
    scan_action.reset_simulation_mode()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app and change copy mode to direct copy. Verify that copymode changed with cdm.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_change_copymode
    +test:
        +title:test_copy_ui_change_copymode
        +guid: cbf655b2-4e08-4f07-bb44-0b72faf1829c
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_change_copymode(setup_teardown_default_copy_mode, spice,cdm,udw):
    
    # Start with indirect copy mode
    copy_instance = Copy(cdm, udw)

    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check copy mode button
    copymode_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_button)
    # Visible, enabled
    spice.validate_button(copymode_button)

    # Click on copy mode button
    copymode_button.mouse_click()
    
    # Check there exists 2 options inside the copy mode menu both enabled
    indirect_mode = spice.wait_for(CopyAppWorkflowObjectIds.copymode_modal_indirect_copy_menu_radio_button)
    spice.validate_button(indirect_mode)

    direct_mode = spice.wait_for(CopyAppWorkflowObjectIds.copymode_modal_direct_copy_menu_radio_button)
    spice.validate_button(direct_mode)

    # Click on direct copy mode
    direct_mode.mouse_click()

    # Exit dialog
    close_button = spice.wait_for(CopyAppWorkflowObjectIds.copymode_modal_close_button)
    close_button.mouse_click()
    
    # Check via cdm the copymode has changed and its direct.
    assert copy_instance.is_copymode_direct()
    assert not copy_instance.is_copymode_indirect()

    # Back Home
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter settings app and change copy mode to direct copy. Verify that copymode changed with cdm.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_settings_change_copymode
    +test:
        +title:test_settings_change_copymode
        +guid: bba0d71c-765c-4ca2-9092-52220aed5562
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_settings_change_copymode(setup_teardown_default_copy_mode, spice, udw, cdm, net, locale: str = "en"):
    
    # Start with indirect copy mode
    copy_instance = Copy(cdm, udw)

    # Navigate to copymode in settings
    spice.homeMenuUI().goto_copymodeoptions(spice, net, locale)

    # Check via cdm the copymode is indirect
    assert copy_instance.is_copymode_indirect()

    # Check there exists 2 options inside the copy mode menu both enabled
    indirect_mode = spice.wait_for(CopyAppWorkflowObjectIds.copymode_modal_indirect_copy_menu_radio_button)
    spice.validate_button(indirect_mode)

    direct_mode = spice.wait_for(CopyAppWorkflowObjectIds.copymode_modal_direct_copy_menu_radio_button)
    spice.validate_button(direct_mode)

    # Click on direct copy mode
    direct_mode.mouse_click()

    # Wait until direct mode radiobutton is activated
    spice.wait_until(lambda: direct_mode["checked"], timeout = 2.0)

    # Check via cdm the copymode has changed and its direct.
    assert copy_instance.is_copymode_direct()
    assert copy_instance.is_allow_interrupt_active()
    assert not copy_instance.is_copymode_indirect()

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check that a cdm patch of copyMode is allowed or not.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134203
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_cdm_settings_copymode_permission
    +test:
        +title:test_copy_cdm_settings_copymode_permission
        +guid: 518bbb28-b558-11ee-975f-3fcb63a5e1d0
        +dut:
            +type:Simulator,Emulator
            +configuration: DeviceFunction=Copy & DeviceClass=MFP & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_settings_copymode_permission(setup_teardown_default_copy_mode, cdm, configuration):    
    # Attempt to change copy mode
    try:
        path_return = cdm.put_raw(CdmEndpoints.COPY_CONFIGURATION_ENDPOINT, {"copyMode": "printWhileScanning"})
        assert path_return.status_code == 204 # OK with no content
    except HTTPError:
        # If patch fails, check if the device is a designjet to notify test error
        assert configuration.familyname != "designjet"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Cancel Direct Copy Job Warning Prompt when user press home Button in CopyApp and Cancel Job 
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-102306
    +timeout:120
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_direct_copy_validate_cancel_job_warning_prompt_on_home_event_then_cancel_job_in_preview_state
    +test:
        +title:test_copy_ui_when_direct_copy_validate_cancel_job_warning_prompt_on_home_event_then_cancel_job_in_preview_state
        +guid:09d1afbc-bf95-11ee-a9e1-a37181b1d2ca
        +dut:
            +type:Simulator
            +configuration: DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy= ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

@pytest.mark.skip(reason="Fails with DEVICE NOT READY in TearDown, locally passing, it requires investigation, we'll fix it in future DUNE-210189")
def test_copy_ui_when_direct_copy_validate_cancel_job_warning_prompt_on_home_event_then_cancel_job_in_preview_state(spice, job, udw, cdm, setup_teardown_print_device, setup_teardown_default_copy_mode):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    # Make sure media is  present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Make sure copy mode is direct
    copy_instance = Copy(cdm, udw)
    copy_instance.set_copymode_direct()

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
    +purpose: test Cancel Direct Copy Job Warning Prompt when user press home Button in CopyApp and then don't cancel
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-102306
    +timeout:180
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_direct_copy_validate_cancel_job_warning_prompt_on_home_event_then_do_not_cancel_in_preview_state
    +test:
        +title:test_copy_ui_when_direct_copy_validate_cancel_job_warning_prompt_on_home_event_then_do_not_cancel_in_preview_state
        +guid:faf19516-bf94-11ee-b521-53fd8c1afb07
        +dut:
            +type:Simulator
            +configuration: DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_direct_copy_validate_cancel_job_warning_prompt_on_home_event_then_do_not_cancel_in_preview_state(spice, udw, job, cdm, setup_teardown_print_device, setup_teardown_default_copy_mode):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    # Make sure media is  present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Make sure copy mode is direct
    copy_instance = Copy(cdm, udw)
    copy_instance.set_copymode_direct()

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
    +purpose: Test Cancel Direct Copy Job from not home action button then copy app should still there without crashes
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-175557
    +timeout:180
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_direct_copy_validate_cancel_job_externally_and_copy_app_return_to_idle_state
    +test:
        +title:test_copy_ui_when_direct_copy_validate_cancel_job_externally_and_copy_app_return_to_idle_state
        +guid:f6694890-bf94-11ee-9ecb-1796cf50f9cc
        +dut:
            +type:Simulator
            +configuration: DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_direct_copy_validate_cancel_job_externally_and_copy_app_return_to_idle_state(spice, job, udw, cdm, setup_teardown_print_device, setup_teardown_default_copy_mode):
    
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    # Make sure media is  present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Make sure copy mode is direct
    copy_instance = Copy(cdm, udw)
    copy_instance.set_copymode_direct()

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
