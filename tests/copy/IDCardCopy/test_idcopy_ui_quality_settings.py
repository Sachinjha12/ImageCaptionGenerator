
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform id copy job with Quality as Best
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatbed_landingpage_quality_best
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_landingpage_quality_best
        +guid: 93d79ffe-3247-4cea-8e91-93f50038940c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=IDCopy & ScannerInput=Flatbed & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_landingpage_quality_best(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'quality': 'Best'
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform id copy job with Quality as Standard
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatbed_menupage_quality_standard
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_menupage_quality_standard
        +guid: afe79320-45c0-45e6-8156-c78f417d9913
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=IDCopy & ScannerInput=Flatbed & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_menupage_quality_standard(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'quality': 'Standard'
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardMenuPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform id copy job with Quality as Draft
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-23144
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_flatbed_landingpage_quality_draft
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_landingpage_quality_draft
        +guid: 84f6730b-7be5-4774-8571-72e5e08dc6fa
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=Quality & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_landingpage_quality_draft(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'quality': 'Draft'
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.wait_ready()
