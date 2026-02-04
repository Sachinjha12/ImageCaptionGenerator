import logging
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting background color removal as on
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_mdf_menupage_background_noise_removal_on
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_mdf_menupage_background_noise_removal_on
        +guid: 288f2214-7c67-4fd5-a092-e8500ee85f15
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanSettings=BackgroundNoiseRemoval
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menupage_background_noise_removal_on(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'background_noise_removal': True
            }
        loadmedia = 'MDF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting background color removal as off
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_mdf_landingpage_background_noise_removal_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_mdf_landingpage_background_noise_removal_off
        +guid: 01d0400a-eb5d-4544-9c76-aef9428b849c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanSettings=BackgroundNoiseRemoval
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_landingpage_background_noise_removal_off(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'background_noise_removal': False
            }
        loadmedia = 'MDF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

