import pytest
import logging
import time
import datetime

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-109033
    +timeout: 300
    +asset: Copy
    +test_framework: TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_ui_basic_copy_jobdetails_completed
    +test:
        +title: test_copy_ui_basic_copy_jobdetails_completed
        +guid:d7ab5d0f-1d52-4301-8789-7ab422515a29
        +dut:
            +type: Simulator, Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & JobHistory=SingleJob
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_basic_copy_jobdetails_completed(scan_emulation, configuration, job, spice, udw):
    logging.info("============================================")
    logging.info("configuration.productname=(%s)",configuration.productname)
    if configuration.productname == "jupiter" or configuration.productname.startswith("beam"):
        logging.info("[EXIT-TEST] this test is only valid for models with a copy function from flatbed/ADF")
        return

    logging.info("======================")
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    scan_emulation.media.load_media(media_id='ADF')

    try:
        # Go to copy app and start copy job
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()

        # Wait for the job to complete and get the job id.
        job_id = job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        logging.info("jobId is "+ job_id_cdm)

        # Go to Homescreen and Job Queue App screen
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()

        # Check that the job is in "History" section
        spice.job_ui.goto_job(job_id_cdm)
        assert spice.job_ui.recover_job_status() == "Completed"

        # Check by CDM that the job has passed to history
        job_cdm = job.get_job_from_history_by_id(job_id_cdm)
        assert job_cdm["jobId"] == job_id_cdm

        time.sleep(3)
    
        # Check job details
        logging.info("Copies        : "+ spice.job_ui.recover_job_copies())
        logging.info("Total Pages   : "+ spice.job_ui.recover_job_total_pages())
        logging.info("Started       : "+ spice.job_ui.recover_job_start_time()[0:-4])
        logging.info("Completed     : "+ spice.job_ui.recover_job_completion_time()[0:-4])
        logging.info("User Name     : "+ spice.job_ui.recover_job_user_name())
        logging.info("Job Type      : "+ spice.job_ui.recover_job_type())
        logging.info("Source        : "+ spice.job_ui.recover_job_media_source())
        logging.info("Paper Type    : "+ spice.job_ui.recover_job_media_tpye())
        logging.info("Output Size   : "+ spice.job_ui.recover_job_output_size())
        logging.info("Color Mode    : "+ spice.job_ui.recover_job_color_mode())
        logging.info("Original Size : "+ spice.job_ui.recover_job_original_size())

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-109033
    +timeout: 600
    +asset: Copy
    +test_framework: TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_ui_a4_copy_jobdetails_completed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_a4_copy_jobdetails_completed
        +guid:570e9f43-932c-4075-8965-dd14e458036a
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A4 & MediaInputInstalled=Tray1 & JobHistory=SingleJob   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_a4_copy_jobdetails_completed(configuration, job, tray, spice, udw):
    logging.info("============================================")
    logging.info("configuration.productname=(%s)",configuration.productname)
    if configuration.productname == "jupiter" or configuration.productname.startswith("beam"):
        logging.info("[EXIT-TEST] this test is only valid for models with a copy function from flatbed/ADF")
        return
    
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:

        tray.unload_media('all')

        if tray.is_size_supported('iso_a4_210x297mm', 'tray-1'):
            tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'stationery')
            tray.load_media('tray-1')

        # Go to copy app and start copy job
        spice.copy_ui().goto_copy()

        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_media_size_option("A4")
        spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().start_copy()

        # Wait for the job to complete and get the job id.
        job_id = job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        logging.info("jobId is "+ job_id_cdm)

        # Go to Homescreen and Job Queue App screen
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()

        # Check that the job is in "History" section
        spice.job_ui.goto_job(job_id_cdm)
        assert spice.job_ui.recover_job_status() == "Completed"

        # Check by CDM that the job has passed to history
        job_cdm = job.get_job_from_history_by_id(job_id_cdm)
        assert job_cdm["jobId"] == job_id_cdm

        time.sleep(3)
    
        # Check job details
        logging.info("Copies        : "+ spice.job_ui.recover_job_copies())
        logging.info("Total Pages   : "+ spice.job_ui.recover_job_total_pages())
        logging.info("Started       : "+ spice.job_ui.recover_job_start_time()[0:-3])
        logging.info("Completed     : "+ spice.job_ui.recover_job_completion_time()[0:-3])
        logging.info("User Name     : "+ spice.job_ui.recover_job_user_name())
        logging.info("Job Type      : "+ spice.job_ui.recover_job_type())
        logging.info("Source        : "+ spice.job_ui.recover_job_media_source())
        logging.info("Paper Type    : "+ spice.job_ui.recover_job_media_tpye())
        logging.info("Output Size   : "+ spice.job_ui.recover_job_output_size())
        logging.info("Color Mode    : "+ spice.job_ui.recover_job_color_mode())
        logging.info("Original Size : "+ spice.job_ui.recover_job_original_size())
        assert spice.job_ui.recover_job_media_source() == "Tray 1"
        assert spice.job_ui.recover_job_output_size() == "A4 (210x297 mm)"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
