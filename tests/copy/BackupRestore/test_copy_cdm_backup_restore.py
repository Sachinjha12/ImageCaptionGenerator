import logging
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to test basic operations of Copy Backup Restore 
    +test_tier: 2
    +is_manual: False
    +reqid: DUNE-151499
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_cdm_backup_restore_settings
    +test:
        +title:test_copy_cdm_backup_restore_settings
        +guid: ccfa93a8-f5f2-4c1c-9a27-58a7b25f960c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP  & ScannerInput=Flatbed & Maintenance=BackUpRestore
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:120
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test Steps :
# 1. Get Default settings
# 2. Change default job ticket.
# 3. Keep the changes values before back up
# 4. Take a backup
# 5. After backup do more chnages to the ticket
# 6. Restore the setting back
# 7. Validate the settings are matching with 3)
# 8. cleanup, change the default to the same as step1, beginning of the test.

def test_copy_cdm_backup_restore_settings(cdm, net, ews,udw):
    # 1. Get Default settings

    ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_default_response.status_code < 300
    ticket_default_body_at_start = ticket_default_response.json()
    color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
    
    # 2. Change default job ticket.
    new_dest_print_copies = 3 
    new_src_scan_colorMode = "grayscale"
    new_src_scan_mediaSource = "flatbed"
    new_src_scan_mediaSize = "iso_a4_210x297mm"
    new_pipelineOptions_imageModifications_pagesPerSheet = "twoUp"
    
    ticket_new_default_values_body = {
        'src': {
		    'scan': {
                'mediaSource': new_src_scan_mediaSource, 
		    	'mediaSize': new_src_scan_mediaSize
            } 
        },
        'pipelineOptions': {
            'imageModifications': {
                'pagesPerSheet': new_pipelineOptions_imageModifications_pagesPerSheet
            }
        },
        'dest': {
            'print': {
                'copies': new_dest_print_copies
            },
        }
    }
    if color_supported:
        ticket_new_default_values_body['src']['scan']['colorMode'] = new_src_scan_colorMode
    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, ticket_new_default_values_body)
    assert put_response.status_code < 300  
    ticket_response_after_update1 = cdm.get_raw(cdm.JOB_TICKET_COPY) 
    assert ticket_response_after_update1.status_code < 300
    ticket_body_after_update1 = ticket_response_after_update1.json()

    # 3. Keep the changes values before back up
    dest_copy_copies_before_backup = ticket_body_after_update1["dest"]["print"]["copies"]
    src_scan_colormode_before_backup = ticket_body_after_update1["src"]["scan"]["colorMode"]
    src_scan_mediasource_before_backup = ticket_body_after_update1["src"]["scan"]["mediaSource"]
    src_scan_mediasize_before_backup = ticket_body_after_update1["src"]["scan"]["mediaSize"]
    pipelineOptions_imageModifications_pagesPerSheet_before_backup = ticket_body_after_update1["pipelineOptions"]["imageModifications"]["pagesPerSheet"]
    
    # 4. Take a backup
    cdm.backup_restore.backup_data(udw)

    # 5. After backup do more chnages to the ticket
    ticket_default_response_after_backup = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_default_response_after_backup.status_code < 300
    ticket_default_body_after_backup = ticket_default_response_after_backup.json() 

    value_dest_copies                   = 5 
    if cdm.device_feature_cdm.is_color_supported():        
        value_src_colormode             = "color"
    else:
        value_src_colormode             = "grayscale"
    value_src_mediaSource               = "adf"
    value_src_mediaSize                 = "na_legal_8.5x14in"
    value_pipelineOptions_pagesPerSheet = "oneUp"

    ticket_update_body_after_backup = {
        'src': {
		    'scan': {
                'colorMode': value_src_colormode, 
	    		'mediaSource': value_src_mediaSource, 
		    	'mediaSize': value_src_mediaSize
            } 
        },
        'pipelineOptions': {
            'imageModifications': {
                'pagesPerSheet': value_pipelineOptions_pagesPerSheet
            }
        },
        'dest': {
            'print': {
                'copies': value_dest_copies
            },
        }
    }

    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, ticket_update_body_after_backup)
    assert put_response.status_code < 300
    ticket_update_after_backup_response = cdm.get_raw(cdm.JOB_TICKET_COPY) 
    ticket_update_after_backup_body = ticket_update_after_backup_response.json()

    updated_copies_before_restore = ticket_update_after_backup_body["dest"]["print"]["copies"]

    # 6. Restore the setting back
    cdm.backup_restore.restore_data()

    
    ticket_after_restore_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_after_restore_response.status_code < 300
    ticket_after_restore_body = ticket_after_restore_response.json()
    
    dest_copy_copies_after_restore = ticket_after_restore_body["dest"]["print"]["copies"]
    src_scan_colormode_after_restore = ticket_after_restore_body["src"]["scan"]["colorMode"]
    src_scan_mediasource_after_restore = ticket_after_restore_body["src"]["scan"]["mediaSource"]
    src_scan_mediasize_after_restore = ticket_after_restore_body["src"]["scan"]["mediaSize"]
    pipelineOptions_imageModifications_pagesPerSheet_after_restore = ticket_after_restore_body["pipelineOptions"]["imageModifications"]["pagesPerSheet"]

    
    # 7. Validate the settings are matching with values before backup.
    assert dest_copy_copies_after_restore == dest_copy_copies_before_backup
    assert src_scan_colormode_after_restore == src_scan_colormode_before_backup
    assert src_scan_mediasource_after_restore == src_scan_mediasource_before_backup
    assert src_scan_mediasize_after_restore == src_scan_mediasize_before_backup
    assert pipelineOptions_imageModifications_pagesPerSheet_after_restore == pipelineOptions_imageModifications_pagesPerSheet_before_backup


    # 8. Cleanup, change the default to the same as step1, beginning of the test.
    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, ticket_default_body_at_start)
    assert put_response.status_code < 300


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to test basic operations of Copy config Backup Restore 
    +test_tier: 2
    +is_manual: False
    +reqid: DUNE-176799
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_config_cdm_backup_restore_settings
    +test:
        +title:test_copy_config_cdm_backup_restore_settings
        +guid: 96ac1361-1143-4454-bd86-07ad274798c7
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP & Copy=GrayScale & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:120
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Test Steps :
# 1. Get Default config settings
# 2. Change default config.
# 3. Keep the changes values before back up
# 4. Take a backup
# 5. After backup do more chnages to the config
# 6. Restore the setting back
# 7. Validate the settings are matching with 3)
# 8. cleanup, change the default to the same as step1, beginning of the test.
def test_copy_config_cdm_backup_restore_settings(cdm, net, udw):
    # 1. Get Default settings
    default_copy_config_response = cdm.get_raw(cdm.COPY_CONFIGURATION_ENDPOINT)
    assert default_copy_config_response.status_code < 300
    default_copy_config_at_start = default_copy_config_response.json()
    
    # 2. Change default copy config.
    config_new_values_body = {
        'copyEnabled': False,
        'colorCopyEnabled': False
    }
    put_response = cdm.put_raw(cdm.COPY_CONFIGURATION_ENDPOINT, config_new_values_body)
    assert put_response.status_code < 300  
    copy_config_after_update1 = cdm.get_raw(cdm.COPY_CONFIGURATION_ENDPOINT) 
    assert copy_config_after_update1.status_code < 300
    copy_config_after_update1 = copy_config_after_update1.json()
    
    # 3. Keep the changes values before back up
    copy_enable_before_backup = copy_config_after_update1["copyEnabled"]
    color_copy_enable_before_backup = copy_config_after_update1["colorCopyEnabled"]
    
    # 4. Take a backup
    cdm.backup_restore.backup_data(udw)
    
    # 5. After backup do more changes to the copy config
    put_response = cdm.put_raw(cdm.COPY_CONFIGURATION_ENDPOINT, {'copyEnabled': True, 'colorCopyEnabled': True})
    assert put_response.status_code < 300
    
    # 6. Restore the setting back
    cdm.backup_restore.restore_data()
    
    # 7. Validate the settings are matching with values before backup
    copy_config_after_restore_response = cdm.get_raw(cdm.COPY_CONFIGURATION_ENDPOINT)
    assert copy_config_after_restore_response.status_code < 300
    copy_config_after_restore_body = copy_config_after_restore_response.json()
    
    copy_enable_after_restore = copy_config_after_restore_body["copyEnabled"]
    color_copy_enable_after_restore = copy_config_after_restore_body["colorCopyEnabled"]
    
    assert copy_enable_after_restore == copy_enable_before_backup
    assert color_copy_enable_after_restore == color_copy_enable_before_backup

    # 8. Cleanup, change the default to the same as step1, beginning of the test.
    put_response = cdm.put_raw(cdm.COPY_CONFIGURATION_ENDPOINT, default_copy_config_at_start)
    assert put_response.status_code < 300
    
