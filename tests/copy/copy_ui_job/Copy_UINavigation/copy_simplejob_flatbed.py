"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform simple  copy job with flatbed
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:240
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_simple_job_flatbed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_simple_job_flatbed
        +guid: 48b3cc8f-a8b0-4b70-882b-f0e9d41b32ba
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_simple_job_flatbed(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()

        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        udw.mainApp.ScanMedia.loadMedia("ADF")

