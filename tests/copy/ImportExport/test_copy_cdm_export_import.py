import logging
import time
import json
import pytest
import uuid

from dunetuf.copy.copy import *
from tests.copy import CopyBasicQuicksetHelper

def do_export_operations(udwExportImport, operationType, contentId, exportedFileKey="dummykey", exportCategories = "CopySettings"):
    if "BACKUP_RESTORE" == operationType:
        supported = udwExportImport.backupRestoreSupportedForTest()
        if 0 == supported:
            pytest.skip("Skip backup and restore test case because it's not supported")
        elif 0 > supported:
            pytest.skip("Skip backup and restore test case because it's unknown to support backup/restore")

    
    exportedFilePath = "/tmp/exportimport_test_export"
    # exportCategories = r'CopySettings'

    result = udwExportImport.doExport(operationType, exportCategories, exportedFilePath, exportedFileKey)
    print(" DoExport done:{}".format(result))
    if isinstance(result, str):
        assert result.isdigit(), "fail to doExport:{}".format(result)
        result = int(result)

    if result == 10 and "BACKUP_RESTORE" == operationType:
        pytest.skip("Skip backup and restore test case because system key is not provided")

    assert result < 4, "fail to doExport:{}".format(result)
    progress = 0
    for i in range(5):
        progress = udwExportImport.progress()

        assert progress <= 100, "invalid progress at {}".format(i)

        if progress == 100:
            break

        print("  doExport progress:{}:{}".format(i,progress))
        time.sleep(0.3)
    assert progress == 100, "timeout before doExport:"

def do_import_operations(udwExportImport, operationType, contentId, exportedFileKey="dummykey", exportCategories = "CopySettings"):

    exportedFilePath = "/tmp/exportimport_test_export"
    # exportCategories = r'CopySettings'
    result = udwExportImport.previewImportFile(exportedFilePath, exportedFileKey)
    print(" PreviewImportFile done:{}".format(len(result)))
    # categoryId = r'CopySettings'

    if isinstance(result, str) and result.isdigit():
        assert False, "fail to previewImportFile:{}".format(result)
    else:
        previewInfo = json.loads(result)
        assert previewInfo["identification"] != None, "identification not found"
        assert len(previewInfo["identification"]["uuid"]) > 0, "length of deviceUuid is zero"
        assert len(previewInfo["identification"]["serialNumber"]) > 0, "length of serialNumber is zero"
        assert len(previewInfo["identification"]["base"]) >= 0, "length of base is zero"
        assert len(previewInfo["identification"]["model"]) > 0, "length of model is zero"
        assert len(previewInfo["identification"]["append"]) >= 0, "length of append is zero"
        assert len(previewInfo["identification"]["family"]) > 0, "length of family is zero"
        assert len(previewInfo["identification"]["fwVersion"]) > 0, "length of fwVersion is zero"
        assert len(previewInfo["identification"]["dateTime"]) > 0, "length of dateTime is zero"
        assert previewInfo["identification"]["sameUuid"] == True, "sameUuid is wrong"
        assert previewInfo["identification"]["sameSerialNumber"] == True, "sameSerialNumber is wrong"
        assert previewInfo["identification"]["sameModel"] == True, "sameModel is wrong"
        assert previewInfo["identification"]["sameFamily"] == True, "sameFamily is wrong"
        assert previewInfo["identification"]["sameFwVersion"] == True, "sameFwVersion is wrong"
        assert previewInfo["importType"] == operationType, "importType is wrong"
        # assert previewInfo["categories"] == categoryId, "categories is wrong"

    fileInfoBeforeImport = udwExportImport.getFileInfoForTest(contentId)

    
    result = udwExportImport.doImport(operationType, exportCategories, exportedFilePath, exportedFileKey)
    print(" DoImport done:{}".format(result))
    if isinstance(result, str):
        assert result.isdigit(), "fail to doImport:{}".format(result)
        result = int(result)

    assert result < 4, "fail to doImport:{}".format(result)
    progress = 0
    for i in range(5):
        progress = udwExportImport.progress()

        assert progress <= 100, "invalid progress at {}".format(i)

        if progress == 100:
            break

        print("  doImport progress:{}:{}".format(i,progress))
        time.sleep(0.3)
    assert progress == 100, "timeout before doImport:"




"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to test basic operations of Copy Export Import 
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
    +name:test_copy_cdm_export_import_settings
    +test:
        +title:test_copy_cdm_export_import_settings
        +guid: 5c79e4a7-939d-4c83-b95e-2dccaf3a3508
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP  & ScannerInput=Flatbed & Maintenance=ImportExport
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test Steps :
# 1. Get Default settings
# 2. Change default job ticket.
# 3. Keep the changes values before back up
# 4. export setting
# 5. After export do more chnages to the ticket
# 6. import the setting back
# 7. Validate the settings are matching with 3)
# 8. cleanup, change the default to the same as step1, beginning of the test.

