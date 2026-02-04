import logging
import pytest
from time import sleep,time

from dunetuf.job.job import Job
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from test_copy_helpers import wait_for_print_menu_text,wait_for_print_to_complete

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check if Beam's simulated scanner allows copy.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-179188
    +timeout:300
    +asset:UI
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_with_simulated_scanner_beam
    +test:
        +title:test_copy_with_simulated_scanner_beam
        +guid:6c9d336a-e69a-4c2f-81fe-74be9a17e947
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & ScanEngine=LFPCandela
    +delivery_team:LFP
    +feature_team:LFP_SOHO&SMB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_with_simulated_scanner_beam(copy_screen_setup, spice, net, job, printjob, udw, locale: str = "en-US"):
    # setup for this test
    udw.mainApp.execute("FormatterToScanner PUB_setScanningDelay 3 15000") # 15s delay scanning

    last_job_id = job.get_last_job_id()

    # start copy
    spice.copy_ui().copy_button_present(spice)
    spice.copy_ui().press_copy_button(spice)
    sleep(3)

    # first part: 'Scanning...'
    wait_for_print_menu_text("cStringEllipsis", spice, net, locale, "cScanning")

    # wait for send
    send_scan_btn = spice.wait_for(MenuAppWorkflowObjectIds.send_scan_copy_button, timeout=20)
    send_scan_btn.mouse_click() # we're done
    
    # second part: 'Copying...'
    wait_for_print_menu_text("cStringEllipsis", spice, net, locale, "cCopying")

    # complete copy
    finish_btn, _ = wait_for_print_to_complete("cCopyCompleteMessage", spice, net, locale)
    finish_btn.mouse_click()

    # wait for the new job completion and get job_id
    job_id = job.print_completed_job(last_job_id)
    assert job_id != last_job_id, "The new job has not been generated"

    # get status job
    printjob.wait_for_job_completion(job_id)
    status_job = job.get_status_job(job_id)

    # assert - check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # back to the 'copy' screen?
    spice.copy_ui().copy_button_present(spice)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check if Beam's simulated scanner allows cancel copy while scanning.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-179188
    +timeout:300
    +asset:UI
    +test_framework:TUF
    +test_classification:System
    +name:test_cancel_copy_while_scanning_with_simulated_scanner_beam
    +test:
        +title:test_cancel_copy_while_scanning_with_simulated_scanner_beam
        +guid:20680917-7be5-4f7e-9fd1-f1366ba72e2d
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & ScanEngine=LFPCandela
    +delivery_team:LFP
    +feature_team:LFP_SOHO&SMB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_cancel_copy_while_scanning_with_simulated_scanner_beam(copy_screen_setup, spice, net, udw, locale: str = "en-US"):
    # setup for this test
    udw.mainApp.execute("FormatterToScanner PUB_setScanningDelay 3 15000") # 15s delay scanning
    udw.mainApp.execute("FormatterToScanner PUB_setScanningDelay 4 5000")  #  5s delay cancelling

    # start copy
    spice.copy_ui().copy_button_present(spice)
    spice.copy_ui().press_copy_button(spice)

    # cancel scan
    logging.info("Waiting some time before canceling scan...")
    sleep(1)
    logging.info("Canceling scan...")
    spice.wait_for(MenuAppWorkflowObjectIds.scan_progress_cancel).mouse_click()
    logging.info("Scan cancel petition sent, validation required")
    
    # confirm cancel
    sleep(1)
    logging.info("Sending OK to scan cancel petition...")
    spice.wait_for(MenuAppWorkflowObjectIds.scan_progress_cancel_confirm).mouse_click()
    logging.info("Scan should be canceled now")

    # complete copy
    finish_btn, _ = wait_for_print_to_complete("cCopyCanceledMessage", spice, net, locale)
    finish_btn.mouse_click()

    # back to the 'copy' screen?
    spice.copy_ui().copy_button_present(spice)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check if Beam's simulated scanner allows cancel copy while printing.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-195197
    +timeout:300
    +asset:UI
    +test_framework:TUF
    +test_classification:System
    +name:test_cancel_copy_while_printing_with_simulated_scanner_beam
    +test:
        +title:test_cancel_copy_while_printing_with_simulated_scanner_beam
        +guid:0d242523-f465-492b-b4cc-a7a5514aaeb1
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & ScanEngine=LFPCandela
    +delivery_team:LFP
    +feature_team:LFP_SOHO&SMB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_cancel_copy_while_printing_with_simulated_scanner_beam(copy_screen_slow_printing_setup, job, spice, net, locale: str = "en-US"):
    # start copy
    spice.copy_ui().copy_button_present(spice)
    spice.copy_ui().press_copy_button(spice)

    # wait for send
    send_scan_btn = spice.wait_for(MenuAppWorkflowObjectIds.send_scan_copy_button, timeout=8)
    send_scan_btn.mouse_click() # we're done

    current_job_id = job.get_last_job_id()

    # there's 3 screens after clicking the 'Send' button: 'Scanning' (for a few seconds), 'Copying...' (the one we're
    # waiting on the statement on the top), and after less than a second, 'Copying job <name>...' appears. After this
    # two statements we'll be on the last screen.
    wait_for_print_menu_text("cStringEllipsis", spice, net, locale, "cCopying") # wait for 'Copying...'
    spice.wait_until(lambda: 'PRINTING' in job.get_details_job(current_job_id), timeout=10, \
                        waiting_for='current job starts printing')
    assert 'COMPLETED' not in job.get_details_job(current_job_id), \
            "The waiting was too long; printing is already finished so we can't cancel it anymore"

    # cancel print
    logging.info("Canceling print...")
    spice.main_app.wait_and_click_on_middle(MenuAppWorkflowObjectIds.copy_progress_cancel)
    logging.info("Print cancel petition sent; validation required")
    
    # confirm cancel
    logging.info("Sending OK to print cancel petition...")
    spice.wait_for(MenuAppWorkflowObjectIds.copy_progress_cancel_confirm).mouse_click()
    logging.info("Print should be canceled now")

    # complete copy
    finish_btn, _ = wait_for_print_to_complete("cCopyCanceledMessage", spice, net, locale)
    finish_btn.mouse_click()

    # back to the 'copy' screen?
    spice.copy_ui().copy_button_present(spice)
