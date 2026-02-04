import json
from pprint import pprint
import random
import logging
from typing import Dict, List
from multiprocessing.dummy import Pool as ThreadPool

import pytest
import time

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


def get_ticket(cdm, ticket_id: str) -> Dict:
    rep = cdm.get_raw(cdm.JOB_TICKET_MODIFY_ENDPOINT.format(ticket_id))
    return rep.json()


def set_ticket(cdm, ticket_id: str, body: Dict):
    rep = cdm.patch_raw(cdm.JOB_TICKET_MODIFY_ENDPOINT.format(ticket_id), body)
    rep.raise_for_status()


def get_constraints(cdm, ticket_id: str) -> Dict:
    rep = cdm.get_raw(cdm.JOB_TICKET_MODIFY_ENDPOINT_CONSTRAINTS.format(ticket_id))
    rep.raise_for_status()
    return rep.json()['validators']


def enabled_options(validators: Dict, path: str) -> List[str]:
    prop = [x for x in validators if x['propertyPointer'] == path][0]
    enabled = [x['seValue'] for x in prop['options']
               if ('disabled' not in x) or x['disabled'] == 'false']
    logging.debug(f'{path}: enabled options: {enabled}')
    return enabled


# HELPER METHODS - BEGIN

def source_destination(source, dest):
    return {'src': {source: {}}, 'dest': {dest: {}}}


def extract_src_dest(body):
    keys = ["src", "dest"]
    return {key: body[key] for key in keys}


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

def source_mediasource(mediasource):
    return {'src': {'scan': {}}, 'dest': {'print': {'mediaSource': mediasource}}}

def find_constraint(constraints_json, constraint_path):
    for validator in constraints_json['validators'] :
        if validator['propertyPointer'] == constraint_path :
            return validator
    return None

def find_validator_option(validator, seValue):
    for dude in validator['options']:
        if seValue == dude['seValue']:
            return dude
    return None

def count_disabled_options(the_list):
    disabled_count = 0
    for i in range(len(the_list)):
        if 'disabled' in the_list[i]:
            disabled_count = disabled_count + 1
    return disabled_count

def singleMediaSourceDevice(the_list):
    isSingleMediaSource = True
    count = 0
    for i in range(len(the_list)):
        list_item = the_list[i]
        if list_item['seValue'] == 'auto':
            continue 
        else:
            count = count + 1

    if count > 1:
        isSingleMediaSource = False        
    return isSingleMediaSource

# Expects the patch operation to return a status code of 400
# Should return empty string on success, error message on failure
def expect_patch_failure( cdm, ticket_path, table ):
    retVal = ""
    #print("Patching ticket with: " + json.dumps(table))
    result = cdm.patch_raw(ticket_path, table).status_code
    if result != 400 :
        #retVal = "Error! Code = " + result +" Patching: "+ json.dumps(table)
        retVal = "    expect_patch_failure Error! Code ={0} Payload: {1}\n".format(result, json.dumps(table))
    return retVal

# Expects the patch operation to return a status code of 200
# Should return empty string on success, error message on failure
def expect_patch_success( cdm, ticket_path, table ):
    retVal = ""
    #print("Patching ticket with: " + json.dumps(table))
    result = cdm.patch_raw(ticket_path, table).status_code
    print("expect_patch_success result : {0}".format( result) )
    if result != 200 :
        retVal = "    expect_patch_success Error! Code ={0} Payload: {1}\n".format(result, json.dumps(table))
    return retVal

def is_disabled(disabled_options, value):
    for option in disabled_options:
        if option["seValue"] == value:
            return option["disabled"] == 'true'
    return False

def is_enabled(available_options, value):
    for option in available_options:
        if option["seValue"] == value :
            return True
    return False

def expected_min_max(constraints_json, min, max):
    if constraints_json["min"]["value"] != min:
        return False
    if constraints_json["max"]["value"] != max:
        return False
    return True

def flatten_dict(init_dict):
    res_dict = {}
    if type(init_dict) is not dict:
        return res_dict

    for k, v in init_dict.items():
        if type(v) == dict:
            res_dict.update(flatten_dict(v))
        else:
            res_dict[k] = v

    return res_dict

def constrain_disabled(constraints_json):
    return constraints_json["disabled"]["value"] == 'true'

def check_output_content_orientation(cdm, url, content_orientation):
    current_ticket = cdm.get(url)
    return current_ticket['pipelineOptions']['imageModifications']['outputCanvasOrientation'] == content_orientation


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Basic job ticket constraints verification. Specifically for Jupiter/MFP it checks that at least the needed media destinations are present.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-78658
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_jupiter_jobticket_media_output_destination
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_cdm_jupiter_jobticket_media_output_destination
        +guid: bdd588f9-8d10-4bc2-8585-18990ab4375e
        +dut:
            +type: Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & CopyOutputDestination=Stacker
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_jupiter_jobticket_media_output_destination(cdm, udw, net):
    print("\ntest_copy_jobticket_auto_constraints_cdm: BEGIN")

    # Create a new ticket.
    
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300

    ticket_user_body = ticket_user_response.json()

    # Get constraints.
    uri = ticket_user_body["links"][1].get("href")
    constraint_response = cdm.get(uri, None)

    # Gather Resolution values present in constraints.
    found_size_list = []

    for x in constraint_response["validators"]:
        if x["propertyPointer"] == "dest/print/mediaDestination":
            for y in x.get("options"):
                found_size_list.append(y["seValue"])

    # Check size.
    assert( len(found_size_list) >= 1 )

    # Check we have the ones needed.
    assert( "stacker-1" in found_size_list )
    # On future, could we need to add Folder here

    print("\ntest_copy_jobticket_auto_constraints_cdm: END")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Basic job ticket constraints verification
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-21596
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_jobticket_constraints_cdm
        +guid: 4a2895d4-87c9-4683-8ba9-6792ba2d76cc
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

