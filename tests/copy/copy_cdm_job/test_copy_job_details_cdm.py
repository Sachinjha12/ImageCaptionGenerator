import logging
from datetime import datetime

from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A0 and check its jobs details in job queue from cdm
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-117175
    +timeout:120
    +asset: LFP
    +test_framework: TUF
    +name: test_copy_job_details_cdm
    +test:
        +title: test_copy_job_details_cdm
        +guid: 43259dfe-ef1c-11ed-b091-37cb300937d9
        +dut:
            +type:Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceFunction=Copy & EngineFirmwareFamily=Maia
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_job_details_cdm(setup_teardown_with_copy_job, cdm, udw, tcl, usb, job, copy):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan
    height_in_mm = 1189
    width_in_mm = 841

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
    }
    # Do one copy with the settings
    copy.copy_simulation(height_in_mm, width_in_mm, settings, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Check if the job stats for the specific jobId returns success
    response = cdm.get_raw(cdm.JOB_STATS_ENDPOINT.format(job.get_jobid(job_id)))
    logging.info(response)
    assert response.status_code==200, 'Unexpected response'
    
    response_job_stats = response.json()
    logging.info(response_job_stats)

    assert "jobInfo" in response_job_stats, 'jobInfo is null'
    assert "printInfo" in response_job_stats, 'printInfo is null'
    assert "scanInfo" in response_job_stats, 'scanInfo is null'
    assert response_job_stats["printInfo"]["usageByPrintCategory"][0]["pageCount"] == 1, 'unexpected page count'
    assert response_job_stats["printInfo"]["impressionCount"] == 1, 'unexpected impression count'
    assert response_job_stats["printInfo"]["copiesCount"] == 1, 'unexpected copies count'
    assert response_job_stats['jobInfo']['startTime'] != "", 'Unexpected start time'
    assert response_job_stats['jobInfo']['endTime'] != "", 'Unexpected end time'
    assert check_timedelta(response_job_stats['jobInfo']['endTime'], response_job_stats['jobInfo']['startTime']).days >= 0
    assert response_job_stats['jobInfo']['userName'] != "", 'Unexpected username'
    assert response_job_stats['jobInfo']['jobCategory'] == "copy", 'Unexpected job category'
    assert response_job_stats["printInfo"]["printSettings"]["mediaRequested"]["mediaInput"]["mediaSourceId"] == "auto", 'Unexpected media source id'
    assert response_job_stats["printInfo"]["usageByMediaSourceAttributes"][0]["mediaTypeId"] == "custom", 'Unexpected media type id'
    # assert response_job_stats["scanInfo"]["mediaSize"] == "any", 'Unexpected media size'
    assert response_job_stats["scanInfo"]["xResolution"] == "e300Dpi", 'Unexpected xResolution'
    assert response_job_stats["printInfo"]["printSettings"]["printQuality"] == "draft", 'Unexpected print quality'
    assert response_job_stats["scanInfo"]["colorMode"] == "color", 'Unexpected color mode'


def check_timedelta(timedelta_1, timedelta_2):
    time_delta_1 = datetime.strptime(timedelta_1, '%Y-%m-%dT%H:%M:%SZ')
    time_delta_2 = datetime.strptime(timedelta_2, '%Y-%m-%dT%H:%M:%SZ')
    return time_delta_1 - time_delta_2