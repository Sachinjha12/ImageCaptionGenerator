import json
from pprint import pprint

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

# HELPER METHODS - END

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint content type setting.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_content_type_constraint_LFP_CDM
    +test:
        +title: test_copy_content_type_constraint_LFP_CDM
        +guid: 35955198-60ce-11ed-bc42-c3f5ca3287c8
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanOriginalPaperType=AmmoniaOldBlueprint & ScanOriginalPaperType=Blueprint & ScanOriginalPaperType=Translucent
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_content_type_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"

    print("step 1: Get actual values")
    url = ticket_path
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)
    default_mediaType = default_values_dict['mediaType']

    # Scenario content type setting
    #********************************

    # Check 1: mediaType = translucentPaper -> contentType == lineDrawing
    media = "translucentPaper"
    available_options = []
    disabled_options = []
    print()
    print("Check 1: mediaType = translucentPaper -> contentType == lineDrawing")
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': media}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "src/scan/contentType")
    available_options.append(find_validator_option(current_constraints, "lineDrawing"))
    disabled_options.append(find_validator_option(current_constraints, "image"))
    disabled_options.append(find_validator_option(current_constraints, "mixed"))
    assert is_enabled(available_options,"lineDrawing")
    assert  is_disabled(disabled_options,"image") and \
            is_disabled(disabled_options,"mixed")
    
    # Check 2: mediaType = blueprints -> contentType == lineDrawing
    media = "blueprints"
    available_options = []
    disabled_options = []
    print()
    print("Check 2: mediaType = blueprints -> contentType == lineDrawing")
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': media}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "src/scan/contentType")
    available_options.append(find_validator_option(current_constraints, "lineDrawing"))
    disabled_options.append(find_validator_option(current_constraints, "image"))
    disabled_options.append(find_validator_option(current_constraints, "mixed"))
    assert is_enabled(available_options,"lineDrawing")
    assert  is_disabled(disabled_options,"image") and \
            is_disabled(disabled_options,"mixed")

    # Check 3: mediaType = darkBlueprints -> contentType == lineDrawing, mixed
    media = "darkBlueprints"
    available_options = []
    disabled_options = []
    print()
    print("Check 3: mediaType = darkBlueprints -> contentType == lineDrawing, mixed")
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': media}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "src/scan/contentType")
    available_options.append(find_validator_option(current_constraints, "lineDrawing"))
    disabled_options.append(find_validator_option(current_constraints, "image"))
    available_options.append(find_validator_option(current_constraints, "mixed"))
    assert is_enabled(available_options,"lineDrawing") and \
        is_enabled(available_options,"mixed")
    assert  is_disabled(disabled_options,"image")

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': default_mediaType}}})

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint invert colors.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_invert_colors_constraint_LFP_CDM
    +test:
        +title: test_copy_invert_colors_constraint_LFP_CDM
        +guid: bcdb7c59-1839-4d45-a358-4844adc238b7
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_invert_colors_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"
    
    # Scenario invert colors setting  (invert blueprint on UI) 
    #********************************

    # Check 1: mediaType != blueprints or darkBlueprints -> invertColors = false
    mediaType = ["translucentPaper", "photoPaper", "whitePaper", "oldRecycledPaper"]
    for media in mediaType:
        disabled_options = []
        print()
        print("Check 1: mediaType != blueprints or dark blueprints -> invertColors = true")
        print()
        expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType':media}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "src/scan/invertColors")
        disabled_options.append(find_validator_option(current_constraints, "true"))
        assert is_disabled(disabled_options,"true")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint color mode.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_color_mode_constraint_LFP_CDM
    +test:
        +title: test_copy_color_mode_constraint_LFP_CDM
        +guid: d3b4e42f-3d97-4a13-aa47-81054659791f
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanOriginalPaperType=AmmoniaOldBlueprint & ScanOriginalPaperType=Blueprint & ScanOriginalPaperType=Translucent
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_color_mode_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")

    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    
    print("step 1: Get actual values")
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)

    default_mediaType = default_values_dict['mediaType']
    # Scenario color mode setting
    #********************************

    # Check 1: mediaType = blueprints, translucent -> Color or grayscale
    mediaType = ["blueprints", "translucentPaper"]

    for media in mediaType:
        available_options = []
        print()
        print("Check 1: mediaType = blueprints -> colorMode = Color or grayscale")
        print()
        expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': media}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "src/scan/colorMode")
        available_options.append(find_validator_option(current_constraints, "color"))
        available_options.append(find_validator_option(current_constraints, "grayscale"))
        assert  is_enabled(available_options,"color") and \
                is_enabled(available_options,"grayscale")

    # Check 2: mediaType = DarkBlueprint -> grayscale
    media = "darkBlueprints"
    available_options = []
    disabled_options = []
    print()
    print("Check 2: mediaType = darkBlueprints -> colorMode = Grayscale")
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': media}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "src/scan/colorMode")
    available_options.append(find_validator_option(current_constraints, "grayscale"))
    disabled_options.append(find_validator_option(current_constraints, "color"))
    assert  is_enabled(available_options,"grayscale")
    assert  is_disabled(disabled_options,"color")

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': default_mediaType}}})

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint background color removal.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_background_color_removal_constraint_LFP_CDM
    +test:
        +title: test_copy_background_color_removal_constraint_LFP_CDM
        +guid: 63fd7cf4-14a2-40c4-9d41-ff12deee82c5
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing & ScanOriginalPaperType=AmmoniaOldBlueprint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_background_color_removal_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    
    print("step 1: Get actual values")
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)

    default_mediaType = default_values_dict['mediaType']
    default_colorMode = default_values_dict['colorMode']
    # Scenario background color removal setting
    #********************************

    # Check 1: contentType == photo OR contentType == image OR -> backgroundColorRemoval = disabled
    mediaType = "photoPaper"
    disabled_options = []
    print()
    print("Check 1: contentType == photo OR contentType == image -> backgroundColorRemoval = disabled")
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': mediaType}}})
    response = cdm.get(constraints_url)
    ticket = cdm.get(url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/backgroundColorRemoval")
    disabled_options.append(find_validator_option(current_constraints, "true"))
    assert is_disabled(disabled_options,"true")
    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': default_mediaType}}})

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'colorMode': default_colorMode}}})

    # Check 3: contentType == photo OR contentType == image OR -> backgroundColorRemoval = disabled
    mediaType = "darkBlueprints"
    print()
    print("Check 3: contentType == photo OR contentType == image -> backgroundColorRemoval = disabled but with value true")
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': mediaType}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/backgroundColorRemoval")
    disabled_options.append(find_validator_option(current_constraints, "false"))
    assert is_disabled(disabled_options,"false")
    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': default_mediaType}}})

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint background Color Removal Level.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_background_color_removal_level_constraint_LFP_CDM
    +test:
        +title: test_copy_background_color_removal_level_constraint_LFP_CDM
        +guid: 2b4d40d5-89cf-4f6a-88ee-08b48506abbb
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_background_color_removal_level_constraint_LFP_CDM(cdm):

    available_options = []
    print("1. Creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"

    # Scenario background color removal level setting
    #********************************

    # Check 1: backgroundColorRemoval == disabled -> backgroundColorRemovalLevel = disabled and backgroundColorRemovalLevel=0
    field_mock = {"seValue" : None}
    disabled_options = []
    print()
    print("Check 1: backgroundColorRemoval == disabled -> backgroundColorRemovalLevel = disabled and backgroundColorRemovalLevel=0") 
    print()
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': "whitePaper"}}})
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'colorMode': "grayscale"}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'backgroundColorRemoval': 'true'}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'backgroundColorRemovalLevel': 2}}})
    # This should force backgroundColorRemoval to be false
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'mediaType': "photoPaper"}}})
    response = cdm.get(constraints_url)
    min = max = 0
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/backgroundColorRemovalLevel")
    available_options.append(find_validator_option(current_constraints, "0"))
    # current_constraints anwer is not standard in this json
    # We need to reconfigure it (mock) a litle to be used with is_disabled() function
    key = "disabled"
    value = current_constraints[key] ["value"]
    field_mock[key] = value
    disabled_options.append(field_mock)
    disabled_options.append(current_constraints)
    assert is_disabled(disabled_options,None)
    assert is_enabled(available_options, "0") 

