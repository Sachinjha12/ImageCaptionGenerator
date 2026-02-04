import logging
from time import sleep
from dunetuf.copy.copy import *
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:CAT_Test - check copy ui two 2 one using flatbed
            1. Wait for home screen.
            2. Clear ADF media.
            3. Load flatbed with Letter.
            4. Load/configure Tray 2 with Plain Letter.
            5. Enter Copy App.
            6. Show Copy options.
            7. Set input size to Letter.
            8. Set paper selection to Tray2.
            9. Hide Copy options.
            10. Set sides to Two2One.
            11. Start copy job (first page).
            12. Wait for first side to print.
            13. Flip sheet on flatbed (second page) and continue.
            14. Wait until asks for another page, select 'Done'.
            15. Wait for jobs to complete, verify success.
            16. Cleanup: Navigate Home.
            17. Cleanup: Reset trays.
        18. Cleanup: Clear flatbed media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-88892
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +name:test_copy_ui_flatbed_two2one
    +test:
        +title:test_copy_ui_flatbed_two2one
        +guid:0d2e6d64-486e-4118-92c5-d9f6a31ea552
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_two2one(spice, job, cdm, udw, net, copy,tray, configuration,scan_emulation):
    job.bookmark_jobs()

    logging.info("Unload ADF")
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('Flatbed', 1)
    
    if tray.is_size_supported('na_letter_8.5x11in', 'tray-2'):
        tray.configure_tray('tray-2', 'na_letter_8.5x11in', 'stationery')
        tray.load_media('tray-2')

    logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 1-2 Sided")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_copy_side(side_mode='2_1_sided')

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_app = spice.copy_ui()
    sleep(10)
    copy_app.start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_1_sided")

    logging.info("Validate copy settings for current job")
    copy.validate_settings_used_in_copy(sides='oneSided', pages_per_sheet='oneUp', media_source='flatbed')

    logging.info("Check the copy job complete successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete')
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    spice.goto_homescreen()
    scan_emulation.media.load_media('ADF',1)
