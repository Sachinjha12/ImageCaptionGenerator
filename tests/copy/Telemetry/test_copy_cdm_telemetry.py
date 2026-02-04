#!/usr/bin/python3

import json
import os
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.control.control import Control

TESTRESOURCEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')

category = "job"

copy_job_payload = {
    'src': {
        'scan': {
            'colorMode':'color',
            'mediaSize':'na_letter_8.5x11in',
            'plexMode':'simplex',
            'resolution':'e300Dpi',
            'mediaSource':'adf',
            'contentType':'mixed',
        },
    },
    'dest': {
        'print': {
            'copies': 1,
            'mediaSource': 'auto',
            'mediaSize':'na_letter_8.5x11in',
            'mediaType': 'stationery',
            'plexMode':'simplex',
            'printQuality' : 'normal',
        }
    },
    'pipelineOptions': {
        'imageModifications': {
            'exposure': 5,
        },
        'scaling': {
            'xScalePercent': 100,
            'yScalePercent': 100,
        }
    }
}

def get_device_counters(cdm):
    """
    Retrieves the device counters from the CDM.

    Args:
        cdm: The CDM object used to make the API call.

    Returns:
        A dictionary containing the device counters.
    """

    response = cdm.get_raw(cdm.DEVICE_USAGE_LIFETIME_COUNTERS)
    assert response.status_code == 200
    data = json.loads(response.content)
    return data

