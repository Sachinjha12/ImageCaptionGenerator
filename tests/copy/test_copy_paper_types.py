import logging
from dunetuf.copy.copy import *
from dunetuf.metadata import get_supported_mediatypes_from_metadata
from dunetuf.localization.LocalizationHelper import LocalizationHelper

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify that the EWS copy mediaTypes are matching with expected metadata mediaTypes.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-133786
    +timeout:180
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_mediatypes
    +test:
        +title:test_copy_ews_mediatypes
        +guid:55d11a5c-e72c-426a-8c41-3298f38603a3
        +dut:
            +type:Engine, Simulator, Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineType=Canon & DoXSupported=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_mediatypes(net, cdm, configuration, ews):
    logging.debug("Get expected mediaTypes from metadata")
    expected_mediaTypes = get_supported_mediatypes_from_metadata(cdm,configuration)
    expected_mediaTypes.sort()

    logging.debug("Get ews copy mediaTypes")
    ews_copy_mediaTypes = ews.media.get_ews_copy_mediatypes()
    ews_copy_mediaTypes.sort()

    ews_expected_copy_mediaTypes = []
    for type in expected_mediaTypes:
        ews_expected_copy_mediaTypes.append(LocalizationHelper.get_string_translation(net, ews.media.media_types_map[type]))
    ews_expected_copy_mediaTypes.sort()

    logging.debug("Make sure that the metadata expected mediaTypes are matching with ews copy mediaTypes")
    assert ews_expected_copy_mediaTypes == ews_copy_mediaTypes,"Failed to match expected metadata paper types with ews copy mediaTypes"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify that the controlPanel copy mediaTypes are matching with expected metadata mediaTypes.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-133786
    +timeout:4000
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_mediatypes
    +test:
        +title:test_copy_ui_mediatypes
        +guid:e7d33742-7d9c-45e8-8ca2-8b63d14aaeb4
        +dut:
            +type:Engine, Simulator, Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineType=Canon & DoXSupported=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mediatypes(spice, cdm, configuration, subtests):
    logging.debug("Get expected mediaTypes from metadata")
    expected_mediaTypes = get_supported_mediatypes_from_metadata(cdm,configuration)

    ews_expected_copy_mediaTypes = []
    for type in expected_mediaTypes:
        ews_expected_copy_mediaTypes.append(spice.copy_ui().metadata_to_ui_media_types_map[type]['ui'])
    ews_expected_copy_mediaTypes.sort()

    logging.debug("Navigate to Copy -->PaperSelection -->PapeType list and make sure expected mediaTypes are reported in Copy PaperType list")
    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().go_to_paper_selection()
    logging.debug(ews_expected_copy_mediaTypes)
    for type in ews_expected_copy_mediaTypes:
        with subtests.test("Testing Copy UI Paper {0} Type".format(type)):
            result = spice.copy_ui().is_paper_type_option_available(type)
            assert True == result,"Failed to find {0} type option in Copy -->PaperSelection -->PapeType list".format(type)
        spice.copy_ui().go_back_to_setting_from_paper_selection()

    spice.copy_ui().go_back_to_setting_from_paper_selection()
    spice.copy_ui().back_to_landing_view()
    spice.goto_homescreen()