import time
import logging
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy

category = "job"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-73925
    +timeout: 300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_classification: System
    +test_framework: TUF
    +name:test_copy_ui_quickset_job_telemtry
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickset_job_telemtry
        +guid:3f651af0-0da0-4fea-ac9c-ac2cfffb8239
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder  & EWS=Quicksets
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_quickset_job_telemtry(job, udw, spice, net, cdm):

    # check jobId
    udw.mainApp.ScanMedia.loadMedia("ADF")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        if cdm.device_feature_cdm.is_color_supported():      
            color_mode = 'color'
        else:
            color_mode = 'grayscale'
        custom_copy_configuration_payload =  {
            "src": {
                    "scan": {
                    "colorMode": color_mode
                    }
                }
        }
        response = cdm.patch_raw(href, custom_copy_configuration_payload)
        assert response.status_code == 200, "PATCH OPERATION WAS SUCCESSFUL"
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("MyCopy", shortcut_id, "scan", ["print"], "open", "true", False, href)

        # Copy quickset job through copy app.
        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)
        spice.copy_ui().start_copy()

        # Wait for the job to complete and get the job id.
        job_id = job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        print("job id is "+ job_id_cdm)

        # Read Data and filter Job Telemetry
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
                        assert event["eventDetail"]["scanInfo"]["scanMediaSourceId"] == "adf"
                        assert event["eventDetail"]["scanInfo"]["colorMode"] == color_mode

        print("job telemetry events found: "+ str(len(eventFilteredList)))
        assert len(eventFilteredList) != 0


    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify information with some settings is displayed at a remote endpoint correctly after a idcopy job
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-18294
    +timeout: 600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_idcopy_flatbed_grayscale_best_tray3_ui_and_check_jobTelemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_flatbed_grayscale_best_tray3_ui_and_check_jobTelemetry
        +guid:785396b3-2164-4c95-90f8-e72ef1226ac3
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=GrayScale & Copy=IDCopy
        

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_flatbed_grayscale_best_tray3_ui_and_check_jobTelemetry(job, spice, net, cdm, udw):
    
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        logging.info("Unload media from ADF")
        udw.mainApp.ScanMedia.unloadMedia("ADF")

        # Id card copy job through id card copy app.
        idcopy_job_app = spice.idcard_copy_app
        idcopy_job_app.goto_idcopy()
        logging.info("Go to ID Card Copy -> Options screen")
        idcopy_job_app.goto_copy_options_list()

        logging.info("Go to ID Card Copy -> Options -> Color screen")
        idcopy_job_app.goto_idcopy_option_color_screen()

        logging.info("Set Color mode to Grayscale")
        idcopy_job_app.set_idcopy_color_options(net, idcopy_color_options="Grayscale")

        logging.info("Go to Paper Tray")
        idcopy_job_app.goto_idcopy_options_paper_tray()
        logging.info("Set Paper Tray to Tray 3")
        idcopy_job_app.set_idcopy_paper_tray_options(net, idcopy_paper_tray_options="Tray 3")

        logging.info("Go back ID Copy Landing screen from Options screen")
        idcopy_job_app.back_to_landing_view()

        logging.info("Start ID Card copy")
        idcopy_job_app.start_id_copy(dial_value=0)

        logging.info("Select continue button")
        idcopy_job_app.select_idcopy_first_continue_button()
        logging.info("Select second continue button")
        idcopy_job_app.select_idcopy_second_continue_button()

        # Wait for the job to complete and get the job id.
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
                        print("[printInfo] mediaSourceId is " + event["eventDetail"]["printInfo"]["printSettings"]["mediaRequested"]["mediaInput"]["mediaSourceId"])
                        assert event["eventDetail"]["jobInfo"]["jobCategory"] == "copy"
                        # We only check "jobCompletionState" is exist or not.
                        assert (event["eventDetail"]["jobInfo"]["jobCompletionState"] is None) == False
                        assert event["eventDetail"]["scanInfo"]["scanMediaSourceId"] == "flatbed"
                        assert event["eventDetail"]["scanInfo"]["colorMode"] == "grayscale"
                        assert event["eventDetail"]["printInfo"]["printSettings"]["mediaRequested"]["mediaInput"]["mediaSourceId"] == "tray-3"

        print("job telemetry events found: "+ str(len(eventFilteredList)))
        assert len(eventFilteredList) != 0

    finally:
        spice.goto_homescreen()
        spice.wait_ready()