import logging
import time
import pytest
import dunetuf.common.commonActions as CommonActions

from dunetuf.control.control import Control
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from tests.ui.lib.actions.commonsActions import *
from time import sleep
import unittest
from dunetuf.copy.copy import Copy

N_COPIES = 3  # Number of copies  
SINGLE_COPY_COUNT_INCREMENT = 1

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. It is only Touch screen because 
        for selene we have no home button or common command with  designjet to go back to the home
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-22046
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_scan_a_job
    +test:
        +title:test_copy_ui_enter_app_and_scan_a_job
        +guid: 2de86c76-5166-47c9-ba78-255cb5be3b97
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_scan_a_job(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_instance = Copy(cdm, udw) 
    
    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()

    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy
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
    spice.validate_app(home, False)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test you can scan a sheet while in the more options window. Then go back to main app and complete it.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-119383
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_pagesensor_enter_more_options_and_scan
    +test:
        +title:test_copy_ui_pagesensor_enter_more_options_and_scan
        +guid: 069f5eee-ad11-11ed-afa9-7f81c4e6390e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.skip(reason="Not stable test, need investigation, we'll fix it in future DUNE-192444")
def test_copy_ui_pagesensor_enter_more_options_and_scan(spice, cdm, net, udw, tcl, job, copy,setup_teardown_print_device, locale: str = "en"):

    # Create an instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is NOT present before going to App screen
    Control.validate_result(scan_action.unload_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Goto to More Options.
    spice.copy_ui().press_options_detail_panel()
    optionPanel = spice.wait_for(CopyAppWorkflowObjectIds.setings_openSettings_option)
    spice.wait_until(lambda: optionPanel["visible"] == True, 5)

    # Load Media.
    Control.validate_result(scan_action.load_media("MDF"))

    # Wait for previews.
    previous_job_id = job.get_last_job_id()
    job_id = Job.find_job_manager_job_id(udw, previous_job_id, 30)

    # If the pages cdm report no pages the wait for previews return True immediately.
    sleep(1)
    Control.validate_result(job.wait_all_previews_done( job_id ))

    # Get back to Copy App.
    spice.copy_ui().close_options_detail_panel()

    # Wait until the copy button is enabled
    spice.main_app.wait_locator_enabled(spice.copy_app.locators.copy_button)

    # Finish Copy
    # I could cancel, but takes longer.
    spice.copy_app.finish_copy()

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    
    # Wait for the job completion and Get Job ID
    job.print_completed_job(last_job_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test probes that stop scan button works well and copy job ends successfully
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134225
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_scan_a_job_and_stop_it
    +test:
        +title:test_copy_ui_scan_a_job_and_stop_it
        +guid:05bbd3a0-f0ae-11ed-a952-77fe645d049f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_scan_a_job_and_stop_it(spice, cdm, net, udw, tcl, job, configuration, locale: str = "en"):

    # Create an instance of the common actions ScanAction class, set with a big size of plot
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw).set_configuration(configuration)
    # The previous size cause problems with stacker max size. Since the purpose of bigger plot is only 
    # introducing a delay for stop scan to appear, we are using this size + 600dpi resolution
    simulation = scan_action.set_scan_random_acquisition_mode(1000, 841)
    Control.validate_simulation(simulation)
    
    copy_instance = Copy(cdm, udw) 

    # Load media
    scan_action.load_media("MDF")

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    spice.copy_ui().press_options_detail_panel()
    spice.copy_ui().set_detailed_options_resolution("600Dpi")
    spice.copy_ui().close_options_detail_panel()
    
    # Start Copy
    spice.copy_ui().start_copy()

    # Stop Acquisition
    spice.copy_ui().scan_operations.go_and_verify_manually_stop_scanner_screen(udw, net, locale, "#CopyAppApplicationStackView")

    # Make sure scanning is done
    copy_instance.wait_for_corresponding_scanner_status_with_cdm("Idle", timeout=30)

    # Wait until the copy button is enabled
    spice.main_app.wait_locator_enabled(spice.copy_app.locators.copy_button)

    # Finish Copy
    spice.copy_app.finish_copy()

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id, 180)

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
    spice.validate_app(home, False)

    # Reset current simulation mode
    scan_action.reset_simulation_mode()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. Open copy app and copy with default values N repeated times.
        It is only Touch screen because for selene we have no home button or common command with  designjet to go back to the home
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_enter_copy_ui_app_and_copy_with_default_values_N_repeated_times
    +test:
        +title:test_enter_copy_ui_app_and_copy_with_default_values_N_repeated_times
        +guid: 0315c0c2-5c02-11eb-b064-cbb6b4b56f23
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_enter_copy_ui_app_and_copy_with_default_values_N_repeated_times(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_instance = Copy(cdm, udw) 

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)


    for i in range(N_COPIES):
        logging.info( "Iteration number " + str( i ) )
        # Get Job ID
        last_job_id = job.get_last_job_id()

        # Load media to trigger the next scan except on the first,
        # because media was already loaded when entering the app
        # and batch-scanning should start automatically.
        if i > 0:
            logging.info( "Loading media for job number " + str( i ) )

            # Ensure media is present
            Control.validate_result(scan_action.load_media("MDF"))
        else:
            # Start Copy
            logging.info( "Starting copy number " + str( i ) )
            spice.copy_app.start_copy()

        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

        # Finish Copy
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
    spice.validate_app(home, False)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. Open copy app n times and copy one job per time.
        It is only Touch screen because for selene we have no home button or common command with  designjet to go back to the home
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_n_times_and_copy_one_job_per_time
    +test:
        +title:test_copy_ui_enter_app_n_times_and_copy_one_job_per_time
        +guid: f6a5f302-5c01-11eb-befa-ffcb2076063a
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.timeout(500)
def test_copy_ui_enter_app_n_times_and_copy_one_job_per_time(setup_teardown_print_device, spice, cdm, udw, tcl, job, copy):

    # activate more logging
    # JRP: These calls are meant for debugging and not for general execution. 
    #tcl.execute("Debug PUB_setFilterLevelAcrossAllDomains c true") 
    #tcl.execute("Debug PUB_setFilterLevelAcrossAllDomains d true")

    copy_instance = Copy(cdm, udw) 
    
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw)
    simulation = scan_action.set_scan_random_acquisition_mode(210, 297)
    Control.validate_simulation(simulation)

    # Ensure we are in Homescreen
    spice.goto_homescreen()
    
    # Wait for HomeScreen to appear and dismiss SystemError if exists
    spice.cleanSystemEventAndWaitHomeScreen()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    for _ in range(N_COPIES):

        # Get Job ID
        last_job_id = job.get_last_job_id()

        # Ensure media is present before going to App screen
        Control.validate_result(scan_action.load_media("MDF"))

        spice.main_app.goto_copy_app()

        # CopyApp
        copy_app = spice.copy_app.get_copy_app()
        spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
        spice.validate_app(copy_app, False)

        # Start Copy and wait until Copy button is ready
        spice.copy_app.start_copy()
        spice.copy_ui().wait_main_button_to_finish_copy(cdm)
        
        # Click on Copy
        spice.copy_app.finish_copy()

        # Wait for the new job completion and Get Job ID
        job_id = job.print_completed_job(last_job_id, job_wait_time = 120)

        # Check if the new job has been generated
        assert job_id != last_job_id, "The new job has not been generated"

        # Get status job
        status_job = job.get_status_job(job_id)
        logging.info( "Job Status : {0}".format(status_job))
        # Check if status is completion and success
        assert status_job[1] == "COMPLETED", "Process Status is not completed"
        assert status_job[2] == "SUCCESS", "Process Status is not success"
        
        # Back To Home to set initial state again
        spice.copy_app.goto_home()
        spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
        spice.validate_app(home, False)



