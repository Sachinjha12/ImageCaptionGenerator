import pytest, os, json

from dunetuf.print.output.intents import Intents
from dunetuf.scan.ScanAction import ScanAction

from tests.print.test_print_intent import get_field_value

# Global Constant Variables
AUTO_ROTATE_ENABLED             = 1
AUTO_ROTATE_DISABLED            = 0
ORIGINAL_SCAN_WIDTH_PX          = 2490
ORIGINAL_SCAN_LENGTH_PX         = 3510
ORIGINAL_SCAN_WIDTH_A0_MM       = 841
ORIGINAL_SCAN_LENGTH_A0_MM      = 1189
ORIGINAL_SCAN_WIDTH_A0_PX       = 9930
ORIGINAL_SCAN_LENGTH_A0_PX      = 14040
ACCEPTABLE_DIFFERENCE_IN_PIXELS = 150 # Edge Detection could cause differ for width length, this will reduce random errors.

LIST_VARIABLE_PARAMETERS = (
    "rotate, media_source, width_expected, length_expected, auto_rotate_expected"
)

DICT_PARAMETRIZED_TESTS = [
    ("auto",        "auto",     ORIGINAL_SCAN_LENGTH_PX,    ORIGINAL_SCAN_WIDTH_PX,     AUTO_ROTATE_ENABLED),
    ("auto",        "auto",     ORIGINAL_SCAN_LENGTH_PX,    ORIGINAL_SCAN_WIDTH_PX,     AUTO_ROTATE_ENABLED),
    ("rotate0",     "roll-1",   ORIGINAL_SCAN_WIDTH_PX,     ORIGINAL_SCAN_LENGTH_PX,    AUTO_ROTATE_DISABLED),
    ("rotate90",    "roll-1",   ORIGINAL_SCAN_LENGTH_PX,    ORIGINAL_SCAN_WIDTH_PX,     AUTO_ROTATE_DISABLED),
    ("rotate180",   "roll-1",   ORIGINAL_SCAN_WIDTH_PX,     ORIGINAL_SCAN_LENGTH_PX,    AUTO_ROTATE_DISABLED),
    ("rotate270",   "roll-1",   ORIGINAL_SCAN_LENGTH_PX,    ORIGINAL_SCAN_WIDTH_PX,     AUTO_ROTATE_DISABLED)
]

