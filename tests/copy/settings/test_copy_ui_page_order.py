import logging, pytest, os, json
from dunetuf.scan.ScanAction import ScanAction
from tests.print.test_print_intent import get_field_value
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

SCAN_WAIT_TIMEOUT = 30.0

# Create an instance of the common actions ScanAction class
scan_action = ScanAction()

@pytest.fixture(autouse=True)
def setup_teardown_page_order_copy_settings(spice, device, udw, scp, outputsaver, tcl, net):
    
    logging.info('-- SETUP Page Order Copy Settings --')
    
    spice.goto_homescreen()

    outputsaver.clear_output()
    outputsaver.save_print_intents(True)

    scan_action.set_net(net).set_scp(scp).set_udw(udw).set_tcl(tcl)
    scan_action.unload_media("MDF")

    yield
    
    logging.info('-- TEARDOWN Page Order Copy Settings --')

    outputsaver.clear_output()

    spice.goto_homescreen()
    
    result = device.device_ready(10)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test that page order setting is available and working correctly in the Copy app
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114578
    +timeout:400
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:A4_Color_200.ppm=d4f3409e817cc3f8e0bbcfac143c7b4152e6dc0262f883df5f0a176d8babd251
    +test_classification:System
    +name:test_given_a_copy_app_when_copying_using_page_order_setting_then_print_order_is_as_expected
    +test:
        +title:test_given_a_copy_app_when_copying_using_page_order_setting_then_print_order_is_as_expected
        +guid:ffb2c565-42e2-468b-aed1-3a652dbd2a0d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceFunction=UI & Copy=PageOrder & ScannerInput=ManualFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.skip(reason="Not stable test, need deep investigation, we'll fix it in future DUNE-169073")
def test_given_a_copy_app_when_copying_using_page_order_setting_then_print_order_is_as_expected(setup_teardown_print_device, spice, job, outputsaver):
    
    # TODO: try it with scan_action.set_scan_pnm_acquisition_mode() when DUNE-133124 is fixed. Further check behaviour of CRC generation: right now they are different each time the same page is scanned. Also each each CRC is generated after each page is scanned, not once the whole job is sent to print. Read and verify that obtained checksums are in the expected order if above behaviour is changed in the future.
    #first_scanned_page = os.getcwd() + "/input/system_test_binaries/" + "d4f3409e817cc3f8e0bbcfac143c7b4152e6dc0262f883df5f0a176d8babd251"
    #second_scanned_page = os.getcwd() + "/input/system_test_binaries/" + ""

    spice.copy_ui().goto_copy()
    last_job_id = job.get_last_job_id()

    # ====== First Page On Top ======
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().select_copy_printing_order(CopyAppWorkflowObjectIds.combo_copyPrintingOrder_option_firstPageOnTop)
    spice.copy_ui().back_to_landing_view()

    # Simulate random scan
    scan_action.load_media("MDF")

    # Validate printing order is constrained once scan has started
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().verify_copy_printing_order_constrained()
    spice.copy_ui().back_to_landing_view()

    # Start printing
    spice.copy_ui().done_button_present(spice, SCAN_WAIT_TIMEOUT)
    spice.copy_ui().press_done_button(spice)

    current_job_id = job.get_last_job_id()
    assert last_job_id != current_job_id, "The new job has not been generated"
    job.wait_for_job_completion(job.get_last_job_id())

    # Check print intent
    output_files = outputsaver.save_output()
    print_intent_file = [file for file in output_files if 'PrintIntentPage_' in file][0]
    with open(os.path.join(outputsaver.local_staging, print_intent_file), 'r') as intent:
        print_intent = json.load(intent)

    assert get_field_value(print_intent, 'PRINTING_ORDER') == 0, "PRINTING_ORDER is expected to be print \"First Page On Top\"."
    outputsaver.clear_output()

    # ====== Last Page On Top ======
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().select_copy_printing_order(CopyAppWorkflowObjectIds.combo_copyPrintingOrder_option_lastPageOnTop)
    spice.copy_ui().back_to_landing_view()

    last_job_id = job.get_last_job_id()

    # Simulate random scan
    scan_action.load_media("MDF")

    # Start printing
    spice.copy_ui().done_button_present(spice, SCAN_WAIT_TIMEOUT)
    spice.copy_ui().press_done_button(spice)

    current_job_id = job.get_last_job_id()
    assert last_job_id != current_job_id, "The new job has not been generated"
    job.wait_for_job_completion(job.get_last_job_id())

    # Check print intent
    output_files = outputsaver.save_output()
    print_intent_file = [file for file in output_files if 'PrintIntentPage_' in file][0]
    with open(os.path.join(outputsaver.local_staging, print_intent_file), 'r') as intent:
        print_intent = json.load(intent)
    
    assert get_field_value(print_intent, 'PRINTING_ORDER') == 1, "PRINTING_ORDER is expected to be print \"Last Page On Top\"."
    outputsaver.clear_output()

