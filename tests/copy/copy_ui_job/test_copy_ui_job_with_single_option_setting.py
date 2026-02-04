import logging
from dunetuf.copy.copy import *

def check_duplex_support(cdm):
    response = cdm.get(cdm.SCANNER_STATUS)
    if(response['adf']['duplexSupported'] == 'false'):
        return False
    return True

def enable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(True)
    result = check_duplex_support(cdm)
    assert result == True
    udw.mainApp.ScanMedia.loadMedia("ADF")

def disable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(False)
    result = check_duplex_support(cdm)
    assert result == False
    udw.mainApp.ScanMedia.loadMedia("ADF")


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with 1 to 2-Sided setting
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_with_sides_document_feeder
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_sides_document_feeder
        +guid:69016e4b-11cf-4ca8-9588-a6dcf7690fe3
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

def test_copy_ui_job_with_sides_document_feeder(setup_teardown_with_copy_job, scan_emulation, job, spice, udw, net, cdm, configuration):
    # Ensure media is present before going to App screen
    logging.info("load the ADF media")
    scan_emulation.media.load_media(media_id='ADF')
    is_adf_duplex_supported = check_duplex_support(cdm)
    if is_adf_duplex_supported == False:
        enable_duplex_supported(cdm, udw)
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    logging.info("go to sides -> 1 to 2-Sided")
    copy_job_app.goto_sides_option()
    logging.info("check the string on sides and click on side option")
    copy_job_app.check_copy_options_sides_and_select_side(net, "1_2_sided")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        sides="twoSidedLongEdge",
        orientation="portrait",
        content_type="mixed",
        two_side_page_flip_up="false",
        pages_per_sheet="oneUp",
        collate="collated"
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    logging.info("unload the ADF media")
    scan_emulation.media.unload_media('ADF')
