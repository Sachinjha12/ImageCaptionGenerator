import time
import pytest
import logging

from dunetuf.job.job import Job
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel

def reset_trays(tray, print_emulation):
    # load and configure the installed trays with default values(letter and plain)
    tray_list = print_emulation.tray.get_installed_trays()
    for tray_id in tray_list:
        print_emulation.tray.capacity_unlimited(tray_id)
        if tray_id == MediaInputIds.Tray1.name:
            print_emulation.tray.load(tray_id, MediaSize.Letter.name)
        else:
            print_emulation.tray.open(tray_id)
            print_emulation.tray.load(tray_id, MediaSize.Letter.name)
            print_emulation.tray.close(tray_id)
    # configure the trays with default values using CDM call
    tray.reset_trays()

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
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_flatbed_one_2_one_test2
    +test:
        +title:test_copy_ui_flatbed_one_2_one_test2
        +guid:6acf8b40-daba-49ef-98e7-1f2381b8418c
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter  & MediaInputInstalled=Tray2  
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_one_2_one_test2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw, configuration):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed',1)
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
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
        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded = False)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('Flatbed')
        reset_trays(tray, print_emulation)

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
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_two2one
    +test:
        +title:test_copy_ui_two2one
        +guid:73c778a1-7475-468f-9fa4-0d01e1ae31fe
        +dut:
            +type:Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter  & MediaInputInstalled=Tray2 & Copy=2Sided2To1 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_two2one(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw, configuration):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_mediaM(media_id='Flatbed', media_numsheet=1, is_duplex='true')
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
        logging.info("Go to Copy > Options, set Pages per sheet to 2, set Sides as 2-1 Sided")
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_1_sided")
        spice.copy_ui().select_media_size_option("Letter")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy(familyname=configuration.familyname, adfLoaded=False, sided="2_1_sided")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('Flatbed')
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy two2two test from flatbed
            1. Wait for home screen.
            2. Load Flatbed with Letter Portrait (duplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Enter Copy App.
            5. Set sides to Two2Two.
            6. Show Copy options.
            7. Set input size to Letter.
            8. Set paper selection to Tray 2.
            9. Start copy job.
            10.Give Continue to scan other side.
            11. Wait for jobs to complete, verify success.
            12. Cleanup: Navigate Home.
            13. Cleanup: Reset trays.
            14. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:400
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_flatbed_two2two_test
    +test:
        +title:test_copy_ui_flatbed_two2two_test
        +guid:e01e8f31-927c-4ec7-966b-911d65f51068
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter  & MediaInputInstalled=Tray2 & Copy=2Sided2To2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_two2two_test(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw, configuration):
    try:
        scan_emulation.media.load_mediaM(media_id='Flatbed', media_numsheet=1, is_duplex='true')
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Low.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
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
        scan_emulation.media.unload_media('Flatbed')
        reset_trays(tray, print_emulation)

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
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_reduce_enlarge_basic_manual_300_flatbed2
    +test:
        +title:test_copy_ui_reduce_enlarge_basic_manual_300_flatbed2
        +guid:d78280b4-62fc-45ca-82ed-bbdf7f0334aa
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter  & MediaInputInstalled=Tray2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_reduce_enlarge_basic_manual_300_flatbed2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.unload_media('ADF')
        scan_emulation.media.load_media('Flatbed',1)
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
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
        spice.copy_ui().start_copy(familyname="enterprise", adfLoaded=False)
        
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('Flatbed')
        reset_trays(tray, print_emulation)
