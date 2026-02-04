import pytest
import logging
import time

from dunetuf.copy.copy import *
from dunetuf.job.job import Job


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy two2two test from flatbed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-70289
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +name:test_copy_ui_flatbed_two_2_two_test
    +test:
        +title:test_copy_ui_flatbed_two_2_two_test
        +guid:b2437924-0454-4a33-8749-d6109c212e6c
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed  & MediaInputInstalled=Tray2


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_flatbed_two_2_two_test(job, tray, device, udw, spice, configuration, scan_emulation):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed', 1)
        tray.unload_media('all')

        if tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
            tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
            tray.load_media('tray-2')

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().select_media_size_option("Letter")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_2_sided")

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.load_media('ADF',1)
        tray.reset_trays()
