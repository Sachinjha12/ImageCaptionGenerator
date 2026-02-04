import pytest
import logging

from dunetuf.copy.copy import Copy
from dunetuf.scan.ScanAction import ScanAction

@pytest.fixture
def setup_teardown_with_copy_job(job, device, outputsaver, cdm, udw, spice, tcl):
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
    ScanAction().set_tcl(tcl).reset_simulation_mode()

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
    ScanAction().set_tcl(tcl).reset_simulation_mode()

@pytest.fixture
def setup_teardown_with_copy_job_crc(job, device, outputsaver, cdm, udw, spice, tcl):
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
    logging.info("Enable saving of CRC.")
    outputsaver.operation_mode('CRC')
    logging.info("Get default copy setting")
    copy_default_settings = Copy(cdm, udw).get_copy_default_ticket(cdm)
    ScanAction().set_tcl(tcl).reset_simulation_mode()

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
    ScanAction().set_tcl(tcl).reset_simulation_mode()

@pytest.fixture
def setup_teardown_with_copy_job_crc_direct_mode(setup_teardown_with_copy_job_crc, copy, configuration):
    copy.set_copymode_direct()
    yield
    copy.reset_copymode_to_default(configuration)