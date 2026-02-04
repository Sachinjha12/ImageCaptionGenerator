from time import sleep
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test to validate copy cancel job when user presses cancel button
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-144459
    +timeout:120
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_validate_copy_cancel_job_cancel_button
    +test:
        +title: test_copy_ui_validate_copy_cancel_job_cancel_button
        +guid:cd169969-8a5b-4176-8b62-50a50ae6865d
        +dut:
            +type:Engine, Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ConsumableSupport=Toner
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_copy_cancel_job_cancel_button(job, udw, spice, net, cdm, configuration):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().start_copy()
        current_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_button)
        current_button.mouse_click()
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Canceling')

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job was canceled
        Job.verify_job_status_udw(udw, copy_job_id, "CANCELING", "COMPLETED")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut1.
        csc.delete_shortcut(shortcut_id)
