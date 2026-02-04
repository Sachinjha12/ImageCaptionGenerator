
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Trays as Tray1 from ADF.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_tray1
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_tray1
        +guid:05ac1b68-eaab-459a-80a0-2f818e626d3d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperTray & Widget=Settings & MediaInputInstalled=Tray1 & ScannerInput=AutomaticDocumentFeeder & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_tray1(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_tray': 'Tray 1'
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
    +purpose: Perform copy job with Trays as Tray2 from Flatbed.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_tray2
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_landingpage_tray2
        +guid:ea4a15a5-82bb-4f6a-aaf3-f594b053b22b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperTray & MediaInputInstalled=Tray2 & ScannerInput=Flatbed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_tray2(scan_emulation, spice, job, udw, net, tray, configuration): 
    scan_emulation.media.unload_media(media_id='ADF')
    job.bookmark_jobs()
    try:

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_tray': 'Tray 2'
            }
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, familyname = configuration.familyname, scan_emulation = scan_emulation)    
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 
		

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Trays as Tray3 from ADF.
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
    +name: test_copy_ui_adf_menupage_tray3
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_menupage_tray3
        +guid:34db3367-257e-463f-88a9-9e569ccfb51b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperTray & MediaInputInstalled=Tray3 & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_tray3(scan_emulation, spice, job, udw, net, tray): 
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_tray': 'Tray 3'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation = scan_emulation)   
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Trays as Tray4 from ADF.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-145027
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_menupage_tray4
    +test:
        +title: test_copy_ui_adf_menupage_tray4
        +guid:54765f36-6791-4b7a-86e9-6a3951b4624d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperTray & MediaInputInstalled=Tray4 & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_tray4(scan_emulation, spice, job, udw, net, tray): 
    job.bookmark_jobs()
    scan_emulation.media.load_media(media_id='ADF')
    try:

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_tray': 'Tray 4'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Trays as Tray5 from ADF.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-145027
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_menupage_tray5
    +test:
        +title: test_copy_ui_adf_menupage_tray5
        +guid:62545325-dbd1-4b39-ae96-f94748614243
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperTray & MediaInputInstalled=Tray5 & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_tray5(scan_emulation, spice, job, udw, net, tray): 
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_tray': 'Tray 5'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Trays as Tray6 from ADF.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-145027
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_menupage_tray6
    +test:
        +title: test_copy_ui_adf_menupage_tray6
        +guid:a02a8661-39c8-44f1-81ed-bc336ad451aa
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperTray & MediaInputInstalled=Tray6 & ScannerInput=AutomaticDocumentFeeder 
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_tray6(scan_emulation, spice, job, udw, net, tray): 
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:

        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_tray': 'Tray 6'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 
