import logging
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job

def assert_field_equal(body_a, body_b):
    '''
    Compare all the fields of body_a and body_b
    Throw assert, if fields are not equal
    '''
    assert(isinstance(body_a,dict))
    assert(isinstance(body_b,dict))
    for key in body_a:
        if( key in body_b.keys() ):
            if( isinstance(body_a[key], dict) ):
                logging.info("%s body_a comparing to body_b %s ",body_a[key], body_b[key])
                assert_field_equal(body_a[key],body_b[key])
            else:
                logging.info("%s body_a comparing to body_b %s ",body_a[key], body_b[key])
                assert(body_a[key] == body_b[key])
    pass


def perform_copy_job_through_quickset(scan_emulation, cdm, udw, spice, net, job, quickset_name, settings: dict, scanner_source="ADF"):
    '''
    Perform a Copy job through Custom quickset
    '''
    # Clear all the previous jobs data
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Clear previous jobIds")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    logging.info("Enter in try block")

    try:
        #enable duplex support for tests with 1-2 and 2-2 sides
        spice.copy_ui().enable_duplex_supported(cdm,udw)
        
        # get a shortcut service object
        cdm_shortcut_service = CDMShortcuts(cdm, net)
        logging.info("Create a copy job ticket")

        # create a copy job ticket
        ticket_body = create_copy_job_ticket(cdm)
        jobticketid = ticket_body.get('ticketId')
        logging.info("copy job ticket created %s", jobticketid)

        # Modify the copy job ticket with settings
        logging.info("Modify job ticket with the settings")
        logging.info(settings)
        modify_copy_job_ticket(cdm, ticket_body, jobticketid, settings)
        logging.info("iJob ticket Modified")

        # create custom quickset
        shortcut_id = str(uuid.uuid4())
        logging.info("Create a shortcut quickset %s", shortcut_id)
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticketid
        cdm_shortcut_service.create_custom_shortcut_with_href(quickset_name, shortcut_id, "scan", [
                                   "print"], "open", "true", False, href)
        logging.info("Custom quickset created %s", quickset_name)

        # Go To Copy App and select Quickset -> Start job
        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#" + quickset_name)

        spice.copy_ui().start_copy()

        copy_job_details_body = job.get_job_details(current_job_type="copy")

        # Wait for job to complete
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        job.wait_for_no_active_jobs()

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
        assert_field_equal(ticket_body['src']['scan'], copy_job_details_body['src']['scan'])
        assert_field_equal(ticket_body['dest']['print'], copy_job_details_body['dest']['print'])

    finally:
        logging.info("Enter in finally")
        spice.goto_homescreen_back_button()
        # delete previously added shorcut
        cdm_shortcut_service.delete_shortcut(shortcut_id)
        udw.mainApp.ScanCapabilities.setHasDuplexSupport(False)

def create_copy_job_ticket(cdm, ticket_reference = "defaults/copy"):
    '''
    create a copy job ticket and retrun it response
    '''
    payload = {
        "ticketReference": ticket_reference
    }

    response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, payload)
    assert response.status_code == 201
    return response.json()

