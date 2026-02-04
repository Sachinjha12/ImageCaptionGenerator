import dunetuf.common.commonActions as CommonActions

from dunetuf.control.control import Control
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction, ScanSimMode
from dunetuf.engine.maia.Power import Power

import time

"""
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: We need test to check our data is persisted after reboot and prevent unwanted changes
        +test_tier: 1
        +is_manual: False
        +test_classification:System
        +reqid: DUNE-53117
        +timeout:360
        +asset: Scan
        +test_framework: TUF
        +name: test_scan_by_cdm_check_persistance_after_reboot
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test:
            +title: test_scan_by_cdm_check_persistance_after_reboot
            +guid:d091133d-b0dc-4c97-a40f-75582a653b5a
            +dut:
                +type:Engine
                +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=DigitalSend & DigitalStorageType=HardDisk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_scan_by_cdm_check_persistance_after_reboot(tcl, scp, ssh, job, copy):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_tcl(tcl)

    # Simulation DIN A0
    simulation = scan_action.set_scan_random_acquisition_mode(841, 1189)
    Control.validate_simulation(simulation)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "file_name": "persistRaster001",
        "file_type": "ISF"
    }

    copy.create_run_configuration_copy(settings)

    # Get Job ID    
    job_id = job.get_last_job_id()
    job_id_cdm = job.get_last_job_id_cdm()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Download the file into tmp
    isf_file_name = settings["file_name"] + "." + settings["file_type"]
    isf_file_name_remote_path = "/mnt/customer/jobs/" + str(job_id_cdm) + "/" + isf_file_name

    isf_file_name_local_path = "/tmp/" + isf_file_name
    isf_file_name_local_path_aux = "/tmp/" + isf_file_name + ".AUX"
    file_downloaded = CommonActions.download_file_by_scp(scp, isf_file_name_remote_path, isf_file_name_local_path)

    # Check if file is downloaded
    Control.validate_file_downloaded(isf_file_name_local_path, file_downloaded)

    # Reboot the printer
    ssh.run("reboot")
    time.sleep(120)

    # Check if file can be downloaded after reboot
    file_downloaded = CommonActions.download_file_by_scp(scp, isf_file_name_remote_path, isf_file_name_local_path_aux)
    Control.validate_file_downloaded(isf_file_name_local_path_aux, file_downloaded)

    # Restore default simulation
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)

"""
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: We need test to check our data is persisted and prevent unwanted changes
        +test_tier: 1
        +is_manual: False
        +test_classification:System
        +reqid: DUNE-53117
        +timeout:120
        +asset: Scan
        +test_framework: TUF
        +name: test_scan_by_cdm_check_persistance
        +delivery_team:WalkupApps
        +feature_team:CopySolns
        +test:
            +title: test_scan_by_cdm_check_persistance
            +guid:bcf79e13-2361-431a-a0e5-76f9eed7ec14
            +dut:
                +type:Simulator
                +configuration:ScanFileFormat=PDF &DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=DigitalSend & DigitalStorageType=HardDisk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_scan_by_cdm_check_persistance(tcl, scp, job, copy):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_tcl(tcl)

    # Simulation DIN A0
    simulation = scan_action.set_scan_random_acquisition_mode(841, 1189)
    Control.validate_simulation(simulation)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "file_name": "persistRaster001",
        "file_type": "PDF"
    }

    copy.create_run_configuration_copy(settings)

    # Get Job ID
    job_id_cdm = job.get_last_job_id_cdm()
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Download the file into tmp
    isf_file_name = settings["file_name"] + "." + settings["file_type"]
    isf_file_name_remote_path = "/mnt/customer/jobs/" + str(job_id_cdm) + "/" + isf_file_name

    isf_file_name_local_path = "/tmp/" + isf_file_name
    file_downloaded = CommonActions.download_file_by_scp(scp, isf_file_name_remote_path, isf_file_name_local_path)

    # Check if file is downloaded
    Control.validate_file_downloaded(isf_file_name_local_path, file_downloaded)

    # Restore default simulation
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)

