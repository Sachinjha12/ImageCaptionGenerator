import logging
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting auto paper color removal
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-191053
    +timeout:300
    +asset: Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +name: test_copy_ui_set_auto_paper_color_removal_on_and_change_level
    +test:
        +title: test_copy_ui_set_auto_paper_color_removal_on_and_change_level
        +guid: 855912a6-da7e-490f-8c6e-be08e2f1c31c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=AutoPaperColorRemoval
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_set_auto_paper_color_removal_on_and_change_level(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'auto_paper_color_removal': True,
            'auto_paper_color_removal_level': 5
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
