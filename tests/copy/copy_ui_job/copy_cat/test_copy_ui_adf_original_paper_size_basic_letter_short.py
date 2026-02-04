import pytest
import logging

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy jobs using the letter paper size
            1. Wait for home screen.
            2. Load ADF with 1 sheet of Letter Portrait (simplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Enter Copy App.
            5. Show Copy options.
            6. Set input size to Letter.
            7. Start copy job.
            8. Wait for jobs to complete, verify success.
            9. Cleanup: Navigate Home.
            10. Cleanup: Reset trays.
            11. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_classification:System
    +name:test_copy_ui_adf_original_paper_size_basic_letter_short
    +test:
        +title:test_copy_ui_adf_original_paper_size_basic_letter_short
        +guid:613187c0-beb2-489e-92b7-625b2a93337b
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder  & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_original_paper_size_basic_letter_short(job, tray, device, udw, spice, scan_emulation):
    try:
        scan_emulation.media.load_media('ADF',1)
        tray.unload_media('all')

        default_configuration = tray.get_tray_configuration()
        default_second_tray = default_configuration[1]['mediaSourceId']
        if tray.is_size_supported('na_letter_8.5x11in', default_second_tray):
            tray.configure_tray(default_second_tray, 'na_letter_8.5x11in', 'stationery')
            tray.load_media(default_second_tray)

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_media_size_option("Letter")
        # Eddington support tray main/alternate
        if default_second_tray == "alternate":
            spice.copy_ui().select_paper_tray_option("Tray Alternate")
        else:
            spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
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
