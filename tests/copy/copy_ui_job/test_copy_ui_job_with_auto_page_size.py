import logging
from dunetuf.copy.copy import *
from dunetuf.emulation.print.print_emulation_ids import DuneEnginePlatform

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To check auto page size for scannerInuput flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-77856
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_job_with_auto_page_size_adf_flatbed_on_A4_models
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_auto_page_size_adf_flatbed_on_A4_models
        +guid:4d08cc92-6e48-4702-af55-78e7b7eec7ca
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & PrintEngineFormat=A4 & FlatbedMediaSize=AnySize

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_with_auto_page_size_adf_flatbed_on_A4_models(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    
    logging.info("Go to Copy > moreoptions > original size > select any > go back to landing >click on copy")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_original_size("Any")
    logging.info("Back to copy landing view.")
    copy_job_app.back_to_landing_view()
    copy_job_app.start_copy(familyname = configuration.familyname)
    # DUNE-114562 re-implemented Flatbed prescan in simulator
    Copy(cdm, udw).validate_settings_used_in_copy(original_size="na_letter_8.5x11in")
    job.wait_for_no_active_jobs()
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To check auto page size for scannerInuput flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-77856
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_with_auto_page_size_adf_flatbed_on_A3_models
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_auto_page_size_adf_flatbed_on_A3_models
        +guid:398a9c4e-fda3-4bee-ad11-d70c2bd8e61e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & PrintEngineFormat=A3 & FlatbedMediaSize=AnySize
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
  
def test_copy_ui_job_with_auto_page_size_adf_flatbed_on_A3_models(scan_emulation, print_emulation, setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    scan_emulation.media.unload_media(media_id='ADF')
    if print_emulation.print_engine_platform == DuneEnginePlatform.emulator.name:
        scan_emulation.media.load_mediaM(media_id='Flatbed', media_size='letter', media_orientation='long')
    
    logging.info("Go to Copy > moreoptions > original size > select any > go back to landing >click on copy")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_original_size("Any")
    logging.info("Back to copy landing view.")
    copy_job_app.back_to_landing_view()
    adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded)
    # DUNE-114562 re-implemented Flatbed prescan in simulator
    Copy(cdm, udw).validate_settings_used_in_copy(original_size="na_letter_8.5x11in")
    logging.info("Check the copy job complete successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
    
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    scan_emulation.media.load_media(media_id='ADF')