def test_copy_cdm_export_import_settings(cdm, net, ews,udw):
    # 1. Get Default settings

    ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_default_response.status_code < 300
    ticket_default_body_at_start = ticket_default_response.json()
    
    # 2. Change default job ticket.
    new_dest_print_copies = 3 
    new_src_scan_colorMode = "grayscale"
    new_src_scan_mediaSource = "flatbed"
    new_src_scan_mediaSize = "iso_a4_210x297mm"
    new_pipelineOptions_imageModifications_pagesPerSheet = "twoUp"
    new_media_source = "tray-1"
    new_output_plex_mode = "duplex"
    new_print_quality = "normal"
    color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
    
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
                    'copies': new_dest_print_copies,
                    'mediaSource': new_media_source,
                    'plexMode':new_output_plex_mode,
                    'printQuality' : new_print_quality
                }
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
    dest_copy_copies_before_export = ticket_body_after_update1["dest"]["print"]["copies"]
    src_scan_colormode_before_export = ticket_body_after_update1["src"]["scan"]["colorMode"]
    src_scan_mediasource_before_export = ticket_body_after_update1["src"]["scan"]["mediaSource"]
    src_scan_mediasize_before_export = ticket_body_after_update1["src"]["scan"]["mediaSize"]
    pipelineOptions_imageModifications_pagesPerSheet_before_export = ticket_body_after_update1["pipelineOptions"]["imageModifications"]["pagesPerSheet"]
    dest_media_source_before_export = ticket_body_after_update1["dest"]["print"]["mediaSource"]
    dest_plex_mode_before_export = ticket_body_after_update1["dest"]["print"]["plexMode"]
    dest_print_quality_before_export = ticket_body_after_update1["dest"]["print"]["printQuality"]

    
    # 4. Export settings
    do_export_operations(udw.mainApp.ExportImportManager, "EXPORT_IMPORT", "CopySettings", "dummykey", "CopySettings")
    
    # 5. After export do more changes to the ticket
    ticket_default_response_after_export = cdm.get_raw(cdm.JOB_TICKET_COPY)
    assert ticket_default_response_after_export.status_code < 300
    ticket_default_body_after_export = ticket_default_response_after_export.json() 

    new_dest_print_copies = 2
    new_src_scan_colorMode = "color"
    new_src_scan_mediaSource = "adf"
    new_src_scan_mediaSize = "na_letter_8.5x11in"
    new_pipelineOptions_imageModifications_pagesPerSheet = "oneUp"
    new_media_source = "tray-2"
    new_output_plex_mode = "simplex"
    new_print_quality = "best"
    
    ticket_update_body_after_export = {
         'src': {
		    'scan': {
                'colorMode': new_src_scan_colorMode, 
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
                    'copies': new_dest_print_copies,
                    'mediaSource': new_media_source,
                    'plexMode':new_output_plex_mode,
                    'printQuality' : new_print_quality
                }
        }
    }

    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, ticket_update_body_after_export)
    assert put_response.status_code < 300
    ticket_update_after_export_response = cdm.get_raw(cdm.JOB_TICKET_COPY) 
    ticket_update_after_export_body = ticket_update_after_export_response.json()

    # 6. import the setting back
    do_import_operations(udw.mainApp.ExportImportManager, "EXPORT_IMPORT", "CopySettings")
    
    ticket_after_import_response = cdm.get_raw(cdm.JOB_TICKET_COPY) 
    assert ticket_after_import_response.status_code < 300
    ticket_after_import_body = ticket_after_import_response.json()
    
    dest_copy_copies_after_import = ticket_after_import_body["dest"]["print"]["copies"]
    src_scan_colormode_after_import = ticket_after_import_body["src"]["scan"]["colorMode"]
    src_scan_mediasource_after_import = ticket_after_import_body["src"]["scan"]["mediaSource"]
    src_scan_mediasize_after_import = ticket_after_import_body["src"]["scan"]["mediaSize"]
    pipelineOptions_imageModifications_pagesPerSheet_after_import = ticket_after_import_body["pipelineOptions"]["imageModifications"]["pagesPerSheet"]
    dest_media_source_after_import = ticket_body_after_update1["dest"]["print"]["mediaSource"]
    dest_media_source_after_import = ticket_body_after_update1["dest"]["print"]["mediaSource"]
    dest_plex_mode_after_import = ticket_body_after_update1["dest"]["print"]["plexMode"]
    dest_print_quality_after_import = ticket_body_after_update1["dest"]["print"]["printQuality"]


    
    # 7. Validate the settings are matching with values before export.
    assert dest_copy_copies_after_import == dest_copy_copies_before_export
    assert src_scan_colormode_after_import == src_scan_colormode_before_export
    assert src_scan_mediasource_after_import == src_scan_mediasource_before_export
    assert src_scan_mediasize_after_import == src_scan_mediasize_before_export
    assert pipelineOptions_imageModifications_pagesPerSheet_after_import == pipelineOptions_imageModifications_pagesPerSheet_before_export
    assert dest_media_source_after_import == dest_media_source_before_export
    assert dest_plex_mode_after_import == dest_plex_mode_before_export
    assert dest_print_quality_after_import == dest_print_quality_before_export


    # 8. Cleanup, change the default to the same as step1, beginning of the test.
    put_response = cdm.put_raw(cdm.JOB_TICKET_COPY, ticket_default_body_at_start)
    assert put_response.status_code < 300

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to test basic operations of Copy Export Import 
    +test_tier: 2
    +is_manual: False
    +reqid: DUNE-190031
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_cdm_export_import_settings
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_cdm_export_import_settings
        +guid: d14ee837-b195-41e7-a2a4-0d35665152c5
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP & ScannerInput=Flatbed & Maintenance=ImportExport
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test Steps :
# 1. Create a custom shortcut
# 2. Do export
# 3. Delete the shortcut
# 4. Do import
# 5. Validate the shortcut is restored
# 6. Cleanup, delete the shortcut created in step 1
def test_copy_quickset_cdm_export_import_settings(scan_emulation, cdm, udw, spice, net, job):

    try:
        # 1. Create a custom shortcut
        settings = {
            'inputMediaSize': 'na_letter_8.5x11in',
            'copies': 20,
            'pagesPerSheet': 'oneUp',
            'contentType': 'text',
            'outputScale': 'fitToPage'
            }
        # CopyBasicQuicksetHelper.create_custom_shortcut(scan_emulation, cdm, udw, spice, net, job, "MyCopy", settings)
        shortcut_id = str(uuid.uuid4())
        CopyBasicQuicksetHelper.create_custom_shortcut(cdm, net, "MyCopy", shortcut_id)
        # CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)

        # 2. Do export
        do_export_operations(udw.mainApp.ExportImportManager, "EXPORT_IMPORT", "QuickSets", "dummykey", "QuickSets")

        # 3. Delete the shortcut
        CopyBasicQuicksetHelper.delete_custom_shortcut(cdm, net, shortcut_id)

        # 4. Do import
        do_import_operations(udw.mainApp.ExportImportManager, "EXPORT_IMPORT", "QuickSets", "dummykey", "QuickSets")

        # 5. Validate the shortcut is restored
        shortcut_id = CopyBasicQuicksetHelper.validate_custom_shortcut(cdm, net, "MyCopy")

        assert shortcut_id != 0 , "Shortcut not restored after import"

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#" + shortcut_id)
    finally:
        # 6. Cleanup, delete the shortcut
        CopyBasicQuicksetHelper.delete_all_shortcuts(cdm, net)
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: to test basic operations of Copy Export Import 
    +test_tier: 2
    +is_manual: False
    +reqid: DUNE-190031
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_cdm_backup_restore_settings
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_cdm_backup_restore_settings
        +guid: 2698c796-d1bc-4f1e-ad2c-5f021d86d9ae
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & DeviceClass=MFP  & ScannerInput=Flatbed & Maintenance=BackUpRestore
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Test Steps :
# 1. Create a custom shortcut
# 2. Do export
# 3. Delete the shortcut
# 4. Do import
# 5. Validate the shortcut is restored
# 6. Cleanup, delete the shortcut created in step 1
def test_copy_quickset_cdm_backup_restore_settings(scan_emulation, cdm, udw, spice, net, job):
    try:
        # 1. Create a custom shortcut
        settings = {
            'inputMediaSize': 'na_letter_8.5x11in',
            'copies': 20,
            'pagesPerSheet': 'oneUp',
            'contentType': 'text',
            'outputScale': 'fitToPage'
            }
        # CopyBasicQuicksetHelper.create_custom_shortcut(scan_emulation, cdm, udw, spice, net, job, "MyCopy", settings)
        shortcut_id = str(uuid.uuid4())
        CopyBasicQuicksetHelper.create_custom_shortcut(cdm, net, "MyCopy", shortcut_id)
        # CopyBasicQuicksetHelper.perform_copy_job_through_quickset(scan_emulation,cdm, udw, spice, net, job, "MyCopy", settings)

        # 2. Do export
        do_export_operations(udw.mainApp.ExportImportManager, "BACKUP_RESTORE", "QuickSets", "dummykey", "QuickSets")

        # 3. Delete the shortcut
        CopyBasicQuicksetHelper.delete_custom_shortcut(cdm, net, shortcut_id)

        # 4. Do import
        do_import_operations(udw.mainApp.ExportImportManager, "BACKUP_RESTORE", "QuickSets", "dummykey", "QuickSets")

        # 5. Validate the shortcut is restored
        shortcut_id = CopyBasicQuicksetHelper.validate_custom_shortcut(cdm, net, "MyCopy")

        assert shortcut_id != 0 , "Shortcut not restored after import"

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#" + shortcut_id)

    finally:
    
        # 6. Cleanup, delete the shortcut
        CopyBasicQuicksetHelper.delete_custom_shortcut(cdm, net, shortcut_id)
        spice.goto_homescreen()
        spice.wait_ready()