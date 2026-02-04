from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction

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
    +name: test_copy_A0_using_cdm
    +test:
        +title: test_copy_A0_using_cdm
        +guid: 86eec6ac-656f-11eb-9277-fba46d01282a
        +dut:
            +type:Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_A0_using_cdm(udw, tcl, job, copy):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan
    height = 1189 # mm
    width = 841 # mm

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
    copy.copy_simulation(height, width, settings, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"