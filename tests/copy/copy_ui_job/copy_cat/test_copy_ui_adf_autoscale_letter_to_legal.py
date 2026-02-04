import pytest
import logging
import time

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test for Autoscale Letter to Legal
            1. Wait for home screen.
            2. Load ADF with 1 sheet of Letter Portrait (simplex).
            3. Load/configure Tray 1 with Plain Legal.
            4. Enter Copy App.
            5. Show Copy options.
            6. Set input size to Letter.
            7. Set paper selection to Tray 1.
            8. Start copy job.
            9. Wait for jobs to complete, verify success.
            10. Cleanup: Navigate Home.
            11. Cleanup: Reset trays.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:EnterpriseA4 
    +feature_team:ENTA4ProductTest
    +name:test_copy_ui_adf_autoscale_legal_to_letter
    +test:
        +title:test_copy_ui_adf_autoscale_legal_to_letter
        +guid:401554e8-600b-4a89-8b96-32dd90d61d47
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_autoscale_legal_to_letter(job, tray, device, udw, spice, scan_emulation):
    try:
        scan_emulation.media.load_media('ADF',1)
        tray.unload_media('all')
        if tray.is_size_supported('na_legal_8.5x14in', 'tray-1'):
            tray.configure_tray('tray-1', 'na_legal_8.5x14in', 'stationery')
            tray.load_media('tray-1')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_media_size_option("Legal")
        spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_resize_option("Legal to letter(72%)")
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        time.sleep(15)
        spice.copy_ui().media_mismatch_flow()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
