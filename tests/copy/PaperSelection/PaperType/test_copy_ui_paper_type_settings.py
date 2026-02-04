import pytest
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.emulation.print.tray import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as matte 90
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
    +name: test_copy_ui_adf_widget_paper_type_matte_90
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_type_matte_90
        +guid: cb83e10f-940c-42b3-be21-d92a67929dd5
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & Widget=Settings & MediaType=HPLaserJet90g & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_type_matte_90(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.matte-90gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Matte (90g)'
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
    +purpose: Perform copy job with setting paper type as envelope
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
    +name: test_copy_ui_adf_menupage_paper_type_envelope
    +test:
        +title: test_copy_ui_adf_menupage_paper_type_envelope
        +guid: 24b5cb58-f104-4a9d-8785-814aa3b21737
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Envelope & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_envelope(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('ADF',10)
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'envelope')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Envelope'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia=None,copy_path=copy_path,copy_settings=options, udw=udw, net=net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as matte 105gsm
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
    +name: test_copy_ui_flatbed_landingpage_paper_type_matte_105
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_matte_105
        +guid: c6de91c9-3ee2-4f98-a9d1-570166b6f9ee
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPColorLaserMatte105g & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_matte_105(setup_teardown_with_copy_job, spice, job, udw, net, tray, scan_emulation,print_emulation):
    job.bookmark_jobs()
    tray.reset_trays()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.matte-105gsm')
        if print_emulation.print_engine_platform == 'emulator':
            default = 'Tray1' if 'tray-1' in default else 'Tray2'
            print_emulation.tray.load(default, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
            
        else:
            tray.load_media(default)
        #tray.load_media(default)
        
        copy_job_app = spice.copy_ui()
        paper_type = 'HP Matte (105g)'

        copy_job_app.goto_copy_from_copyapp_at_home_screen()
        scan_emulation.media.load_media('Flatbed')
        copy_job_app.goto_copy_options_list()
        copy_job_app.go_to_paper_selection()
        copy_job_app.select_paper_type_option(paper_type)
        copy_job_app.check_paper_type_value(paper_type, net)
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as HP Matte (120g)
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
    +name: test_copy_ui_adf_widget_paper_type_matte_120
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_type_matte_120
        +guid: 918f9c3e-6fea-4419-8548-c51afbac0cac
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Copy=PaperType & MediaType=HPPremiumChoiceMatte120g & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_type_matte_120(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.matte-120gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Matte (120g)'
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
    +purpose: Perform copy job with setting paper type as matte 105gsm
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
    +name: test_copy_ui_flatbed_landingpage_paper_type_brochure_matte_150gsm
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_brochure_matte_150gsm
        +guid: adf81ab0-f37d-4a18-8bae-a080d37e6982
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPBrochureMatte150g & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_brochure_matte_150gsm(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.matte-160gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Matte (150g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as matte 105gsm
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
    +name: test_copy_ui_flatbed_menupage_paper_type_hp_glossy_150gsm
    +test:
        +title: test_copy_ui_flatbed_menupage_paper_type_hp_glossy_150gsm
        +guid: 51bd732d-78e2-402e-98a0-8488c648f841
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPBrochureGlossy150g & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_paper_type_hp_glossy_150gsm(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.glossy-160gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Glossy (150g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Opaque Film
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
    +name:test_copy_ui_adf_widget_paper_type_opaque_film
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_widget_paper_type_opaque_film
        +guid:0d8c0bfd-a381-4a23-bc71-8c32ef467d5a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Copy=PaperType & MediaType=OpaqueFilm & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_type_opaque_film(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'com.hp.film-opaque')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Opaque Film'
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
    +purpose: Perform copy job with setting paper type as Color Transparency
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
    +name:test_copy_ui_flatbed_landingpage_paper_type_color_transparency
    +test:
        +title:test_copy_ui_flatbed_landingpage_paper_type_color_transparency
        +guid:ac5e10a7-0b77-4b47-8ab3-ef42b2721ab8
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Transparency & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_color_transparency(spice, job, udw, net, tray, scan_emulation, print_emulation, media, cdm):
    job.bookmark_jobs()
    try:
        tray1 = MediaInputIds.Tray1.name
        print_emulation.tray.empty(tray1)
        print_emulation.tray.load(tray1, MediaSize.Letter.name, MediaType.Transparency.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        tray.configure_tray("tray-1", 'na_letter_8.5x11in', 'transparency')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Transparency'
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
		# For Simulator default scan resouce is ADF, then need to reload ADF end of testing 
        scan_emulation.media.load_media('ADF')
		
		
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Heavy Rough
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
    +name:test_copy_ui_adf_menupage_paper_type_heavy_rough
    +test:
        +title:test_copy_ui_adf_menupage_paper_type_heavy_rough
        +guid:2adece88-3557-4be0-9c70-3725f6ea968a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Rough & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_heavy_rough(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('ADF',10)
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'com.hp.heavy-rough')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Heavy Rough'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia=None, copy_path=copy_path, copy_settings=options, udw=udw, net=net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
		
		
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Rough
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
    +name:test_copy_ui_adf_widget_paper_type_rough
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_widget_paper_type_rough
        +guid:99029b35-2627-4620-b152-816fbfe521f1
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Copy=PaperType & MediaType=Rough & ScannerInput=AutomaticDocumentFeeder  & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_type_rough(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'com.hp.rough')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Rough'
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
    +purpose: Perform copy job with setting paper type as Recycled.
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
    +name:test_copy_ui_flatbed_landingpage_paper_type_recycled
    +test:
        +title:test_copy_ui_flatbed_landingpage_paper_type_recycled
        +guid:6a6db2f7-8713-4437-9097-10e9525b7f57
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Recycled & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_recycled(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default_tray = tray.get_default_source()
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'com.hp.recycled')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Recycled'
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
		# For Simulator default scan resouce is ADF, then need to reload ADF end of testing 
        udw.mainApp.ScanMedia.loadMedia("ADF")



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as plain
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
    +name: test_copy_ui_adf_widget_paper_type_plain
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_type_plain
        +guid: 3b3e6fce-dcca-4e97-a60a-976ca88f0ad7
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Copy=PaperType & MediaType=Plain & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_type_plain(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Plain'
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
    +purpose: Perform copy job with setting paper type as HP Matte (200g)
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
    +name: test_copy_ui_flatbed_landingpage_paper_type_matte_200gsm
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_matte_200gsm
        +guid: 9dc6d10f-902d-4b33-910d-6759eefe26c8
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPMatte200g & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_matte_200gsm(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.matte-200gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Matte (200g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as HP Glossy (120g)
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
    +name: test_copy_ui_adf_menupage_paper_type_glossy_120gsm
    +test:
        +title: test_copy_ui_adf_menupage_paper_type_glossy_120gsm
        +guid: 0dfeea32-a889-4c27-8959-8466822f5266
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPPremiumPresentationGlossy120g & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_glossy_120gsm(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.glossy-130gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Glossy (120g)'
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
    +purpose: Perform copy job with setting paper type as HP Glossy (200g)
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
    +name: test_copy_ui_flatbed_widget_paper_type_glossy_200gsm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_paper_type_glossy_200gsm
        +guid: 520fb2ba-7b69-4ce2-b274-675dc190ea18
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Copy=PaperType & MediaType=HPBrochureGlossy200g & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_type_glossy_200gsm(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.glossy-220gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Glossy (200g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as HP Tri-Fold Glossy (150g)
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
    +name: test_copy_ui_adf_landingpage_paper_type_hp_tri_fold_glossy_150gsm
    +test:
        +title: test_copy_ui_adf_landingpage_paper_type_hp_tri_fold_glossy_150gsm
        +guid: 081c72f0-99ec-4623-917b-ec63ee1c8df4
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPTri-foldBrochureGlossy150g & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_type_hp_tri_fold_glossy_150gsm(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp-trifold-brochure-glossy-150gsm')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP Tri-Fold Glossy (150g)'
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
    +purpose: Perform copy job with setting paper type as Light (60-74g)
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
    +name: test_copy_ui_flatbed_menupage_paper_type_stationery_lightweight
    +test:
        +title: test_copy_ui_flatbed_menupage_paper_type_stationery_lightweight
        +guid: a2b6fc12-19a0-4262-ba2f-b2542a15141c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Plain & ScannerInput=Flatbed & Copy=2PagesPerSheet
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_paper_type_stationery_lightweight(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-lightweight')

        # Clear all alerts/prompts in homescreen
        spice.cleanSystemEventAndWaitHomeScreen()

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Light (60-74g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Intermediate (85-95g)
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
    +name: test_copy_ui_adf_widget_paper_type_intermediate
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_paper_type_intermediate
        +guid: 5f0aedb2-0eb4-4aee-8a7e-0f3b5e80e188
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Widget=Settings & Copy=PaperType & MediaType=Intermediate85-95g & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_paper_type_intermediate(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.intermediate')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Intermediate (85-95g)'
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
    +purpose: Perform copy job with setting paper type as Mid-Weight (96-110g)
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
    +name: test_copy_ui_adf_menupage_paper_type_midweight
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_menupage_paper_type_midweight
        +guid: e5bb5484-2580-4e2e-8f86-a29843bdaff1
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=PlainPaper-Thick & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_midweight(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.midweight')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Mid-Weight (96-110g)'
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
    +purpose: Perform copy job with setting paper type as Heavy (111-130g)
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
    +name: test_copy_ui_flatbed_landingpage_paper_type_stationery_heavyweight
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_stationery_heavyweight
        +guid: 506bda5f-2bac-4ed4-814c-723b64c21fc8
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=PlainPaper-Thick & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_stationery_heavyweight(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-heavyweight')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Heavy (111-130g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Extra Heavy (131-175g)
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
    +name: test_copy_ui_flatbed_widget_paper_type_extra_heavy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_paper_type_extra_heavy
        +guid: 0019788e-cb54-4b6c-aed6-45e3ab36ab36
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=ExtraHeavy131-175g & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_type_extra_heavy(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.extra-heavy')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Extra Heavy (131-175g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as cardstock
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
    +name: test_copy_ui_adf_menupage_paper_type_cardstock
    +test:
        +title: test_copy_ui_adf_menupage_paper_type_cardstock
        +guid: 5dde85ea-68f5-40b3-9554-cf28b198f3e2
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Cardstock & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_cardstock(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'cardstock')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Cardstock (176-220g)'
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
    +purpose: Perform copy job with setting paper type as Heavy Glossy (111-130g)
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
    +name: test_copy_ui_adf_landingpage_paper_type_heavy_glossy
    +test:
        +title: test_copy_ui_adf_landingpage_paper_type_heavy_glossy
        +guid: eb8a4ca0-6509-4044-b790-36c6789cf623
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HeavyGlossy111-130g & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_type_heavy_glossy(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.heavy-glossy')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Heavy Glossy (111-130g)'
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
    +purpose: Perform copy job with setting paper type as HP EcoFFICIENT
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
    +name: test_copy_ui_flatbed_landingpage_paper_type_hp_ecofficient
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_hp_ecofficient
        +guid: c8f58849-0ce0-4035-a56c-113de868620e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=HPEcoFFICIENT & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_hp_ecofficient(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.EcoSMARTLite')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'HP EcoFFICIENT'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as any
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
    +name: test_copy_ui_adf_menupage_paper_type_any
    +test:
        +title: test_copy_ui_adf_menupage_paper_type_any
        +guid: 79fa3f81-acd0-405e-ae5c-89fc86d13c7c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=AnyType & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_any(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'any')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Any Type'
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
    +purpose: Perform copy job with setting paper type as Extra Heavy Glossy (131-175g)
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
    +name: test_copy_ui_flatbed_widget_paper_type_extra_heavy_gloss
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_paper_type_extra_heavy_gloss
        +guid: 70bcd0d9-b54e-44df-88a7-e6449610e547
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=ExtraHeavyGlossy131-175g & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_type_extra_heavy_gloss(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.extra-heavy-gloss')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Extra Heavy Glossy (131-175g)'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Cardstock Glossy (176-220g)
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
    +name: test_copy_ui_adf_landingpage_paper_type_cardstock_glossy
    +test:
        +title: test_copy_ui_adf_landingpage_paper_type_cardstock_glossy
        +guid: 0b13668e-a1ea-48e2-978b-36e34798cfba
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=CardGlossy176-220g & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_type_cardstock_glossy(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.cardstock-glossy')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Cardstock Glossy'
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
    +purpose: Perform copy job with setting paper type as Bond
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
    +name:test_copy_ui_flatbed_widget_paper_type_bond
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_flatbed_widget_paper_type_bond
        +guid:766a956b-8ca6-443d-be73-8e410c56669b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Bond & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_type_bond(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-bond')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Bond'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        # For Simulator default scan resouce is ADF, then need to reload ADF end of testing 
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Colored
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
    +name:test_copy_ui_adf_landingpage_paper_type_colored
    +test:
        +title:test_copy_ui_adf_landingpage_paper_type_colored
        +guid:fbbe4dfd-336b-4b94-85d0-7658e966b14f
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=ColouredPaper & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_type_colored(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-colored')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Colored'
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
    +purpose: Perform copy job with setting paper type as Preprinted
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
    +name:test_copy_ui_flatbed_widget_paper_type_preprinted
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_flatbed_widget_paper_type_preprinted
        +guid:ef5aa206-30c4-4def-9b17-4e1a3f8db3ef
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Preprinted & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_type_preprinted(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-preprinted')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Preprinted'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        # For Simulator default scan resouce is ADF, then need to reload ADF end of testing 
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as Prepunched
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
    +name:test_copy_ui_adf_landingpage_paper_type_prepunched
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_paper_type_prepunched  
        +guid:a99239f4-a780-42cd-a19a-1678ca855bc4
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Prepunched & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_type_prepunched(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-prepunched')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Prepunched'
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
    +purpose: Perform copy job with setting paper type as Letterhead
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
    +name:test_copy_ui_flatbed_widget_paper_type_letterhead
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_flatbed_widget_paper_type_letterhead
        +guid:274ca5a7-2eea-4a40-afda-aafaad1ee1bd
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Letterhead & ScannerInput=Flatbed & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_paper_type_letterhead(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'stationery-letterhead')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Letterhead'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        # For Simulator default scan resouce is ADF, then need to reload ADF end of testing 
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting paper type as labels
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
    +name:test_copy_ui_adf_landingpage_paper_type_labels
    +test:
        +title:test_copy_ui_adf_landingpage_paper_type_labels
        +guid:050e5ec0-5643-4e0c-b666-7acab6253e34
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & MediaType=Labels & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_paper_type_labels(spice, job, udw, net, tray, scan_emulation, print_emulation):
    # wait for no active jobs and then perform copy
    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    job.clear_joblog()

    job.bookmark_jobs()
    tray.reset_trays()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'labels')
        
        if print_emulation.print_engine_platform == 'emulator':
            default = 'Tray1' if 'tray-1' in default else 'Tray2'
            print_emulation.tray.load(default, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
            
        else:
            tray.load_media(default)

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Labels'
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
    +purpose: Perform copy job with setting paper type as Heavy Envelope
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
    +name: test_copy_ui_adf_menupage_paper_type_envelope_heavyweight
    +test:
        +title: test_copy_ui_adf_menupage_paper_type_envelope_heavyweight
        +guid: 10a4b74c-45ad-4188-9042-10b67c32879e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperType &MediaType=HeavyEnvelope & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_paper_type_envelope_heavyweight(spice, job, udw, net, tray, scan_emulation):
    job.bookmark_jobs()
    try:
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'envelope-heavyweight')

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_type': 'Heavy Envelope'
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
