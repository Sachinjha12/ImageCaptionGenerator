import logging
from dunetuf.copy.copy import *

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with Clip Contents Copy Margin
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-88887
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +delivery_team:Home
    +feature_team:RCB-UI
    +test_classification:System
    +name:test_copy_ui_job_with_copy_margins_clipcontents_setting
    +test:
        +title:test_copy_ui_job_with_copy_margins_clipcontents_setting
        +guid:2b7a2928-9e71-4572-96e3-acf14a132b26
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & CopyPrintMargins=ClipContentsByMargins

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_job_with_copy_margins_clipcontents_setting(setup_teardown_with_copy_job, job, spice, net, cdm, udw, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_copy_margins("Clip from Contents")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        copy_margins="clipContents"
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