def getSizeTxt(width, resolution, isMetricInInches):
    if isMetricInInches:
        return str(dpiToInch(width, resolution)) + " inches"
    else:
        return str(dpiToMm(width, resolution)) + " mm"


def dpiToInch(value, resolution= 10000):
    return round(value / resolution)


def dpiToMm(value, resolution = 10000):
    result = (value / resolution)
    return round((result * 2.54) * 10)
    #2.54 = cm per inch



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check Paper selection in copy app
    +test_tier:1
    +is_manual: False
    +reqid:DUNE-147480
    +timeout:500
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_enter_app_and_check_paper_selecction
    +test:
        +title:test_copy_ui_enter_app_and_check_paper_selecction
        +guid:68ac4895-d2a2-4817-85c4-4cdba6f5b79c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & MediaInputInstalled=ROLL1 & MediaInputInstalled=ROLL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_paper_selecction(setup_teardown_copy_paper_source,spice, cdm, net, copy):

     # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    paper_source = spice.wait_for(spice.copy_app.locators.paper_source_combo )
    paper_source.mouse_click()
    sleep(2)

    popupRoll1= spice.wait_for("#ComboBoxOptionsroll_dash_1 SpiceText[visible=true]")["text"]
    popupRoll2= spice.wait_for("#ComboBoxOptionsroll_dash_2 SpiceText[visible=true]" )["text"]
    
    metric = cdm.get(cdm.SYSTEM_CONFIGURATION)
    isMetricInInches = False
    if(metric["displayUnitOfMeasure"]== "imperial"):
        isMetricInInches = True

    isRoll1 = True
    isCustom = True
    default_payload = cdm.get(cdm.CDM_MEDIA_CONFIGURATION)
    inputs = default_payload["inputs"]
    for i in range(len(inputs)):
        mediaSourceId = default_payload["inputs"][i]["mediaSourceId"]
        if("roll" in mediaSourceId):
            currentMediaType = default_payload["inputs"][i]["currentMediaType"]
            mediaWidth  = default_payload["inputs"][i]["currentMediaWidth"]
            resolution  = default_payload["inputs"][i]["currentResolution"]
            currentMediaSize = getSizeTxt(mediaWidth, resolution, isMetricInInches)

            if currentMediaType != "custom" :
                currentMediaName = LocalizationHelper.get_string_translation(net, "cMediaTypeIdPlain", 'en-US')
                isCustom = False

            if isRoll1 :
                if isCustom:
                    paper_selection_text = "Roll 1 (" + currentMediaSize + ")"
                else:
                    paper_selection_text = "Roll 1 (" + currentMediaName + " , " + currentMediaSize + ")"
                assert popupRoll1 == paper_selection_text 
                isRoll1 = False
            else:
                if isCustom:
                    paper_selection_text = "Roll 2 (" + currentMediaName + ")"
                    
                else:
                    paper_selection_text = "Roll 2 (" + currentMediaName + " , " + currentMediaSize + ")"
                assert popupRoll2 == paper_selection_text


      
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. Open copy app and copy with default values N copies of one job
        It is only Touch screen because for selene we have no home button or common command with  designjet to go back to the home
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_copy_with_default_values_n_copies_of_one_job
    +test:
        +title:test_copy_ui_enter_app_and_copy_with_default_values_n_copies_of_one_job
        +guid: e3984c9c-5c01-11eb-8ac5-9bae3908aaad
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_copy_with_default_values_n_copies_of_one_job(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    copy_instance = Copy(cdm, udw) 

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Change number of copies
    number_of_copies = spice.wait_for(spice.copy_app.locators.number_of_copies)
    number_of_copies["value"] = N_COPIES
    
    # Start Copy
    spice.copy_app.start_copy()
    
    # Checks that number of copies has not been modified by any settings update since it�s set by testcase
    # to N_COPIES, it was a bug 1/2022 ncopies were decreased to 1 when settings update were received
    value = spice.wait_for(spice.copy_app.locators.number_of_copies )["value"]
    Control.compare_integers(value, N_COPIES)

    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy
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
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. It unloads media, enters the app 
              and loads media again to test it is automatically detected and the scan started.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-38134
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_load_media
    +test:
        +title:test_copy_ui_enter_app_and_load_media
        +guid: de37fe60-cf4b-11eb-ae7d-cb41b790189f
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_load_media(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    copy_instance = Copy(cdm, udw) 

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    
    # Ensure media is unloaded before going to App screen.
    Control.validate_result(scan_action.unload_media("MDF"))
    
    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)
    
    spice.copy_ui().wait_main_button_to_start_copy(cdm, is_constrained = True)

    # Load media, scan should auto-start.
    # Ensure media is present
    Control.validate_result(scan_action.load_media("MDF"))
    
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    spice.copy_ui().wait_main_button_to_finish_copy(cdm)

    # Finish Copy
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
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks the behaviour of scan start button when loading/unloading media.
              It loads media, enters the app, unloads media and loads again
              to test that button is shown properly.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-38134
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_unload_media
    +test:
        +title:test_copy_ui_enter_app_and_unload_media
        +guid: 66196588-cf58-11eb-a816-db4de2ba1b14
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_unload_media(spice, cdm, udw, tcl, copy, ews, setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw).set_cdm(cdm)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check button status. 
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.copy_button)
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.copy_button)
    
    spice.copy_ui().wait_main_button_to_start_copy(cdm)

    # Ensure media is unloaded.
    Control.validate_result(scan_action.unload_media("MDF"))
    
    # Check when media is unloaded: text of main button remains Start 
    spice.copy_ui().wait_main_button_to_start_copy(cdm, is_constrained = True)
      
    # Back To Home to set initial state agains
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks the behaviour when loading/unloading media. 
              It loads media, enters the app, unloads media and loads again 
              to test that the job is completed properly.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-22046
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_unload_then_load_media
    +test:
        +title:test_copy_ui_enter_app_and_unload_then_load_media
        +guid: 78074974-cf60-11eb-a82a-7b006ee4e6bc
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_unload_then_load_media(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    copy_instance = Copy(cdm, udw) 

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))
    
    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)
    
    spice.copy_ui().wait_main_button_to_start_copy(cdm)

    # Unload then load the media.
    # Ensure media is unloaded
    Control.validate_result(scan_action.unload_media("MDF"))
    
    # Check when media is unloaded: text of main button remains as Start
    spice.copy_ui().wait_main_button_to_start_copy(cdm, is_constrained = True)

    # Ensure media is present
    Control.validate_result(scan_action.load_media("MDF"))
    
    # Media load starts the copy.
  
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)
    
    # Finish Copy
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
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks the eject button behaviour.
              Enters copyApp and checks its visibility without
              loaded media in output.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-37946
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_check_eject_button_notloaded_notreleasable
    +test:
        +title:test_copy_ui_enter_app_and_check_eject_button_notloaded_notreleasable
        +guid: 1fd8519a-db03-11eb-8eae-d3073d860e66
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_eject_button_notloaded_notreleasable(spice, cdm, udw, tcl, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is unloaded before going to App screen.
    Control.validate_result(scan_action.unload_media("MDF"))
    
    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check eject button is not present. NLI_NLO state. 
    spice.copy_app.wait_locator_not_visible(spice.copy_app.locators.eject_button)

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks the eject button behaviour.
              Enters copyApp and checks its visibility with
              loaded media on output.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-37946
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_check_eject_button_loaded_releasable
    +test:
        +title:test_copy_ui_enter_app_and_check_eject_button_loaded_releasable
        +guid: 5961ef56-db13-11eb-950d-fbd67608a0ad
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_eject_button_loaded_releasable(spice, cdm, udw, tcl, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is loaded before going to App screen.
    Control.validate_result(scan_action.load_media("MDF"))
    
    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check eject button is present. LI_NLO state.
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.eject_button)
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.eject_button)

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks the eject button behaviour.
              Enters copyApp and checks its visibility with
              loaded media on output.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-37946
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_check_eject_button_notloaded_releasable
    +test:
        +title:test_copy_ui_enter_app_and_check_eject_button_notloaded_releasable
        +guid: 68dd9f24-dd8a-11eb-b87f-8f8477c37d09
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_eject_button_notloaded_releasable(spice, cdm, udw, tcl, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is unloaded and releasable before going to App screen.
    Control.validate_result(scan_action.unloaded_and_releasable_media("MDF"))
    
    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check eject button is present. NLI_LO state.
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.eject_button)
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.eject_button)

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test checks the eject button behaviour.
              Checks its visibility/enabling while scanning.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-37946
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_check_eject_button_while_scanning
    +test:
        +title:test_copy_ui_enter_app_and_check_eject_button_while_scanning
        +guid: 6e6abc50-db0b-11eb-a0d8-cfe9bb8c31ff
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_eject_button_while_scanning(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    copy_instance = Copy(cdm, udw) 

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check eject button is present.
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.eject_button)
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.eject_button)

    # Start Copy
    spice.copy_app.start_copy()

    # Check eject button is not present.
    spice.copy_app.wait_locator_not_visible(spice.copy_app.locators.eject_button)

    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy
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
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Open copy app, copy n times and check eject button.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-37946
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_copy_and_check_eject_button_when_batch_copying
    +test:
        +title:test_copy_ui_enter_app_and_copy_and_check_eject_button_when_batch_copying
        +guid: a2836772-df0b-11eb-af0f-67b2fe56957f
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_copy_and_check_eject_button_when_batch_copying(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw)
    simulation = scan_action.set_scan_random_acquisition_mode(210, 297)
    Control.validate_simulation(simulation)
    copy_instance = Copy(cdm, udw) 
    

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))
    
    # Get Job ID
    last_job_id = job.get_last_job_id()
    
    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # wait for copy landing view
    spice.copy_ui().wait_for_copy_landing_view()

    for i in range(N_COPIES):
        logging.info( "Iteration number " + str( i ) )
        
        # Load media to trigger the next scan except on the first,
        # because media was already loaded when entering the app
        # and batch-scanning should start automatically.
        if i > 0:
            # Ensure media is present
            Control.validate_result(scan_action.load_media("MDF"))
        else:
            # Start Copy
            spice.copy_app.start_copy()
        
        # Check eject button is not present.
        spice.copy_app.wait_locator_not_visible(spice.copy_app.locators.eject_button)

        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)
        
        # Check eject button is present.
        spice.copy_app.wait_locator_visible(spice.copy_app.locators.eject_button)
        spice.copy_app.wait_locator_enabled(spice.copy_app.locators.eject_button)

        # Eject media.
        spice.copy_app.goto(spice.copy_app.locators.eject_button)

        # Check eject button is not present.
        spice.copy_app.wait_locator_not_visible(spice.copy_app.locators.eject_button)

    # Finish Copy
    spice.copy_app.finish_copy()
    
    # # Wait for the new job completion and Get Job ID
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
    spice.validate_app(home, False)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: +purpose: This test checks the eject button behaviour when it is pressed and media is loaded.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-37946
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_check_eject_button_when_loaded
    +test:
        +title:test_copy_ui_enter_app_and_check_eject_button_when_loaded
        +guid: 70fef3b4-de4e-11eb-a668-13d24c7326b6
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_check_eject_button_when_loaded(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions Send class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    # Go to Copy App.
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check eject button is present.
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.eject_button)
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.eject_button)

    # Eject media.
    spice.copy_app.goto(spice.copy_app.locators.eject_button)

    # Check eject button is not present.
    spice.copy_app.wait_locator_not_visible(spice.copy_app.locators.eject_button)

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform a copy with multiple pages, and check if copy job contain multiple pages
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-34697
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_multiple_pages_and_check_copy_job_contain_multiple_pages
    +test:
        +title:test_copy_multiple_pages_and_check_copy_job_contain_multiple_pages
        +guid: 45578cdc-778f-11ec-8e02-f7810f546656
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_multiple_pages_and_check_copy_job_contain_multiple_pages(spice, cdm, udw, tcl, job, copy, setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_instance = Copy(cdm, udw) 

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp 
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy 
    spice.copy_app.start_copy()

    # Wait for the page to be scanned and insert 2 more pages.
    for page in range(2):

        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

        # Load new media
        Control.validate_result(scan_action.load_media("MDF"))

    # Wait for the last page to complete
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy
    spice.copy_app.finish_copy()

    # Wait for the new job completion and Get Job ID 
    job_id = job.print_completed_job(last_job_id)

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    logging.info( "status_job " + str( status_job ) )

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check if settings are disabled while a job is active.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-34697
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_settings_are_disabled_while_job_is_active
    +test:
        +title:test_copy_settings_are_disabled_while_job_is_active
        +guid: cb7af12a-7792-11ec-ba6a-ab55311181a4
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_settings_are_disabled_while_job_is_active(spice, cdm, udw, tcl, job, copy, setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_instance = Copy(cdm, udw) 

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start copy
    spice.copy_app.start_copy()

    # Wait setting view is not enabled
    spice.copy_app.wait_locator_disabled(spice.copy_app.locators.options_detail_panel_button)

    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)
    
    # Finish Copy
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
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check that the setting view loads and closes correctly
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-33179
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_enter_copy_ui_app_open_setting_and_close
    +test:
        +title:test_enter_copy_ui_app_open_setting_and_close
        +guid: 2bf4cc80-5c34-11ec-b013-7b3ba69e2b6c
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_enter_copy_ui_app_open_setting_and_close(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Open setting
    spice.copy_app.wait_and_click_setting_view()

    # Validate setting view
    setting_view = spice.copy_app.get_setting_view()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.copy_settings_view)
    spice.validate_app(setting_view, False)

    # Close setting
    spice.copy_app.close_setting_view()

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Complete check simulated from ui to copy job. It is only Dial for selene we have no home button
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-22046
    +timeout:500
    +asset:LFP
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_scan_a_job_dial
    +test:
        +title:test_copy_ui_enter_app_and_scan_a_job_dial
        +guid: de660dff-8db0-46b5-b261-68681670569c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=Dial
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


# Test name
def test_copy_ui_enter_app_and_scan_a_job_dial(spice, net, configuration):
    spice.copy_ui().goto_copy()
    spice.copy_ui().ui_select_copy_page()
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message="Copying", timeout=60)
    spice.copy_ui().goto_menu_mainMenu()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Create Copy system test for one copy job with n pages
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-80832
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_one_copy_job_with_n_pages_ui
    +test:
        +title:test_one_copy_job_with_n_pages_ui
        +guid: 19f594ba-cd22-11ec-9cf2-97613ad900b5
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Test name
def test_one_copy_job_with_n_pages_ui(spice,udw,net,job,cdm,tcl,setup_teardown_print_device):

    last_job_id = job.get_last_job_id()
    cp_ui = spice.copy_ui()
    
    copy_instance = Copy(cdm, udw) 

    spice.cleanSystemEventAndWaitHomeScreen()
    # Ensure HomeScreen
    cp_ui.goto_menu_mainMenu()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app) 

    # Prepare underwear actions 
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw)
    simulation = scan_action.set_scan_random_acquisition_mode(210, 297)
    Control.validate_simulation(simulation)

    # Ensure media is loaded
    Control.validate_result(scan_action.load_media("MDF"))
    
    # Go to Copy App.
    # We dont need to scroll right to click Copy app on Jupiter 
    cp_ui.goto_copy_from_copyapp_at_home_screen()
    spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.view_copyScreen)

    # Check Start Copy button
    spice.copy_ui().wait_main_button_to_start_copy(cdm)

    # Start Copy
    spice.copy_app.start_copy()
    # Get Job ID
    previous_job_id = job.get_last_job_id()
    job_id = Job.find_job_manager_job_id(udw, previous_job_id, 30)

    # Repeat the process for N_COPIES
    for i in range(N_COPIES):
        if i>0:
            Control.validate_result(scan_action.load_media("MDF"))
        # Wait for all previews
        Control.validate_result(job.wait_all_previews_done( job_id, 40 ))

        # Wait for scan to finish and eject button appears
        spice.copy_app.wait_locator_visible(CopyAppWorkflowObjectIds.eject_button)
        spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.eject_button)

        # Make sure scanning is done
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)
        
        # Check for Copy button to appear too
        spice.copy_ui().wait_main_button_to_finish_copy(cdm)
        spice.copy_app.wait_locator_enabled(spice.copy_app.locators.copy_button)

    # Press Copy button
    cp_ui.press_copy_button(spice)

    # Check if job was completed successfully
    job_id = job.print_completed_job(last_job_id)
    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"
    # Get status job
    status_job = job.get_status_job(job_id)
    logging.info( "last_job_ID " + str( last_job_id ) )
    logging.info( "status_job " + str( status_job ) )
    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Return to main menu
    cp_ui.goto_menu_mainMenu()

    # Left scanner loaded as default
    Control.validate_result(scan_action.load_media("MDF"))

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: We check the appearance of a toast when modifying the setting between pages.
        This toast should only appear once after modifying any setting.
        We will show the toast twice after modifying the settings between several pages.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-98320
    +timeout:500
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_check_toast_for_changing_settings_between_pages
    +test:
        +title:test_copy_ui_check_toast_for_changing_settings_between_pages
        +guid: 5356fd16-4978-11ed-baaf-c34fd896fa69
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_check_toast_for_changing_settings_between_pages(spice, cdm, udw, net, job, configuration):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    copy_instance = Copy(cdm, udw) 

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Start Copy
    logging.info( "Starting copy " )
    spice.copy_app.start_copy()

    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # we check that the toast does not appear without modifying settings
    spice.copy_ui().check_job_toast_or_modal_not_appear(net, configuration, message='SomeSettingsChangedBetweenPages', timeout=3)

    # change a setting to check the appearance of the toast
    spice.copy_ui().ui_copy_set_no_of_pages(3)
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='SomeSettingsChangedBetweenPages', timeout=3)

    # we verify that the toast only appears the first time a setting is modified
    spice.copy_ui().ui_copy_set_no_of_pages(5)
    spice.copy_ui().check_job_toast_or_modal_not_appear(net, configuration, message='SomeSettingsChangedBetweenPages', timeout=3)

    # Load media and make a scan
    Control.validate_result(scan_action.load_media("MDF"))
    
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # change a setting after load media another time to check the toast reappears when modify setting
    spice.copy_ui().ui_copy_set_no_of_pages(2)
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='SomeSettingsChangedBetweenPages', timeout=3)

    # Finish Copy
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
    spice.validate_app(home, False)

