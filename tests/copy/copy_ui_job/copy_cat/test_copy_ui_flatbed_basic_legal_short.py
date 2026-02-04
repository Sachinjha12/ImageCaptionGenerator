import time
import pytest
import logging

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy jobs using the Legal paper size
            1. Wait for home screen.
            2. Clear ADF media.
            3. Load flatbed with Legal.
            4. Load/configure Tray 1 with Plain Legal.
            5. Set number of copies to 2.
            6. Set input size to Legal.
            7. Set paper selection to Tray 1.
            8. Start Copy job.
            9. Wait for jobs to complete, verify success.
            10. Cleanup: Reset, to change Copy count.
            11. Cleanup: Reset trays.
            13. Cleanup: Clear flatbed media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_classification:System
    +name:test_copy_ui_flatbed_basic_legal_short
    +test:
        +title:test_copy_ui_flatbed_basic_legal_short
        +guid:019275c5-5234-4a5e-9c69-097f739911b4
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Legal

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_flatbed_basic_legal_short(configuration, job, tray, device, udw, spice, scan_emulation):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 1)

        tray.unload_media('all')

        if tray.is_size_supported('na_legal_8.5x14in', 'tray-1'):
            tray.configure_tray('tray-1', 'na_legal_8.5x14in', 'stationery')
            tray.load_media('tray-1')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().ui_copy_set_no_of_pages(2)
        spice.copy_ui().select_original_size("Legal")
        spice.copy_ui().select_media_size_option("Legal")
        spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy(familyname=configuration.familyname, adfLoaded=False)
        time.sleep(20)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
