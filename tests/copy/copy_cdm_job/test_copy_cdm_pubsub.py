import logging
import sys
import pytest
import json
from dunetuf.cdm.Pubsub import PubSub
from tests.copy.copy_pubsub_payloads import *
from copy import deepcopy


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Pubsub subscription events for Copy Configuration
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-69060
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_cdm_pubsub_jobticket_defaults
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_pubsub_jobticket_defaults
        +guid:ea05aca2-e3cc-4eed-8ef0-d0c32688435e
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_pubsub_jobticket_defaults(cdm, configuration):
    try:
        default_payload = cdm.get(cdm.JOB_TICKET_COPY)
        #CREATE EVENT
        subscriptionId = cdm.PubSub.add_subscription_id( "com.hp.cdm.service.jobTicket.version.1.resource.copyConfigurationDefaults", "copyconfig", "copyconfig1")
        logging.info(subscriptionId)
        updated_default_payload = deepcopy(default_payload)
        updated_default_payload["pipelineOptions"]["scaling"]["scaleSelection"] = "custom"
        updated_default_payload["pipelineOptions"]["scaling"]["scaleToSize"] = "iso_a4_210x297mm"

        # If there is any Folder installed, folding style will change automatically by Force Sets in Patching interaction
        if configuration.familyname == "designjet" and cdm.get(cdm.MEDIA_FINISHER_CONFIGURATION)['folders'][0]['state'] == "ok":
            logging.info("Designjet Mfp products has Folder that will cause on patch interaction folding style auto adjust.")
            logging.info("force folding state expected to avoid issue")
            updated_default_payload['dest']['print']['foldingStyleId'] = 256

        response = cdm.patch_raw(cdm.JOB_TICKET_COPY, updated_default_payload)
        assert response.status_code == 200, "PATCH OPERATION WAS SUCCESSFUL" + cdm.JOB_TICKET_COPY
        #VALIDATE EVENT
        cdm.PubSub.validate_subscription_event( subscriptionId, updated_default_payload)
        #DELETE EVENT
        cdm.PubSub.delete_subscription( subscriptionId + "?clientId=copyconfig", "com.hp.cdm.service.jobTicket.version.1.resource.copyConfigurationDefaults")
    finally:
        r = cdm.put_raw(cdm.JOB_TICKET_COPY, default_payload)
        assert r.status_code == 200
