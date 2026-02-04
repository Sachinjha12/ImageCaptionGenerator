import logging
import pytest
from dunetuf.job.storejob import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform storage job retrive operation and verify the job status
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-234794
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_verify_storage_job_retrive
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_verify_storage_job_retrive
        +guid: 48d2cdda-372b-48a6-963f-edf16739d1c4
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=DigitalSend & ScanDestination=JobStorage & JobSettings=JobStorage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_storage_job_retrive(spice, job, dunestorejob):
    try:
        logging.info("Go to Scan --> Go to Scan to Job Storage Appplication --> Perform scan to job storage operation")
        job_name = "scan_job1"
        spice.scan_job_storage.goto_send_to_job_storage_from_admin_app()
        spice.scan_job_storage.input_job_name_in_landing_view(job_name)
        spice.scan_job_storage.press_save_to_job_storage()

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
        assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

        spice.goto_homescreen()

        logging.info("Go to Home Screen --> Go to Print from Job Storage Application --> Perform print from job storage operation with scanned job")
        storejobs = dunestorejob.get_all()
        assert len(storejobs) > 0, 'Unexpected number of stored jobs found!'

        storedJobId = storejobs[0].get('jobId')
        logging.info('Stored job id: ' + storedJobId)

        spice.storejob.goto_job_storage()
        assert spice.wait_for("#JobStorageAppApplicationStackView")

        spice.storejob.select_storageJob("untitled", storedJobId)
        spice.storejob.print_storeJob_selected()

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
        assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'
    finally:
        # Delete all the stored jobs
        spice.storejob.delete_all_store_jobs(dunestorejob)
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform stroage job retrive operation for multiple files and verify the job status
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-234794
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_verify_storage_job_retrive_multiple_files
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_verify_storage_job_retrive_multiple_files
        +guid: 8426e28e-62c1-4e6b-8b70-8cd563f22faa
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=DigitalSend & ScanDestination=JobStorage & JobSettings=JobStorage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_storage_job_retrive_multiple_files(spice, job, dunestorejob):
    try:
        logging.info("Go to Scan --> Go to Scan to Job Storage Appplication --> Perform scan to job storage operation")
        job_names_list = ["scan_job1", "scan_job2", "scan_job3"]
        
        spice.scan_job_storage.goto_send_to_job_storage_from_admin_app()
        
        for job_name in job_names_list:
            spice.scan_job_storage.input_job_name_in_landing_view(job_name)
            spice.scan_job_storage.press_save_to_job_storage()

            job.wait_for_no_active_jobs()
            new_jobs = job.get_newjobs()
            assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
            assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'
        
        spice.goto_homescreen()
        logging.info("Go to Home Screen --> Go to Print from Job Storage Application --> Perform print from job storage operation with scanned job")
        storeJobs = dunestorejob.get_all()
        assert len(storeJobs) >= 3, 'Unexpected number of stored jobs found!'

        spice.storejob.goto_job_storage()
        assert spice.wait_for("#JobStorageAppApplicationStackView")
        spice.storejob.job_storage_click_button("untitled")

        for storeJob in storeJobs:
            storedJobId = storeJob.get('jobId')
            logging.info('Stored job id: ' + storedJobId)
            spice.storejob.job_storage_click_button(storedJobId)

        spice.storejob.print_storeJob_selected()

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert len(new_jobs) >=3 , 'Unexpected number of jobs found!'

        for job_index in range(len(new_jobs)-1, len(new_jobs)-len(job_names_list), -1):
            assert new_jobs[job_index].get('state') == 'completed', 'Job not completed'
            assert new_jobs[job_index].get('completionState') == 'success', 'Job is not success'
    finally:
        # Delete all the stored jobs
        spice.storejob.delete_all_store_jobs(dunestorejob)
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform storage job retrive operation and print the jobs with more 1 copies
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-234794
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_verify_storage_job_retrive_multiple_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_verify_storage_job_retrive_multiple_copies
        +guid: 984bedc8-774a-47ad-9ede-9d128bab012a
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=DigitalSend & ScanDestination=JobStorage & JobSettings=JobStorage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_storage_job_retrive_multiple_copies(spice, job, dunestorejob):
    try:
        logging.info("Go to Scan --> Go to Scan to Job Storage Appplication --> Perform scan to job storage operation")
        job_name = "scan_job1"
        spice.goto_homescreen()
        spice.scan_job_storage.goto_send_to_job_storage_from_admin_app()
        spice.scan_job_storage.input_job_name_in_landing_view(job_name)
        spice.scan_job_storage.press_save_to_job_storage()

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
        assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

        spice.goto_homescreen()

        logging.info("Go to Home Screen --> Go to Print from Job Storage Application --> Perform print from job storage operation with scanned job")
        storejobs = dunestorejob.get_all()
        assert len(storejobs) > 0, 'Unexpected number of stored jobs found!'

        storedJobId = storejobs[0].get('jobId')
        logging.info('Stored job id: ' + storedJobId)

        spice.storejob.goto_job_storage()
        assert spice.wait_for("#JobStorageAppApplicationStackView")
        spice.storejob.select_storageJob("untitled", storedJobId)

        spice.storejob.detailed_storeJob_selected()
        spice.storejob.click_on_copies_plus_button()
        spice.storejob.print_storeJob_selected()

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
        assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'
    finally:
        # Delete all the stored jobs
        spice.storejob.delete_all_store_jobs(dunestorejob)
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform storage job retrive operation and print the same job multiple times in print from job storage app
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-234794
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_verify_storage_job_retrive_same_job_perform_multiple_prints
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_verify_storage_job_retrive_same_job_perform_multiple_prints
        +guid: 18ee81c1-7a89-4ab9-9b9d-037b5e9df910
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=DigitalSend & ScanDestination=JobStorage & JobSettings=JobStorage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_storage_job_retrive_same_job_perform_multiple_prints(spice, job, dunestorejob):
    try:
        logging.info("Go to Scan --> Go to Scan to Job Storage Appplication --> Perform scan to job storage operation")
        job_name = "scan_job1"
        spice.goto_homescreen()
        spice.scan_job_storage.goto_send_to_job_storage_from_admin_app()
        spice.scan_job_storage.input_job_name_in_landing_view(job_name)
        spice.scan_job_storage.press_save_to_job_storage()

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
        assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

        spice.goto_homescreen()

        logging.info("Go to Home Screen --> Go to Print from Job Storage Application --> Perform print from job storage operation with scanned job")
        storejobs = dunestorejob.get_all()
        assert len(storejobs) > 0, 'Unexpected number of stored jobs found!'

        storedJobId = storejobs[0].get('jobId')
        logging.info('Stored job id: ' + storedJobId)

        spice.storejob.goto_job_storage()
        assert spice.wait_for("#JobStorageAppApplicationStackView")
        spice.storejob.job_storage_click_button("untitled")
        
        for _ in range(3):
            spice.storejob.job_storage_click_button(storedJobId)
            spice.storejob.print_storeJob_selected()

            job.wait_for_no_active_jobs()
            new_jobs = job.get_newjobs()
            assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
            assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'
    finally:
        # Delete all the stored jobs
        spice.storejob.delete_all_store_jobs(dunestorejob)
        spice.goto_homescreen()
