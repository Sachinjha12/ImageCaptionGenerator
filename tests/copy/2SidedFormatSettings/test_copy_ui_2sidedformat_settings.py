
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with 2-Sided Pages Flip Up as On.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:400
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_2sidedformat_flip_on
    +test:
        +title:test_copy_ui_adf_landingpage_2sidedformat_flip_on
        +guid:89650fd4-e2ec-4d7f-afa8-77af10507e21
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2SidedFormatFlip & Copy=2Sided1To2
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_2sidedformat_flip_on(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'sides': '2_2_sided',
            '2sidedformat_flip': 'on'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        spice.copy_ui().enable_duplex_supported(cdm,udw)
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with 2-Sided Pages Flip Up as Off.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_menupage_2sidedformat_flip_off
    +test:
        +title:test_copy_ui_adf_menupage_2sidedformat_flip_off
        +guid:d31f4bea-64d9-4e11-bcd4-49fa54c36dc9
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2SidedFormatFlip & Copy=2Sided2To2
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_2sidedformat_flip_off(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'sides': '2_2_sided',
            '2sidedformat_flip': 'off'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        spice.copy_ui().enable_duplex_supported(cdm,udw)
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
