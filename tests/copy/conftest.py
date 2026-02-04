import pytest
import logging
from time import sleep
from dunetuf.copy.copy import Copy
from dunetuf.ews.helper import EwsHelper
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmEndpoints import CdmEndpoints
from dunetuf.emulation.print.print_emulation_ids import DuneEngineMake, DuneEnginePlatform
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.job.storejob import DuneStoreJob

@pytest.fixture
def helper(ews):
    yield EwsHelper(ews)

@pytest.fixture
def dunestorejob(cdm, udw):
    yield DuneStoreJob(cdm, udw)

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



@pytest.fixture
def setup_teardown_copy_paper_source(spice, cdm, net, tray):
     # Load generic media
    default_tray = tray.get_default_source()
    tray.reset_trays()
    tray.configure_tray('roll-1', 'custom', 'custom')
    tray.load_media('roll-1')
    tray.configure_tray('roll-2', 'custom', 'stationery', width=360000.0, length=0.0, resolution=10000)
    tray.load_media('roll-2')
    
    yield

    tray.reset_trays()
    logging.info("back to the home screen after finish the job")
    spice.goto_homescreen()
    
@pytest.fixture()
def setup_teardown_homescreen(spice, job):
    
    spice.cleanSystemEventAndWaitHomeScreen()

    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)
    job.cancel_active_jobs()
    job.clear_joblog()
    
    yield
    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

@pytest.fixture()
def setup_teardown_default_copy_mode(cdm, udw, job, printjob, configuration):
    """Setup and teardown default copy mode.
    """
    copy_instance = Copy(cdm, udw)
    copy_instance.reset_copymode_to_default(configuration)

    yield

    copy_instance.reset_copymode_to_default(configuration)


@pytest.fixture()
def setup_teardown_interrupt_copymode(cdm, udw, configuration, printjob, usbdevice, job):
    logging.info('-- SETUP (Job Interrupt Tests) --')

    # Default copymode
    copy_instance = Copy(cdm, udw)
    copy_instance.reset_copymode_to_default(configuration)
    
    job.clear_joblog()
    job.bookmark_jobs()
    printjob.bookmark_jobs()

    # Add USB device
    logging.info("Add USB device")
    if not usbdevice.check_device("usbdisk1"):
        logging.info('Adding USB mock device')
        usbdevice.add_mock_device('usbdisk1', 'UsbDisk1', 'frontUsb')

    yield
    logging.info('-- TEARDOWN (Job Interrupt Tests) --')
    job.cancel_active_jobs()
    job.wait_for_no_active_jobs()
    
    # Remove USB device
    logging.info("Remove USB device")
    if usbdevice.check_device('usbdisk1'):
        logging.info('Removing USB mock device')
        usbdevice.remove_mock_device('usbdisk1')
   
    # Exit all priority mode sessions
    logging.info("Exit all priority mode sessions")
    job.exit_all_priority_mode_sessions()

    # Set default copymode
    copy_instance.reset_copymode_to_default(configuration)
    
@pytest.fixture()
def setup_teardown_folding_style(spice, cdm):
    """Default setup/teardown fixture for folding style tests."""
    logging.info('-- SETUP (Folding style Tests) --')

    response_job_ticket_copy = cdm.get_raw(CdmEndpoints.JOB_TICKET_COPY).json()
    logging.info(response_job_ticket_copy)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    yield

    logging.info('-- TEARDOWN (Folding style Tests) --')

    # Back To Home to set initial state again
    spice.copy_app.goto_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

@pytest.fixture
def copy_screen_setup(spice, udw):
    logging.info('-- SETUP copy_screen_setup --')
    # go to "copy" menu
    spice.homeMenuUI().goto_menu_copy(spice)

    yield

    logging.info('-- TEARDOWN copy_screen_setup --')

    # back to default scanning times
    udw.mainApp.execute("FormatterToScanner PUB_resetScanningDelay")

    # go to homescreen
    try:
        spice.goto_homescreen()
    except Exception:
        pass
    finally:
        # stuck at 'send' button screen?
        if not spice.is_HomeScreen():
            logging.info('Not on homescreen after teardown; trying again...')
            sleep(10) # just in case we're in a loading screen

            try:
                logging.info(f"Trying to press '{MenuAppWorkflowObjectIds.send_scan_copy_button}', just in case it got stuck...")
                spice.wait_for(MenuAppWorkflowObjectIds.send_scan_copy_button, timeout=1).mouse_click()
                sleep(10) # we'll have to wait for the next loading screen until the 'home' button appears
            except Exception:
                logging.info(f"Couldn't find button '{MenuAppWorkflowObjectIds.send_scan_copy_button}'")
            finally:
                logging.info('Re-try homescreen...')
                spice.goto_homescreen() # try again

@pytest.fixture
def copy_screen_slow_printing_setup(copy_screen_setup, siriusEngine):
    # setup slow printing
    logging.info('Setting sweep time...')
    siriusEngine.mech.set_print_sweep_time(1000) # 1s/print sweep

    # run the tests
    yield

    logging.info('Clearing sweep time...')
    siriusEngine.mech.set_print_sweep_time(0) # back to defaults

@pytest.fixture
def setup_teardown_ensure_scan_media_is_loaded(udw, cdm):
    scan_action = ScanAction().set_udw(udw).set_cdm(cdm)
    scan_action.load_media()
    # run the tests
    yield

    scan_action.load_media()


@pytest.fixture(autouse=True)
def setup_teardown_reset_copy_default_settings(cdm, job, request):
    if 'disable_autouse' in request.keywords:
        yield
    else:
        job.cancel_active_jobs()
        job.clear_joblog()
        logging.info("Get Default Copy Options before running the test")
        copy_default_settings = cdm.get(cdm.JOB_TICKET_COPY)
        logging.debug("Default Copy Options before running the test:: {0}".format(copy_default_settings))
        job.wait_for_no_active_jobs()

        yield

        job.cancel_active_jobs()
        job.clear_joblog()
        logging.debug("Default Copy Options after running the test:: {0}".format(cdm.get(cdm.JOB_TICKET_COPY)))
        logging.info("Set original Default Copy Options after running the test")
        cdm.put(cdm.JOB_TICKET_COPY, copy_default_settings)
        job.wait_for_no_active_jobs()


@pytest.fixture(autouse=True)
def setup_teardown_reset_tray_load_paper(print_emulation):
    logging.info("Set Trays to default paper size and type before test.")
    if (print_emulation.print_engine_platform == DuneEnginePlatform.emulator.name) and (print_emulation.engine_make == DuneEngineMake.canonHomepro.name):
            # Reset tray and load paper on canon Homepro emulators
            print_emulation.tray.reset_trays()

    yield

    logging.info("Set Trays to default paper size and type after test.")
    if (print_emulation.print_engine_platform == DuneEnginePlatform.emulator.name) and (print_emulation.engine_make == DuneEngineMake.canonHomepro.name):
            # Reset tray and load paper on canon Homepro emulators
            print_emulation.tray.reset_trays()