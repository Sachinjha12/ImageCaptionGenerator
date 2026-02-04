import logging
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up flatbed
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
    +name:test_copy_ui_2up_flatbed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_flatbed
        +guid:cab28dc5-1b7a-416a-a2b2-21beac99b502
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2PagesPerSheet & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_flatbed(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    
    logging.info("Go to Copy > Options, set Pages per sheet to 2")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()
    adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded, pages_per_sheet ="2")


    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up adf multipage and copies
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
    +name:test_copy_ui_2up_adf_multipage_and_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_adf_multipage_and_copies
        +guid:4d21661a-677c-412b-b05c-7f691cc937cc
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_adf_multipage_and_copies(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):

    job.bookmark_jobs()

    logging.info("Load 3 pages on ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    udw.mainApp.ScanDeviceService.setNumScanPages(3)

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set number of copies as 3")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.ui_copy_set_no_of_pages(3)

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy()

    logging.info("Validate copy settings for current job")
    Copy(cdm, udw).validate_settings_used_in_copy(number_of_copies=3, pages_per_sheet='twoUp', media_source='adf')

    logging.info("Check the copy job complete successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanDeviceService.setNumScanPages(1)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up 2-2sided flatbed manual duplex continue
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
    +name:test_copy_ui_2up_2_2sided_flatbed_manual_duplex_continue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_2_2sided_flatbed_manual_duplex_continue
        +guid:26e10b36-918d-4532-b0d8-d77c0eb44149
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2PagesPerSheet & Copy=2Sided2To2 & DeviceFunction=Quickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_2_2sided_flatbed_manual_duplex_continue(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 2-2 Sided")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.select_copy_side(side_mode='2_2_sided')

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_2_sided", pages_per_sheet="2")

    logging.info("Check the copy job complete successfully")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up 2-2sided flatbed manual duplex cancel
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
    +name:test_copy_ui_2up_2_2sided_flatbed_manual_duplex_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_2_2sided_flatbed_manual_duplex_cancel
        +guid:0cb9d5b3-2c97-4a6c-94e7-35fe232ea1e9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To2 & Copy=2PagesPerSheet & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_2_2sided_flatbed_manual_duplex_cancel(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration, scan_emulation):
    # job.clear_all_jobs()
    job.bookmark_jobs()

    logging.info("Unload ADF")
    # udw.mainApp.ScanMedia.unloadMedia("ADF")
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('Flatbed',1)

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 2-2 Sided")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.select_copy_side(side_mode='2_2_sided')

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname=configuration.familyname)

    logging.info("Validate copy settings for current job")
    Copy(cdm, udw).validate_settings_used_in_copy(sides='twoSidedLongEdge', pages_per_sheet='twoUp', media_source='flatbed')
    
    spice.copy_ui().cancel_copy_2sided_operation(familyname=configuration.familyname)
    logging.info("Check the copy job cancelled successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')
    job.wait_for_no_active_jobs()
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
    scan_emulation.media.load_media('ADF',1)
    # udw.mainApp.ScanMedia.loadMedia("ADF")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up 2-1sided flatbed manual_duplex continue
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_2up_2_1sided_flatbed_manual_duplex_continue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_2_1sided_flatbed_manual_duplex_continue
        +guid:cea6bb70-6009-4f29-9b56-05148bafccf8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & Copy=2PagesPerSheet & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_2_1sided_flatbed_manual_duplex_continue(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 2-1 Sided")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.select_copy_side(side_mode='2_1_sided')

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_1_sided", pages_per_sheet="2")
    
    logging.info("Check the copy job complete successfully")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up 1-2sided flatbed manual duplex continue
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
    +name:test_copy_ui_2up_1_2sided_flatbed_manual_duplex_continue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_1_2sided_flatbed_manual_duplex_continue
        +guid:2873cb78-d4cf-446a-a029-c282a1bf3638
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2PagesPerSheet & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_1_2sided_flatbed_manual_duplex_continue(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 1-2 Sided")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.select_copy_side(side_mode='1_2_sided')

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname=configuration.familyname, adfLoaded=False, sided="1_2_sided", pages_per_sheet="2")

    logging.info("Check the copy job complete successfully")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 1up 2-2sided outputscale 400 multipage adf
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_1up_2_2sided_outputscale_400_multipage_adf
    +test:
        +title:test_copy_ui_1up_2_2sided_outputscale_400_multipage_adf
        +guid:d250b6d3-5d47-4445-ae6d-a201a7af1897
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided2To2
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1up_2_2sided_outputscale_400_multipage_adf(setup_teardown_with_copy_job, job, spice, udw, cdm, net, configuration,scan_emulation):
    job.bookmark_jobs()

    logging.info("Load 3 pages in ADF ")
    is_adf_duplex_supported = spice.copy_ui().check_duplex_support(cdm)
    if is_adf_duplex_supported == False:
     spice.copy_ui().enable_duplex_supported(cdm, udw)
    scan_emulation.media.load_media('ADF',3)

    copy_app = spice.copy_ui()

    copy_app.goto_copy()

    copy_app.goto_copy_options_list()
    #outputscale cannot be custom when pages is 2up
    logging.info("Set Pages per sheet as 1.")
    copy_app.select_pages_per_sheet_option(udw, "1")

    logging.info("Set sides as 2-2 sided")
    copy_app.select_copy_side("2_2_sided")

    logging.info("Set Flip Up as ON")
    copy_app.set_copy_2sided_flip_up_options("on")

    logging.info("Set Output scale as Custom 400%")
    copy_app.goto_copy_option_output_scale()
    copy_app.goto_copy_output_scale_custom_menu()
    copy_app.set_copy_custom_value_option(input_value=400)
    copy_app.back_to_copy_options_list_view("Back_to_options_list")

    logging.info("Back to copy landing view.")
    copy_app.back_to_landing_view()

    copy_app.start_copy()

    scaleToFitEnabled = 'false'
    if configuration.familyname == 'enterprise':
        scaleToFitEnabled = 'true'

    # Note: According to DUNE-73524, scaling option is disallowed when 2PagesPerSheet is on.
    Copy(cdm, udw).validate_settings_used_in_copy(
        pages_per_sheet="oneUp",
        output_scale_setting={'scaleToFitEnabled': scaleToFitEnabled, 'xScalePercent': 400, 'yScalePercent': 400, 'scaleSelection': 'custom'},
        sides = "twoSidedShortEdge",
        media_source="adf",
        )
    logging.info("Check the copy job complete successfully")
    copy_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete', timeout=90)
    
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up originalsize legal adf
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
    +name:test_copy_ui_2up_originalsize_legal_adf
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_originalsize_legal_adf
        +guid:1cb6d098-b48e-4155-8047-3f0ddcdc9e36
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & ADFMediaSize=Legal
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_originalsize_legal_adf(setup_teardown_with_copy_job, tray, media, job, spice, udw, cdm, net, configuration):
    try:
        job.bookmark_jobs()

        default_tray = tray.get_default_source()
        if tray.is_size_supported('na_legal_8.5x14in', default_tray):
            tray.configure_tray(default_tray, 'na_legal_8.5x14in', 'stationery')

        # Clear all alerts/prompts in homescreen
        if configuration.familyname == 'enterprise':
            spice.cleanSystemEventAndWaitHomeScreen()

        logging.info("Load 2 pages in ADF ")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainApp.ScanDeviceService.setNumScanPages(2)

        copy_app = spice.copy_ui()

        spice.goto_homescreen()
        copy_app.goto_copy_from_copyapp_at_home_screen()
        copy_app.goto_copy_options_list()

        logging.info("Set original size as Legal")
        copy_app.select_original_size("Legal")

        logging.info("Set Pages per sheet as 2.")
        copy_app.select_pages_per_sheet_option(udw, "2")

        logging.info("Back to copy landing view.")
        copy_app.back_to_landing_view()

        copy_app.start_copy()

        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="na_legal_8.5x14in",
            pages_per_sheet="twoUp",
            media_source="adf",
        )
        logging.info("Check the copy job complete successfully")
        copy_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')

        logging.info("check the job state from cdm")
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        tray.reset_trays()
        udw.mainApp.ScanDeviceService.setNumScanPages(1)
        # Make sure to go back to HomeScreen
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up miscellaneous options
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:360
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_2up_miscellaneous_options
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_miscellaneous_options
        +guid:451d2c99-286e-48bb-b5c0-73380ebe8384
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_miscellaneous_options(setup_teardown_with_copy_job, job, spice, udw, cdm, net, configuration):

    job.bookmark_jobs()

    logging.info("Load 3 pages in ADF ")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    udw.mainApp.ScanDeviceService.setNumScanPages(3)

    copy_app = spice.copy_ui()

    logging.info("Go to copy screen -> copy options")
    copy_app.goto_copy()
    copy_app.goto_copy_options_list()
    if cdm.device_feature_cdm.is_color_supported():
        logging.info("set the color to grayscale")
        copy_app.select_color_mode("Grayscale")
        
    logging.info("Set Pages per sheet as 2.")
    copy_app.select_pages_per_sheet_option(udw, option='2')

    logging.info("Set Content type as Photograph.")
    copy_app.select_content_type("Photograph")

    logging.info("Set lighter darker to max(9).")
    copy_app.select_scan_settings_lighter_darker(9)

    logging.info("Back to copy landing view.")
    copy_app.back_to_landing_view()

    copy_app.start_copy()
    if cdm.device_feature_cdm.is_color_supported():

        Copy(cdm, udw).validate_settings_used_in_copy(
            color_mode="grayscale", 
            content_type='photo', 
            lighter_darker=9, 
            media_source='adf'
        )
    else:
            Copy(cdm, udw).validate_settings_used_in_copy(
            content_type='photo', 
            lighter_darker=9, 
            media_source='adf'
        )

    logging.info("Check the copy job complete successfully")
    copy_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')

    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm([{"type":"copy","status":"success"}])
    udw.mainApp.ScanDeviceService.setNumScanPages(1)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up 2-2sided flip up on flatbed manual duplex continue
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_2up_2_2sided_flipup_on_flatbed_manual_duplex_continue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_2_2sided_flipup_on_flatbed_manual_duplex_continue
        +guid:fc7ce6c2-345f-43dc-ac06-b528b5d56e2e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To2 & Copy=2PagesPerSheet & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_2_2sided_flipup_on_flatbed_manual_duplex_continue(setup_teardown_with_copy_job, job, spice, udw, cdm, net, configuration):
    # Known bug: HMDE-709: Printer crash then reboot automatically when click "Continue" on 2-Sided Copying screen with some combined settings.
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 2-2 Sided, set Flip Up as ON")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.select_copy_side(side_mode='2_2_sided')
    copy_job_app.set_copy_2sided_flip_up_options(two_sided_options="on")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_2_sided", pages_per_sheet="2")

    logging.info("Check the copy job complete successfully")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 1up 2-2sided Flatbed collate off
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-91176
    +timeout:400
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_2up_2_2sided_flatbed_collate_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_2up_2_2sided_flatbed_collate_off
        +guid:8c39e0c0-5c10-48c0-acbe-4e7693cf277f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To2 & Copy=2PagesPerSheet & ImagePreview=Refresh
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_2_2sided_flatbed_collate_off(setup_teardown_with_copy_job, job, spice, udw, cdm, net, configuration):
    job.bookmark_jobs()

    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 2-2 Sided")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')
    copy_job_app.select_copy_side(side_mode='2_2_sided')
    logging.info("Set number of copies as 10, set collate to off")
    copy_job_app.ui_copy_set_no_of_pages(10)
    copy_job_app.change_collate(collate_option="off")
    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start a copy job")
    copy_job_app.start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_2_sided", pages_per_sheet="2")

    logging.info("Check the copy job complete successfully")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing 
    udw.mainApp.ScanMedia.loadMedia("ADF")
