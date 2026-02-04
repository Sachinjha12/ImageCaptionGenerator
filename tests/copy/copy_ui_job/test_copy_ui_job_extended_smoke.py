import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To verify copy job works fine with color and best quality settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:360
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_using_best_color
    +test:
        +title:test_copy_ui_job_using_best_color
        +guid:af907314-3124-4274-a58c-d27f3ac2d62b
        +dut:
            +type:Simulator, Engine, Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Quality & Copy=IDCopy & Copy=Color & Print=Best
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_using_best_color(setup_teardown_with_copy_job, job, spice, net, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_color_mode("Color")
    logging.info("Set Copy Quality to Best")
    #copy_job_app.goto_quality_option()
    copy_job_app.select_quality_option("Best")
    logging.info("Back to copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)

    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])