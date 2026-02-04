import logging
from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction, ScanSimMode
import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test with a simulated 100x100mm that copy accounting data is correct
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-21713
    +timeout: 200
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_accounting
    +test:
        +title: test_copy_accounting
        +guid:a4416105-47c1-4a26-9122-7ed030a1aa19
        +dut:
            +type: Simulator
            +configuration:PrintEngineFormat=A4 & DeviceClass=MFP & DeviceFunction=Copy & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_accounting(tcl, cdm, job, udw, copy, configuration):
    # Create configuration Scan
    height = 100 # mm
    width = 100 # mm
    
    # Get default resolution and color mode from default ticket 
    response = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert response.status_code == 200
    default_colormode = response.json()["src"]["scan"]["colorMode"]
    default_resolution = response.json()["src"]["scan"]["resolution"]

    settings =	{
        "src": "scan",
        "color_mode": default_colormode,
        "resolution": default_resolution,
        "dest": "print",
        "copies": 1,
    }
    # Init simulation
    scan_action = ScanAction()
    scan_action.set_tcl(tcl).set_udw(udw).set_configuration(configuration)
    simulation = scan_action.set_scan_random_acquisition_mode(height, width)
    Control.validate_simulation(simulation) 
    copy.do_copy_job()

    # Restore default scan simulation mode
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)
    
    # Read Data and filter Job Telemetry
    response = cdm.get_raw(cdm.JOB_HISTORY_STATS_ENDPOINT)
    assert response.status_code == 200
    # get last job's historyStats
    job_scan_info_stats = response.json()["historyStats"][-1]["scanInfo"]

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
    +purpose: Verify number of counters copies 1 and pages 10 while perforiming copy job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_verify_copy_counter_number_of_copies_1_and_10_pages_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_cdm_verify_copy_counter_number_of_copies_1_and_10_pages_copy_job
        +guid:5c52fd7c-20d5-41c9-8939-79edc7d264a6
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_verify_copy_counter_number_of_copies_1_and_10_pages_copy_job(cdm, udw, ews, spice, job, net, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('ADF',10)
    # udw.mainApp.ScanDeviceService.setNumScanPages(10)
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'copies':'1'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        # already loaded media so no need to pass load media again
        copy_job_app.copy_job_ticket_general_method(loadmedia=None, copy_path=copy_path, copy_settings=options, udw=udw, net=net)
        time.sleep(10)
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 

        logging.info(job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + job_id)
        assert response.status_code==200, 'Unexpected response'
    
        cdm_response = response.json()
        logging.info(cdm_response)
        assert cdm_response['printInfo']['impressionCount'] == 10 , "Number of scan pages mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedImpressionCount'] == 10 , "Incorrect requestedImpressionCount"
        assert cdm_response['printInfo']['copiesCount'] == 1 , "Number of copies count mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedCopiesCount'] == 1 , "Incorrect requestedCopiesCount"
        assert cdm_response['scanInfo']['scannedPageCount'] == 10 , "Incorrect scanned page count"
    finally:
        scan_emulation.media.load_media('ADF',1)
        udw.mainApp.ScanDeviceService.setNumScanPages(1)
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify number of counters copies 3 and pages 1 while perforiming copy job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_verify_copy_counter_number_of_copies_3_and_1_pages_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_cdm_verify_copy_counter_number_of_copies_3_and_1_pages_copy_job
        +guid:d47a9958-b10e-4760-b888-e9b3e2da9a56
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_verify_copy_counter_number_of_copies_3_and_1_pages_copy_job(cdm, udw, ews, spice, job, net):
    job.bookmark_jobs()
    job.clear_joblog()
    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'copies':'3'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        time.sleep(10)
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 

        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + job_id)
        assert response.status_code==200, 'Unexpected response'
    
        cdm_response = response.json()
        logging.info(cdm_response)
        assert cdm_response['printInfo']['impressionCount'] == 3 , "Number of scan pages mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedImpressionCount'] == 3 , "Incorrect requestedImpressionCount"
        assert cdm_response['printInfo']['copiesCount'] == 3 , "Number of copies count mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedCopiesCount'] == 3 , "Incorrect requestedCopiesCount"
        assert cdm_response['scanInfo']['scannedPageCount'] == 1 , "Incorrect scanned page count"
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify number of counters copies 2 and pages 5 while perforiming copy job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_verify_copy_counter_number_of_copies_2_and_5_pages_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_cdm_verify_copy_counter_number_of_copies_2_and_5_pages_copy_job
        +guid:dc015bad-c3e2-4513-81f9-96538385c2ae
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_verify_copy_counter_number_of_copies_2_and_5_pages_copy_job(cdm, udw, ews, spice, job, net, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('ADF',5)
    # udw.mainApp.ScanDeviceService.setNumScanPages(5)
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'copies':'2'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        # already loaded media so no need to pass load media again
        copy_job_app.copy_job_ticket_general_method(loadmedia=None, copy_path=copy_path, copy_settings=options, udw=udw, net=net)
        time.sleep(10)
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 

        logging.info(job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + job_id)
        assert response.status_code==200, 'Unexpected response'
    
        cdm_response = response.json()
        logging.info(cdm_response)
        assert cdm_response['printInfo']['impressionCount'] == 10 , "Number of scan pages mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedImpressionCount'] == 10 , "Incorrect requestedImpressionCount"
        assert cdm_response['printInfo']['copiesCount'] == 2 , "Number of copies count mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedCopiesCount'] == 2 , "Incorrect requestedCopiesCount"
        assert cdm_response['scanInfo']['scannedPageCount'] == 5 , "Incorrect scanned page count"
    finally:
        udw.mainApp.ScanDeviceService.setNumScanPages(1)
        spice.goto_homescreen()
        spice.wait_ready()
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify job completion state, number of counters copies and requested Copies Count while perforiming copy job cancel
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_verify_copy_counter_number_of_copies_1_and_10_pages_cancel_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_cdm_verify_copy_counter_number_of_copies_1_and_10_pages_cancel_copy_job
        +guid:b8d0c1c8-c6de-41f9-b110-0ad12447aef0
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_verify_copy_counter_number_of_copies_1_and_10_pages_cancel_copy_job(cdm, udw, ews, spice, job, net, configuration, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    scan_emulation.media.load_media('ADF',10)
    # udw.mainApp.ScanMedia.loadMedia("ADF")
    # udw.mainApp.ScanDeviceService.setNumScanPages(10)
    
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.start_copy()
        # Cancel Copy
        current_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_button)
        current_button.mouse_click()
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')
        time.sleep(5)
        #job_id = job.get_last_job_id_cdm() 
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 
        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + job_id)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        assert cdm_response['jobInfo']['jobCompletionState'] == 'cancelled' , 'Job was not cancelled'
        assert cdm_response['printInfo']['impressionCount'] == 0 , "Number of scan pages mismatch"
        assert cdm_response['printInfo']['copiesCount'] == 0 , "Number of copies count mismatch"
        assert cdm_response['printInfo']['printSettings']['requestedCopiesCount'] == 1 , "Incorrect requestedCopiesCount"
        
    finally:
        scan_emulation.media.load_media('ADF',1)
        # udw.mainApp.ScanDeviceService.setNumScanPages(1)
        spice.goto_homescreen()
        spice.wait_ready()
    
