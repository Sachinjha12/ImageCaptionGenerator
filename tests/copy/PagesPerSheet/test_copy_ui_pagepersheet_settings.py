
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Pages per Sheet as 1.
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
    +name: test_copy_ui_adf_widget_pagepersheet_1
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_pagepersheet_1
        +guid:9a569586-d49c-4786-86db-94d79b07b18c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=2PagesPerSheet & ScannerInput=AutomaticDocumentFeeder & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_pagepersheet_1(spice, job, udw, net, tray):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'pagesPerSheet': '1'
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Pages per Sheet as 2.
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
    +name: test_copy_ui_flatbed_landingpage_pagepersheet_2
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_landingpage_pagepersheet_2
        +guid:670290b1-be2b-42cc-becb-3b76475214d4
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=2PagesPerSheet & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_pagepersheet_2(spice, job, udw, net, tray, scan_emulation): 
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'pagesPerSheet': '2'
        }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation = scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with Pages per Sheet as 2 through ADF.
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
    +name: test_copy_ui_adf_widget_pagepersheet_2
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_widget_pagepersheet_2
        +guid:b46e8a5e-76ce-4eb2-83d6-fe95fe5e1f05
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=2PagesPerSheet & ScannerInput=AutomaticDocumentFeeder & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_pagepersheet_2(spice, job, udw, net, tray): 
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'pagesPerSheet': '2'
        }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
