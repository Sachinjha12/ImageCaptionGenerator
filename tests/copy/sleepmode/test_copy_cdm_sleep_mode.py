from dunetuf.copy.copy import *
import time
import logging
import sys
from dunetuf.power.power import Power, ActivityMode
from dunetuf.job.job import Job
from dunetuf.cdm.CdmEndpoints import CdmEndpoints
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

CDM_SLEEPNOW_ENDPOINT = CdmEndpoints.POWER_SLEEP_NOW

payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                },
            },
            'dest': {
                'print': {
                    "copies": 5,
                    'mediaSize':'na_letter_8.5x11in'
                }
            }
}

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: perform copy job while device in sleep
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-177486
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_sleep_mode_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_sleep_mode_copy_job
        +guid:013dc9b4-7516-40be-baf2-1437313b7b11
        +dut:
            +type:Simulator
            +configuration: ScannerInput=Flatbed & DeviceClass=MFP & GeneralSettings=InactivityTimeout
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cdm_sleep_mode_copy_job(cdm, udw, scan_emulation, net,job,configuration):

    job.bookmark_jobs()
    #scan_action.set_number_scan_pages(10)
    udw.mainApp.ScanDeviceService.setNumScanPages(10)

    logging.info("Get default timeout for sleep")
    power = Power(udw, target_ip=net.ip_address, cdm=cdm)
    default_timeout_value = power.get_current_each_activity_timeout_CDM(check_inactivity_supported=False)

    logging.info("Put device to deep sleep mode")
    power.put_device_to_sleep_mode_CDM(ActivityMode.deep_sleep, inactivity_timeout=30, check_inactivity_supported=False)

    scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_job( familyname = configuration.familyname, **payload)
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
    scan_emulation.media.load_media('ADF',1)
    activity_state = power.get_current_activity_state()
    logging.info("Validate Current Activity State:" + str(activity_state))
    assert activity_state < ActivityMode.sleep.value, "Check device wakes from sleep"
    logging.info("check the job state from cdm")
    job.wait_for_no_active_jobs()
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Make sure the CP wakes up when the ADF is loaded with paper while the device is in sleep mode.
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-221701
    +timeout:900
    +asset: Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_cdm_cp_wakes_up_when_loaded_adf
    +test:
        +title:test_copy_cdm_cp_wakes_up_when_loaded_adf
        +guid:134ed0ab-6447-4a4a-a2c1-93f7ae798904
        +dut:
            +type: Simulator
            +configuration:DeviceFunction=UI & DeviceClass=MFP & PowerSettings=SleepNow & UIExperience=Workflow2
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:900
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_cp_wakes_up_when_loaded_adf(spice, cdm, udw, job, scan_emulation, configuration):    
    try:
        job.bookmark_jobs()
        spice.goto_homescreen()
        
        beforeSleep_CDM = cdm.get(CDM_SLEEPNOW_ENDPOINT)
        logging.info(" cdmValue Before sleep  = ", beforeSleep_CDM)
        assert beforeSleep_CDM["state"] == "idle"

        #UDW for sleepNow
        logging.info("Executing SleepNOw udw command to make the device enter into sleep mode")
        udw.mainUiApp.execute("SleepNowApp PUB_sleepNow")
        time.sleep(30)
        
        logging.info("Checking the power level of the device after sleepNow command")
        power_level = int(udw.mainApp.execute("SystemScheduler PUB_getSystemPowerLevel"))
        logging.info(f"Power Level: is {power_level}, checking for device is sleep or not ")
        
        if (power_level == 2):
            logging.info("Sleep Now successful")
            assert power_level == 2
        else:
            assert power_level != 2
            logging.info("Unable to sleep as the device is already busy with some systemActivity")
        
        time.sleep(5) # Allowing  device to sleep for additional time before waking it up with spice CP

        # Trigger wake from spice CP with press and release activity
        logging.info("Trigger wake from spice CP with press and release activity")
        spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)
        scan_emulation.media.load_media('ADF',1)

        # To check the activity state
        activityState = int(udw.mainApp.ActivityMonitor.getCurrentState().split(" ")[1])
        logging.info("Validate Wake Activity State:" + str(activityState))
        assert activityState == 0

        afterSleep_CDM = cdm.get(CDM_SLEEPNOW_ENDPOINT)
        logging.info(" cdmValue after sleep  = ", afterSleep_CDM)
        assert afterSleep_CDM["lastResult"] == "success"

        #Verify that the copy job is performed properly.
        Copy(cdm, udw).do_copy_job( familyname = configuration.familyname, **payload)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    
    finally:
        spice.wait_ready()