import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.copy.copy import *

max_no_copies = 999
min_no_copies = 1

payload = {
            'src': {
                'scan': {
                    'colorMode':'color',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                }
            }
        }

def check_for_reprint_button_for_given_job(spice, job, cdm,job_id):
    
    job_cdm = job.get_job_from_history_by_id(job_id)
    assert job_cdm["jobId"] == job_id
    spice.job_ui.goto_job(job_id)
    button_found = False
    try:
        spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_reprint_btn)
        button_found = True
    except TimeoutError:
        logging.info("reprintButton not present")
    return button_found

def delete_content_of_given_job(spice, job, cdm, job_id):
    job_cdm = job.get_job_from_history_by_id(job_id)
    assert job_cdm["jobId"] == job_id
    job_ui = spice.wait_for("#mainPanelArea #JOB_" + job_id)
    job_ui.mouse_click()
    spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_deletejob_btn).mouse_click()
    spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_deletejob_confirm_btn).mouse_click()

def enter_reprint_screen(spice):
    reprint_button = spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_reprint_btn)
    reprint_button.mouse_click()

def go_back_to_jobque_detail_panel(spice):
    cancel_btn = spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_job_reprint_screen_cancel_btn)
    cancel_btn.mouse_click()

def start_reprint_job_and_verify_it_is_printed(spice, job, cdm, udw, net, configuration, numCopies):
    # Set number of copies
    time.sleep(2)   # waiting for Constraints get call to resolve
    reprint_spin = spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_job_reprint_screen_spin_box)
    reprint_spin["value"] = numCopies
    reprint_button_confirm = spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_job_reprint_screen_reprint_btn)
    reprint_button_confirm.mouse_click()

    # Check for reprint scanning toast/Modal will not appear
    #spice.copy_ui().check_job_toast_or_modal_not_appear(net, configuration, message='Scanning')
    Copy(cdm, udw).validate_settings_used_in_copy(number_of_copies=numCopies)
    # Get job
    queue = job.get_job_queue()
    if len(queue)>0:
        # Get last job from job_queue
        queue_job_id = queue[-1]["jobId"]
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, timeout=720)  # waiting for printing copies
    else:
        # Get last job from job_history
        time.sleep(4)
        queue = job.get_job_history()
        assert len(queue)>0 ,"I can't get printed job"
        queue_job_id = queue[-1]["jobId"]
    
    # wait for job in  "History" section
    spice.job_ui.goto_job(queue_job_id)
    time.sleep(3)
    assert spice.wait_for(CopyAppWorkflowObjectIds.jobs_app_reprint_btn, timeout=60)
    
    # Check by CDM that the job is printed
    job_cdm = job.get_job_from_history_by_id(queue_job_id)
    assert job_cdm["jobId"] == queue_job_id

def perform_copy_job(spice, cdm, udw, job ,net,configuration):
    #currently reprint implemented only in beam and jupiter
    udw.mainApp.ScanMedia.loadMedia("MDF")
    if configuration.productname in ["beam/beamsfp_power", "beam/beammfp_power"]:
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()
        spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()
    elif configuration.productname in ["jupiter"]:
        spice.copy_ui().goto_copyapp_at_home_screen() # TODO change it to goto_copy
        spice.copy_ui().start_copy()
        time.sleep(8)
        spice.wait_for(CopyAppWorkflowObjectIds.done_button).mouse_click()
    queue = job.get_job_queue()
    assert len(queue) >0
    job_id = queue[-1]["jobId"]
    return job_id