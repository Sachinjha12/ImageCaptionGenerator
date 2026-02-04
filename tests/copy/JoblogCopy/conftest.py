import pytest
from dunetuf.copy.copy import Copy
from dunetuf.send.email.email import Email
from dunetuf.send.common.common import Common
from dunetuf.send.usb.usb import Usb
from dunetuf.send.folder.folder import Folder
from dunetuf.fax.fax import Fax
import logging


@pytest.fixture
def copy(cdm, udw):
    yield Copy(cdm, udw)


@pytest.fixture
def email(cdm, udw):
    yield Email(cdm, udw)


@pytest.fixture
def common(cdm, udw):
    yield Common(cdm, udw)


@pytest.fixture
def usb(cdm, udw, net):
    yield Usb(cdm, udw, net)


@pytest.fixture
def networkfolder(cdm, udw):
    yield Folder(cdm, udw)


@pytest.fixture
def fax(cdm, udw):
    yield Fax(cdm, udw)

@pytest.fixture
def setup_teardown_for_fax_negative(job, cdm , outputsaver):
    # ---- Setup ----
    job.cancel_active_jobs()
    job.clear_joblog()
    outputsaver.clear_output()

    logging.info("Set all redials to 0")
    uri = cdm.FAX_MODEM_CONFIGURATION_ENDPOINT
    config_default_body = cdm.get(uri)  

    config_new_default_values_body = {
        "analogFaxOperation":
        {
            'redialInterval':1, # change 5min to 1min for auto test
            'redialOnError': 0,
		    'redialOnNoAnswer': 0,
		    'redialOnBusy': 0,
        },
        'faxSendHeader': 'overlay' # set fax header overlay
    } 
        
    cdm.patch(uri, config_new_default_values_body)
    yield
    # ---- Teardown ----
    job.cancel_active_jobs()
    job.clear_joblog()
    cdm.patch(uri, config_default_body)

    outputsaver.clear_output()

@pytest.fixture
def setup_teardown_fax_contention(job, cdm, outputsaver):
    # ---- Setup ----
    job.cancel_active_jobs()
    job.clear_joblog()
    outputsaver.clear_output()
    logging.info("Set all redials to 0")
    uri = cdm.FAX_MODEM_CONFIGURATION_ENDPOINT
    config_default_body = cdm.get(uri)  

    config_new_default_values_body = {
        "analogFaxOperation":
        {
            'redialInterval':1, # change 5min to 1min for auto test
            'redialOnError': 0,
		    'redialOnNoAnswer': 0,
		    'redialOnBusy': 0,
        },
        'faxSendHeader': 'overlay' # set fax header overlay
    } 
        
    cdm.patch(uri, config_new_default_values_body)
    yield
    # ---- Teardown ----
    job.cancel_active_jobs()
    job.clear_joblog()
    outputsaver.clear_output()
    cdm.patch(uri, config_default_body)
