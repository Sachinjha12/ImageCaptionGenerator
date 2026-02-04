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
    +purpose:Test copy with 2-Sided Pages Filp Up is ON
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_two_sided_pages_filp_up_option
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_two_sided_pages_filp_up_option
        +guid:b09004ca-6075-4aad-aa48-5c72b2022886
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided2To1 & Copy=Collation
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_two_sided_pages_filp_up_option(setup_teardown_with_copy_job, scan_emulation, job, spice, cdm, udw, net, configuration):
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
    #todo: need to update here for HMDE-357
    copy_job_app.select_copy_side("1_1_sided")
    current_pages_flip_up_status = copy_job_app.get_copy_2sided_pages_flip_up_status()
    assert current_pages_flip_up_status is False

    copy_job_app.select_copy_side("1_2_sided")
    current_pages_flip_up_status = copy_job_app.get_copy_2sided_pages_flip_up_status()
    assert current_pages_flip_up_status is False

    copy_job_app.select_copy_side("2_1_sided")
    current_pages_flip_up_status = copy_job_app.get_copy_2sided_pages_flip_up_status()
    assert current_pages_flip_up_status is False

    copy_job_app.select_copy_side("2_2_sided")
    current_pages_flip_up_status = copy_job_app.get_copy_2sided_pages_flip_up_status()
    assert current_pages_flip_up_status is False

    logging.info("set flip up as ON")
    copy_job_app.set_copy_2sided_flip_up_options(two_sided_options="on")

    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value= 0)

    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto", 
        sides="twoSidedShortEdge",
        orientation="portrait",
        quality="normal",
        content_type="mixed", 
        pages_per_sheet="oneUp",
        collate="collated"
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    logging.info("unload the ADF media")
    scan_emulation.media.unload_media(media_id='ADF')
    if is_adf_duplex_supported == False:
        disable_duplex_supported(cdm, udw)
    scan_emulation.media.load_media(media_id='ADF')
