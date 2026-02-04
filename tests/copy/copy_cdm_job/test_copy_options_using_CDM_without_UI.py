import logging
import json
import pprint

from dunetuf.copy.copy import *

import pytest


payload = {
            'src': {
                'scan': {
                    'colorMode':'color',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'edgeToEdgeScan':'false',
                    'longPlotScan':'false',
                    'invertColors':'false',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'printMargins':'clipContents',
                }
            }
        }

payload2 = {
            'src': {
                'scan': {
                    'colorMode':'color',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'edgeToEdgeScan':'true',
                    'longPlotScan':'true',
                    'invertColors':'true',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'printMargins':'oversize',
                }
            }
        }

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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_copy_clone_job_ticket_and_validate_src_options
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-71948
    +timeout:120
    +asset: LFP
    +test_framework: TUF
    +name: test_copy_clone_job_ticket_and_validate_src_options
    +test:
        +title: test_copy_clone_job_ticket_and_validate_src_options
        +guid:be799e46-3615-40e2-9fbf-231a9b0a1003
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_clone_job_ticket_and_validate_src_options(cdm, udw, net):
    
    print("test_copy_jobticket_clone: BEGIN")

    print("1. Creating a new ticket")
  
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default fields")
    assert ticket_user_body['src']['scan']['edgeToEdgeScan'] == 'false'
    assert ticket_user_body['src']['scan']['longPlotScan'] == 'false'
    assert ticket_user_body['src']['scan']['invertColors'] == 'false'

    print("3. Updating the ticket")
    print("Updating edgeToEdgeScan in scan")
    ticket_user_body['src']['scan']['edgeToEdgeScan'] = 'true'
    print("Updating longPlotScan in scan")
    ticket_user_body['src']['scan']['longPlotScan'] = 'true'
    print("Updating invertColors in scan")
    ticket_user_body['src']['scan']['invertColors'] = 'true'
    
    ticket_body = {'src': {'scan': {'edgeToEdgeScan': 'true', 'longPlotScan': 'true', 'invertColors': 'true'}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the values")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
  
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the values")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the values")
    assert ticket_user_body['src']['scan']['edgeToEdgeScan'] == 'true'
    assert ticket_user_body['src']['scan']['longPlotScan'] == 'true'
    assert ticket_user_body['src']['scan']['invertColors'] == 'true'

    assert_field_equal(ticket_user_body['src']['scan'], new_ticket_user_body['src']['scan'])
    assert_field_equal(ticket_user_body['dest']['print'], new_ticket_user_body['dest']['print'])    


    """
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using the A4 paper size
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-71948
    +timeout:120
    +asset: LFP
    +test_framework: TUF
    +name: test_copy_clone_job_ticket_and_validate_dest_option
    +test:
        +title: test_copy_clone_job_ticket_and_validate_dest_option
        +guid:a94ee19e-ebee-11ec-a027-2f7e996eb625
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_clone_job_ticket_and_validate_dest_option(cdm, udw, net):
    
    default_payload = cdm.get(cdm.JOB_TICKET_COPY)
    print("test_copy_jobticket_clone: BEGIN")
    copy = Copy(cdm,udw)
    print("1. Creating a new ticket")

    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default field")
    assert ticket_user_body['dest']['print']['printMargins'] == 'clipContents'

    print("3. Updating the ticket")
    print("Updating printMargins in print")
    update_print_margins = ""
    if copy.is_constraints_include_print_margins_in_cdm("oversize"):
        update_print_margins = "oversize"
    elif copy.is_constraints_include_print_margins_in_cdm("addToContents"):
        update_print_margins = "addToContents"
    else:
        update_print_margins = "clipContents"     

    ticket_user_body['dest']['print']['printMargins'] = update_print_margins
    ticket_body = {'dest': {'print': {'printMargins': update_print_margins}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the values")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
   
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the values")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the values")
    assert ticket_user_body['dest']['print']['printMargins'] == update_print_margins

    assert_field_equal(ticket_user_body['src']['scan'], new_ticket_user_body['src']['scan'])
    assert_field_equal(ticket_user_body['dest']['print'], new_ticket_user_body['dest']['print'])
    r = cdm.put_raw(cdm.JOB_TICKET_COPY, default_payload)
    assert r.status_code == 200

    """
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using finisher media destination
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-154785
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +name: test_copy_clone_job_ticket_and_validate_dest_media_option
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title: test_copy_clone_job_ticket_and_validate_dest_media_option
        +guid:36848e2a-c90a-4033-b9ac-ed939483fd68
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & ScannerInput=Flatbed
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_clone_job_ticket_and_validate_dest_media_option(cdm, udw, net):
    
    default_payload = cdm.get(cdm.JOB_TICKET_COPY)
    print("test_copy_jobticket_clone: BEGIN")
    copy = Copy(cdm,udw)
    print("1. Creating a new ticket")
  
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default field")
    assert (ticket_user_body['dest']['print']['mediaDestination'] == 'auto' or ticket_user_body['dest']['print']['mediaDestination'] == 'standard-bin')

    print("3. Updating the ticket")
    print("Updating mediaDestination in print")
    update_media_destination = ""
    if copy.is_constraints_include_media_destination_in_cdm("tray-1"):
        update_media_destination = "tray-1"
    elif copy.is_constraints_include_media_destination_in_cdm("tray-2"):
        update_media_destination = "tray-2"    
    elif copy.is_constraints_include_media_destination_in_cdm("tray-3"):
        update_media_destination = "tray-3"
    elif copy.is_constraints_include_media_destination_in_cdm("standard-bin"):
        update_media_destination = "standard-bin"
    else:
        update_media_destination = "auto"

    ticket_user_body['dest']['print']['mediaDestination'] = update_media_destination
    ticket_body = {'dest': {'print': {'mediaDestination': update_media_destination}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the values")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
   
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the values")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the values")
    assert ticket_user_body['dest']['print']['mediaDestination'] == update_media_destination

    assert_field_equal(ticket_user_body['src']['scan'], new_ticket_user_body['src']['scan'])
    assert_field_equal(ticket_user_body['dest']['print'], new_ticket_user_body['dest']['print'])

    """
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using finisher staple option
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-142400
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +name: test_copy_cdm_staple_options
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title: test_copy_cdm_staple_options
        +guid:4f242bb4-38d3-4a34-b8bd-990f3d4e8269
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & ScannerInput=Flatbed
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_staple_options(cdm, udw, net):
    
    default_payload = cdm.get(cdm.JOB_TICKET_COPY)
    print("test_copy_jobticket_clone: BEGIN")
    copy = Copy(cdm,udw)
    print("1. Creating a new ticket")
   
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default field")
    assert (ticket_user_body['dest']['print']['stapleOption'] == 'none')

    print("3. Updating the ticket")
    print("Updating staple option in print")
    update_staple_option = ""
    if copy.is_constraints_include_staple_option_in_cdm("topAnyOnePointAny"):
        update_staple_option = "topAnyOnePointAny"
    elif copy.is_constraints_include_staple_option_in_cdm("topLeftOnePointAngled"):
        update_staple_option = "topLeftOnePointAngled"    
    else:
        update_staple_option = "none"

    ticket_user_body['dest']['print']['stapleOption'] = update_staple_option
    ticket_body = {'dest': {'print': {'stapleOption': update_staple_option}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the values")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
    
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the values")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the values")
    assert ticket_user_body['dest']['print']['stapleOption'] == update_staple_option

    assert_field_equal(ticket_user_body['src']['scan'], new_ticket_user_body['src']['scan'])
    assert_field_equal(ticket_user_body['dest']['print'], new_ticket_user_body['dest']['print'])

    """
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using finisher punch option
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-142400
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +name: test_copy_cdm_punch_options
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test:
        +title: test_copy_cdm_punch_options
        +guid:c1403a89-b17a-441b-a477-9020699d1f85
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & ScannerInput=Flatbed
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_punch_options(cdm, udw, net):
    
    default_payload = cdm.get(cdm.JOB_TICKET_COPY)
    print("test_copy_jobticket_clone: BEGIN")
    copy = Copy(cdm,udw)
    print("1. Creating a new ticket")
  
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    print("2. Validating the default field")
    assert (ticket_user_body['dest']['print']['stapleOption'] == 'none')

    print("3. Updating the ticket")
    print("Updating staple option in print")
    update_punch_option = ""
    if copy.is_constraints_include_punch_option_in_cdm("leftTwoPointDin"):
        update_punch_option = "leftTwoPointDin"
    elif copy.is_constraints_include_punch_option_in_cdm("leftThreePointUs"):
        update_punch_option = "leftThreePointUs"
    elif copy.is_constraints_include_punch_option_in_cdm("leftFourPointSwd"):
        update_punch_option = "leftFourPointSwd"    
    else:
        update_punch_option = "none"

    ticket_user_body['dest']['print']['punchOption'] = update_punch_option
    ticket_body = {'dest': {'print': {'punchOption': update_punch_option}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' + ticket_user_body['ticketId']
    print("PATCH the values")
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("4. Cloning the ticket")
   
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    print("POST the values")
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    
    print("5. Validate the values")
    assert ticket_user_body['dest']['print']['punchOption'] == update_punch_option

    assert_field_equal(ticket_user_body['src']['scan'], new_ticket_user_body['src']['scan'])
    assert_field_equal(ticket_user_body['dest']['print'], new_ticket_user_body['dest']['print'])

