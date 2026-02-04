import logging
import uuid
import pytest
from dunetuf.send.common import common
from dunetuf.copy.copy import *
from dunetuf.ssh import SSH
from dunetuf.job.job import Job
import dunetuf.common.commonActions as CommonActions
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from tests.ui.lib.actions.commonsActions import *
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.control.control import Control
from dunetuf.localization.LocalizationHelper import LocalizationHelper


N_COPIES = 3
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify visual components of copy app are correctly loaded when widget opens app from click on settings button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-52678
    +timeout:500
    +asset:Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_verify_app_configuration_when_is_opened_by_settings_button
    +test:
        +title:test_copy_widget_verify_app_configuration_when_is_opened_by_settings_button
        +guid:baa74e48-c4b2-11ed-b0f7-7f1cb5d92de5
        
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_verify_app_configuration_when_is_opened_by_settings_button(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Start Copy.
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # Size of the FrontPanel.
    ui_size = udw.mainUiApp.ControlPanel.getBreakPoint()

    # App must be open for all products.
    spice.copy_ui().wait_for_copy_landing_view_from_widget_or_one_touch_quickset()

    if ui_size in ["XL"]:
        # Preview and summarize settings shown.
        assert not spice.copy_ui().is_landing_expanded(spice)

        # Quicksets must be shown.
        assert spice.copy_ui().are_quicksets_visible(spice)

    # Go back to mainApp and check that value has remained after entering the copyApp.
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, True)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test that changing the number of copies in the widget and clicking and going in quickset is there on moreoptions to open copyapp reflects same number of copies.
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-89750
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_widget_change_num_copies_and_launch_copyapp_to_verify_num_copies_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_widget_change_num_copies_and_launch_copyapp_to_verify_num_copies_quickset
        +guid:c632c390-f99c-4136-a119-3716b0d42378
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset & UIComponent=CopyWidget
   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_change_num_copies_and_launch_copyapp_to_verify_num_copies_quickset(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device, net):

    # Create some instance of the common actions ScanAction class
    csc = CDMShortcuts(cdm, net)
    shortcut_id = str(uuid.uuid4())
    # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
    csc.create_custom_shortcut("MyCopy", shortcut_id, "scan", [
                                "print"], "open", "true", False, csc.JobTicketType.COPY)
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Change number of copies
    spice.copy_ui().change_num_copies(N_COPIES)
    
    spice.copy_ui().launch_copyapp_from_widget_more_options()
    spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
    spice.copy_ui().goto_copy_options_list()
    assert spice.copy_ui().get_number_of_copies() == N_COPIES
    spice.copy_ui().back_to_landing_view()
    
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    # delete previously added shorcut
    csc.delete_shortcut(shortcut_id)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with copy number as 1
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_copy_num_1
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_copy_num_1
        +guid: e61a80ff-51fa-42f6-8f50-e25d2780da67
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_copy_num_1(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'copies': '1'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation) 
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with copy number as 999
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:1620
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_copy_num_999
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_copy_num_999
        +guid: f6d72da7-7397-42ad-a3f9-1e8c57231817
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_copy_num_999(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    job.clear_joblog
    try:
        copy_job_app = spice.copy_ui()
        #reducing to 99 as 999 jobs take longer time
        options = {
            'copies': '99'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs(time_out=1500)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Validate that the JobTicket propagates user-set numCopies back into copyWidget on HomeScreen.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-102475
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_widget_change_num_copies_and_verify_num_copies_on_widget_exit
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_widget_change_num_copies_and_verify_num_copies_on_widget_exit
        +guid:4abc5e16-9bc1-4df0-8ad3-ad43184f0d3f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy  & Widget=Settings & UIComponent=CopyWidget
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_change_num_copies_and_verify_num_copies_on_widget_exit(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    expected_number_of_incremented_copies = 4
    expected_number_of_default_copies = 1

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Change number of copies
    spice.copy_ui().change_num_copies(expected_number_of_incremented_copies)
    
    # decrease to 3
    spice.copy_ui().decrease_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)

    # launch Copy App more Options
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # validate incremented counts
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().back_to_landing_view()

    # go back to mainApp to check that value has remained after entering the copyApp:
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Check the copy Count in the widget. Should match what we set it to!:
    assert spice.copy_ui().get_number_of_widget_copies() == expected_number_of_default_copies

    # Reset the copy count:
    spice.copy_ui().change_num_copies(SINGLE_COPY_COUNT_INCREMENT)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. Open copy app and copy with default values N repeated times.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_copy_with_default_values_3_repeated_times
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_enter_app_and_copy_with_default_values_3_repeated_times
        +guid: 70575238-0969-4de0-b910-1d8427cb2cf7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=ImagePreview
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


# Test name
def test_copy_ui_enter_app_and_copy_with_default_values_3_repeated_times(spice, scan_emulation, cdm, udw, net, configuration, job):
    # Fixtures
    duneJobInterface = Job(cdm, udw)
    jobIds = duneJobInterface.get_recent_job_ids()
    lastJobId = jobIds[len(jobIds) - 1]
    jobIds.clear()
    adfLoaded = True
    common_instance = common.Common(cdm, udw)
    loadmedia = common_instance.scan_resource()
    loadmedia = "Flatbed" if loadmedia == "Glass" else loadmedia

    spice.copy_ui().goto_copy()
    for copy_n_time in range(N_COPIES):
        job.bookmark_jobs()
        if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
            scan_emulation.media.load_media('MDF', 1)

            if not copy_n_time: 
                spice.copy_ui().start_preview()
            spice.copy_ui().verify_preview()
        if loadmedia == "Flatbed":
            adfLoaded = False
        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded=adfLoaded)
        if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
            spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()
        sleep(2)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    spice.copy_ui().goto_menu_mainMenu()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. Open copy app 3 times and copy one job per time.
        It is only dial because for selene we have no home button to go back to the home
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_enter_app_3_times_and_copy_one_job_per_time
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_enter_app_3_times_and_copy_one_job_per_time
        +guid:0cb30f2a-5150-4b5f-8e37-36b2cf56e18a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


# Test name
def test_copy_ui_enter_app_3_times_and_copy_one_job_per_time(cdm, udw, spice, net, configuration):
    # Fixtures
    duneJobInterface = Job(cdm, udw)
    jobIds = duneJobInterface.get_recent_job_ids()
    lastJobId = jobIds[len(jobIds) - 1]
    jobIds.clear()

    for _ in range(N_COPIES):
        spice.copy_ui().goto_copy()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message="Complete", timeout=60)
    spice.copy_ui().goto_menu_mainMenu()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. Open copy app and copy with default values 3 copies of one job
        It is only dial because for selene we have no home button to go back to the home
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_copy_with_default_values_3_copies_of_one_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_enter_app_and_copy_with_default_values_3_copies_of_one_job
        +guid: 687a84dd-aae9-40f8-8bf4-d220846e6b9a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name
def test_copy_ui_enter_app_and_copy_with_default_values_3_copies_of_one_job(spice, net, configuration):
    spice.copy_ui().goto_copy()
    spice.copy_ui().ui_copy_set_no_of_pages(N_COPIES)
    spice.copy_ui().ui_select_copy_page()
    sleep(5)
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, timeout=60)
    spice.copy_ui().goto_menu_mainMenu()
