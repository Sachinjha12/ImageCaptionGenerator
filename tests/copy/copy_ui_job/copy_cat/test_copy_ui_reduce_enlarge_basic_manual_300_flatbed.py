import pytest
import logging

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test for reduce enlarge basic manual scalling 300%
            1.Wait for home screen.
            2. Load flatbed with Letter.
            3. Load/configure Tray 2 with Plain Letter.
            4. Enter Copy App.
            5. Show Copy options.
            6. Set input size to Letter.
            7. Set paper selection to Tray 2.
            8. Set Reduce/Enlarge to to 300.
            9. Start copy job.
            10. Wait for jobs to complete, verify success.
            11. Cleanup: Navigate Home.
            12. Cleanup: Reset trays.
            13. Cleanup: Clear flatbed media
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_classification:System
    +name:test_copy_ui_reduce_enlarge_basic_manual_300_flatbed
    +test:
        +title:test_copy_ui_reduce_enlarge_basic_manual_300_flatbed
        +guid:4d1a8e07-5a7f-4cac-b617-0e2e33151764
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_reduce_enlarge_basic_manual_300_flatbed(job, tray, device, udw, spice, configuration, scan_emulation):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 1)

        tray.unload_media('all')

        if tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
            tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
            tray.load_media('tray-2')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("Letter")
        spice.copy_ui().select_media_size_option("Letter")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().goto_copy_option_output_scale()
        spice.copy_ui().goto_copy_output_scale_custom_menu()
        spice.copy_ui().set_copy_custom_value_option(300)
        spice.copy_ui().back_to_copy_options_list_view("Back_to_options_list")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded = False)

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.load_media('ADF',1)
        tray.reset_trays()
