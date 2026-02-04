import pytest
import logging
from tests.security.syslog.SecuritySyslogMessages import SecuritySyslogMessages as SyslogMessage
from dunetuf.servers.syslogngServer import SyslogOutcome

from dunetuf.copy.copy import Cancel

@pytest.fixture(autouse=True)
def Initialize_Cleanup(ews, cdm, udw, spice, testname, job):
    # Test Initialize
    logging.info("[test][Initialize] START ===============")
    logging.info("[test][Initialize] testname(%s)", testname)
    spice.goto_homescreen()
    ews.home.load_home_page()
    if testname == 'test_copy_syslog_completed_guest' or testname == 'test_copy_syslog_canceled_guest':
        logging.info("Clear job job")
        job.clear_joblog()
    logging.info("[test][Initialize] END ===============")

    yield [ews, cdm, udw, spice]

    # Test Cleanup
    logging.info("[test][Cleanup] START ===============")
    logging.info("[test][Cleanup] testname(%s)", testname)
    if testname == 'test_copy_syslog_completed_guest' or testname == 'test_copy_syslog_canceled_guest':
        logging.info("Clear job job")
        job.clear_joblog()
    spice.goto_homescreen()
    ews.home.load_home_page()
    logging.info("[test][Cleanup] END ===============")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify syslog of copy job (succeed)
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-55372
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_syslog_completed_guest
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Diagnostics
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_syslog_completed_guest
        +guid:23f136db-ed2f-4426-93ed-6ceb461ce4f4
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ADFMediaSize=Letter & Print=OutputScale & ScannerInput=Flatbed & Security=Syslog
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_syslog_completed_guest(copy, job, spice, configuration, syslogng):
    logging.info("======================")
    logging.info("1. Start to test: copy job")
    # check jobId
    job_ids = job.get_recent_job_ids()
    job_ids.clear()

    # OPS (enterprise)
    if configuration.familyname == "enterprise":
        # Go to copy app and start copy job
        expected_copies = 1
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()
    
    #HPS (homepro)
    else:
        expected_copies = 10
        payload = {
            'src': {
                'scan': {
                    'mediaSize': 'na_letter_8.5x11in',
                    'plexMode': 'simplex',
                    'resolution': 'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    'copies': expected_copies,
                    'mediaSize': 'na_letter_8.5x11in',
                    'plexMode': 'simplex',
                }
            }
        }
        logging.info("Send the copy job from flatbed")
        copy.do_copy_job(**payload)
    
    logging.info("======================")
    messages = syslogng.get_syslog_messages()
    for message in messages:
        logging.info("message:"+message)
    
    logging.info("======================")
    logging.info("2. Verify syslog entry was made for copy job completion")
    syslogng.wait_for_validate_syslog_message(SyslogMessage.SYSLOG_JOBCOMPLETION_COPY_MSG,
                                              outcome=SyslogOutcome.SUCCESS,
                                              clear_log=True)
    logging.info("======================")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify syslog of copy job (canceled)
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-55372
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_syslog_canceled_guest
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Diagnostics
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_syslog_canceled_guest
        +guid:d158535b-641b-49ee-ba72-34c3b68132cc
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ADFMediaSize=Letter & ScannerInput=AutomaticDocumentFeeder & Security=Syslog
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_syslog_canceled_guest(job, spice, udw, copy, syslogng):
    logging.info("======================")
    logging.info("1. Start to test: copy job")
    job.delay_job(30)

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    expected_copies = 10
    payload = {
        'src': {
            'scan': {
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'simplex',
                'resolution': 'e300Dpi',
            },
        },
        'dest': {
            'print': {
                'copies': expected_copies,
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'simplex',
            }
        }
    }

    udw.mainApp.ScanMedia.loadMedia("ADF")

    logging.info("Cancel the job after copy job is sent from ADF")
    copy.do_copy_job(cancel=Cancel.after_start, **payload)

    udw.mainApp.ScanMedia.unloadMedia("ADF")

    # Wait for the job to complete and get the job id.
    job_id = job.wait_for_completed_job(last_job_id, job, udw)
    job_id_cdm = job.get_jobid(job_id, guid=True)
    logging.info("jobId is "+ job_id_cdm)

    # Go to Homescreen and Job Queue App screen
    spice.goto_homescreen()
    spice.main_app.goto_job_queue_app()

    # Check that the job is in "History" section
    spice.job_ui.goto_job(job_id_cdm)
    assert spice.job_ui.recover_job_status() == "Canceled"

    # Check by CDM that the job has passed to history
    job_cdm = job.get_job_from_history_by_id(job_id_cdm)
    assert job_cdm["jobId"] == job_id_cdm

    logging.info("======================")
    messages = syslogng.get_syslog_messages()
    for message in messages:
        logging.info("message:"+message)
    
    logging.info("======================")
    logging.info("2. Verify syslog entry was made for copy job completion")
    syslogng.wait_for_validate_syslog_message(SyslogMessage.SYSLOG_JOBCOMPLETION_COPY_MSG,
                                              outcome=SyslogOutcome.CANCELLED,
                                              clear_log=True)
    logging.info("======================")

