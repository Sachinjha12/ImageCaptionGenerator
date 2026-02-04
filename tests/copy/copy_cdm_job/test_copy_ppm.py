import os

from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction

TESTRESOURCEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A0 and check memory pools and copy pipelines works for a big and typical size plot of Large Format printers
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-29874
    +timeout:120
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +external_files: A4_Color_200.ppm=d4f3409e817cc3f8e0bbcfac143c7b4152e6dc0262f883df5f0a176d8babd251
    +name: test_copy_ppm
    +test:
        +title: test_copy_ppm
        +guid: 0b36984e-e32a-4392-ba8a-1f6861608868
        +dut:
            +type:Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceFunction=Copy & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ppm(setup_teardown_with_copy_job, cdm, udw, tcl, usb, job, copy, ssh, scp):

    scan_action = ScanAction()
    scan_action.set_ssh(ssh)
    scan_action.set_scp(scp)
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    file_hash = "d4f3409e817cc3f8e0bbcfac143c7b4152e6dc0262f883df5f0a176d8babd251"
    scan_action.set_scan_pnm_acquisition_mode_hash_file(file_hash)

    # Get Job ID
    last_job_id = job.get_last_job_id()

    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
    }

    # Create payload
    payload = copy.build_payload(settings)

    copy.do_copy_job(**payload)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    scan_action.reset_simulation_mode()