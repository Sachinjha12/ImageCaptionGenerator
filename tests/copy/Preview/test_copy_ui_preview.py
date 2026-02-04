import logging
import time
import copy
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.copy.copy import Copy
from dunetuf.control.control import Control

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app preview job cancel before send
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134225
    +timeout:500
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_ui_copy_job_open_preview_and_exit_app
    +test:
        +title:test_ui_copy_job_open_preview_and_exit_app
        +guid:7af1dcc6-c872-42a5-a660-5f504643d856
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ui_copy_job_open_preview_and_exit_app(
    spice, udw, tcl, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):

    # The idea here is to do the following:
    # 2. Select Coppy from Home Screen
    # 4. Perform one scan by click on start.
    # 5. Exit to Home Screen 
    # 6. Check job is cancelled

    #configure simulation: random color A4 landscape
    scan_action = ScanAction()
    scan_action.set_tcl(tcl)
    scan_action.set_udw(udw)
    scan_action.set_scan_random_acquisition_mode(210, 297)

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))

    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    #Open Preview Window
    spice.scan_settings.wait_and_click_preview_n(1)
    #Validate preview window is shown
    spice.scan_settings.wait_for_preview_window()

    # Go to Main App Screen
    spice.scan_settings.back_from_preview()
    spice.scan_settings.goto_homescreen_with_ongoing_scan_job()

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is Not Cancelled'


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy preview job finish after send
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-134225
    +timeout:500
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_ui_copy_job_open_preview_and_click_back_button
    +test:
        +title:test_ui_copy_job_open_preview_and_click_back_button
        +guid:bc8c113e-4e73-48fc-95fc-dae8d0bae07c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ui_copy_job_open_preview_and_click_back_button(
    spice, udw, tcl, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # The idea here is to do the following:
    # 1. Pre-requisite: A. Unload media
    # 2. Select Copy from Home Screen to Menu App
    # 4. Perform one scan by loading media.
    # 5. Click on first thumbnail to enter in zoom screen
    # 6. Click back button to return to scan landing view
    # 7. Perform other scan by loading media.
    # 8. Click back button to return to scan landing view
    # 9. Perform other scan by loading media.
    # 10. Click done and wait the job to end
    # 11. Return to homescreen
    SCAN_WAIT_TIMEOUT = 30.0

    #configure simulation: random color A4 landscape
    scan_action = ScanAction()
    scan_action.set_tcl(tcl)
    scan_action.set_udw(udw)
    scan_action.set_scan_random_acquisition_mode(210, 297)

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))

    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    #Open Preview Window
    spice.scan_settings.wait_and_click_preview_n(1)
    #Validate preview window is shown
    spice.scan_settings.wait_for_preview_window()
    # Click back button
    spice.scan_settings.back_from_preview()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Load media
    udw.mainApp.ScanMedia.loadMedia("MDF")
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(2)
    #Open Preview Window
    spice.scan_settings.wait_and_click_preview_n(2)
    #Validate preview window is shown
    spice.scan_settings.wait_for_preview_window()
    # Click back button
    spice.scan_settings.back_from_preview()

    # Validate we are in CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_visible(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Click done button
    spice.copy_ui().done_button_present(spice, SCAN_WAIT_TIMEOUT)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check preview panel for flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-74689
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_with_preview_flatbed_copy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_preview_flatbed_copy
        +guid:985efb98-695e-4358-ab88-6ab5d365d504
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_with_preview_flatbed_copy(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    
    logging.info("Go to Copy > Previewpanel > click on preview > click on copy")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_preview_panel()
    copy_job_app.start_preview()
    copy_job_app.verify_preview()
    copy_job_app.start_copy_from_secondary_panel(familyname = configuration.familyname, adfLoaded = False)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check preview panel for flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-74689
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_flatbed_cancel_preview_then_copy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_flatbed_cancel_preview_then_copy
        +guid:48cdd015-d343-4bf8-95cb-916761f8a0af
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_flatbed_cancel_preview_then_copy(spice, job, cdm, udw, net, configuration):
    try:
        job.bookmark_jobs()

        logging.info("Unload ADF")
        udw.mainApp.ScanMedia.unloadMedia("ADF")

        logging.info("Go to Copy > Previewpanel > click on preview > click on cancel > click on preview > click on copy")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy_from_copyapp_at_home_screen()
        copy_job_app.go_to_preview_and_come_back_homescreen()
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')

        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
        job.clear_joblog()

        copy_job_app.goto_copy_from_copyapp_at_home_screen()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_copy_from_preview_panel(familyname = configuration.familyname, adfLoaded = False)
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='starting')

        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    finally:
        # Load media in ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check preview panel for MDF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-74689
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_MDF_preview_oncopy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_MDF_preview_oncopy
        +guid:8d95ee0e-1bc0-4eac-9448-0d88894127e0
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=ManualFeeder & Copy=ImagePreview
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_MDF_preview_oncopy(
    spice, job, net, configuration, setup_teardown_with_copy_job, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    logging.info("Go to Copy > click on start > wait for preview > click on Done")
    copy_job_app = spice.copy_ui()
    spice.main_app.goto_copy_app()
    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    copy_job_app.start_copy_from_preview_panel()
    #Click on Done
    copy_job_app.start_copy()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check preview panel for MDF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-74689
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_MDF_preview_oncopy_then_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_MDF_preview_oncopy_then_cancel_job
        +guid:9cbe3026-c2d6-4fa7-9fe5-c94eef13131e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=ManualFeeder & Copy=ImagePreview
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_MDF_preview_oncopy_then_cancel_job(
    spice, job, net, configuration, setup_teardown_with_copy_job, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    logging.info("Go to Copy > click on start > wait for preview > click on cancel job")
    copy_job_app = spice.copy_ui()
    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    copy_job_app.start_copy_from_preview_panel()
    job.cancel_active_jobs()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check preview panel not visible for flatbed duplex mode
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-74689
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_flatbed_duplex_preview_button_visible
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_flatbed_duplex_preview_button_visible
        +guid:f9a365ac-76f5-4009-97f6-ccce398f375b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & Copy=2Sided1To2

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_flatbed_duplex_preview_button_visible(scan_emulation, setup_teardown_with_copy_job, spice, job, cdm, udw, net):
    job.bookmark_jobs()
    logging.info("Unload ADF")
    scan_emulation.media.unload_media(media_id='ADF')
    logging.info("Go to Copy > Change Settings-> 1_2 sided -> Go To Preview Panel-> check Preview button visible")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_copy_side("1_2_sided")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Goto Preview Panel")
    copy_job_app.goto_preview_panel()
    logging.info("Preview button should visible")
    copy_job_app.check_preview_button_visible()
    copy_job_app.back_to_homescreen()
    scan_emulation.media.load_media(media_id='ADF')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check preview panel not visible for pages per sheet 2 selected
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-74689
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_flatbed_pagespersheet_2_preview_button_visible
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_flatbed_pagespersheet_2_preview_button_visible
        +guid:3b1e6388-963b-4318-a448-4182cc970e7c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & Copy=2PagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_flatbed_pagespersheet_2_preview_button_visible(scan_emulation, setup_teardown_with_copy_job, spice, job, cdm, udw, net):
    job.bookmark_jobs()
    logging.info("Unload ADF")
    scan_emulation.media.unload_media(media_id='ADF')
    logging.info("Go to Copy > Change Settings-> 1_2 sided -> Go To Preview Panel-> check Preview button visible")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("Select pages per sheet 2")
    copy_job_app.select_pages_per_sheet_option(udw, "2")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Goto Preview Panel")
    copy_job_app.goto_preview_panel()
    logging.info("Preview button should visible")
    copy_job_app.check_preview_button_visible()
    copy_job_app.back_to_homescreen()
    scan_emulation.media.load_media(media_id='ADF')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check refresh preview panel for flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-99349
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_flatbed_refresh_preview_then_copy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_flatbed_refresh_preview_then_copy
        +guid:ebcac08b-62c4-43c6-805a-0a6d07eb2128
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_flatbed_refresh_preview_then_copy(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    
    logging.info("Go to Copy > Previewpanel > click on preview > click on refresh > verify preview > click on copy")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_preview_panel()
    copy_job_app.start_preview()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting')
    copy_job_app.verify_preview()
    time.sleep(10)
    copy_job_app.refresh_preview_from_preview_panel_refresh_button()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting')
    copy_job_app.verify_preview()
    copy_job_app.start_copy_from_secondary_panel(familyname = configuration.familyname, adfLoaded = False)
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check warning icon is shown if user change setting in preview job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-99349
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_preview_wanrning_icon_shown_after_changing_settings
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_preview_wanrning_icon_shown_after_changing_settings
        +guid:1bcaf748-68c8-4754-93a0-ad157cb118ff
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=GrayScale & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_preview_wanrning_icon_shown_after_changing_settings(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    
    logging.info("Go to Copy > Previewpanel > click on preview >Change Settings > click on warning icon > refresh preview > verify preview > click on copy")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_preview_panel()
    copy_job_app.start_preview()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting')
    copy_job_app.verify_preview()
    copy_job_app.goto_main_panel()
    copy_job_app.goto_copy_options_list()
    if cdm.device_feature_cdm.is_color_supported():
        copy_job_app.select_color_mode(option="Grayscale")
    copy_job_app.back_to_landing_view()
    copy_job_app.goto_preview_panel()
    copy_job_app.refresh_preview_from_warning_icon()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting')
    copy_job_app.verify_preview()
    copy_job_app.start_copy_from_secondary_panel(familyname = configuration.familyname, adfLoaded = False)
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net,configuration ,"Complete")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Job in porgress Modal should show if user change, scan source to ADF while preview is in progress
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-117131
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_preview_adf_loaded_warning_modal
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_preview_adf_loaded_warning_modal
        +guid:55e53c40-1645-4d34-b568-b42ea5ec1d48
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & ImagePreview=Refresh & Copy=BindingMargin
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_preview_adf_loaded_warning_modal(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    logging.info("Go to Copy > Previewpanel > click on preview >Load ADF > Verify ADF Wanring Modal > Unload ADF> click on copy")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_preview_panel()
    copy_job_app.start_preview()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Scanning')
    copy_job_app.verify_preview()
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_job_app.verify_adf_loaded_warning_modal_dialog()
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    copy_job_app.verify_preview()
    copy_job_app.start_copy_from_secondary_panel(familyname = configuration.familyname, adfLoaded = False)
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: If Preview job is canceled from EWS or third party, Copy basic job should work
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-117131
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job__preview_cancel_job_from_queue_and_perfom_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job__preview_cancel_job_from_queue_and_perfom_copy_job
        +guid:195d366b-e204-4186-adc6-1d9b9f487d52
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
def test_copy_ui_job__preview_cancel_job_from_queue_and_perfom_copy_job(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration, scan_emulation):
    try:
        job.clear_joblog()
        job.bookmark_jobs()
        logging.info("Unload ADF")
        scan_emulation.media.unload_media(media_id='ADF')
        logging.info("Go to Copy > Previewpanel > click on preview >Cance job from third party > Verify preview is removed > Perform basic copy job")
        spice.goto_homescreen()
        spice.cleanSystemEventAndWaitHomeScreen()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.start_preview()
        copy_job_app.verify_preview()
        time.sleep(5)
        # cancel the job
        job.cancel_active_jobs()
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')
        time.sleep(2)
        job.wait_for_no_active_jobs()
        copy_job_app.check_for_cancel_model()
        copy_job_app.verify_prepreview_screen()
        copy_job_app.goto_main_panel()
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded=False, sided="1_1_sided")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}, {"type": "copy", "status": "success"}])
    finally:
        spice.goto_homescreen()
        scan_emulation.media.load_media(media_id='ADF')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with 1-2 Sided in Preview Image Refresh Warning Icon not Visible
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-125332
    +timeout: 360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_perform_copy_job_with_one_two_sided_in_preview_image_refresh_warning_icon_not_visible
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_perform_copy_job_with_one_two_sided_in_preview_image_refresh_warning_icon_not_visible
        +guid:74110883-9b44-4a76-b275-4c0c539fb4d3
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & ImagePreview=Refresh
        

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_copy_job_with_one_two_sided_in_preview_image_refresh_warning_icon_not_visible(scan_emulation, setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    logging.info("Unload ADF")
    scan_emulation.media.unload_media(media_id='ADF')

    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.change_num_copyApp_copies(90)
        copy_job_app.select_copy_side("1_2_sided")
        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()
        spice.wait_for(CopyAppWorkflowObjectIds.copy_2sided_prompt, timeout = 15.0)

        logging.info("Click Continue button on 2-Sided Copying screen")
        copy_job_app.click_on_copy_duplex_continue_button()
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete',timeout = 500)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"success"}])

        copy_job_app.goto_preview_panel_after_copy_complete()
        copy_job_app.start_preview()
        copy_job_app.verify_preview()
        preview_warnining_icon = spice.query_item("#icon_0")
        assert preview_warnining_icon["visible"] == False
        
        job.cancel_active_jobs()
        job.wait_for_no_active_jobs()
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To Check prepreview panel content in adf
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170940
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_verify_prepreview_screen_adf
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_prepreview_screen_adf
        +guid:b9e03069-fce6-4093-ab4a-47f7b3a1a458
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & ImagePreview=Refresh
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_verify_prepreview_screen_adf(spice, job, cdm, udw, net):
    try:
        job.bookmark_jobs()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.verify_prepreview_screen_string_adf(udw,net)
        copy_job_app.goto_main_panel()
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify preview and copy job should be success.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_preview_and_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_preview_and_copy_job
        +guid:b40d1c77-3c37-4f65-b390-ad58f3577df7
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & ImagePreview=Refresh & FlatbedMediaSize=Letter
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_preview_and_copy_job(spice, job, cdm, udw, net, configuration):

    job.bookmark_jobs()
    job.clear_joblog()
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        logging.info("Set Original size as Letter")
        spice.copy_ui().select_original_size('Letter')
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().goto_preview_panel()
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        #check preivew job
        spice.copy_ui().start_copy_from_preview_panel(configuration.familyname,adfLoaded)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
        #check copy job
        spice.copy_ui().start_copy()
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"success"}])
    finally:
        spice.goto_homescreen()
        # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        
        
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: To validate header in Preview Header
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-179109
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_validate_preview_header
    +test:
        +title:test_copy_ui_validate_preview_header
        +guid:7d974829-a57d-426f-aebf-0698c94f28d0
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Copy= ImagePreview
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_preview_header(
    spice, job, udw, scan_emulation, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):

    job.bookmark_jobs()
    job.clear_joblog()

    spice.copy_ui().goto_copy()
    if "mdf" not in udw.mainApp.ScanMedia.listInputDevices().lower():
        scan_emulation.media.unload_media(media_id='ADF')
        spice.scan_settings.click_expand_button()
        spice.scan_settings.click_preview_button()
    else:
        spice.copy_app.start_copy()
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))

    #Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1)
    #Open Preview Window
    time.sleep(5)
    spice.scan_settings.wait_and_click_preview_n(1)
    #Validate preview window is shown
    time.sleep(5)
    spice.scan_settings.wait_for_preview_window()
    assert spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_header)
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_header_moreOptions)
    spice.scan_settings.back_from_preview()

    spice.goto_homescreen()
    assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
    yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_Cancel_Button.mouse_click()

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to validate header in preview edit template
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-186070
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_validate_edit_preview_header
    +test:
        +title:test_copy_ui_validate_edit_preview_header
        +guid:f73fade6-71d2-4afa-aaca-b68a11def98a
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Copy=ImageEdition
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_edit_preview_header(
    spice, job, udw, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    job.bookmark_jobs()
    job.clear_joblog()
            
    spice.copy_ui().goto_copy()
    if "mdf" not in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        spice.scan_settings.click_expand_button()
        spice.scan_settings.click_preview_button()
    else:
        spice.copy_app.start_copy()
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))

    time.sleep(5)
    spice.scan_settings.click_on_edit_button()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_edit_header)
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_header_moreOptions)
    spice.scan_settings.click_on_edit_done_button()

    spice.goto_homescreen()
    assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
    yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_Cancel_Button.mouse_click()

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to validate header in brightness edit preview
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-186070
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_validate_edit_brightness_preview_header
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_edit_brightness_preview_header
        +guid:4db93bde-d621-4505-ad6c-6f68cbf1ed13
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Copy=ImageEdition
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_edit_brightness_preview_header(
    spice, job, udw, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    job.bookmark_jobs()
    job.clear_joblog()
            
    spice.copy_ui().goto_copy()
    if "mdf" not in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        spice.scan_settings.click_expand_button()
        spice.scan_settings.click_preview_button()
    else:
        spice.copy_app.start_copy()
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
        
    time.sleep(5)
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_edit_header)
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_header_moreOptions)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_done_button()

    spice.goto_homescreen()
    assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
    yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_Cancel_Button.mouse_click()

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: perform copy Job when image preview configuration enabled
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-186110
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_perform_copy_job_when_image_preview_configuration_enabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_perform_copy_job_when_image_preview_configuration_enabled
        +guid:f38afcb0-1f4f-4614-b6a0-57482ad923d4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaAlerts=JamAutoNav
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_copy_job_when_image_preview_configuration_enabled(spice,job,udw, cdm, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.unload_media(media_id='ADF')
    try:
        # enable image preview configuration     
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "enable")
        
        spice.copy_ui().goto_copy()
        spice.copy_ui().validate_string_id_on_main_action_button(cdm, CopyAppWorkflowObjectIds.copy_button_preview_str_id)
        spice.copy_ui().click_on_main_action_button_in_detail_panel()
        spice.copy_ui().validate_preview_in_preview_panel()
        time.sleep(3)
 
        spice.goto_homescreen()
        spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
 
        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
   
    finally:
        # Go to Main App Screen
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: perform copy Job when image preview configuration optional
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-186110
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_perform_copy_job_when_image_preview_configuration_optional
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_perform_copy_job_when_image_preview_configuration_optional
        +guid:135da282-b09f-4e35-9942-370a03b54632
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaAlerts=JamAutoNav
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_copy_job_when_image_preview_configuration_optional(spice,job,udw, cdm, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.unload_media(media_id='ADF')
    try:
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "optional")

        spice.copy_ui().goto_copy()
        spice.copy_ui().validate_string_id_on_main_action_button(cdm, CopyAppWorkflowObjectIds.copy_button_copy_str_id)
        
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        #Wait for generated thumbnail
        spice.scan_settings.wait_for_preview_n(1)

        spice.goto_homescreen()
        spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

    finally:
        # Go to Main App Screen
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: perform copy Job when image preview configuration disabled
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-186110
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_perform_copy_job_when_image_preview_configuration_disabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_perform_copy_job_when_image_preview_configuration_disabled
        +guid:c7a0b59a-9dc3-4a4b-a21a-e819abe5f9b1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaAlerts=JamAutoNav
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_copy_job_when_image_preview_configuration_disabled(spice,job,udw, cdm, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.unload_media(media_id='ADF')   
    try:
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "disable")

        spice.copy_ui().goto_copy()
        spice.copy_ui().validate_string_id_on_main_action_button(cdm, CopyAppWorkflowObjectIds.copy_button_copy_str_id)
        spice.copy_ui().click_on_main_action_button_in_detail_panel()
        time.sleep(3)
 
        spice.goto_homescreen()
        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
   
    finally:
        # Go to Main App Screen
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to validate preview edit job cancel
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-161363 
    +timeout:660
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_validate_edit_cancel_preview
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_edit_cancel_preview
        +guid:9facfebc-e542-4ef2-bb69-38df00cc06a8
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Copy=ImageEdition
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_edit_cancel_preview(
    spice, job, udw, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    job.bookmark_jobs()
    job.clear_joblog()
            
    spice.copy_ui().goto_copy()
    if "mdf" not in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        spice.scan_settings.click_expand_button()
        spice.scan_settings.click_preview_button()
    else:
        spice.copy_app.start_copy()
        spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))

    time.sleep(5)
    spice.scan_settings.click_on_edit_button()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_edit_header)
    spice.wait_for(CopyAppWorkflowObjectIds.copy_preview_header_moreOptions)
    spice.scan_settings.click_on_edit_done_button()

    spice.goto_homescreen()
    assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
    yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_Cancel_Button.mouse_click()
    time.sleep(5)
    job.wait_for_no_active_jobs()
    # Verify job is cancelled
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is not cancelled'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy preview edit brightness done and cancel the job. verify cancel job status.
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-161363 
    +timeout:720
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_edit_done_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_edit_done_cancel
        +guid:187b4a38-b1b5-4454-bd6c-8f2e4c1a3410
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & EngineFirmwareFamily=Maia & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_edit_done_cancel(
    spice, udw, cdm, job, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    spice.main_app.goto_copy_app()

    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Load media
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    #Open Preview Window
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(2)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_done_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)
    job.cancel_active_jobs()
    time.sleep(5)
    job.wait_for_no_active_jobs()
    # Verify job is cancelled
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is not cancelled'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy preview configuration setting
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-186110
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_validate_copy_preview_configuration_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_copy_preview_configuration_setting
        +guid:dd6cdfd3-7f6d-49c7-a3dc-ee7bfe70e442
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaAlerts=JamAutoNav
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_copy_preview_configuration_setting(spice,job,udw, cdm):
    try:
        spice.menu_operations.goto_menu_settings_image_preview(spice)
        spice.copy_ui().check_preview_configuration_selected_option("Make Optional")

    finally:
        # Go to Main App Screen
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy pre preview string for adf when preview is enabled
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-175214
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_enabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_enabled
        +guid: a0a26493-16d4-4c33-b2d0-62b419a8c7d8
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=ImagePreview & ScanMode=Book
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_enabled(spice, scan_emulation, job, udw, net, cdm):
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        scan_emulation.media.load_media(media_id='ADF')

        # Make Preview Enabled 
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "enable")
        
        copy_job_app = spice.copy_ui()
        spice.copy_ui().goto_copy()
        if spice.uisize == "S":
            copy_job_app.goto_preview_panel()
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
            spice.copy_ui().goto_main_panel()
        else:
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
    finally:
        scan_emulation.media.unload_media(media_id='ADF')
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy pre preview string for adf when preview is optional
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-175214
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_optional
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_optional
        +guid: af46184b-b31e-457d-b1ab-7ed868c6025d
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=ImagePreview & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_optional(spice, scan_emulation, job, udw, net, cdm):
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        scan_emulation.media.load_media(media_id='ADF')

        # Make  Preview Optional 
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "optional")
        
        copy_job_app = spice.copy_ui()
        spice.copy_ui().goto_copy()
        if spice.uisize == "S":
            copy_job_app.goto_preview_panel()
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
            spice.copy_ui().goto_main_panel()
        else:
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
    finally:
        scan_emulation.media.unload_media(media_id='ADF')
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy pre preview string for adf when preview is disabled
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-175214
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_disabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_disabled
        +guid: 634150f9-dd8f-4ed5-89d7-3563453620d6
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=ImagePreview & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_prepreview_string_for_adf_when_preview_is_disabled(spice, scan_emulation, job, udw, net, cdm):
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        scan_emulation.media.load_media(media_id='ADF')

        # Make Preview Disabled
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "disable")
        
        copy_job_app = spice.copy_ui()
        spice.copy_ui().goto_copy()
        if spice.uisize == "S":
            copy_job_app.goto_preview_panel()
            spice.copy_ui().verify_prepreview_disabled_screen_string(udw, net)
            spice.copy_ui().goto_main_panel()
        else:
            spice.copy_ui().verify_prepreview_disabled_screen_string(udw, net)
    finally:
        scan_emulation.media.unload_media(media_id='ADF')
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy pre preview string for flatbed when preview is enabled
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-175214
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_enabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_enabled
        +guid: b23d3f98-41f1-4270-b9f0-437ec3145e32
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_enabled(spice, scan_emulation, job, udw, net, cdm):
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        scan_emulation.media.unload_media(media_id='ADF')

        # Make Preview Disabled
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "enable")
        
        copy_job_app = spice.copy_ui()
        spice.copy_ui().goto_copy()
        if spice.uisize == "S":
            copy_job_app.goto_preview_panel()
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
            spice.copy_ui().goto_main_panel()
        else:
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
    finally:
        scan_emulation.media.load_media(media_id='ADF')
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy pre preview string for flatbed when preview is optional
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-175214
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_optional
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_optional
        +guid: a240ae68-22cf-48bd-9759-33cd85313914
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_optional(spice, scan_emulation, job, udw, net, cdm):
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        scan_emulation.media.unload_media(media_id='ADF')

        # Make Preview Disabled
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "optional")
        
        copy_job_app = spice.copy_ui()
        spice.copy_ui().goto_copy()
        if spice.uisize == "S":
            copy_job_app.goto_preview_panel()
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
            spice.copy_ui().goto_main_panel()
        else:
            spice.copy_ui().verify_prepreview_enabled_screen_string(udw, net)
    finally:
        scan_emulation.media.load_media(media_id='ADF')
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy pre preview string for flatbed when preview is disabled
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-175214
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_disabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_disabled
        +guid: 061e46b0-f36f-4e7e-bfda-4c9b90612b87
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=ImagePreview & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_prepreview_string_for_flatbed_when_preview_is_disabled(spice, scan_emulation, job, udw, net, cdm):
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        scan_emulation.media.unload_media(media_id='ADF')

        # Make Preview Disabled
        default_job_ticket = Copy(cdm, udw).configure_copy_image_preview_mode(cdm, "disable")
        
        copy_job_app = spice.copy_ui()
        spice.copy_ui().goto_copy()
        if spice.uisize == "S":
            copy_job_app.goto_preview_panel()
            spice.copy_ui().verify_prepreview_disabled_screen_string(udw, net)
            spice.copy_ui().goto_main_panel()
        else:
            spice.copy_ui().verify_prepreview_disabled_screen_string(udw, net)
    finally:
        scan_emulation.media.load_media(media_id='ADF')
        spice.goto_homescreen()
        Copy(cdm, udw).patch_operation_on_default_copy_job_ticket(cdm, default_job_ticket)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate the Inactivity Timeout Prompt for Copy Preview Job
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-241726
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_start_preview_validate_inactivity_timeout_continue_then_cancel
    +test:
        +title: test_copy_ui_start_preview_validate_inactivity_timeout_continue_then_cancel
        +guid: 7f6a6541-5bd9-4165-96a5-69ee8e5a1a82
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_start_preview_validate_inactivity_timeout_continue_then_cancel(setup_teardown_with_copy_job, spice, job, udw):
    default_inactivity_timeout = udw.mainUiApp.ApplicationEngine.getInactivityTimerinSeconds()
    try:
        job.bookmark_jobs()
        job.clear_joblog()

        # Set the Inactivity Timer to 10 seconds
        udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(10)

        spice.goto_homescreen()
        spice.copy_ui().goto_copy()
        spice.copy_ui().wait_for_copy_landingview_to_load()
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().wait_for_preview_panel_to_load()
        spice.copy_ui().verify_preview()
        # Validate Inactivity Timeout Prompt and click on continue button
        spice.copy_ui().click_on_inactivity_timeout_prompt_continue_button()
        spice.copy_ui().wait_for_preview_panel_to_load()
        # Validate Inactivity Timeout Prompt and click on cancel button
        spice.copy_ui().click_on_inactivity_timeout_prompt_cancel_button()

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
    finally:
        # Reset the Inactivity Timer to 30 seconds
        udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(default_inactivity_timeout)
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify scan stop button appear while every scanning
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-240990 
    +timeout:720
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_verify_stop_scan_button_appear_while_every_scanning
    +test:
        +title:test_copy_ui_verify_stop_scan_button_appear_while_every_scanning
        +guid:cc535826-814a-42d9-b909-d8775c8e66cf
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & EngineFirmwareFamily=Maia & Copy=ImageEdition & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_stop_scan_button_appear_while_every_scanning(
    spice, udw, cdm, job, tcl, configuration, net, setup_teardown_homescreen, setup_teardown_with_copy_job):

    # HomeScreen
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw).set_configuration(configuration)
    simulation = scan_action.set_scan_random_acquisition_mode(1000, 1000)
    Control.validate_simulation(simulation)
    udw.mainApp.ScanMedia.loadMedia("MDF")
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    spice.copy_ui().goto_copy()
    # CopyApp
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)
    spice.copy_app.start_copy()
    for n in range(1, 4):
        spice.scan_settings.wait_for_preview_n(n, timeout=100)
        udw.mainApp.ScanMedia.loadMedia("MDF")
        stop_button = spice.wait_for(CopyAppWorkflowObjectIds.stop_scan_button, 200)
        spice.wait_until(lambda: stop_button["visible"] == True, timeout=200)

    spice.goto_homescreen()
    assert spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)
    yes_Cancel_Button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_Cancel_Button.mouse_click()
    time.sleep(5)
    job.wait_for_no_active_jobs()
    # Verify job is cancelled
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is not cancelled'
