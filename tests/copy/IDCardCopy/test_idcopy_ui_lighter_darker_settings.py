
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perfrom id copy job with lighter darker settings as 1
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatbed_menupage_lighter_darker_leastvalue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_menupage_lighter_darker_leastvalue
        +guid: f1a99bc4-932d-495d-9303-1090c61c242d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=IDCopy & ScannerInput=Flatbed & ScanSettings=LighterDarker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_menupage_lighter_darker_leastvalue(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'lighter_darker': '1'
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardMenuPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perfrom id copy job with lighter darker settings as 9
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatbed_landingpage_lighter_darker_maxvalue
    +test:
        +title: test_idcopy_ui_flatbed_landingpage_lighter_darker_maxvalue
        +guid: b8ebe284-2548-4587-8434-43e609b4b5c5
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & ScanSettings=LighterDarker & Copy=IDCopy
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_landingpage_lighter_darker_maxvalue(scan_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.unload_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'lighter_darker': '9'
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
