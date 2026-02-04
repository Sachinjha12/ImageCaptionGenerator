import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify ADF load toast message chevron button
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-107039
    +timeout: 120
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_scan_ui_adf_toast_message_chevron_button
    +test:
        +title: test_scan_ui_adf_toast_message_chevron_button
        +guid:f720a7a3-7da9-47c6-b498-6ebf7ed576dc
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & ScannerInput=AutomaticDocumentFeeder 
           
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_scan_ui_adf_toast_message_chevron_button(spice, udw):

    # Go to HomeScreen
    spice.goto_homescreen()
    
    # Load Doucument in ADF
    udw.mainApp.ScanMedia.loadMedia("ADF")

    current_button = spice.wait_for("#toastHideButton")
    assert current_button

    # Click on Chevron button
    current_button.mouse_click()

