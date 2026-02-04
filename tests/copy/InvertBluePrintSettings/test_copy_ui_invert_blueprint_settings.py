"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with invert blueprint settings as true
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name:test_copy_ui_mdf_landingpage_invert_blueprint_on
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_mdf_landingpage_invert_blueprint_on
        +guid:c50eee70-e2d0-45d7-83e9-2bfc06d388a7
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanOriginalPaperType=Blueprint & Copy=BluePrint & DeviceClass=MFP
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_landingpage_invert_blueprint_on(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'originalPaperType': 'blueprint',
            'blueprint_invert': True
            }
        loadmedia = 'MDF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with invert blueprint settings as false
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_mdf_menupage_invert_blueprint_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_mdf_menupage_invert_blueprint_off
        +guid:d374c0a0-3dee-4f30-9f35-4af5615d4cea
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanOriginalPaperType=Blueprint & Copy=BluePrint & DeviceClass=MFP
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menupage_invert_blueprint_off(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'originalPaperType': 'blueprint',
            'blueprint_invert': False
            }
        loadmedia = 'MDF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
