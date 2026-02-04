import os
import sys
import logging
from dunetuf.copy.copy import Copy
from dunetuf.send.email.email import Email
from dunetuf.send.folder.folder import Folder
from dunetuf.fax.fax import Fax, set_pagestosend, Cancel as FaxCancel
from dunetuf.copy.copy import Cancel as CopyCancel
from dunetuf.send.common.common import Common, Cancel as SendCancel
from tests.copy.Contention.contention_common import send_print_job_from_usb, execute_print_storejob, execute_ipp_print_job, dismiss_load_paper_alert, execute_ipp_print_job_with_timeout
from copy import deepcopy
from tests.fax.Contention.contention_common import wait_for_print_report_in_job_state, send_scan_to_sharepoint_job, send_scan_to_usb_job
import time
from tests.fax.conftest import setup_fax_using_cdm
from dunetuf.utility.systemtestpath import get_system_test_binaries_path
from dunetuf.send.usb import usb
from tests.send.SendToUSB.conftest import usb_removed_alert_cancel

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start copy job as soon the scan completes start email and print job in contention
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:onepage-letter-srgb-8-300dpi.pwg=f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e
    +test_classification:System
    +name:test_copy_contention_followed_send_email_print_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_send_email_print_job
        +guid:381ca606-320a-4c62-89be-dcb8543cf454
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy&ScannerInput=AutomaticDocumentFeeder&ScannerInput=Flatbed&ScanDestination=Email & DocumentFormat=PWGRaster & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_send_email_print_job(setup_teardown_print_idle_status, setup_teardown_email_server, cdm, udw, counters, job, printjob):
    """
    1. Settings/config details
    Copy( 5 page duplex) : ADF, Letter media
    Scan to email(1 page duplex): FB
    Print ( 1 page, raster file)
    Print report - Usage report page
    2. Validations/Expected Behavior
    Validate the complete job status - 
        1. Copy job : Success
        2. Scan to email job: Success
        3. Print job: Success
        4. Validate the print usage counter.
    3. Description
    Start copy job as soon the scan completes start email and print job in contention
    """
    email_instance, serverDetails = setup_teardown_email_server
    copy_instence = Copy(cdm, udw) 

    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'adf',
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'duplex'
            },
        },
        'dest': {
            'print': {
                'copies': 5,
                'mediaSize': 'na_letter_8.5x11in'
            }
        }
    }

    email_payload = {
        'src': {
            'scan': {
                'mediaSource': 'flatbed'
            },
        },
        'dest': {
                'email': {
                    'subject':'Test Email',
                    'body':'Test email body',
                    'from':{'emailAddress' :  serverDetails['userDetails']['user']},
                    'senderProfileName': 'Profile1'
                    }
                }
    }

    logging.info("Start 1st copy job-> Copy( 5 page duplex) : ADF, Letter media")
    logging.info("To load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)
    copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30)
    
    logging.info("Start 2nd Send to email job while copy job is in progress-> Scan to email(1 page duplex): FB")
    email_instance.perform_scan_to_email_job_cdm(job_ticket_payload=email_payload, cancel=SendCancel.submit_and_exit)
    
    logging.info("Start 3rd Print job PWGRASTER file.-> Print ( 1 page, raster file)")
    printjob.start_print('f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e', assert_expected_jobs=False)

    logging.info("Start 4th Print Usage report page job while the print job is in progress->Print report - Usage report page")
    wait_for_print_report_in_job_state(job, cdm, udw, 'Usage Report')

    logging.info("Wait all jobs complete and check all jobs are successful using cdm")
    job.check_job_log_by_status_and_type_cdm(
        completion_state_list=[
            {"type": "copy", "status": "success"},
            {"type": "scanEmail", "status": "success"},
            {"type": "print", "status": "success"},
            {"type": "print", "status": "success"}
            ],
            time_out=300
    )

    logging.info("Verify the output printed page count.")
    deviceusage_info = counters.deviceusage.get_device_usage()
    assert deviceusage_info["printUsage"]["sheets"]["total"] == 12, "Failed to check printed sheets total counter"
    assert deviceusage_info["scanUsage"]["totalImages"] == 3, "Failed to check scanned totalImages counter"
    assert deviceusage_info["jobUsage"]["emailJobCount"] == 1,"Failed to check email job counter"
    assert deviceusage_info["jobUsage"]["copyJobCount"] == 1,"Failed to check copy job counter"
    assert deviceusage_info["jobUsage"]["printJobCount"] == 2,"Failed to check print job counter"

    udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start 10 page copy job and cancel during scanning.Print 10 page.Print a report page
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:900
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:letter_plain.jpg=15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9
    +test_classification:System
    +name:test_copy_contention_followed_multiple_print_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_multiple_print_job
        +guid:37659779-6b23-437a-b80b-85644294a9a2
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Report=ConfigurationReport & Report=HPCartridgesStatusReport & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_multiple_print_job(setup_teardown_print_idle_status, cdm, udw, job, counters, printjob):
    """
    1. Settings/config details
    Copy - 10 page(simplex): ADF, A4 media
    Print - 10 page(JPEG files)
    Report print: Printer Configuration page
    Supplies status page
    2. Validations/Expected Behavior
    Validate the complete job status - 
        1. Copy job : Cancelled
        2. Print job: Success
        3. Report jobs: Success
        4. Validate the print usage counter as long the cancel job don't cause intermittency.
    3. Description
    Start 10 page copy job and cancel during scanning.
    Print 10 page
    Print a report page
    """
    default_print_option = cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)
    copy_instence = Copy(cdm, udw) 
    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'adf',
                'mediaSize': 'iso_a4_210x297mm',
                'plexMode': 'simplex'

            },
        },
        'dest': {
            'print': {
                'copies': 10,
                'mediaSize': 'iso_a4_210x297mm'
            }
        }
    }
    logging.info("Set the print option copies as 10 via cdm")
    print_payload = deepcopy(default_print_option)
    print_payload['dest']['print']['copies'] = 10
    response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, print_payload)
    assert response.status_code == 200

    logging.info("Start 1st Copy - 10 page(simplex): ADF, A4 media job then cancel it while is scanning")
    logging.info("To load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copyjob_id = copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)
    job.cancel_job(copyjob_id)

    udw.mainApp.ScanMedia.loadMedia("ADF")
    logging.info("Start 2nd Print - 10 page(JPEG files) job")
    printjob.start_print('15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9', assert_expected_jobs=False)

    logging.info("Set the print option to default via cdm")
    response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, default_print_option)
    assert response.status_code == 200

    logging.info("Start 3rd Printer Configuration page job while the print job is in progress")
    wait_for_print_report_in_job_state(job, cdm, udw, 'Configuration Report')

    logging.info("Start 4th Supplies status page job while the print job is in progress")
    wait_for_print_report_in_job_state(job, cdm, udw, 'HP Supplies Status Report')

    logging.info("Wait all jobs complete and check all jobs are successful using cdm")
    copyjob_state = job.wait_for_job_completion_cdm(copyjob_id)
    job.check_job_log_by_status_and_type_cdm(
        completion_state_list=[
            {"type": "copy", "status": copyjob_state},
            {"type": "print", "status": "success"},
            {"type": "print", "status": "success"},
            {"type": "print", "status": "success"}],
            time_out=300
    )

    deviceusage_info = counters.deviceusage.get_device_usage()

    assert deviceusage_info["printUsage"]["sheets"]["total"] >= 12, "Failed to check printed sheets total counter"
    assert deviceusage_info["scanUsage"]["totalImages"] == 1 or deviceusage_info["scanUsage"]["totalImages"] == 0, "Failed to check scanned totalImages counter"
    assert deviceusage_info["jobUsage"]["copyJobCount"] == 1,"Failed to check cop job counter"
    assert deviceusage_info["jobUsage"]["printJobCount"] == 3,"Failed to check print job counter"



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start copy job, multiple reprint jobs in contention.
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_contention_followed_reprint_jobs_letter
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_reprint_jobs_letter
        +guid:7881308f-eb46-4893-9e2f-0d13c5fdec3f
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter & JobHistory=MultipleJobs & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_reprint_jobs_letter(setup_teardown_print_idle_status, cdm, udw, job, counters, printjob, tray):
    """
    1. Settings/config details
    Copy - 1 page(simplex): FB, Letter media
    Reprint- copy job(1 copies/default)
    Reprint - copy job(3 copies)
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate the complete job status - 
        1. Copy job : Success
        2. Reprint job: Success
        3. Reprint job: Success
        4. Validate the print usage counter.
    3. Description
    Start copy job.
    Reprint copy job with default copies.
    Reprint copy job with 3 copies.
    Repeat the above steps in loop of 2. 
    """
    copy_instence = Copy(cdm, udw)
    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'flatbed',
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'simplex'
            },
        },
        'dest':{
            'print':{
                    'plexMode': 'simplex'
            }
        }
    }
    
    print_payload = {
            'dest':{
                'print':{
                    'copies': 3,
                    'mediaSize': 'na_letter_8.5x11in'
                }
            }
    }
    default_tray = tray.get_default_source()
    if tray.is_size_supported('any', default_tray):
        tray.configure_tray(default_tray, 'any', 'stationery')
    if job.reprint_job_supported == 'true':
        logging.info("Perform a default copy job for reprint")
        copy_job_id = copy_instence.do_copy_job()
        job.wait_for_job_completion_cdm(copy_job_id)

    for i in range(2):
        logging.info(f"The <{i}> time to perform the test steps")

        logging.info("unload ADF")
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        logging.info("Start 1st Copy - 1 page(simplex): FB, Letter media job")
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30) 
        copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)

        logging.info("Start 2nd reprint copy job")
        if job.reprint_job_supported == 'true':
            jobinfo = job.get_job_info(copy_job_id)
            assert jobinfo.get('reprintJobAvailable') == job.reprint_job_supported, 'Unexpected reprintJobAvailable value!'
            printjob.start_reprint(jobinfo)
        else:
            logging.info('Reprint is not supported, not attempting to reprint!')

        logging.info("Start 3rd reprint copy job with 3 copies")
        if job.reprint_job_supported == 'true':
            printjob.start_reprint(jobinfo, print_payload)
        else:
            logging.info('Reprint is not supported, not attempting to reprint!')
        

    logging.info("Wait all jobs complete and check all jobs are successful using cdm")
    if job.reprint_job_supported == 'true':
        raise Exception("Need to add checkpoint if printer support reprint job for Copy")

    else:
        job.check_job_log_by_status_and_type_cdm(
            completion_state_list=[
                {"type": "copy", "status": "success"},
                {"type": "copy", "status": "success"}
            ],time_out=300
        )
        deviceusage_info = counters.deviceusage.get_device_usage()
        assert deviceusage_info["printUsage"]["sheets"]["total"] == 2, "Failed to check printed sheets total counter"
        assert deviceusage_info["scanUsage"]["totalImages"] == 2, "Failed to check scanned totalImages counter"
        assert deviceusage_info["jobUsage"]["copyJobCount"] == 2,"Failed to check cop job counter"

    udw.mainApp.ScanMedia.loadMedia("ADF")
    tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start the copy job 5 page, once scanning completes, start the sharepoint job.Print a file. Print report. Re-print. Repeat above step in loop of 2.
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:720
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:letter_plain.jpg=15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9
    +test_classification:System
    +name:test_copy_contention_followed_scan_to_sharepoint_multiple_prints_jobs
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_scan_to_sharepoint_multiple_prints_jobs
        +guid:5f3fd91b-bd6b-45d6-8c8f-e4eabc2b8588
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScanDestination=SharePoint & ScannerInput=AutomaticDocumentFeeder & DocumentFormat=JPEG & Report=DiagnosticsReport & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_scan_to_sharepoint_multiple_prints_jobs(setup_teardown_print_idle_status, cdm, udw, tray, job, printjob, counters):
    """
    1. Settings/config details
    Copy - 5 page(Duplex): ADF, Letter media
    Sharepoint - 1 Page - FB
    Print - 10 page
    Print report - Diagnostic page
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate all the job status
        Validate the print usage counter.
    3. Description
    Start the copy job 5 page, once scanning completes
    Start the sharepoint job.
    Print a file
    Print report
    Re-print
    Repeat above step in loop of 2.
    """
    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'adf',
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'duplex'

            },
        },
        'dest': {
            'print': {
                'copies': 5,
                'mediaSize': 'na_letter_8.5x11in'
            }
        }
    }
    default_tray = tray.get_default_source()
    copy_instence = Copy(cdm, udw)

    if job.reprint_job_supported == 'true':
        logging.info("Perform a default copy job for reprint")
        copy_job_id = copy_instence.do_copy_job()
        job.wait_for_job_completion_cdm(copy_job_id)

    if tray.is_size_supported('na_letter_8.5x11in'):
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'stationery')

    for i in range(2):
        logging.info(f"The <{i}> time to perform the test steps")

        logging.info("load ADF")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        logging.info("Start 1st Copy - 5 page(Duplex): ADF, Letter media job")
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30) 
        copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30)

        logging.info("Start 2nd Sharepoint - 1 Page - FB job")
        send_scan_to_sharepoint_job(cdm, udw, cancel=SendCancel.submit_and_exit)

        default_print_option = cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)
        logging.info("Set the print option copies as 10 via cdm")
        print_payload = deepcopy(default_print_option)
        print_payload['dest']['print']['copies'] = 10
        response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, print_payload)
        assert response.status_code == 200
        logging.info("Start 3rd Print - 10 page job")
        printjob.start_print('773148e5f01002bd9136559adcf80d1bfb9d326e5ff9fc3cd33e877bb412fa74', assert_expected_jobs=False)

        logging.info("Reset the print option")
        response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, default_print_option)
        assert response.status_code == 200

        logging.info("Start 4th Print report - Diagnostic page job")
        wait_for_print_report_in_job_state(job, cdm, udw, 'Diagnostics Test Page')

        logging.info("Start 5th Re-print last previous job")
        if job.reprint_job_supported == 'true':
            jobinfo = job.get_job_info(copy_job_id)
            assert jobinfo.get('reprintJobAvailable') == job.reprint_job_supported, 'Unexpected reprintJobAvailable value!'
            printjob.start_reprint(jobinfo)
        else:
            logging.info('Reprint is not supported, not attempting to reprint!')


    logging.info("Wait all jobs complete and check all jobs are successful using cdm")
    if job.reprint_job_supported == 'true':
        raise Exception("Need to add checkpoint if printer support reprint job for Copy")

    else:
        job.check_job_log_by_status_and_type_cdm(
            completion_state_list=[
                {"type": "copy", "status": "success"},
                {"type": "scanSharePoint", "status": "success"},
                {"type": "print", "status": "success"},
                {"type": "print", "status": "success"},
                {"type": "copy", "status": "success"},
                {"type": "scanSharePoint", "status": "success"},
                {"type": "print", "status": "success"},
                {"type": "print", "status": "success"}
            ],time_out=300
        )
        deviceusage_info = counters.deviceusage.get_device_usage()
        assert deviceusage_info["printUsage"]["sheets"]["total"] == 42, "Failed to check printed sheets total counter"
        assert deviceusage_info["scanUsage"]["totalImages"] == 6, "Failed to check scanned totalImages counter"
        assert deviceusage_info["jobUsage"]["copyJobCount"] == 2,"Failed to check copy job counter"
        assert deviceusage_info["jobUsage"]["printJobCount"] == 4,"Failed to check print job counter"


    logging.info("load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start the copy job 5 page, once scanning completes, start the sharepoint job.Print a file. Print report. Re-print. Repeat above step in loop of 2.
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:720
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:onepage-letter-srgb-8-300dpi.pwg=f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e&Pdf_1pgModified.prn=a80db6579ece6a9d7c53dc7d23e1d7b230f21d38fe53d668953e87fd48f49e86&PH0016_LETTER.ps=dbdbcdd5929fa6f323a0bc210b64ab2c6a78558d11951e0dc8799d5ae45d09a5
    +test_classification:System
    +name:test_copy_contention_followed_scan_to_usb_multiple_prints_jobs
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_scan_to_usb_multiple_prints_jobs
        +guid:21e59a51-9d3a-4b4d-9357-83cfe81d7753
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceFunction=Fax & DocumentFormat=PostScript & DocumentFormat=PWGRaster & ScanDestination=USB & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_scan_to_usb_multiple_prints_jobs(setup_teardown_with_empty_usb_drive,setup_fax_using_cdm, setup_teardown_print_idle_status, net, cdm, udw, tray, job, printjob, counters, usbdevice, configuration):
    """
    1. Settings/config details
    Copy - 5 page(Duplex): ADF, Letter media
    Send to usb - 5 Page - ADF
    print a different file from usb - 5 page
    Send PC fax - 1 page(simplex fb)
    Print job - 5 page(file type: PS)
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate all the job status
        Validate the print usage counter at end
    3. Description
    Start the copy job 5 page, once scanning completes
    Start the send to usb job.
    Print from USB
    PC Fax
    Re-print
    Repeat above step in loop of 2.
    """

    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'adf',
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'duplex'

            },
        },
        'dest': {
            'print': {
                'copies': 5,
                'mediaSize': 'na_letter_8.5x11in'
            }
        }
    }

    if job.reprint_job_supported == 'true':
        logging.info("Perform a default copy job for reprint")
        copy_job_id = copy_instence.do_copy_job()
        job.wait_for_job_completion_cdm(copy_job_id)

    default_tray = tray.get_default_source()
    copy_instence = Copy(cdm, udw)
    scan_instance = Common(cdm, udw)
    fax_instence = Fax(cdm, udw)
    

    if job.reprint_job_supported == 'true':
        logging.info("Perform a default copy job for reprint")
        copy_job_id = copy_instence.do_copy_job()
        job.wait_for_job_completion_cdm(copy_job_id)

    if tray.is_size_supported('na_letter_8.5x11in'):
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'stationery')
        tray.load_media(default_tray)

    for i in range(2):
        logging.info(f"The <{i}> time to perform the test steps")

        logging.info("load ADF")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        logging.info("Start 1st Copy - 5 page(Duplex): ADF, Letter media job")
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30) 
        copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit, familyname=configuration.familyname)
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30)

        logging.info("Start 2nd Send to usb - 5 Page - ADF job")
        logging.info("load ADF")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        send_scan_to_usb_job(cdm, udw, net, job, cancel=SendCancel.submit_and_exit) 
        scan_instance.wait_for_corresponding_scanner_status_with_cdm(timeout=30)
        #Dont patch copies for print Job as the copies is taken from the binary being passed which is 1
        logging.info("Start 3rd print a different file from usb - 1 page job")
        send_print_job_from_usb(usbdevice, job, 1) 
        scan_instance.wait_for_corresponding_scanner_status_with_cdm(timeout=30)
        logging.info("Start 4th Send PC fax - 1 page(simplex fb) job")
        logging.info("unload ADF")
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        dat_file = os.path.join('/code/tests/fax/data_files/',
                                'pcfax-create-job-and-send-document-single-destination-uri.test')
        fax_instence.wait_for_execute_ipp_pcfax_in_job_state(net.ip_address, dat_file, get_system_test_binaries_path(
            'a80db6579ece6a9d7c53dc7d23e1d7b230f21d38fe53d668953e87fd48f49e86'))

        default_print_option = cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)
        logging.info("Set the print option copies as 1 via cdm")
        print_payload = deepcopy(default_print_option)
        #Dont patch copies for print Job as the copies is taken from the binary being passed which is 1
        #print_payload['dest']['print']['copies'] = 5
        response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, print_payload)
        assert response.status_code == 200

        logging.info("Start 5th Print job - 5 page(file type: PS) job")
        printjob.start_print('f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e', assert_expected_jobs=False)
        response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, default_print_option)
        assert response.status_code == 200

    
        logging.info("Start 6th Re-print last previous job")
        if job.reprint_job_supported == 'true':
            jobinfo = job.get_job_info(copy_job_id)
            assert jobinfo.get('reprintJobAvailable') == job.reprint_job_supported, 'Unexpected reprintJobAvailable value!'
            printjob.start_reprint(jobinfo)
        else:
            logging.info('Reprint is not supported, not attempting to reprint!')


    logging.info("Wait all jobs complete and check all jobs are successful using cdm")
    if job.reprint_job_supported == 'true':
        raise Exception("Need to add checkpoint if printer support reprint job for Copy")

    else:
        job.check_job_log_by_status_and_type_cdm(
            completion_state_list=[
                {"type": "copy", "status": "success"},
                {"type": "scanUsb", "status": "success"},
                {"type": "usbPrint", "status": "success"},
                {"type": "scanFax", "status": "success"},
                {"type": "print", "status": "success"},
                {"type": "copy", "status": "success"},
                {"type": "scanUsb", "status": "success"},
                {"type": "usbPrint", "status": "success"},
                {"type": "scanFax", "status": "success"},
                {"type": "print", "status": "success"}
            ],time_out=720
        )
        deviceusage_info = counters.deviceusage.get_device_usage()
        assert deviceusage_info["printUsage"]["sheets"]["total"] == 24, "Failed to check printed sheets total counter"
        assert deviceusage_info["scanUsage"]["totalImages"] == 6, "Failed to check scanned totalImages counter"
        assert deviceusage_info["jobUsage"]["copyJobCount"] == 2,"Failed to check copy job counter"
        assert deviceusage_info["jobUsage"]["printJobCount"] == 2,"Failed to check print job counter"
        assert deviceusage_info["jobUsage"]["sendFaxJobCount"] == 2,"Failed to check send fax job counter"
        assert deviceusage_info["jobUsage"]["removalStorageJobCount"] == 4,"Failed to check send fax job counter"

    logging.info("load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start a copy job of 10 page then receive a stored fax immediately, send a print file, print the stored fax job, re-print last previous job. Pause the device and resume. Repeat above step in loop of 2.
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:900
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:1Page-lj9k_bw_rletter.pdf=3eeaf5b8c35551a80f50810d12f9ad758b3b0ab8cfc7f70c3c0aa17d38813934
    +test_classification:System
    +name:test_copy_contention_followed_receivefax_ipp_print_jobs
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_receivefax_ipp_print_jobs
        +guid:67c5f96e-ad75-4a0b-bcf0-562998cc378b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceFunction=Fax & JobSettings=JobStorage & ScannerInput=AutomaticDocumentFeeder & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_receivefax_ipp_print_jobs(setup_fax_using_cdm, fax_config_reset, setup_teardown_dunestore_job, setup_teardown_print_idle_status, cdm, udw, net, job, counters, printjob, tray, dunestorejob):
    """
    1. Settings/config details
    Copy - 10 page(simplex): ADF, A5 media
    Receive 10 page fax
    Print - IPP Print job, 10 page(PDF file)
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate all the job status
        Validate the device is paused/resumed
        Validate the print usage counter at end
    3. Description
    Start a copy job of 10 page
    Receive a fax immediately - stored
    Send a print file
    Print the stored fax job
    Re-print last previous job
    Pause the device and resume
    Repeat above step in loop of 2.
    """
    default_tray = tray.get_default_source()
    tray.reset_trays()
    copy_instence = Copy(cdm, udw)
    fax_instence = Fax(cdm, udw)
    udw.mainApp.ScanDeviceService.setNumScanPages(1)

    faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]
    #faxSimIp = "172.17.0.2"

    logging.info("Enable fit to page to make sure the receive-print counters correct")
    response = cdm.get(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT)
    logging.info(f"The default fax receive config is {response}")
    default_fit_to_page = response['fitToPageEnabled']
    if default_fit_to_page == "false":
        data = {"fitToPageEnabled": "true"}
        cdm.patch_raw(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT, data)

    logging.info("Enabling store job")
    fax_instence.set_stored_job_config(storeJobEnable='true')
    default_fax_receive = cdm.get(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT) 
    if default_fax_receive["faxPrintingSchedule"] != "alwaysStoreAndPrint":
        default_fax_receive["faxPrintingSchedule"] = "alwaysStoreAndPrint"
        cdm.put(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT, default_fax_receive)

    if job.reprint_job_supported == 'true':
        logging.info("Perform a default copy job for reprint")
        copy_job_id = copy_instence.do_copy_job()
        job.wait_for_job_completion_cdm(copy_job_id) 

    logging.info("Prepare the fax store job")
    fax_job_id = fax_instence.receive_fax(faxSimIp)
    job.wait_for_job_completion_cdm(fax_job_id)
    storejob = dunestorejob.get(fax_job_id)
    logging.info(f"The prepared store fax job id is <{fax_job_id}>")

    logging.info("Set receive fax page as 10")
    set_pagestosend(faxSimIp, pagestosend=10)

    for i in range(2):
        logging.info("Start 1st Copy - 10 page(simplex): ADF, A5 media")
        copy_payload = {
            'src': {
                'scan': {
                    'mediaSource':'adf',
                    'plexMode': 'simplex'

                },
            },
            'dest': {
                'print': {
                    'copies': 10
                }
            }
        }
        logging.info("load ADF")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30) 
        copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)
        logging.info("Start 2nd Receive 10 page fax")
        fax_instence.receive_fax(faxSimIp, cancel=FaxCancel.submit_and_exit)
        

        logging.info("Start 3rd Print - IPP Print job, 10 page(PDF file)")
        ipp_test_attribs = {'document-format': 'application/pdf', 'copies': 10}
        #Changing the timeout of IPP tool to 300
        execute_ipp_print_job_with_timeout(net, printjob, ipp_test_attribs, print_file = '3eeaf5b8c35551a80f50810d12f9ad758b3b0ab8cfc7f70c3c0aa17d38813934', timeout=300)
        logging.info("Start 4th Print the stored fax job")
        fax_instence.wait_for_fax_job_state_displayed(job_type="faxReceiveState", expected_state="printing")
        execute_print_storejob(job, dunestorejob, storejob)

        logging.info("Start 5th Re-print last previous job")
        if job.reprint_job_supported == 'true':
            jobinfo = job.get_job_info(copy_job_id)
            assert jobinfo.get('reprintJobAvailable') == job.reprint_job_supported, 'Unexpected reprintJobAvailable value!'
            printjob.start_reprint(jobinfo)
        else:
            logging.info('Reprint is not supported, not attempting to reprint!')

        #Will be re-enabled with DUNE-54426
        #if job.pause_queue_supported == 'true':
            #logging.info("Pause the job")
            #job.set_device_state("pauseProcessing")
            #assert job.check_device_status(paused=True), 'Failed to pause the job'

            #logging.info("Resume the job")
            #job.set_device_state("resumeProcessing")
            #assert job.check_device_status(paused=False), 'Failed to resume the job'
        #else:
            #logging.info("Pause and Resume is not supported, Pause and Resume")


    if job.reprint_job_supported == 'true':
        raise Exception("Need to add checkpoint if printer support reprint job for Copy")
    else:
        job.check_job_log_by_status_and_type_cdm(
            completion_state_list=[
                {"type": "receiveFax", "status": "success"},
                {"type": "copy", "status": "success"},
                {"type": "receiveFax", "status": "success"},
                {"type": "print", "status": "success"},
                {"type": "receiveFax", "status": "success"},
                {"type": "copy", "status": "success"},
                {"type": "receiveFax", "status": "success"},
                {"type": "print", "status": "success"},
                {"type": "receiveFax", "status": "success"}
            ],time_out=300
        )

        deviceusage_info = counters.deviceusage.get_device_usage()
        assert deviceusage_info["printUsage"]["sheets"]["total"] == 63, "Failed to check printed sheets total counter"
        assert deviceusage_info["scanUsage"]["totalImages"] == 2, "Failed to check scanned totalImages counter"
        assert deviceusage_info["jobUsage"]["printJobCount"] == 2,"Failed to check print job counter"
        assert deviceusage_info["jobUsage"]["copyJobCount"] == 2,"Failed to check copy job counter"
        assert deviceusage_info["jobUsage"]["receiveFaxJobCount"] == 5,"Failed to check receive fax job counter"


    set_pagestosend(faxSimIp, pagestosend=1)
    udw.mainApp.ScanMedia.loadMedia("ADF")
    tray.reset_trays()
    logging.info("Reset fit to page")
    data = {"fitToPageEnabled": default_fit_to_page}
    cdm.patch_raw(cdm.FAX_RECEIVE_CONFIGURATION_ENDPOINT, data)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Fax receive during copy scanning in progress
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-221746
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_contention_faxreceive_during_copy_duplex_scanning_inprogress
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_faxreceive_during_copy_duplex_scanning_inprogress
        +guid:4bb7621a-e592-4466-a482-d076122d516f
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Fax  & ScanOriginalSides=2-sided & ScannerInput=AutomaticDocumentFeeder


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_contention_faxreceive_during_copy_duplex_scanning_inprogress(setup_fax_using_cdm,configuration, cdm,spice,net, udw, job):
    try:
        payload = {
            'src': {
                'scan': {
                    'plexMode':'duplex',
                },
            },
            'dest': {
                'print': {
                    'plexMode':'duplex',
                }
            }
        }
        job.bookmark_jobs()
        logging.info("Load  pages in ADF for fax send")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainApp.ScanDeviceService.setNumScanPages(30)
        Copy(cdm, udw).do_copy_job(cancel=CopyCancel.submit_and_exit,**payload)
        #spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', wait_for_toast_dismiss=False)
        faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]
        fax_instance = Fax(cdm, udw)
        fax_instance._Fax__receive_fax(faxSimIp)
        spice.fax_ui().wait_for_fax_job_status_toast(net,"Incoming fax", 40)
        job.wait_for_no_active_jobs()
        logging.info("Wait all jobs complete and check all jobs are successful using cdm")
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"},{"type": "receiveFax", "status": "success"}])
        recent_jobs = job.get_newjobs()
        numofjobs = len(recent_jobs)
        assert numofjobs ==2
        logging.info("latest number of jobs is",numofjobs)

    finally:
      spice.goto_homescreen()
      udw.mainApp.ScanDeviceService.setNumScanPages(1)



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start the copy job 5 page, once scanning completes. Start the Scan to Network Folder job. Print a file. Print from USB. Print report. Repeat above step in loop of 2.
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:720
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_czlib_H64_PgCnt1_RGB__JPG_Source.pdf=773148e5f01002bd9136559adcf80d1bfb9d326e5ff9fc3cd33e877bb412fa74&onepage-letter-srgb-8-300dpi.pwg=f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e
    +test_classification:System
    +name:test_copy_contention_followed_scan_to_network_folder_print_print_report_jobs
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_scan_to_network_folder_print_print_report_jobs
        +guid:5fa24f89-3771-4768-94a0-105dd84266ae
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DocumentFormat=PCLm & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & NetworkReports=ConnectivityStatusReport & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_scan_to_network_folder_print_print_report_jobs(setup_teardown_print_idle_status, setup_teardown_with_empty_usb_drive, cdm, udw, usbdevice, job, counters, printjob, tray, configuration):
    """
    1. Settings/config details
    Copy - 1 page(simplex): FB, Letter media
    SNF - 10 Page ADF
    Print - 10 page(file type: PCLm)
    Print report - Connectivity status page
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate all the job status
        Validate the print usage counter at end
    3. Description
    Start the copy job 5 page, once scanning completes
    Start the Scan to Network Folder job.
    Print a file
    Print from USB
    Print report
    Repeat above step in loop of 2.
    """
    counters.clear_counters()
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'adf',
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'simplex'

            },
        },
        'dest': {
            'print': {
                'copies': 5,
                'mediaSize': 'na_letter_8.5x11in'
            }
        }
    }
    default_tray = tray.get_default_source()
    copy_instence = Copy(cdm, udw)
    
    folder_supported = cdm.device_feature_cdm.is_scan_to_network_folder_supported()
    if folder_supported == True:
        folder_instence = Folder(cdm, udw)
        folder_instence.set_up_folder_server()
    
    try:
        if tray.is_size_supported('na_letter_8.5x11in'):
            tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'stationery')

        expected_job_list = []

        for i in range(2):
            logging.info(f"The <{i}> time to perform the test steps")

            logging.info("unload ADF")
            udw.mainApp.ScanMedia.unloadMedia("ADF")
            logging.info("Start 1st Copy - 1 page(simplex) 5 copies: FB, Letter media job")
            copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30) 
            udw.mainApp.ScanDeviceService.setNumScanPages(1)
            copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)
            expected_job_list.append({"type": "copy", "status": "success"})
            job_info_url = job.get_current_job_url("copy")
            #Wait for copy job to completed else Scanned Pages from ADF will change
            job.wait_for_job_state_complete_successfully(job_info_url,time_out=30)

            logging.info("Start 2nd Scan to NetworkFolder - 10 Page ADF job")
            if folder_supported == True:
                logging.info("load ADF")
                udw.mainApp.ScanMedia.loadMedia("ADF")
                test_config ={
                    'mediaSource': 'adf'
                }
                udw.mainApp.ScanDeviceService.setNumScanPages(10)
                udw.mainApp.ScanMedia.loadMedia("ADF")
                folder_instence.do_folder_job(test_config, cancel=SendCancel.submit_and_exit)
                expected_job_list.append({"type": "scanNetworkFolder", "status": "success"})

            else:
                logging.info("Scan to NetworkFolder is not supported, not attempting to Scan to NetworkFolder!")
            default_print_option = cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)

            logging.info("Set the print option copies as 10 via cdm")
            print_payload = deepcopy(default_print_option)
            print_payload['dest']['print']['copies'] = 10
            response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, print_payload)
            assert response.status_code == 200

            logging.info("Start 3rd Print - 10 page(file type: PCLm) job")
            printjob.start_print('773148e5f01002bd9136559adcf80d1bfb9d326e5ff9fc3cd33e877bb412fa74', assert_expected_jobs=False)
            expected_job_list.append({"type": "print", "status": "success"})
            logging.info("Reset the print option")
            response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, default_print_option)
            assert response.status_code == 200

            logging.info("Start 4th print from usb job")
            send_print_job_from_usb(usbdevice, job) 
            expected_job_list.append({"type": "usbPrint", "status": "success"})

            logging.info("Start 5th Print report - Connectivity status page job")
            wait_for_print_report_in_job_state(job, cdm, udw, 'Connectivity Status Report', state="SUCCESS")
            expected_job_list.append({"type": "print", "status": "success"})

        job.check_job_log_by_status_and_type_cdm(completion_state_list=expected_job_list,time_out=300)  
        deviceusage_info = counters.deviceusage.get_device_usage()
        #Copy - 5Page, Print (PCLM Job) - 10 Page, Print (USB) - 1 Page, Connectivity Report - 2Page = 18, looping twice = 36
        if configuration.familyname == "homepro":
            #configuration report is 1 page for homepro products
            assert deviceusage_info["printUsage"]["sheets"]["total"] == 34, "Failed to check printed sheets total counter"
        else:
            assert deviceusage_info["printUsage"]["sheets"]["total"] == 36, "Failed to check printed sheets total counter"
        if folder_supported == True:
            assert deviceusage_info["scanUsage"]["totalImages"] == 22, "Failed to check scanned totalImages counter"
            assert deviceusage_info["jobUsage"]["networkFolderJobCount"] == 2,"Failed to check scan to network folder job counter"
        else:
            assert deviceusage_info["scanUsage"]["totalImages"] == 2, "Failed to check scanned totalImages counter"
        assert deviceusage_info["jobUsage"]["copyJobCount"] == 2,"Failed to check copy job counter"
        assert deviceusage_info["jobUsage"]["printJobCount"] == 4,"Failed to check print job counter"

    finally:
        if folder_supported == True:
            folder_instence.tear_down_folder_server()
        
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainApp.ScanDeviceService.setNumScanPages(1)
        counters.clear_counters()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Start the copy job 5 page, once scanning completes. Print from job storage. Receive a fax. Re-print. Repeat above step in loop of 2.
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:720
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:StoredJob_1Page.prn=7e774102c161af5bf3d04da84a56884ab010d16a4ac8ae7c61006f39042f83bf
    +test_classification:System
    +name:test_copy_contention_followed_print_from_job_storage_receive_fax
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_contention_followed_print_from_job_storage_receive_fax
        +guid:cc088d40-e4b6-4e5c-8e84-5192bb80412c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceFunction=Fax & JobSettings=JobStorage & ScannerInput=AutomaticDocumentFeeder & FaxPrinting=StoreAndPrint & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_followed_print_from_job_storage_receive_fax(setup_teardown_print_idle_status,setup_fax_using_cdm, setup_teardown_dunestore_job, counters, cdm, udw, tray, job, printjob, dunestorejob):
    """
    1. Settings/config details
    Copy - 5 page(Duplex): ADF, Letter media
    Print from job storage - 10 Page
    Fax receive - 2 page
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate all the job status
        Validate the print usage counter at end
    3. Description
    Start the copy job 5 page, once scanning completes
    Print from job storage
    Receive a fax
    Re-print
    Repeat above step in loop of 2.
    """

    if job.reprint_job_supported == 'true':
        logging.info("Perform a default copy job for reprint")
        copy_job_id = copy_instence.do_copy_job()
        job.wait_for_job_completion_cdm(copy_job_id)

    copy_payload = {
        'src': {
            'scan': {
                'mediaSource':'adf',
                'mediaSize': 'na_letter_8.5x11in',
                'plexMode': 'duplex'

            },
        },
        'dest': {
            'print': {
                'mediaSize': 'na_letter_8.5x11in'
            }
        }
    }
    default_tray = tray.get_default_source()
    copy_instence = Copy(cdm, udw)
    fax_instence = Fax(cdm, udw)

    faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]

    if tray.is_size_supported('na_letter_8.5x11in', default_tray):
        tray.configure_tray(default_tray, 'na_letter_8.5x11in', 'stationery')

    default_print_option = cdm.get(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT)
    logging.info("Set the print option copies as 10 via cdm")
    print_payload = deepcopy(default_print_option)
    print_payload['dest']['print']['copies'] = 10
    response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, print_payload)
    assert response.status_code == 200

    expected_job_list = []

    storejob_capabilities = dunestorejob.get_capabilities()
    storejob_print_supported = storejob_capabilities['printSupported']

    if storejob_print_supported == 'true':
        logging.info("Sending a print job and storing it on device")
        printjob.print_verify("7e774102c161af5bf3d04da84a56884ab010d16a4ac8ae7c61006f39042f83bf")
        logging.info('Listing the stored job')
        storejob = dunestorejob.get_all()
        assert len(storejob) == 1, 'Unexpected number of stored jobs were found!'
        logging.info(storejob)
        expected_job_list.append({"type": "print", "status": "success"})
    else:
        logging.info("Current device doesn't support print to job storage")



    for i in range(2):
        logging.info(f"The <{i}> time to perform the test steps")

        logging.info("Start 1st Copy - 5 page(Duplex): ADF, Letter media job")
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainApp.ScanDeviceService.setNumScanPages(5)
        copy_instence.wait_for_corresponding_scanner_status_with_cdm(timeout=30) 
        copy_instence.do_copy_job(**copy_payload, cancel=CopyCancel.submit_and_exit)
        expected_job_list.append({"type": "copy", "status": "success"})

        if storejob_print_supported == 'true':
            logging.info("Start 2nd Print from job storage - 10 Page job")
            execute_print_storejob(job, dunestorejob, storejob[0])
            expected_job_list.append({"type": "print", "status": "success"})
        else:
            logging.info("Current device doesn't support print to job storage, not attempting to print from job storage!")
        

        logging.info("Start 3rd Fax receive - 2 page job")
        logging.info("Set receive fax page as 2")
        set_pagestosend(faxSimIp, pagestosend=2)
        fax_instence.receive_fax(faxSimIp, cancel=FaxCancel.submit_and_exit)
        fax_instence.wait_for_fax_job_state_displayed(job_type="faxReceiveState", expected_state="printing")
        expected_job_list.append({"type": "receiveFax", "status": "success"})

        logging.info("Start 4th Re-print last previous job")
        if job.reprint_job_supported == 'true':
            jobinfo = job.get_job_info(copy_job_id)
            assert jobinfo.get('reprintJobAvailable') == job.reprint_job_supported, 'Unexpected reprintJobAvailable value!'
            printjob.start_reprint(jobinfo)
            expected_job_list.append({"type": "print", "status": "success"})
        else:
            logging.info('Reprint is not supported, not attempting to reprint!')
        

    
    if job.reprint_job_supported == 'true':
        raise Exception("Need to add checkpoint if printer support reprint job for Copy")
    else:
        job.check_job_log_by_status_and_type_cdm(completion_state_list=expected_job_list,time_out=300)

        deviceusage_info = counters.deviceusage.get_device_usage()
        if storejob_print_supported == 'true':
            assert deviceusage_info["printUsage"]["sheets"]["total"] == 26, "Failed to check printed sheets total counter" #print sheet counter is only for print jobs
        else:
            assert deviceusage_info["printUsage"]["sheets"]["total"] == 0, "Failed to check printed sheets total counter"
        assert deviceusage_info["printUsage"]["copyImpressions"]["total"] == 20, "Failed to check printed copyImpressions total counter"
        assert deviceusage_info["printUsage"]["faxInImpressions"]["total"] == 4, "Failed to check printed faxInImpressions total counter"
        assert deviceusage_info["scanUsage"]["totalImages"] == 20, "Failed to check scanned totalImages counter"
        if "printJobCount" in deviceusage_info["jobUsage"]: #Added this check as locally I cannot see printJobCount as part of jobUsage, but in chronicles it is there
            assert deviceusage_info["jobUsage"]["printJobCount"] == 2,"Failed to check print job counter"
        assert deviceusage_info["jobUsage"]["copyJobCount"] == 2,"Failed to check copy job counter"
        assert deviceusage_info["jobUsage"]["receiveFaxJobCount"] == 2,"Failed to check receive fax job counter"

    logging.info("Reset the print option")
    response = cdm.patch_raw(cdm.JOB_TICKET_CONFIGURATION_DEFAULT_PRINT, default_print_option)
    assert response.status_code == 200

    set_pagestosend(faxSimIp, pagestosend=1)
    udw.mainApp.ScanMedia.loadMedia("ADF")
    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check headed contention for max pages copy, scan to USB, receive fax, print from USB in contention 
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-141390
    +timeout:1260
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:letter_plain.jpg=15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9
    +test_classification:System
    +name:test_copy_contention_ui_followed_scan_to_usb_print_from_usb_receive_fax_jobs
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_contention_ui_followed_scan_to_usb_print_from_usb_receive_fax_jobs
        +guid:72b6662e-ee53-412b-9037-6b910d47795d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceFunction=Fax & ScanDestination=USB & DeviceFunction=PrintFromUsb & ScannerInput=AutomaticDocumentFeeder & JobSettings=JobConcurrency
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_ui_followed_scan_to_usb_print_from_usb_receive_fax_jobs(usb_removed_alert_cancel, setup_teardown_with_empty_usb_drive, setup_teardown_print_idle_status,setup_fax_using_cdm, spice, net, cdm, udw, job, counters, usbdevice, configuration, tray):
    """
    1. Settings/config details
    CP > Copy > Document Copy > Set number of Copies to 99. Start a copy job.
    Come back to Home screen. Load 10 pages in ADF. Go to CP > Scan > Scan to USB  > Click on Send to Start a job.
    Receive a fax job (2 pages)
    Go to Print > Print From USB > Start a Print job from CP.
    2. Validations/Expected Behavior
    Validate the complete job status - 
        Validate all the job status
        Validate the print usage counter at end
    """
    tray.reset_trays()
    default = tray.get_default_source()
    logging.info("Start 1st 99 pages copy job")
    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    udw.mainApp.ScanMedia.loadMedia("ADF")
    spice.copy_ui().goto_copy_from_copyapp_at_home_screen()
    spice.copy_ui().ui_copy_set_no_of_pages('99')
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().change_collate("off")
    spice.copy_ui().back_to_landing_view()
    spice.copy_ui().start_copy(familyname=configuration.familyname)
    spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Starting', wait_for_toast_dismiss=True)

    logging.info("Back to home screen from Copy landing screen")
    spice.goto_homescreen()

    logging.info("Start 2nd 30 page ADF Scan to USB job")
    udw.mainApp.ScanMedia.loadMedia("ADF")
    udw.mainApp.ScanDeviceService.setNumScanPages(30)
    spice.usb_scan.goto_scan_to_usb_screen()
    spice.usb_scan.wait_for_save_to_usb_landing_view()
    spice.usb_scan.press_save_to_usb()
    spice.scan_settings.wait_for_scan_status_toast(net, message="Sending", wait_for_toast_dismiss=True,time_out=120)

    logging.info("Back to home screen from Scan to USB landing screen")
    spice.goto_homescreen()

    logging.info("Start 3rd Receive a fax job (2 pages) job")
    faxSimIp = sys.argv[sys.argv.index('faxSimulatorIP')+1]
    set_pagestosend(faxSimIp, pagestosend = 2)
    Fax(cdm, udw).receive_fax(faxSimIp)

    logging.info("Start 4th Print from USB job")
    if tray.is_size_supported("na_letter_8.5x11in", default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    elif tray.is_type_supported("any", default):
        tray.configure_tray(default, 'any', 'stationery')
    usbroot = usbdevice.get_root('usbdisk1')
    print_file_name = "15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9"
    target_file_name = "letter_plain.jpg"
    usbdevice.upload_with_file_name(print_file_name, usbroot, target_file_name)
    spice.print_from_usb.goto_print_app()
    spice.print_from_usb.goto_print_from_usb()
    spice.print_from_usb.select_print_file_or_folder_by_name(target_file_name)
    spice.print_from_usb.start_print()
    logging.info("Back to home screen from Print From USB landing screen")
    spice.goto_homescreen()
    job.wait_for_no_active_jobs(time_out=1200)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"},
                                                                    {"type": "scanUsb", "status": "success"},
                                                                    {"type": "receiveFax", "status": "success"},
                                                                    {"type": "usbPrint", "status": "success"}])

    deviceusage_info = counters.deviceusage.get_device_usage()
    assert deviceusage_info["printUsage"]["sheets"]["total"] == 102, "Failed to check printed sheets total counter"
    assert deviceusage_info["scanUsage"]["totalImages"] == 31, "Failed to check scanned totalImages counter"
    assert deviceusage_info["jobUsage"]["copyJobCount"] == 1,"Failed to check copy job counter"
    assert deviceusage_info["jobUsage"]["receiveFaxJobCount"] == 1,"Failed to check receive fax job counter"
    assert deviceusage_info["jobUsage"]["removalStorageJobCount"] == 2,"Failed to check removal storage job counter"

    logging.info("cleaning up")
    set_pagestosend(faxSimIp, pagestosend = 1)
    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copy job and send to usb job should be success 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:700
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_contention_ui_copies_99_copy_job_and_send_to_usb_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_contention_ui_copies_99_copy_job_and_send_to_usb_job
        +guid:097877b2-c722-4dcf-a7b5-958ea677ca92
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & DeviceFunction=DigitalSend & ScanDestination=USB & JobSettings=JobConcurrency
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_contention_ui_copies_99_copy_job_and_send_to_usb_job(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    u = usb.Usb(cdm,udw,net)
    u.selectUsbDevice()
    try:
        job.bookmark_jobs()
        job.clear_joblog()
        copy_job_app = spice.copy_ui()
        options = {
            'copies':'99'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        copy_job_app.wait_for_copy_status_toast(net, configuration, message='Complete', timeout=180, wait_for_toast_dismiss=True)
        logging.info("Back to home screen from Copy landing screen")
        spice.goto_homescreen()
        spice.usb_scan.goto_scan_to_usb_screen()
        spice.usb_scan.wait_for_save_to_usb_landing_view()
        spice.usb_scan.press_save_to_usb()
        spice.scan_settings.wait_for_scan_status_toast(net,message="complete")
        job.wait_for_no_active_jobs(time_out=400)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"},
                                                                    {"type": "scanUsb", "status": "success"}], time_out=400)

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        #Remove usb drive
        u.deleteAllOutputFiles()
        u.removeUsbDevice()

