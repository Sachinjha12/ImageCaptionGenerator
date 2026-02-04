import logging
from dunetuf.copy.copy import *
import time
from dunetuf.ui.uioperations.WorkflowOperations.IDCardCopyAppWorkflowObjectIds import IDCardCopyAppWorkflowObjectIds

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:when implement the id copy job, select the cancel button on second screen
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard_cancel_after_1st_side_scan
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcard_cancel_after_1st_side_scan
        +guid:8c2c4f2b-f9d8-4ef5-83d4-315f8500dbf8
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_idcard_cancel_after_1st_side_scan(setup_teardown_with_id_copy_job, job, spice, net, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to id copy screen")
    idcopy_job_app = spice.idcard_copy_app
    idcopy_job_app.goto_idcopy()
    logging.info("check the strings on the screen")
    idcopy_job_app.check_spec_on_idcopy_screen(net)
    logging.info("start to id card copy")
    idcopy_job_app.start_id_copy()
    concurent = True
    if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power","moreto","moretohi","kebin", "victoria", "victoriaplus"]:
        concurent = False
    idcopy_job_app.select_idcopy_first_continue_button(concurent=concurent)
    logging.info("Select cancel")
    idcopy_job_app.click_idcopy_cancel_on_second_screen()
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"cancelled"}])


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copy button should not greyedout after cancel the idcard job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard_job_cancel_verify_copy_button_should_not_greyedout
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcard_job_cancel_verify_copy_button_should_not_greyedout
        +guid:6517da32-5c9c-479b-9df2-270f2a8b2b66
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_idcard_job_cancel_verify_copy_button_should_not_greyedout(job, udw, spice, net):

    job.bookmark_jobs()
    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")

    try:
        spice.idcard_copy_app.goto_idcopy()
        spice.idcard_copy_app.ui_idcopy_set_no_of_pages(5)
        spice.idcard_copy_app.start_id_copy()
        concurrent = True
        if job.job_concurrency_supported == "false":
            concurrent = False
        spice.idcard_copy_app.select_idcopy_first_continue_button(concurent=concurrent)
        spice.idcard_copy_app.select_idcopy_second_continue_button()
        logging.info("Click Cancel button")
        current_option = spice.wait_for(IDCardCopyAppWorkflowObjectIds.idcard_job_cancel_button)
        current_option.mouse_click()  
        time.sleep(5)
        logging.info("Check the copy job cancelled successfully")
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
        assert spice.wait_for(IDCardCopyAppWorkflowObjectIds.button_startIDCopy) ["visible"] is True, 'Id card copy button is not visible'
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()
        spice.wait_ready()


