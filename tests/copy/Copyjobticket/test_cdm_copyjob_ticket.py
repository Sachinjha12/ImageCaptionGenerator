import json
import logging
import pprint


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

# HELPER METHODS - END

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Saves and Recovers a Copy JobTicket a DataStore
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-5008
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_jobticket_persistence_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_jobticket_persistence_cdm
        +guid:450309a9-3f90-47bb-9032-8a47509b5dc7
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

def test_copy_jobticket_persistence_cdm(cdm, udw, tray):
    print("\ntest_copy_jobticket_persistence_cdm: BEGIN")

    print("1. creating a new ticket")
 
    body = source_destination("scan", "print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code < 300
    ticket_user_body = ticket_user_response.json()

    print("2. retrieving the default job ticket")
    ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY, None)
    assert ticket_default_response.status_code < 300
    ticket_default_body = ticket_default_response.json()

    print("3. compare both tickets")
    src_dest_user_body = extract_src_dest(ticket_user_body)
    src_dest_default_body = extract_src_dest(ticket_default_body)
    assert_field_equal(src_dest_user_body, src_dest_default_body)
    default_src_scan_mediaSize = ticket_default_body["src"]["scan"].get("mediaSize")
    default_dest_print_copies = ticket_default_body["dest"]["print"]["copies"]
    default_dest_print_mediaSource = ticket_default_body["dest"]["print"]["mediaSource"]

    print("4. Calculate the new values for the default job ticket")
    value_src_scan_mediaSize = "na_letter_8.5x11in" if ticket_default_body["src"]["scan"].get("mediaSize") == "iso_a4_210x297mm" else "iso_a4_210x297mm"
    value_dest_print_copies = 3 if ticket_default_body["dest"]["print"]["copies"] == 1 else 1
    default_tray = tray.get_default_source()
    if default_tray == 'main':
        value_dest_print_mediaSource = "alternate" if ticket_default_body["dest"]["print"]["mediaSource"] == "main" else "main"
    else:
        value_dest_print_mediaSource = "tray-2" if ticket_default_body["dest"]["print"]["mediaSource"] == "tray-1" else "tray-1"
    value_pipelineOptions_imageModifications_exposure = "9" if ticket_default_body["pipelineOptions"]["imageModifications"].get("exposure") == "5" else "9"
    value_pipelineOptions_scaling_xScalePercent = "200" if ticket_default_body["pipelineOptions"]["scaling"].get("xScalePercent") == "100" else "200"

    print("5. Change default job ticket")
    tikcet_new_default_values_body = {"src":             {"scan":               {"mediaSize": value_src_scan_mediaSize}}, 
                                      "dest":            {"print":              {"copies": value_dest_print_copies, "mediaSource": value_dest_print_mediaSource}},
                                      "pipelineOptions": {"imageModifications": {"exposure": value_pipelineOptions_imageModifications_exposure}},
                                      "pipelineOptions": {"scaling":            {"xScalePercent": value_pipelineOptions_scaling_xScalePercent}}}
    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, tikcet_new_default_values_body)
    assert put_response.status_code < 300

    print("6. Retrieve new job ticket")
 
    body = source_destination("scan", "print")
    ticket_user_new_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_new_response.status_code < 300
    ticket_user_new_body = ticket_user_new_response.json()

    print("7. Compare changes with the new default values")
    src_dest_user_new_body = extract_src_dest(ticket_user_new_body)
    assert_field_equal(tikcet_new_default_values_body, src_dest_user_new_body)

    print("8. Reset default values")
    ticket_new_default_values_body = {"src": {"scan": {"mediaSize": default_src_scan_mediaSize}}, "dest": {
        "print": {"copies": default_dest_print_copies, "mediaSource": default_dest_print_mediaSource}}}
    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, ticket_new_default_values_body)
    assert put_response.status_code < 300
    ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY, None)
    assert ticket_default_response.status_code < 300
    ticket_default_body = ticket_default_response.json()
    print(ticket_default_body)

    print("\ntest_copy_jobticket_persistence_cdm: END")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate default media size for different country region
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-177512
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_default_mediaSize_for_different_country_region
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_cdm_default_mediaSize_for_different_country_region
        +guid:5fcba652-e479-447d-89b9-c0dd1b3d69c0
        +dut:
            +type: Engine
            +configuration: DeviceFunction=Copy  & Language=ja-JP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_default_mediaSize_for_different_country_region(cdm):
    default_copy_job_ticket = cdm.JOB_TICKET_COPY
    response = cdm.patch_raw(cdm.SYSTEM_CONFIGURATION, {"countryRegion": "US"})
    assert response.status_code == 204, 'Not Restored language to English and country to US'
    default_payload = cdm.get(default_copy_job_ticket)
    assert default_payload['src']['scan']['mediaSize'] == "na_letter_8.5x11in", "Media size is not as expected"

    response = cdm.patch_raw(cdm.SYSTEM_CONFIGURATION, {"countryRegion": "JP"})
    assert response.status_code == 204, 'Not Restored language to Japanese and country to Japan'
    default_payload = cdm.get(default_copy_job_ticket)
    assert default_payload['src']['scan']['mediaSize'] == "iso_a4_210x297mm", "Media size is not as expected"

    response = cdm.patch_raw(cdm.SYSTEM_CONFIGURATION, {"countryRegion": "CA"})
    assert response.status_code == 204, 'Not Restored language to English and country to Canada'
    default_payload = cdm.get(default_copy_job_ticket)
    assert default_payload['src']['scan']['mediaSize'] == "na_letter_8.5x11in", "Media size is not as expected"

