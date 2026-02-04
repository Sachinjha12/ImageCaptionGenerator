import pytest
import logging
import time

from dunetuf.job.job import Job
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel

def reset_trays(tray, print_emulation):
    # load and configure the installed trays with default values(letter and plain)
    tray_list = print_emulation.tray.get_installed_trays()
    logging.info('reset_trays:The available trays are %s', tray_list)
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
    +purpose:Copy Test for Autoscale A4 to Letter
            1. Wait for home screen.
            2. Load ADF with 1 sheet of A4 Portrait (simplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Set A4 Override to On.
            5. Enter Copy App.
            6. Show Copy options.
            7. Set input size to A4.
            8. Set paper selection to Tray 2.
            9. Start copy job.
            10. Wait for jobs to complete, verify success.
            11. Cleanup: Navigate Home.
            12. Cleanup: Set A4 Override back to previous value.
            13. Cleanup: Reset trays.
            14. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_autoscale_a4_to_letter2
    +test:
        +title:test_copy_ui_adf_autoscale_a4_to_letter2
        +guid:e3cd6813-b73b-498d-9cce-a790a53ab34f
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A4 & ADFMediaSize=Letter & MediaInputInstalled=Tray2 & CopyOutputScale=A4toLetter
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_autoscale_a4_to_letter2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw, configuration):
    try:
        scan_emulation.media.load_mediaM(media_id='ADF', media_size='A4', media_numsheet=1)
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("A4")
        # TODO : Set A4 Override to On       
        spice.copy_ui().select_media_size_option("A4")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_resize_option("A4 to Letter(91%)")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        time.sleep(20)
        spice.copy_ui().media_mismatch_flow()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test for Autoscale Legal to Letter
            1. Wait for home screen.
            2. Load ADF with 1 sheet of Legal.
            3. Load/configure Tray 1 with Plain Legal.
            4. Enter Copy App.
            5. Show Copy options.
            6. Set input size to Legal.
            7. Set paper selection to Tray 1.
            8. Start copy job.
            9. Wait for jobs to complete, verify success.
            10. Cleanup: Navigate Home.
            11. Cleanup: Reset trays.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_legal_to_letter
    +test:
        +title:test_copy_ui_adf_legal_to_letter
        +guid:2cbf0544-56cf-4f4e-b399-7b93f11d1d25
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Legal & MediaInputInstalled=Tray1 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_legal_to_letter(cdm, media, job, print_emulation, spice, scan_emulation, tray, udw, configuration):
    try:
        scan_emulation.media.load_mediaM(media_id='ADF', media_size='legal', media_numsheet=1)
        tray1= MediaInputIds.Tray1.name
        tray.configure_tray("tray-1", "na_letter_8.5x11in", "stationery")
        print_emulation.tray.empty(tray1)
        print_emulation.tray.load(tray1, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("Legal") 
        spice.copy_ui().select_media_size_option("Letter")
        spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_resize_option("Legal to letter(72%)")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        time.sleep(30)
        spice.copy_ui().media_mismatch_flow()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test Loading ADF with Legal Short
            1. Wait for home screen.
            2. Load ADF with 1 sheet of Legal Portrait (simplex).
            3. Load/configure Tray 1 with Plain Legal.
            4. Set number of copies to 2.
            5. Set input size to Legal.
            6. Set paper selection to Tray 1.
            7. Start Copy job.
            8. Wait for jobs to complete, verify success.
            9. Cleanup: Reset, to change Copy count.
            10. Cleanup: Reset trays.
            11. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_basic_legal_short
    +test:
        +title:test_copy_ui_adf_basic_legal_short
        +guid:70ef6797-2a1d-45d9-ba0c-ab7317908aa1
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Legal & MediaInputInstalled=Tray1 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_basic_legal_short(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_mediaM(media_id='ADF', media_size='legal', media_numsheet=1)
        tray1= MediaInputIds.Tray1.name
        tray.configure_tray('tray-1', 'na_legal_8.5x14in', 'stationery')
        print_emulation.tray.empty(tray1)
        print_emulation.tray.load(tray1, MediaSize.Legal.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
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
        spice.copy_ui().start_copy()
        time.sleep(30)
        spice.copy_ui().media_mismatch_flow()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy job 10sheets using duplex from ADF
            1. Wait for home screen.
            2. Load ADF with 10 sheets of Letter Portrait (duplex).
            3. Empty all trays.
            4. Load/configure Tray 2 with Plain Letter.
            5. Enter Copy App.
            6. Set sides to Two2Two.
            7. Show Copy options.
            8. Set orientation to portrait.
            9. Start copy job.
            10. Wait for jobs to complete, verify success.
            11. Cleanup: Navigate Home.
            12. Cleanup: Reset trays.
            13. Cleanup: Clear ADF media
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_duplex_job_10sheet
    +test:
        +title:test_copy_ui_adf_duplex_job_10sheet
        +guid:e0fcad37-9eb2-495c-978f-05a0989459b0
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter  & MediaInputInstalled=Tray2 & Copy=2Sided2To2 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_duplex_job_10sheet(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_media(media_id='ADF', media_numsheet=10)
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        # time.sleep(10)
        # tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        # cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_media_size_option("Letter")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

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
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_one2one_test2
    +test:
        +title:test_copy_ui_adf_one2one_test2
        +guid:1f4bf397-1a14-4932-ac15-66133eafe4be
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter  & MediaInputInstalled=Tray2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_one2one_test2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_media(media_id='ADF',media_numsheet=4)
        tray2= MediaInputIds.Tray2.name      
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","na_letter_8.5x11in","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().ui_copy_set_no_of_pages(3)
        spice.copy_ui().select_media_size_option("Letter")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_copy_side("1_1_sided")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy jobs using the A4 paper size
            1. Wait for home screen.
            2. Load ADF with 1 sheet of A4 Portrait (simplex).
            3. Load/configure Tray 2 with Plain A4.
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
    +reqid:DUNE-126822
    +timeout:900
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_original_paper_size_basic_a4_short2
    +test:
        +title:test_copy_ui_adf_original_paper_size_basic_a4_short2
        +guid:f2657618-8a6c-4809-80fe-5431de2a2b57
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A4  & MediaInputInstalled=Tray2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_original_paper_size_basic_a4_short2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_mediaM(media_id='ADF', media_size='A4', media_numsheet=1)
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.A4.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)
        tray.configure_tray("tray-2","iso_a4_210x297mm","stationery")
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list() 
        spice.copy_ui().select_original_size("A4")    
        #TODO: Set A4 Override to Off
        spice.copy_ui().select_media_size_option("A4")
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        logging.info('Cleaning up the test')
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

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
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_original_paper_size_basic_letter_short2
    +test:
        +title:test_copy_ui_adf_original_paper_size_basic_letter_short2
        +guid:da5b4a6e-76bd-4169-a435-15b5101d7954
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter & MediaInputInstalled=Tray2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_original_paper_size_basic_letter_short2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_mediaM(media_id='ADF', media_numsheet=1)
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
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)
        
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy two2two test from adf
            1. Wait for home screen.
            2. Load ADF with 4 sheets of Letter Portrait (duplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Enter Copy App.
            5. Set sides to Two2Two.
            6. Show Copy options.
            7. Set input size to Letter.
            8. Set paper selection to Tray 2.
            9. Start copy job.
            10. Wait for jobs to complete, verify success.
            11. Cleanup: Navigate Home.
            12. Cleanup: Reset trays.
            13. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_two_2_two_test2
    +test:
        +title:test_copy_ui_adf_two_2_two_test2
        +guid:229a4302-3f67-4a30-a237-38c389ffb037
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter & MediaInputInstalled=Tray2 & Copy=2Sided2To2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_two_2_two_test2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_mediaM(media_id='ADF', media_numsheet=4, is_duplex='true')
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
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test for reduce enlarge basic manual scalling 101 %
            1. Wait for home screen.
            2. Load ADF with 1 sheet of Letter Portrait (simplex).
            3. Load/configure Tray 2 with Plain Letter.
            4. Enter Copy App.
            5. Show Copy options.
            6. Set input size to Letter.
            7. Set paper selection to Tray 2.
            8. Set Reduce/Enlarge to 101.
            9. Start copy job.
            10. Navigate Home.
            11. Wait for jobs to complete, verify success.
            12. Cleanup: Navigate Home.
            13. Cleanup: Reset trays.
            14. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-126822
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_reduce_enlarge_basic_manual_101_adf2
    +test:
        +title:test_copy_ui_reduce_enlarge_basic_manual_101_adf2
        +guid:8cd4d633-f3da-4be0-a6ff-d640ef515557
        +dut:
            +type:Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder &  ADFMediaSize=Letter & MediaInputInstalled=Tray2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_reduce_enlarge_basic_manual_101_adf2(cdm, job, media, print_emulation, spice, scan_emulation, tray, udw):
    try:
        scan_emulation.media.load_media('ADF',1)
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
        spice.copy_ui().set_copy_custom_value_option(101)
        spice.copy_ui().back_to_copy_options_list_view("Back_to_options_list")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()      
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw, total_time=120)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.unload_media('ADF')
        reset_trays(tray, print_emulation)
