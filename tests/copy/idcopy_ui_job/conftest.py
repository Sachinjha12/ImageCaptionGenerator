import pytest
import logging


@pytest.fixture
def setup_teardown_with_id_copy_job(job, device, outputsaver, udw, spice):
    """Default setup/teardown fixture for id Copy tests."""

    result = device.device_ready(150)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"

    # ---- Setup ----
    logging.info("Cancel the current job")
    job.cancel_active_jobs()

    logging.info("Clear job job")
    job.clear_joblog()

    logging.info("Clear output")
    outputsaver.clear_output()

    yield
    logging.info("Save all output into local")
    outputsaver.save_output()

    logging.info("Clear output")
    outputsaver.clear_output()

    logging.info("Cancel the current job")
    job.cancel_active_jobs()

    logging.info("back to the home screen after finish the job")
    spice.goto_homescreen()
