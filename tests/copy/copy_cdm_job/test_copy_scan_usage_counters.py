import dunetuf.common.commonActions as CommonActions
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.addressBook.addressBook import *
from .lib.counters_helpers import CounterHelpers

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test scan usage counters with copy
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-82851
    +timeout:120
    +asset: Scan
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_scan_usage_counters
    +test:
        +title: test_copy_scan_usage_counters
        +guid:1d728d20-e896-11ec-addd-7bbce0a6326c
        +dut:
            +type: Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_scan_usage_counters(tcl, udw, copy, job):
    """
        Test scan usage counters values simulating a job copy.
        Total and default scan counters must be afected

        Args:
            tcl,udw,spice,cdm: fixtures
    """

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)
    helper = CounterHelpers(tcl, udw, scan_action)

    # Create configuration Scan
    height = 300 # mm
    width = 400 # mm
    
    # Expected counters increase for the scan size above
    copy_expected_increase = {
        "AREA_OTHER_SCANS"          : 0.0,  # cm2
        "AREA_COPY_SCANS"           : 1200, # cm2
        "TOTAL_SCANNED_AREA"        : 1200, # cm2
        "TOTAL_SCANNED_LENGTH"      : 300,  # mm
        "TOTAL_NUMBER_OTHER_SCANS"  : 0.0,
        "TOTAL_NUMBER_COPY_SCANS"   : 1.0,
        "TOTAL_NUMBER_SCANS"        : 1.0,
        "LENGTH_OTHER_SCANS"        : 0.0,  # mm
        "LENGTH_COPY_SCANS"         : 300   # mm
    }

    # Get current counters values
    initial_counter_status = helper.get_all_scan_counters_values(helper.get_all_scan_counters_by_tcl())
    
    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e200Dpi",
        "dest": "print",
        "copies": 1
    }

    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get counters values after copy
    # Init simulation
    final_counter_status = helper.get_all_scan_counters_values(helper.get_all_scan_counters_by_tcl())

    # Check incremented values in counter.
    current_value = 0.0
    for counter,expected_value in copy_expected_increase.items():
        current_value = round(final_counter_status[counter] - initial_counter_status[counter], 2)
        redundance_accepted = expected_value * 0.02 # 2% of error
        differ_value = abs(expected_value - current_value)
        assert differ_value <= redundance_accepted,\
            f"For the counter: {counter} the current value: {current_value} differ from expected value: {expected_value}"       
