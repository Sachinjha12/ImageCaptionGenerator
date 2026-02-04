import pytest
import logging

from dunetuf.copy.copy import Copy
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.power.power import *

def set_simulators_in_idle_state_and_set_copy_mode(tcl, spice, udw, cdm, tray, copy, job, set_direct_copy=False):
    # Clean job history
    job.cancel_active_jobs()
    job.bookmark_jobs()

    spice.goto_homescreen()

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw).set_cdm(cdm).set_tcl(tcl)

    # Reset scan simulation mode
    scan_action.reset_simulation_mode()

    # Ensure media is loaded
    if not scan_action.is_media_loaded():
        scan_action.load_media()

    if set_direct_copy:
        copy.set_copymode_direct()
    else:
        copy.set_copymode_indirect()

@pytest.fixture
def setup_teardown_with_copy_job(job, device, outputsaver, cdm, udw, spice):
    """Default setup/teardown fixture for Copy tests."""

    result = device.device_ready(150)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"
    # ---- Setup ----
    spice.cleanSystemEventAndWaitHomeScreen()
    logging.info("Cancel the current job")
    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    logging.info("Clear job job")
    job.clear_joblog()
    logging.info("Clear output")
    outputsaver.clear_output()
    logging.info("Enable saving of TIFF.")
    outputsaver.operation_mode('TIFF')
    logging.info("Get default copy setting")
    copy_default_settings = Copy(cdm, udw).get_copy_default_ticket(cdm)

    yield

    logging.info("Save all output into local")
    outputsaver.save_output()
    logging.info("Clear output")
    outputsaver.clear_output()
    logging.info("Cancel the current job")
    job.cancel_active_jobs()
    outputsaver.operation_mode('NONE')
    logging.info("back to the home screen after finish the job")
    spice.goto_homescreen()
    logging.info("Restore copy default settings")
    Copy(cdm, udw).reset_copy_default_ticket(cdm, copy_default_settings)

@pytest.fixture()
def copy_page_sensor_setup(spice, copy, udw, job, cdm, tcl, tray):
    #--------- Set Up -----------
    logging.info("Copy Page Sensor Indirect Copy From Start Test Test Set Up")
    logging.info("Not in Home screen - Checking for System Errors / System Events windows")
    # Wait for HomeScreen to appear
    spice.cleanSystemEventAndWaitHomeScreen()
    set_simulators_in_idle_state_and_set_copy_mode(tcl, spice, udw, cdm, tray, copy, job)

    yield
    #--------- Test Tear Down --------
    set_simulators_in_idle_state_and_set_copy_mode(tcl, spice, udw, cdm, tray, copy, job)

@pytest.fixture()
def copy_page_sensor_setup_indirect_mode_and_out_of_media_inputs(tray, setup_teardown_print_device, copy_page_sensor_setup):
    # Set media input rolls to out of media
    tray.unload_media()
    yield

@pytest.fixture()
def copy_page_sensor_setup_indirect_mode_and_reduce_size_media_inputs(tcl, tray, setup_teardown_print_device, copy_page_sensor_setup):
    # Set media input rolls to out of media
    tray.configure_all_trays(media_size='custom', media_type='stationery', width=120000.0, length=0.0, resolution=10000)
    # Create some instance of the common actions ScanAction class with A2 size
    height = 594 # mm
    width  = 420 # mm
    ScanAction().set_tcl(tcl).set_scan_random_acquisition_mode(height, width)
    yield

@pytest.fixture()
def copy_page_sensor_setup_force_direct_copy_mode(spice, copy, udw, job, cdm, tray, tcl):
    #--------- Set Up -----------
    logging.info("Copy Page Sensor Direct Copy From Start Test Test Set Up")
    logging.info("Not in Home screen - Checking for System Errors / System Events windows")
    # Wait for HomeScreen to appear
    spice.cleanSystemEventAndWaitHomeScreen()
    set_simulators_in_idle_state_and_set_copy_mode(tcl, spice, udw, cdm, tray, copy, job, set_direct_copy=True)

    yield
    #--------- Test Tear Down --------
    set_simulators_in_idle_state_and_set_copy_mode(tcl, spice, udw, cdm, tray, copy, job)

@pytest.fixture()
def copy_page_sensor_setup_direct_mode_and_out_of_media_inputs(tray, setup_teardown_print_device, copy_page_sensor_setup_force_direct_copy_mode):
    # Set media input rolls to out of media
    tray.unload_media()
    yield

@pytest.fixture()
def copy_page_sensor_setup_direct_mode_and_reduce_size_media_inputs(tcl, tray, setup_teardown_print_device, copy_page_sensor_setup_force_direct_copy_mode):
    # Set media input rolls to out of media
    tray.configure_all_trays(media_size='custom', media_type='stationery', width=120000.0, length=0.0, resolution=10000)
    # Create some instance of the common actions ScanAction class with A2 size
    height = 594 # mm
    width  = 420 # mm
    ScanAction().set_tcl(tcl).set_scan_random_acquisition_mode(height, width)
    yield

@pytest.fixture()
def copy_configure_inactivity_30_seconds_scan_prepared(spice, cdm, udw, net):
    # Wait for HomeScreen to appear
    spice.cleanSystemEventAndWaitHomeScreen()
    power = Power(udw, target_ip=net.ip_address, cdm=cdm)

    previousTimeout = power.get_inactivity_timeout_CDM(ActivityModeFlow.inactivity_timeout)

    inactivityTimeout = "30"
    power.set_inactivity_timeout_CDM(ActivityModeFlow.inactivity_timeout, inactivityTimeout)

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw).set_cdm(cdm)

    # Ensure media is present
    scan_action.load_media()

    yield

    # Restore scanner state.
    scan_action.set_scan_state(1)

    # Restore timeout
    power.set_inactivity_timeout_CDM(ActivityModeFlow.inactivity_timeout, previousTimeout)
    spice.goto_homescreen()