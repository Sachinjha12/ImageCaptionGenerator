import logging
from dunetuf.copy.copy import *

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify the error message displayed when starting an IDCopy job from document feeder
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard_job_errorscenario_from_document_feeder
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_idcard_job_errorscenario_from_document_feeder
        +guid:dd61d7de-0e8f-4f46-9537-5c1290b4511c
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder  & Copy=IDCopy


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_idcard_job_errorscenario_from_document_feeder(setup_teardown_with_id_copy_job, job, spice, net, udw):

    logging.info("load the ADF media")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to id copy screen")
    idcopy_job_app = spice.idcard_copy_app
    idcopy_job_app.goto_idcopy()
    logging.info("Start ID Card copy")
    idcopy_job_app.start_id_copy()
    logging.info("New behaviour :IDCard Copy job should happen even though ADF is loaded")
    concurrent = True
    if job.job_concurrency_supported == "false":
        concurrent = False
    idcopy_job_app.select_idcopy_first_continue_button(concurent=concurrent)
    logging.info("Select second continue button")
    idcopy_job_app.select_idcopy_second_continue_button()
    logging.info("wait for the id card copy job complete")
    idcopy_job_app.wait_for_idcopy_complete(net)
    copy_job_details = job.get_job_details(current_job_type="copy")
    # Note: according to DUNE-51040, ADf loaded will be ignored, we will not have any error message, so validate ID card job is from flatbed. 
    assert copy_job_details["src"]["scan"]["mediaSource"] == "flatbed", "ID card from ADF is unexpected."
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"success"}])
    spice.goto_homescreen()
    spice.wait_ready()