# disabled test because objectName not found because the objectNames from cColorLines is Color lines and is not supported because it has a whitespace, jira task created DUNE-106907
"""
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: We enter the copy application and see that the default quicksets is mixed content
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid: DUNE-98608
        +timeout:500
        +asset:LFP
        +delivery_team: LFP
        +feature_team: LFP_ScannerWorkflows
        +test_framework:TUF
        +name:test_copy_ui_check_selected_quickset_by_default_and_values
        +test:
            +title:test_copy_ui_check_selected_quickset_by_default_and_values
            +guid: d7f66798-d8a8-4309-b9c2-68aa68cdc546
            +dut:
                +type:Simulator,Emulator
                +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
#@unittest.skip("objectName not found because the objectNames from cColorLines is Color lines and is not supported because it has a whitespace")
def test_copy_ui_check_selected_quickset_by_default_and_values(setup_teardown_homescreen, spice, udw, net, locale: str = "en"):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Check selected quickset is mixed content
    spice.copy_ui().verify_selected_quickset(CopyAppWorkflowObjectIds.mixed_content_quicksetId)
    
    # Check default values
    time.sleep(2)
    color_mode = spice.wait_for(CopyAppWorkflowObjectIds.color_mode_value)
    assert color_mode["text"] == str(LocalizationHelper.get_string_translation(net, "cColor", locale))
    quality = spice.wait_for(CopyAppWorkflowObjectIds.quality_value)
    assert quality["text"] == "Fast"
    content_type = spice.wait_for(CopyAppWorkflowObjectIds.content_type_value)
    assert content_type["text"] == str(LocalizationHelper.get_string_translation(net, "cMixed", locale))
    paper_source = spice.wait_for(CopyAppWorkflowObjectIds.paper_source_value)
    assert paper_source["text"] == str(LocalizationHelper.get_string_translation(net, "cAutomatic", locale))
    number_of_copies = spice.wait_for(CopyAppWorkflowObjectIds.number_of_copies_value)
    assert number_of_copies["text"] == "1"

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
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
    +name:test_copy_app_increase_num_copies_and_verify_num_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_app_increase_num_copies_and_verify_num_copies
        +guid:d2413fbb-f025-4b78-9c54-7e22d8478c15
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_app_increase_num_copies_and_verify_num_copies(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    cp_ui = spice.copy_ui()

    expected_number_of_incremented_copies = 4

    # HomeScreen
    spice.cleanSystemEventAndWaitHomeScreen()
    
    # Ensure HomeScreen
    cp_ui.goto_menu_mainMenu()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app) 

    # Go to Copy App.
    # We dont need to scroll right to click Copy app on Jupiter 
    cp_ui.goto_copy_from_copyapp_at_home_screen()
    spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.view_copyScreen)

    # Change number of copies
    # increase to 2
    cp_ui.increase_copyApp_num_copies(SINGLE_COPY_COUNT_INCREMENT)

    # increase to 3
    cp_ui.increase_copyApp_num_copies(SINGLE_COPY_COUNT_INCREMENT)

    # increase to 4
    cp_ui.increase_copyApp_num_copies(SINGLE_COPY_COUNT_INCREMENT)

    # validate incremented counts
    cp_ui.goto_copy_options_list()
    assert cp_ui.get_number_of_copies() == expected_number_of_incremented_copies
    
    cp_ui.change_num_copyApp_copies(SINGLE_COPY_COUNT_INCREMENT)

    # Return to main menu
    cp_ui.back_to_landing_view()
    cp_ui.goto_menu_mainMenu()

    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Validate that the spinbox in the Copy App can decrement the copy counts.
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
    +name:test_copy_app_decrease_num_copies_and_verify_num_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_app_decrease_num_copies_and_verify_num_copies
        +guid:23b16e7c-4fa6-493e-9fdb-4f9c92a22187
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_app_decrease_num_copies_and_verify_num_copies(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    cp_ui = spice.copy_ui()

    expected_number_of_incremented_copies = 4
    expected_number_of_decremented_copies = 2

    # HomeScreen
    spice.cleanSystemEventAndWaitHomeScreen()
    
    # Ensure HomeScreen
    cp_ui.goto_menu_mainMenu()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app) 
    
    # Go to Copy App.
    # We dont need to scroll right to click Copy app on Jupiter 
    cp_ui.goto_copy_from_copyapp_at_home_screen()
    spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.view_copyScreen)

    # Change number of copies
    cp_ui.change_num_copyApp_copies(expected_number_of_incremented_copies)
    
    # decrease to 2
    cp_ui.decrease_copyApp_num_copies(expected_number_of_decremented_copies)

    # validate incremented counts
    cp_ui.goto_copy_options_list()
    assert spice.copy_ui().get_number_of_copies() == expected_number_of_decremented_copies

    # reset the copy Count:
    cp_ui.change_num_copyApp_copies(SINGLE_COPY_COUNT_INCREMENT)
    
    # Return to main menu
    cp_ui.back_to_landing_view()
    cp_ui.goto_menu_mainMenu()
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter copy app, start a job and exit as fast as possible. Check the job completes afterwards.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-117360
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_and_scan_a_job_then_exit
    +test:
        +title:test_copy_ui_enter_app_and_scan_a_job_then_exit
        +guid: e11251bc-b810-11ed-8204-d76321e0522f
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_and_scan_a_job_then_exit(spice, udw, job, setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.scan_settings.wait_for_preview_n(1)

    # Then back home cancelling current job
    spice.copy_app.goto_home()
    spice.scan_settings.cancel_current_job_modal_alert(cancel_job=True)
    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)

    # Wait for job to complete.
    Job.wait_for_completed_job(last_job_id, job, udw)

    # We are already at home screen.

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: We check the appearance of a toast when click done button despite having returned to the mainApp.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-145649
    +timeout:500
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_check_toast_for_done_button_is_clicked_and_go_to_mainApp_without_wait
    +test:
        +title:test_copy_ui_check_toast_for_done_button_is_clicked_and_go_to_mainApp_without_wait
        +guid: ee3a6ae6-2642-11ee-8ac3-07229cf8309f
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.skip(reason="Random failing, need deep investigation, low coverage, not really usefull, we'll fix it in future DUNE-193821")
def test_copy_ui_check_toast_for_done_button_is_clicked_and_go_to_mainApp_without_wait(spice, cdm, udw, net, job, configuration):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_instance = Copy(cdm, udw) 

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Ensure media is present before going to App screen
    Control.validate_result(scan_action.load_media("MDF"))

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Start Copy
    logging.info( "Starting copy " )
    spice.copy_app.start_copy()

    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy (click on button done)
    spice.copy_app.finish_copy()

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Check toast appear
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='preparingToCopy', timeout=15)

    # Wait for the new job completion and Get Job ID
    job_id = job.print_completed_job(last_job_id)

    # Check if the new job has been generated  
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perfrom Copy job of 40 pages
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:800
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_enter_app_perform_60_page_job
    +test:
        +title:test_copy_ui_enter_app_perform_60_page_job
        +guid:1fa5f1fc-e7a5-11ef-a14e-170daab90c82
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_enter_app_perform_60_page_job(spice, cdm, udw, job):
    # Fixtures
    duneJobInterface = Job(cdm, udw)
    jobIds = duneJobInterface.get_recent_job_ids()
    job.bookmark_jobs()
    last_job_id = jobIds[len(jobIds) - 1]
    jobIds.clear()
    job_concurrency_path = job.job_concurrency_supported == "true"

    udw.mainApp.ScanMedia.unloadMedia("MDF")
    spice.copy_ui().goto_copy()
    
    # Check ButtonStart.
    if job_concurrency_path:
        spice.copy_ui().wait_main_button_to_start_copy(cdm, is_constrained = True)
    
    for page_number in range(60):
        if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
            udw.mainApp.ScanMedia.loadMedia("MDF")
            # Copy starts automatically, wait previews are ready
            if job_concurrency_path:
                spice.scan_settings.wait_for_preview_n(page_number + 1)

    # Finish job
    spice.copy_ui().ui_select_copy_page()

    if not job_concurrency_path:
        spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()
    
    # Wait for job to complete.
    Job.wait_for_completed_job(last_job_id, job, udw)

    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    spice.copy_ui().goto_menu_mainMenu()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify all constraint modals that appear in the copy application's UI.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-117599
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_validate_constrained_modals_appears_correctly
    +test:
        +title:test_copy_ui_validate_constrained_modals_appears_correctly
        +guid:e19f827d-e2e7-4813-a9dc-318d562be55c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_constrained_modals_appears_correctly(spice, cdm, udw, net, job, setup_teardown_homescreen):

   # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    copy_app = spice.copy_ui()

    # Ensure that there is unload media.
    Control.validate_result(scan_action.unload_media("MDF"))

    # Go to Copy App.
    copy_app.goto_copy_from_copyapp_at_home_screen()
    spice.copy_app.wait_locator_enabled(CopyAppWorkflowObjectIds.view_copyScreen)

    # Check ButtonStart.
    spice.copy_ui().wait_for_copy_landing_view()
    copy_app.wait_main_button_to_start_copy(cdm, is_constrained=True)

    # Start copy, when we press on button Start, if there is not load media appears the modal Insert Page in the Scanner.
    spice.copy_app.start_copy()

    # Verify constrained mensage
    copy_app.verify_copy_constrained_message(net)

    # Load a page in the Scanner.
    Control.validate_result(scan_action.load_media("MDF"))
    spice.scan_settings.wait_for_preview_n(1)

    # Add another page in the UI press the button + that appears in the UI.
    addbutton = spice.wait_for(CopyAppWorkflowObjectIds.button_add_page)
    addbutton.mouse_click()

    # Validate the modal that appears in the UI when you don't load another media.
    spice.wait_for(CopyAppWorkflowObjectIds.preview_add_page_prompt)

    # Dismiss the modal.
    closeModal = spice.wait_for(CopyAppWorkflowObjectIds.button_ok_button_add_page)
    closeModal.mouse_click()

    # Load a page in the Scanner.
    Control.validate_result(scan_action.load_media("MDF"))
    spice.scan_settings.wait_for_preview_n(2)

    # Finish Copy
    spice.copy_app.finish_copy()
