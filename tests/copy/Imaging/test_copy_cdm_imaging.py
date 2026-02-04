import logging
from tests.copy.lib.helpers import Helpers
from tests.copy.lib.assertions import Assertions

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: check default values from copy ticket relative to output size
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-80820
    +timeout:120
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_default_values_from_copy_ticket_relative_to_imaging_settings
    +test: 
        +title: test_default_values_from_copy_ticket_relative_to_imaging_settings
        +guid:fabbe61e-9cf7-11ef-8e14-975666f6f352
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScanEngine=LightWing
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_default_values_from_copy_ticket_relative_to_imaging_settings(cdm):
    '''
    Perform GET operation on the cdm endpoint and get defaults values.

    Args:
        cdm: CDM fixture
    '''
    # retrieving the default job ticket from copy
    ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_default_response.status_code == 200
    # Get json
    ticket_default_body = ticket_default_response.json()
    # Go to imageModifications family fields
    ticket_pipeline_options = ticket_default_body['pipelineOptions']
    ticket_image_modifications = ticket_pipeline_options['imageModifications']
    logging.info(f"Current imageModifications fields and values: {ticket_image_modifications}")
    # Filter the fields to check 
    helper = Helpers()
    assertion = Assertions()
    default_expected = helper.aux_get_valid_values_jupiter()
    filtered_fields = helper.aux_filter_target_fields(ticket_image_modifications,default_expected) 
    # Validate values with default ones
    assertion.aux_fields_validator(filtered_fields,default_expected)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check that all constraints are the expected with the imaging values added
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-88386
    +timeout:120
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF    
    +test_classification:1
    +name: test_constraint_values_from_copy_ticket_relative_to_imaging_settings
    +test:
        +title: test_constraint_values_from_copy_ticket_relative_to_imaging_settings
        +guid:4b977e02-8c48-476b-b8f9-e8b5c9a6f4ba
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScanEngine=LightWing
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_constraint_values_from_copy_ticket_relative_to_imaging_settings(cdm):
    helper = Helpers()
    constraint_expected = helper.aux_get_valid_values_jupiter()

    constraints_url = "/cdm/jobTicket/v1/configuration/defaults/copy/constraints"
    constraints_json = cdm.get(constraints_url)
    assertion = Assertions()

    for contraint_key,contraint_values in constraint_expected.items():

        constraintsFromTicket = helper.find_constraint(constraints_json, "pipelineOptions/imageModifications/" + str(contraint_key))
        assertion.compare_constraints_list(constraintsFromTicket,contraint_values)
