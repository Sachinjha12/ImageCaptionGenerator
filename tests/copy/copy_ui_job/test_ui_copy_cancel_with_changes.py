import logging
import pytest
from time import sleep
from typing import ClassVar

from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Smoke test Copy single/multipage with batch scanning step 1
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-6096
    +timeout:600
    +asset:LFP
    +delivery_team:LFP
    +feature_team:ProductQA
    +test_framework:TUF
    +test_classification:System
    +name:test_cancel_scan_with_changes
    +test:
        +title:test_cancel_scan_with_changes
        +guid:585fb507-2dae-4722-a97a-58c1154941b8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
@pytest.mark.skip(reason="This test actualy doesn't work in a qemu DUNE-121030")
def test_cancel_scan_with_changes(spice, udw, job, tcl, net, printjob, configuration,scan_emulation):

    LOW_WAIT_TIMEOUT = 10.0
    WAIT_TIMEOUT = 30.0

    spice.main_app.get_home()
    # Wait for HomeScreen to appear and dismiss SystemError if exists
    spice.cleanSystemEventAndWaitHomeScreen()

    last_job_id = job.get_last_job_id()
    cp_app = spice.copy_ui()

    # Ensure media is unloaded
    unload_plot(udw)

    ##
    ## Step 1
    ##

    # Ensure HomeScreen
    cp_app.goto_menu_mainMenu()
    sleep(3)

    # Go to Copy App.
    cp_app.goto_copy_from_copyapp_at_home_screen()
    sleep(3)
    
    
    cp_app.cancel_copy_job() 

    # Copy button present and press
    cp_app.copy_button_present(spice)
    cp_app.press_copy_button(spice)
    # Wait for and check "Insert page in scanner" msg
    #check_insert_page_msg(spice)
    # Wait for and Click on "ok" button
    cp_app.ok_button_present(spice)
    cp_app.press_ok_button(spice)
    sleep(5)

    # Change some settings
    change_some_settings(spice,cp_app)
    sleep(5)

    # Load plot
    load_plot(udw)

    spice.wait_for("#image_0")
    
    # Cancel Copy
    cp_app.cancel_copy_fast()

    # Press eject button
    cp_app.press_eject_button(spice)

    assert cp_app.is_media_loaded("MDF", udw)

    spice.goto_homescreen()


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Smoke test Copy single/multipage with batch scanning step 2 and 3
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-6096
    +timeout:600
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cancel_with_changes
    +test:
        +title:test_copy_cancel_with_changes
        +guid:b945c4be-68a0-4004-a1cc-425647170ce1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_cancel_with_changes(spice, udw, job, tcl, net, printjob, configuration):
    OW_WAIT_TIMEOUT = 10.0
    WAIT_TIMEOUT = 30.0

    #tcl.execute("ScanImageProvider PUB_setSimulationSizeInMM 1000 841")  

    spice.main_app.get_home()
    # Wait for HomeScreen to appear and dismiss SystemError if exists
    spice.cleanSystemEventAndWaitHomeScreen()

    last_job_id = job.get_last_job_id()
    cp_app = spice.copy_ui()

    # Ensure media is unloaded
    unload_plot(udw)

    ##
    ## Step 2
    ##

    # Go to home screen
    spice.goto_homescreen()

    #tcl.execute("ScanImageProvider PUB_setSimulationSizeInMM 480 841")  

    cp_app = spice.copy_ui()

    cp_app.goto_menu_mainMenu()
    sleep(3)
    # Go to Copy App.
    cp_app.goto_copy_from_copyapp_at_home_screen()
    sleep(3)
    
    # Change some settings
    change_some_settings(spice,cp_app)

    sleep(5)

    load_plot(udw)
    sleep(20)
    spice.wait_for("#image_0")


    plots = 2
    for i in range(plots):
        load_plot(udw)
        sleep(20)
        change_some_settings_without_access(spice,cp_app)
        sleep(5)
        change_some_settings(spice,cp_app)
        sleep(5)
        cp_app.press_eject_button(spice)
        sleep(20)
        assert cp_app.is_media_loaded("MDF", udw)

    cp_app.done_button_present(spice, WAIT_TIMEOUT)
    cp_app.press_done_button(spice)

     # Wait for the job to end
    job_id = job.print_completed_job(last_job_id)
    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    ##
    ## Step 3
    ##

    sleep(5)
    change_some_settings(spice,cp_app)
    sleep(20)
    plots = 2
    for i in range(plots):
        load_plot(udw)        
        sleep(20)
        cp_app.press_eject_button(spice)
        sleep(20)
        assert cp_app.is_media_loaded("MDF", udw)   

    cp_app.done_button_present(spice, WAIT_TIMEOUT)
    cp_app.press_done_button(spice)
    

    cp_app.goto_menu_mainMenu()

    # Wait for the job to end
    job_id = job.print_completed_job(last_job_id)
    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Ensure HomeScreen
    cp_app.goto_menu_mainMenu()
    sleep(10)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Smoke test Copy single/multipage with batch scanning step 4 and 5
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-6096
    +timeout:600
    +asset:LFP
    +delivery_team:LFP
    +feature_team:ProductQA
    +test_framework:TUF
    +test_classification:System
    +name:test_cancel_scan_with_changes_and_scan
    +test:
        +title:test_cancel_scan_with_changes_and_scan
        +guid:bd4c83d3-f890-4d0c-99b9-e10a9d325d00
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
@pytest.mark.skip(reason="This test actualy doesn't work in a qemu DUNE-121030")
def test_cancel_scan_with_changes_and_scan(spice, udw, job, tcl, net, printjob, configuration):
    OW_WAIT_TIMEOUT = 10.0
    WAIT_TIMEOUT = 30.0

    #tcl.execute("ScanImageProvider PUB_setSimulationSizeInMM 1000 841")  

    spice.main_app.get_home()
    # Wait for HomeScreen to appear and dismiss SystemError if exists
    spice.cleanSystemEventAndWaitHomeScreen()

    last_job_id = job.get_last_job_id()
    cp_app = spice.copy_ui()

    # Ensure media is unloaded
    unload_plot(udw)

    ##
    ## Step 4
    ##

    # Go to Copy App.
    cp_app.goto_copy_from_copyapp_at_home_screen()
    sleep(3)

    # Change some settings
    change_some_settings(spice,cp_app)

    # Load plot
    load_plot(udw)

    # Cancel Copy
    cp_app.cancel_copy_job()

    # Press eject button
    cp_app.press_eject_button(spice)

    ##
    ## Step 5
    ##

    sleep(15)
    load_plot(udw)
    sleep(15)
   
    button = spice.wait_for("#_ExpandButton")
    button.mouse_click()
    sleep(5)
    # Change some settings
    change_some_settings(spice,cp_app)

    sleep(1)
    cp_app.eject_button_present(spice, WAIT_TIMEOUT)
    cp_app.done_button_present(spice, WAIT_TIMEOUT)
    cp_app.press_done_button(spice)

    cp_app.goto_menu_mainMenu()

    # Wait for the job to end
    job_id = job.print_completed_job(last_job_id)
    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"
    

def unload_plot(udw):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    Control.validate_result(scan_action.unload_media("MDF"))

def check_insert_page_msg(spice):
    # Check that "Insert page in scanner" message appears
    expected_msg = LocalizationHelper.get_string_translation(net, "cInsertPageInScanner")
    screen_text = spice.copy_ui().get_insert_page_msg(spice)
    # Check expected Msg
    assert screen_text == expected_msg
    
def change_some_settings(spice,cp_app):
   
    cp_app.press_options_detail_panel()
    
    cp_app.select_content_type("Image")
    
    cp_app.set_detailed_options_resolution("300Dpi")
    
    cp_app.set_detailed_original_media("photo")
    
    cp_app.close_options_detail_panel()

def change_some_settings_without_access(spice,cp_app):
   
    cp_app.press_options_detail_panel()
    
    cp_app.change_options_color_mode()
    sleep(2)
    cp_app.press_ok_button(spice)
    
    cp_app.close_options_detail_panel()

def load_plot(udw):
    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    Control.validate_result(scan_action.load_media("MDF"))
