import logging
from dunetuf.copy.copy import *
from dunetuf.metadata import get_supported_mediasizes_from_metadata
from dunetuf.emulation.print.print_emulation_ids import DuneEngineMake

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify that the EWS Copy paper sizes are matching with expected metadata paper sizes.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-151898
    +timeout:180
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_mediasizes
    +test:
        +title:test_copy_ews_mediasizes
        +guid:7ee4e3ba-308c-4c0b-911e-72063706ccea
        +dut:
            +type:Engine,Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineType=Canon & DoXSupported=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_mediasizes(cdm, configuration, ews, print_emulation):
    logging.debug("Get expected mediaSizes from metadata")
    expected_mediaSizes = get_supported_mediasizes_from_metadata(cdm,configuration)
    expected_mediaSizes.remove('any') # Note: Any Size is not supported in copy paper sizes list.
    expected_mediaSizes.sort()

    if print_emulation.engine_make == DuneEngineMake.canonHomepro.name:
        # A5-R paper size is not supported in copy paper size for canon ProA4 products.
        if "com.hp.ext.mediaSize.iso_a5_148x210mm.rotated" in expected_mediaSizes:
            expected_mediaSizes.remove("com.hp.ext.mediaSize.iso_a5_148x210mm.rotated")
    # Media Size "jpn_photo-l_89x127mm" is same as "oe_photo-l_3.5x5in" and FW report only "oe_photo-l_3.5x5in" for Flowers.
    if configuration.productname.strip() in ["lotus"]:
        if "iso_c6_114x162mm" in expected_mediaSizes:
            # C6 paper size is not supported in copy paper size for Lotus
            expected_mediaSizes.remove("iso_c6_114x162mm")

    logging.debug("Get ews copy mediaSizes")
    ews_copy_mediaSizes = ews.media.get_ews_copy_mediasizes()
    ews_copy_mediaSizes.sort()

    ews_expected_copy_mediaSizes = []
    for size in expected_mediaSizes:
        ews_expected_copy_mediaSizes.append(ews.media.media_sizes_map[size]['ews'])
    ews_expected_copy_mediaSizes.sort()

    logging.debug("Make sure that the metadata expected mediaSizes are matching with ews copy mediaSizes")
    assert ews_expected_copy_mediaSizes == ews_copy_mediaSizes,"Failed to match expected metadata mediaSizes with ews copy mediaSizes"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify that the ControlPanel Copy paper sizes are matching with expected metadata paper sizes.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-151898
    +timeout:1800
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_mediasizes
    +test:
        +title:test_copy_ui_mediasizes
        +guid:2940de19-bb7a-4c36-a7a8-8b2434bcde03
        +dut:
            +type:Engine,Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineType=Canon & DoXSupported=True
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mediasizes(spice, cdm, configuration, subtests, print_emulation):
    logging.debug("Get expected mediaSizes from metadata")
    expected_mediaSizes = get_supported_mediasizes_from_metadata(cdm,configuration)
    expected_mediaSizes.remove('any') # Note: Any Size is not supported in copy paper sizes list.

    if print_emulation.engine_make == DuneEngineMake.canonHomepro.name:
        # A5-R paper size is not supported in copy paper size for canon ProA4 products.
        if "com.hp.ext.mediaSize.iso_a5_148x210mm.rotated" in expected_mediaSizes:
            expected_mediaSizes.remove("com.hp.ext.mediaSize.iso_a5_148x210mm.rotated")
    # Media Size "jpn_photo-l_89x127mm" is same as "oe_photo-l_3.5x5in" and FW report only "oe_photo-l_3.5x5in" for Flowers.
    if configuration.productname.strip() in ["lotus"]:
        if "iso_c6_114x162mm" in expected_mediaSizes:
            # C6 paper size is not supported in copy paper size for Lotus
            expected_mediaSizes.remove("iso_c6_114x162mm")

    expected_copy_ui_mediaSizes = []
    for size in expected_mediaSizes:
        expected_copy_ui_mediaSizes.append(spice.copy_ui().metadata_to_ui_media_sizes_map[size]['ui'])
    expected_copy_ui_mediaSizes.sort()

    logging.debug("Navigate to Copy -->PaperSelection -->Paper Size list and make sure expected mediaSizes are reported in Copy PaperSize list")
    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().go_to_paper_selection()
    logging.debug(expected_copy_ui_mediaSizes)
    for size in expected_copy_ui_mediaSizes:
        with subtests.test("Testing Copy UI Paper {0} Size".format(size)):
            result = spice.copy_ui().is_paper_size_option_available(size)
            assert True == result,"Failed to find {0} size option in Copy -->PaperSelection -->Paper Size list".format(size)
        spice.copy_ui().go_back_to_setting_from_paper_selection()

    spice.copy_ui().go_back_to_setting_from_paper_selection()
    spice.copy_ui().back_to_landing_view()
    spice.goto_homescreen()
