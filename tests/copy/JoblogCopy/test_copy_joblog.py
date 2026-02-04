import pytest
import logging
import time

from dunetuf.copy.copy import Cancel

@pytest.fixture(autouse=True)
def Initialize_Cleanup(ews, cdm, udw, spice, testname, job):
    # Test Initialize
    logging.info("[test][Initialize] START ===============")
    logging.info("[test][Initialize] testname(%s)", testname)
    spice.goto_homescreen()
    ews.home.load_home_page()
    if testname == 'test_copy_joblog_jobdetails_completed_guest' or testname == 'test_copy_joblog_jobdetails_canceled_guest':
        logging.info("Clear job job")
        job.clear_joblog()
    logging.info("[test][Initialize] END ===============")

    yield [ews, cdm, udw, spice]

    # Test Cleanup
    logging.info("[test][Cleanup] START ===============")
    logging.info("[test][Cleanup] testname(%s)", testname)
    if testname == 'test_copy_joblog_jobdetails_completed_guest' or testname == 'test_copy_joblog_jobdetails_canceled_guest':
        logging.info("Clear job job")
        job.clear_joblog()
    spice.goto_homescreen()
    ews.home.load_home_page()
    logging.info("[test][Cleanup] END ===============")

def patch_mediaSize_with_any(payload):
    logging.info("Before patching: ")
    logging.info(payload)
    payload['src']['scan']['mediaSize'] = 'any'
    payload['dest']['print']['mediaSize'] = 'any'
    logging.info("After patching: ")
    logging.info(payload)
    return payload

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job and verify job details in Job logs
    +test_tier: 2
    +is_manual: False
    +reqid: DUNE-34710 
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_joblog_completed_guest
    +test:
        +title: test_copy_joblog_completed_guest
        +guid:d45c2dc7-5092-4e63-83ef-3b3cacd1ee3c
        +dut: 
            +type: Simulator
            +configuration: DeviceFunction=Copy
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
""" 


def test_copy_joblog_completed_guest(copy, job, configuration):
    logging.info("============================================")
    logging.info("configuration.productname=(%s)",configuration.productname)
    if configuration.productname.startswith("beam"):
        logging.info("[EXIT-TEST] this test is only valid for models which support media size=letter")
        return
    logging.info("======================")
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

    # We need to change the payload to make this test work in Jupiter. 
    if configuration.productname == "jupiter" : 
        payload = patch_mediaSize_with_any(payload)
        
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

    job_type =  new_jobs[0].get("jobType")
    assert job_type == "copy", "Unexpected job type!"

    #Username check not necessary
    #job_username = new_jobs[0].get("userName")
    #assert job_username == "guest", "Unexpected user login!"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify job details of copy job (succeed)
    +test_tier: 3
    +is_manual: False
    +reqid:DUNE-80159,DUNE-93380
    +timeout:240
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_joblog_jobdetails_completed_guest
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_joblog_jobdetails_completed_guest
        +guid:74F29173-B128-46C3-A27E-86F1AA3D7E39
        +dut: 
            +type: Simulator
            +configuration: DeviceFunction=Copy &  ADFMediaSize=Letter & JobHistory=SingleJob
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
""" 


