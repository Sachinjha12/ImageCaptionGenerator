import logging
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up right then down flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_4up_right_then_down_adf
    +test:
        +title:test_copy_ui_4up_right_then_down_adf
        +guid:a2681ad7-cb50-4dde-aa3e-4119bb22b257
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=FourRightThenDownPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_right_then_down_adf(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 4 pages in ADF")
        scan_emulation.media.load_media('ADF', 4)

        logging.info("Go to Copy > Options, set Pages per sheet to 4_rightThenDown")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_pages_per_sheet_option(udw, option='4_rightThenDown')

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toRightToBottom",
            image_border='noBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up down then right flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:360
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_4up_down_then_right_adf
    +test:
        +title:test_copy_ui_4up_down_then_right_adf
        +guid:3f0fb9d6-964f-4474-adbd-fb45d624f10f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=FourDownThenRightPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_down_then_right_adf(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 4 pages in ADF")
        scan_emulation.media.load_media('ADF', 4)

        logging.info("Go to Copy > Options, set Pages per sheet to 4_downThenRight")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_pages_per_sheet_option(udw, option='4_downThenRight')

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        logging.info("Start a copy job")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded, pages_per_sheet ="4_downThenRight")

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toBottomToRight",
            image_border='noBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up right then down flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_4up_right_then_down_flatbed
    +test:
        +title:test_copy_ui_4up_right_then_down_flatbed
        +guid:c95ec6f0-3aec-4626-9b1d-8eb1f96a9722
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=FourRightThenDownPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_right_then_down_flatbed(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 4)

        logging.info("Go to Copy > Options, set Pages per sheet to 4_rightThenDown")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_pages_per_sheet_option(udw, option='4_rightThenDown')

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        logging.info("Start a copy job")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded, pages_per_sheet ="4_rightThenDown")

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='flatbed',
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toRightToBottom",
            image_border='noBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        logging.info("Load ADF")
        scan_emulation.media.load_media('ADF')
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up down then right flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_4up_down_then_right_flatbed
    +test:
        +title:test_copy_ui_4up_down_then_right_flatbed
        +guid:0cd354bc-e32e-4324-8f7d-ef20bc2d214f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=FourRightThenDownPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_down_then_right_flatbed(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 4)

        logging.info("Go to Copy > Options, set Pages per sheet to 4_downThenRight")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_pages_per_sheet_option(udw, option='4_downThenRight')

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        logging.info("Start a copy job")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded, pages_per_sheet ="4_downThenRight")

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='flatbed',
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toBottomToRight",
            image_border='noBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        logging.info("Load ADF")
        scan_emulation.media.load_media('ADF')
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up miscellaneous options
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:360
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_4up_miscellaneous_options
    +test:
        +title:test_copy_ui_4up_miscellaneous_options
        +guid:8ba38f40-d480-47c9-af4e-e08328b6ebf9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=FourRightThenDownPagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_miscellaneous_options(scan_emulation, ews,job, spice, udw, cdm, net, configuration):

    job.bookmark_jobs()
    logging.info("Load 4 pages in ADF")
    scan_emulation.media.load_media('ADF', 4)
    copy_app = spice.copy_ui()
    color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
    try:
        logging.info("Go to copy screen -> copy options")
        copy_app.goto_copy()
        copy_app.goto_copy_options_list()
        if color_supported:

            logging.info("set the color to grayscale")
            copy_app.select_color_mode("Grayscale")

        logging.info("Set Pages per sheet as 4_rightThenDown")
        copy_app.select_pages_per_sheet_option(udw, option='4_rightThenDown')

        logging.info("Set Content type as Photograph.")
        copy_app.select_content_type("Photograph")

        logging.info("Set lighter darker to max(9).")
        copy_app.select_scan_settings_lighter_darker(9)

        logging.info("Back to copy landing view.")
        copy_app.back_to_landing_view()

        copy_app.start_copy()
        validate_settings_args = {
        'content_type': 'photo',
        'lighter_darker': 9,
        'media_source': 'adf',
        'pages_per_sheet': 'fourUp',
        'numberUp_presentation_direction': "toRightToBottom",
        'image_border': 'noBorder'
        }

        if color_supported:
            validate_settings_args['color_mode'] = 'grayscale'
        Copy(cdm, udw).validate_settings_used_in_copy(**validate_settings_args)
        
        logging.info("Check the copy job complete successfully")
        copy_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
        logging.info("check the job state from cdm")
        job.check_job_log_by_status_and_type_cdm([{"type":"copy","status":"success"}])

    finally:
        logging.info("Load ADF")
        scan_emulation.media.load_media('ADF', 1)
        spice.goto_homescreen()
