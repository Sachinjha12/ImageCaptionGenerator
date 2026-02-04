"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify ticket settings are set on A4 to Letter scale UI setting
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-97261
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:1
    +name:test_copy_ui_select_a4_to_letter
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_select_a4_to_letter
        +guid:7451e7da-cda3-4ebd-a13f-e7d7379daef1
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceClass=MFP & ScannerInput=AutomaticDocumentFeeder & CopyOutputScale=A4toLetter

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_select_a4_to_letter(udw, spice, cdm):
    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().goto_copy_option_output_scale()
        spice.wait_for("#copyResizeView")

        udwOutput = udw.mainApp.execute("JobTicketResourceManager PUB_getAllJobTicketIDs")
        udwEntries = udwOutput.split("\n")
        assert len(udwEntries) >= 3, "Behavior is undefined for more than 1 job ticket returned from JobTicketResourceManager PUB_getAllJobTicketIDs"

        # In SSQ we can have previous job ticket not deleted, so we need to get the last job ticket
        jobTicketId = udwEntries[-1]
        
        currentTicketEndpoint = cdm.JOB_TICKET_ENDPOINT  + "/" + jobTicketId
        spice.copy_ui().select_resize_option("None")
        jobTicketOnNone = cdm.get(currentTicketEndpoint)

        assert jobTicketOnNone["pipelineOptions"]["scaling"]["xScalePercent"] == 100, "Job ticket set to no scaling should have 100 percent scaling"
        assert jobTicketOnNone["pipelineOptions"]["scaling"]["yScalePercent"] == 100, "Job ticket set to no scaling should have 100 percent scaling"
        assert jobTicketOnNone["pipelineOptions"]["scaling"]["scaleSelection"] == "none", "Job ticket set to no scaling should have the scaleSelection set to 'none'"

        spice.copy_ui().select_resize_option("A4 to Letter(91%)")
        jobTicketOnA4ToLetter = cdm.get(currentTicketEndpoint)

        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["xScalePercent"] == 91, "Job ticket set to A4 to Letter should have 91 percent scaling"
        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["yScalePercent"] == 91, "Job ticket set to A4 to Letter should have 91 percent scaling"
        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["scaleSelection"] == "a4ToLetter", "Job ticket set to A4 to Letter should have the scaleSelection set to 'a4ToLetter'"

        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()