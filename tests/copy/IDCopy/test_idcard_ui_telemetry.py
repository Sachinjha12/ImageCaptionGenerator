import logging
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy

category = "job"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check that job telemetry works properly for copy with adf and color.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-73925
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +timeout: 300
    +test_framework: TUF
    +name: test_copy_ui_idcopy_job_telemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_idcopy_job_telemetry
        +guid:000a61be-6043-4d24-9c35-c0347f7ed32f
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_idcopy_job_telemetry(job, spice, net, cdm, udw):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        job.bookmark_jobs()
        # Id card copy job through id card copy app.
        copy_job_app = spice.copy_ui()
        if cdm.device_feature_cdm.is_color_supported():
            color_mode = 'Color'
        else:
            color_mode = 'Grayscale'
        options = {
            'colorMode': color_mode
            }
        loadmedia='Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)

        # Wait for the job to complete and get the job id.
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
        job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        logging.info("jobId is "+ job_id_cdm)

        #Read Data and filter Job Telemetry
        eventFilteredList = []
        r = cdm.get_raw(cdm.EVENTING_EVENTS)
        assert r.status_code == 200
        eventList = r.json()

        if "events" in eventList:
            for event in eventList["events"]:
                if event["eventCategory"] == category:
                    if event["eventDetail"]["jobInfo"]["jobUuid"] == job_id_cdm:
                        eventFilteredList.append(event)
                        print("[jobInfo] jobUuid is " + event["eventDetail"]["jobInfo"]["jobUuid"])
                        print("[jobInfo] jobCategory is " + event["eventDetail"]["jobInfo"]["jobCategory"])
                        print("[jobInfo] jobCompletionState is " + event["eventDetail"]["jobInfo"]["jobCompletionState"])
                        print("[scanInfo] scanMediaSourceId is " + event["eventDetail"]["scanInfo"]["scanMediaSourceId"])
                        print("[scanInfo] colorMode is " + event["eventDetail"]["scanInfo"]["colorMode"])
                        assert event["eventDetail"]["jobInfo"]["jobCategory"] == "copy"
                        # We only check "jobCompletionState" is exist or not.
                        assert (event["eventDetail"]["jobInfo"]["jobCompletionState"] is None) == False
                        assert event["eventDetail"]["scanInfo"]["scanMediaSourceId"] == "flatbed"
                        assert event["eventDetail"]["scanInfo"]["colorMode"] == color_mode.lower()

        print("job telemetry events found: "+ str(len(eventFilteredList)))
        assert len(eventFilteredList) != 0

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
