from copy_quicksets_jupiter import COPYquicksets
from dunetuf.cdm.CdmShortcuts import CDMShortcuts

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy quicksets for jupiter
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-92515
    +timeout:240
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_validate_number_of_copy_qs_by_CDM
    +test:
        +title: test_validate_number_of_copy_qs_by_CDM
        +guid:f647759a-2471-11ed-ac25-6bfc813a86fc
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_validate_number_of_copy_qs_by_CDM(cdm, net, configuration):
    if configuration.productname == "jupiter":
        # Expected shortcuts and quicksets for jupiter
        cp_qsets = COPYquicksets()
        cdms = CDMShortcuts(cdm, net)
        copy_source = cdms.ShortcutSource.SCAN.value
        copy_destination = cdms.ShortcutDestination.PRINT.value

        # Current shortcuts
        cp_shortcut_expected = cdms.get_current_shortcuts_set_raw_data_by_type_CDM(copy_source, copy_destination)
        current_shortcuts = {}

        # Get ticket relevant data for current shortcuts 
        for shortcut in cp_shortcut_expected:
            ticket = cp_qsets.get_shortcut_ticket(cdm, net, shortcut)
            ticket_id = ticket ['ticketId']
            # Currently there is a problem with some fields in the ticked referenced in the shortcut
            # One workarround is to clone it and use that cloned ticket (with those available fields )
            new_ticket_user_body = cp_qsets.clone_ticket(cdm, ticket_id)
            shortcut_title = shortcut['title']
            shortcut_id = shortcut['id']
            relevant_shortcut_data = cp_qsets.extract_ticket_relevant_data(shortcut_id,new_ticket_user_body,cp_qsets)
            current_shortcuts[shortcut_title]= relevant_shortcut_data
            
        print("\n Current shortcuts data: \n", current_shortcuts)
        # Expected reference shortcuts quicksets (relevant data)
        expected_shortcuts = cp_qsets.get_expected_copy_shortcuts_quicksets()
        print("\n Expected shortcuts data: \n", expected_shortcuts)

        # Check that we have the expected number of quicksets
        assert len(expected_shortcuts) == len(current_shortcuts), f"The current number of quicksets differs from expected."
        
        # For each shortcut we check the relevant quickset data
        for expected_shortcut_title, expected_quickset_data in expected_shortcuts.items():
            # Check title on current shortcut
            assert current_shortcuts[expected_shortcut_title], f"The current shortcut title: {expected_shortcut_title} differs from expected."
        
            # Get quickset data from current shortcut
            current_quickset_data = current_shortcuts[expected_shortcut_title] 
        
            # For each ticket field check that we get the expected value
            for ticket_field, ticket_value in expected_quickset_data.items():
                assert current_quickset_data[ticket_field] == ticket_value, f"The current shortcut: {expected_shortcut_title}, field: {ticket_field} differs from expected."
