
import logging
import uuid
import pytest
from dunetuf.ssh import SSH
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.cdm.CdmEndpoints import CdmEndpoints
from tests.ui.lib.actions.commonsActions import *
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

N_COPIES = 5
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Start copy from copy widget.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-52678
    +timeout:600
    +asset:Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_ui_start_copy
    +test:
        +title:test_copy_widget_ui_start_copy
        +guid:7475b0dd-85c0-48f1-8e36-16280c8422cf
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_ui_start_copy(spice, cdm, udw, job, configuration, net, setup_teardown_print_device):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    #Mfp's need paper loaded to start automaticaly copy from widget
    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")
    else:
        udw.mainApp.ScanMedia.unloadMedia("ADF")

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Check number of copies default value (widget)
    assert spice.wait_for(CopyAppWorkflowObjectIds.spinBox_widget_numberOfCopies)["value"] == 1

    # Start Copy 
    spice.copy_ui().start_copy_widget()
    if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
          spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()
          #spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration,"Complete")
          spice.goto_homescreen()
          #copy will be verified using cdm

    # Size of the FrontPanel
    ui_size = udw.mainUiApp.ControlPanel.getBreakPoint()
    if ui_size in ["XL"]:
        #Wait and check Copy app must be expanded
        spice.copy_ui().wait_for_landing_is_expanded()
        
        #Check Qs must not be shown
        assert not spice.copy_ui().are_quicksets_visible(spice)

        # Wait for copy button to be enabled.
        spice.copy_ui().copy_button_present(spice, 15)

        # Click Copy button to finish job, and returning to home
        spice.copy_ui().wait_and_click_copy_button_of_main_panel(spice, cdm, 15)

        # Check toast appear
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='preparingToCopy', timeout=3)


    spice.validate_app(home, True)

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id)

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Wait to receive a completed job
    job.wait_for_job_completion(job.get_last_job_id())

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    if not "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("ADF")        

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test that changing the number of copies in the widget functions.
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-52678
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_widget_change_num_copies_and_copy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_widget_change_num_copies_and_copy
        +guid:ee57324b-9bc4-45ed-ad54-661ceb2f99ee
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & UIComponent=CopyWidget

   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_change_num_copies_and_copy(spice, cdm, udw, tcl,configuration, job, copy,setup_teardown_print_device):
    job.clear_joblog()
    # Create some instance of the common actions ScanAction class
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Change number of copies
    spice.copy_ui().change_num_copies(N_COPIES)

    # Start Copy
    spice.copy_ui().start_copy_widget()


    if configuration.familyname == "enterprise":
        job.wait_for_alerts('flatbedAddPage')
        job.alert_action('flatbedAddPage', 'Response_02')    

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id)

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"
    job.wait_for_job_completion(job_id)

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Change number of copies back to default
    spice.copy_ui().change_num_copies(1)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test that changing the number of copies in the widget and clicking on moreoptions to open copyapp reflects same number of copies.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-89750
    +timeout:500
    +asset:Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_change_num_copies_and_launch_copyapp_to_verify_num_copies
    +test:
        +title:test_copy_widget_change_num_copies_and_launch_copyapp_to_verify_num_copies
        +guid:725dac17-083e-4b06-8e59-457856730862
        +dut:
            +type:Simulator,Emulator,Engine
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget
   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_change_num_copies_and_launch_copyapp_to_verify_num_copies(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Change number of copies
    spice.copy_ui().change_num_copies(N_COPIES)
    spice.copy_ui().launch_copyapp_from_widget_more_options()
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().goto_no_of_copies()
    assert spice.copy_ui().get_number_of_copies() == N_COPIES
    spice.copy_ui().back_to_landing_view()
    
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test that changing the number of copies in the copy Widget via the up button is reflected under the moreOptions.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-102475
    +timeout:300
    +asset:Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_widget_increase_num_copies_and_verify_num_copies
    +test:
        +title:test_copy_widget_increase_num_copies_and_verify_num_copies
        +guid:f13fe2cb-7d4c-4bd3-93b5-8cd1decafdd1
        +dut:
            +type:Simulator, Engine
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_increase_num_copies_and_verify_num_copies(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    expected_number_of_incremented_copies = 4

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Reset the copy count to 1
    spice.copy_ui().change_num_copies(SINGLE_COPY_COUNT_INCREMENT)

    # Change number of copies
    # increase to 2
    spice.copy_ui().increase_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    assert spice.copy_ui().get_number_of_widget_copies() == 2

    # increase to 3
    spice.copy_ui().increase_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    assert spice.copy_ui().get_number_of_widget_copies() == 3

    # increase to 4
    spice.copy_ui().increase_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    assert spice.copy_ui().get_number_of_widget_copies() == expected_number_of_incremented_copies

    # launch Copy App more Options
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # validate incremented counts
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().goto_no_of_copies()
    # validate the number of copies in the copy app
    assert spice.copy_ui().get_number_of_copies() == expected_number_of_incremented_copies
    spice.copy_ui().back_to_landing_view()

    # go back to mainApp to test decrementing:
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # reset the copy Count:
    spice.copy_ui().change_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test that changing the number of copies in the copy Widget via the up button is reflected under the moreOptions.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-102475
    +timeout:300
    +asset:Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_widget_decrease_num_copies_and_verify_num_copies
    +test:
        +title:test_copy_widget_decrease_num_copies_and_verify_num_copies
        +guid:27084423-857f-4ca2-b609-3e1a3acc8038
        +dut:
            +type:Simulator, Engine
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_decrease_num_copies_and_verify_num_copies(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    expected_number_of_incremented_copies = 4
    expected_number_of_decremented_copies = 2

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Change number of copies
    spice.copy_ui().change_num_copies(expected_number_of_incremented_copies)

    # decrease to 2
    spice.copy_ui().decrease_widget_num_copies(expected_number_of_decremented_copies)
    assert spice.copy_ui().get_number_of_widget_copies() == expected_number_of_decremented_copies

    # launch Copy App more Options
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # validate incremented counts
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().goto_no_of_copies()
    assert spice.copy_ui().get_number_of_copies() == expected_number_of_decremented_copies
    spice.copy_ui().back_to_landing_view()

    # go back to mainApp to test decrementing:
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # reset the copy Count:
    spice.copy_ui().change_num_copies(SINGLE_COPY_COUNT_INCREMENT)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test you can see the folding style setting constrained in more options window.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-141884
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_ui_folding_style_is_constrained_in_more_options
    +test:
        +title:test_copy_widget_ui_folding_style_is_constrained_in_more_options
        +guid: 5040e69a-c416-11ee-98d4-eb9aba975404
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & UIComponent=CopyWidget & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_widget_ui_folding_style_is_constrained_in_more_options(spice, cdm, setup_teardown_folding_style):

    body = {
        "dest": 
        {
            "print": 
            {
                'mediaDestination': 'stacker-1',
                'foldingStyleId': 259
            }
        }
    }

    # Set job ticket copy values
    cdm.put(CdmEndpoints.JOB_TICKET_COPY, body)

    # Go to CopyApp from widget copy
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # Go to More Options.
    spice.copy_ui().goto_copy_options_list()

    # Check if folding style is constrained
    spice.copy_ui().verify_folding_style_combobox_constrained()
    
    # Get back to Copy App.
    spice.copy_ui().close_options_detail_panel()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test you can see the folding style setting in more options window.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-141884
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_ui_folding_style_in_more_options
    +test:
        +title:test_copy_widget_ui_folding_style_in_more_options
        +guid: 3bbcef26-c4e7-11ee-bf2c-c3172ac5d649
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & UIComponent=CopyWidget & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_widget_ui_folding_style_in_more_options(spice, cdm, setup_teardown_folding_style):

    body = {
        "dest": 
        {
            "print": 
            {
                'mediaDestination': 'folder-1',
                'foldingStyleId': 259
            }
        }
    }

    # Set job ticket copy values
    cdm.put(CdmEndpoints.JOB_TICKET_COPY, body)

    # Go to CopyApp from widget copy
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # Go to More Options.
    spice.copy_ui().goto_copy_options_list()

    # Select the opposite folding style
    spice.copy_ui().select_folding_style("FoldingStyle1")
    
    # Get back to Copy App.
    spice.copy_ui().close_options_detail_panel()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Start copy from copy widget, then navigate to edit screen and exit.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-203572
    +timeout:120
    +asset:Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_widget_ui_start_copy_then_enter_edit
    +test:
        +title:test_copy_widget_ui_start_copy_then_enter_edit
        +guid:aa75fd7c-6f5f-11ef-a2f1-e3b08ebb4467
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget & ImagePreview=Edit
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_ui_start_copy_then_enter_edit(cdm, spice, udw, setup_teardown_print_device):
    # Create an instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Mfp's need paper loaded to start automaticaly copy from widget
    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")
    else:
        udw.mainApp.ScanMedia.unloadMedia("ADF")

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Start Copy.
    spice.copy_ui().start_copy_widget()
    spice.scan_settings.wait_for_preview_n(1)

    # Go to edit screen.
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_edit_done_button()

    # Click Copy button to finish job and return to home.
    spice.copy_ui().wait_and_click_copy_button_of_main_panel(spice, cdm, 15)