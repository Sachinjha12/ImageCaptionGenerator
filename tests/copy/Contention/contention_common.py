import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd
from tests.network.print.ipp_utils import execute_ipp_test_with_timeout



def send_print_job_from_usb(usbdevice, job, copies=1, file_name='f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e'):
    """
    Send print job from usb via cdm
    :param usbdevice:
    :param job:
    :param file_name:
    :param copies:
    :return: job_id
    """
    usb_root = usbdevice.get_root('usbdisk1')
    filepath = usbdevice.upload(file_name, usb_root)

    logging.info('Creating print from USB job ticket')
    resource = {'src': {'usb': {}}, 'dest': {'print': {}}}
    ticket_id = job.create_job_ticket(resource)

    resource = {
        'src': {
            'usb': {'path': filepath}
        },
        'dest': {
            'print': {
                'copies': copies,
                'mediaSource': 'auto',
                'mediaSize': 'na_letter_8.5x11in',
                'mediaType': 'stationery',
                'plexMode': 'simplex',
                'printQuality': 'normal',
                'colorMode': 'color'
            }
        }
    }

    logging.info('Updating print from USB job ticket with source and destination')
    job.update_job_ticket(ticket_id, resource)

    logging.info('Create a print job and retrieve print job id')
    job_id = job.create_job(ticket_id)

    logging.info('Initialize and start the print job - %s', job_id)
    job.change_job_state(job_id, 'initialize', 'initializeProcessing')
    job.check_job_state(job_id, 'ready', 30)
    job.change_job_state(job_id, 'start', 'startProcessing')

    return job_id


def execute_ipp_print_job(net, printjob, ipp_test_attribs = None, print_file = '15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9'):
    """
    Purpose: This method is execute ipp print job for contention. 
    This method does not wait for the job to complete
    param net
    param printjob
    param ipp_test_attribs
    param print_file
    return jobid
    """
    if ipp_test_attribs is None:
        ipp_test_attribs = {'document-format': 'image/jpeg' }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    print_file = printjob.get_file(print_file)
    logging.info("Start IPP Print job")
    returncode, decoded_output = execute_ipp_cmd(net.ip_address, ipp_test_file, print_file)
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'

    jobid = printjob.wait_for_jobs(assert_expected_jobs=False)

    return jobid

def execute_ipp_print_job_with_timeout(net, printjob, ipp_test_attribs = None, print_file = '15c9aa681a80be29e3743de3a5f26fb3d400365bf5c20dcc78b2889c1cc50ef9', timeout=120):
    """
    Purpose: This method is execute ipp print job for contention. 
    This method does not wait for the job to complete
    param net
    param printjob
    param ipp_test_attribs
    param print_file
    return jobid
    """
    if ipp_test_attribs is None:
        ipp_test_attribs = {'document-format': 'image/jpeg' }

    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    print_file = printjob.get_file(print_file)
    logging.info("Start IPP Print job")
    returncode = execute_ipp_test_with_timeout(net.ip_address, ipp_test_file, print_file,'',timeout)
    assert returncode == 0, "test_ipp_get_printer_attributes Failed."
    jobid = printjob.wait_for_jobs(assert_expected_jobs=False)
    return jobid


def execute_print_storejob(job, dunestorejob, storejob, passwords = ""):
    """
    Purpose: This method is execute_print_storejob for contention. 
    param job
    param dunestorejob
    param passwords
    return print_jobid
    """
    jobs = job.get_recent_job_ids()

    ticket_id = dunestorejob.retrieve(storejob, passwords)

    logging.info('Create a print job and retrieve print job id')
    print_jobid = job.create_job(ticket_id)

    logging.info('Initialize and start the print job - %s', print_jobid)
    job.change_job_state(print_jobid, 'initialize', 'initializeProcessing')
    job.check_job_state(print_jobid, "ready", 30)
    job.change_job_state(print_jobid, 'start', 'startProcessing')

    return print_jobid

def dismiss_load_paper_alert(cdm):
    """
    Purpose: Click OK button on Load Paper Error screen
    """

    logging.info("Try to dismiss_mdf_eject_page_alert")
    alert_detail = cdm.alerts.wait_for_alerts("mediaLoadFlow")[0]
    url = alert_detail["actions"]["links"][0]["href"]
    action_value = alert_detail["actions"]["supported"][0]["value"]["seValue"]
    cdm.put(url, {"selectedAction" : action_value})
