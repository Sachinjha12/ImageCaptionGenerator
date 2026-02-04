import time


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple Copy Job, single page
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-4000
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_simple_copy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_simple_copy_job
        +guid:7c0bdc3c-1259-4284-98dc-1e78b569ae97
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_simple_copy_job(scan_emulation, udw):
    """Simple copy job.

    FIXME:
        This test has multiple disabled actions, needs to be checked if it is
        actually testing what it is meant to test...
    """

    # set number of pages in the scanner
    scan_emulation.media.load_media(media_id='ADF',media_numsheet=1)

    # Get the "last" job ID.  Even if no job existed since boot, this
    # will still return a valid integer.
    jmUwPreviousJobId = udw.mainApp.JobManager.getRecentJobs().split('\n')[-1]
    print("jmUwPrevious JobId: " + jmUwPreviousJobId)

    # This method create, initialize, and start a CopyJob. It will wait for
    # JobComplete and return the full job guid. Execute job will return the
    # full job Guid.
    fullJobId = udw.mainApp.CopyJobService.executeJob()
    print("Guid".ljust(12) + " JobId: " + fullJobId)

    # Get the current jobId as defined by the jobManager
    # underware commands.  Loop through until we find it.
    # print("Finding jobId")
    # jobId = Job.find_job_manager_job_id(udw, jmUwPreviousJobId, 15)
    # if( jobId != 0 ):
    #     print("JobManager".ljust(12) + " JobId: " + jobId)
    # else:
    #     print("JobManager".ljust(12) + " Failed to discover jobManager jobID, Failed test!")
    #     return

    # Now, wait for the Job to complete
    #jobstate = Job.wait_for_job_complete(udw, jobId, 50)
    #wait_for_job_complete is obsolete, use Job.wait_for_job_completion

    # Report test results
    # Job.report_test_results(jobstate)