# Scenario 6: Black enhancement level (currently black and white still not accepted)
#********************************
# Check: colorMode == black and white -> black enhancement level = 60

# Scenario 7: Auto Deskew Setting (currently 1200 dpi is not supported) 
# Check: Resolution == 1200 -> auto deskew = off
#********************************

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint scan acquisition speed.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_scan_acquisition_speed_constraint_LFP_CDM
    +test:
        +title: test_copy_scan_acquisition_speed_constraint_LFP_CDM
        +guid: 3c0323b5-71a7-4057-affd-4b0b4e323112
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_scan_acquisition_speed_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    
    print("step 1: Get actual values")
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)

    default_scanAcquisitionsSpeed = default_values_dict['scanAcquisitionsSpeed']
    default_colorMode = default_values_dict['colorMode']

    # Scenario Scan acquisition speed (reduce scan speed)
    #********************************

    # Check 1: Resolution == 600 or 1200 (currently 1200 dpi is not supported) ->  acquisition speed can only be auto
    
    available_options = []
    disabled_options = []
    resolution = "e600Dpi"
    # resolutions = ["e600Dpi", "e1200Dpi"] (currently 1200 dpi is not supported) 
    print()
    print("Check 1: Resolution == 600 or 1200 (currently 1200 dpi is not supported) ->  acquisition speed can only be auto") 
    print()
    # This sould force scanAcquisitionsSpeed to slow
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'colorMode': "grayscale"}}})
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'scanAcquisitionsSpeed': "slow"}}})
    # This sould activate the constraint scanAcquisitionsSpeed == auto
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'resolution': resolution}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "src/scan/scanAcquisitionsSpeed")
    available_options.append(find_validator_option(current_constraints, "auto"))
    disabled_options.append(find_validator_option(current_constraints, "slow"))
    assert is_disabled(disabled_options,"slow")
    assert is_enabled(available_options, "auto")

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'colorMode': default_colorMode}}})
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'scanAcquisitionsSpeed': default_scanAcquisitionsSpeed}}})
    
    # Check 8.2: Resolution == 300 and colorMode = color -> acquisition speed can only be auto
    resolution = "e300Dpi"
    available_options = []
    disabled_options = []
    print()
    print("Check 2: Resolution == 300 and colorMode = color -> acquisition speed can only be auto") 
    print()
    # This sould force scanAcquisitionsSpeed to slow
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'colorMode': "grayscale"}}})
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'scanAcquisitionsSpeed': "slow"}}})
    # This sould activate the constraint scanAcquisitionsSpeed == auto
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'resolution': resolution}}})
    expect_patch_success(cdm, ticket_path, {'src': {'scan': {'colorMode': "color"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "src/scan/scanAcquisitionsSpeed")
    available_options.append(find_validator_option(current_constraints, "auto"))
    disabled_options.append(find_validator_option(current_constraints, "slow"))
    assert is_disabled(disabled_options,"slow")
    assert is_enabled(available_options, "auto")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint OutputCanvasMediaId.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_output_canvas_media_id_constraint_LFP_CDM
    +test:
        +title: test_copy_output_canvas_media_id_constraint_LFP_CDM
        +guid: eceb11a8-923b-4992-9e8c-0737fa89990d
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_output_canvas_media_id_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    
    print("step 1: Get actual values")
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)

    default_mediaSource = default_values_dict['mediaSource']
    
    # Scenario OutputCanvasMediaId (output size to media source)
    #********************************

    # Check 1: outputMediaSource (paper selection, media input) is not autoselect ->  output canvas media id can only be autoselect
    available_options = []
    disabled_options = []
    print()
    print("Check 1: outputMediaSource (paper selection, media input) is not autoselect ->  output canvas media id can only be autoselect") 
    print()
    expect_patch_success(cdm, ticket_path, {'dest': {'print': {'mediaSource': "roll-1"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/outputCanvasMediaId")
    available_options.append(find_validator_option(current_constraints, "auto"))
    disabled_options.append(find_validator_option(current_constraints, "roll-1"))
    disabled_options.append(find_validator_option(current_constraints, "roll-2"))
    assert is_disabled(disabled_options,"roll-1")
    assert is_disabled(disabled_options,"roll-2")
    assert is_enabled(available_options, "auto")

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'dest': {'print': {'mediaSource': default_mediaSource}}})
   
    # Check 2: scaleSelection = scaleToOutput and scaletoOutput is any roll ->  output canvas media id can only be autoselect
    default_scaleToOutput = default_values_dict['scaleToOutput']
    default_scaleSelection = default_values_dict['scaleSelection']
    available_options = []
    disabled_options = []
    rolls = ["roll-1","roll-2"]
    for any_roll in rolls:
        print()
        print("# Check 2: scaleSelection = scaleToOutput and scaletoOutput is any roll ->  output canvas media id can only be autoselect") 
        print()
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'scaling': {'scaleToOutput': any_roll}}})
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'scaling': {'scaleSelection': "scaleToOutput"}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "pipelineOptions/imageModifications/outputCanvasMediaId")
        available_options.append(find_validator_option(current_constraints, "auto"))
        disabled_options.append(find_validator_option(current_constraints, "roll-1"))
        disabled_options.append(find_validator_option(current_constraints, "roll-2"))
        assert is_disabled(disabled_options,"roll-1")
        assert is_disabled(disabled_options,"roll-2")
        assert is_enabled(available_options, "auto")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint Output canvas anchor.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_output_canvas_anchor_constraint_LFP_CDM
    +test:
        +title: test_copy_output_canvas_anchor_constraint_LFP_CDM
        +guid: cd92b3c2-5b85-4ade-a875-361afa3642f6
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_output_canvas_anchor_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"

    # Scenario Output canvas anchor (alingment of outputsize)
    #********************************

    # Check 1 : output canvas media size is Any and output canvas media id is autoSelect
    available_options = []
    disabled_options = []
    print()
    print("# Check 1 : output canvas media size is Any and output canvas media id is autoSelect") 
    print()
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': "any"}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaId': 'auto'}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/outputCanvasAnchor")
    available_options.append(find_validator_option(current_constraints, "topCenter"))
    disabled_options.append(find_validator_option(current_constraints, "topRight"))
    disabled_options.append(find_validator_option(current_constraints, "middleLeft"))
    disabled_options.append(find_validator_option(current_constraints, "middleCenter"))
    disabled_options.append(find_validator_option(current_constraints, "middleRight"))
    disabled_options.append(find_validator_option(current_constraints, "bottomLeft"))
    disabled_options.append(find_validator_option(current_constraints, "bottomCenter"))
    disabled_options.append(find_validator_option(current_constraints, "bottomRight"))
    assert is_disabled(disabled_options,"topRight")
    assert is_disabled(disabled_options,"middleLeft")
    assert is_disabled(disabled_options,"middleCenter")
    assert is_disabled(disabled_options,"middleRight")
    assert is_disabled(disabled_options,"bottomLeft")
    assert is_disabled(disabled_options,"bottomCenter")
    assert is_disabled(disabled_options,"bottomRight")
    assert is_enabled(available_options, "topCenter")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint Output canvas orientation.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_output_canvas_orientation_constraint_LFP_CDM
    +test:
        +title: test_copy_output_canvas_orientation_constraint_LFP_CDM
        +guid: 1c41ba7b-fa73-4d90-94ce-64b563665598
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_output_canvas_orientation_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
    
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    
    print("step 1: Get actual values")
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)

    default_outputCanvasMediaSize = default_values_dict['outputCanvasMediaSize']
    default_outputCanvasMediaId = default_values_dict['outputCanvasMediaId']
    default_outputCanvasOrientation = default_values_dict['outputCanvasOrientation']

    # Scenario Scenario Output canvas orientation
    #********************************
    
    # Check 1: outputcanvasmediasize is A0,B0 or B1 -> orientation can only be portrait
    available_options = []
    disabled_options = []
    portraid_sizes = ["iso_a0_841x1189mm","iso_b0_1000x1414mm","iso_b1_707x1000mm"]
    for size in portraid_sizes:
        print()
        print("Check 1: outputcanvasmediasize is A0,B0,B1 or custom -> orientation can only be portrait")
        print()
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': size}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "pipelineOptions/imageModifications/outputCanvasOrientation")
        available_options.append(find_validator_option(current_constraints, "portrait"))
        disabled_options.append(find_validator_option(current_constraints, "landscape"))
        assert is_disabled(disabled_options,"landscape")
        assert is_enabled(available_options, "portrait")

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': default_outputCanvasMediaSize}}})

    # Check 2: output canvas media size is Any and output canvas media id is autoSelect -> orientation can be both but are disabled

    available_options = []
    disabled_options = []
    print()
    print("# Check 2: output canvas media size is Any and output canvas media id is autoSelect -> orientation can be both but are disabled")
    print()
    # Patch ticket or the defaul value (Landscape) will remain
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasOrientation': 'landscape'}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': "any"}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaId': 'auto'}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/imageModifications/outputCanvasOrientation")
    assert constrain_disabled(current_constraints)
    available_options.append(find_validator_option(current_constraints, "portrait"))
    available_options.append(find_validator_option(current_constraints, "landscape"))
    assert is_enabled(available_options,"landscape")
    assert is_enabled(available_options, "portrait")

    assert check_output_content_orientation(cdm, url, 'landscape')

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': default_outputCanvasMediaSize}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaId': default_outputCanvasMediaId}}})
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasOrientation': default_outputCanvasOrientation}}})

    # Check 3: output canvas media size is Any or Custom -> orientation can be both but are disabled

    available_options = []
    disabled_options = []
    portraid_sizes = ["any","custom"]
    for size in portraid_sizes:
        print()
        print("Check 3: output canvas media size is Any or Custom -> orientation can be both but are disabled") 
        print()
        # Patch ticket or the defaul value (portrait) will remain
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasOrientation': 'landscape'}}})
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': size}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "pipelineOptions/imageModifications/outputCanvasOrientation")
        assert constrain_disabled(current_constraints)
        available_options.append(find_validator_option(current_constraints, "portrait"))
        available_options.append(find_validator_option(current_constraints, "landscape"))
        assert is_enabled(available_options,"landscape")
        assert is_enabled(available_options, "portrait")

        assert check_output_content_orientation(cdm, url, 'landscape')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint Scale Selection.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_scale_selection_constraint_LFP_CDM
    +test:
        +title: test_copy_scale_selection_constraint_LFP_CDM
        +guid: 717ee8cc-c059-48e2-8b8d-5d77966a67ce
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_scale_selection_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"
    
    # Scenario Scenario Scale Selection
    #********************************

    # Check 1: copy margins is oversize -> scale selection can only be custom o scale to standard sizes
    available_options = []
    disabled_options = []
    print()
    print("# Check 1: copy margins is oversize -> scale selection can only be custom o scale to standard sizes") 
    print()
    expect_patch_success(cdm, ticket_path, {'dest': {'print': {'printMargins': "oversize"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/scaling/scaleSelection")
    available_options.append(find_validator_option(current_constraints, "custom"))
    available_options.append(find_validator_option(current_constraints, "standardSizeScaling"))
    disabled_options.append(find_validator_option(current_constraints, "scaleToOutput"))
    assert is_enabled(available_options, "custom")
    assert is_enabled(available_options, "standardSizeScaling")
    assert is_disabled(disabled_options,"scaleToOutput")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint scale to output.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_scale_to_output_constraint_LFP_CDM
    +test:
        +title: test_copy_scale_to_output_constraint_LFP_CDM
        +guid: eddf7d04-9efd-48f4-b316-f47e5ab348b1
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_scale_to_output_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    url = ticket_path
    constraints_url = ticket_path + "/constraints"
    
    print("step 1: Get actual values")
    default_ticket = cdm.get(url)
    default_values_dict = flatten_dict(default_ticket)
    print("Default ticket values are: ",default_ticket)

    default_mediaSource = default_values_dict['mediaSource']
    default_outputCanvasMediaId = default_values_dict['outputCanvasMediaId']
    # Scenario Scenario Scale to output
    #********************************

    # Check 1: output media source (paper selection, media input) is not auto select (is selected any roll) -> scale to output can only be auto select
    disabled_options = []
    print()
    print("# Check 1: output media source (paper selection, media input) is not auto select (is selected any roll) -> scale to output can only be auto select") 
    print()
    rolls = ["roll-1","roll-2"]
    for any_roll in rolls:
        expect_patch_success(cdm, ticket_path, {'dest': {'print': {'mediaSource': any_roll}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "pipelineOptions/scaling/scaleSelection")
        disabled_options.append(find_validator_option(current_constraints, "scaleToOutput"))
        assert is_disabled(disabled_options,"scaleToOutput")

    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'dest': {'print': {'mediaSource': default_mediaSource}}})

    # Check 2: output canvas media id (output size to media source) is not auto select (is selected any roll) -> scale to output can only be auto select
    disabled_options = []
    print()
    print("# Check 2: output canvas media id (output size to media source) is not auto select (is selected any roll) -> scale to output can only be auto select") 
    print()
    rolls = ["roll-1","roll-2"]
    for any_roll in rolls:
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaId': any_roll}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "pipelineOptions/scaling/scaleSelection")
        disabled_options.append(find_validator_option(current_constraints, "scaleToOutput"))
        assert is_disabled(disabled_options,"scaleToOutput")
    
    # Return modified values to their defaults
    expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaId': default_outputCanvasMediaId}}})

    # Check 3: copy margins is oversize -> scale to output can only be auto select
    disabled_options = []
    print()
    print("# Check 3: copy margins is oversize -> scale to output can only be auto select") 
    print()
    expect_patch_success(cdm, ticket_path, {'dest': {'print': {'printMargins': "oversize"}}})
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "pipelineOptions/scaling/scaleSelection")
    disabled_options.append(find_validator_option(current_constraints, "scaleToOutput"))
    assert is_disabled(disabled_options,"scaleToOutput")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint media Source.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_media_source_constraint_LFP_CDM
    +test:
        +title: test_copy_media_source_constraint_LFP_CDM
        +guid: 66a9e9c3-29cb-4e8c-80ea-0e3db1b49be6
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_media_source_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"
    
    # Scenario Print media source
    #********************************

    # Check 1: output canvas media id (output size media source) is not autoselect (is selected any roll) -> print media source can only be auto select

    available_options = []
    disabled_options = []
    rolls = ["roll-1","roll-2"]
    for any_roll in rolls:
        print()
        print("# Check 1: output canvas media id (output size media source) is not autoselect (is selected any roll) -> print media source can only be auto select") 
        print()
        expect_patch_success(cdm, ticket_path, {'pipelineOptions': {'imageModifications': {'outputCanvasMediaId': any_roll}}})
        response = cdm.get(constraints_url)
        current_constraints = find_constraint(response, "dest/print/mediaSource")
        available_options.append(find_validator_option(current_constraints, "auto"))
        disabled_options.append(find_validator_option(current_constraints, "roll-1"))
        disabled_options.append(find_validator_option(current_constraints, "roll-2"))
        assert is_enabled(available_options, "auto")
        assert is_disabled(disabled_options,"roll-1")
        assert is_disabled(disabled_options,"roll-2")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test dinamic copy constraint collate.
    +test_tier: 1
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-98306
    +timeout:30
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_collate_constraint_LFP_CDM
    +test:
        +title: test_copy_collate_constraint_LFP_CDM
        +guid: 86b54eb8-7d40-43f2-b362-dd75e0b46928
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_collate_constraint_LFP_CDM(cdm):

    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("Ticket URI: " + cdm.JOB_TICKET_ENDPOINT)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id

    constraints_url = ticket_path + "/constraints"
    
    # Scenario Scenario Collate setting
    #********************************

    # Check 1: number of copies is 1 -> collate can only be true.
    available_options = []
    disabled_options = []

    print()
    print("# Check 1: number of copies is 1 by default-> collate can only be true.")
    print()
    response = cdm.get(constraints_url)
    current_constraints = find_constraint(response, "dest/print/collate")
    available_options.append(find_validator_option(current_constraints, "collated"))
    disabled_options.append(find_validator_option(current_constraints, "uncollated"))
    assert is_enabled(available_options, "collated")
    assert is_disabled(disabled_options,"uncollated")

    """
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy to check that deserialize values with compatibility values in a unique action works
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-207886
    +timeout:60
    +asset: Copy
    +test_framework: TUF
    +name: test_copy_output_canvas_patch_compatible_settings_with_multiple_values_in_ticket
    +delivery_team:LFP
    +feature_team:LFP_ScannerWorkflows
    +test:
        +title: test_copy_output_canvas_patch_compatible_settings_with_multiple_values_in_ticket
        +guid:fa1da6ca-7655-11ef-9a7c-1f8f892ea0e3
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & ScanEngine=LightWing
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_output_canvas_patch_compatible_settings_with_multiple_values_in_ticket(cdm):
    
    print("1. Creating a new ticket")
   
    source = "scan"
    dest = "print"
    body = source_destination(source, dest)
    print("Body: ",body)
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    print("initial response:  %d" % ticket_user_response.status_code)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. Updating ticket using payload.")
    ticket_id = ticket_user_body["ticketId"]
    print("Ticket ticket_id: " + ticket_id)

    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    dict_json_patch = {'pipelineOptions': {'imageModifications': {'outputCanvasMediaSize': 'iso_a2_420x594mm','outputCanvasAnchor':'middleCenter'}}}
    expect_patch_success(cdm, ticket_path, dict_json_patch)

    print("3. Get the ticket after changes")
    ticket_user_response = cdm.get(ticket_path)
    
    print("4. Validate the values")
    assert ticket_user_response['pipelineOptions']['imageModifications']['outputCanvasMediaSize'] == 'iso_a2_420x594mm'
    assert ticket_user_response['pipelineOptions']['imageModifications']['outputCanvasAnchor'] == 'middleCenter'


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy Pre preview job, check the constrints and validate the values
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-137932
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_preview_get_ticket_and_check_constraints
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_preview_get_ticket_and_check_constraints
        +guid:ea324e0c-1c72-4854-b6d6-c535e03ff679
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=ImagePreview & ScanMode=Book
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_preview_get_ticket_and_check_constraints(job, copy, cdm, udw, scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
                    'resolution':'e300Dpi',
                    'scanCaptureMode': 'addpage'
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }
 
    # Create a preview job and get the ticket
    ticket_id = copy.do_preview_job(waitTime = 60, **payload)
    ticket = job.get_job_ticket_info(ticket_id)

    # Check the constraints
    assert ticket is not None, "Ticket should not be None"

    ticket_path = cdm.JOB_TICKET_ENDPOINT + "/" + ticket_id
    ticket_constraints_path = ticket_path + "/constraints"

    # check with adf first
    constraints_json = cdm.get(ticket_constraints_path)

    content_type = find_constraint(constraints_json, "src/scan/contentType")
    color_mode = find_constraint(constraints_json, "src/scan/colorMode")
    scan_plexMode = find_constraint(constraints_json, "src/scan/plexMode")
    scan_capture_mode = find_constraint(constraints_json, "src/scan/scanCaptureMode")
    content_orientation = find_constraint(constraints_json, "src/scan/contentOrientation")
    resolution = find_constraint(constraints_json, "src/scan/resolution")
    scale_selection = find_constraint(constraints_json, "pipelineOptions/scaling/scaleSelection")
    pages_FlipUpEnabled = find_constraint(constraints_json, "src/scan/pagesFlipUpEnabled")
    background_ColorRemoval = find_constraint(constraints_json, "pipelineOptions/imageModifications/backgroundColorRemoval")
    background_ColorRemovalLevel = find_constraint(constraints_json, "pipelineOptions/imageModifications/backgroundColorRemovalLevel")
    pages_PerSheet = find_constraint(constraints_json, "pipelineOptions/imageModifications/pagesPerSheet")
    booklet_format = find_constraint(constraints_json, "pipelineOptions/imageModifications/bookletFormat")
    blank_page_suppression = find_constraint(constraints_json, "pipelineOptions/imageModifications/blankPageSuppressionEnabled")
    sharpness = find_constraint(constraints_json, "pipelineOptions/imageModifications/sharpness")
    contrast = find_constraint(constraints_json, "pipelineOptions/imageModifications/contrast")
    exposure = find_constraint(constraints_json, "pipelineOptions/imageModifications/exposure")
    backGround_cleanup = find_constraint(constraints_json, "pipelineOptions/imageModifications/backgroundCleanup")
    autoPaperColor_Removal = find_constraint(constraints_json, "pipelineOptions/imageModifications/autoPaperColorRemoval")
    output_mediaType = find_constraint(constraints_json, "dest/print/mediaType")
    media_Destination = find_constraint(constraints_json, "dest/print/mediaDestination")
    

    assert ("disabled" in scale_selection)
    assert ("disabled" in content_type)
    assert ("disabled" in color_mode)
    assert ("disabled" in scan_plexMode)
    assert ("disabled" in resolution)
    assert ("disabled" in scan_capture_mode)
    assert ("disabled" in content_orientation)
    assert ("disabled" in pages_PerSheet)
    assert ("disabled" in pages_FlipUpEnabled)
    assert ("disabled" in background_ColorRemoval)
    assert ("disabled" in background_ColorRemovalLevel)
    assert ("disabled" in booklet_format)
    assert ("disabled" in blank_page_suppression)
    assert ("disabled" in sharpness)
    assert ("disabled" in contrast)
    assert ("disabled" in exposure)
    assert ("disabled" in backGround_cleanup)
    assert ("disabled" in autoPaperColor_Removal)
    assert ("disabled" in output_mediaType)
    assert ("disabled" in media_Destination)