def check_for_impressions(before, after):
    """
    Check if the impressions counters have been properly updated.

    Args:
        before (dict): Dictionary containing the impression counters before the update.
        after (dict): Dictionary containing the impression counters after the update.

    Raises:
        AssertionError: If the length of `before` or `after` is not equal to 3 + 1, or if the color mode counters have not been increased properly, or if the total counter has not been increased properly.
    """

    assert len(before) == 3 + 1, "A new color mode has been added to impressions"
    assert len(after) == 3 + 1, "A new color mode has been added to impressions"

    color_mode_tests = [
        before["monochrome"] < after["monochrome"],
        before["color"] < after["color"],
        before["fullColor"] < after["fullColor"]
    ]
    assert color_mode_tests.count(True) == 1, "Color mode counters have not been increased properly. List of results: {0}".format(color_mode_tests)
    assert before["total"] < after["total"]


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
    +timeout: 120
    +test_framework: TUF
    +name: test_copy_adf_color_job_telemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_adf_color_job_telemetry
        +guid:d8626972-04b5-4663-95aa-ad5b9c908c76
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & DeviceFunction=CopyColor 
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_adf_color_job_telemetry(cdm, copy, job):

    # Set mediasource and colormode
    copy_job_payload['src']['scan']['colorMode'] = 'color'
    copy_job_payload['src']['scan']['mediaSource'] = 'adf'

    # Copy job
    copy.do_copy_job(**copy_job_payload)

    # Get Job ID
    job_id = job.get_last_job_id_cdm()
    print("jobId is "+ job_id)

    # Read Data and filter Job Telemetry
    eventFilteredList = []
    r = cdm.get_raw(cdm.EVENTING_EVENTS)
    assert r.status_code == 200
    eventList = r.json()

    if "events" in eventList:
        for event in eventList["events"]:
            if event["eventCategory"] == category:
                if event["eventDetail"]["jobInfo"]["jobUuid"] == job_id:
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
                    assert event["eventDetail"]["scanInfo"]["colorMode"] == "color"


    print("job telemetry events found: "+ str(len(eventFilteredList)))
    assert len(eventFilteredList) != 0

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check that job telemetry works properly for copy with flatbed and grayscale.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-73925
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +timeout: 120
    +test_framework: TUF
    +name: test_copy_flatbed_grayscale_job_telemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_flatbed_grayscale_job_telemetry
        +guid:fd1da3d5-3d7b-4acd-adf4-b4b2665c8d13
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=GrayScale
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_flatbed_grayscale_job_telemetry(cdm, copy, job, configuration, udw):

    # Set mediasource and colormode
    copy_job_payload['src']['scan']['colorMode'] = 'grayscale'
    copy_job_payload['src']['scan']['mediaSource'] = 'flatbed'

    udw.mainApp.ScanMedia.unloadMedia("ADF")

    # Copy job
    copy.do_copy_job(familyname = configuration.familyname,**copy_job_payload)

    # Get Job ID
    job_id = job.get_last_job_id_cdm()
    print("jobId is "+ job_id)

    # Read Data and filter Job Telemetry
    eventFilteredList = []
    r = cdm.get_raw(cdm.EVENTING_EVENTS)
    assert r.status_code == 200
    eventList = r.json()

    if "events" in eventList:
        for event in eventList["events"]:
            if event["eventCategory"] == category:
                if event["eventDetail"]["jobInfo"]["jobUuid"] == job_id:
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
                    assert event["eventDetail"]["scanInfo"]["colorMode"] == "grayscale"


    print("job telemetry events found: "+ str(len(eventFilteredList)))
    assert len(eventFilteredList) != 0

    udw.mainApp.ScanMedia.loadMedia("ADF")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check that job telemetry works properly for canceled copy job.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-73925
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +timeout: 120
    +test_framework: TUF
    +name: test_copy_cancel_job_telemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cancel_job_telemetry
        +guid:2837a06e-286d-4397-9c9f-32177f2039bf
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder 
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cancel_job_telemetry(cdm, copy, job, configuration):

    # Set mediasource and colormode
    if cdm.device_feature_cdm.is_color_supported():
        copy_job_payload['src']['scan']['colorMode'] = 'color'  
    else:
        copy_job_payload['src']['scan']['colorMode'] = 'grayscale'
    copy_job_payload['src']['scan']['mediaSource'] = 'adf'
    copy_job_payload['dest']['print']['plexMode'] = 'simplex'
    copy_job_payload['dest']['print']['printQuality'] = 'normal'

    # Cancel copy job after job started
    copy.do_copy_job(cancel=Cancel.after_start, familyname = configuration.familyname, **copy_job_payload)

    # Get Job ID
    job_id = job.get_last_job_id_cdm()
    print("jobId is "+ job_id)

    # Read Data and filter Job Telemetry
    eventFilteredList = []
    r = cdm.get_raw(cdm.EVENTING_EVENTS)
    assert r.status_code == 200
    eventList = r.json()

    if "events" in eventList:
        for event in eventList["events"]:
            if event["eventCategory"] == category:
                if event["eventDetail"]["jobInfo"]["jobUuid"] == job_id:
                    eventFilteredList.append(event)
                    print("[jobInfo] jobUuid is " + event["eventDetail"]["jobInfo"]["jobUuid"])
                    print("[jobInfo] jobCategory is " + event["eventDetail"]["jobInfo"]["jobCategory"])
                    print("[jobInfo] jobCompletionState is " + event["eventDetail"]["jobInfo"]["jobCompletionState"])
                    print("[printInfo] plexMode is " + event["eventDetail"]["printInfo"]["printSettings"]["plexMode"])
                    print("[printInfo] printQuality is " + event["eventDetail"]["printInfo"]["printSettings"]["printQuality"])
                    print("[scanInfo] scanMediaSourceId is " + event["eventDetail"]["scanInfo"]["scanMediaSourceId"])
                    print("[scanInfo] colorMode is " + event["eventDetail"]["scanInfo"]["colorMode"])
                    assert event["eventDetail"]["jobInfo"]["jobCategory"] == "copy"
                    # We check on state of jobCompletionState is "cancelled".
                    assert event["eventDetail"]["jobInfo"]["jobCompletionState"] == "cancelled"
                    assert event["eventDetail"]["printInfo"]["printSettings"]["plexMode"] == "simplex"
                    assert event["eventDetail"]["printInfo"]["printSettings"]["printQuality"] == "normal"
                    assert event["eventDetail"]["scanInfo"]["scanMediaSourceId"] == "adf"
                    if cdm.device_feature_cdm.is_color_supported():
                        assert event["eventDetail"]["scanInfo"]["colorMode"] == "color"
                    else:
                        assert event["eventDetail"]["scanInfo"]["colorMode"] == "grayscale"
                    


    print("job telemetry events found: "+ str(len(eventFilteredList)))
    assert len(eventFilteredList) != 0

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that the information with all fields in the payload is displayed correctly after copy job is performed
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-18294
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_adf_grayscale_200dpi_a4_CDM_and_check_jobTelemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_adf_grayscale_200dpi_a4_CDM_and_check_jobTelemetry
        +guid:9dbaeb10-a54b-4609-8dc2-1b5f625a0d67
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=GrayScale & Copy=Quality & ADFResolution=200dpi
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_adf_grayscale_200dpi_a4_CDM_and_check_jobTelemetry(cdm, copy, job):
    
    # Set mediasource, colormode, resolution and mediasize
    copy_job_payload['src']['scan']['mediaSource'] = 'adf'
    copy_job_payload['src']['scan']['colorMode'] = 'grayscale'
    copy_job_payload['src']['scan']['resolution'] = 'e200Dpi'
    copy_job_payload['src']['scan']['mediaSize'] = 'iso_a4_210x297mm'

    # Copy job
    copy.do_copy_job(**copy_job_payload)

    # Get Job ID
    job_id = job.get_last_job_id_cdm()
    print("jobId is "+ job_id)

    # Read Data and filter Job Telemetry
    eventFilteredList = []
    r = cdm.get_raw(cdm.EVENTING_EVENTS)
    assert r.status_code == 200
    eventList = r.json()

    if "events" in eventList:
        for event in eventList["events"]:
            if event["eventCategory"] == category:
                if event["eventDetail"]["jobInfo"]["jobUuid"] == job_id:
                    eventFilteredList.append(event)
                    print("[jobInfo] jobUuid is " + event["eventDetail"]["jobInfo"]["jobUuid"])
                    print("[jobInfo] jobCategory is " + event["eventDetail"]["jobInfo"]["jobCategory"])
                    print("[jobInfo] jobCompletionState is " + event["eventDetail"]["jobInfo"]["jobCompletionState"])
                    print("[scanInfo] scanMediaSourceId is " + event["eventDetail"]["scanInfo"]["scanMediaSourceId"])
                    print("[scanInfo] colorMode is " + event["eventDetail"]["scanInfo"]["colorMode"])
                    print("[scanInfo] xResolution is " + event["eventDetail"]["scanInfo"]["xResolution"])
                    print("[scanInfo] mediaSize is " + event["eventDetail"]["scanInfo"]["mediaSize"])
                    assert event["eventDetail"]["jobInfo"]["jobCategory"] == "copy"
                    # We only check "jobCompletionState" is exist or not.
                    assert (event["eventDetail"]["jobInfo"]["jobCompletionState"] is None) == False
                    assert event["eventDetail"]["scanInfo"]["scanMediaSourceId"] == "adf"
                    assert event["eventDetail"]["scanInfo"]["colorMode"] == "grayscale"
                    assert event["eventDetail"]["scanInfo"]["xResolution"] == "e200Dpi"
                    assert event["eventDetail"]["scanInfo"]["mediaSize"] == "iso_a4_210x297mm"


    print("job telemetry events found: "+ str(len(eventFilteredList)))
    assert len(eventFilteredList) != 0

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that the information with all fields in the payload is displayed correctly after copy job is performed
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-18294
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_flatbed_color_300dpi_b5_2sided_CDM_and_check_jobTelemetry
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_flatbed_color_300dpi_b5_2sided_CDM_and_check_jobTelemetry
        +guid:da740c4f-f7e3-4856-9400-f0535ed90eaa
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=Quality & Copy=2Sided2To1
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_flatbed_color_300dpi_b5_2sided_CDM_and_check_jobTelemetry(cdm, udw):
    
    # Set mediasource, colormode, resolution, mediasize and plexmode
    copy_job_payload['src']['scan']['mediaSource'] = 'flatbed'
    if cdm.device_feature_cdm.is_color_supported():
        colorMode = 'color'
    else:
        colorMode = 'grayscale'
    copy_job_payload['src']['scan']['colorMode'] = colorMode
    copy_job_payload['src']['scan']['resolution'] = 'e300Dpi'
    copy_job_payload['src']['scan']['mediaSize'] = 'jis_b5_182x257mm'
    copy_job_payload['src']['scan']['plexMode'] = 'duplex'

     # perform Copy Job and then get Job ID
    job_id = Copy(cdm, udw).start_copy_job(**copy_job_payload)
    job = Job(cdm, udw)
    job.wait_for_alerts('scanManualDuplexSecondPage')
    job.alert_action('scanManualDuplexSecondPage', 'Response_01')
    job.check_job_state(job_id, 'completed', 60)
        
    # Get Job ID
    print("jobId is "+ job_id)

    # Read Data and filter Job Telemetry
    eventFilteredList = []
    r = cdm.get_raw(cdm.EVENTING_EVENTS)
    assert r.status_code == 200
    eventList = r.json()

    if "events" in eventList:
        for event in eventList["events"]:
            if event["eventCategory"] == category:
                if event["eventDetail"]["jobInfo"]["jobUuid"] == job_id:
                    eventFilteredList.append(event)
                    print("[jobInfo] jobUuid is " + event["eventDetail"]["jobInfo"]["jobUuid"])
                    print("[jobInfo] jobCategory is " + event["eventDetail"]["jobInfo"]["jobCategory"])
                    print("[jobInfo] jobCompletionState is " + event["eventDetail"]["jobInfo"]["jobCompletionState"])
                    print("[scanInfo] scanMediaSourceId is " + event["eventDetail"]["scanInfo"]["scanMediaSourceId"])
                    print("[scanInfo] colorMode is " + event["eventDetail"]["scanInfo"]["colorMode"])
                    print("[scanInfo] xResolution is " + event["eventDetail"]["scanInfo"]["xResolution"])
                    print("[scanInfo] mediaSize is " + event["eventDetail"]["scanInfo"]["mediaSize"])
                    print("[scanInfo] plexMode is " + event["eventDetail"]["scanInfo"]["plexMode"])
                    assert event["eventDetail"]["jobInfo"]["jobCategory"] == "copy"
                    # We only check "jobCompletionState" is exist or not.
                    assert (event["eventDetail"]["jobInfo"]["jobCompletionState"] is None) == False
                    assert event["eventDetail"]["scanInfo"]["scanMediaSourceId"] == "flatbed"
                    assert event["eventDetail"]["scanInfo"]["colorMode"] == colorMode
                    assert event["eventDetail"]["scanInfo"]["xResolution"] == "e300Dpi"
                    assert event["eventDetail"]["scanInfo"]["mediaSize"] == "jis_b5_182x257mm"
                    assert event["eventDetail"]["scanInfo"]["plexMode"] == "duplex"

    print("job telemetry events found: "+ str(len(eventFilteredList)))
    assert len(eventFilteredList) != 0

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test with a simulated 200x100mm that copy scanInfo data is correct
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-125135
    +timeout: 200
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_cdm_mdf_landingpagecopy_scan_info_telemetry
    +test:
        +title: test_copy_cdm_mdf_landingpagecopy_scan_info_telemetry
        +guid:71e77bf6-7f7f-4ead-8a13-7e9eec865a45
        +dut:
            +type: Simulator
            +configuration:PrintEngineFormat=A4 & DeviceClass=MFP & DeviceFunction=Copy & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_mdf_landingpagecopy_scan_info_telemetry(tcl, cdm, udw, copy, configuration, job):
    # Create configuration Scan
    height = 200 # mm
    width = 100 # mm

    # Init simulation
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw).set_configuration(configuration)
    simulation = scan_action.set_scan_random_acquisition_mode(height, width)
    Control.validate_simulation(simulation)
    copy_job_id = copy.do_copy_job()
    job.wait_for_job_completion_cdm(copy_job_id)

    # Restore default scan simulation mode
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)

    # Read Data and filter Job Telemetry
    response = cdm.get_raw(cdm.EVENTING_EVENTS)
    assert response.status_code == 200

    # Check last job finish correctly
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    job_scan_info_stats = {}

    # Obtain the scanInfo of last job
    eventList = response.json()
    if "events" in eventList:
        for event in eventList["events"]:
            if event["eventCategory"] == "job":
                if event["eventDetail"]["jobInfo"]["jobUuid"] == new_jobs[-1].get('jobId'):
                    job_scan_info_stats = event["eventDetail"]["scanInfo"]

    assert job_scan_info_stats["colorMode"] == "color"
    assert job_scan_info_stats["mediaOrientation"] == "portrait"
    assert job_scan_info_stats["scanMediaSourceId"] == "mdf"
    assert job_scan_info_stats["scannedPageCount"] == 1
    assert job_scan_info_stats["xResolution"] == "e300Dpi"
    assert job_scan_info_stats["yResolution"] == "e300Dpi"

    # TO BE FIXED
    # Currently, Jupiter simulator environment applies edge detection
    # even if scan simulator strategy is set to random. Images coming
    # from random strategy do not have the usual scanner gray background
    # and edge detection has an unexpected input and clips the image.
    new_width = 90
    min_area = (height / 10) * (new_width / 10)
    max_area = (height / 10) * (width / 10)

    assert min_area <= job_scan_info_stats["scanAreaUsage"]["scanArea"]["count"] <= max_area
    assert job_scan_info_stats["scanAreaUsage"]["scanArea"]["unit"] == "sqcm"
    assert job_scan_info_stats["scanAreaUsage"]["scanLength"]["count"] == height
    assert job_scan_info_stats["scanAreaUsage"]["scanLength"]["unit"] == "millimeters"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test with a simulated 200x100mm that copy scanInfo data is correct
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-125135
    +timeout: 200
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_cdm_mdf_landingpagecopy_scan_info_telemetry_reported_in_history_stats
    +test:
        +title: test_copy_cdm_mdf_landingpagecopy_scan_info_telemetry_reported_in_history_stats
        +guid:fc12a532-aa90-4788-9dae-f3d4b4e47f06
        +dut:
            +type: Simulator
            +configuration:PrintEngineFormat=A4 & DeviceClass=MFP & DeviceFunction=Copy & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_mdf_landingpagecopy_scan_info_telemetry_reported_in_history_stats(tcl, cdm, udw, copy, configuration, job):
    # Create configuration Scan
    height_in_mm = 200 # mm
    width_in_mm = 100 # mm

    # Init simulation
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw).set_configuration(configuration)
    simulation = scan_action.set_scan_random_acquisition_mode(height_in_mm, width_in_mm)
    Control.validate_simulation(simulation)
    copy_job_id = copy.do_copy_job()
    job.wait_for_job_completion_cdm(copy_job_id)

    # Restore default scan simulation mode
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)

    # Read Data and filter Job Telemetry
    response = cdm.get_raw(cdm.JOB_HISTORY_STATS_ENDPOINT)
    assert response.status_code == 200
    # get last job's historyStats
    job_scan_info_stats = response.json()["historyStats"][-1]["scanInfo"]

    assert job_scan_info_stats["colorMode"] == "color"
    assert job_scan_info_stats["mediaOrientation"] == "portrait"
    assert job_scan_info_stats["scanMediaSourceId"] == "mdf"
    assert job_scan_info_stats["scannedPageCount"] == 1
    assert job_scan_info_stats["xResolution"] == "e300Dpi"
    assert job_scan_info_stats["yResolution"] == "e300Dpi"

    # TO BE FIXED
    # Currently, Jupiter simulator environment applies edge detection
    # even if scan simulator strategy is set to random. Images coming
    # from random strategy do not have the usual scanner gray background
    # and edge detection has an unexpected input and clips the image.
    new_width_in_mm = 90
    factor_mm_to_cm = 0.1
    min_area_in_mm  = (height_in_mm * factor_mm_to_cm) * (new_width_in_mm * factor_mm_to_cm)
    max_area_in_mm  = (height_in_mm * factor_mm_to_cm) * (width_in_mm * factor_mm_to_cm)

    assert min_area_in_mm  <= job_scan_info_stats["scanAreaUsage"]["scanArea"]["count"] <= max_area_in_mm 
    assert job_scan_info_stats["scanAreaUsage"]["scanArea"]["unit"] == "sqcm"
    assert job_scan_info_stats["scanAreaUsage"]["scanLength"]["count"] == height_in_mm
    assert job_scan_info_stats["scanAreaUsage"]["scanLength"]["unit"] == "millimeters"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checking if counters properly update after copy job.
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5924
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +test_classification:System
    +external_files: A4_Color_200_with_margins.ppm=87add0647f8e21b9c9c7cdf189fe87a75702f5b5ed0bae7db061627c18538422
    +name:test_lifetime_counter_copy_maia
    +test:
        +title:test_lifetime_counter_copy_maia
        +guid:4e13b103-73fe-4716-ac9d-8ed9ed9e6e07
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=Maia & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_lifetime_counter_copy_maia(cdm, udw, ssh, copy, job, tcl, tclMaia, scp, configuration):

    try:
        tclMaia.execute("setEmulatorReady", recvTimeout=20)
        printer_type = "emulator"
    except:
        printer_type ="simulator"
    
    scan_action = ScanAction()
    scan_action.set_scp(scp).set_udw(udw).set_tcl(tcl).set_configuration(configuration)

    # Create configuration Scan A4
    height_in_mm = 307 # 297 length A4 + 5mm margin offset
    area_diff_in_cm2 = 645 # ~ 307 * 217 / 100

    height_threshold = height_in_mm / 100 #Max acceptable error: 1% of length
    area_threshold = area_diff_in_cm2 / 100 #Max acceptable error: 1% of area

    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e200Dpi",
        "dest": "print",
        "copies": 1,
    }

    job.clear_joblog()
    init_count = get_device_counters(cdm)
    file = '87add0647f8e21b9c9c7cdf189fe87a75702f5b5ed0bae7db061627c18538422'
    copy.copy_pnm_simulation_force_start_CDM(file, settings, job, ssh, scan_action)
    final_count = get_device_counters(cdm)

    # Get counters and check before and after.
    assert init_count["jobUsage"]["copyJobCount"] < final_count["jobUsage"]["copyJobCount"]

    check_for_impressions(init_count["printUsage"]["impressions"], final_count["printUsage"]["impressions"])
    check_for_impressions(init_count["printUsage"]["copyImpressions"], final_count["printUsage"]["copyImpressions"])

    assert init_count["printUsage"]["areaUsage"]["usedArea"]["count"] < final_count["printUsage"]["areaUsage"]["usedArea"]["count"]
    assert init_count["printUsage"]["areaUsage"]["imagedArea"]["count"] < final_count["printUsage"]["areaUsage"]["imagedArea"]["count"]
    if printer_type == "emulator":
        assert init_count["printUsage"]["areaUsage"]["printedArea"]["count"] < final_count["printUsage"]["areaUsage"]["printedArea"]["count"]
    assert init_count["printUsage"]["areaUsage"]["usedLength"]["count"] < final_count["printUsage"]["areaUsage"]["usedLength"]["count"]

    # Scan Usage checks
    assert init_count["scanUsage"]["totalImages"] < final_count["scanUsage"]["totalImages"]
    assert init_count["scanUsage"]["copyImages"] < final_count["scanUsage"]["copyImages"]
    assert init_count["scanUsage"]["scanAreaUsage"]["scanArea"]["count"] < final_count["scanUsage"]["scanAreaUsage"]["scanArea"]["count"]
    assert init_count["scanUsage"]["scanAreaUsage"]["scanLength"]["count"] < final_count["scanUsage"]["scanAreaUsage"]["scanLength"]["count"]

    # Check for scan area
    area_diff = final_count["scanUsage"]["scanAreaUsage"]["scanArea"]["count"] - init_count["scanUsage"]["scanAreaUsage"]["scanArea"]["count"]
    assert abs(area_diff - area_diff_in_cm2) < area_threshold, "Scan area is not correct. Expected: {0} Actual: {1}".format(area_diff_in_cm2, area_diff)

    # Check for scan length
    length_diff = final_count["scanUsage"]["scanAreaUsage"]["scanLength"]["count"] - init_count["scanUsage"]["scanAreaUsage"]["scanLength"]["count"]
    assert abs(length_diff - height_in_mm) < height_threshold, "Scan length is not correct. Expected: {0} Actual: {1}".format(height_in_mm , length_diff)

    response = json.loads(cdm.get_raw(cdm.DEVICE_USAGE_LIFETIME_COUNTERS).content)
    usedArea = 0
    imagedArea = 0
    printedArea = 0
    for category in response["printUsage"]["usageByPrintCategory"]:
        usedArea = usedArea + category["usedArea"]["count"]
        imagedArea = imagedArea + category["imagedArea"]["count"]
        printedArea = printedArea + category["printedArea"]["count"]

    assert usedArea == response["printUsage"]["areaUsage"]["usedArea"]["count"]
    assert imagedArea == response["printUsage"]["areaUsage"]["imagedArea"]["count"]
    if printer_type == "emulator":
        assert printedArea == response["printUsage"]["areaUsage"]["printedArea"]["count"]
    