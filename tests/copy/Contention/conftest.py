import logging
from dunetuf.send.email.email import Email
from dunetuf.send.folder.folder import Folder
from dunetuf.job.storejob import DuneStoreJob
import time
import pytest
from dunetuf.fax.fax import Fax

@pytest.fixture
def dunestorejob(cdm, udw):
    yield DuneStoreJob(cdm, udw)

@pytest.fixture
def setup_teardown_email_server(cdm, udw, request):
    email_instance = Email(cdm,udw)
    email_instance.start_email_server()
    serverDetails = email_instance._email_server.get_email_server_details()
    
    yield email_instance, serverDetails

    email_instance.delete_all_email_profiles()
    email_instance.stop_email_server(request)


@pytest.fixture
def setup_teardown_folder_server(cdm, udw):
    folder_instence = Folder(cdm, udw)
    folder_instence.set_up_folder_server()
    
    yield folder_instence

    folder_instence.tear_down_folder_server()

@pytest.fixture
def setup_teardown_print_idle_status(job, counters, udw):
    job.cancel_active_jobs()
    time.sleep(3)
    job.wait_for_no_active_jobs()

    job.clear_joblog()
    udw.mainApp.PrintMeter.ClearSystemCounters()
    if "ScanMeter" in udw.mainApp.__dict__:
        udw.mainApp.ScanMeter.clearAllCounters()
    if "SendFaxMeter" in udw.mainApp.__dict__:
        udw.mainApp.SendFaxMeter.clearAllCounters()
    udw.mainApp.JobMeter.clearAllCounters()
    logging.info("bookmark jobs")
    job.bookmark_jobs()

    yield

    udw.mainApp.PrintMeter.ClearSystemCounters()
    if "ScanMeter" in udw.mainApp.__dict__:
        udw.mainApp.ScanMeter.clearAllCounters()
    if "SendFaxMeter" in udw.mainApp.__dict__:
        udw.mainApp.SendFaxMeter.clearAllCounters()
    udw.mainApp.JobMeter.clearAllCounters()
    job.cancel_active_jobs()
    time.sleep(3)
    job.wait_for_no_active_jobs()
    job.clear_joblog()

@pytest.fixture
def setup_teardown_dunestore_job(dunestorejob, usbdevice, device, ssh, udw):
    result = device.device_ready(50)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"

    isSimulator = udw.mainUiApp.ControlPanel.isSimulator()

    if isSimulator:
        logging.info('-- SETUP (Stored Job Tests) --')
        usbdevice.remove_all_mock_devices(ssh)

        logging.info('Adding USB mock device')
        usbdevice.add_mock_device('usbdisk2', 'UsbDisk2', 'rearUsb', is_paired = True)

    logging.info('Cleanup up existing stored job')
    dunestorejob.delete_all(',1111,1234,2345,Alphanumeric1,Alphanumeric2')

    logging.info('Reset stored job configuration')
    dunestorejob.reset_configuration()

    yield

    logging.info('-- TEARDOWN (Stored Job Tests) --')
    logging.info('Reset stored job configuration')
    dunestorejob.reset_configuration()

    logging.info('Cleanup up existing stored job')
    dunestorejob.delete_all(',1111,1234,2345,Alphanumeric1,Alphanumeric2')

    if isSimulator:
        logging.info('Removing USB mock device')
        usbdevice.remove_all_mock_devices(ssh)

@pytest.fixture
def setup_teardown_with_empty_usb_drive(usbdevice, device, ssh):
    """Default setup/teardown fixture for usb print tests."""

    result = device.device_ready(150)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"

    # ---- Setup ----
    logging.info("remove all the mock devices")
    usbdevice.remove_all_mock_devices(ssh)

    if not usbdevice.check_device("usbdisk1"):
        logging.info('Adding USB mock device')
        usbdevice.add_mock_device('usbdisk1', 'UsbDisk1', 'frontUsb')


    yield

    logging.info("remove all the mock devices")
    usbdevice.remove_all_mock_devices(ssh) 

@pytest.fixture
def fax_config_reset(udw, cdm):
    """
    Setup/tear down for Fax setup/send setting/receive setting
    """
    logging.info("Default for Fax sending setting")
    config_default_send_response = cdm.get(cdm.FAX_SEND_CONFIGURATION_ENDPOINT) 

    logging.info("Default for Fax receive setting")
    config_default_receive_response = cdm.get(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT) 

    logging.info("Default for Fax Setup Config")
    config_default_setup_response = cdm.get(cdm.FAX_MODEM_CONFIGURATION_ENDPOINT)

    logging.info("Default for Fax Job Ticket Config")
    config_default_fax_job_response = cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_SCANFAX)

    logging.info("Default for Fax Receive Job Ticket Config")
    config_default_receive_fax_job_response = cdm.get(cdm.JOB_TICKET_CONFIGURATION_FAX_RECEIVE)

    logging.info("Default for Fax Forward Config")
    config_default_fax_forward_response = cdm.get(cdm.FAX_FORWARD_ENDPOINT)

    logging.info("Default for Fax Archive Config")
    config_default_fax_archive_response = cdm.get(cdm.FAX_ARCHIVE_ENDPOINT)

    yield

    logging.info("Reset Fax Setup Config")
    cdm.put(cdm.FAX_MODEM_CONFIGURATION_ENDPOINT, config_default_setup_response)
    time.sleep(1)
    logging.info("Default for Fax sending setting")
    cdm.put(cdm.FAX_SEND_CONFIGURATION_ENDPOINT, config_default_send_response) 
    time.sleep(1)
    logging.info("Default for Fax receive setting")
    cdm.put(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT, config_default_receive_response) 
    time.sleep(1)
    logging.info("Default forFax Job Ticket setting")
    cdm.put(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_SCANFAX, config_default_fax_job_response) 
    time.sleep(1)
    logging.info("Default for Fax Receive Job Ticket setting")
    cdm.put(cdm.JOB_TICKET_CONFIGURATION_FAX_RECEIVE, config_default_receive_fax_job_response)  
    time.sleep(1)
    logging.info("Default for Fax Forward Config")
    cdm.put(cdm.FAX_FORWARD_ENDPOINT, config_default_fax_forward_response)
    time.sleep(1)
    logging.info("Default for Fax Archive Config")
    cdm.put(cdm.FAX_ARCHIVE_ENDPOINT, config_default_fax_archive_response)
    time.sleep(1)

@pytest.fixture
def setup_fax_using_cdm(job,cdm,udw):
    default_data = Fax(cdm, udw).get_fax_setup_config()
    default_newdata = {'analogFaxSetup': {'faxNumber': '101', 'companyName': 'automation', 'analogFaxCountry': 'US'}}

    Fax(cdm, udw).reset_fax_setup_config(default_newdata)

    yield

    Fax(cdm, udw).reset_fax_setup_config(default_data)
