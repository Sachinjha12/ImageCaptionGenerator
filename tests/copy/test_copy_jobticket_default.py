import os
import json
import pprint
import time

TESTRESOURCEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')

# HELPER METHODS - BEGIN
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
    +name: test_copy_jobticket_designjet_default
    +test: 
        +title: test_copy_jobticket_designjet_default
        +guid: 2d637294-6575-11eb-a873-efce225b769e
        +dut:
            +type: Simulator
            +configuration:UIType=TouchScreen & DeviceClass=LFP & DeviceFunction=CopyColor & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_jobticket_designjet_default(cdm):
    '''
    Check default values for designjet
    '''
    
    family = "designjet"
    group = "defaultProductGroup"
    check_copy_job_ticket_expected_values(cdm, family, group) 

