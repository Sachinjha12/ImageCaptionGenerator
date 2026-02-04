import logging
from time import sleep
from dunetuf.copy.copy import *
from dunetuf.job.job import Job



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To verify Copy from ADF with collate switch
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-91176
    +timeout:800
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_using_collate_robustness_switch
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_using_collate_robustness_switch
        +guid:3db1977b-eca6-43ec-92f1-ed924bdf3dac
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
"""

def test_copy_ui_job_using_collate_robustness_switch(scan_emulation, setup_teardown_with_copy_job, job, spice, udw, net, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("load media to ADF")
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    count=20
    for loop in range(0, count):
        copy_job_app.change_collate(collate_option="off")
        copy_job_app.change_collate(collate_option="on")
    logging.info("Back to copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Set no of copies to 2")
    copy_job_app.ui_copy_set_no_of_pages(2)
    logging.info("Start to copy")
    copy_job_app.ui_select_copy_page()

    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

