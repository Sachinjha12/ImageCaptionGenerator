import pytest
import logging

from dunetuf.copy.copy import Cancel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Send simple copy job and verify Job Log
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-24136
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_joblog_flatbed_cdm_copy
    +test:
        +title: test_joblog_flatbed_cdm_copy
        +guid: ff774ac4-b6d0-4cec-972b-02g72c83369b
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & DeviceClass=MFP & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_joblog_flatbed_cdm_copy(copy, job):
    job.bookmark_jobs()

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
                'copies': 10,
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'simplex',
            }
        }
    }

    logging.info("Send the copy job from flatbed")
    copy.do_copy_job(**payload)

    job_queue = job.get_job_queue()
    assert len(job_queue) == 0, "Job Queue not cleared after job completion"

    new_jobs = job.get_newjobs()
    assert len(new_jobs) == 1, 'Unexpected number of new jobs!'

    job_state = new_jobs[0].get("state")
    assert job_state == "completed", "Unexpected job state!"

    job_completionstate = new_jobs[0].get("completionState")
    assert job_completionstate in ['success', 'failed', 'cancelled'], "Unexpected job completion state!"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Send and cancel adf copy job and verify Job Log
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-24136
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_joblog_adf_cdm_copy_cancel
    +test:
        +title: test_joblog_adf_cdm_copy_cancel
        +guid: ff774ac4-b7e0-4ced-962b-04g72c83389b
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & DeviceClass=MFP & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_joblog_adf_cdm_copy_cancel(job, udw, copy, scan_emulation):
    job.delay_job(30)
    job.bookmark_jobs()

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
                'copies': 10,
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'simplex',
            }
        }
    }
    scan_emulation.media.load_media(media_id='ADF', media_numsheet=1)  
    # udw.mainApp.ScanMedia.loadMedia("ADF")

    logging.info("Cancel the job after copy job is sent from ADF")
    copy.do_copy_job(cancel=Cancel.after_start, **payload)
    scan_emulation.media.unload_media("ADF")
    # udw.mainApp.ScanMedia.unloadMedia("ADF")
    
    try:

        job_queue = job.get_job_queue()
        assert len(job_queue) == 0, "Job Queue not cleared after job completion"

        new_jobs = job.get_newjobs()
        assert len(new_jobs) == 1, "Unexpected number of new jobs!"

        job_state = new_jobs[0].get("state")
        assert job_state == "completed", "Unexpected job state!"

        job_completionstate = new_jobs[0].get("completionState")
        assert job_completionstate in 'cancelled', "Unexpected job completion state!"

    finally:
        scan_emulation.media.load_media('ADF',1)
        # udw.mainApp.ScanMedia.loadMedia("ADF")


