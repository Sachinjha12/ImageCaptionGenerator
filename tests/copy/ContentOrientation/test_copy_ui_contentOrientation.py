from logging import exception
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate content orientation comboBox in Scan Settings
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-
    +timeout:300
    +asset: Copy
    +test_framework: TUF
    +name: test_copy_ui_validate_content_orientation_setting
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test: 
        +title: test_copy_ui_validate_content_orientation_setting
        +guid:b59fac7e-00cd-4758-8f09-2465effcba1a
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & CopyOutputSize=Orientation
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_content_orientation_setting(job, net, udw, spice, cdm):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_portrait_option)
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().back_to_landing_view()

        spice.copy_ui().start_copy()

        Copy(cdm, udw).validate_settings_used_in_copy(
            orientation = "landscape"
        )

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()