import pytest
import logging
import time

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test for Autoscale A4 to Letter
            1. Wait for home screen.
            2. Load ADF with 1 sheet of A4 Portrait (simplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Set A4 Override to On.
            5. Enter Copy App.
            6. Show Copy options.
            7. Set input size to A4.
            8. Set paper selection to Tray 2.
            9. Start copy job.
            10. Wait for jobs to complete, verify success.
            11. Cleanup: Navigate Home.
            12. Cleanup: Set A4 Override back to previous value.
            13. Cleanup: Reset trays.
            14. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:EnterpriseA4 
    +feature_team:ENTA4ProductTest
    +name:test_copy_ui_adf_autoscale_a4_to_letter
    +test:
        +title:test_copy_ui_adf_autoscale_a4_to_letter
        +guid:6c77f5ad-0ed9-43d7-bc2d-c5f8f1a7ab12
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_autoscale_a4_to_letter(job, tray, device, udw, spice, scan_emulation):
    try:
        scan_emulation.media.load_media('ADF',1)
        tray.unload_media('all')
        if tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
            tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
            tray.load_media('tray-2')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("A4")
        # TODO : Set A4 Override to On
        spice.copy_ui().select_media_size_option("A4")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_resize_option("A4 to Letter(91%)")
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        time.sleep(15)
        spice.copy_ui().media_mismatch_flow()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        job.wait_for_no_active_jobs()

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
