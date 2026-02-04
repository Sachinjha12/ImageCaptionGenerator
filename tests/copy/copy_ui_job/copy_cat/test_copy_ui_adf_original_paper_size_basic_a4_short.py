import pytest
import logging
import time

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy jobs using the A4 paper size
            1. Wait for home screen.
            2. Load ADF with 1 sheet of A4 Portrait (simplex).
            3. Load/configure Tray 3 with Plain A4.
            4. Set A4 Override to Off.
            5. Enter Copy App.
            6. Show Copy options.
            7. Set input size to A4.
            8. Start copy job.
            9. Wait for jobs to complete, verify success.
            10. Cleanup: Navigate Home.
            11. Cleanup: Set A4 Override back to previous value.
            12. Cleanup: Reset trays.
            13. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_classification:System
    +name:test_copy_ui_adf_original_paper_size_basic_a4_short
    +test:
        +title:test_copy_ui_adf_original_paper_size_basic_a4_short
        +guid:6ef4d079-e616-4dcb-90b3-cb1dbd7b00ef
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaInputInstalled=Tray3

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_original_paper_size_basic_a4_short(job, tray, device, udw, spice, scan_emulation):
    try:
        scan_emulation.media.load_media('ADF',1)
        tray.unload_media('all')

        if tray.is_size_supported('iso_a4_210x297mm', 'tray-3'):
            tray.configure_tray('tray-3', 'iso_a4_210x297mm', 'stationery')
            tray.load_media('tray-3')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        #TODO: Set A4 Override to Off
        spice.copy_ui().select_media_size_option("A4")
        spice.copy_ui().select_paper_tray_option("Tray 3")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_resize_option("Legal to letter(72%)")
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
