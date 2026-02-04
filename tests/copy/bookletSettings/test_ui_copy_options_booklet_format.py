import logging
import time
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for booklet format on adf
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_booklet_format_on_adf
    +test:
        +title:test_copy_ui_booklet_format_on_adf
        +guid:e1cf22a8-6182-43c5-8fc4-ad7e1bab9681
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_format_on_adf(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)

        logging.info("Go to Copy > Options, set booklet format on")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_booklet_option('bookletFormat')

        logging.info("Back to copy landing view.")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex",
            image_border='noBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for booklet format on and borders on each page on adf
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_booklet_borders_on_each_page_adf
    +test:
        +title:test_copy_ui_booklet_borders_on_each_page_adf
        +guid:9439f9d9-d588-4ca9-9560-613ee9f15474
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=BookletFormat & CopyBooklet=BookletBordersOnEachPage

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_borders_on_each_page_adf(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)

        logging.info("Go to Copy > Options, set booklet format on")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_booklet_option('bookletFormat')
        time.sleep(10)
        copy_job_app.select_booklet_option('bordersOnEachPage')

        logging.info("Back to copy landing view.")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex",
            image_border='defaultLineBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for booklet format on flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_booklet_format_on_flatbed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_booklet_format_on_flatbed
        +guid:bcd20ddf-f5d2-417c-b275-6b3eb2107ebe
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_format_on_flatbed(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 4)

        logging.info("Go to Copy > Options, set booklet format on")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_booklet_option('bookletFormat')
        copy_job_app.select_scan_mode_option("standard")

        logging.info("Back to copy landing view.")
        copy_job_app.back_to_landing_view()
        
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        logging.info("Start a copy job")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded, pages_per_sheet ="2")

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='flatbed',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex",
            image_border='noBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for booklet format on and borders on each page on flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_booklet_borders_on_each_page_flatbed
    +test:
        +title:test_copy_ui_booklet_borders_on_each_page_flatbed
        +guid:1ba64381-8027-422c-aae9-13ef3f41d568
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=BookletFormat & CopyBooklet=BookletBordersOnEachPage

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_borders_on_each_page_flatbed(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 4)

        logging.info("Go to Copy > Options, set booklet format on")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_booklet_option('bookletFormat')
        time.sleep(5)
        copy_job_app.select_booklet_option('bordersOnEachPage')

        logging.info("Back to copy landing view.")
        copy_job_app.back_to_landing_view()

        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        logging.info("Start a copy job")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded, pages_per_sheet ="2")

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='flatbed',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex",
            image_border='defaultLineBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        
    finally:
        spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for booklet format miscellaneous options
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:360
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_booklet_format_miscellaneous_options
    +test:
        +title:test_copy_ui_booklet_format_miscellaneous_options
        +guid:745f6c9d-6421-4822-9617-d418797532b5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=GrayScale & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_format_miscellaneous_options(scan_emulation, job, spice, udw, cdm, net, configuration):

    job.bookmark_jobs()
    logging.info("Load 20 pages in ADF")
    scan_emulation.media.load_media('ADF', 20)
    copy_app = spice.copy_ui()
    try:
        logging.info("Go to copy screen -> copy options")
        copy_app.goto_copy()
        copy_app.goto_copy_options_list()

        logging.info("set the color to grayscale")
        copy_app.select_color_mode("Grayscale")

        logging.info("Set Content type as Photograph.")
        copy_app.select_content_type("Photograph")

        logging.info("Set lighter darker to max(9).")
        copy_app.select_scan_settings_lighter_darker(9)

        logging.info("Set booklet format on and borders on each page on.")
        copy_app.select_booklet_option('bookletFormat')
        time.sleep(5)
        copy_app.select_booklet_option('bordersOnEachPage')

        logging.info("Back to copy landing view.")
        copy_app.back_to_landing_view()

        copy_app.start_copy()

        Copy(cdm, udw).validate_settings_used_in_copy(
            color_mode="grayscale", 
            content_type='photo', 
            lighter_darker=9, 
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex",
            image_border='defaultLineBorder')
        
        logging.info("Check the copy job complete successfully")
        copy_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
        logging.info("check the job state from cdm")
        job.check_job_log_by_status_and_type_cdm([{"type":"copy","status":"success"}])

    finally:
        logging.info("Load ADF")
        scan_emulation.media.load_media('ADF', 1)
        spice.goto_homescreen()