def test_copy_jobticket_constraints_cdm(cdm, udw, net):
    print("\ntest_copy_jobticket_constraints_cdm: BEGIN")

    print("1. creating a new ticket")
   
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()
    print("ticket_user_body: %s" % ticket_user_body)

    print("2. parsing constraints link")
    uri = ticket_user_body["links"][1].get("href")
    print("uri: %s" % uri)
    print("3. requesting constraints")
    ticket_default_response = cdm.get(uri, None)
    print("version: ", ticket_default_response["version"])

    print("4. requesting constraints again to verify they can be read more than once")
    ticket_user_response = cdm.get(uri)
    print("version: ", ticket_user_response["version"])
    found_list = {}
    for x in ticket_user_response["validators"]:
        print("Property: ", x["propertyPointer"])
        found_list[x["propertyPointer"]] = "true"
    assert (found_list.get("dest/print/collate") == "true")
    assert (found_list.get("dest/print/copies") == "true")
    assert (found_list.get("dest/print/mediaSize") == "true")
    assert (found_list.get("dest/print/mediaSource") == "true")
    assert (found_list.get("dest/print/duplexBinding") == "true")
    assert (found_list.get("dest/print/plexMode") == "true")
    assert (found_list.get("garbage!!!") != "true")

    assert (found_list.get("src/scan/plexMode") == "true")
    assert (found_list.get("src/scan/descreen") == "true")
    assert (found_list.get("src/scan/resolution") == "true")

    print("\ntest_copy_jobticket_constraints_cdm: END")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Basic job ticket constraints verification. Specifically for Jupiter/MFP it checks that at least the needed resolutions are present.
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-79762
    +timeout:120
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_jupiter_jobticket_resolution_cdm
    +test:
        +title: test_copy_jupiter_jobticket_resolution_cdm
        +guid: e8799fea-4999-4394-a75e-c12d809e1ff9
        +dut:
            +type: Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_jupiter_jobticket_resolution_cdm(cdm, udw, net):
    print("\ntest_copy_jobticket_auto_constraints_cdm: BEGIN")

    # Create a new ticket.
    
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300

    ticket_user_body = ticket_user_response.json()

    # Get constraints.
    uri = ticket_user_body["links"][1].get("href")
    constraint_response = cdm.get(uri, None)

    # Gather Resolution values present in constraints.
    found_size_list = []

    for x in constraint_response["validators"]:
        if x["propertyPointer"] == "src/scan/resolution":
            for y in x.get("options"):
                found_size_list.append(y["seValue"])

    # Check size.
    assert( len(found_size_list) >= 3 )

    # Check we have the ones needed.
    assert( "e200Dpi" in found_size_list )
    assert( "e300Dpi" in found_size_list )
    assert( "e600Dpi" in found_size_list )
    # 1200 should be present but it is not supported yet.
    #assert( "e1200Dpi" in found_size_list )

    print("\ntest_copy_jobticket_auto_constraints_cdm: END")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Get Media sizes/types from Constraints When Mediasource is Auto.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-30588
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_auto_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_jobticket_auto_constraints_cdm
        +guid:5e012585-4dce-4de6-9556-5229650b0b7d
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
def test_copy_jobticket_auto_constraints_cdm(cdm, udw, net):
    print("\ntest_copy_jobticket_auto_constraints_cdm: BEGIN")

    print("1. creating a new ticket")
    
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()
    print("ticket_user_body: %s" % ticket_user_body)

    print("\n2. parsing constraints link")
    uri = ticket_user_body["links"][1].get("href")
    print("uri: %s" % uri)
    print("3. requesting constraints")
    ticket_user_response = cdm.get(uri, None)

    print("4. getting media sizes and media types")
    found_size_list = []
    found_type_list = []

    for x in ticket_user_response["validators"]:
        if x["propertyPointer"] == "dest/print/mediaSize":
            for y in x.get("options"):
                found_size_list.append(y["seValue"])
        elif x["propertyPointer"] == "dest/print/mediaType":
            for y in x.get("options"):
                found_type_list.append(y["seValue"])

    print("----------------MediaSize----------------")
    print("size of found_size_list ", len(found_size_list))
    for x in found_size_list:
        print(x)
    print("-----------------------------------------")
    print("----------------MediaType----------------")
    print("size of found_type_list ", len(found_type_list))
    for x in found_type_list:
        print(x)
    print("-----------------------------------------")

    print("\ntest_copy_jobticket_auto_constraints_cdm: END")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Get Media sizes/types from Constraints When Mediasource is Tray1.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-30588
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_tray1_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_jobticket_tray1_constraints_cdm
        +guid:03fa3fcf-c1af-4427-9712-66a3d614e4ef
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=Tray1

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_jobticket_tray1_constraints_cdm(cdm, udw, net, tray):
    print("\ntest_copy_jobticket_tray1_constraints_cdm: BEGIN")

    print("1. creating a new ticket")
   
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    default_tray = tray.get_default_source()
    if default_tray == 'main':
        body = source_mediasource("alternate")
    else:
        body = source_mediasource("tray-1")
    print("Ticket Path ", ticket_path)
    ticket_user_updated_response = cdm.patch_raw(ticket_path, body)
    pprint(ticket_user_updated_response)
    assert ticket_user_updated_response.status_code < 300
    print("3. getting jobticket again.")
    ticket_user_response = cdm.get(ticket_path)
    print("ticket_user_body ", ticket_user_response)

    print("\n4. parsing constraints link")
    uri = ticket_user_response["links"][1].get("href")
    print("uri: %s" % uri)
    print("5. requesting constraints")
    ticket_user_response = cdm.get(uri, None)

    print("6. getting media sizes and media types")
    found_size_list = []
    found_type_list = []

    for x in ticket_user_response["validators"]:
        if x["propertyPointer"] == "dest/print/mediaSize":
            for y in x.get("options"):
                found_size_list.append(y["seValue"])
        elif x["propertyPointer"] == "dest/print/mediaType":
            for y in x.get("options"):
                found_type_list.append(y["seValue"])

    print("----------------MediaSize----------------")
    print("size of found_size_list ", len(found_size_list))
    for x in found_size_list:
        print(x)
    print("-----------------------------------------")
    print("----------------MediaType----------------")
    print("size of found_type_list ", len(found_type_list))
    for x in found_type_list:
        print(x)
    print("-----------------------------------------")

    print("\ntest_copy_jobticket_tray1_constraints_cdm: END")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Get Media sizes/types from Constraints When Mediasource is Tray2.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-30588
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_tray2_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_jobticket_tray2_constraints_cdm
        +guid:7cd71dc6-df69-424a-8823-62483f10831d
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=Tray2

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_jobticket_tray2_constraints_cdm(cdm, udw, net, tray):
    print("\ntest_copy_jobticket_tray2_constraints_cdm: BEGIN")

    print("1. creating a new ticket")
    
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    default_tray = tray.get_default_source()
    if default_tray == 'main':
        body = source_mediasource("alternate")
    else:
        body = source_mediasource("tray-2")
    print("Ticket Path ", ticket_path)
    ticket_user_updated_response = cdm.patch_raw(ticket_path, body)
    assert ticket_user_updated_response.status_code < 300
    print("3. getting jobticket again.")
    ticket_user_response = cdm.get(ticket_path)
    print("ticket_user_body ", ticket_user_response)

    print("\n4. parsing constraints link")
    uri = ticket_user_response["links"][1].get("href")
    print("uri: %s" % uri)
    print("5. requesting constraints")
    ticket_user_response = cdm.get(uri, None)

    print("6. getting media sizes and media types")
    found_size_list = []
    found_type_list = []

    for x in ticket_user_response["validators"]:
        if x["propertyPointer"] == "dest/print/mediaSize":
            for y in x.get("options"):
                found_size_list.append(y["seValue"])
        elif x["propertyPointer"] == "dest/print/mediaType":
            for y in x.get("options"):
                found_type_list.append(y["seValue"])

    print("----------------MediaSize----------------")
    print("size of found_size_list ", len(found_size_list))
    for x in found_size_list:
        print(x)
    print("-----------------------------------------")
    print("----------------MediaType----------------")
    print("size of found_type_list ", len(found_type_list))
    for x in found_type_list:
        print(x)
    print("-----------------------------------------")

    print("\ntest_copy_jobticket_tray2_constraints_cdm: END")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Get Constraint related to the scan media interfaces.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-45031
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_related_to_scanmedia_interface_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_related_to_scanmedia_interface_cdm
        +guid:75ba966e-3627-4e88-b1ab-b43ea2756567
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
def test_copy_constraints_related_to_scanmedia_interface_cdm(cdm, udw, net):
    print("\ntest_copy_constraints_related_to_scanMedia_interface_cdm: BEGIN")

    print("1. creating a new ticket")
   
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    print("Ticket Path ", ticket_path)
    ticket_user_updated_response = cdm.patch_raw(ticket_path, body)
    assert ticket_user_updated_response.status_code < 300
    print("3. getting jobticket again.")
    ticket_user_response = cdm.get(ticket_path)
    print("ticket_user_body ", ticket_user_response)

    print("\n4. parsing constraints link")
    uri = ticket_user_response["links"][1].get("href")
    print("uri: %s" % uri)
    print("5. requesting constraints")
    ticket_user_response = cdm.get(uri, None)

    print("\n6. getting constraints related to the scan media interfaces")

    for x in ticket_user_response["validators"]:
        if x["propertyPointer"] == "src/scan/mediaSize":
            print("src/scan/mediaSize")
            print("Number of mediaSize :", len(x.get("options")))
            if x.get("options") == None:
                print("x.get() is ", x.get("options"))
            else:
                for y in x.get("options"):
                    print(y)
            print("")
        elif x["propertyPointer"] == "src/scan/mediaType":
            print("src/scan/mediaType")
            print("Number of mediaType :", len(x.get("options")))
            if x.get("options") == None:
                print("x.get() is ", x.get("options"))
            else:
                for y in x.get("options"):
                    print(y)
            print("")
        elif x["propertyPointer"] == "src/scan/mediaSource":
            print("src/scan/mediaSource")
            print("Number of mediaSource :", len(x.get("options")))
            if x.get("options") == None:
                print("x.get() is ", x.get("options"))
            else:
                for y in x.get("options"):
                    print(y)
            print("")
        elif x["propertyPointer"] == "src/scan/resolution":
            print("src/scan/resolution")
            print("Number of resolution :", len(x.get("options")))
            for y in x.get("options"):
                print(y)
            print("")
        elif x["propertyPointer"] == "src/scan/colorMode":
            print("src/scan/colorMode")
            print("Number of colorMode :", len(x.get("options")))
            if x.get("options") == None:
                print("x.get() is ", x.get("options"))
            else:
                for y in x.get("options"):
                    print(y)
            print("")
        elif x["propertyPointer"] == "src/scan/gamma":
            print("src/scan/gamma")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")
        elif x["propertyPointer"] == "src/scan/highlight":
            print("src/scan/highlight")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")
        elif x["propertyPointer"] == "src/scan/shadow":
            print("src/scan/shadow")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")
        elif x["propertyPointer"] == "src/scan/threshold":
            print("src/scan/threshold")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")
        elif x["propertyPointer"] == "pipelineOptions/imageModifications/exposure":
            print("pipelineOptions/imageModifications/exposure")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")
        elif x["propertyPointer"] == "pipelineOptions/imageModifications/contrast":
            print("pipelineOptions/imageModifications/contrast")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")
        elif x["propertyPointer"] == "pipelineOptions/imageModifications/sharpness":
            print("pipelineOptions/imageModifications/sharpness")
            print(x['min'])
            print(x['max'])
            print(x['step'], "\n")

    print("\ntest_copy_constraints_related_to_scanMedia_interface_cdm: END")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test out of bounds settings for copy ticket.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-46149
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_out_of_bounds_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_jobticket_out_of_bounds_constraints_cdm
        +guid:0cc3fcdf-1694-49b3-a9df-e5b8737cae32
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy &UIType=TouchScreen
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_jobticket_out_of_bounds_constraints_cdm(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    print("\test_copy_jobticket_out_of_bounds_constraints_cdm: BEGIN")

    print("1. creating a new ticket")
   
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    runningErrors = ""
    # Due to relaxed parsing, the following properties on this test are expected to pass with 200 ok after given a patch request with an unknown value, they have been removed from this test:
    # colorMode, mediaSource, mediaSize, resolution, contentType, contentOrientation, autoColorDetect, mediaType, ccdChannel, binaryRendering, scanCaptureMode, scanAcquisitionsSpeed

    ## src.scan stuff
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'colorRange': 101} } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'colorSensitivity': 101 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'compressionFactor': 101 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'gamma': 2001 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'highlight': 111 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'shadow': 101 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'threshold': 256 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'xOffset': 1001 } } })
    runningErrors += expect_patch_failure(cdm,ticket_path, {'src':{'scan':{'yOffset': 1001 } } })

    ## pipelineOptions stuff
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions':{'imageModifications' :{'backgroundCleanup': 101 }}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions':{'imageModifications':{'contrast': 2001} }})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions':{'imageModifications':{'exposure': 11}  } })
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions':{'imageModifications':{'sharpness': 11} } })
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions':{'scaling':{'xScalePercent': 401} } })
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions':{'scaling':{'yScalePercent': 401} } })

    # dest.print stuff
    runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'copies': 20000}}})
    # these are no longer expected to fail (relaxed parsing requirement)
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'collate': 'collated_bad'}}} )
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'mediaSize': 'na_legal_8.5x14in_bad'}}} )
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'mediaSource': 'tray-1_bad'}}} )
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'mediaSource': 'tray-13'}}} )
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'duplexBinding': 'twoSidedLongEdge_bad'}}} )
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'plexMode': 'simplex_bad'}}} )
    # runningErrors += expect_patch_failure(cdm, ticket_path, {'dest': {'print': {'printQuality': 'draft_bad'}}} )
    # All the tests are done, check the errors
    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test valid ticket settings.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-46149
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_in_bounds_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_jobticket_in_bounds_constraints_cdm
        +guid:73d9fb33-ee7a-4376-aa91-dcb0614433f6
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy &UIType=TouchScreen & MediaInputInstalled=Tray1 & ADFMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_jobticket_in_bounds_constraints_cdm(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    runningErrors =""
    # set in boounds
    # src.scan stuff
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'autoColorDetect': 'detectOnly' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'binaryRendering': 'halftone' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'ccdChannel': 'ntsc' }}})
    if cdm.device_feature_cdm.is_color_supported():        
        runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'colorMode': 'color' }}})
    else:
        runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'colorMode': 'grayscale' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'colorRange': 99 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'colorSensitivity': 99 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'compressionFactor': 1 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'contentOrientation': 'portrait' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'contentType': 'text' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'gamma': 29 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'highlight': 9 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'mediaSize': 'na_letter_8.5x11in' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'mediaSource': 'adf' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'mediaType': 'whitePaper' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'pageBinding': 'oneSided' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'plexMode': 'simplex' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'resolution': 'e75Dpi' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'scanAcquisitionsSpeed': 'slow' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'scanCaptureMode': 'standard' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'shadow': 99 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'threshold': 99 }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'xOffset': 50 }}} )
    runningErrors += expect_patch_success(cdm, ticket_path, {'src':{'scan':{'yOffset': 50 }}} )
    # pipelineOptions stuff
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'imageModifications' :{'backgroundCleanup': 2 }}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'imageModifications' :{'contrast': 6 }}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'imageModifications' :{'exposure': 9 }}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'imageModifications' :{'pagesPerSheet': 'oneUp'}}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'imageModifications' :{'sharpness': 5}}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'manualUserOperations' :{'imagePreviewConfiguration': 'optional'}}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'scaling':{ 'xScalePercent': 399 }}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'pipelineOptions':{'scaling':{ 'yScalePercent': 399 }}})

    # dest.print stuff
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'copies': 2}}})
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'mediaSource': 'tray-1'}}} )
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'printQuality': 'draft'}}} )
    # Why don't these pass???
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'collate': 'collated'}}} )
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'mediaSize': 'na_legal_8.5x14in'}}} )
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'mediaType': 'stationery-letterhead'}}} )
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'duplexBinding': 'twoSidedLongEdge'}}} )
    runningErrors += expect_patch_success(cdm,ticket_path, {'dest': {'print': {'plexMode': 'simplex'}}} )
    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test valid ticket settings.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-46149
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_related_usb_jobticket_in_bounds_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Negative
    +test:
        +title: test_copy_related_usb_jobticket_in_bounds_constraints_cdm
        +guid:7c654f4d-f2a0-4020-8b35-84882050e8b8
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy &UIType=TouchScreen & ScannerInput=AutomaticDocumentFeeder & MediaInputInstalled=Tray1 & ADFMediaSize=Letter
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_related_usb_jobticket_in_bounds_constraints_cdm(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    print("1. creating a new ticket")
   
    source = "scan"
    dest = "usb"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    runningErrors =""
    # set in boounds
    # src.scan stuff
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'colorMode': 'color' } } })
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'adf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSize': 'na_letter_8.5x11in'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'xOffset': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'yOffset': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'plexMode': 'simplex'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'resolution': 'e300Dpi'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'contentType': 'mixed'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'contentOrientation': 'portrait'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'pagesFlipUpEnabled': 'false'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'autoColorDetect': 'detectOnly'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'blackBackground': 'false'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaType': 'whitePaper'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'autoExposure': 'false'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'gamma': 100}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'highlight': 5}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'colorSensitivity': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'colorRange': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'ccdChannel': 'grayCcdEmulated'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'binaryRendering': 'halftone'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'descreen': 'false'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'feederPickStop': 'false'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'shadow': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'compressionFactor': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'threshold': 0}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'scanCaptureMode': 'standard'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'scanAcquisitionsSpeed': 'auto'}}})
    # pipelineOptions
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'sharpness': 1}}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'backgroundCleanup': 2}}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'exposure': 5}}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'contrast': 1}}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'blankPageSuppressionEnabled': 'false'}}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'pagesPerSheet': 'oneUp'}}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'manualUserOperations': {  'imagePreviewConfiguration': 'disable' }}})
    runningErrors += expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'manualUserOperations': {  'autoRelease': 'false' }}})

    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test invalid ticket settings.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-46149
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_related_usb_jobticket_out_of_bounds_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Negative
    +test:
        +title: test_copy_related_usb_jobticket_out_of_bounds_constraints_cdm
        +guid:23eab41d-e13a-44ae-bd1f-1f4d88357027
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & ScanDestination=USB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_related_usb_jobticket_out_of_bounds_constraints_cdm(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    print("1. creating a new ticket")
   
    source = "scan"
    dest = "usb"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    runningErrors =""
    # set in boounds
    # src.scan stuff

    # Due to relaxed parsing, the following properties on this test are expected to pass with 200 ok after given a patch request with an unknown value, they have been removed from this test:
    # colorMode, mediaSource, mediaSize, resolution, contentType, contentOrientation, autoColorDetect, mediaType, ccdChannel, binaryRendering, scanCaptureMode, scanAcquisitionsSpeed

    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'xOffset': 22222}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'yOffset': 22222}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'plexMode': 'simplex_'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'pagesFlipUpEnabled': 'false_'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'blackBackground': 'false--'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'autoExposure': 'false--'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'gamma': 2001}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'highlight': 101}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'colorSensitivity': 20000}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'colorRange': 200000}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'descreen': 'false--'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'feederPickStop': 'false--'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'shadow': 101}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'compressionFactor': 20000}}})
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'threshold': 20000}}})
    # pipelineOptions
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'sharpness': 11}}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'backgroundCleanup': 2555555}}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'exposure': 50000}}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'contrast': 155555}}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'blankPageSuppressionEnabled': 'false---'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': { 'imageModifications': {   'pagesPerSheet': 'oneUp_'}}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': {'manualUserOperations': {  'imagePreviewConfiguration': 'disable_' }}})
    runningErrors += expect_patch_failure(cdm, ticket_path, {'pipelineOptions': {'manualUserOperations': {  'autoRelease': 'false--' }}})

    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test default copy ticket is valid.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-70609
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_default_ticket_is_valid
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_default_ticket_is_valid
        +guid: 0691ff96-0401-48e8-aae8-6d4b829bff62
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_default_ticket_is_valid(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    # The goal of this test is to ensure that the default copy ticket values are in harmony with the default copy constraints
    # Thoretically this test should pass against any copy device.
    # But some products are not yet awesome enough to pass this simple test (24 Feb 2022); but we want to make sure
    # Selene can pass this one.
    
    constraints_json = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    scan_input_source = find_constraint(constraints_json, "src/scan/mediaSource")
    adf_entry = find_validator_option(scan_input_source, "adf")
    if adf_entry == None or ( 'disabled' in adf_entry and adf_entry['disabled'] == "true") :
        print("This is only supposed to run on devices that have an ADF; go no further ")
        return

    print("step 1. Get the default copy ticket")
    ticket_response = cdm.get(cdm.JOB_TICKET_COPY, None)
    print("ticket_user_body ", ticket_response)
    jsonBody = ticket_response
    print("step 2. Patch the default copy ticket with the default values")
    ticket_response = cdm.patch_raw(cdm.JOB_TICKET_COPY, jsonBody)
    print("ticket_response: ", ticket_response)
    print("step 3. verify it was a success")
    assert ticket_response.status_code < 300
    print("step 4. you're awesome")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy scaling is disabled when 2PagesPerSheet enabled.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_scaling_disabled_with_2PagesPerSheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_scaling_disabled_with_2PagesPerSheet
        +guid: d793415b-35dc-406c-901f-5fdf8cda5ef5
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & Copy=2PagesPerSheet
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_scaling_disabled_with_2PagesPerSheet(cdm, udw, net, configuration):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    # The goal of this test is to ensure that the default copy ticket values are in harmony with the default copy constraints
    # Thoretically this test should pass against any copy device.
    # But some products are not yet awesome enough to pass this simple test (24 Feb 2022); but we want to make sure
    # Selene can pass this one.

    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    runningErrors = ""
    print("step 1: ensure 2PagesPerSheet Disabled")
    runningErrors += expect_patch_success(cdm, ticket_path, { "pipelineOptions":{"imageModifications":{"pagesPerSheet": "oneUp"}}})

    print("step 2: get constraints")
    constraints_json = cdm.get(constraints_url)
    print("constraints_json" , constraints_json)

    print("step 3: find scale constraints")
    x_scale_percent = find_constraint(constraints_json, "pipelineOptions/scaling/xScalePercent")
    y_scale_percent = find_constraint(constraints_json, "pipelineOptions/scaling/yScalePercent")
    scale_selection = find_constraint(constraints_json, "pipelineOptions/scaling/scaleSelection")
    scale_to_size = find_constraint(constraints_json, "pipelineOptions/scaling/scaleToSize")
    scale_to_output = find_constraint(constraints_json, "pipelineOptions/scaling/scaleToOutput")

    print("x_scale_percent" , x_scale_percent)

    assert ("disabled" not in x_scale_percent)
    assert ("disabled" not in y_scale_percent)
    assert ("disabled" not in scale_selection)
    assert ("disabled" not in scale_to_size)
    assert ("disabled" not in scale_to_output)

    print("step 4: repeat with 2PagesPerSheet enabled")
    runningErrors += expect_patch_success(cdm, ticket_path, { "pipelineOptions":{"imageModifications":{"pagesPerSheet": "twoUp"}}})

    constraints_json = cdm.get(constraints_url)
    print("constraints_json" , constraints_json)

    x_scale_percent = find_constraint(constraints_json, "pipelineOptions/scaling/xScalePercent")
    y_scale_percent = find_constraint(constraints_json, "pipelineOptions/scaling/yScalePercent")
    scale_selection = find_constraint(constraints_json, "pipelineOptions/scaling/scaleSelection")
    scale_to_size = find_constraint(constraints_json, "pipelineOptions/scaling/scaleToSize")
    scale_to_output = find_constraint(constraints_json, "pipelineOptions/scaling/scaleToOutput")
    print("x_scale_percent" , x_scale_percent)

    # Constraint BehaVIOUR IS DIFFERENT BETWEEN eNTERPRISE AND NON-ENTERPRISE
    if configuration.familyname == 'enterprise':
        assert ("disabled" not in x_scale_percent)
        assert ("disabled" not in y_scale_percent)
        assert ("disabled" in scale_selection['options'][2])
        assert ("disabled" not in scale_to_size)
        assert ("disabled" in scale_to_output['options'][0])
    else:
        assert ("disabled" in x_scale_percent)
        assert ("disabled" in y_scale_percent)
        assert ("disabled" in scale_selection)
        assert ("disabled" in scale_to_size)
        assert ("disabled" in scale_to_output)

    cdm.delete_raw(ticket_path)

def verify_scan_paper_sizes(cdm,source, dest):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note,This test is to check a special case.
    # Since the key of the code is different from the one stored in the cdm.
    # This occurs because the value of cdm is a c++ reserved word.

    print("1. creating a new ticket src: {} dest: {}".format(source, dest))
    
    #source = "scan"
    #dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    ticket_constraints_path = ticket_path + "/constraints"

    runningErrors = ""
    # check with adf first
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'adf'}}})
    constraints_json = cdm.get(ticket_constraints_path)
    paperSizes = find_constraint(constraints_json, "src/scan/mediaSize")
    print(" paper sizes:")
    print(paperSizes)
    expectedOptions = [
        "na_letter_8.5x11in",
        "na_legal_8.5x14in",
        "na_executive_7.25x10.5in",
        "na_foolscap_8.5x13in",
        "na_index-5x8_5x8in",
        "iso_a4_210x297mm",
        "iso_a5_148x210mm",
        "jis_b5_182x257mm",
        "jis_b6_128x182mm",
        "na_oficio_8.5x13.4in",
        "om_16k_195x270mm",
        "om_16k_184x260mm",
        "roc_16k_7.75x10.75in",
        "jpn_oufuku_148x200mm",
        "na_invoice_5.5x8.5in"
    ]
    foundOption = {}
    for paperSize in expectedOptions:
        foundOption  = find_validator_option(paperSizes, paperSize)
        if foundOption == None:
            runningErrors += "(adf) Could not find paper size: " + paperSize +"\n"

    # Now switch to flatbed and check they are correct too.
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'flatbed'}}})
    constraints_json = cdm.get(ticket_constraints_path)
    paperSizes = find_constraint(constraints_json, "src/scan/mediaSize")
    print(" paper sizes:")
    print(paperSizes)

    expectedOptions = [
        "any",
        "na_letter_8.5x11in",
        "na_executive_7.25x10.5in",
        "na_index-4x6_4x6in",
        "na_index-5x8_5x8in",
        "iso_a4_210x297mm",
        "iso_a5_148x210mm",
        "iso_a6_105x148mm",
        "jis_b5_182x257mm",
        "jis_b6_128x182mm",
        "om_small-photo_100x150mm",
        "na_oficio_8.5x13.4in",
        "om_16k_195x270mm",
        "om_16k_184x260mm",
        "roc_16k_7.75x10.75in",
        "jpn_hagaki_100x148mm",
        "jpn_oufuku_148x200mm",
        "na_number-10_4.125x9.5in",
        "na_monarch_3.875x7.5in",
        "iso_b5_176x250mm",
        "iso_c5_162x229mm",
        "iso_dl_110x220mm",
        "na_invoice_5.5x8.5in"
    ]
    for paperSize in expectedOptions:
        foundOption  = find_validator_option(paperSizes, paperSize)
        if foundOption == None:
            runningErrors += "(flatbed) Could not find paper size: " + paperSize +"\n"

    print("verify_scan_paper_sizes, dest= "+ dest + " runningErrors:\n" +runningErrors)
    return runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test invalid ticket settings.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73472
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_related_input_media_constraints_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_related_input_media_constraints_cdm
        +guid:6da4133c-27c6-4ba6-9433-8a3031cd9e0e
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & Copy=GrayScale  & ADFMediaSize=JapanesePostcard & FlatbedMediaSize=10x15cm & FlatbedMediaSize=EnvelopeDL
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_related_input_media_constraints_cdm(cdm, udw, net):

    runningErrors = verify_scan_paper_sizes(cdm, "scan", "print")
    assert runningErrors == ""

    runningErrors = verify_scan_paper_sizes(cdm, "scan", "email")
    assert runningErrors == ""

    runningErrors = verify_scan_paper_sizes(cdm, "scan", "usb")
    assert runningErrors == ""

    runningErrors = verify_scan_paper_sizes(cdm, "scan", "folder")
    assert runningErrors == ""

    runningErrors = verify_scan_paper_sizes(cdm, "scan", "sharePoint")
    assert runningErrors == ""

    runningErrors = verify_scan_paper_sizes(cdm, "scan", "print")
    assert runningErrors == ""

    # TODO: File bug with Fax; Fax needs to hookup 'scannerMedia_' and 'scannerCapabilities_'
    #runningErrors = verify_scan_paper_sizes(cdm, "scan", "fax")
    #assert runningErrors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy constraints re-gen.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-77525
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_relaxed_parsing
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_relaxed_parsing
        +guid: b6c3cfa1-12a3-4f0a-980b-9e67f024e415
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_relaxed_parsing(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    # The goal of this test is to ensure that the default copy ticket values are in harmony with the default copy constraints
    # Thoretically this test should pass against any copy device.
    # But some products are not yet awesome enough to pass this simple test (24 Feb 2022); but we want to make sure
    # Selene can pass this one.
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    runningErrors =""
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'colorMode': 'color_asdfasdf' } } })
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'adf_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSize': 'na_letter_8.5x11in_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'resolution': 'e300Dpi_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'contentType': 'mixed_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'contentOrientation': 'portrait_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'autoColorDetect': 'detectOnly_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaType': 'whitePaper_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'ccdChannel': 'grayCcdEmulated_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'binaryRendering': 'halftone_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'scanCaptureMode': 'standard_asdfasdf'}}})
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'scanAcquisitionsSpeed': 'auto_asdfasdf'}}})

    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy constraints force sets.
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-77525
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_force_sets
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_force_sets
        +guid: a5f6dcba-fe7a-4f73-a13d-6079f327bcf3
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_force_sets(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    #1. [DUNE-66540] Copy force set "dest.print.quality -> best => scan.resolution -> 600 dpi."
    runningErrors =""
    runningErrors += expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSource': 'adf'}}} )
    ticket_user_body = cdm.get(ticket_path)

    assert ticket_user_body['src']['scan']['mediaSource']  == 'adf'
    assert ticket_user_body['src']['scan']['resolution']   == 'e300Dpi'
    runningErrors += expect_patch_success(cdm, ticket_path, {'dest': {'print': {'printQuality': 'best'}}} )
    ticket_user_body = cdm.get(ticket_path)

    assert ticket_user_body['src']['scan']['resolution']  == 'e300Dpi'
    runningErrors += expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSource': 'flatbed'}}} )
    ticket_user_body = cdm.get(ticket_path)

    assert ticket_user_body['src']['scan']['resolution']  == 'e600Dpi'
    runningErrors += expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSource': 'adf'}}} )
    ticket_user_body = cdm.get(ticket_path)

    assert ticket_user_body['src']['scan']['resolution']  == 'e300Dpi'

    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy constraints regen.
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-77525
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_regen
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_regen
        +guid: e8645f57-e38e-4455-b7ac-c959fa7cbc71
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & ScannerInput=Flatbed & ScannerInput=AutomaticDocumentFeeder & Copy=Quality & Copy=GrayScale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_regen(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    # The goal of this test is to ensure that the default copy ticket values are in harmony with the default copy constraints
    # Thoretically this test should pass against any copy device.
    # But some products are not yet awesome enough to pass this simple test (24 Feb 2022); but we want to make sure
    # Selene can pass this one.
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    runningErrors =""
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'adf'} } })  # start with adf
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'flatbed', 'resolution': 'e600Dpi'} } })
    runningErrors += expect_patch_failure(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'adf', 'resolution': 'e600Dpi'} } })
    runningErrors += expect_patch_success(cdm, ticket_path,  { 'src' :{ 'scan':{ 'mediaSource': 'adf'} } })  # start with adf

    print("runningErrors: '\n" + runningErrors + "'")
    assert "" == runningErrors

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy constraints addToContents ('dest/print/printMargins' property)
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-86443
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_addToContents
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_addToContents
        +guid: ed4abcf7-a5b3-4db2-8a8f-fea0ede35de4
        +dut:
            +type: Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & UIType=TouchScreen & CopyPrintMargins=AddToContents
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_addToContents(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    constraints_json = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    copy_margins_option = find_constraint(constraints_json, "dest/print/printMargins")
    addToContents_entry = find_validator_option(copy_margins_option, "addToContents")
    my_errors = ""
    if addToContents_entry == None or ( 'disabled' in addToContents_entry and addToContents_entry['disabled'] == "true") :
        my_errors = "Error, Expected to have an enabled printMargins constraint of 'addToContents'"

    assert my_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy constraints compressionFactor
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-85193
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_compressionFactor
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_compressionFactor
        +guid: d61e3187-5d45-4b24-926c-f9aa2f60a499
        +dut:
            +type: Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & UIType=TouchScreen
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_compressionFactor(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    constraints_json = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    copy_margins_option = find_constraint(constraints_json, "src/scan/compressionFactor")
    #print(copy_margins_option)
    my_errors = ""
    if copy_margins_option['min']['value'] != 0 or copy_margins_option['max']['value'] != 100 or copy_margins_option['step']['value'] != 1:
        my_errors = "Error 'compressionFactor' expected to have constraint min:0, max:10, step:1"

    assert my_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy constraints no copy margins property
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-77525
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_no_margins_property
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_no_margins_property
        +guid:ecbeafe8-45eb-4799-8635-2592b2e4d552
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & Copy=BindingMargin & Copy=ImagePreview & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_no_margins_property(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    printTable = ticket_user_body['dest']['print']
    #print(printTable)
    # testing the 'supportsProperty()' functinality on the TicketAdapter.
    assert ( ('printMargins' in printTable) == False )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy constraints has copy margins property LFP
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-77525
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_has_margins_property_lfp
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_has_margins_property_lfp
        +guid: a3f91f0b-f444-46f9-be17-026df6e271ef
        +dut:
            +type: Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & UIType=TouchScreen
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_has_margins_property_lfp(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    printTable = ticket_user_body['dest']['print']
    #print(printTable)
    assert ( ('printMargins' in printTable) == True )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy 2PagesPerSheet is disabled when scaleSelection is active.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_pages_per_sheet_disabled_with_scaleSelection
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_pages_per_sheet_disabled_with_scaleSelection
        +guid: a986a10b-f011-4200-887c-4e4f6df44179
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & Copy=2PagesPerSheet
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_pages_per_sheet_disabled_with_scaleSelection(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata

    #"pipelineOptions/imageModifications/pagesPerSheet"
    #"pipelineOptions/scaling/scaleSelection"

    print("1. creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"

    print("step 1: set scaleSelection to none")
    cdm.patch_raw(url,  { "pipelineOptions":{"scaling":{"scaleSelection": "none"}}})

    print("step 2: get constraints")
    constraints_json = cdm.get(constraints_url)
    print("constraints_json" , constraints_json)

    print("step 3: find pagesPerSheet constraints")
    pages_per_sheet = find_constraint(constraints_json, "pipelineOptions/imageModifications/pagesPerSheet")

    print("pages_per_sheet" , pages_per_sheet)

    disabled_options = []
    disabled_options.append(find_validator_option(pages_per_sheet, "twoUp"))

    assert  is_enabled(disabled_options,"twoUp")

    print("step 4: repeat with scaleSelecting = fitToPage")
    cdm.patch_raw(url,  { "pipelineOptions":{"scaling":{"scaleSelection": "fitToPage"}}})

    constraints_json = cdm.get(constraints_url)
    print("constraints_json" , constraints_json)

    pages_per_sheet = find_constraint(constraints_json, "pipelineOptions/imageModifications/pagesPerSheet")

    print("pages_per_sheet" , pages_per_sheet)

    disabled_options = []
    disabled_options.append(find_validator_option(pages_per_sheet, "twoUp"))

    assert  is_enabled(disabled_options,"twoUp")
    cdm.delete(ticket_path)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test constraints disable duplex when non-duplex paper types are selected
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_collate_pages_per_sheet_disables_stuff
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_collate_pages_per_sheet_disables_stuff
        +guid: 188f4602-cffd-4f3e-9434-6f76da7b36a5
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & PrintEngineFormat=A4 & Copy=Quality & Copy=2PagesPerSheet
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_collate_pages_per_sheet_disables_stuff(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    running_errors = ""
    print("1. creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    # pipelineOptions/imageModifications/pagesPerSheet
    print("2. patch pipelineOptions/imageModifications/pagesPerSheet = twoUp")
    response = cdm.patch_raw(ticket_path, { "pipelineOptions": {"imageModifications": {"pagesPerSheet": "twoUp" }}} )
    assert response.status_code == 200

    these_should_be_disabled = [
        "pipelineOptions/scaling/scaleSelection",
        "pipelineOptions/scaling/scaleToOutput",
        "pipelineOptions/scaling/scaleToSize",
        "pipelineOptions/scaling/xScalePercent",
        "pipelineOptions/scaling/yScalePercent"
    ]

    ticket_response = cdm.get(ticket_path)
    if (ticket_response['dest']['print']['collate'] == "uncollated" ) :
        print( "collate is disabled, that's good :)" )
    else:
        running_errors += "collate should have been disabled with 2up\n"

    constraints_json = cdm.get(constraints_url)
    for property in these_should_be_disabled:
        my_constraints = find_constraint(constraints_json, property)
        #option = find_validator_option(my_constraints, "duplex")
        if ( 'disabled' in my_constraints and my_constraints['disabled']['value'] == "true") :
            print( "{0}:  is disabled by 'pagesPerSheet=2up', that's good :)".format(property))
        else:
            running_errors += " 'pagesPerSheet=2up' should have been disabled {0}\n".format(property )

    cdm.delete(ticket_path)
    assert running_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test constraints disable non-duplex paper types with duplex output
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_non_duplex_paper_types_disabled_with_duplex
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_non_duplex_paper_types_disabled_with_duplex
        +guid: c9e179b5-4163-4a68-b988-fbe1d53e63e3
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_non_duplex_paper_types_disabled_with_duplex(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    running_errors = ""
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    print("2. patch dest/print/plexMode = duplex")
    cdm.patch_raw(ticket_path, { "dest": {"print": {"plexMode":"duplex"}}} )
    constraints_json = cdm.get(constraints_url)
    media_types = find_constraint(constraints_json, "dest/print/mediaType")
    non_duplex_paper_types = ["transparency", "labels", "envelope"]
    for paper_type in non_duplex_paper_types:
        option = find_validator_option(media_types, paper_type)
        if option != None  :
            if ( 'disabled' in option and option['disabled'] == "true") :
                print( paper_type + " is disabled, that's good")
            else:
                running_errors += "{0} should have been disabled\n".format(paper_type)
    cdm.delete(ticket_path)
    assert running_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test constraints disable non-duplex paper sizes with duplex output
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_non_duplex_paper_sizes_disabled_with_duplex
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_non_duplex_paper_sizes_disabled_with_duplex
        +guid: 7c8ba4f7-e523-43af-a415-4baa976b61ce
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_non_duplex_paper_sizes_disabled_with_duplex(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    running_errors = ""
    print("1. creating a new ticket")
  
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    print("2. patch dest/print/plexMode = duplex")
    cdm.patch_raw(ticket_path, { "dest": {"print": {"plexMode":"duplex"}}} )
    constraints_json = cdm.get(constraints_url)
    media_sizes = find_constraint(constraints_json, "dest/print/mediaSize")
    non_duplex_paper_sizes = [ # initially filled out for selene, may need to adjust later
        "na_index-4x6_4x6in",
        "jis_b6_128x182mm",
        "na_index-5x8_5x8in",
        "iso_a6_105x148mm",
    ]
    for paper_size in non_duplex_paper_sizes:
        option = find_validator_option(media_sizes, paper_size)
        if option != None:
            if ( 'disabled' in option and option['disabled'] == "true") :
                print( paper_size + " is disabled, that's good")
            else:
                running_errors += "{0} should have been disabled with duplex\n".format(paper_size)

    cdm.delete(ticket_path)
    assert running_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test constraints disable duplex when non-duplex paper sizes are selected
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_duplex_disabled_with_non_duplex_paper_sizes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_duplex_disabled_with_non_duplex_paper_sizes
        +guid: e58b4844-4c76-488b-b2d9-123682a5287c
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & Duplexer=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_duplex_disabled_with_non_duplex_paper_sizes(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    running_errors = ""
    print("1. creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    print("2. patch dest/print/plexMode = duplex")
    # initially filled out for selene, we may need to adjust later (we don't want to make system tests product-specific)
    non_duplex_paper_sizes = [
        "na_index-4x6_4x6in",
        "jis_b6_128x182mm",
        "na_index-5x8_5x8in",
        "iso_a6_105x148mm",
    ]
    for paper_size in non_duplex_paper_sizes:
        cdm.patch_raw(ticket_path, { "dest": {"print": {"mediaSize": paper_size }}} )
        constraints_json = cdm.get(constraints_url)
        plex_constraints = find_constraint(constraints_json, "dest/print/plexMode")
        option = find_validator_option(plex_constraints, "duplex")
        if ( 'disabled' in option and option['disabled'] == "true") :
            print( "with {0}: duplex is disabled, that's good :)".format(paper_size))
        else:
            running_errors += "duplex should have been disabled with size: {0}\n".format(paper_size)

    cdm.delete(ticket_path)
    assert running_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test constraints disable duplex when non-duplex paper types are selected
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_constraints_duplex_disabled_with_non_duplex_paper_types
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_duplex_disabled_with_non_duplex_paper_types
        +guid: aefbfdb5-3a4b-4eaa-a60b-7d8c117f71ae
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & MediaType=Transparency & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_duplex_disabled_with_non_duplex_paper_types(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    running_errors = ""
    print("1. creating a new ticket")

    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    print("2. patch dest/print/plexMode = duplex")
    # initially filled out for selene, we may need to adjust later (we don't want to make system tests product-specific)
    non_duplex_paper_types = ["transparency", "labels", "envelope"]
    for paper_size in non_duplex_paper_types:
        cdm.patch_raw(ticket_path, { "dest": {"print": {"mediaType": paper_size }}} )
        constraints_json = cdm.get(constraints_url)
        plex_constraints = find_constraint(constraints_json, "dest/print/plexMode")
        option = find_validator_option(plex_constraints, "duplex")
        if ( 'disabled' in option and option['disabled'] == "true") :
            print( "with {0}: duplex is disabled, that's good :)".format(paper_size))
        else:
            running_errors += "duplex should have been disabled with size: {0}\n".format(paper_size )

    cdm.delete(ticket_path)
    assert running_errors == ""


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test media source constraints
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_media_source_constraints
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_media_source_constraints
        +guid: f9abf6bb-31e3-4257-a7ac-a5df787a7bb4
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIType=TouchScreen & ScannerInput=AutomaticDocumentFeeder 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_media_source_constraints(cdm, udw, net):
    # Note, 'cdm' defined in test/dunetuf/dunetuf cdm__init__.py
    # Note, Metadata definitions are located on page:   https://dune-btf-ui.boi.rd.hpicorp.net/#/Metadata
    running_errors = ""
    print("1. creating a new ticket")
  
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    constraints_json = cdm.get(constraints_url)
    mediaSource_constraints_1 = find_constraint(constraints_json, "dest/print/mediaSource")
    print("Set mediaSize to something not supported in all trays")
    cdm.patch_raw(ticket_path, { "dest": {"print": {"mediaSize": "na_number-10_4.125x9.5in" }}} )
    constraints_json = cdm.get(constraints_url)
    mediaSource_constraints_2 = find_constraint(constraints_json, "dest/print/mediaSource")
    print(mediaSource_constraints_1)
    print(mediaSource_constraints_2)
    cdm.delete(ticket_path) # Cleanup object

    disabled_items_count_1 = count_disabled_options(mediaSource_constraints_1['options'])
    disabled_items_count_2 = count_disabled_options(mediaSource_constraints_2['options'])
    print("disabled_items_count_1: " + str(disabled_items_count_1))
    print("disabled_items_count_2: " + str(disabled_items_count_2))
    #ensure that there are some disabled items for 'mediaSource_constraints_2' now
    if (singleMediaSourceDevice(mediaSource_constraints_1['options'])):
        assert ( disabled_items_count_1 <= disabled_items_count_2 )
    else:
        assert ( disabled_items_count_1 < disabled_items_count_2 )


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test media size / output plex relationship
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-73524
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_media_size_and_plex
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_media_size_and_plex
        +guid: 53418c30-36b3-4e7b-b2a4-2c128a8e8a2c
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_media_size_and_plex(cdm, udw, net):
    running_errors = ""
    print("1. creating a new ticket")

    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"
    constraints_json = cdm.get(constraints_url)
    media_sizes = find_constraint(constraints_json, "dest/print/mediaSize")
    a6_option = find_validator_option(media_sizes, "iso_a6_105x148mm")

    if a6_option != None :
        if ( 'disabled' in a6_option and a6_option['disabled'] == "true") :
            print("a6 option:")
            print(a6_option)
            print("a6 is not enabled by default, test case doesn't fit this product")
            cdm.delete(ticket_path) #cleanup ticket
            return  ###### Bail out of test case; it doesn't make sense for the current product

        # Set to a duplex, to a duplex-able media size
        result = cdm.patch_raw(ticket_path, { "dest": { "print": { "mediaSize": "na_letter_8.5x11in", "plexMode": "duplex" } } })
        assert result.status_code  < 300

        result = cdm.patch_raw(ticket_path, { "dest": { "print": { "mediaSize": "iso_a6_105x148mm", "plexMode": "simplex" } } })
        assert result.status_code  < 300
        # success, we just proved that
        print("test_copy_media_size_and_plex = success ")
    else:
        print("A6 mediaSize is not available, so we don't care to run anything here")
    cdm.delete(ticket_path) #cleanup ticket

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy pagesPerSheet is disabled when originalSize Mixed is active
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-106570
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name: test_copy_constraints_pages_per_sheet_disabled_with_originalSize_mixed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_constraints_pages_per_sheet_disabled_with_originalSize_mixed
        +guid:ab647d46-e0ba-430c-97a6-7a2168df8199
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedA4A3 & Copy=2PagesPerSheet
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_pages_per_sheet_disabled_with_originalSize_mixed(cdm):

    #"pipelineOptions/imageModifications/pagesPerSheet"
    #"src/scan/mediaSize"
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"

    print("3. patch src/scan/mediaSize = any")
    available_options = []
    disabled_options = []
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSize': "any"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/pagesPerSheet")
    available_options.append(find_validator_option(current_constraints, "oneUp"))
    available_options.append(find_validator_option(current_constraints, "twoUp"))
    assert is_enabled(available_options, "oneUp")
    assert is_enabled(available_options, "twoUp")

    print("4. patch src/scan/mediaSize = mixed-a4-a3")
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSize': "com.hp.ext.mediaSize.mixed-a4-a3"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/pagesPerSheet")
    available_options.append(find_validator_option(current_constraints, "oneUp"))
    disabled_options.append(find_validator_option(current_constraints, "twoUp"))
    assert is_enabled(available_options, "oneUp")
    assert is_disabled(disabled_options, "twoUp")

    print("5. patch src/scan/mediaSize = mixed-letter-legal")
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSize': "com.hp.ext.mediaSize.mixed-letter-legal"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/pagesPerSheet")
    available_options.append(find_validator_option(current_constraints, "oneUp"))
    disabled_options.append(find_validator_option(current_constraints, "twoUp"))
    assert is_enabled(available_options, "oneUp")
    assert is_disabled(disabled_options, "twoUp")

    print("6. patch src/scan/mediaSize = mixed-letter-ledger")
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaSize': "com.hp.ext.mediaSize.mixed-letter-ledger"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/pagesPerSheet")
    available_options.append(find_validator_option(current_constraints, "oneUp"))
    disabled_options.append(find_validator_option(current_constraints, "twoUp"))
    assert is_enabled(available_options, "oneUp")
    assert is_disabled(disabled_options, "twoUp")

    cdm.delete(ticket_path)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy page sources is disabled when originalSize Mixed is active
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-106570
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_constraints_pages_per_sheet_disables_with_paperSource
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_constraints_pages_per_sheet_disables_with_paperSource
        +guid:8d2660f2-a978-430a-813a-5af8118b067a
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_pages_per_sheet_disables_with_paperSource(cdm):

    running_errors = ""
    print("1. creating a new ticket")
 
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"

    print("3. patch src/scan/mediaSize = mixed-a4-a3")
    cdm.patch_raw(ticket_path, { "src": {"scan": {"mediaSize":"com.hp.ext.mediaSize.mixed-a4-a3"}}} )
    constraints_json = cdm.get(constraints_url)
    media_sources = find_constraint(constraints_json, "dest/print/mediaSource")
    list_paper_sources = ["tray-1", "tray-2", "tray-3"]
    for paper_source in list_paper_sources:
        option = find_validator_option(media_sources, paper_source)
        if option != None  :
            if ( 'disabled' in option and option['disabled'] == "true") :
                print( paper_source + " is disabled, that's good")
            else:
                running_errors += "{0} should have been disabled\n".format(paper_source)
    assert running_errors == ""

    print("4. patch src/scan/mediaSize = mixed-letter-legal")
    cdm.patch_raw(ticket_path, { "src": {"scan": {"mediaSize":"com.hp.ext.mediaSize.mixed-letter-legal"}}} )
    constraints_json = cdm.get(constraints_url)
    media_sources = find_constraint(constraints_json, "dest/print/mediaSource")
    list_paper_sources = ["tray-1", "tray-2", "tray-3"]
    for paper_source in list_paper_sources:
        option = find_validator_option(media_sources, paper_source)
        if option != None  :
            if ( 'disabled' in option and option['disabled'] == "true") :
                print( paper_source + " is disabled, that's good")
            else:
                running_errors += "{0} should have been disabled\n".format(paper_source)
    assert running_errors == ""

    print("5. patch src/scan/mediaSize = mixed-letter-ledger")
    cdm.patch_raw(ticket_path, { "src": {"scan": {"mediaSize":"com.hp.ext.mediaSize.mixed-letter-ledger"}}} )
    constraints_json = cdm.get(constraints_url)
    media_sources = find_constraint(constraints_json, "dest/print/mediaSource")
    list_paper_sources = ["tray-1", "tray-2", "tray-3"]
    for paper_source in list_paper_sources:
        option = find_validator_option(media_sources, paper_source)
        if option != None  :
            if ( 'disabled' in option and option['disabled'] == "true") :
                print( paper_source + " is disabled, that's good")
            else:
                running_errors += "{0} should have been disabled\n".format(paper_source)
    cdm.delete(ticket_path)
    assert running_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy original size is disabled when twoup is active
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-106570
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_constraints_original_size_disables_with_pages_per_sheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_constraints_original_size_disables_with_pages_per_sheet
        +guid:9ae37437-35ee-4ec3-96ee-2cbf77578ac7
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedA4A3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_constraints_original_size_disables_with_pages_per_sheet(cdm):

    running_errors = ""
    print("1. creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    constraints_url = ticket_path + "/constraints"

    print("3. patch pipelineOptions/imageModifications/pagesPerSheet = twoUp")
    cdm.patch_raw(ticket_path, { "pipelineOptions": {"imageModifications": {"pagesPerSheet": "twoUp" }}} )
    constraints_json = cdm.get(constraints_url)
    media_sources = find_constraint(constraints_json, "src/scan/mediaSize")
    list_paper_sources = [
        "com.hp.ext.mediaSize.mixed-a4-a3",
        "com.hp.ext.mediaSize.mixed-letter-legal",
        "com.hp.ext.mediaSize.mixed-letter-ledger"]
    for paper_source in list_paper_sources:
        option = find_validator_option(media_sources, paper_source)
        if option != None  :
            if ( 'disabled' in option and option['disabled'] == "true") :
                print( paper_source + " is disabled, that's good")
            else:
                running_errors += "{0} should have been disabled\n".format(paper_source)
    assert running_errors == ""

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_copy_cdm_job_contenttype_backgroundcolorremoval_dynamic_constraint
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-119844
    +timeout: 200
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_job_contenttype_backgroundcolorremoval_dynamic_constraint
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_job_contenttype_backgroundcolorremoval_dynamic_constraint
        +guid: 8bf33b95-6dce-45b2-aba8-3123436a5c2f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=BackgroundColorRemoval
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_job_contenttype_backgroundcolorremoval_dynamic_constraint(cdm):
   
    body = { 'src': {'scan':{}}, 'dest': {'print':{}} }
    rep = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert 200 <= rep.status_code < 300
    ticket_id = rep.json()['ticketId']

    bgr_path = 'pipelineOptions/imageModifications/backgroundColorRemoval'
    ct_path = 'src/scan/contentType'

    constraints = get_constraints(cdm, ticket_id)
    if bgr_path not in [x['propertyPointer'] for x in constraints]:
        pytest.skip('Skipping test: backgroundColorRemoval not supported')
    if 'image' not in enabled_options(constraints, ct_path):
        pytest.skip("Skipping test: ContentType doesn't support Image option")

    # Set Content Type to Mixed, Background Noise Removal to ON
    body = {'src': {'scan': {'contentType': 'mixed'}},
            'pipelineOptions': {'imageModifications': {'backgroundColorRemoval': 'true'}}}
    set_ticket(cdm, ticket_id, body)

    # Set Content Type to Image, and verify that Background Noise Removal is
    # constrained to only OFF
    set_ticket(cdm, ticket_id, {'src': {'scan': {'contentType': 'image'}}})
    constraints = get_constraints(cdm, ticket_id)
    # assert enabled_options(constraints, bgr_path) == ['false']
    # Also verify that the ticket has been overwritten accordingly
    ticket = get_ticket(cdm, ticket_id)
    assert ticket['pipelineOptions']['imageModifications']['backgroundColorRemoval'] == 'false'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy access constraints from multiple threads using cdm
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-240124
    +timeout:60
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_get_constraints_multi_threading
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_get_constraints_multi_threading
        +guid: 94f7c934-0655-11f0-9834-673a1061bd1c
        +dut:
            +type: Simulator
            +configuration:DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_get_constraints_multi_threading(cdm):
    urls = [cdm.JOB_TICKET_COPY_CONSTRAINTS for _ in range(40)]

    # Make the Pool with 10 thread workers
    pool = ThreadPool(10)
    # Connect get method with url map
    pool.map(cdm.get, urls)
    #close the pool and wait for the work to finish
    pool.close()
    pool.join()
