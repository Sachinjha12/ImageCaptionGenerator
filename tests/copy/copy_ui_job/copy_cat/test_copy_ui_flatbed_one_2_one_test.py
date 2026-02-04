import pytest
import logging

from dunetuf.copy.copy import *
from dunetuf.job.job import Job


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy one2one test from Flatbed
            1. Wait for home screen.
            2. Clear ADF media.
            3. Load flatbed with Letter.
            4. Load/configure Tray 2 with Plain Letter.
            5. Enter Copy App.
            6. Set sides to One2One.
            7. Show Copy options.
            8. Set input size to Letter.
            9. Set paper selection to tray 2.
            10. Start copy job.
            11. Wait for jobs to complete, verify success.
            12. Cleanup: Navigate Home.
            13. Cleanup: Reset trays.
            14. Cleanup: Clear flatbed media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_classification:System
    +name:test_copy_ui_flatbed_one_2_one_test
    +test:
        +title:test_copy_ui_flatbed_one_2_one_test
        +guid:dc8e0835-b705-4450-9023-502c20f29b75
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed  & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_flatbed_one_2_one_test(job, tray, device, udw, spice, configuration, scan_emulation):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 1)
        tray.unload_media('all')

        if tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
            tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
            tray.load_media('tray-2')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_media_size_option("Letter")

        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_copy_side("1_1_sided")
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded=False)

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.load_media('ADF',1)
        tray.reset_trays()
