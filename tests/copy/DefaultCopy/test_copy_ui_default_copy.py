from dunetuf.send.common import common
import logging
import time
from dunetuf.copy.copy import *
from dunetuf.power.power import Power, ActivityMode
from tests.copy import CopyBasicQuicksetHelper
import uuid
import pytest
from dunetuf.ssh import SSH
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

N_COPIES = 5
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0

def __power_cycle(udw):
    '''
    Reboot simulator using udw command.
    '''
    powerObj = Power(udw)
    powerObj.power_cycle()
    time.sleep(10)

@pytest.fixture
def setup_teardown_copy_widget(spice, job, outputsaver, device, media, tclMaia, ssh: SSH, udw, configuration):
    yield
    home_screen = spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
    if(home_screen["activeFocus"] != True):
        logging.error("ActiveFocus disabled. Unable to proceed.")
        if configuration.productname in ["camden", "jasper"]:
            __power_cycle(udw)
        else:
            ssh.run("/sbin/reboot")
        device.device_ready(150)
        home_screen = spice.wait_for(SignInAppWorkflowObjectIds.homeScreenView)
        spice.wait_until(lambda: home_screen["activeFocus"] == True, 120)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Start copy from copy widget.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-52678
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_walkupapp_copy_widget_ui_start_copy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_walkupapp_copy_widget_ui_start_copy
        +guid:b9c9a795-fa09-4e81-ad61-9ac2341964d9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_walkupapp_copy_widget_ui_start_copy(spice, cdm, udw, job, configuration, net, setup_teardown_print_device):
    # Create some instance of the common actions ScanAction class
    udw.mainApp.ScanMedia.loadMedia("ADF") #test failed because of some previous test which cause job to launch from flatbed
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    #Mfp's need paper loaded to start automaticaly copy from widget
    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")

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
        spice.copy_ui().wait_for_copy_landing_view_from_widget_or_one_touch_quickset()
        assert spice.copy_ui().is_landing_expanded(spice)

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


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 2up, 20 copies, 1_1 sided, grayscale, Photo through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui__validate_basic_copy_scenario_1_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui__validate_basic_copy_scenario_1_via_quickset
        +guid:dc94f389-6755-4811-9309-0c51aa0e2515
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & ADFMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui__validate_basic_copy_scenario_1_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'colorMode': 'grayscale',
        'copies': 20,
        'pagesPerSheet': 'twoUp',
        'contentType': 'photo'
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1up, 20 copies, 1_1 sided, color, Text, fitToPage through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_2_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_2_via_quickset
        +guid:79fbb6a6-62ab-4e79-838a-fc9e4571db45
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_2_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 20,
        'pagesPerSheet': 'oneUp',
        'contentType': 'text',
        'outputScale': 'fitToPage'
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1up, 1 copies, 1_1 sided, color, text, fullpage through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_3_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_3_via_quickset
        +guid:5653d01d-bd08-427b-a544-1c74c22c676e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset & CopyOutputScale=FullPage

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_3_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 1,
        'pagesPerSheet': 'oneUp',
        'contentType': 'text',
        'outputScale': 'fullPage'
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1up, 20 copies, 1_1 sided, grayscale, mixed, custom through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_4_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_4_via_quickset
        +guid:a0a546c6-f737-4a8d-8bc1-808e77426538
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & ADFMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_4_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'colorMode': 'grayscale',
        'copies': 20,
        'pagesPerSheet': 'oneUp',
        'contentType': 'mixed',
        'outputScale': 'custom',
        'customValue': 55
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 50 copies, 1up, photo, color, 1_2 sided through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_5_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_5_via_quickset
        +guid:3617f87e-4d62-490d-aa4d-86a636dafdb0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_5_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 50,
        'pagesPerSheet': 'oneUp',
        'sides': '1_2Sided',
        'contentType': 'photo'
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1 copy, 2up, 1_2 sided, fitToPage, grayscale, text through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_6_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_6_via_quickset
        +guid:9bb0107b-c69e-46db-a042-f0b07cc03655
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_6_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 1,
        'pagesPerSheet': 'twoUp',
        'sides': '1_2Sided',
        'colorMode': 'grayscale',
        'contentType': 'text',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 20 copies, 1up, 1_2 sided, fullPage, color, photo through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_7_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_7_via_quickset
        +guid:20781252-a5e5-4aa2-8b70-37f5283dafc3
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset & CopyOutputScale=FullPage

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_7_via_quickset(scan_emulation,cdm, udw, spice, net, job):
    
    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 20,
        'pagesPerSheet': 'oneUp',
        'sides': '1_2Sided',
        'outputScale': 'fullPage',
        'contentType': 'photo',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 20 copies, 2up, 1_2 sided, custom, color, mixed through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_8_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_8_via_quickset
        +guid:471e0df8-b418-4489-9803-116069c04e22
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_8_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 20,
        'pagesPerSheet': 'twoUp',
        'sides': '1_2Sided',
        'contentType': 'mixed',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1 copy, 1up, 2_1 sided, grayscale, text through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_9_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_9_via_quickset
        +guid:8da4074e-48d9-4547-b227-0df03959a92b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & FlatbedMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_9_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 1,
        'pagesPerSheet': 'oneUp',
        'sides': '2_1Sided',
        'colorMode': 'grayscale',
        'contentType': 'text',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 10 copies, 2up, 2_1 sided, fitToPage, grayscale, mixed through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_10_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_10_via_quickset
        +guid:37d5afb9-b222-4fdc-bfc8-165a471299a5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & FlatbedMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_10_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 10,
        'pagesPerSheet': 'twoUp',
        'sides': '2_1Sided',
        'colorMode': 'grayscale',
        'contentType': 'mixed',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 50 copies, 1up, 2_1 sided, fullPage, grayscale, photo through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_11_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_11_via_quickset
        +guid:e7a2fe26-a8cc-45e7-a7d8-a092d7ceb81e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & CopyOutputScale=FullPage

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_11_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 50,
        'pagesPerSheet': 'oneUp',
        'sides': '2_1Sided',
        'outputScale': 'fullPage',
        'colorMode': 'grayscale',
        'contentType': 'photo',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1 copy, 2up, 2_1 sided, custom, color, text through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_12_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_12_via_quickset
        +guid:16053b07-9815-4b81-9693-032dd86006c0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_12_via_quickset(scan_emulation,cdm, udw, spice, net, job):
    
    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 1,
        'pagesPerSheet': 'oneUp',
        'sides': '2_1Sided',
        'outputScale': 'custom',
        'customValue': 55,
        'contentType': 'text',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 20 copies, 2up, 2_2 sided, grayscale, mixed through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_13_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_13_via_quickset
        +guid:3340280e-96fc-4741-8c5d-13e9dcf62bc6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & FlatbedMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_13_via_quickset(scan_emulation, cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 20,
        'pagesPerSheet': 'twoUp',
        'sides': '2_2Sided',
        'colorMode': 'grayscale',
        'contentType': 'mixed',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation, cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 20 copies, 1up, 2_2 sided, fitToPage, color, photo through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_14_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_14_via_quickset
        +guid:22f11e36-149f-4869-9493-36f51f85f613
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_14_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 20,
        'pagesPerSheet': 'oneUp',
        'sides': '2_2Sided',
        'outputScale': 'fitToPage',
        'contentType': 'photo',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1 copy, 2up, 2_2 sided, fullPage, color, text through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_15_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_15_via_quickset
        +guid:4e25eee4-3af7-42e3-b7b5-059c8d188e39
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_15_via_quickset(scan_emulation, cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 1,
        'pagesPerSheet': 'twoUp',
        'sides': '1_2Sided',
        'contentType': 'text',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation, cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1 copy, 2up, 2_2 sided, custom, grayscale, photo through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_16_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_16_via_quickset
        +guid:0c7c491f-b948-464f-937d-1bd918b0c49a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_16_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 1,
        'pagesPerSheet': 'twoUp',
        'sides': '2_2Sided',
        'colorMode': 'grayscale',
        'contentType': 'photo',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy job of 1 copy, 2up, 2_2 sided, custom, grayscale, photo through quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-100501
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns 
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_basic_copy_scenario_17_via_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_basic_copy_scenario_17_via_quickset
        +guid:62501e17-0c7f-42fe-968d-722293eef295
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FitToPage & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=GrayScale & FlatbedMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_basic_copy_scenario_17_via_quickset(scan_emulation,cdm, udw, spice, net, job):

    settings = {
        'inputMediaSize': 'na_letter_8.5x11in',
        'copies': 20,
        'pagesPerSheet': 'oneUp',
        'sides': '2_2Sided',
        'outputScale': 'fitToPage',
        'colorMode': 'grayscale',
        'contentType': 'text',
        }
    CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)
    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Perform a default single copy job.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui__default_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui__default_copy_job
        +guid:a3278751-3909-4545-b478-934e43e561aa
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator    
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui__default_copy_job(setup_teardown_with_copy_job, cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()

    # common_instance = common.Common(cdm, udw)
    # scan_resource = common_instance.scan_resource()
    copy_job_app = spice.copy_ui()
    scan_resource = copy_job_app.get_scan_resource_used(udw, scan_emulation)
    scan_resource = "Flatbed" if scan_resource == "Glass" else scan_resource
    options = {}
    loadmedia= scan_resource
    copy_path = 'CopyLandingPage'
    copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
    job.wait_for_no_active_jobs()
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=20)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Entry Exit test case for Copy from Menu
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ui__entry_exit
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui__entry_exit
        +guid:8221b015-a77f-4679-b8cc-98303fa01856
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.disable_autouse
def test_copy_ui__entry_exit(setup_teardown_homescreen, cdm, spice, job, udw, net):
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Entry Exit test case for Copy from Menu 2 times
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ui_entry_exit_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_entry_exit_job
        +guid:a6bf0171-4e89-46c0-94e8-69a9f8aeee20
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP & ScannerInput=AutomaticDocumentFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_entry_exit_job(setup_teardown_with_copy_job, cdm, spice, job, udw, net,configuration):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    job.bookmark_jobs()
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    spice.goto_homescreen()

    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("Start to copy")
    copy_job_app.start_copy()
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Entry Exit test case for Copy from Menu
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ui__all_options_entry_exit
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui__all_options_entry_exit
        +guid:89cef2e9-3b15-4a56-b28a-dc8631c10f48
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui__all_options_entry_exit(spice):
    spice.cleanSystemEventAndWaitHomeScreen()
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.back_to_landing_view()
    spice.goto_homescreen()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy from documentfeeder with default setting
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_documentfeeder_with_default_values
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_documentfeeder_with_default_values
        +guid:57632a28-feca-4f27-b2d0-b07661e48f61
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=Collation

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator



$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_job_documentfeeder_with_default_values(setup_teardown_with_copy_job, scan_emulation, job, spice, cdm, udw, net, configuration):
    # todo: need check copy toast, wait for HMDE-285
    # Ensure media is present before going to App screen
    logging.info("load the ADF media")
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("check the strings on copy screen")
    copy_job_app.check_spec_on_copy_home(net)
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy()
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        sides="oneSided",
        orientation="portrait",
        quality="normal",
        content_type="mixed",
        two_side_page_flip_up="false",
        pages_per_sheet="oneUp",
        collate="collated"
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy from flatbed with default setting
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_flatbed_with_default_values
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_flatbed_with_default_values
        +guid:b60a1769-cbd3-42c4-9500-37c7a5f535d1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed  & Copy=Collation


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_job_flatbed_with_default_values(setup_teardown_with_copy_job, scan_emulation, job, spice, net, cdm, udw, configuration):
    logging.info("load the Flatbed media")
    scan_emulation.media.unload_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")
    
    value = "collated"
    if configuration.familyname in ["homepro"]:
        value = "uncollated"

    
    # todo: need check "Preview" on Copy Home, wait for bug HMDE-344
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    time.sleep(3)
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = False)
    if job.job_concurrency_supported == "false":
        copy_job_app.wait_for_release_page_prompt_and_click_relasePage()
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        sides="oneSided",
        orientation="portrait",
        quality="normal",
        content_type="mixed",
        two_side_page_flip_up="false",
        pages_per_sheet="oneUp",
        collate=value
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    scan_emulation.media.load_media(media_id='ADF')

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy while printer is busy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_printer_busy_from_document_feeder
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_printer_busy_from_document_feeder
        +guid:9eab82df-c121-44fe-8679-5ba2a56a600e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_printer_busy_from_document_feeder(scan_emulation, setup_teardown_with_copy_job, job, spice, udw, cdm, net):
    logging.info("load the ADF media")
    scan_emulation.media.load_media(media_id='ADF', media_numsheet=10)
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.start_copy()
    logging.info("Behaviour changed from Proselect : when click on start button it gets disabled until scanner is available")
    copy_job_app.check_copy_start_button_disabled()
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter Exit Copy App for Basic memory usage
    +test_tier: 3
    +is_manual: False
    +reqid:122346
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_app_with_default_values
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_app_with_default_values
        +guid:c2119d01-a824-4832-93f8-3c7a4995d3ec
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_app_with_default_values(setup_teardown_with_copy_job, spice, net, cdm, udw, configuration,job):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")

    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    time.sleep(3)
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    copy_job_app.start_copy()
    if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
        copy_job_app.wait_for_release_page_prompt_and_click_relasePage(timeout =50)
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, timeout=120)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