def test_copy_joblog_jobdetails_completed_guest(copy, job, spice, udw, ews, cdm, configuration):

    logging.info("============================================")
    logging.info("configuration.productname=(%s), familynam(%s)", configuration.productname, configuration.familyname)

    # skip GSB (designjet)
    if configuration.familyname == "designjet":
        logging.info("[EXIT-TEST] this test is only valid for models with a copy function from flatbed/ADF")
        return

    logging.info("======================")
    logging.info("1. Start to test: copy job")
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    # OPS (enterprise)
    if configuration.familyname == "enterprise":
        # Go to copy app and start copy job
        expected_copies = 1
        expected_pages = 1
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()
    
    #HPS (homepro)
    else:
        expected_copies = 10
        expected_pages = 1
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

    expected_requestedCopiesCount = expected_copies
    expected_requestedImpressionCount = expected_copies * expected_pages
    expected_copiesCount = expected_copies
    expected_impressionCount = expected_copies * expected_pages
    expected_scannedPages = expected_pages

    # Wait for the job to complete and get the job id.
    job_id = job.wait_for_completed_job(last_job_id, job, udw)
    job_id_cdm = job.get_jobid(job_id, guid=True)
    logging.info("jobId is "+ job_id_cdm)

    # Go to Homescreen and Job Queue App screen
    spice.goto_homescreen()
    spice.main_app.goto_job_queue_app()

    # Check that the job is in "History" section
    spice.job_ui.goto_job(job_id_cdm)
    assert spice.job_ui.recover_job_status() == "Completed"

    # Check by CDM that the job has passed to history
    job_cdm = job.get_job_from_history_by_id(job_id_cdm)
    assert job_cdm["jobId"] == job_id_cdm

    logging.info("======================")
    logging.info("2. Verify job details on CDM")
    job.verify_jobdetails_stats_data(cdm, job, "copy", expected_copies, expected_pages)

    logging.info("======================")
    logging.info("3. expected")
    expected = {"Scanned Pages": f'{expected_scannedPages}', "Copies": f'{expected_copiesCount}/{expected_requestedCopiesCount}', "Pages": f'{expected_impressionCount}', "Total Pages": f'{expected_requestedImpressionCount}',
        "Job Name": "Copy", "Status": "Completed", #"User Name": "Guest",
        "Job Type": "Copy",
        'Trays': 'Automatic', 'Paper Type': 'Plain', 'Output Size': 'Letter (8.5x11 in.)',
        'Resolution': '300 dpi', 'Quality': 'Normal', 'Color Mode': 'Color',
        'Original Size': 'Letter (8.5x11 in.)',
        'Original Sides': '1-Sided'}
    if configuration.familyname == "enterprise":
        expected.update({"Resolution": "600 dpi"})
        expected.update({"Color Mode": "Automatic"})

    logging.info(expected)

    logging.info("======================")
    logging.info("4. Verify job details on CP")
    job.verify_job_details_on_CP(job, spice, configuration.productname, "completed", "copy", expected)

    logging.info("======================")
    logging.info("5. Verify job details on EWS")
    expected.update({"Copies": f'{expected_copiesCount} of {expected_requestedCopiesCount}'})
    job.verify_job_details_on_EWS(job, ews, configuration.productname, "completed", "copy", expected)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify job details of copy job (canceled)
    +test_tier: 3 
    +is_manual: False
    +reqid:DUNE-80159,DUNE-93380
    +timeout:180
    +asset: Copy
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_joblog_jobdetails_canceled_guest
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_joblog_jobdetails_canceled_guest
        +guid:7771E099-94F0-429C-9145-4027C018096B
        +dut: 
            +type: Simulator
            +configuration: DeviceFunction=Copy & JobHistory=MultipleJobs
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_joblog_jobdetails_canceled_guest(job, spice, udw, copy, cdm, ews, configuration, counters):
    logging.info("============================================")
    logging.info("configuration.productname=(%s), familynam(%s)", configuration.productname, configuration.familyname)
    if configuration.familyname == "designjet":
        logging.info("[EXIT-TEST] this test is only valid for models with a copy function from flatbed/ADF")
        return
    counters.scan.clear_counters()
    counters.job.clear_counters()
    
    logging.info("======================")
    logging.info("1. Start to test: copy job")
    job.delay_job(30)

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    expected_copies = 10    # i.e. requested copies
    expected_pages = 0
    expected_scannedPages = 0 # expected_pages, Scanned Page Count is increased once scan starts hence for cancel case the count is still 1
    expected_requestedCopiesCount = expected_copies
    expected_requestedImpressionCount = expected_copies * expected_pages
    expected_copiesCount = 0 # expected_copies
    expected_impressionCount = 0 # expected_copies * expected_pages
    mediaSize = "na_letter_8.5x11in"
    if "beam" in configuration.productname:
        mediaSize = 'any'

    payload = {
        'src': {
            'scan': {
                'mediaSize': mediaSize,
                'plexMode': 'simplex',
                'resolution': 'e300Dpi',
            },
        },
        'dest': {
            'print': {
                'copies': expected_copies,
                'mediaSize': mediaSize,
                'plexMode': 'simplex',
            }
        }
    }
    if configuration.familyname == "enterprise":
        payload['src']['scan']['resolution'] = 'e600Dpi'

    udw.mainApp.ScanMedia.loadMedia("ADF")

    logging.info("Cancel the job after copy job is sent from ADF")
    copy.do_copy_job(cancel=Cancel.after_start, **payload)

    time.sleep(2)
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

    #DUNE-230023 Timing in Selene causes the cancel to happen after scanning is done
    #Updating the expected pages and impression count if scanned pages > 0
    response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + job_id_cdm)
    assert response.status_code==200, 'Unexpected response'
    cdm_response = response.json()
    logging.info(cdm_response)
    if cdm_response['scanInfo']['scannedPageCount'] != 0:
        logging.info("Scanned Page Count is not 0")
        expected_pages = cdm_response['scanInfo']['scannedPageCount']
        expected_requestedImpressionCount = expected_copies * expected_pages

    logging.info("======================")
    logging.info("2. Verify job details on CDM")
    job.verify_jobdetails_stats_data(cdm, job, "copy", expected_copies, expected_pages)

    logging.info("======================")
    logging.info("3. expected")
    expected_requestedImpressionCount_str = f'{expected_requestedImpressionCount}' if expected_requestedImpressionCount > 0 else '--'
    expected = {"Scanned Pages": f'{expected_scannedPages}', "Copies": f'{expected_copiesCount}/{expected_requestedCopiesCount}', "Pages": f'{expected_impressionCount}', "Total Pages": f'{expected_requestedImpressionCount_str}',
        "Status": "Canceled", "Job Type": "Copy",
        }
    if configuration.familyname == "enterprise":
        expected.update({"Color Mode": "Automatic"})
        expected.update({"Resolution": "600 dpi"})
    logging.info(expected)

    logging.info("======================")
    logging.info("4. Verify job details on CP")
    job.verify_job_details_on_CP(job, spice, configuration.productname, "canceled", "copy", expected)

    logging.info("======================")
    logging.info("5. Verify job details on EWS")
    expected.update({"Copies": f'{expected_copiesCount} of {expected_requestedCopiesCount}'})
    job.verify_job_details_on_EWS(job, ews, configuration.productname, "canceled", "copy", expected)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform ID Copy job and verify job details in Job logs
    +test_tier: 2 
    +is_manual: False
    +reqid: DUNE-34710
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_Copyid_joblog_cancelled_guest
    +test:
        +title: test_Copyid_joblog_cancelled_guest
        +guid:1647575b-4301-4618-968c-2125eb6c9261
        +dut: 
            +type: Simulator
            +configuration: DeviceFunction=Copy
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_Copyid_joblog_cancelled_guest(job, udw, copy, configuration):
    logging.info("============================================")
    logging.info("configuration.productname=(%s)",configuration.productname)
    if configuration.productname == "jupiter" or configuration.productname.startswith("beam"):
        logging.info("[EXIT-TEST] this test is only valid for models with a copy function from flatbed/ADF")
        return

    logging.info("======================")
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

    default_media = "ADF"

    # We need to change the payload and the media to make this test work in Jupiter. 
    if configuration.productname == "jupiter" : 
        payload = patch_mediaSize_with_any(payload)
        default_media = "MDF"

    udw.mainApp.ScanMedia.loadMedia(default_media)

    logging.info("Cancel the job after copy job is sent from ADF")
    copy.do_copy_job(cancel=Cancel.after_start, **payload)

    udw.mainApp.ScanMedia.unloadMedia(default_media)

    job_queue = job.get_job_queue()
    assert len(job_queue) == 0, "Job Queue not cleared after job completion"

    new_jobs = job.get_newjobs()
    assert len(new_jobs) == 1, "Unexpected number of new jobs!"

    job_state = new_jobs[0].get("state")
    assert job_state == "completed", "Unexpected job state!"

    job_type =  new_jobs[0].get("jobType")
    assert job_type == "copy", "Unexpected job type!"

    #Username check not necessary
    #job_username = new_jobs[0].get("userName")
    #assert job_username == "guest", "Unexpected user login!"

    job_completionstate = new_jobs[0].get("completionState")
    assert job_completionstate in 'cancelled', "Unexpected job completion state!"
