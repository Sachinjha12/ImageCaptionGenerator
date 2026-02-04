import pytest
import logging

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy one2one test from adf
            1. Wait for home screen.
            2. Load ADF with 4 pages of Letter Portrait (simplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Enter Copy App.
            5. Show Copy options.
            6. Set input size to Letter.
            7. Set paper selection to tray 2.
            8. Set number of copies to 3.
            9. Hide Copy options.
            10. Set sides to One2One.
            11. Start copy job.
            12. Wait for jobs to complete, verify success.
            13. Cleanup: Navigate Home.
            14. Cleanup: Reset trays.
            15. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +name:test_copy_ui_adf_one2one_test
    +test:
        +title:test_copy_ui_adf_one2one_test
        +guid:434689f4-0b36-456b-b15d-011475a26520
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaInputInstalled=Tray2


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_one2one_test(job, tray, device, udw, spice,scan_emulation):
    try:
        scan_emulation.media.load_media('ADF',4)
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
        spice.copy_ui().ui_copy_set_no_of_pages(3)
        spice.copy_ui().select_copy_side("1_1_sided")
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
