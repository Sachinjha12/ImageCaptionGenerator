import logging, pytest, os, json
from dunetuf.scan.ScanAction import ScanAction
from tests.print.test_print_intent import get_field_value
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

SCAN_WAIT_TIMEOUT = 30.0

# Create an instance of the common actions ScanAction class
scan_action = ScanAction()

@pytest.fixture(autouse=True)
def setup_teardown_rotation_copy_settings(spice, device, udw, scp, outputsaver, tcl, net):
    
    logging.info('-- SETUP Rotation Copy Settings --')
    
    spice.goto_homescreen()

    outputsaver.clear_output()
    outputsaver.save_print_intents(True)

    scan_action.set_net(net).set_scp(scp).set_udw(udw).set_tcl(tcl)
    scan_action.unload_media("MDF")

    yield
    
    logging.info('-- TEARDOWN Rotation Copy Settings --')

    outputsaver.clear_output()

    # Recover settings
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().go_to_paper_selection()
    spice.copy_ui().select_copy_paper_source(CopyAppWorkflowObjectIds.combo_option_paper_selection_source_auto)
    spice.copy_ui().go_back_to_setting_from_paper_selection()
    spice.copy_ui().back_to_landing_view()
    
    spice.goto_homescreen()
    
    result = device.device_ready(10)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check in the UI that rotation values for Copy settings and their dynamic constraints are as expected
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114577
    +timeout:500
    +asset:Copy
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_given_copy_rotation_settings_when_checking_them_then_values_and_constraints_are_as_expected
    +test:
        +title:test_given_copy_rotation_settings_when_checking_them_then_values_and_constraints_are_as_expected
        +guid:5331a90e-96e1-48bc-ba5c-f30462249978
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & DeviceClass=MFP & DeviceFunction=UI & DeviceFunction=Copy & ScanSettings=Orientation & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_given_copy_rotation_settings_when_checking_them_then_values_and_constraints_are_as_expected(spice, job, outputsaver, net, locale: str = "en"):

    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()

    last_job_id = job.get_last_job_id()

    # Check Rotation values in Copy options list
    spice.copy_ui().check_copy_rotation(net, locale, "cAutomatic")

    # ===== Temporary fix from DUNE-141750 leads to disabling the complete combobox =====
    # Check available Rotation
    spice.copy_ui().verify_copy_rotation_combobox_constrained()
    # spice.copy_ui().select_copy_rotation(CopyAppWorkflowObjectIds.combo_option_rotation_auto)

    # Check Rotation constrains when automatic Paper Source is selected
    # spice.copy_ui().verify_copy_rotation_constrained(CopyAppWorkflowObjectIds.combo_option_rotation_180)
    # =====
    
    # Check Rotation constrains when specific Paper Source is selected
    spice.copy_ui().go_to_paper_selection()
    spice.copy_ui().select_copy_paper_source(CopyAppWorkflowObjectIds.combo_option_paper_selection_source_roll1)
    spice.copy_ui().go_back_to_setting_from_paper_selection()

    expected_rotations = [CopyAppWorkflowObjectIds.combo_option_rotation_auto,
                          CopyAppWorkflowObjectIds.combo_option_rotation_0,
                          CopyAppWorkflowObjectIds.combo_option_rotation_90,
                          CopyAppWorkflowObjectIds.combo_option_rotation_180,
                          CopyAppWorkflowObjectIds.combo_option_rotation_270]
    for rotation in expected_rotations:
        spice.copy_ui().select_copy_rotation(rotation)

    # Check Print Intent
    spice.copy_ui().back_to_landing_view()

    scan_action.load_media("MDF")
    spice.copy_ui().done_button_present(spice, SCAN_WAIT_TIMEOUT)
    spice.copy_ui().press_done_button(spice)

    current_job_id = job.get_last_job_id()
    assert last_job_id != current_job_id, "The new job has not been generated"
    job.wait_for_job_completion(job.get_last_job_id())

    output_files = outputsaver.save_output()
    print_intent_file = [file for file in output_files if 'PrintIntentPage_' in file][0]
    with open(os.path.join(outputsaver.local_staging, print_intent_file), 'r') as intent:
        print_intent = json.load(intent)

    assert get_field_value(print_intent, 'AUTOROTATE_ENABLE') == 0, "AUTOROTATE_ENABLE is not disabled in the Print Intent after selecting \"Rotate\" 270 deg"
    outputsaver.clear_output()