def check_rotation_result(
    job,
    cdm,
    outputverifier,
    width_expected=ORIGINAL_SCAN_WIDTH_PX,
    length_expected=ORIGINAL_SCAN_LENGTH_PX,
    auto_rotate_expected=AUTO_ROTATE_ENABLED,
    acceptable_difference=ACCEPTABLE_DIFFERENCE_IN_PIXELS
):
    '''Method to check if rotation result is the expected

    Args:
        job (lib): Job Library
        cdm (lib): Cdm library
        outputverifier (lib): Print output verifier library
        width_expected (int, optional): Width output expected . Defaults to ORIGINAL_SCAN_WIDTH_PX.
        length_expected (int, optional): Length output expected. Defaults to ORIGINAL_SCAN_LENGTH_PX.
        auto_rotate_expected (int, optional): Auto rotation value in print intents expected. Defaults to 1.
        acceptable_difference (int, optional): acceptable possible redundancy difference in size, Default to ACCEPTABLE_DIFFERENCE_IN_PIXELS.
    '''
    # Check Completion status
    job.wait_for_no_active_jobs(time_out=30)
    job.check_job_log_by_status_and_type_cdm(
        [{"type": "copy", "status": "success"}], time_out=30
    )
    job.verify_jobdetails_stats_data(cdm, job, "copy", 1, 1)

    # Verify the final rotation angle
    outputverifier.save_and_parse_output(is_copy_job=True)

    # Verify sizes
    outputverifier.verify_page_width(
        intent=Intents.printintent, page_width=width_expected, redundance_accepted=acceptable_difference
    )
    outputverifier.verify_page_height(
        intent=Intents.printintent, page_height=length_expected, redundance_accepted=acceptable_difference
    )
    outputverifier.verify_image_width(
        intent=Intents.printintent, image_width=width_expected, redundance_accepted=acceptable_difference
    )
    outputverifier.verify_image_height(
        intent=Intents.printintent, image_height=length_expected, redundance_accepted=acceptable_difference
    )

    # Verify Auto Rotation Value
    output_files = outputverifier.outputsaver.save_output()
    print_intent_file = [file for file in output_files if "PrintIntentPage_" in file][0]
    with open(
        os.path.join(outputverifier.outputsaver.local_staging, print_intent_file), "r"
    ) as intent:
        print_intent = json.load(intent)

    assert (
        get_field_value(print_intent, "AUTOROTATE_ENABLE") == auto_rotate_expected
    ), "AUTOROTATE_ENABLE is not enabled"

    # TO IMPROVE - rotation is part of imaging intent that currently cannot be checked at here.
    # If there was any moment on how to check properly if imaging intent has last change properly.
    # Add it here to check that part


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy different rotation result with original A4
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-221923
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_job_indirect_rotation
    +test:
        +title: test_copy_job_indirect_rotation
        +guid: 1ea406d6-9cff-11ef-b41d-bb9029f21691
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.parametrize(LIST_VARIABLE_PARAMETERS, DICT_PARAMETRIZED_TESTS)
def test_copy_job_indirect_rotation(
    setup_teardown_with_copy_job_crc,
    rotate,
    media_source,
    width_expected,
    length_expected,
    auto_rotate_expected,
    copy,
    job,
    cdm,
    outputverifier,
):

    settings = {"rotate": rotate, "mediaSource": media_source}
    copy.create_run_configuration_copy(settings)

    check_rotation_result(
        job,
        cdm,
        outputverifier,
        width_expected=width_expected,
        length_expected=length_expected,
        auto_rotate_expected=auto_rotate_expected
    )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy differant rotations result with original A4 
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-221923
    +timeout:180
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_job_direct_rotation
    +test:
        +title: test_copy_job_direct_rotation
        +guid: 5ea0cdfe-9d28-11ef-b4ab-b7856c9d6345
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.parametrize(LIST_VARIABLE_PARAMETERS, DICT_PARAMETRIZED_TESTS)
def test_copy_job_direct_rotation(
    setup_teardown_with_copy_job_crc_direct_mode,
    rotate,
    media_source,
    width_expected,
    length_expected,
    auto_rotate_expected,
    copy,
    job,
    cdm,
    outputverifier,
):

    settings = {"rotate": rotate, "mediaSource": media_source}
    copy.create_run_configuration_copy(settings)

    check_rotation_result(
        job,
        cdm,
        outputverifier,
        width_expected=width_expected,
        length_expected=length_expected,
        auto_rotate_expected=auto_rotate_expected
    )


# A0 size
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy auto rotation result with original A0 
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-221923
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_job_indirect_auto_rotation_A0
    +test:
        +title: test_copy_job_indirect_auto_rotation_A0
        +guid: 62712c62-9d2d-11ef-b5d9-0320d5f8fd6b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_job_indirect_auto_rotation_A0(
    setup_teardown_with_copy_job_crc, copy, job, cdm, tcl, outputverifier
):
    settings = {"rotate": "auto"}
    ScanAction().set_tcl(tcl).set_scan_random_acquisition_mode(
        ORIGINAL_SCAN_LENGTH_A0_MM, ORIGINAL_SCAN_WIDTH_A0_MM
    )
    copy.create_run_configuration_copy(settings, wait_time=120)
    check_rotation_result(
        job,
        cdm,
        outputverifier,
        width_expected=ORIGINAL_SCAN_WIDTH_A0_PX,
        length_expected=ORIGINAL_SCAN_LENGTH_A0_PX
    )


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check copy auto rotation result with original A0
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-221923
    +timeout:240
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name: test_copy_job_direct_auto_rotation_A0
    +test:
        +title: test_copy_job_direct_auto_rotation_A0
        +guid: 825cf2fe-9d2d-11ef-bc69-6371e46687b8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_job_direct_auto_rotation_A0(
    setup_teardown_with_copy_job_crc_direct_mode, copy, job, cdm, tcl, outputverifier
):
    settings = {"rotate": "auto"}
    ScanAction().set_tcl(tcl).set_scan_random_acquisition_mode(
        ORIGINAL_SCAN_LENGTH_A0_MM, ORIGINAL_SCAN_WIDTH_A0_MM
    )
    copy.create_run_configuration_copy(settings, wait_time=120)
    check_rotation_result(
        job,
        cdm,
        outputverifier,
        width_expected=ORIGINAL_SCAN_WIDTH_A0_PX,
        length_expected=ORIGINAL_SCAN_LENGTH_A0_PX
    )
