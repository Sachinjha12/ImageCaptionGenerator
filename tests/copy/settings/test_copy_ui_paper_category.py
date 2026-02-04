import logging, pytest, os, json
from dunetuf.scan.ScanAction import ScanAction
from tests.print.test_print_intent import get_field_value
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

SCAN_WAIT_TIMEOUT = 30.0

# Create an instance of the common actions ScanAction class
scan_action = ScanAction()

@pytest.fixture(autouse=True)
def setup_teardown_paper_category_copy_settings(spice, device, udw, scp, outputsaver, tcl, net):
    
    logging.info('-- SETUP Paper Category Copy Settings --')
    
    spice.goto_homescreen()

    outputsaver.clear_output()
    outputsaver.save_print_intents(True)

    scan_action.set_net(net).set_scp(scp).set_udw(udw).set_tcl(tcl)
    scan_action.unload_media("MDF")

    yield
    
    logging.info('-- TEARDOWN Paper Category Copy Settings --')

    outputsaver.clear_output()
  
    spice.goto_homescreen()
    
    result = device.device_ready(10)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check in the UI that paper category values for Copy settings and their dynamic constraints are as expected
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
    +name:test_given_copy_paper_category_settings_when_checking_them_then_values_and_constraints_are_as_expected
    +test:
        +title:test_given_copy_paper_category_settings_when_checking_them_then_values_and_constraints_are_as_expected
        +guid:a2e85139-381d-4ba9-a0f8-47f72553a5f9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & DeviceClass=MFP & DeviceFunction=UI & DeviceFunction=Copy & Copy=PaperType & Copy=PaperTray
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.skip(reason="Not stable test, need investigation, we'll fix it in future DUNE-169069")
def test_given_copy_paper_category_settings_when_checking_them_then_values_and_constraints_are_as_expected(spice, job, outputsaver, net, locale: str = "en"):

    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()

    last_job_id = job.get_last_job_id()

    # Check Paper Selection values in Copy options list
    spice.copy_ui().check_paper_selection(net, locale, "cAny", "cAutomaticallySelect")
    spice.copy_ui().go_to_paper_selection()

    # Check available Paper Categories
    expected_paper_categories = [CopyAppWorkflowObjectIds.combo_option_paper_selection_family_adhesive,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_backlit,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_banner,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_bondandcoated,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_blueprint,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_custom,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_film,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_photo,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_poster,
                                 CopyAppWorkflowObjectIds.combo_option_paper_selection_family_technical]
    for paper_category in expected_paper_categories:
        spice.copy_ui().select_copy_paper_category(paper_category)

    # Check Print Intent
    spice.copy_ui().go_back_to_setting_from_paper_selection()
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

    assert get_field_value(print_intent, 'MEDIA_CATEGORY') == "TECHNICAL", "The \"Paper Category\" in the Print Intent is not TECHNICAL"
    outputsaver.clear_output()
    
    # Check Paper Source constrains when specific Paper Category is selected
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().go_to_paper_selection()
    spice.copy_ui().verify_copy_paper_source_combobox_constrained()

    # Paper Category back to "Any"
    spice.copy_ui().select_copy_paper_category(CopyAppWorkflowObjectIds.combo_option_paper_selection_family_unknown)

    # Check available Paper Sources
    expected_paper_sources = [CopyAppWorkflowObjectIds.combo_option_paper_selection_source_roll1,
                              CopyAppWorkflowObjectIds.combo_option_paper_selection_source_roll2]
    for paper_source in expected_paper_sources:
        spice.copy_ui().select_copy_paper_source(paper_source)

    # Check Paper Category constrains when specific Paper Source is selected
    spice.copy_ui().verify_copy_paper_category_constrained(CopyAppWorkflowObjectIds.combo_option_paper_selection_family_photo)

    # Paper Source back to "Automatically Select"
    spice.copy_ui().select_copy_paper_source(CopyAppWorkflowObjectIds.combo_option_paper_selection_source_auto)
    spice.copy_ui().go_back_to_setting_from_paper_selection()
    spice.copy_ui().back_to_landing_view()
