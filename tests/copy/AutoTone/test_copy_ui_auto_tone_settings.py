import logging
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting auto tone
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-191053
    +timeout:300
    +asset: Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +name: test_copy_ui_set_auto_tone_on_and_change_level
    +test:
        +title: test_copy_ui_set_auto_tone_on_and_change_level
        +guid: e46987b5-299b-424e-a423-a60d0c990573
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=AutomaticTone
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_set_auto_tone_on_and_change_level(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'auto_tone': True,
            'auto_tone_level': 5
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
