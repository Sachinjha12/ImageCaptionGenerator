import pytest
import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.job.job import Job
from dunetuf.copy.copy import * 

def source_destination(source, dest):
    return {'src': {source: {}}, 'dest': {dest: {}}}

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test Loading ADF with Letter SEF
            1. Wait for home screen.
            2. Validate the original SEF size
            3. Validate the media SEF size
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:1100
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_SEF_LEF_paper_size
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_SEF_LEF_paper_size
        +guid:b1ac9077-362e-41bb-8cbb-1a2a43b061b0
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & Copy=OriginalSize & Copy=PaperSize

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_verify_SEF_LEF_paper_size(spice):
    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().goto_copy_option_original_size_screen()
        spice.copy_ui().check_original_size_option("Letter")
        spice.copy_ui().check_original_size_option("Letter_SEF")
        spice.copy_ui().check_original_size_option("A4")
        spice.copy_ui().check_original_size_option("A4_SEF")
        spice.copy_ui().check_original_size_option("A5")
        spice.copy_ui().check_original_size_option("A5_SEF")
        spice.copy_ui().check_original_size_option("B5")
        spice.copy_ui().check_original_size_option("B5_SEF")
        backButton = spice.wait_for("#scan_originalSizeMenuSelectionList #BackButton", timeout=4)
        backButton.mouse_click()

        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().goto_copy_paper_size_screen()
        spice.copy_ui().check_media_size_option("Letter")
        spice.copy_ui().check_media_size_option("Letter_SEF")
        spice.copy_ui().check_media_size_option("A4")
        spice.copy_ui().check_media_size_option("A4_SEF")
        spice.copy_ui().check_media_size_option("A5")
        spice.copy_ui().check_media_size_option("A5_SEF")
        spice.copy_ui().check_media_size_option("B5")
        spice.copy_ui().check_media_size_option("B5_SEF")
        backButton = spice.wait_for("#copy_paperSelectionMenuList #BackButton", timeout=4)
        backButton.mouse_click()

        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Copy Test Loading ADF with Letter SEF
            1. Wait for home screen.
            2. Load ADF with 1 sheet of Letter Portrait (simplex).
            3. Load/configure Tray 1 with Plain Letter SEF.
            4. Set number of copies to 3.
            5. Set input size to Letter SEF.
            6. Set paper selection to Tray 1.
            7. Start Copy job.
            8. Wait for jobs to complete, verify success.
            9. Cleanup: Reset, to change Copy count.
            10. Cleanup: Reset trays.
            11. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_basic_letter_SEF
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_basic_letter_SEF
        +guid:2d4f11d5-dcf3-4f82-9420-535d42a809fe
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & PrintEngineFormat=A3 & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_adf_basic_letter_SEF(job, tray, cdm, device, udw, spice):
    try:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainApp.ScanDeviceService.setNumScanPages(1)
        tray.unload_media('all')

        default_tray = tray.get_default_source()
        if tray.is_size_supported('com.hp.ext.mediaSize.na_letter_8.5x11in.rotated', default_tray):
            tray.configure_tray(default_tray, 'com.hp.ext.mediaSize.na_letter_8.5x11in.rotated', 'stationery')
            tray.load_media(default_tray)

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().ui_copy_set_no_of_pages(3)
        spice.copy_ui().select_original_size("Letter_SEF")
        spice.copy_ui().go_to_paper_selection()
        # Eddington support tray main/alternate
        if default_tray == "main":
            spice.copy_ui().select_paper_tray_option("Tray Main")
        else:
            spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().select_media_size_option("Letter_SEF")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size= "com.hp.ext.mediaSize.na_letter_8.5x11in.rotated",
            paper_size = "com.hp.ext.mediaSize.na_letter_8.5x11in.rotated")
        time.sleep(20)

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size A4.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_a4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_a4
        +guid: 3281c829-826a-4718-ac84-e5e0be1594b7
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Widget=Settings & Copy=PaperSize & ADFMediaSize=A4 & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_a4(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "iso_a4_210x297mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'A4'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()

		
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Letter.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_letter
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_letter
        +guid: 03c9e04a-3804-4ebb-aaee-4f5f377050f4
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=Letter & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_letter(spice, job, udw, net, tray, cdm, media, scan_emulation):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_letter_8.5x11in", 'stationery')
        try:
            cdm.alerts.wait_for_alerts('sizeType',1)
            media.alert_action(category='sizeType', response='ok')
        except:
            logging.debug("SizeType Alert does not appear. Paper is already loaded in tray.")
        
        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Letter'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
        #Load media from ADF since ADF is default scan resource for Simulator
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Legal.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_menupage_paper_size_legal
    +test:
        +title: test_copy_ui_adf_menupage_paper_size_legal
        +guid: c86d8714-b84a-41b5-96de-c15e9d053bb0
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & ADFMediaSize=Legal & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_size_legal(spice, job, udw, net, tray, scan_emulation, print_emulation):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_legal_8.5x14in", 'stationery')
        
        if print_emulation.print_engine_platform == 'emulator':
            default_tray = 'Tray1' if 'tray-1' in default_tray else 'Tray2'
            print_emulation.tray.load(default_tray, MediaSize.Legal.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
            
        else:
            tray.load_media(default_tray)
            
        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Legal'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Executive (7.25x10.5 in.).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_widget_paper_size_executive
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_paper_size_executive
        +guid: 9b15eaf3-a3c0-48e8-98e2-b47cbef62777
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & FlatbedMediaSize=Executive & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_size_executive(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_executive_7.25x10.5in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Executive'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size B5 (JIS) (182x257 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_landingpage_paper_size_jis_b5
    +test:
        +title: test_copy_ui_adf_landingpage_paper_size_jis_b5
        +guid: 8a3adb05-038c-4d07-8436-3792dafcd143
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & ADFMediaSize=B5-JIS & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_size_jis_b5(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "jis_b5_182x257mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'jis_b5'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()      


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size B6 (JIS) (128x182 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_widget_paper_size_jis_b6
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_paper_size_jis_b6
        +guid: 742fc8d6-4b02-42e3-860a-51af5e7ebc13
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & FlatbedMediaSize=B6-JIS & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_size_jis_b6(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "jis_b6_128x182mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'B6 (JIS) (128x182 mm)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Statement (5.5x8.5 in.).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_landingpage_paper_size_statement
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_paper_size_statement
        +guid: bf270908-4d10-432e-8718-bd7f714b8854
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize  & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_size_statement(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_invoice_5.5x8.5in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Statement (8.5x5.5 in.)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size A5.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_flatbed_widget_paper_size_a5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_flatbed_widget_paper_size_a5
        +guid:f87595a1-8932-4bec-b6a3-f4e1bfbe790d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & FlatbedMediaSize=A5 & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_size_a5(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "iso_a5_148x210mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'A5'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size A6 (105x148 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_a6
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_a6
        +guid:b6417a34-3b35-4558-a142-c0144d995607
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=A6 & ScannerInput=AutomaticDocumentFeeder 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_a6(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "iso_a6_105x148mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'A6 (105x148 mm)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size 4x6 Inch.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_4x6
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_4x6
        +guid:a91f51e9-ec71-4fb6-bb2e-da7a3659e717
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize  & ScannerInput=Flatbed & MediaSizeSupported=na_index-4x6_4x6in
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_4x6(spice, job, udw, net, tray, cdm, media, scan_emulation, print_emulation): 
    job.bookmark_jobs()
    try:
        tray_name = tray.get_default_source()
        tray_id = None
        if tray_name == 'main':
            tray_id = MediaInputIds.Main.name
        elif tray_name == 'tray-1':
            tray_id = MediaInputIds.Tray1.name
        tray.configure_tray(tray_name, "na_index-4x6_4x6in", "stationery")
        print_emulation.tray.load(tray_id, MediaSize.FourXSix.name, MediaType.Plain.name, MediaOrientation.Portrait.name, TrayLevel.Full.name)
        try:
            cdm.alerts.wait_for_alerts('sizeType',1)
            media.alert_action(category='sizeType', response='ok')
        except:
            logging.debug("SizeType Alert does not appear. Paper is already loaded in tray1.")
        
        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': '4x6 in.'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()   


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size 5x8 Inch.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_5x8
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_5x8
        +guid:1c0b75be-f461-4c60-ae35-fe0a957b0dfb
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings  & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_5x8(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_index-5x8_5x8in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': '5x8 in.'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Oficio (216x340 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_oficio_8_5x13_4in
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_oficio_8_5x13_4in
        +guid:b0d686bf-a1ce-44a8-845a-58a90121047c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=Oficio8.5x13 & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_oficio_8_5x13_4in(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_oficio_8.5x13.4in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Oficio_8_5x13_4'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Envelope B5 (176x250 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_envelope_b5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_envelope_b5
        +guid:45fe1864-b110-4cd9-a29b-032f5c416233
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=B5-JIS & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_envelope_b5(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "iso_b5_176x250mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Envelope B5 (176x250 mm)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Envelope Monarch (3.9x7.5 in.).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_envelope_monarch
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_envelope_monarch
        +guid:b1195c1d-2bf8-4194-a1ea-0355854e2a1b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=EnvelopeMonarch  & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_envelope_monarch(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_monarch_3.875x7.5in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Envelope Monarch (3.9x7.5 in.)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Envelope C5 (162x229 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_envelope_c5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_envelope_c5
        +guid:b78b04f2-30c6-40ad-bc1f-ac52309e81cd
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=EnvelopeC5 & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_envelope_c5(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "iso_c5_162x229mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Envelope C5 (162x229 mm)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Envelope DL (110x220 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:400
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_envelope_dl
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_envelope_dl
        +guid:9f944bc8-990d-4e7e-bc47-4201482885a8
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & ScannerInput=Flatbed & MediaSizeSupported=iso_dl_110x220mm
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_envelope_dl(spice, job, udw, net, tray, cdm, media, scan_emulation, print_emulation): 
    job.bookmark_jobs()
    try:
        tray_name = tray.get_default_source()
        tray_id = None
        if tray_name == 'main':
            tray_id = MediaInputIds.Main.name
        elif tray_name == 'tray-1':
            tray_id = MediaInputIds.Tray1.name
        tray.configure_tray(tray_name, "iso_dl_110x220mm", "stationery")
        print_emulation.tray.load(tray_id, MediaSize.DLEnvelope.name, MediaType.Plain.name, MediaOrientation.Portrait.name, TrayLevel.Full.name)
        try:
            cdm.alerts.wait_for_alerts('sizeType',1)
            media.alert_action(category='sizeType', response='ok')
        except:
            logging.debug("SizeType Alert does not appear. Paper is already loaded in tray1.")

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Envelope DL (110x220 mm)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size 16K (184x260 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_16k_184x260mm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_16k_184x260mm
        +guid:745125da-08c9-4a43-8c37-e81dd01389c7
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=16K184x260mm & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_16k_184x260mm(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "om_16k_184x260mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': '16K (184x260 mm)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size 16K (195x270 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_16k_195x270mm
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_16k_195x270mm
        +guid:f8dc3841-9a14-4de0-a503-145283cf3d56
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=16K195x270mm & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_16k_195x270mm(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "om_16k_195x270mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': '16K (195x270 mm)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size 16K (197x273 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_16k_197x273mm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_16k_197x273mm
        +guid:3077bc52-72a8-4691-9596-c40aa67ba0b8
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=16K197x273mm & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_16k_197x273mm(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "roc_16k_7.75x10.75in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': '16K (197x273 mm)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size 100x150mm.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_10x15cm
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_10x15cm
        +guid:50463b31-dd30-4672-8619-83dc879319e2
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=10x15cm & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_10x15cm(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "om_small-photo_100x150mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': '100x150mm'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Double Postcard (JIS) (148x200 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_double_postcard_jis
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_double_postcard_jis
        +guid:0400fc8f-925b-46a7-8ec9-a3000bff3c94
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=DoubleJapanPostcardRotated & ScannerInput=AutomaticDocumentFeeder  & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_double_postcard_jis(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "jpn_oufuku_148x200mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Double Postcard (JIS) (148x200 mm)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Envelope #10 (4.1x9.5 in.).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_size_envelope_10
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_size_envelope_10
        +guid:092e9ce0-8871-49c1-b7d1-1e06089f2b1d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=Envelope-10 & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_size_envelope_10(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_number-10_4.125x9.5in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Envelope #10 (4.1x9.5 in.)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Oficio (8.5x13 in.).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_paper_size_oficio_8_5x13in
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_size_oficio_8_5x13in
        +guid:a051b4dc-c5ce-45f3-b327-989d4781addc
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & Widget=Settings & ADFMediaSize=Oficio8.5x13 & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_size_oficio_8_5x13in(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "na_foolscap_8.5x13in", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'oficio_8_5x13'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with paper size Postcard (JIS) (100x148 mm).
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_menupage_paper_size_hagaki
    +test:
        +title: test_copy_ui_flatbed_menupage_paper_size_hagaki
        +guid:82fcfb66-0947-4905-ac72-6d635250013c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & FlatbedMediaSize=JapanesePostcard & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_paper_size_hagaki(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, "jpn_hagaki_100x148mm", 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Postcard (JIS) (100x148 mm)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()

