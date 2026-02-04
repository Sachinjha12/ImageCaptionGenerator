import logging
from dunetuf.copy.copy import *
import time
from dunetuf.power.power import Power, ActivityMode

def check_duplex_support(cdm):
    response = cdm.get("cdm/scan/v1/status")
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
    +purpose:Test copy with Add to Contents Copy Margin
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-88887
    +timeout:600
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_with_copy_margins_addtocontents_setting
    +test:
        +title:test_copy_ui_job_with_copy_margins_addtocontents_setting
        +guid:e49a37bc-4770-40b5-b205-c9901de9baab
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & CopyPrintMargins=AddToContents & ScanEngine=LightWing

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_job_with_copy_margins_addtocontents_setting(setup_teardown_with_copy_job, job, spice, net, cdm, udw, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_copy_margins("Add to Contents")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        copy_margins="addToContents"
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