def modify_copy_job_ticket(cdm, ticket_body, jobticketId, settings: dict):
    '''
    modify copy job ticket for quickset creation
    '''

    if "sides" in settings.keys():
        logging.info("set the sides %s", settings["sides"])
        if settings["sides"] == "1_1Sided":
            settings["inputPlexMode"] = "simplex"
            settings["outputPlexMode"] = "simplex"
            settings["duplexBinding"] = "oneSided"
        elif settings["sides"] == "1_2Sided":
            settings["inputPlexMode"] = "simplex"
            settings["outputPlexMode"] = "duplex"
            settings["duplexBinding"] = "twoSidedLongEdge"
        elif settings["sides"] == "2_1Sided":
            settings["inputPlexMode"] = "duplex"
            settings["outputPlexMode"] = "simplex"
            settings["duplexBinding"] = "oneSided"
        else:
            settings["inputPlexMode"] = "duplex"
            settings["outputPlexMode"] = "duplex"
            settings["duplexBinding"] = "twoSidedLongEdge"
    
    if "pageFlipUpEnable" in settings.keys():
        if settings["pageFlipUpEnable"]:
            settings["duplexBinding"] = "twoSidedShortEdge"
        else:
            settings["duplexBinding"] = "twoSidedLongEdge"
        
    
    if "outputScale" in settings.keys():
        if settings["outputScale"] == "custom":
            ticket_body["pipelineOptions"]["scaling"]["scaleSelection"] = settings["outputScale"]
            ticket_body["pipelineOptions"]["scaling"]["xScalePercent"] = settings["customValue"]
            ticket_body["pipelineOptions"]["scaling"]["yScalePercent"] = settings["customValue"]
        elif settings["outputScale"] == "fitToPage":
            ticket_body["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = True
            ticket_body["pipelineOptions"]["scaling"]["scaleSelection"] = settings["outputScale"]
            ticket_body["pipelineOptions"]["scaling"]["xScalePercent"] = 100
            ticket_body["pipelineOptions"]["scaling"]["yScalePercent"] = 100
        elif settings["outputScale"] == "fullPage":
            ticket_body["pipelineOptions"]["scaling"]["scaleSelection"] = settings["outputScale"]
            ticket_body["pipelineOptions"]["scaling"]["xScalePercent"] = 91
            ticket_body["pipelineOptions"]["scaling"]["yScalePercent"] = 91
        elif settings["outputScale"] == "legalToLetter":
            ticket_body["pipelineOptions"]["scaling"]["scaleSelection"] = settings["outputScale"]
            ticket_body["pipelineOptions"]["scaling"]["xScalePercent"] = 72
            ticket_body["pipelineOptions"]["scaling"]["yScalePercent"] = 72
        elif settings["outputScale"] == "letterToA4":
            ticket_body["pipelineOptions"]["scaling"]["scaleSelection"] = settings["outputScale"]
            ticket_body["pipelineOptions"]["scaling"]["xScalePercent"] = 94
            ticket_body["pipelineOptions"]["scaling"]["yScalePercent"] = 94
        else:
            ticket_body["pipelineOptions"]["scaling"]["scaleSelection"] = settings["outputScale"]
            ticket_body["pipelineOptions"]["scaling"]["xScalePercent"] = 100
            ticket_body["pipelineOptions"]["scaling"]["yScalePercent"] = 100



    if "colorMode" in settings.keys():
        logging.info("setting the colorMode to %s", settings["colorMode"])
        ticket_body["src"]["scan"]["colorMode"] = settings["colorMode"]
    
    if "inputMediaSize" in settings.keys():
        logging.info("setting the inputMediaSize to %s", settings["inputMediaSize"])
        ticket_body["src"]["scan"]["mediaSize"] = settings["inputMediaSize"]
    
    if "inputPlexMode" in settings.keys():
        logging.info("setting the inputPlexMode to %s", settings["inputPlexMode"])
        ticket_body["src"]["scan"]["plexMode"] = settings["inputPlexMode"]
    
    if "contentType" in settings.keys():
        logging.info("setting the contentType to %s", settings["contentType"])
        ticket_body["src"]["scan"]["contentType"] = settings["contentType"]
    
    if "lighterDarker" in settings.keys():
        logging.info("setting the lighterDarker to %s", settings["lighterDarker"])
        ticket_body["pipelineOptions"]["imageModifications"]["exposure"] = settings["lighterDarker"]
    
    if "pagesPerSheet" in settings.keys():
        logging.info("setting the pagesPerSheet to %s", settings["pagesPerSheet"])
        ticket_body["pipelineOptions"]["imageModifications"]["pagesPerSheet"] = settings["pagesPerSheet"]
    
    if "collate" in settings.keys():
        logging.info("setting the collate to %s", settings["collate"])
        ticket_body["dest"]["print"]["collate"] = settings["collate"]
    
    if "copies" in settings.keys():
        logging.info("setting the copies to %s", settings["copies"])
        ticket_body["dest"]["print"]["copies"] = settings["copies"]
    
    if "outputMediaSource" in settings.keys():
        logging.info("setting the outputMediaSource to %s", settings["outputMediaSource"])
        ticket_body["dest"]["print"]["mediaSource"] = settings["outputMediaSource"]
    
    if "outputMediaSize" in settings.keys():
        logging.info("setting the outputMediaSize to %s", settings["outputMediaSize"])
        ticket_body["dest"]["print"]["mediaSize"] = settings["outputMediaSize"]
    else: 
        if ticket_body['dest']['print']['mediaSize'] == 'any':
            ticket_body['dest']['print']['mediaSize'] = 'na_letter_8.5x11in'
    
    if "outputMediaType" in settings.keys():
        logging.info("setting the outputMediaType to %s", settings["outputMediaType"])
        ticket_body["dest"]["print"]["mediaType"] = settings["outputMediaType"]
    
    if "outputPlexMode" in settings.keys():
        logging.info("setting the outputPlexMode to %s", settings["outputPlexMode"])
        ticket_body["dest"]["print"]["plexMode"] = settings["outputPlexMode"]
    
    if "duplexBinding" in settings.keys():
        logging.info("setting the duplexBinding to %s", settings["duplexBinding"])
        ticket_body["dest"]["print"]["duplexBinding"] = settings["duplexBinding"]
    
    if "printQuality" in settings.keys():
        logging.info("setting the printQuality to %s", settings["printQuality"])
        ticket_body["dest"]["print"]["printQuality"] = settings["printQuality"]

    uri = cdm.JOB_TICKET_ENDPOINT + "/" + jobticketId
    response = cdm.patch_raw(uri, ticket_body)
    assert response.status_code == 200
    
