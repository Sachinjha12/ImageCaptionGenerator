import logging
from time import sleep
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
import json
import pprint
import pytest


# HELPER METHODS - BEGIN

def source_destination(source,dest):
    return {'src': {source:{}}, 'dest': {dest:{}} }

def extract_src_dest(body):
    keys = ["src", "dest"]
    return { key: body[key] for key in keys }

def assert_field_equal(body_a, body_b):
    assert(isinstance(body_a,dict))
    assert(isinstance(body_b,dict))
    for key in body_a:
        if( key in body_b.keys() ):
            if( isinstance(body_a[key], dict) ):
                assert_field_equal(body_a[key],body_b[key])
            else:
              assert(body_a[key] == body_b[key])
    pass

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test id card copy in CDM with grayscale
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-106894
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_idcard_color_grayscale
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_cdm_idcard_color_grayscale
        +guid:24719681-4571-4ca8-864d-59ea10e0ba4a
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy & Copy=GrayScale
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_cdm_idcard_color_grayscale(cdm, udw, net, configuration):
    
    print("test_copy_jobticket_clone: BEGIN")

    print("1. Creating a new ticket")
    
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default field")
    if configuration.familyname == 'enterprise':
        if cdm.device_feature_cdm.is_color_supported():        
            assert ticket_user_body['src']['scan']['colorMode'] == 'autoDetect'
        else:
            assert ticket_user_body['src']['scan']['colorMode'] == 'grayscale'
    else:
        assert ticket_user_body['src']['scan']['colorMode'] == 'color'
    
    print("3. Updating the ticket")
    print("Updating colorMode in scan")
    ticket_user_body['src']['scan']['colorMode'] = 'grayscale'
    
    ticket_body = {'src': {'scan': {'colorMode': 'grayscale'}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the value")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
   
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the value")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the values")
    assert ticket_user_body['src']['scan']['colorMode'] == 'grayscale'

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test id card copy in CDM with blackonly
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-106894
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_idcard_color_blackonly
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_cdm_idcard_color_blackonly
        +guid:0370e74b-e628-4792-9f2b-b0567c910e7a
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy & Copy=BlackOnly
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_cdm_idcard_color_blackonly(cdm, udw, net):
    
    print("test_copy_jobticket_clone: BEGIN")

    print("1. Creating a new ticket")
   
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default field")
    assert ticket_user_body['src']['scan']['colorMode'] == 'color'
    
    print("3. Updating the ticket")
    print("Updating colorMode in scan")
    ticket_user_body['src']['scan']['colorMode'] = 'blackonly'
    
    ticket_body = {'src': {'scan': {'colorMode': 'blackonly'}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the value")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
   
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the value")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the value")
    assert ticket_user_body['src']['scan']['colorMode'] == 'blackonly'
    
