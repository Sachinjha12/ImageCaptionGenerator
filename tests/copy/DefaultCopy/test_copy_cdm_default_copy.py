import json
import pprint
import os
import time

TESTRESOURCEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')

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






def check_copy_job_ticket_expected_values(cdm, family, group):
    '''
    Perform GET operation on the cdm endpoint and get defaults values.

    Args:
        cdm: CDM fixture
        family: Target selene or designjet
        group: default product group
    '''
    
    # retrieving the default job ticket
    ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_default_response.status_code == 200

    # Get json
    ticket_default_body = ticket_default_response.json()
    
    default_dest_print_copies = ticket_default_body["dest"]["print"]["copies"] 
    default_src_scan_colorMode = ticket_default_body["src"]["scan"]["colorMode"]
    default_src_scan_resolution = ticket_default_body["src"]["scan"]["resolution"]

    # get default values from json
    with open(TESTRESOURCEPATH+'ticket_default_values_expected.json') as fileJson:
        data = json.load(fileJson)

    default_copies = data[family][group]["dest"]["print"]["copies"] 
    default_colorMode = data[family][group]["src"]["scan"]["colorMode"] 
    default_resolution = data[family][group]["src"]["scan"]["resolution"] 

    # check results
    assert default_dest_print_copies == default_copies
    assert default_src_scan_colorMode == default_colorMode
    assert default_src_scan_resolution == default_resolution    

    # Relative checks
    # Imaging settings

    if( ('pipelineOptions' in data[family][group]) and ('imageModifications' in data[family][group]['pipelineOptions']) ):
        default_image_modifications_ticket = ticket_default_body['pipelineOptions']['imageModifications']
        default_expected_image_modifications = data[family][group]['pipelineOptions']['imageModifications']

        if( 'outputCanvasMediaSize' in default_expected_image_modifications):
            assert default_expected_image_modifications['outputCanvasMediaSize'] == default_image_modifications_ticket['outputCanvasMediaSize']

        if( 'outputCanvasMediaId' in default_expected_image_modifications):
            assert default_expected_image_modifications['outputCanvasMediaId'] == default_image_modifications_ticket['outputCanvasMediaId']

        if( 'outputCanvasCustomWidth' in default_expected_image_modifications):
            assert default_expected_image_modifications['outputCanvasCustomWidth'] == default_image_modifications_ticket['outputCanvasCustomWidth']

        if( 'outputCanvasCustomLength' in default_expected_image_modifications):
            assert default_expected_image_modifications['outputCanvasCustomLength'] == default_image_modifications_ticket['outputCanvasCustomLength']

        if( 'outputCanvasAnchor' in default_expected_image_modifications):
            assert default_expected_image_modifications['outputCanvasAnchor'] == default_image_modifications_ticket['outputCanvasAnchor']

        if( 'outputCanvasOrientation' in default_expected_image_modifications):
            assert default_expected_image_modifications['outputCanvasOrientation'] == default_image_modifications_ticket['outputCanvasOrientation']

        if( 'backgroundColorRemoval' in default_expected_image_modifications):
            assert default_expected_image_modifications['backgroundColorRemoval'] == default_image_modifications_ticket['backgroundColorRemoval']

        if( 'backgroundColorRemovalLevel' in default_expected_image_modifications):
            assert default_expected_image_modifications['backgroundColorRemovalLevel'] == default_image_modifications_ticket['backgroundColorRemovalLevel']

        if( 'blackEnhancementLevel' in default_expected_image_modifications):
            assert default_expected_image_modifications['blackEnhancementLevel'] == default_image_modifications_ticket['blackEnhancementLevel']

    if ( 'mediaDestination' in data[family][group]["dest"]["print"] ):
        default_dest_print_mediaDestination = ticket_default_body["dest"]["print"]["mediaDestination"]
        default_destination = data[family][group]["dest"]["print"]['mediaDestination']
        assert default_dest_print_mediaDestination == default_destination
    

# HELPER METHODS - END
 
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Cloning of copy jobTicket after updating ticket
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-32886
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy__clone_job_ticket
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy__clone_job_ticket
        +guid:970c3665-bd19-4d1d-914b-9bd05b8214e0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=GrayScale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy__clone_job_ticket(cdm, udw, net, configuration):
    print("test_copy_jobticket_clone: BEGIN")

    print("1. creating a new ticket")
    
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()
    print("Updating colorMode in scan")
    ticket_user_body['src']['scan']['colorMode'] = 'grayscale'
    ticket_user_body['dest']['print']['autoRotate'] = 'true'
    if configuration.familyname in ["designjet"]:
        ticket_user_body['dest']['print']["foldingStyleId"] = 256

    print("2. Updating the ticket")
    ticket_body = {'src': {'scan': {'colorMode': 'grayscale'}}}
    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' +ticket_user_body['ticketId']
    response = cdm.patch_raw(uri_put, ticket_body)
    assert response.status_code == 200

    print("3. Cloning the ticket")
   
    reqPayload = {
            'ticketReference' : 'user/ticket/' + ticket_user_body['ticketId']
            }
    new_ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, reqPayload)
    assert new_ticket_user_response.status_code == 201
    new_ticket_user_body = new_ticket_user_response.json()
    #Assertign the fields
    assert 'grayscale' == new_ticket_user_body['src']['scan']['colorMode']

    assert_field_equal(ticket_user_body['src']['scan'], new_ticket_user_body['src']['scan'])
    assert_field_equal(ticket_user_body['dest']['print'], new_ticket_user_body['dest']['print'])


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check default values for selene
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-29873
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_jobticket_selene_default
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title:  test_copy_cdm_jobticket_selene_default
        +guid: 188bf9da-879b-40cb-806b-01d16e91b3ad
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=CopyColor & PrintEngineFormat=A4 & Copy=Quality
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cdm_jobticket_selene_default(cdm):
    '''
    Check default values for selene
    '''
    
    family = "selene"
    group = "defaultProductGroup"
    check_copy_job_ticket_expected_values(cdm, family, group) 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check default values for designjet
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-29873
    +timeout:120
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_walkupapp_copy_jobticket_designjet_default
    +test: 
        +title: test_walkupapp_copy_jobticket_designjet_default
        +guid: 9924b691-6dff-4bbf-b929-98b23196bb15
        +dut:
            +type: Simulator
            +configuration:UIType=TouchScreen & DeviceClass=LFP & DeviceFunction=CopyColor & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_walkupapp_copy_jobticket_designjet_default(cdm):
    '''
    Check default values for designjet
    '''
    
    family = "designjet"
    group = "defaultProductGroup"
    check_copy_job_ticket_expected_values(cdm, family, group) 


