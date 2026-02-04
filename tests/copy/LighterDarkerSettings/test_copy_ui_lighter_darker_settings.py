import logging
import pytest
from dunetuf.copy.copy import *


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perfrom Copy job with lighter darker settings as 1
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_lighter_darker_leastvalue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_lighter_darker_leastvalue
        +guid: adc737a5-3b6f-4768-96ee-ef23de3177df
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanSettings=LighterDarker

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.disable_autouse
def test_copy_ui_adf_landingpage_lighter_darker_leastvalue(cdm, spice, job, udw, net, scan_emulation):
    try:
        job.cancel_active_jobs()
        job.wait_for_no_active_jobs()
        job.clear_joblog()
        job.bookmark_jobs()

        copy_job_app = spice.copy_ui()
        options = {
            'lighter_darker': '1'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perfrom Copy job with lighter darker settings as 9
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_widget_lighter_darker_maxvalue
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_lighter_darker_maxvalue
        +guid: 1a5774e0-3da0-48a7-bdd7-e9437a574c98
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanSettings=LighterDarker & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_lighter_darker_maxvalue(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'lighter_darker': '9'
            }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


